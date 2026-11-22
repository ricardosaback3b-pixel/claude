"""Personagens da cartela do dono (assets/personagens/*.png) com expressões e boca animada.

O desenho original nunca muda: por cima do rosto só se desenham olhos (arregalado/fechado),
sobrancelhas e a boca (fechada, meio aberta, aberta, "o", triste, sorriso).
"""
import json, os
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
# estilo "cartela": corpo inteiro (assets/personagens); estilo "catalogo": busto (assets/catalogo)
DIRS = {"cartela": os.path.join(ROOT, "personagens"), "catalogo": os.path.join(ROOT, "catalogo")}
OUT = (22, 16, 20)


@lru_cache(None)
def _meta_dir(estilo):
    with open(os.path.join(DIRS[estilo], "rostos.json")) as f:
        return json.load(f)


def estilo_de(name):
    for est in ("cartela", "catalogo"):
        if name in _meta_dir(est):
            return est
    raise KeyError(f"personagem '{name}' não existe na cartela nem no catálogo")


def _meta():
    out = {}
    for est in DIRS:
        out.update(_meta_dir(est))
    return out


def lista(estilo=None):
    ests = [estilo] if estilo else list(DIRS)
    return sorted(k for e in ests for k, v in _meta_dir(e).items() if v)


def e_busto(name):
    return estilo_de(name) == "catalogo"


def _is_skinish(p):
    r, g, b, al = p
    return al > 0 and max(r, g, b) > 120 and not (min(r, g, b) > 228)


def _full_eye(a, box):
    """Olho inteiro = parte branca + pupila preta + contorno; varre a partir da parte branca até achar pele."""
    x0, y0, x1, y1 = box
    cy = int((y0 + y1) / 2)
    h, w = a.shape[:2]
    def scan(x, y, dx, dy):
        n = 0
        while 0 <= x < w and 0 <= y < h and n < 80:
            if _is_skinish(a[y, x]):
                return x, y
            x += dx; y += dy; n += 1
        return x, y
    L, _ = scan(int(x0), cy, -1, 0)
    R, _ = scan(int(x1) - 1, cy, 1, 0)
    cx = int((L + R) / 2)
    _, T = scan(cx, int(y0), 0, -1)
    _, B = scan(cx, int(y1) - 1, 0, 1)
    return [float(L), float(T), float(R), float(B)]


