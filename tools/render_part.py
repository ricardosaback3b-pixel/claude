"""Renderiza uma parte de uma história.

Uso: python3 tools/render_part.py <slug> <n>
Lê historias/<slug>/historia.json, resolve personagens ("ref") e gera
videos/<slug>/parte<n>.mp4, videos/<slug>/capa<n>.jpg e imprime a legenda.
"""
import json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import engine  # noqa: E402

TAGS = "#historia #misterio #suspense #historiasempartes #contos #mundoemhistorias"


def resolve(story, part):
    chars = story.get("personagens", {})
    total = 6
    script = part["script"]
    scenes = []
    for sc in script["scenes"]:
        sc = dict(sc)
        res = []
        for c in sc.get("chars", []):
            base = dict(chars.get(c.get("ref"), {})) if c.get("ref") else {}
            base.update({k: v for k, v in c.items() if k != "ref"})
            res.append(base)
        sc["chars"] = res
        scenes.append(sc)
    n = part["n"]
    meta = {
        "title": story["titulo"],
        "part": n,
        "total": total,
        "cover_text": script["cover_text"],
        "final": n == total or script.get("final", False),
        "vote": story["tipo"] == "votacao" and n < total,
        "options": script.get("opcoes", []),
        "mood": script.get("mood", "suspense"),
    }
    caption = script["caption"].strip()
    if "#" not in caption:
        caption += "\n\n" + TAGS
    return {"meta": meta, "scenes": scenes, "caption": caption}


def main(slug, n):
    path = os.path.join(ROOT, "historias", slug, "historia.json")
    with open(path) as f:
        story = json.load(f)
    part = next(p for p in story["partes"] if p["n"] == n)
    data = resolve(story, part)
    tmp = os.path.join("/tmp", f"render_{slug}_{n}")
    shutil.rmtree(tmp, ignore_errors=True)
    mp4, dur = engine.render(data, tmp)
    out = os.path.join(ROOT, "videos", slug)
    os.makedirs(out, exist_ok=True)
    shutil.copy(mp4, os.path.join(out, f"parte{n}.mp4"))
    shutil.copy(os.path.join(tmp, "capa.jpg"), os.path.join(out, f"capa{n}.jpg"))
    print(json.dumps({"video": f"videos/{slug}/parte{n}.mp4", "capa": f"videos/{slug}/capa{n}.jpg",
                      "duracao_s": round(dur, 1), "legenda": data["caption"]}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
