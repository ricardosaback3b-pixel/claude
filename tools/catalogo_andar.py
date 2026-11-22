"""Catálogo próprio no estilo de "O Andar que Não Existe".

Gera assets/andar/<id>.png (corpo inteiro, 600x1420) e assets/andar/rostos.json.
Todos têm o mesmo formato: cabeça redonda grande, orelhas, olhos brancos com pupila,
contorno preto grosso, tronco retangular, braços, cinto, calça e tênis.
Uso: python3 tools/catalogo_andar.py
"""
import json, math, os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "assets", "andar")
S = 2                      # desenha em 2x e reduz (bordas suaves)
W, H = 600, 1420
OL = (22, 16, 20)
LW = 7                     # contorno (em coordenadas 1x)

PELES = {"clara": (246, 205, 170), "media": (232, 178, 132), "morena": (196, 138, 98), "escura": (140, 92, 64)}


YMAP = [False]


def _y(y):
    """Corpo mais curto: tronco e pernas comprimidos (a cabeça não muda)."""
    if not YMAP[0] or y <= 430:
        return y
    if y <= 935:
        return 430 + (y - 430) * 0.70
    return 430 + 505 * 0.70 + (y - 935) * 0.80


def sc(v):
    out = []
    for i, c in enumerate(v):
        out.append((_y(c) if i % 2 else c) * S)
    return out


class Pen:
    def __init__(self, d):
        self.d = d

    def rect(self, box, fill, r=0, ol=True, w=LW):
        if r:
            self.d.rounded_rectangle(sc(box), radius=r * S, fill=fill, outline=OL if ol else None, width=w * S if ol else 0)
        else:
            self.d.rectangle(sc(box), fill=fill, outline=OL if ol else None, width=w * S if ol else 0)

    def ell(self, box, fill, ol=True, w=LW):
        self.d.ellipse(sc(box), fill=fill, outline=OL if ol else None, width=w * S if ol else 0)

    def chord(self, box, a0, a1, fill, ol=True, w=LW):
        self.d.chord(sc(box), a0, a1, fill=fill, outline=OL if ol else None, width=w * S if ol else 0)

    def poly(self, pts, fill, ol=True, w=LW):
        self.d.polygon([(x * S, _y(y) * S) for x, y in pts], fill=fill, outline=OL if ol else None, width=w * S if ol else 0)

    def line(self, pts, fill=OL, w=LW):
        self.d.line([(x * S, _y(y) * S) for x, y in pts], fill=fill, width=w * S, joint="curve")

    def arc(self, box, a0, a1, fill=OL, w=LW):
        self.d.arc(sc(box), a0, a1, fill=fill, width=w * S)


def escurecer(c, f=0.78):
    return tuple(int(v * f) for v in c)


def clarear(c, f=0.25):
    return tuple(int(v + (255 - v) * f) for v in c)


# ------------------------------------------------------------------ partes
def cabelo_atras(p, c):
    hs, cor = c.get("cabelo"), c.get("cor_cabelo", (70, 44, 28))
    if hs in ("longo", "longo_franja", "cacheado_longo"):
        if hs == "cacheado_longo":
            for i in range(9):
                ang = math.radians(150 + i * 30)
                for rr in (0, 1):
                    x = 300 + (215 + rr * 10) * math.cos(ang)
                    y = 300 + (240 + rr * 40) * math.sin(ang) * 0.9 + (120 if math.sin(ang) > 0 else 0)
                    p.ell([x - 70, y - 70, x + 70, y + 70], cor, ol=True)
        p.rect([80, 150, 520, 640], cor, r=90)
    if hs == "rabo":
        p.ell([470, 170, 575, 470], cor)
    if hs == "maria":
        p.ell([40, 180, 140, 380], cor)
        p.ell([460, 180, 560, 380], cor)


