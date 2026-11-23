"""Cortes rápidos (regra do dono): quebra cenas longas em cenas curtas de 1 frase (2–4 s),
variando o plano (zoom, pan, close) como nos vídeos virais de referência.

Uso:  python3 tools/cortes.py <slug> <parte> [--max 16]
Ou em código: cortes.cortar(script) -> script novo.
Mantém tudo o que importa: personagens, falas, vozes, cenário, efeitos, capa e gancho.
Revise o resultado: a ferramenta só divide; o texto continua o mesmo.
"""
import json, os, re, sys

CAMS = ["in", "zoom_rosto", "pan_l", "out", "zoom_forte", "pan_r"]


def _frases(texto, maxp):
    partes = [p.strip() for p in re.split(r"(?<=[.!?…])\s+", texto.strip()) if p.strip()]
    blocos, atual = [], ""
    for p in partes:
        junto = (atual + " " + p).strip()
        if atual and len(junto.split()) > maxp:
            blocos.append(atual)
            atual = p
        else:
            atual = junto
    if atual:
        blocos.append(atual)
    return blocos or [texto]


def _pedacos(sc, maxp):
    """Lista de (text|None, linhas|None) de cada pedaço da cena."""
    if sc.get("linhas"):
        out, grupo, n = [], [], 0
        for ln in sc["linhas"]:
            w = len(ln.get("texto", "").split())
            if grupo and (n + w > maxp or ln.get("voz") != grupo[-1].get("voz")):
                out.append((None, grupo))
                grupo, n = [], 0
            grupo.append(ln)
            n += w
        if grupo:
            out.append((None, grupo))
        return out
    return [(t, None) for t in _frases(sc.get("text", ""), maxp)]


def cortar(script, maxp=16):
    novas, k = [], 0
    for sc in script.get("scenes", []):
        peds = _pedacos(sc, maxp)
        if len(peds) == 1:
            novas.append(sc)
            continue
        for j, (txt, linhas) in enumerate(peds):
            nova = {key: v for key, v in sc.items() if key not in ("text", "linhas")}
            if txt is not None:
                nova["text"] = txt
            else:
                nova["linhas"] = linhas
            if j > 0:
                for key in ("cover", "hook", "hold"):
                    nova.pop(key, None)
                if sc.get("cam") in ("shake", "zoom_tremido") or sc.get("tint"):
                    nova["cam"] = sc["cam"] if sc.get("cam") else "zoom_rosto"
                else:
                    nova["cam"] = CAMS[(k + j) % len(CAMS)]
                    if nova["cam"] == novas[-1].get("cam"):
                        nova["cam"] = CAMS[(k + j + 1) % len(CAMS)]
                if linhas and len(nova.get("chars", [])) > 1:
                    quem = linhas[0].get("voz")
                    so = [c for c in nova["chars"] if c.get("ref") == quem]
                    if so:  # plano fechado em quem fala
                        c = dict(so[0])
                        c["x"] = 0.5
                        nova["chars"] = [c]
            novas.append(nova)
        k += 1
    s = dict(script)
    s["scenes"] = novas
    return s


if __name__ == "__main__":
    slug, n = sys.argv[1], int(sys.argv[2])
    maxp = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 16
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, "historias", slug, "historia.json")
    h = json.load(open(path))
    p = next(x for x in h["partes"] if x["n"] == n)
    antes = len(p["script"]["scenes"])
    p["script"] = cortar(p["script"], maxp)
    json.dump(h, open(path, "w"), ensure_ascii=False, indent=1)
    print(f"{slug} parte {n}: {antes} -> {len(p['script']['scenes'])} cenas")
