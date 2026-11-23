"""Renderiza uma parte de uma história.

Uso: python3 tools/render_part.py <slug> <n>
Lê historias/<slug>/historia.json, resolve personagens ("ref") e gera
videos/<slug>/parte<n>.mp4, videos/<slug>/capa<n>.jpg e imprime a legenda.
"""
import json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import engine  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, "tools"))

TAGS = "#historia #misterio #suspense #historiasempartes #contos #mundoemhistorias"


def _faixa(story, n, script):
    """Texto da faixa branca do topo (estilo dos episódios)."""
    if story["tipo"] == "votacao" and n > 1:
        ant = next((p for p in story["partes"] if p["n"] == n - 1), {})
        if ant.get("escolha"):
            return f"PARTE {n} · VOCÊS ESCOLHERAM {ant['escolha']}"
    return f"PARTE {n} · {script.get('cover_text', story['titulo']).upper()}"


def _rostos_voto(story, script, chars):
    """Rosto de cada opção na tela de votos: script.opcoes_rostos ou os personagens da última cena."""
    if story["tipo"] != "votacao":
        return None
    specs = script.get("opcoes_rostos")
    if not specs:
        ult = [c for c in script["scenes"][-1].get("chars", []) if c.get("ref")]
        outros = [{"ref": r} for r in chars if r not in [c["ref"] for c in ult]]
        specs = (ult + outros)[:2]
    out = []
    for s in specs[:2]:
        base = dict(chars.get(s.get("ref"), {}))
        base.update({k: v for k, v in s.items() if k in ("eyes", "brows", "mouth")})
        out.append(base if base.get("sprite") else None)
    while len(out) < 2:
        out.append(None)
    return out


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
        "estilo": story.get("estilo"),
        "voto_rostos": _rostos_voto(story, script, chars),
        "voto_chamada": script.get("chamada"),
        "faixa": script.get("faixa") or _faixa(story, n, script),
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
            estilos.add(sprites.familia(nome))
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


TRAVA_PATH = os.path.join(ROOT, "elencos_travados.json")
# Chaves que mudam o físico ou a voz: não podem ser sobrescritas dentro de uma cena.
PROIBIDAS_EM_CENA = ("sprite", "cloth", "skin", "hair", "hairstyle", "escuro", "voz", "pitch", "speed", "nome")


def checar_travas(story, slug, gravar=False):
    """Trava do dono: físico e voz de cada personagem ficam guardados em elencos_travados.json
    e nunca mudam. Só é permitido acrescentar história nova ou personagem novo."""
    trava = json.load(open(TRAVA_PATH)) if os.path.exists(TRAVA_PATH) else {"historias": {}}
    hist = trava.setdefault("historias", {})
    pers = story.get("personagens", {})
    lock = story.get("personagens_travados") or {}
    entrada = hist.get(slug)
    novos = []
    if entrada is None:
        entrada = {"titulo": story.get("titulo"), "personagens": {}}
        hist[slug] = entrada
    for ref, spec in entrada["personagens"].items():
        if pers.get(ref) != spec:
            sys.exit(f"ERRO (trava do dono): o personagem {ref} de '{slug}' mudou de físico ou voz ou foi removido. "
                     f"Restaure em 'personagens' exatamente o que está em elencos_travados.json.")
        if ref in lock and lock[ref] != spec:
            sys.exit(f"ERRO (trava do dono): 'personagens_travados' de {ref} em '{slug}' foi alterado. "
                     f"Restaure igual a elencos_travados.json.")
    for ref, spec in pers.items():
        if ref not in entrada["personagens"]:
            novos.append(ref)
            entrada["personagens"][ref] = json.loads(json.dumps(spec))
    for p in story.get("partes", []):
        for sc in (p.get("script") or {}).get("scenes", []):
            for c in sc.get("chars", []):
                ruins = [k for k in PROIBIDAS_EM_CENA if k in c]
                if ruins:
                    sys.exit(f"ERRO (trava do dono): a parte {p['n']} de '{slug}' muda {ruins} do personagem "
                             f"{c.get('ref')} dentro de uma cena. Físico e voz vêm só de 'personagens'.")
    if novos and gravar:
        with open(TRAVA_PATH, "w") as f:
            json.dump(trava, f, ensure_ascii=False, indent=1)
        print("trava: personagens novos guardados:", ", ".join(novos), file=sys.stderr)
    return novos


def main(slug, n):
    path = os.path.join(ROOT, "historias", slug, "historia.json")
    with open(path) as f:
        story = json.load(f)
    checar_catalogos(story)
    checar_travas(story, slug, gravar=True)
    import preparar  # processo obrigatório: catálogo, falas e verificação
    erros, avisos, feito = preparar.preparar(slug, n)
    for x in feito + avisos:
        print("preparação:", x, file=sys.stderr)
    if erros:
        sys.exit("ERRO na preparação: " + " | ".join(erros))
    with open(path) as f:
        story = json.load(f)
    checar_travas(story, slug)
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