def corpo(p, c):
    pele = c["pele"]
    roupa = c.get("roupa", (60, 100, 160))
    manga = c.get("manga", roupa)
    calca = c.get("calca", (46, 56, 92))
    curta = c.get("manga_curta", False)
    tipo = c.get("top", "camiseta")
    baixo = c.get("baixo", "calca")
    # pernas e sapatos
    if baixo in ("saia", "vestido"):
        cor_saia = roupa if baixo == "vestido" else c.get("cor_saia", calca)
        for x0, x1 in ((165, 285), (315, 435)):
            p.rect([x0, 1080, x1, 1320], pele)
        p.poly([(128, 880), (472, 880), (505, 1130), (95, 1130)], cor_saia)
    elif baixo == "bermuda":
        for x0, x1 in ((165, 285), (315, 435)):
            p.rect([x0, 1080, x1, 1320], pele)
        p.rect([150, 900, 292, 1110], calca)
        p.rect([308, 900, 450, 1110], calca)
    else:
        if tipo == "macacao":
            calca = roupa
        p.rect([150, 900, 292, 1325], calca)
        p.rect([308, 900, 450, 1325], calca)
    tenis = c.get("tenis", (250, 250, 250))
    for x0, x1 in ((122, 300), (300, 478)):
        p.rect([x0, 1295, x1, 1378], tenis, r=28)
        p.rect([x0 + 4, 1350, x1 - 4, 1372], (46, 46, 52), ol=False)
    # braços
    for x0, x1 in ((40, 126), (474, 560)):
        if curta:
            p.rect([x0, 500, x1, 840], pele, r=42)
            if tipo != "regata":
                p.rect([x0 - 4, 488, x1 + 4, 650], manga, r=42)
        else:
            p.rect([x0, 488, x1, 840], manga, r=42)
        p.ell([x0 - 2, 800, x1 + 2, 886], pele)
    # tronco
    p.rect([92, 430, 508, 935], roupa, r=95)
    if c.get("cinto"):
        p.rect([118, 885, 482, 925], c["cinto"])
    detalhes_roupa(p, c, tipo, roupa)