@lru_cache(None)
def _base(name):
    est = estilo_de(name)
    im = Image.open(os.path.join(DIRS[est], f"{name}.png")).convert("RGBA")
    m = dict(_meta_dir(est)[name])
    a = np.asarray(im).astype(int)
    m["olhos"] = [_full_eye(a, e) for e in m["olhos"]]
    (l0, t0, l1, b0), (r0, t1, r1, b1) = m["olhos"]
    eh = max(b0 - t0, b1 - t1)
    m["olho_h"] = eh
    ex0, ex1 = (l0 + l1) / 2, (r0 + r1) / 2
    dd = ex1 - ex0
    eb = max(b0, b1)
    # boca: traço escuro entre os olhos, um pouco abaixo deles
    if est == "catalogo":
        y0, y1 = int(eb + dd * 0.32), int(eb + dd * 0.98)
    else:
        y0, y1 = int(eb + eh * 0.05), int(eb + eh * 0.75)
    x0, x1 = int(ex0 + dd * 0.15), int(ex1 + dd * 0.05)
    reg = a[y0:y1, x0:x1]
    dark = (reg[..., :3].max(axis=2) < 110) & (reg[..., 3] > 0)
    if dark.sum() > 3:
        ys, xs = np.nonzero(dark)
        # fica com a maior concentração (ignora nariz isolado em cima): usa a linha mais baixa com tinta
        yb = np.percentile(ys, 60)
        sel = ys >= yb - eh * 0.12
        m["boca"] = [float(xs[sel].mean() + x0), float(ys[sel].mean() + y0)]
        m["boca_w"] = float(max(6, xs[sel].max() - xs[sel].min() + 2))
        if est == "catalogo":  # rosto de frente: boca no meio, altura = tinta perto do centro
            mid = (ex0 + ex1) / 2 - x0
            near = np.abs(xs - mid) < dd * 0.25
            if near.sum() > 2:
                # tinta grossa e escura em cima = bigode; boca fica logo abaixo dele
                yy = ys[near]
                rows = np.bincount(yy)
                thick = rows > max(3, dd * 0.25)
                if thick.sum() >= max(3, dd * 0.06):
                    m["bigode"] = True
                    m["boca"][1] = float(np.nonzero(thick)[0].max() + y0 + dd * 0.07)
                else:
                    from scipy import ndimage as _nd
                    ink = (reg[..., :3].max(axis=2) < 150) & (reg[..., 3] > 0)
                    ink[:, :max(0, int(mid - dd * 0.3))] = False
                    ink[:, int(mid + dd * 0.3):] = False
                    lb, nn = _nd.label(ink)
                    best = None
                    for sl_i, sl in enumerate(_nd.find_objects(lb)):
                        if sl is None:
                            continue
                        w_ = sl[1].stop - sl[1].start
                        if w_ > dd * 0.6 or sl[0].stop >= ink.shape[0] - 1 or w_ < 2:
                            continue
                        cyy = (sl[0].start + sl[0].stop) / 2
                        if best is None or cyy > best[0]:
                            best = (cyy, (sl[1].start + sl[1].stop) / 2)
                    if best:
                        m["boca"][1] = float(best[0] + y0)
            m["boca"][0] = float((ex0 + ex1) / 2)
            m["boca_w"] = float(max(m["boca_w"], dd * 0.5))
    else:
        m["boca"] = [ex0 + dd * 0.6, eb + eh * 0.4]
        m["boca_w"] = dd * 0.4
    bx, by = m["boca"]
    sk = a[int(by - eh * 0.35):int(by + eh * 0.35), int(bx - dd * 0.5):int(bx + dd * 0.5)]
    sk = sk[(sk[..., 3] > 0)]
    sk = sk[(sk[..., :3].max(axis=1) > 140) & (sk[..., :3].min(axis=1) < 235) & ((sk[..., 0] - sk[..., 2]) > 25)]
    m["busto"] = est == "catalogo"
    m["dd"] = dd
    m["pele"] = tuple(int(v) for v in np.median(sk[:, :3], axis=0)) if len(sk) else (240, 200, 170)
    return im, m


