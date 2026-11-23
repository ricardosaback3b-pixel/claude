"""Conferência visual obrigatória antes de publicar (regra do dono, 23/11).

Uso: python3 tools/conferir_video.py <slug> <n>
Gera duas imagens para OLHAR (com a ferramenta de ler imagem) antes de publicar:
  /tmp/conferir_<slug>_<n>_quadros.png  -> 1 quadro a cada 2,5 s do vídeo renderizado
  /tmp/conferir_<slug>_<n>_rostos.png   -> cada personagem da parte com todas as bocas (falando, triste, "o"...)
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from PIL import Image  # noqa: E402
import engine  # noqa: E402,F401  (carrega fontes/medidas usadas pelos sprites)
import sprites  # noqa: E402


def quadros(slug, n):
    mp4 = os.path.join(ROOT, "videos", slug, f"parte{n}.mp4")
    out = f"/tmp/conferir_{slug}_{n}_quadros.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf",
                    "fps=1/2.5,scale=270:480,tile=8x5", "-frames:v", "1", out], check=True)
    return out


def rostos(slug, n):
    with open(os.path.join(ROOT, "historias", slug, "historia.json")) as f:
        story = json.load(f)
    part = next(p for p in story["partes"] if p["n"] == n)
    refs = []
    for sc in part["script"]["scenes"]:
        for c in sc.get("chars", []):
            if c.get("ref") and c["ref"] not in refs:
                refs.append(c["ref"])
    nomes = [story["personagens"][r]["sprite"] for r in refs if story["personagens"].get(r, {}).get("sprite")]
    estados = [("normal", "idle"), ("normal", "meia"), ("normal", "aberta"), ("arregalado", "o"),
               ("normal", "triste"), ("normal", "sorriso")]
    tiles = []
    for nome in nomes:
        for e, mo in estados:
            im = sprites.render(nome, 600, e, mo)
            tiles.append(im.crop((0, 0, im.width, int(im.height * 0.5))))
    out = f"/tmp/conferir_{slug}_{n}_rostos.png"
    if not tiles:
        return None
    tw = max(t.width for t in tiles)
    th = max(t.height for t in tiles)
    o = Image.new("RGB", (tw * len(estados), th * len(nomes)), (70, 80, 100))
    for i, t in enumerate(tiles):
        o.paste(t, ((i % len(estados)) * tw, (i // len(estados)) * th), t)
    o.thumbnail((2400, 2400))
    o.save(out)
    return out


if __name__ == "__main__":
    slug, n = sys.argv[1], int(sys.argv[2])
    print(rostos(slug, n))
    print(quadros(slug, n))