def detalhes_roupa(p, c, tipo, roupa):
    escuro = escurecer(roupa)
    camisa = c.get("camisa", (245, 245, 240))
    if tipo == "moletom":
        p.rect([185, 425, 415, 500], escuro, r=36)
        p.line([(268, 490), (262, 640)], (250, 250, 250), w=9)
        p.line([(332, 490), (338, 640)], (250, 250, 250), w=9)
        p.rect([175, 760, 425, 890], escuro, r=30)
    elif tipo in ("camiseta", "regata"):
        p.chord([225, 405, 375, 505], 0, 180, c["pele"])
    elif tipo == "listrada":
        for y in range(520, 880, 70):
            p.rect([100, y, 500, y + 32], c.get("listra", (250, 250, 250)), ol=False)
        p.rect([92, 430, 508, 935], None, r=95)
        p.chord([225, 405, 375, 505], 0, 180, c["pele"])
    elif tipo == "polo":
        p.poly([(245, 440), (300, 470), (270, 520)], escuro)
        p.poly([(355, 440), (300, 470), (330, 520)], escuro)
        p.line([(300, 470), (300, 580)], w=4)
        for y in (505, 550):
            p.ell([292, y, 308, y + 16], (240, 240, 240), w=3)
    elif tipo in ("camisa", "social"):
        p.poly([(240, 440), (300, 485), (262, 530)], camisa)
        p.poly([(360, 440), (300, 485), (338, 530)], camisa)
        p.line([(300, 485), (300, 880)], w=4)
        for y in (560, 660, 760):
            p.ell([292, y, 308, y + 16], (230, 230, 230), w=3)
    elif tipo == "jaleco":
        p.poly([(238, 440), (362, 440), (300, 610)], camisa)
        if c.get("gravata"):
            p.poly([(292, 470), (308, 470), (316, 590), (300, 612), (284, 590)], c["gravata"], w=4)
        p.line([(238, 440), (300, 610), (300, 900)], w=5)
        p.line([(362, 440), (300, 610)], w=5)
        p.rect([360, 560, 440, 650], (250, 250, 250), w=5)
        p.rect([372, 575, 428, 615], c.get("cor_cracha", (110, 150, 200)), ol=False)
        if c.get("estetoscopio"):
            p.arc([180, 430, 420, 700], 20, 160, (70, 70, 80), w=10)
            p.ell([222, 650, 262, 690], (170, 170, 180), w=5)
    elif tipo == "terno":
        p.poly([(250, 440), (350, 440), (300, 650)], camisa)
        p.poly([(290, 470), (310, 470), (320, 640), (300, 672), (280, 640)], c.get("gravata", (40, 70, 150)), w=4)
        p.line([(250, 440), (300, 650), (300, 900)], w=5)
        p.line([(350, 440), (300, 650)], w=5)
        for y in (700, 780):
            p.ell([288, y, 312, y + 24], escurecer(roupa, 0.6), w=3)
        if c.get("faixa_presidencial"):
            p.poly([(130, 470), (180, 450), (470, 860), (420, 885)], (40, 150, 70), w=4)
            p.poly([(150, 462), (165, 455), (452, 868), (437, 876)], (250, 210, 40), ol=False)
    elif tipo == "farda":
        p.poly([(255, 440), (345, 440), (300, 530)], (245, 245, 240))
        p.line([(255, 440), (300, 530), (345, 440)], w=5)
        for x0 in (150, 352):
            p.rect([x0, 560, x0 + 98, 640], clarear(roupa, 0.12), w=5)
            p.rect([x0 + 18, 575, x0 + 80, 595], (235, 225, 190), w=3)
        for y in (560, 650, 740, 830):
            p.ell([290, y, 310, y + 20], (225, 185, 70), w=3)
    elif tipo == "policia":
        p.poly([(255, 440), (345, 440), (300, 520)], escuro)
        p.line([(300, 520), (300, 880)], w=4)
        p.poly([(380, 560), (392, 590), (424, 590), (398, 610), (408, 640), (380, 622), (352, 640), (362, 610), (336, 590), (368, 590)],
               (250, 205, 60), w=4)
    elif tipo == "colete":
        p.poly([(240, 440), (360, 440), (300, 620)], camisa)
        p.poly([(255, 440), (300, 475), (275, 510)], camisa)
        p.poly([(345, 440), (300, 475), (325, 510)], camisa)
        p.line([(240, 440), (300, 620), (360, 440)], w=5)
        for y in (660, 740, 820):
            p.ell([290, y, 310, y + 20], escurecer(roupa, 0.6), w=3)
    elif tipo == "cardigan":
        p.rect([250, 445, 350, 900], c.get("camisa", clarear(roupa, 0.45)), ol=False)
        p.line([(250, 445), (250, 900)], w=5)
        p.line([(350, 445), (350, 900)], w=5)
        for y in (560, 660, 760):
            p.ell([232, y, 252, y + 20], escurecer(roupa, 0.6), w=3)
    elif tipo == "avental":
        p.chord([225, 405, 375, 505], 0, 180, c["pele"])
        p.rect([165, 560, 435, 905], (250, 248, 240), r=20, w=5)
        p.line([(185, 560), (215, 450)], (250, 248, 240), w=12)
        p.line([(415, 560), (385, 450)], (250, 248, 240), w=12)
        p.rect([250, 700, 350, 770], (225, 220, 210), w=4)
    elif tipo == "dolma":
        p.poly([(240, 430), (360, 430), (340, 490), (260, 490)], (210, 50, 40))
        for x in (230, 370):
            for y in (560, 650, 740):
                p.ell([x - 12, y, x + 12, y + 24], (60, 60, 60), w=3)
    elif tipo == "macacao":
        p.chord([225, 405, 375, 505], 0, 180, c["pele"])
        p.rect([175, 600, 425, 905], escuro, r=10, w=5)
        p.line([(190, 600), (190, 445)], escuro, w=18)
        p.line([(410, 600), (410, 445)], escuro, w=18)
        p.rect([250, 640, 350, 720], clarear(roupa, 0.15), w=4)
    elif tipo == "vestido":
        p.chord([225, 405, 375, 505], 0, 180, c["pele"])
        p.rect([96, 690, 504, 715], escuro, ol=False)
    elif tipo == "blazer":
        p.poly([(245, 440), (355, 440), (300, 620)], camisa)
        p.line([(245, 440), (300, 620), (300, 900)], w=5)
        p.line([(355, 440), (300, 620)], w=5)
    if c.get("alcas"):
        cor = c["alcas"]
        p.rect([128, 460, 168, 900], cor, w=5)
        p.rect([432, 460, 472, 900], cor, w=5)
    if c.get("estampa") == "flor":
        for k in range(5):
            a = math.radians(k * 72)
            x, y = 300 + 38 * math.cos(a), 640 + 38 * math.sin(a)
            p.ell([x - 26, y - 26, x + 26, y + 26], (250, 250, 250), w=4)
        p.ell([282, 622, 318, 658], (250, 200, 40), w=4)
    if c.get("estampa") == "controle":
        p.rect([220, 610, 380, 680], (200, 205, 220), r=30, w=5)
        p.line([(250, 645), (275, 645)], w=6)
        p.line([(262, 632), (262, 658)], w=6)
        p.ell([325, 630, 343, 648], (60, 60, 70), w=3)
        p.ell([345, 645, 363, 663], (60, 60, 70), w=3)
    if c.get("numero"):
        p.d.text((300 * S, _y(640) * S), c["numero"], fill=(240, 240, 240), anchor="mm",
                 font=_font(70 * S))