def render(name, altura, eyes="normal", mouth="idle", brows=None, flip=False):
    """Retorna RGBA com altura ~= altura px."""
    im, m = _base(name)
    k = altura / im.height
    big = im.resize((max(1, int(im.width * k)), int(altura)), Image.LANCZOS)
    big = big.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    base_alpha = big.split()[3]
    over = Image.new("RGBA", big.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    lw = max(3, int(2.2 * k))
    pele = m["pele"]
    (l0, t0, l1, b0), (r0, t1, r1, b1) = [[c * k for c in e] for e in m["olhos"]]
    eh = m["olho_h"] * k
    # olhos
    for (x0, y0, x1, y1) in ((l0, t0, l1, b0), (r0, t1, r1, b1)):
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rw, rh = (x1 - x0) / 2 + 2 * k, (y1 - y0) / 2 + 2 * k
        if eyes == "fechado":
            d.ellipse([cx - rw - lw, cy - rh - lw, cx + rw + lw, cy + rh + lw], fill=pele)
            d.arc([cx - rw, cy - rh * 0.3, cx + rw, cy + rh * 0.9], 200, 340, fill=OUT, width=lw)
        elif eyes == "arregalado":
            d.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=(255, 255, 255), outline=OUT, width=lw)
            pr = min(rw, rh) * 0.38
            d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=OUT)
            d.ellipse([cx - pr * 0.2, cy - pr * 0.7, cx + pr * 0.25, cy - pr * 0.25], fill=(255, 255, 255))
    # sobrancelhas
    if brows:
        for side, (x0, y0, x1, y1) in ((-1, (l0, t0, l1, b0)), (1, (r0, t1, r1, b1))):
            cx = (x0 + x1) / 2
            w = (x1 - x0) * 0.55
            by = y0 - eh * 0.12
            inner, outer = (cx + w, cx - w) if side < 0 else (cx - w, cx + w)
            dy = eh * 0.14
            if brows == "bravo":
                pts = [(outer, by - dy), (inner, by + dy)]
            elif brows == "preocupado":
                pts = [(outer, by + dy), (inner, by - dy)]
            elif brows == "surpreso":
                pts = [(outer, by - dy * 1.4), (inner, by - dy * 1.4)]
            else:
                pts = [(outer, by), (inner, by)]
            d.line(pts, fill=OUT, width=int(lw * 1.8))
    # boca
    if mouth != "idle":
        bx, by = m["boca"][0] * k, m["boca"][1] * k
        bw = max(m["boca_w"] * k, eh * 0.55)
        # apaga a boca original
        if m.get("busto"):
            dk = m["dd"] * k
            if m.get("bigode"):
                d.ellipse([bx - dk * 0.22, by - dk * 0.03, bx + dk * 0.22, by + dk * 0.12], fill=pele)
            else:
                d.ellipse([bx - dk * 0.36, by - dk * 0.15, bx + dk * 0.36, by + dk * 0.17], fill=pele)
            eh = dk * 0.55
        else:
            d.ellipse([bx - bw * 0.62, by - eh * 0.16, bx + bw * 0.62, by + eh * 0.2], fill=pele)
        mw = bw * 0.5
        if mouth == "fechada":
            d.arc([bx - mw, by - eh * 0.18, bx + mw, by + eh * 0.12], 20, 160, fill=OUT, width=lw)
        elif mouth == "sorriso":
            d.arc([bx - mw * 1.1, by - eh * 0.25, bx + mw * 1.1, by + eh * 0.2], 15, 165, fill=OUT, width=lw)
        elif mouth == "triste":
            d.arc([bx - mw, by - eh * 0.02, bx + mw, by + eh * 0.3], 200, 340, fill=OUT, width=lw)
        elif mouth in ("meia", "aberta", "o"):
            hh = {"meia": 0.12, "aberta": 0.24, "o": 0.22}[mouth]
            ww = mw * (0.55 if mouth == "o" else 0.85)
            box = [bx - ww, by - eh * hh * 0.6, bx + ww, by + eh * hh * 1.2]
            d.ellipse(box, fill=(120, 30, 40), outline=OUT, width=lw)
            if mouth == "aberta":
                d.chord([box[0] + lw, box[1] + (box[3] - box[1]) * 0.45, box[2] - lw, box[3] - lw], 0, 180, fill=(225, 100, 110))
    inner = base_alpha.filter(ImageFilter.MinFilter(max(3, (int(3 * k) // 2) * 2 + 1)))
    oa = np.minimum(np.asarray(over.split()[3]), np.asarray(inner))
    over.putalpha(Image.fromarray(oa.astype(np.uint8)))
    big.alpha_composite(over)
    if m.get("busto"):
        # o busto continua até a base da tela: estica a última linha (roupa) para baixo
        ext = int(big.height * 0.6)
        row = big.crop((0, big.height - 2, big.width, big.height - 1)).resize((big.width, ext))
        tall = Image.new("RGBA", (big.width, big.height + ext), (0, 0, 0, 0))
        tall.paste(big, (0, 0))
        tall.paste(row, (0, big.height - 1))
        big = tall
    if flip:
        big = big.transpose(Image.FLIP_LEFT_RIGHT)
    return big


if __name__ == "__main__":
    import sys
    nomes = sys.argv[1:] or ["protagonista", "prefeito", "policial"]
    estados = [("normal", "idle", None), ("normal", "aberta", None), ("normal", "meia", None),
               ("arregalado", "o", "surpreso"), ("normal", "triste", "preocupado"), ("normal", "fechada", "bravo"),
               ("fechado", "sorriso", None)]
    tiles = []
    for n in nomes:
        for e, mo, br in estados:
            im = render(n, 700, e, mo, br)
            w = im.width
            face = im.crop((0, 0, w, int(700 * (0.85 if e_busto(n) else 0.5))))
            tiles.append(face)
    tw = max(t.width for t in tiles); th = max(t.height for t in tiles)
    cols = len(estados)
    o = Image.new("RGB", (tw * cols, th * len(nomes)), (70, 80, 100))
    for i, t in enumerate(tiles):
        o.paste(t, ((i % cols) * tw, (i // cols) * th), t)
    o.thumbnail((2400, 2400))
    o.save("/tmp/expr.png")
    print("ok")
