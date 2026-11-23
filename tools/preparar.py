"""Processo obrigatório antes de gerar qualquer vídeo.

Uso: python3 tools/preparar.py <slug> <n>
  1. ESTILO/CATÁLOGO: confere (ou, em história nova, escolhe e grava) o catálogo de personagens
     da história e trava o visual de cada personagem.
  2. FALAS: confere e grava as vozes de cada personagem e todas as falas da parte em
     historias/<slug>/falas.json (o que cada um disse em cada parte).
  3. VERIFICAÇÃO: confere se está tudo certo (catálogo, vozes iguais às travadas, quem fala existe,
     gancho visual na 1ª cena, zoom nas cenas de tensão, tamanho da parte, opções de votação).
Erros param o vídeo (código de saída 1). Avisos só aparecem no relatório.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def _load(p, default=None):
    try:
        with open(p) as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def _save(p, data):
    with open(p, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def preparar(slug, n, salvar=True):
    import sprites
    erros, avisos, feito = [], [], []
    hp = os.path.join(ROOT, "historias", slug, "historia.json")
    ep = os.path.join(ROOT, "estado.json")
    story = _load(hp)
    estado = _load(ep, {})
    part = next((p for p in story["partes"] if p["n"] == n), None)
    if not part or not part.get("script"):
        return [f"parte {n} sem roteiro"], avisos, feito
    script = part["script"]
    pers = story.get("personagens", {})

    # ---------- 1. estilo / catálogo ----------
    estilos = {sprites.familia(v["sprite"]) for v in pers.values() if v.get("sprite") and v["sprite"] in sprites.lista()}
    if not story.get("estilo"):
        if len(estilos) == 1:
            story["estilo"] = estilos.pop()
        else:
            story["estilo"] = "andar" if estado.get("ultimo_estilo") == "cartela" else "cartela"
        estado["ultimo_estilo"] = story["estilo"]
        feito.append(f"história nova: estilo '{story['estilo']}' escolhido e gravado")
    for ref, v in pers.items():
        s = v.get("sprite")
        if not s or s not in sprites.lista():
            erros.append(f"{ref}: desenho '{s}' não existe nos catálogos")
        elif sprites.familia(s) != story["estilo"]:
            erros.append(f"{ref}: '{s}' é de outro estilo (a história é '{story['estilo']}')")
    usados = [v.get("sprite") for v in pers.values() if not v.get("escuro")]  # versão escurecida (ex.: "outro eu") pode repetir
    if len(usados) != len(set(usados)):
        erros.append("dois personagens usam o mesmo desenho")
    trav = story.get("personagens_travados")
    if trav is None:
        story["personagens_travados"] = json.loads(json.dumps(pers))
        feito.append("visual e voz dos personagens travados")
    else:
        for ref, spec in trav.items():
            if pers.get(ref) != spec:
                erros.append(f"{ref} mudou de visual ou voz desde que foi travado")
        for ref in pers:
            if ref not in trav:
                trav[ref] = json.loads(json.dumps(pers[ref]))
                feito.append(f"personagem novo {ref} travado")

    # ---------- 2. falas ----------
    combos = {}
    for ref, v in pers.items():
        if not v.get("voz"):
            erros.append(f"{ref}: sem voz definida")
            continue
        pe = min(1.08, max(0.93, float(v.get("pitch", 1.0))))  # mesmo limite do tts.py
        for (vz, pp), outro in combos.items():
            if vz == v["voz"] and abs(pp - pe) < 0.04 and abs(float(pers[outro].get("speed", 1)) - float(v.get("speed", 1))) < 0.05:
                erros.append(f"{ref} e {outro} ficam com a mesma voz; afaste o pitch (0.93–1.08) ou o speed")
        combos[(v["voz"], pe)] = ref
    narr = story.get("narrador")
    if narr and narr not in pers:
        erros.append(f"narrador '{narr}' não está nos personagens")
    falas = []
    for i, sc in enumerate(script.get("scenes", [])):
        for ln in sc.get("linhas") or [{"voz": narr, "texto": sc.get("text", "")}]:
            quem = ln.get("voz") or narr
            if quem and quem not in pers:
                erros.append(f"cena {i + 1}: '{quem}' fala mas não existe nos personagens")
            falas.append({"cena": i + 1, "personagem": quem, "texto": ln.get("texto", "")})
        for c in sc.get("chars", []):
            if c.get("ref") not in pers:
                erros.append(f"cena {i + 1}: personagem em cena '{c.get('ref')}' não existe")
    fp = os.path.join(ROOT, "historias", slug, "falas.json")
    reg = _load(fp, {"vozes": {}, "partes": {}})
    reg["vozes"] = {r: {k: v.get(k) for k in ("nome", "voz", "pitch", "speed")} for r, v in pers.items()}
    reg["partes"][str(n)] = falas
    falantes = {f["personagem"] for f in falas if f["personagem"] and f["personagem"] != narr}
    feito.append(f"{len(falas)} falas da parte {n} gravadas ({len(falantes)} personagens falando)")

    # ---------- 3. verificação ----------
    scenes = script.get("scenes", [])
    if not scenes:
        erros.append("parte sem cenas")
    else:
        c1 = scenes[0]
        if not c1.get("hook"):
            erros.append("a 1ª cena precisa de gancho visual (\"hook\": true, imagem mais forte da parte)")
        if not (c1.get("chars") or c1.get("prop")):
            avisos.append("1ª cena sem personagem nem objeto: o gancho visual fica fraco")
    tensas = [i + 1 for i, sc in enumerate(scenes)
              if (sc.get("hook") or sc.get("tensao") or sc.get("tint")) and sc.get("chars")
              and sc.get("cam") not in (None, "zoom_rosto", "zoom_tremido", "zoom_forte", "shake")]
    if tensas:
        avisos.append(f"cenas de tensão sem zoom no rosto: {tensas} (use cam zoom_rosto/zoom_tremido ou deixe sem cam)")
    # cenário, zoom e efeitos (regra do dono: nada genérico demais)
    if scenes:
        bgs = [sc.get("bg") for sc in scenes]
        if bgs.count("escuro") > 2:
            erros.append(f"{bgs.count('escuro')} cenas com fundo 'escuro' (máximo 2): use cenários de verdade (ver Cenários no AGENTE.md)")
        if len(set(bgs)) < 3:
            erros.append(f"só {len(set(bgs))} cenário(s) diferente(s) na parte (mínimo 3)")
        zooms = sum(1 for sc in scenes if sc.get("cam") in ("zoom_rosto", "zoom_tremido", "zoom_forte", "shake")
                    or ((sc.get("tensao") or sc.get("hook")) and sc.get("cam") is None))
        if zooms < 3:
            erros.append(f"só {zooms} cena(s) com zoom/tremida (mínimo 3: gancho + momentos de tensão)")
        def _efeito(sc):
            bp = sc.get("bg_params") or {}
            return bool(sc.get("tint") or sc.get("filtro") or bp.get("chuva") or bp.get("neblina")
                        or bp.get("alerta") or bp.get("luz") == "apagada")
        fx = sum(1 for sc in scenes if _efeito(sc))
        if fx < 2:
            erros.append(f"só {fx} cena(s) com efeito (mínimo 2): tint, filtro \"tv\", ou bg_params chuva/neblina/alerta/luz apagada")
        if sum(1 for sc in scenes if sc.get("bg_params")) < 2:
            avisos.append("personalize pelo menos 2 cenários com bg_params (hora, texto, cor...)")
    palavras = sum(len(f["texto"].split()) for f in falas)
    if not 8 <= len(scenes) <= 10:
        avisos.append(f"{len(scenes)} cenas (o ideal é 8 a 10)")
    if not 190 <= palavras <= 240:
        avisos.append(f"{palavras} palavras faladas (o ideal é 190 a 240)")
    if len(falantes) < 1 or sum(1 for f in falas if f["personagem"] != narr) < 2:
        avisos.append("menos de 2 falas de personagens além da narração")
    if story["tipo"] == "votacao" and n < 6 and len(script.get("opcoes", [])) != 2:
        erros.append("história com votação: a parte precisa de 2 opções em script.opcoes")
    if story["tipo"] == "votacao" and n > 1:
        ant = next((p for p in story["partes"] if p["n"] == n - 1), {})
        if not ant.get("escolha"):
            erros.append(f"a escolha da parte {n - 1} não foi registrada (conte os votos antes)")

    if salvar and not erros:
        _save(hp, story)
        _save(fp, reg)
        _save(ep, estado)
        salvar_elencos()
        feito.append("elenco da história salvo (elenco.json, falas.json e ELENCOS.md)")
    return erros, avisos, feito


def salvar_elencos():
    """Grava elenco.json de cada história e o resumo ELENCOS.md (sempre, a cada preparação)."""
    import glob
    linhas = ["# Elencos salvos (catálogo e vozes de cada história)", "",
              "O visual e a voz de cada personagem ficam travados até o fim da história.", ""]
    for f in sorted(glob.glob(os.path.join(ROOT, "historias", "*", "historia.json"))):
        h = _load(f)
        pers = h.get("personagens", {})
        el = {"slug": h["slug"], "titulo": h["titulo"], "estilo": h.get("estilo"), "narrador": h.get("narrador"),
              "status": h.get("status"),
              "personagens": {r: {k: v.get(k) for k in ("nome", "sprite", "escuro", "voz", "pitch", "speed")}
                              for r, v in pers.items()}}
        d = os.path.dirname(f)
        _save(os.path.join(d, "elenco.json"), el)
        fp = os.path.join(d, "falas.json")
        reg = _load(fp, {"vozes": {}, "partes": {}})
        reg["vozes"] = el["personagens"]
        _save(fp, reg)
        linhas.append(f"## {h['titulo']} (`{h['slug']}`) — estilo `{h.get('estilo')}`, {h.get('status', '')}")
        for r, v in el["personagens"].items():
            esc = " (escurecido)" if v.get("escuro") else ""
            linhas.append(f"- **{v['nome']}** ({r}): desenho `{v['sprite']}`{esc}, voz `{v['voz']}` "
                          f"pitch {v['pitch']} speed {v['speed']}")
        linhas.append("")
    with open(os.path.join(ROOT, "ELENCOS.md"), "w") as f:
        f.write("\n".join(linhas))


if __name__ == "__main__":
    slug, n = sys.argv[1], int(sys.argv[2])
    erros, avisos, feito = preparar(slug, n)
    print("PREPARAÇÃO", slug, "parte", n)
    for x in feito:
        print("  ok:", x)
    for x in avisos:
        print("  aviso:", x)
    for x in erros:
        print("  ERRO:", x)
    if erros:
        print("NÃO GERAR O VÍDEO: corrija os erros e rode de novo.")
        sys.exit(1)
    print("Tudo certo: pode gerar o vídeo.")