def _font(sz):
    from PIL import ImageFont
    return ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf", sz)


def cabeca(p, c):
    pele = c["pele"]
    p.ell([76, 262, 140, 348], pele)
    p.ell([460, 262, 524, 348], pele)
    p.ell([92, 68, 508, 484], pele)
    if c.get("rugas"):
        for y in (150, 175):
            p.arc([230, y - 20, 370, y + 25], 200, 340, (200, 150, 120), w=4)


def rosto(p, c):
    pele = c["pele"]
    # olhos (sem sobrancelha: o renderizador desenha a sobrancelha conforme a emoção)
    for cx in (228, 372):
        p.ell([cx - 40, 260, cx + 40, 340], (255, 255, 255), w=7)
        p.ell([cx - 14, 286, cx + 14, 314], OL, ol=False)
        p.ell([cx - 7, 288, cx + 2, 297], (255, 255, 255), ol=False)
    # nariz
    p.arc([284, 332, 316, 362], 20, 160, (150, 95, 70), w=4)
    # barba
    if c.get("barba"):
        cor = c.get("cor_barba", c.get("cor_cabelo", (60, 40, 28)))
        p.chord([96, 180, 504, 488], 15, 165, cor)
        p.ell([252, 362, 348, 425], pele, ol=False)
    # boca
    if c.get("boca") == "o":
        p.ell([284, 378, 316, 410], (120, 30, 40), w=5)
    else:
        p.arc([262, 362, 338, 410], 25, 155, OL, w=6)
    if c.get("bigode"):
        cor = c.get("cor_bigode", c.get("cor_cabelo", (60, 40, 28)))
        p.chord([236, 340, 364, 392], 180, 360, cor, w=5)
    if c.get("bochecha"):
        for cx in (170, 430):
            p.ell([cx - 26, 350, cx + 26, 378], (240, 150, 140), ol=False)
    if c.get("oculos"):
        cor = c.get("cor_oculos", OL)
        for cx in (228, 372):
            if c.get("oculos") == "redondo":
                p.ell([cx - 56, 244, cx + 56, 356], None, w=9) if cor == OL else p.d.ellipse(sc([cx - 56, 244, cx + 56, 356]), outline=cor, width=9 * S)
            else:
                p.d.rounded_rectangle(sc([cx - 60, 248, cx + 60, 352]), radius=14 * S, outline=cor, width=10 * S)
        p.line([(284, 296), (316, 296)], cor, w=9)


