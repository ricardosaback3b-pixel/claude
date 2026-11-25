"""Sobreposições da REFERÊNCIA VIRAL 25/11 (alerta + POV), desenhadas com PIL, sem mexer no motor.

Uso (renderiza igual ao render_part.py, com as sobreposições ligadas):
  python3 tools/sobreposicoes.py <slug> <n>

O que dá para pôr no roteiro (tudo opcional; sem esses campos o vídeo sai igual ao render_part.py):
  script.banner = {"remetente": "SIRENE DA CIDADE · 17:59", "titulo": "FALTAM 60 SEGUNDOS",
                   "instrucao": "Entre em casa. Não olhe pra cima.", "cor": [200, 20, 40]}
      -> R1: banner de alerta no terço de cima da cena 1, desde 0,0 s (entra no lugar do gancho_tela).
         Alerta ficcional da própria história: nunca imite marca, app ou órgão real.
  cena.etiquetas = [{"texto": "PONTEIRO · 10 s", "x": 260, "y": 900, "cor": [200, 20, 40]}]
      -> R5: etiqueta com número sobre o lugar (x, y em pixels do fundo, 1231x2188; acompanha a câmera).
  script.cartao_escolha = {"a": "ESCADA · 40 degraus", "b": "JANELA · 3 m"}
      -> R5: cartão final "O QUE VOCÊ FARIA?" com botão A vermelho, B azul e "Comenta aqui embaixo ↓"
         no lugar da tela final (o vídeo termina ali).
  cena.cam = "shake" / "zoom_tremido" já fazem o tremor (R3) no motor.
Funções soltas (banner_img, etiqueta_img, cartao_escolha_img) também servem para cartazes.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [ROOT, os.path.join(ROOT, "tools")]
import engine  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

W, H = engine.W, engine.H
_meta_atual = {}
_cache = {}


def _f(path, size, bold=False):
    return engine.font(path, size, bold)


def banner_img(remetente, titulo, instrucao="", cor=(200, 20, 40)):
    """Banner de notificação/alerta no terço de cima (camada W x H transparente)."""
    key = ("banner", remetente, titulo, instrucao, tuple(cor))
    if key in _cache:
        return _cache[key]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x0, x1, y0 = 50, W - 50, 250
    ft = _f(engine.ANTON, 118)
    linhas = engine.wrap(titulo.upper(), ft, x1 - x0 - 90)
    while len(linhas) > 2 and ft.size > 80:
        ft = _f(engine.ANTON, ft.size - 8)
        linhas = engine.wrap(titulo.upper(), ft, x1 - x0 - 90)
    fi = _f(engine.MONT, 44, True)
    inst = engine.wrap(instrucao, fi, x1 - x0 - 90) if instrucao else []
    h = 110 + len(linhas) * int(ft.size * 1.05) + len(inst) * 56 + 62
    # sombra
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x0 + 6, y0 + 14, x1 + 6, y0 + h + 14], 46, fill=(0, 0, 0, 170))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([x0, y0, x1, y0 + h], 46, fill=(250, 248, 244, 248), outline=tuple(cor), width=8)
    d.rounded_rectangle([x0, y0, x1, y0 + 92], 46, fill=tuple(cor))
    d.rectangle([x0, y0 + 50, x1, y0 + 92], fill=tuple(cor))
    # ícone de alerta (triângulo) + remetente
    tx = x0 + 50
    d.polygon([(tx, y0 + 70), (tx + 26, y0 + 22), (tx + 52, y0 + 70)], fill=(255, 255, 255))
    d.text((tx + 26, y0 + 58), "!", font=_f(engine.ANTON, 36), fill=tuple(cor), anchor="mm")
    fr = _f(engine.MONT, 36, True)
    d.text((tx + 72, y0 + 46), remetente.upper(), font=fr, fill=(255, 255, 255), anchor="lm")
    d.text((x1 - 40, y0 + 46), "agora", font=_f(engine.MONT, 32), fill=(255, 235, 235), anchor="rm")
    y = y0 + 110 + ft.size * 0.5
    for ln in linhas:
        d.text((x0 + 45, y), ln, font=ft, fill=(20, 16, 16), anchor="lm")
        y += ft.size * 1.05
    y += 6
    for ln in inst:
        d.text((x0 + 45, y), ln, font=fi, fill=(70, 60, 60), anchor="lm")
        y += 56
    _cache[key] = lay
    return lay


def etiqueta_img(texto, cor=(200, 20, 40)):
    """Etiqueta com número (pílula com seta para baixo), para colar sobre o lugar."""
    f = _f(engine.ANTON, 64)
    tw = int(f.getlength(texto.upper()))
    w, h = tw + 70, 104
    im = Image.new("RGBA", (w, h + 34), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h], 30, fill=tuple(cor), outline=(255, 255, 255), width=6)
    d.polygon([(w / 2 - 24, h - 3), (w / 2 + 24, h - 3), (w / 2, h + 32)], fill=(255, 255, 255))
    d.polygon([(w / 2 - 15, h - 6), (w / 2 + 15, h - 6), (w / 2, h + 20)], fill=tuple(cor))
    d.text((w / 2, h / 2 + 2), texto.upper(), font=f, fill=(255, 255, 255), anchor="mm")
    return im


def cartao_escolha_img(a, b, pergunta="O QUE VOCÊ FARIA?"):
    """Cartão final de escolha: pergunta + botão A (vermelho) e B (azul) + 'Comenta aqui embaixo ↓'."""
    key = ("cartao", a, b, pergunta)
    if key in _cache:
        return _cache[key]
    im = engine.vgrad(W, H, (40, 8, 14), (8, 6, 20)).convert("RGBA")
    d = ImageDraw.Draw(im)
    fp = _f(engine.ANTON, 140)
    y = 520
    for ln in engine.wrap(pergunta, fp, W - 120):
        d.text((W / 2, y), ln, font=fp, fill=engine.YELLOW, anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
        y += 150
    y += 60
    fb = _f(engine.ANTON, 70)
    for lab, txt, cor in (("A", a, (210, 30, 40)), ("B", b, (30, 90, 210))):
        d.rounded_rectangle([90, y, W - 90, y + 190], 50, fill=cor, outline=(255, 255, 255), width=8)
        d.ellipse([125, y + 35, 245, y + 155], fill=(255, 255, 255))
        d.text((185, y + 97), lab, font=_f(engine.ANTON, 90), fill=cor, anchor="mm")
        ls = engine.wrap(txt.upper(), fb, W - 400)
        ty = y + 95 - (len(ls) - 1) * 38
        for ln in ls[:2]:
            d.text((275, ty), ln, font=fb, fill=(255, 255, 255), anchor="lm")
            ty += 76
        y += 230
    y += 40
    d.text((W / 2, y), "Comenta aqui embaixo ↓", font=_f(engine.MONT, 58, True), fill=(255, 255, 255), anchor="mm")
    d.text((W / 2, y + 90), engine.HANDLE, font=_f(engine.ANTON, 70), fill=engine.YELLOW, anchor="mm")
    _cache[key] = im
    return im


def instalar():
    """Liga as sobreposições no motor (só nesta execução; os arquivos do motor não mudam)."""
    import render_part
    if getattr(engine, "_sobreposicoes", False):
        return
    engine._sobreposicoes = True
    _resolve, _build, _gancho, _end, _render = (render_part.resolve, engine.build_scene, engine.gancho_img,
                                                 engine.end_card, engine.render)

    def resolve(story, part):
        data = _resolve(story, part)
        sc = part["script"]
        for k in ("banner", "cartao_escolha"):
            if sc.get(k):
                data["meta"][k] = sc[k]
        if sc.get("banner") and not data["meta"].get("gancho_tela"):
            data["meta"]["gancho_tela"] = sc["banner"].get("titulo", " ")  # liga o desenho na cena 1
        return data

    def build_scene(sc):
        img = _build(sc)
        if sc.get("etiquetas"):
            img = img.convert("RGBA")
            bw, bh = img.size
            for e in sc["etiquetas"]:
                et = etiqueta_img(e["texto"], tuple(e.get("cor", (200, 20, 40))))
                x = int(min(max(e.get("x", bw / 2) - et.width / 2, 20), bw - et.width - 20))
                y = int(min(max(e.get("y", bh / 3) - et.height, 20), bh - et.height - 20))
                img.alpha_composite(et, (x, y))
            img = img.convert("RGB")
        return img

    def gancho_img(texto):
        b = _meta_atual.get("banner")
        if b:
            return banner_img(b.get("remetente", "ALERTA"), b.get("titulo", texto), b.get("instrucao", ""),
                              tuple(b.get("cor", (200, 20, 40))))
        return _gancho(texto)

    def end_card(meta, base):
        c = meta.get("cartao_escolha")
        if c:
            return cartao_escolha_img(c["a"], c["b"], c.get("pergunta", "O QUE VOCÊ FARIA?")).convert("RGB")
        return _end(meta, base)

    def render(script, out_dir):
        _meta_atual.clear()
        _meta_atual.update(script["meta"])
        return _render(script, out_dir)

    render_part.resolve = resolve
    engine.build_scene = build_scene
    engine.gancho_img = gancho_img
    engine.end_card = end_card
    engine.render = render


if __name__ == "__main__":
    instalar()
    import render_part
    render_part.main(sys.argv[1], int(sys.argv[2]))
