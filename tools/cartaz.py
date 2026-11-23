"""Cartaz de story do @mundoemhistorias.

Uso (dentro do repositório):
  python3 tools/cartaz.py <slug> <n> embreve <saida.jpg> "23/11 · 8h52"
  python3 tools/cartaz.py <slug> <n> saiu <saida.jpg>
  python3 tools/cartaz.py <slug> <n> estreou <saida.jpg>

Base da imagem, nesta ordem (nunca inventa personagem nem nome):
  1. videos/<slug>/capa<n>.jpg (a capa real do vídeo), se existir;
  2. a cena de capa do roteiro da parte n em historia.json;
  3. a cena de capa da última parte com roteiro (mesmo fundo e mesmos personagens travados),
     com o nome da história e "PARTE n" e sem subtítulo;
  4. sem roteiro nenhum: fundo escuro + até 2 personagens travados (narrador primeiro).
Faixas: embreve = amarela "EM BREVE" + data · horário; saiu = amarela "PARTE N" / "JÁ NO CANAL!";
estreou = amarela "ESTREOU!".
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [ROOT, os.path.join(ROOT, "tools")]
import engine, render_part, sprites  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402


def _cena_capa(story, part, n):
    data = render_part.resolve(story, part)
    meta, scenes = data["meta"], data["scenes"]
    meta["part"] = n
    meta["final"] = n == 6
    sc = next((s for s in scenes if s.get("cover")), scenes[0])
    src = engine.build_scene(sc).copy()
    for c in [c for c in sc.get("chars", []) if c.get("sprite")]:
        spr = engine.draw_char(c, c.get("scale", 1.0))
        x = int(c.get("x", 0.5) * engine.BW - spr.width / 2)
        md = c.get("enquadramento") or sprites.enquadramento_padrao(c["sprite"])
        if md == "medio":
            y = int(engine.BH * c.get("y", 0.325))
        elif sprites.e_busto(c["sprite"], c.get("enquadramento")):
            y = int(engine.BH * c.get("y", 0.25))
        else:
            y = int((c.get("y", 0.86) - 0.07) * engine.BH - spr.height)
        src.paste(spr, (x, y), spr)
    return meta, engine.camera(src, sc.get("cam", "in"), 0.5)


def base(slug, n):
    capa = os.path.join(ROOT, "videos", slug, f"capa{n}.jpg")
    if os.path.exists(capa):
        return Image.open(capa).convert("RGBA"), "capa do vídeo"
    story = json.load(open(os.path.join(ROOT, "historias", slug, "historia.json")))
    render_part.checar_travas(story, slug)  # trava do dono: físico e voz nunca mudam
    partes =[p for p in story["partes"] if (p.get("script") or {}).get("scenes")]
    part = next((p for p in partes if p["n"] == n), None)
    origem = "roteiro da parte"
    if part is None:
        if partes:
            part = json.loads(json.dumps(max(partes, key=lambda p: p["n"])))
            part["script"]["cover_text"] = ""
            origem = f"cena de capa da parte {part['n']} (sem subtítulo)"
        else:  # séries antigas sem roteiro: fundo escuro + até 2 personagens travados (narrador primeiro)
            trav = story.get("personagens_travados") or story.get("personagens", {})
            refs = sorted(trav, key=lambda r: r != story.get("narrador"))[:2]
            xs = [0.5] if len(refs) == 1 else [0.28, 0.72]
            chars = [{"ref": r, "x": x, "eyes": "arregalado"} for r, x in zip(refs, xs)]
            part = {"n": n, "script": {"cover_text": "", "caption": "", "scenes": [
                {"bg": "escuro", "cover": True, "cam": "in", "chars": chars}]}}
            origem = "fundo escuro + personagens travados (história sem roteiro salvo)"
    meta, img = _cena_capa(story, part, n)
    tmp = f"/tmp/cartaz_{slug}_{n}.jpg"
    engine.make_cover(meta, img, tmp)
    return Image.open(tmp).convert("RGBA"), origem


def faixa(im, linhas, amarela):
    W, H = im.size
    d = ImageDraw.Draw(im)
    size = 190 if len(linhas) == 1 else 150
    f = engine.font(engine.ANTON, size)
    tw = min(W - 80, max(f.getlength(l) for l in linhas) + 120)
    lh = size * 1.08
    hgt = lh * len(linhas) + 70
    top = 1700 - hgt
    d.rounded_rectangle([W / 2 - tw / 2, top, W / 2 + tw / 2, top + hgt], 44,
                        fill=engine.YELLOW if amarela else (200, 20, 40), outline=(0, 0, 0), width=10)
    for i, l in enumerate(linhas):
        d.text((W / 2, top + 35 + lh * (i + 0.5)), l, font=f, fill=(0, 0, 0) if amarela else (255, 255, 255),
               anchor="mm", stroke_width=0 if amarela else 7, stroke_fill=(0, 0, 0))


def main():
    slug, n, modo, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    render_part.checar_travas(json.load(open(os.path.join(ROOT, "historias", slug, "historia.json"))), slug)
    im, origem = base(slug, n)
    if modo == "embreve":
        faixa(im, ["EM BREVE", sys.argv[5].upper()], True)
    elif modo == "saiu":
        faixa(im, [f"PARTE {n}", "JÁ NO CANAL!"], True)
    elif modo == "estreou":
        faixa(im, ["ESTREOU!"], True)
    else:
        sys.exit("modo deve ser embreve, saiu ou estreou")
    im.convert("RGB").save(out, quality=90)
    print(json.dumps({"cartaz": out, "base": origem}, ensure_ascii=False))


if __name__ == "__main__":
    main()