def cabelo_frente(p, c):
    hs, cor = c.get("cabelo"), c.get("cor_cabelo", (70, 44, 28))
    if hs == "tigela":
        p.chord([84, 50, 516, 400], 180, 360, cor)
    elif hs in ("curto", "curto_lado"):
        p.chord([90, 52, 510, 352], 180, 360, cor)
        p.poly([(98, 200), (150, 195), (128, 262)], cor)
        p.poly([(502, 200), (450, 195), (472, 262)], cor)
        if hs == "curto_lado":
            p.poly([(160, 190), (330, 120), (250, 215)], escurecer(cor, 0.9), w=5)
    elif hs in ("cacheado", "cacheado_longo"):
        p.chord([94, 70, 506, 360], 180, 360, cor)
        for i in range(11):
            a = math.radians(180 + i * 18)
            x, y = 300 + 200 * math.cos(a), 235 + 175 * math.sin(a)
            p.ell([x - 46, y - 46, x + 46, y + 46], cor)
    elif hs in ("longo", "longo_franja", "rabo", "maria", "coque"):
        p.chord([90, 55, 510, 360], 180, 360, cor)
        if hs in ("longo", "longo_franja"):
            p.rect([92, 170, 150, 560], cor, r=28)
            p.rect([450, 170, 508, 560], cor, r=28)
        if hs == "longo_franja":
            p.rect([150, 150, 450, 215], cor, r=20)
        if hs == "coque":
            p.ell([235, 0, 365, 120], cor)
    elif hs == "careca":
        p.ell([84, 190, 150, 300], cor)
        p.ell([450, 190, 516, 300], cor)
    elif hs == "raspado":
        p.chord([96, 66, 504, 330], 180, 360, cor)


def chapeu(p, c):
    h = c.get("chapeu")
    if not h:
        return
    cor = c.get("cor_chapeu", (40, 60, 120))
    if h == "quepe":
        p.chord([96, 10, 504, 250], 180, 360, cor)
        p.rect([110, 125, 490, 205], cor, r=10)
        p.rect([118, 168, 482, 212], escurecer(cor, 0.8), w=5)
        p.chord([150, 180, 450, 262], 0, 180, escurecer(cor, 0.65))
        p.ell([278, 60, 322, 104], c.get("cor_emblema", (200, 180, 80)), w=5)
    elif h == "bone":
        p.chord([94, 30, 506, 320], 180, 360, cor)
        p.chord([110, 150, 490, 250], 0, 180, escurecer(cor, 0.75))
        p.ell([288, 20, 312, 44], escurecer(cor, 0.7), w=3)
    elif h == "bone_tras":
        p.chord([94, 30, 506, 320], 180, 360, cor)
        p.rect([120, 165, 480, 190], escurecer(cor, 0.75), w=5)
    elif h == "cozinheiro":
        for x in (180, 300, 420):
            p.ell([x - 85, -10, x + 85, 150], (252, 252, 252))
        p.rect([130, 90, 470, 190], (252, 252, 252), r=10)
    elif h == "boina":
        p.ell([110, 40, 470, 170], cor)
        p.ell([285, 25, 305, 45], escurecer(cor), w=3)
    elif h == "capacete":
        p.chord([90, 20, 510, 330], 180, 360, cor)
        p.rect([70, 160, 530, 200], escurecer(cor, 0.85), r=18)
        p.ell([280, 60, 320, 110], (240, 200, 60), w=4)
    elif h == "faixa":
        p.rect([96, 160, 504, 200], cor, w=5)
        p.rect([96, 172, 504, 186], (250, 250, 250), ol=False)
    elif h == "fones":
        p.arc([80, 40, 520, 420], 190, 350, (40, 40, 46), w=20)
        p.rect([58, 230, 126, 360], (40, 40, 46), r=26)
        p.rect([474, 230, 542, 360], (40, 40, 46), r=26)
    elif h == "touca_freira":
        pass
    elif h == "tiara":
        p.arc([110, 70, 490, 420], 200, 340, cor, w=22)
    elif h == "laco":
        p.poly([(300, 70), (240, 30), (240, 110)], cor)
        p.poly([(300, 70), (360, 30), (360, 110)], cor)
        p.ell([285, 55, 315, 85], escurecer(cor), w=4)


