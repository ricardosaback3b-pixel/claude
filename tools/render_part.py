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
            if c.get("ref"):
                base["_ref"] = c["ref"]
            for k in ("voz", "pitch", "speed", "nome"):
                base.pop(k, None)
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
        "narrador": story.get("narrador"),
        "vozes": {k: {kk: v[kk] for kk in ("voz", "pitch", "speed") if kk in v} for k, v in chars.items() if "voz" in v},
        "nomes": {k: v.get("nome", k.title()) for k, v in chars.items()},
        "cores": {k: v.get("cloth", [200, 20, 40]) for k, v in chars.items()},
        "sem_voz": story.get("sem_voz", False),
    }
    caption = script["caption"].strip()
    if "#" not in caption:
        caption += "\n\n" + TAGS
    return {"meta": meta, "scenes": scenes, "caption": caption}


def checar_catalogos(story):
    """Trava: todo personagem tem que vir das cartelas do dono, todos do mesmo estilo."""
    import sprites
    estilos = set()
    for ref, spec in story.get("personagens", {}).items():
        nome = spec.get("sprite")
        if not nome:
            sys.exit(f"ERRO: o personagem {ref} não usa um desenho dos catálogos do dono (falta 'sprite'). "
                     f"Escolha um nome de sprites.lista().")
        try:
            estilos.add(sprites.estilo_de(nome))
        except KeyError:
            sys.exit(f"ERRO: '{nome}' (personagem {ref}) não existe nos catálogos do dono.")
    if len(estilos) > 1:
        sys.exit("ERRO: a história mistura os dois estilos (cartela e catálogo). Use um estilo só.")
    if story.get("estilo") and estilos and story["estilo"] not in estilos:
        sys.exit(f"ERRO: a história diz estilo '{story['estilo']}' mas os personagens são de outro estilo.")
    for p in story.get("partes", []):
        for sc in (p.get("script") or {}).get("scenes", []):
            for c in sc.get("chars", []):
                if not c.get("ref"):
                    sys.exit("ERRO: personagem em cena sem 'ref'. Todo personagem em cena precisa vir de 'personagens'.")


def main(slug, n):
    path = os.path.join(ROOT, "historias", slug, "historia.json")
    with open(path) as f:
        story = json.load(f)
    checar_catalogos(story)
    part = next(p for p in story["partes"] if p["n"] == n)
    # Trava de personagens: na primeira renderização guarda uma cópia; depois, qualquer mudança
    # de visual ou voz de um personagem existente faz a renderização parar com erro.
    lock = story.get("personagens_travados")
    if lock is None:
        story["personagens_travados"] = json.loads(json.dumps(story.get("personagens", {})))
        with open(path, "w") as f:
            json.dump(story, f, ensure_ascii=False, indent=1)
    else:
        for ref, spec in lock.items():
            atual = story.get("personagens", {}).get(ref)
            if atual != spec:
                sys.exit(f"ERRO: o personagem {ref} mudou de visual ou voz. Restaure em 'personagens' "
                         f"exatamente o que está em 'personagens_travados'.")
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