def desenhar(c):
    im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    p = Pen(ImageDraw.Draw(im))
    cabelo_atras(p, c)
    YMAP[0] = True
    corpo(p, c)
    YMAP[0] = False
    cabeca(p, c)
    rosto(p, c)
    cabelo_frente(p, c)
    chapeu(p, c)
    im = im.resize((W, H), Image.LANCZOS)
    return im.crop((0, 0, W, im.getbbox()[3]))


# ------------------------------------------------------------------ elenco
P = PELES
CAST = {
    # trio de "O Andar que Não Existe" (iguais aos episódios)
    "voce": dict(desc="protagonista estudante", pele=P["clara"], cabelo="tigela", cor_cabelo=(70, 40, 20), top="moletom", roupa=(52, 92, 150), alcas=(200, 60, 40), boca="o"),
    "medico": dict(desc="médico de jaleco", pele=P["clara"], cabelo="tigela", cor_cabelo=(150, 150, 150), top="jaleco", roupa=(245, 245, 248), camisa=(110, 160, 210), estetoscopio=True, calca=(60, 64, 80)),
    "porteiro": dict(desc="porteiro de farda e quepe", pele=P["morena"], chapeu="quepe", cor_chapeu=(88, 104, 58), cabelo="raspado", cor_cabelo=(40, 30, 24), top="farda", roupa=(96, 112, 64), calca=(70, 82, 48), bigode=True, cor_bigode=(150, 150, 150)),
    # outros
    "estudante_ana": dict(desc="estudante, cabelo longo", pele=P["clara"], cabelo="longo", cor_cabelo=(80, 50, 30), top="moletom", roupa=(232, 120, 150), calca=(120, 150, 200), chapeu="tiara", cor_chapeu=(240, 110, 140)),
    "amigo_cacheado": dict(desc="amigo, cabelo cacheado", pele=P["media"], cabelo="cacheado", cor_cabelo=(80, 48, 24), top="moletom", roupa=(70, 130, 60), calca=(40, 44, 50)),
    "rival": dict(desc="rival de boné", pele=P["media"], cabelo="curto", cor_cabelo=(30, 24, 20), chapeu="bone_tras", cor_chapeu=(30, 30, 34), top="camiseta", roupa=(34, 34, 38), manga_curta=True, calca=(50, 60, 90)),
    "professor": dict(desc="professor grisalho de óculos", pele=P["clara"], cabelo="curto_lado", cor_cabelo=(140, 140, 140), oculos="quadrado", top="social", roupa=(245, 245, 245), camisa=(245, 245, 245), calca=(70, 70, 80)),
    "medica": dict(desc="médica de coque", pele=P["media"], cabelo="coque", cor_cabelo=(90, 54, 30), top="jaleco", roupa=(245, 245, 248), camisa=(90, 150, 200), estetoscopio=True, calca=(60, 64, 80)),
    "policial": dict(desc="policial", pele=P["media"], cabelo="curto", cor_cabelo=(50, 34, 24), chapeu="quepe", cor_chapeu=(30, 38, 60), cor_emblema=(240, 200, 60), top="policia", roupa=(36, 48, 80), calca=(32, 40, 66)),
    "faxineira": dict(desc="faxineira", pele=P["media"], cabelo="coque", cor_cabelo=(140, 140, 140), top="avental", roupa=(160, 60, 60), manga_curta=True, calca=(70, 70, 90)),
    "idoso": dict(desc="idoso de bigode", pele=P["clara"], cabelo="careca", cor_cabelo=(170, 170, 170), bigode=True, cor_bigode=(160, 160, 160), rugas=True, top="colete", roupa=(110, 70, 40), manga=(245, 230, 180), camisa=(245, 230, 180), calca=(90, 60, 40)),
    "idosa": dict(desc="idosa de óculos", pele=P["clara"], cabelo="coque", cor_cabelo=(190, 190, 190), oculos="redondo", rugas=True, top="cardigan", roupa=(140, 90, 170), camisa=(220, 200, 230), baixo="saia", cor_saia=(80, 70, 90)),
    "jornalista": dict(desc="jornalista", pele=P["clara"], cabelo="longo", cor_cabelo=(110, 64, 34), top="blazer", roupa=(210, 110, 130), camisa=(250, 250, 250), calca=(50, 50, 60)),
    "empresario": dict(desc="empresário de terno", pele=P["clara"], cabelo="curto_lado", cor_cabelo=(60, 44, 30), top="terno", roupa=(34, 44, 70), gravata=(150, 40, 40), calca=(34, 44, 70)),
    "mae": dict(desc="mãe", pele=P["media"], cabelo="longo", cor_cabelo=(70, 44, 26), top="camiseta", roupa=(240, 225, 190), manga_curta=True, calca=(80, 110, 160)),
    "pai": dict(desc="pai de barba", pele=P["media"], cabelo="curto", cor_cabelo=(50, 34, 24), barba=True, top="polo", roupa=(40, 70, 130), manga_curta=True, calca=(60, 60, 70)),
    "menino": dict(desc="criança curiosa", pele=P["media"], cabelo="cacheado", cor_cabelo=(70, 40, 20), top="camiseta", roupa=(250, 200, 50), manga_curta=True, baixo="bermuda", calca=(60, 90, 150), alcas=(60, 100, 60)),
    "menina": dict(desc="criança alegre", pele=P["clara"], cabelo="maria", cor_cabelo=(110, 64, 34), chapeu="laco", cor_chapeu=(240, 110, 150), top="camiseta", roupa=(240, 130, 170), manga_curta=True, estampa="flor", baixo="saia", cor_saia=(80, 110, 170), bochecha=True),
    "adolescente_fones": dict(desc="adolescente de fones", pele=P["morena"], cabelo="curto", cor_cabelo=(30, 22, 18), chapeu="fones", top="moletom", roupa=(80, 80, 86), calca=(40, 40, 46)),
    "adolescente_menina": dict(desc="adolescente determinada", pele=P["media"], cabelo="rabo", cor_cabelo=(90, 54, 30), top="moletom", roupa=(150, 110, 200), calca=(50, 50, 60)),
    "cientista": dict(desc="cientista de óculos", pele=P["clara"], cabelo="curto_lado", cor_cabelo=(110, 70, 40), oculos="redondo", top="jaleco", roupa=(245, 245, 248), camisa=(150, 190, 220), gravata=(60, 90, 160), calca=(60, 64, 80)),
    "esportista": dict(desc="esportista", pele=P["morena"], cabelo="curto", cor_cabelo=(30, 22, 18), chapeu="faixa", cor_chapeu=(40, 70, 150), top="regata", roupa=(40, 70, 150), manga_curta=True, numero="11", baixo="bermuda", calca=(30, 30, 40)),
    "artista": dict(desc="artista de boina", pele=P["clara"], cabelo="longo", cor_cabelo=(90, 54, 30), chapeu="boina", cor_chapeu=(200, 40, 40), top="avental", roupa=(240, 220, 160), manga_curta=True, calca=(70, 90, 130)),
    "gamer": dict(desc="gamer", pele=P["clara"], cabelo="tigela", cor_cabelo=(30, 24, 20), chapeu="fones", top="camiseta", roupa=(30, 30, 36), manga_curta=True, estampa="controle", calca=(50, 60, 90)),
    "leitora": dict(desc="leitora de óculos", pele=P["clara"], cabelo="longo_franja", cor_cabelo=(120, 74, 40), oculos="redondo", top="cardigan", roupa=(120, 60, 110), camisa=(240, 220, 200), calca=(60, 60, 80)),
    "motorista": dict(desc="motorista de ônibus", pele=P["escura"], cabelo="raspado", cor_cabelo=(30, 22, 18), chapeu="bone", cor_chapeu=(40, 70, 140), top="social", roupa=(170, 200, 230), camisa=(170, 200, 230), bigode=True, cor_bigode=(40, 30, 24), calca=(40, 50, 80)),
    "seguranca": dict(desc="segurança", pele=P["escura"], cabelo="raspado", cor_cabelo=(30, 22, 18), top="polo", roupa=(30, 30, 34), calca=(30, 30, 34)),
    "entregador": dict(desc="entregador", pele=P["media"], cabelo="curto", cor_cabelo=(40, 28, 20), chapeu="bone", cor_chapeu=(210, 60, 40), top="camiseta", roupa=(220, 70, 50), manga_curta=True, calca=(60, 80, 120)),
    "vizinha": dict(desc="vizinha de cabelo cacheado", pele=P["morena"], cabelo="cacheado_longo", cor_cabelo=(40, 26, 18), top="vestido", roupa=(90, 140, 80), manga_curta=True, baixo="vestido"),
    "vizinho": dict(desc="vizinho", pele=P["clara"], cabelo="curto", cor_cabelo=(200, 160, 80), top="listrada", roupa=(60, 150, 90), listra=(250, 250, 250), manga_curta=True, calca=(50, 70, 110)),
    "prefeito": dict(desc="prefeito de faixa", pele=P["clara"], cabelo="curto_lado", cor_cabelo=(70, 50, 34), top="terno", roupa=(34, 40, 56), gravata=(160, 40, 40), faixa_presidencial=True, calca=(34, 40, 56)),
    "zelador": dict(desc="zelador de macacão", pele=P["media"], cabelo="careca", cor_cabelo=(80, 60, 40), top="macacao", roupa=(110, 120, 130), manga_curta=True, bigode=True, cor_bigode=(70, 50, 34)),
    "enfermeira": dict(desc="enfermeira", pele=P["morena"], cabelo="coque", cor_cabelo=(40, 26, 18), top="camiseta", roupa=(120, 190, 200), manga_curta=True, calca=(120, 190, 200)),
    "cozinheiro": dict(desc="cozinheiro", pele=P["clara"], cabelo="curto", cor_cabelo=(50, 34, 24), chapeu="cozinheiro", bigode=True, top="dolma", roupa=(250, 250, 250), calca=(40, 40, 46)),
    "bombeiro": dict(desc="bombeiro", pele=P["media"], cabelo="curto", cor_cabelo=(50, 34, 24), chapeu="capacete", cor_chapeu=(210, 50, 40), top="farda", roupa=(200, 60, 40), calca=(60, 50, 50)),
    "garota_loira": dict(desc="garota loira", pele=P["clara"], cabelo="longo", cor_cabelo=(240, 200, 90), top="camiseta", roupa=(30, 30, 36), manga_curta=True, calca=(110, 150, 200)),
}


def gerar():
    os.makedirs(OUTDIR, exist_ok=True)
    meta = {}
    for nome0, c in CAST.items():
        nome = "andar_" + nome0  # nomes únicos (não colidem com as cartelas)
        im = desenhar(c)
        im.save(os.path.join(OUTDIR, f"{nome}.png"))
        boca_y = 400 if c.get("bigode") else 386
        meta[nome] = {"w": W, "h": im.height, "exato": True, "desc": c["desc"],
                      "olhos": [[188, 260, 268, 340], [332, 260, 412, 340]], "olho_h": 80, "dd": 144,
                      "boca": [300, boca_y], "boca_w": 76, "pele": list(c["pele"]), "bigode": bool(c.get("bigode"))}
    with open(os.path.join(OUTDIR, "rostos.json"), "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    return meta


if __name__ == "__main__":
    m = gerar()
    print(len(m), "personagens")
