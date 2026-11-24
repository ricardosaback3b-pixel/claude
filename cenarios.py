"""30 cenários personalizáveis do @mundoemhistorias (desenho plano, mesmo estilo dos fundos do engine).

Uso no roteiro:  {"bg": "cozinha", "bg_params": {"luz": "apagada", "cor": [90, 120, 160]}}

Parâmetros que TODOS os cenários aceitam (todos opcionais):
  hora     "dia" | "tarde" | "noite" | "amanhecer"   (céu e janelas; padrão "noite")
  luz      "acesa" | "apagada"                         (lugares fechados; apagada = escuro com 1 luz)
  cor      [r, g, b]                                  (cor principal: parede, letreiro ou objeto marcante)
  texto    "..."                                      (placa, quadro, letreiro, pichação, espelho...)
  chuva    true | false        neblina  true | false
  alerta   true | false        (luz vermelha piscante de sirene/alarme, pinta a cena de vermelho)
  seed     número              (muda a disposição dos detalhes, ex.: outros prédios, outras árvores)
Extras de alguns cenários estão na lista CENARIOS (campo "extras").
"""
import math, random
from PIL import Image, ImageDraw, ImageFilter

E = None  # módulo engine (injetado por fundos())

CEUS = {
    "dia": ((120, 180, 240), (200, 230, 250)),
    "tarde": ((250, 140, 90), (255, 210, 150)),
    "amanhecer": ((110, 120, 190), (255, 190, 150)),
    "noite": ((8, 10, 32), (46, 26, 66)),
}


# ------------------------------------------------------------- ajudantes
def sh(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def mix(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def _p(p, k, d):
    v = p.get(k, d)
    return tuple(v) if isinstance(v, list) else v


def txt(d, xy, s, maxw, size, fill, stroke=0, sf=(0, 0, 0)):
    s = str(s)
    size = int(size)
    while size > 24 and E.font(E.ANTON, size).getlength(s) > maxw:
        size -= 4
    d.text(xy, s, font=E.font(E.ANTON, size), fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=sf)


def ceu(p, h=None):
    hora = p.get("hora", "noite")
    top, bot = CEUS.get(hora, CEUS["noite"])
    img = E.vgrad(E.BW, h or E.BH, top, bot).convert("RGBA")
    rng = random.Random(p.get("seed", 1))
    d = ImageDraw.Draw(img)
    if hora == "noite":
        for _ in range(80):
            x, y = rng.randint(0, E.BW), rng.randint(0, 800)
            d.ellipse([x, y, x + 3, y + 3], fill=(230, 230, 255))
        d.ellipse([E.BW - 330, 160, E.BW - 170, 320], fill=(240, 236, 210))
    elif hora == "dia":
        E.glow(img, (E.BW - 250, 250), 160, (255, 250, 210), 220)
        for _ in range(4):
            x, y = rng.randint(0, E.BW - 300), rng.randint(150, 650)
            for k in range(3):
                d.ellipse([x + k * 70, y - (k % 2) * 30, x + k * 70 + 150, y + 80 - (k % 2) * 30], fill=(250, 252, 255))
    else:
        E.glow(img, (E.BW // 2, 1150), 300, (255, 230, 180), 220)
    return img


def noite(p):
    return p.get("hora", "noite") == "noite"


def janela(img, box, p, grade=True):
    x0, y0, x1, y1 = box
    sky = ceu(p, y1 - y0 + 40).crop((0, 0, x1 - x0, y1 - y0))
    img.alpha_composite(sky, (x0, y0))
    d = ImageDraw.Draw(img)
    d.rectangle(box, outline=(40, 30, 26), width=14)
    if grade:
        d.line([(x0 + x1) // 2, y0, (x0 + x1) // 2, y1], fill=(40, 30, 26), width=10)
        d.line([x0, (y0 + y1) // 2, x1, (y0 + y1) // 2], fill=(40, 30, 26), width=10)


def sala(p, parede=(150, 130, 110), chao=(90, 64, 50), piso_y=1500):
    cor = _p(p, "cor", parede)
    img = E.vgrad(E.BW, E.BH, sh(cor, 1.05), sh(cor, 0.8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rectangle([0, piso_y, E.BW, E.BH], fill=chao)
    d.rectangle([0, piso_y - 30, E.BW, piso_y], fill=sh(cor, 0.55))
    for x in range(0, E.BW, 160):
        d.line([x, piso_y, x - 260, E.BH], fill=sh(chao, 0.82), width=4)
    return img


def _sem_cor(p):
    return {k: v for k, v in p.items() if k != "cor"}


def lampada(img, x, y, cor=(255, 230, 170), r=260):
    d = ImageDraw.Draw(img)
    d.line([x, 0, x, y - 30], fill=(30, 30, 30), width=6)
    d.polygon([(x - 70, y), (x + 70, y), (x + 40, y - 40), (x - 40, y - 40)], fill=(50, 50, 56))
    E.glow(img, (x, y + 30), r, cor, 120)


def chao_ext(img, y, cor):
    ImageDraw.Draw(img).rectangle([0, y, E.BW, E.BH], fill=cor)


def arvore(d, x, base, h, rng, cor=(30, 70, 40)):
    d.rectangle([x - 18, base - h * 0.45, x + 18, base], fill=(70, 46, 30))
    for k in range(4):
        r = h * (0.28 - k * 0.04)
        cy = base - h * (0.5 + k * 0.14)
        d.ellipse([x - r + rng.randint(-20, 20), cy - r, x + r, cy + r], fill=sh(cor, 1 + k * 0.08))


def predios(img, p, base, dens=0.3):
    rng = random.Random(p.get("seed", 3))
    n = noite(p)
    pal = [(16, 16, 34), (22, 20, 44), (12, 14, 28)] if n else [(120, 130, 150), (140, 150, 170), (100, 110, 130)]
    E.buildings(img, rng, base, pal, (255, 196, 102) if n else (200, 220, 240), dens if n else 0.12)


def acabamento(img, p):
    """Clima e luzes comuns a todos os cenários."""
    rng = random.Random(p.get("seed", 1) + 99)
    if p.get("luz") == "apagada":
        dark = Image.new("RGBA", img.size, (4, 6, 14, 175))
        img.alpha_composite(dark)
        E.glow(img, (E.BW // 2, 700), 380, (120, 130, 170), 70)
    if p.get("neblina"):
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        for _ in range(9):
            y = rng.randint(900, 1900)
            dl.ellipse([rng.randint(-400, 600), y - 120, rng.randint(700, 1700), y + 120], fill=(200, 205, 215, 70))
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(60)))
    if p.get("chuva"):
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        for _ in range(420):
            x, y = rng.randint(-200, E.BW), rng.randint(-100, E.BH)
            dl.line([x, y, x + 22, y + 70], fill=(190, 205, 230, 120), width=3)
        img.alpha_composite(lay)
        img.alpha_composite(Image.new("RGBA", img.size, (20, 30, 50, 50)))
    if p.get("alerta"):
        img.alpha_composite(Image.new("RGBA", img.size, (200, 0, 20, 55)))
        E.glow(img, (120, 120), 300, (255, 30, 30), 170)
        E.glow(img, (E.BW - 120, 120), 300, (255, 30, 30), 170)
    return img


# ------------------------------------------------------------- lugares fechados
def cozinha(p):
    img = sala(p, (170, 190, 180), (120, 110, 100))
    d = ImageDraw.Draw(img)
    for x in range(0, E.BW, 90):  # azulejos
        for y in range(900, 1300, 90):
            d.rectangle([x, y, x + 88, y + 88], outline=sh(_p(p, "cor", (170, 190, 180)), 0.85), width=3)
    janela(img, (380, 380, 850, 800), p)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1180, E.BW, 1250], fill=(200, 196, 190))
    d.rectangle([0, 1250, E.BW, 1500], fill=(110, 80, 60))
    for x in range(60, E.BW, 300):
        d.rectangle([x, 1290, x + 240, 1470], outline=(70, 50, 36), width=6)
    d.rectangle([60, 260, 300, 560], fill=(110, 80, 60), outline=(70, 50, 36), width=6)
    d.rectangle([E.BW - 300, 260, E.BW - 60, 560], fill=(110, 80, 60), outline=(70, 50, 36), width=6)
    d.rectangle([E.BW - 260, 1050, E.BW - 120, 1180], fill=(70, 70, 76))  # chaleira/fogão
    d.ellipse([E.BW - 240, 1000, E.BW - 140, 1080], fill=(200, 60, 50))
    lampada(img, E.BW // 2, 220)
    return img


def sala_estar(p):
    img = sala(p, (150, 120, 140), (100, 70, 56))
    janela(img, (120, 350, 520, 900), p)
    d = ImageDraw.Draw(img)
    for x in (100, 540):
        d.rectangle([x - 20, 330, x + 0, 950], fill=(140, 40, 50))
    d.rectangle([E.BW - 420, 520, E.BW - 80, 760], fill=(20, 20, 26), outline=(50, 50, 56), width=12)  # TV
    E.glow(img, (E.BW - 250, 640), 160, (120, 170, 255), 70)
    d = ImageDraw.Draw(img)
    d.rectangle([E.BW - 400, 760, E.BW - 100, 1000], fill=(90, 60, 44))
    d.rounded_rectangle([100, 1150, E.BW - 100, 1420], 50, fill=(70, 90, 120))  # sofá
    d.rounded_rectangle([60, 1050, 220, 1440], 40, fill=(60, 80, 108))
    d.rounded_rectangle([E.BW - 220, 1050, E.BW - 60, 1440], 40, fill=(60, 80, 108))
    d.rectangle([700, 300, 900, 450], fill=(220, 200, 150), outline=(80, 60, 40), width=10)  # quadro
    if p.get("texto"):
        txt(d, (800, 375), p["texto"], 180, 60, (60, 40, 30))
    E.glow(img, (300, 1000), 200, (255, 220, 150), 60)
    return img


def banheiro(p):
    img = sala(p, (180, 205, 210), (170, 175, 180))
    d = ImageDraw.Draw(img)
    cor = _p(p, "cor", (180, 205, 210))
    for x in range(0, E.BW, 110):
        for y in range(0, 1500, 110):
            d.rectangle([x, y, x + 108, y + 108], outline=sh(cor, 0.88), width=3)
    d.rectangle([300, 300, E.BW - 300, 900], fill=(200, 215, 225), outline=(120, 120, 130), width=16)  # espelho
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).polygon([(330, 330), (520, 330), (380, 870), (330, 870)], fill=(255, 255, 255, 70))
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    if p.get("texto"):
        txt(d, (E.BW // 2, 600), p["texto"], E.BW - 700, 120, (150, 20, 30))
    d.rectangle([380, 1000, E.BW - 380, 1080], fill=(240, 240, 245))
    d.rectangle([520, 1080, E.BW - 520, 1500], fill=(225, 225, 230))
    d.rectangle([E.BW // 2 - 15, 930, E.BW // 2 + 15, 1000], fill=(160, 160, 170))
    E.glow(img, (E.BW // 2, 200), 300, (240, 250, 255), 120)
    return img


def porao(p):
    img = sala(p, (70, 66, 64), (50, 46, 44))
    d = ImageDraw.Draw(img)
    for y in range(0, 1470, 70):  # tijolos
        off = 0 if (y // 70) % 2 else 70
        for x in range(-off, E.BW, 140):
            d.rectangle([x, y, x + 136, y + 66], outline=(40, 36, 34), width=4)
    for i in range(9):  # escada
        y = 600 + i * 100
        d.rectangle([60 + i * 40, y, 420 + i * 40, y + 30], fill=(100, 76, 56))
    d.rectangle([E.BW - 380, 1100, E.BW - 80, 1480], fill=(110, 84, 60), outline=(60, 44, 30), width=8)  # caixas
    d.rectangle([E.BW - 330, 900, E.BW - 130, 1100], fill=(120, 92, 66), outline=(60, 44, 30), width=8)
    if p.get("texto"):
        txt(d, (E.BW - 230, 1290), p["texto"], 280, 70, (40, 30, 20))
    lampada(img, E.BW // 2 + 60, 380, (255, 210, 140), 300)
    return img


def sotao(p):
    img = sala(p, (120, 96, 72), (90, 66, 48))
    d = ImageDraw.Draw(img)
    d.polygon([(0, 0), (E.BW // 2, 0), (0, 900)], fill=(70, 52, 38))
    d.polygon([(E.BW, 0), (E.BW // 2, 0), (E.BW, 900)], fill=(70, 52, 38))
    for k in range(6):
        d.line([0, 150 * k, E.BW // 2 - 40 * k, 0], fill=(50, 36, 26), width=10)
    win = Image.new("RGBA", img.size, (0, 0, 0, 0))
    janela(win, (E.BW // 2 - 160, 380, E.BW // 2 + 160, 700), p)
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).ellipse([E.BW // 2 - 160, 380, E.BW // 2 + 160, 700], fill=255)
    img.paste(win, (0, 0), Image.composite(Image.new("L", img.size, 255), Image.new("L", img.size, 0), m))
    d = ImageDraw.Draw(img)
    d.ellipse([E.BW // 2 - 160, 380, E.BW // 2 + 160, 700], outline=(40, 30, 22), width=16)
    d.rounded_rectangle([90, 1240, 470, 1480], 30, fill=(100, 60, 40), outline=(50, 30, 20), width=8)  # baú
    d.rectangle([90, 1310, 470, 1340], fill=(180, 150, 60))
    d.rectangle([E.BW - 300, 1000, E.BW - 120, 1480], fill=(200, 200, 205))  # lençol sobre móvel
    d.ellipse([E.BW - 330, 940, E.BW - 90, 1080], fill=(210, 210, 215))
    E.glow(img, (E.BW // 2, 540), 260, (200, 210, 255), 80)
    return img


def hospital(p):
    img = sala(p, (190, 215, 210), (200, 205, 200))
    d = ImageDraw.Draw(img)
    janela(img, (E.BW - 460, 330, E.BW - 90, 820), p)
    d = ImageDraw.Draw(img)
    d.rectangle([90, 420, 400, 650], fill=(20, 26, 24), outline=(90, 100, 100), width=10)  # monitor
    pts = [(110 + i * 10, 540 + (int(40 * math.sin(i)) if i % 7 == 0 else 0)) for i in range(28)]
    d.line(pts, fill=(60, 255, 120), width=5)
    d.line([250, 650, 250, 900], fill=(140, 140, 150), width=10)
    d.rectangle([100, 1180, E.BW - 100, 1290], fill=(240, 242, 245))  # cama
    d.rectangle([100, 1290, E.BW - 100, 1340], fill=(140, 150, 160))
    d.rectangle([100, 1080, 200, 1340], fill=(160, 170, 180))
    d.line([E.BW - 220, 500, E.BW - 220, 1180], fill=(170, 170, 180), width=8)  # soro
    d.rounded_rectangle([E.BW - 270, 500, E.BW - 170, 640], 20, fill=(200, 230, 240))
    d.rectangle([E.BW // 2 - 40, 250, E.BW // 2 + 40, 330], fill=(220, 40, 40))
    d.rectangle([E.BW // 2 - 12, 262, E.BW // 2 + 12, 318], fill=(255, 255, 255))
    d.rectangle([E.BW // 2 - 28, 278, E.BW // 2 + 28, 302], fill=(255, 255, 255))
    E.glow(img, (E.BW // 2, 120), 340, (240, 255, 255), 120)
    return img


def delegacia(p):
    img = sala(p, (110, 120, 130), (70, 72, 80))
    d = ImageDraw.Draw(img)
    d.rectangle([130, 300, E.BW - 130, 900], fill=(170, 130, 90), outline=(90, 60, 40), width=14)  # quadro de cortiça
    rng = random.Random(p.get("seed", 4))
    pins = []
    for i in range(6):
        x, y = 220 + (i % 3) * 300 + rng.randint(-30, 30), 380 + (i // 3) * 260 + rng.randint(-20, 20)
        d.rectangle([x, y, x + 170, y + 200], fill=(235, 230, 220))
        d.ellipse([x + 55, y + 30, x + 115, y + 90], fill=(120, 120, 130))
        d.rectangle([x + 40, y + 95, x + 130, y + 170], fill=(120, 120, 130))
        pins.append((x + 85, y + 10))
    d.line(pins[:4] + [pins[5]], fill=(200, 20, 30), width=5)
    if p.get("texto"):
        txt(d, (E.BW // 2, 340), p["texto"], E.BW - 400, 70, (255, 255, 255), 6)
    d.rectangle([60, 1180, E.BW - 60, 1260], fill=(80, 60, 44))  # mesa
    d.rectangle([100, 1260, 140, 1500], fill=(50, 40, 30))
    d.rectangle([E.BW - 140, 1260, E.BW - 100, 1500], fill=(50, 40, 30))
    d.rectangle([200, 1120, 420, 1180], fill=(230, 225, 210))  # pasta
    lampada(img, E.BW // 2, 200, (255, 240, 200), 280)
    return img


def escritorio(p):
    img = sala(p, (170, 175, 185), (80, 86, 100))
    janela(img, (80, 280, E.BW - 80, 900), p, grade=False)
    d = ImageDraw.Draw(img)
    for x in range(80, E.BW, 270):
        d.line([x, 280, x, 900], fill=(60, 64, 76), width=10)
    predios_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
    predios(predios_img, p, 900, 0.35)
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rectangle([88, 288, E.BW - 88, 892], fill=255)
    img.paste(predios_img, (0, 0), Image.composite(predios_img.split()[3], Image.new("L", img.size, 0), m))
    d = ImageDraw.Draw(img)
    for x in (60, 660):  # mesas e computadores
        d.rectangle([x, 1200, x + 500, 1260], fill=(200, 200, 205))
        d.rectangle([x + 150, 1000, x + 360, 1150], fill=(30, 34, 44), outline=(90, 90, 100), width=8)
        E.glow(img, (x + 255, 1075), 90, (120, 180, 255), 60)
        d = ImageDraw.Draw(img)
        d.rectangle([x + 240, 1150, x + 270, 1200], fill=(90, 90, 100))
    if p.get("texto"):
        txt(d, (E.BW // 2, 200), p["texto"], E.BW - 200, 90, (40, 44, 56))
    return img


def biblioteca(p):
    img = sala(p, (110, 70, 50), (80, 50, 36))
    d = ImageDraw.Draw(img)
    rng = random.Random(p.get("seed", 6))
    for sx in (40, 440, 840):
        d.rectangle([sx, 160, sx + 360, 1470], fill=(70, 44, 30), outline=(40, 24, 16), width=10)
        for sy in range(200, 1440, 180):
            d.rectangle([sx + 10, sy + 150, sx + 350, sy + 165], fill=(50, 30, 20))
            x = sx + 18
            while x < sx + 330:
                w = rng.randint(18, 36)
                h = rng.randint(100, 145)
                d.rectangle([x, sy + 150 - h, x + w, sy + 150], fill=rng.choice([(150, 40, 40), (40, 80, 120), (60, 110, 60), (190, 150, 60), (100, 60, 120)]))
                x += w + 3
    lampada(img, E.BW // 2, 180, (255, 220, 150), 320)
    return img


def mercadinho(p):
    img = sala(_sem_cor(p), (220, 225, 230), (190, 195, 200))
    d = ImageDraw.Draw(img)
    cor = _p(p, "cor", (220, 40, 40))
    d.rectangle([0, 120, E.BW, 300], fill=cor)
    txt(d, (E.BW // 2, 210), p.get("texto", "MERCADINHO"), E.BW - 160, 110, (255, 255, 255), 6)
    rng = random.Random(p.get("seed", 7))
    for sx in (60, 640):
        d.rectangle([sx, 420, sx + 530, 1430], fill=(160, 165, 170))
        for sy in range(470, 1400, 190):
            d.rectangle([sx, sy + 150, sx + 530, sy + 165], fill=(110, 115, 120))
            x = sx + 15
            while x < sx + 500:
                w = rng.randint(40, 70)
                h = rng.randint(70, 140)
                d.rectangle([x, sy + 150 - h, x + w, sy + 150], fill=rng.choice([(240, 200, 40), (40, 160, 220), (230, 80, 60), (90, 190, 90), (250, 250, 250)]))
                x += w + 6
    E.glow(img, (E.BW // 2, 360), 400, (255, 255, 255), 90)
    return img


def lanchonete(p):
    img = sala(_sem_cor(p), (60, 120, 130), (150, 40, 40))
    d = ImageDraw.Draw(img)
    for x in range(0, E.BW, 80):  # chão xadrez
        for y in range(1500, E.BH, 80):
            if (x // 80 + y // 80) % 2:
                d.rectangle([x, y, x + 80, y + 80], fill=(240, 240, 240))
    cor = _p(p, "cor", (255, 60, 160))
    t = p.get("texto", "LANCHES 24H")
    E.glow(img, (E.BW // 2, 330), 330, cor, 110)
    d = ImageDraw.Draw(img)
    txt(d, (E.BW // 2, 330), t, E.BW - 200, 130, (255, 255, 255), 8, cor)
    janela(img, (100, 520, E.BW - 100, 950), p)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1150, E.BW, 1230], fill=(220, 220, 225))
    d.rectangle([0, 1230, E.BW, 1500], fill=(180, 40, 50))
    for x in range(120, E.BW, 280):
        d.rectangle([x + 40, 1300, x + 60, 1500], fill=(160, 160, 170))
        d.ellipse([x - 10, 1270, x + 110, 1320], fill=(200, 40, 50))
    return img


def laboratorio(p):
    img = sala(_sem_cor(p), (60, 80, 90), (40, 48, 56))
    d = ImageDraw.Draw(img)
    d.rectangle([120, 260, E.BW - 120, 760], fill=(10, 20, 26), outline=(80, 100, 110), width=14)  # tela
    cor = _p(p, "cor", (60, 255, 180))
    for i in range(7):
        d.line([160, 330 + i * 60, 160 + (i * 97 % 600) + 200, 330 + i * 60], fill=sh(cor, 0.8), width=8)
    if p.get("texto"):
        txt(d, (E.BW // 2, 680), p["texto"], E.BW - 360, 80, cor)
    E.glow(img, (E.BW // 2, 510), 380, cor, 60)
    d = ImageDraw.Draw(img)
    d.rectangle([40, 1150, E.BW - 40, 1220], fill=(200, 205, 210))
    d.rectangle([40, 1220, E.BW - 40, 1500], fill=(120, 130, 140))
    for i, c in enumerate([(80, 255, 120), (255, 80, 200), (80, 160, 255), (255, 220, 60)]):
        x = 140 + i * 260
        d.polygon([(x, 1150), (x + 110, 1150), (x + 80, 1040), (x + 80, 950), (x + 30, 950), (x + 30, 1040)], fill=(220, 235, 240))
        d.polygon([(x + 8, 1145), (x + 102, 1145), (x + 76, 1070), (x + 34, 1070)], fill=c)
        E.glow(img, (x + 55, 1100), 90, c, 70)
        d = ImageDraw.Draw(img)
    return img


def nave(p):
    img = Image.new("RGBA", (E.BW, E.BH), (40, 46, 60, 255))
    d = ImageDraw.Draw(img)
    rng = random.Random(p.get("seed", 9))
    d.rounded_rectangle([120, 220, E.BW - 120, 1000], 120, fill=(2, 2, 12))
    for _ in range(140):
        x, y = rng.randint(140, E.BW - 140), rng.randint(240, 980)
        d.ellipse([x, y, x + 3, y + 3], fill=(240, 240, 255))
    cor = _p(p, "cor", (90, 140, 255))
    d.ellipse([E.BW - 560, 480, E.BW - 160, 880], fill=cor)
    d.ellipse([E.BW - 520, 520, E.BW - 300, 700], fill=sh(cor, 1.25))
    d.rounded_rectangle([120, 220, E.BW - 120, 1000], 120, outline=(120, 130, 150), width=26)
    d.rectangle([0, 1180, E.BW, E.BH], fill=(30, 34, 44))
    d.polygon([(0, 1180), (E.BW, 1180), (E.BW - 100, 1080), (100, 1080)], fill=(70, 78, 96))
    for i in range(12):
        x = 160 + i * 80
        c = rng.choice([(255, 60, 60), (60, 255, 120), (255, 210, 60), (60, 180, 255)])
        d.rounded_rectangle([x, 1105, x + 50, 1140], 8, fill=c)
    if p.get("texto"):
        txt(d, (E.BW // 2, 1240), p["texto"], E.BW - 300, 80, (120, 220, 255))
    return img


def hotel(p):
    img = sala(p, (130, 40, 50), (60, 30, 30))
    d = ImageDraw.Draw(img)
    for x in range(0, E.BW, 120):
        d.line([x, 0, x, 1470], fill=sh(_p(p, "cor", (130, 40, 50)), 0.85), width=6)
    d.rectangle([150, 300, E.BW - 150, 700], fill=(80, 50, 30), outline=(200, 160, 70), width=10)  # quadro de chaves
    for i in range(12):
        x, y = 220 + (i % 6) * 145, 380 + (i // 6) * 150
        d.ellipse([x, y, x + 30, y + 30], fill=(200, 160, 70))
        d.rectangle([x + 10, y + 30, x + 20, y + 90], fill=(200, 160, 70))
    txt(d, (E.BW // 2, 210), p.get("texto", "RECEPÇÃO"), E.BW - 300, 90, (230, 190, 90))
    d.rectangle([60, 1150, E.BW - 60, 1480], fill=(90, 56, 34), outline=(200, 160, 70), width=10)  # balcão
    d.ellipse([E.BW - 300, 1090, E.BW - 220, 1150], fill=(220, 180, 80))  # sininho
    E.glow(img, (E.BW // 2, 900), 420, (255, 200, 120), 70)
    return img


def gabinete(p):
    img = sala(_sem_cor(p), (180, 170, 150), (110, 70, 50))
    d = ImageDraw.Draw(img)
    janela(img, (E.BW - 470, 300, E.BW - 90, 900), p)
    d = ImageDraw.Draw(img)
    for x in (E.BW - 490, E.BW - 110):
        d.rectangle([x, 280, x + 40, 950], fill=(120, 30, 40))
    d.line([170, 400, 170, 1480], fill=(180, 160, 80), width=12)  # bandeira
    cor = _p(p, "cor", (40, 120, 70))
    d.polygon([(176, 410), (480, 440), (470, 700), (176, 680)], fill=cor)
    d.ellipse([280, 500, 380, 600], fill=(240, 220, 80))
    d.rectangle([520, 320, 720, 560], fill=(230, 220, 200), outline=(150, 120, 60), width=10)  # retrato
    d.ellipse([580, 360, 660, 440], fill=(140, 120, 110))
    d.rectangle([570, 450, 670, 540], fill=(60, 60, 80))
    if p.get("cadeira"):  # cadeira vazia de encosto alto atrás da mesa
        cx = E.BW // 2
        d.rounded_rectangle([cx - 170, 620, cx + 170, 1160], 40, fill=(70, 20, 26), outline=(30, 10, 12), width=10)
        d.rounded_rectangle([cx - 120, 680, cx + 120, 1100], 30, fill=(95, 30, 36))
        for bx in (cx - 140, cx - 70, cx, cx + 70, cx + 140):
            d.ellipse([bx - 9, 650, bx + 9, 668], fill=(200, 170, 80))
    d.rectangle([60, 1150, E.BW - 60, 1230], fill=(90, 50, 30))  # mesa grande
    d.rectangle([90, 1230, E.BW - 90, 1480], fill=(70, 40, 24))
    if p.get("texto"):
        d.rectangle([E.BW // 2 - 220, 1080, E.BW // 2 + 220, 1150], fill=(200, 170, 80))
        txt(d, (E.BW // 2, 1115), p["texto"], 400, 50, (40, 30, 20))
    return img


def ginasio(p):
    img = sala(p, (150, 160, 170), (190, 140, 80))
    d = ImageDraw.Draw(img)
    for i in range(6):  # arquibancada
        y = 500 + i * 120
        d.rectangle([0, y, E.BW, y + 110], fill=sh((120, 130, 150), 1 - i * 0.05))
        d.rectangle([0, y, E.BW, y + 20], fill=(90, 100, 120))
    d.rectangle([E.BW // 2 - 300, 140, E.BW // 2 + 300, 400], fill=(20, 20, 24), outline=(80, 80, 90), width=12)  # placar
    txt(d, (E.BW // 2, 270), p.get("texto", "CASA 0 x 0 VISITA"), 540, 90, (255, 80, 40))
    d.line([0, 1700, E.BW, 1700], fill=(255, 255, 255), width=10)
    d.arc([E.BW // 2 - 300, 1550, E.BW // 2 + 300, 1850], 0, 360, fill=(255, 255, 255), width=10)
    for x in range(100, E.BW, 300):
        E.glow(img, (x, 60), 160, (255, 255, 230), 110)
    return img


def teatro(p):
    img = Image.new("RGBA", (E.BW, E.BH), (20, 10, 14, 255))
    d = ImageDraw.Draw(img)
    cor = _p(p, "cor", (150, 20, 40))
    for x in range(0, E.BW, 70):  # cortina
        d.rectangle([x, 0, x + 70, 1350], fill=sh(cor, 0.85 if (x // 70) % 2 else 1.05))
    d.rectangle([0, 0, E.BW, 160], fill=sh(cor, 0.7))
    d.polygon([(0, 160), (300, 160), (0, 1300)], fill=sh(cor, 0.6))
    d.polygon([(E.BW, 160), (E.BW - 300, 160), (E.BW, 1300)], fill=sh(cor, 0.6))
    d.rectangle([0, 1350, E.BW, 1500], fill=(110, 70, 40))
    d.rectangle([0, 1500, E.BW, E.BH], fill=(40, 26, 20))
    for x in range(40, E.BW, 170):  # poltronas
        d.rounded_rectangle([x, 1800, x + 140, 2000], 30, fill=(110, 20, 30))
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).polygon([(E.BW // 2 - 60, 0), (E.BW // 2 + 60, 0), (E.BW // 2 + 360, 1500), (E.BW // 2 - 360, 1500)], fill=(255, 240, 200, 60))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(20)))
    if p.get("texto"):
        txt(ImageDraw.Draw(img), (E.BW // 2, 90), p["texto"], E.BW - 200, 80, (240, 200, 90))
    return img


def metro(p):
    img = sala(_sem_cor(p), (200, 200, 190), (110, 110, 116), piso_y=1350)
    d = ImageDraw.Draw(img)
    cor = _p(p, "cor", (230, 180, 40))
    d.rectangle([0, 700, E.BW, 760], fill=cor)
    d.rounded_rectangle([E.BW // 2 - 330, 320, E.BW // 2 + 330, 520], 20, fill=(20, 60, 140))
    txt(d, (E.BW // 2, 420), p.get("texto", "ESTAÇÃO CENTRAL"), 600, 90, (255, 255, 255))
    d.rectangle([0, 1350, E.BW, 1390], fill=(240, 200, 40))  # faixa amarela
    d.rectangle([0, 1600, E.BW, E.BH], fill=(30, 30, 34))  # fosso dos trilhos
    for y in (1750, 1950):
        d.rectangle([0, y, E.BW, y + 24], fill=(150, 150, 160))
    for x in range(0, E.BW, 120):
        d.rectangle([x, 1700, x + 60, 2050], fill=(70, 56, 44))
    for x in range(120, E.BW, 400):
        E.glow(img, (x, 150), 170, (255, 255, 230), 120)
    return img


def caverna(p):
    img = Image.new("RGBA", (E.BW, E.BH), (24, 20, 18, 255))
    d = ImageDraw.Draw(img)
    rng = random.Random(p.get("seed", 10))
    cor = _p(p, "cor", (70, 60, 52))
    for k in range(4):
        pts = [(0, 0)] + [(x, 250 + k * 120 + rng.randint(-80, 120)) for x in range(0, E.BW + 100, 100)] + [(E.BW, 0)]
        d.polygon(pts, fill=sh(cor, 0.6 + k * 0.15))
    for x in range(40, E.BW, 140):  # estalactites
        d.polygon([(x, 500), (x + 60, 500), (x + 30, 500 + rng.randint(120, 320))], fill=sh(cor, 0.9))
    d.ellipse([E.BW // 2 - 300, 700, E.BW // 2 + 300, 1500], fill=(6, 6, 8))  # túnel
    d.rectangle([0, 1450, E.BW, E.BH], fill=sh(cor, 0.7))
    for _ in range(14):
        x = rng.randint(0, E.BW)
        d.ellipse([x - 90, 1420, x + 90, 1520], fill=sh(cor, 0.85))
    E.glow(img, (200, 1100), 260, _p(p, "luz_cor", (255, 160, 70)), 110)  # tocha
    return img


# ------------------------------------------------------------- ao ar livre
def ponte(p):
    img = ceu(p)
    d = ImageDraw.Draw(img)
    rng = random.Random(p.get("seed", 2))
    Y = 1640  # tabuleiro na altura dos pés dos personagens
    agua = (40, 70, 90) if not noite(p) else (14, 24, 36)
    d.rectangle([0, Y + 260, E.BW, E.BH], fill=agua)  # rio lá embaixo
    for _ in range(10):
        x, y = rng.randint(0, E.BW - 120), rng.randint(Y + 300, E.BH - 20)
        d.line([x, y, x + 120, y], fill=(200, 230, 255) if not noite(p) else (60, 90, 120), width=5)
    # vão mais estreito: a ponte inteira cabe na tela mesmo com pan/zoom (antes parecia "pela metade")
    L, R = 250, E.BW - 250
    for x0, x1 in ((0, L), (R, E.BW)):  # penhascos
        d.polygon([(x0, Y - 30), (x1, Y), (x1, E.BH), (x0, E.BH)], fill=(70, 60, 50))
    for x in (60, E.BW - 110):
        arvore(d, x, Y - 20, 620, rng, (24, 60, 36) if not noite(p) else (10, 26, 18))
    cor = _p(p, "cor", (130, 90, 50))
    corda = (60, 44, 30)
    yb = lambda x: Y + 90 * math.sin(math.pi * (x - L) / (R - L))
    if p.get("quebrada"):
        # ponte CAÍDA: nada atravessa o vão; cada metade ficou pendurada no seu penhasco
        n = 10
        for lado, xp in ((1, L), (-1, R)):
            xs = xp + lado * 12
            for i in range(n):
                yy = Y + 20 + i * 44
                sw = lado * int(6 * math.sin(i * 0.9))  # leve torção das tábuas
                d.rectangle([xs - 20 + sw, yy, xs + 20 + sw, yy + 28], fill=cor)
            d.line([xs - 22, Y - 190, xs - 22, Y + 20 + n * 44], fill=corda, width=8)
            d.line([xs + 22, Y, xs + 22, Y + 20 + n * 44], fill=corda, width=8)
            # pontas de corda rompidas balançando no topo
            d.line([(xp, Y - 190), (xp + lado * 60, Y - 150), (xp + lado * 80, Y - 100)], fill=corda, width=6)
    else:
        for x in range(L, R, 46):
            d.rectangle([x, yb(x), x + 38, yb(x) + 30], fill=cor)
            d.line([x + 19, yb(x), x + 19, yb(x) - 190], fill=corda, width=4)
        d.line([(x, yb(x) - 190) for x in range(L, R + 1, 20)], fill=corda, width=8)
        d.line([(x, yb(x) + 4) for x in range(L, R + 1, 20)], fill=corda, width=8)
    for x in (L, R):
        d.rectangle([x - 16, Y - 260, x + 16, Y + 20], fill=(90, 64, 40))
    if p.get("texto"):
        d.rectangle([20, Y - 230, 160, Y - 160], fill=(150, 110, 60))
        txt(d, (90, Y - 195), p["texto"], 130, 44, (40, 26, 16))
    return img


def rio(p):
    img = ceu(p)
    d = ImageDraw.Draw(img)
    rng = random.Random(p.get("seed", 3))
    agua = (60, 120, 160) if not noite(p) else (14, 30, 50)
    d.polygon([(0, 900), (E.BW, 1000), (E.BW, 1300), (0, 1250)], fill=(40, 90, 50) if not noite(p) else (12, 30, 20))
    d.rectangle([0, 1250, E.BW, 1700], fill=agua)
    for _ in range(25):
        x, y = rng.randint(0, E.BW), rng.randint(1270, 1680)
        d.line([x, y, x + rng.randint(40, 140), y], fill=sh(agua, 1.6), width=4)
    d.rectangle([0, 1650, E.BW, E.BH], fill=(110, 90, 60))
    for _ in range(9):
        x = rng.randint(0, E.BW)
        d.ellipse([x - 70, 1630, x + 70, 1700], fill=(130, 120, 110))
    for x in range(0, E.BW, 220):
        arvore(d, x + rng.randint(-40, 40), 1000, rng.randint(380, 520), rng, (30, 80, 40) if not noite(p) else (10, 26, 18))
    if p.get("texto"):
        d.rectangle([E.BW - 330, 1450, E.BW - 316, 1700], fill=(80, 60, 40))
        d.rectangle([E.BW - 420, 1420, E.BW - 220, 1500], fill=(150, 110, 60))
        txt(d, (E.BW - 320, 1460), p["texto"], 180, 50, (40, 26, 16))
    return img


def praia(p):
    img = ceu(p)
    d = ImageDraw.Draw(img)
    mar = (40, 140, 190) if not noite(p) else (10, 24, 50)
    d.rectangle([0, 1050, E.BW, 1450], fill=mar)
    for y in range(1080, 1440, 60):
        d.line([0, y, E.BW, y], fill=sh(mar, 1.3), width=4)
    d.polygon([(0, 1450), (E.BW, 1380), (E.BW, E.BH), (0, E.BH)], fill=(230, 200, 140) if not noite(p) else (90, 80, 70))
    d.polygon([(0, 1450), (E.BW, 1380), (E.BW, 1420), (0, 1490)], fill=(250, 250, 250) if not noite(p) else (150, 150, 160))
    x = 140  # coqueiro
    d.line([(x, 1500), (x + 60, 1100), (x + 140, 800)], fill=(110, 80, 50), width=36)
    for a in range(0, 360, 60):
        dx, dy = math.cos(math.radians(a)) * 260, math.sin(math.radians(a)) * 110
        d.polygon([(x + 140, 800), (x + 140 + dx, 800 + dy + 60), (x + 140 + dx * 0.6, 800 + dy - 20)], fill=(40, 120, 50) if not noite(p) else (14, 40, 20))
    cor = _p(p, "cor", (230, 60, 60))
    d.polygon([(E.BW - 260, 1300), (E.BW - 120, 1000), (E.BW + 20, 1300)], fill=cor)  # guarda-sol
    d.line([E.BW - 120, 1000, E.BW - 120, 1600], fill=(80, 60, 40), width=10)
    if p.get("texto"):
        txt(d, (E.BW // 2, 1980), p["texto"], E.BW - 300, 100, (120, 80, 50))
    return img


def praca(p):
    img = ceu(p)
    predios(img, p, 1100, 0.25)
    d = ImageDraw.Draw(img)
    rng = random.Random(p.get("seed", 5))
    chao_ext(img, 1100, (60, 110, 60) if not noite(p) else (16, 36, 22))
    d.rectangle([0, 1450, E.BW, E.BH], fill=(180, 170, 150) if not noite(p) else (60, 58, 60))
    d.polygon([(E.BW // 2 - 260, 1050), (E.BW // 2 + 260, 1050), (E.BW // 2, 880)], fill=(140, 40, 40))  # coreto
    d.rectangle([E.BW // 2 - 230, 1050, E.BW // 2 + 230, 1300], outline=(240, 240, 240), width=12)
    for x in (120, E.BW - 120):
        arvore(d, x, 1450, 640, rng, (36, 90, 46) if not noite(p) else (12, 30, 20))
    for x in (330, E.BW - 560):
        d.rectangle([x, 1360, x + 230, 1390], fill=(120, 80, 50))
        d.rectangle([x, 1310, x + 230, 1335], fill=(120, 80, 50))
        d.rectangle([x + 20, 1390, x + 32, 1450], fill=(40, 40, 40))
        d.rectangle([x + 198, 1390, x + 210, 1450], fill=(40, 40, 40))
    px = E.BW - 300
    d.rectangle([px, 800, px + 20, 1460], fill=(30, 30, 40))
    if noite(p):
        E.glow(img, (px + 10, 790), 200, (255, 214, 130), 130)
        d = ImageDraw.Draw(img)
    d.rounded_rectangle([px - 90, 960, px + 110, 1060], 14, fill=(20, 90, 60), outline=(240, 240, 240), width=6)
    txt(d, (px + 10, 1010), p.get("texto", "PRAÇA"), 180, 56, (255, 255, 255))
    if p.get("ceu_espelho"):
        ceu_espelho(img, p)
    if p.get("relogio"):
        torre_relogio(img, p)
    return img


def torre_relogio(img, p, cx=260, base=1460):
    """Torre do relógio da praça; ponteiro vermelho (hora em p['relogio_hora'], ex. '17:58')."""
    d = ImageDraw.Draw(img)
    n = noite(p)
    pedra = (150, 140, 128) if not n else (58, 56, 62)
    d.rectangle([cx - 95, 640, cx + 95, base], fill=pedra, outline=sh(pedra, 0.6), width=8)
    for y in range(700, base, 90):
        d.line([cx - 95, y, cx + 95, y], fill=sh(pedra, 0.8), width=3)
    d.polygon([(cx - 120, 640), (cx + 120, 640), (cx, 470)], fill=(110, 40, 40) if not n else (50, 22, 26))
    r = 92
    cy = 760
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 240, 225), outline=(40, 34, 30), width=10)
    for k in range(12):
        a = math.radians(k * 30)
        d.line([cx + math.sin(a) * (r - 22), cy - math.cos(a) * (r - 22), cx + math.sin(a) * (r - 8), cy - math.cos(a) * (r - 8)],
               fill=(40, 34, 30), width=6)
    hh, mm = (str(p.get("relogio_hora", "17:58")) + ":0").split(":")[:2]
    hh, mm = int(hh) % 12, int(mm)
    ah = math.radians((hh + mm / 60) * 30)
    am = math.radians(mm * 6)
    d.line([cx, cy, cx + math.sin(ah) * 50, cy - math.cos(ah) * 50], fill=(30, 26, 24), width=12)
    d.line([cx, cy, cx + math.sin(am) * 78, cy - math.cos(am) * 78], fill=(220, 20, 30), width=9)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(220, 20, 30))
    d.rectangle([cx - 30, base - 150, cx + 30, base], fill=(60, 40, 30))  # porta da torre


def ceu_espelho(img, p):
    """O céu vira espelho: a mesma cidade de cabeça pra baixo no terço de cima, com gente olhando pra baixo."""
    corte = img.crop((0, 700, E.BW, 1500)).transpose(Image.FLIP_TOP_BOTTOM)
    roxo = Image.new("RGBA", corte.size, (110, 80, 170, 80))
    corte = Image.alpha_composite(corte, roxo)
    mask = Image.new("L", corte.size, 0)
    dm = ImageDraw.Draw(mask)
    h = corte.size[1]
    for y in range(h):  # some aos poucos perto do horizonte (y = distância do topo do espelho)
        dm.line([0, y, E.BW, y], fill=int(240 * max(0.0, 1 - y / h) ** 0.45))
    img.paste(corte, (0, 170), mask)  # abaixo das faixas do topo, pra aparecer no vídeo
    d = ImageDraw.Draw(img)
    rng = random.Random(p.get("seed", 7) + 5)
    for _ in range(38):  # gente de cabeça pra baixo no céu, olhando pra cá
        x, y = rng.randint(60, E.BW - 60), rng.randint(300, 700)
        s = rng.uniform(1.6, 2.5)
        c = (36, 26, 64, 235)
        d.rectangle([x - 9 * s, y, x - 2 * s, y + 26 * s], fill=c)  # pernas (pra cima)
        d.rectangle([x + 2 * s, y, x + 9 * s, y + 26 * s], fill=c)
        d.rounded_rectangle([x - 12 * s, y + 24 * s, x + 12 * s, y + 52 * s], int(4 * s), fill=c)  # tronco
        d.line([x - 12 * s, y + 30 * s, x - 20 * s, y + 52 * s], fill=c, width=int(5 * s))  # braços
        d.line([x + 12 * s, y + 30 * s, x + 20 * s, y + 52 * s], fill=c, width=int(5 * s))
        d.ellipse([x - 11 * s, y + 51 * s, x + 11 * s, y + 73 * s], fill=c)  # cabeça (embaixo)
        d.ellipse([x - 6 * s, y + 63 * s, x - 2 * s, y + 67 * s], fill=(255, 240, 200))
        d.ellipse([x + 2 * s, y + 63 * s, x + 6 * s, y + 67 * s], fill=(255, 240, 200))
    E.glow(img, (E.BW // 2, 650), 420, (190, 160, 255), 60)


def parque_diversoes(p):
    img = ceu(p)
    d = ImageDraw.Draw(img)
    cx, cy, r = E.BW // 2 + 120, 800, 480
    for a in range(0, 360, 30):
        x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        d.line([cx, cy, x, y], fill=(200, 200, 210), width=8)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(220, 220, 230), width=16)
    for a in range(0, 360, 30):
        x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        d.rounded_rectangle([x - 40, y, x + 40, y + 70], 14, fill=[(230, 60, 60), (60, 150, 230), (240, 200, 40)][a // 30 % 3])
    d.polygon([(cx, cy), (cx - 200, 1500), (cx - 160, 1500)], fill=(150, 150, 160))
    d.polygon([(cx, cy), (cx + 200, 1500), (cx + 160, 1500)], fill=(150, 150, 160))
    cor = _p(p, "cor", (230, 50, 60))
    for i in range(3):  # barraca listrada
        x0 = 40 + i * 120
        d.rectangle([x0, 1150, x0 + 120, 1450], fill=cor if i % 2 == 0 else (250, 250, 250))
    d.polygon([(20, 1150), (400, 1150), (210, 980)], fill=cor)
    chao_ext(img, 1450, (90, 80, 70) if not noite(p) else (30, 28, 30))
    if noite(p):
        for a in range(0, 360, 15):
            x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
            E.glow(img, (int(x), int(y)), 30, (255, 230, 120), 200)
    if p.get("texto"):
        d = ImageDraw.Draw(img)
        txt(d, (210, 1080), p["texto"], 300, 60, (255, 255, 255), 5)
    return img


def estrada(p):
    img = ceu(p)
    d = ImageDraw.Draw(img)
    chao_ext(img, 1000, (150, 130, 90) if not noite(p) else (30, 28, 24))
    d.polygon([(E.BW // 2 - 30, 1000), (E.BW // 2 + 30, 1000), (E.BW + 300, E.BH), (-300, E.BH)], fill=(60, 60, 66) if not noite(p) else (24, 24, 28))
    for k in range(8):
        t0, t1 = (k / 8) ** 1.8, ((k + 0.5) / 8) ** 1.8
        y0, y1 = 1000 + (E.BH - 1000) * t0, 1000 + (E.BH - 1000) * t1
        w0, w1 = 4 + 30 * t0, 4 + 30 * t1
        d.polygon([(E.BW // 2 - w0, y0), (E.BW // 2 + w0, y0), (E.BW // 2 + w1, y1), (E.BW // 2 - w1, y1)], fill=(240, 210, 60))
    d.rectangle([E.BW - 260, 820, E.BW - 246, 1300], fill=(120, 120, 130))  # placa
    d.rectangle([E.BW - 380, 760, E.BW - 120, 900], fill=(20, 110, 60), outline=(240, 240, 240), width=6)
    txt(d, (E.BW - 250, 830), p.get("texto", "KM 47"), 230, 70, (255, 255, 255))
    rng = random.Random(p.get("seed", 8))
    for _ in range(6):
        x = rng.choice([rng.randint(0, 300), rng.randint(E.BW - 300, E.BW)])
        d.ellipse([x - 40, 960, x + 40, 1010], fill=(70, 90, 50) if not noite(p) else (20, 26, 18))
    if noite(p):
        E.glow(img, (E.BW // 2, 1000), 120, (255, 240, 200), 120)  # farol ao longe
    return img


def posto(p):
    img = ceu(p)
    d = ImageDraw.Draw(img)
    chao_ext(img, 1450, (90, 90, 96) if not noite(p) else (30, 30, 34))
    cor = _p(p, "cor", (230, 40, 40))
    d.rectangle([0, 520, E.BW, 640], fill=cor)  # cobertura
    d.rectangle([0, 640, E.BW, 670], fill=(240, 240, 240))
    for x in (180, E.BW - 220):
        d.rectangle([x, 670, x + 40, 1450], fill=(220, 220, 225))
    for x in (380, 720):  # bombas
        d.rounded_rectangle([x, 1050, x + 150, 1450], 20, fill=(240, 240, 240), outline=sh(cor, 0.7), width=8)
        d.rectangle([x + 25, 1100, x + 125, 1180], fill=(20, 20, 26))
    d.rectangle([E.BW - 260, 200, E.BW - 60, 500], fill=(20, 20, 26), outline=cor, width=10)  # preços
    txt(d, (E.BW - 160, 300), p.get("texto", "POSTO"), 180, 60, (255, 210, 60))
    txt(d, (E.BW - 160, 420), "5,99", 180, 70, (60, 255, 120))
    if noite(p):
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).polygon([(100, 670), (E.BW - 100, 670), (E.BW + 100, 1450), (-100, 1450)], fill=(255, 255, 230, 50))
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(30)))
    return img


def cemiterio(p):
    img = ceu(p)
    d = ImageDraw.Draw(img)
    rng = random.Random(p.get("seed", 13))
    chao_ext(img, 1150, (50, 70, 44) if not noite(p) else (14, 22, 16))
    arvore(d, E.BW - 200, 1150, 700, rng, (40, 40, 36) if noite(p) else (60, 80, 50))
    for row, (y, s) in enumerate([(1180, 0.55), (1330, 0.8), (1500, 1.0)]):
        for x in range(60 + row * 60, E.BW, int(260 * s) + 60):
            w, h = 120 * s, 170 * s
            d.rounded_rectangle([x, y - h, x + w, y], int(50 * s), fill=sh((140, 140, 150), 0.6 + 0.3 * s))
            if rng.random() < 0.35:
                d.rectangle([x + w / 2 - 6 * s, y - h - 60 * s, x + w / 2 + 6 * s, y - h + 10], fill=sh((140, 140, 150), 0.7))
                d.rectangle([x + w / 2 - 30 * s, y - h - 40 * s, x + w / 2 + 30 * s, y - h - 28 * s], fill=sh((140, 140, 150), 0.7))
    for x in range(0, E.BW, 50):  # grade
        d.rectangle([x, 900, x + 8, 1150], fill=(20, 20, 24))
    d.rectangle([0, 950, E.BW, 960], fill=(20, 20, 24))
    if p.get("texto"):
        txt(d, (E.BW // 2, 880), p["texto"], E.BW - 300, 70, (200, 200, 210), 5)
    return img


def beco(p):
    img = ceu(p)
    d = ImageDraw.Draw(img)
    cor = _p(p, "cor", (110, 60, 50))
    d.polygon([(0, 0), (380, 300), (380, 1450), (0, E.BH)], fill=sh(cor, 0.8))
    d.polygon([(E.BW, 0), (E.BW - 380, 300), (E.BW - 380, 1450), (E.BW, E.BH)], fill=sh(cor, 0.65))
    d.polygon([(380, 1450), (E.BW - 380, 1450), (E.BW, E.BH), (0, E.BH)], fill=(40, 40, 44))
    for y in range(400, 1400, 260):  # escada de incêndio
        d.rectangle([E.BW - 360, y, E.BW - 120, y + 16], fill=(20, 20, 22))
        d.line([E.BW - 360, y, E.BW - 120, y - 180], fill=(20, 20, 22), width=8)
    d.rectangle([80, 1400, 330, 1700], fill=(40, 90, 60), outline=(20, 40, 30), width=8)  # caçamba
    d.rectangle([60, 1370, 350, 1410], fill=(30, 70, 46))
    pich = str(p.get("texto", "NÃO OLHE")).split()  # uma palavra por linha, dentro da parte visível da parede
    for i, w in enumerate(pich[:4]):
        txt(d, (275, 840 + (i - (len(pich[:4]) - 1) / 2) * 125), w, 190, 120, (255, 60, 160), 5)
    if noite(p):
        E.glow(img, (E.BW // 2, 500), 220, (255, 220, 150), 110)
    return img


def telhado(p):
    img = ceu(p)
    predios(img, p, 1250, 0.35)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1250, E.BW, E.BH], fill=(90, 90, 96) if not noite(p) else (40, 40, 46))
    d.rectangle([0, 1250, E.BW, 1300], fill=(140, 140, 146) if not noite(p) else (60, 60, 66))
    d.rectangle([E.BW - 380, 700, E.BW - 100, 1000], fill=(110, 140, 160))  # caixa d'água
    for x in (E.BW - 360, E.BW - 140):
        d.rectangle([x, 1000, x + 20, 1260], fill=(60, 60, 70))
    d.rectangle([60, 1000, 340, 1260], fill=(130, 130, 136))  # porta da escada
    d.rectangle([140, 1060, 260, 1260], fill=(70, 60, 50))
    if p.get("texto"):
        txt(d, (E.BW - 240, 850), p["texto"], 250, 70, (255, 255, 255))
    for x in range(0, E.BW, 90):
        d.rectangle([x, 1530, x + 10, 1650], fill=(140, 140, 150))
    d.rectangle([0, 1530, E.BW, 1545], fill=(140, 140, 150))
    return img


def fazenda(p):
    img = ceu(p)
    d = ImageDraw.Draw(img)
    rng = random.Random(p.get("seed", 12))
    d.polygon([(0, 1000), (E.BW, 900), (E.BW, E.BH), (0, E.BH)], fill=(110, 150, 60) if not noite(p) else (22, 34, 18))
    cor = _p(p, "cor", (170, 40, 40))
    bx = 520
    d.rectangle([bx, 650, bx + 560, 1150], fill=cor)  # celeiro
    d.polygon([(bx - 40, 650), (bx + 280, 430), (bx + 600, 650)], fill=sh(cor, 0.7))
    d.rectangle([bx + 180, 850, bx + 380, 1150], fill=(250, 245, 230))
    d.line([bx + 180, 850, bx + 380, 1150], fill=cor, width=12)
    d.line([bx + 380, 850, bx + 180, 1150], fill=cor, width=12)
    for x in range(0, E.BW, 120):  # cerca
        d.rectangle([x, 1300, x + 18, 1480], fill=(150, 110, 70))
    for y in (1340, 1420):
        d.rectangle([0, y, E.BW, y + 16], fill=(150, 110, 70))
    for _ in range(40):
        x, y = rng.randint(0, E.BW), rng.randint(1500, E.BH)
        d.line([x, y, x + 6, y - 40], fill=(80, 120, 40) if not noite(p) else (20, 30, 14), width=4)
    arvore(d, 150, 1050, 520, rng, (40, 100, 40) if not noite(p) else (12, 28, 16))
    if p.get("texto"):
        txt(d, (bx + 280, 760), p["texto"], 480, 70, (250, 245, 230))
    return img


def casa(p):
    """Casa de rua caprichada: telhado de telhas, varanda, janelas com cortina, cerca, árvore e poste."""
    img = ceu(p)
    d = ImageDraw.Draw(img)
    rng = random.Random(p.get("seed", 8))
    n = noite(p)
    chao_ext(img, 1420, (40, 70, 40) if not n else (14, 26, 18))
    d.rectangle([0, 1560, E.BW, E.BH], fill=(150, 140, 130) if not n else (42, 40, 46))  # calçada
    for x in range(0, E.BW, 140):
        d.line([x, 1560, x - 60, E.BH], fill=(120, 112, 104) if not n else (30, 30, 34), width=4)
    arvore(d, 110, 1450, 760, rng, (40, 96, 46) if not n else (12, 30, 20))
    cor = _p(p, "cor", (196, 160, 120))
    x0, x1, top = 260, E.BW - 120, 820
    parede = cor if not n else sh(cor, 0.55)
    d.rectangle([x0, top, x1, 1430], fill=parede)
    for y in range(top + 30, 1430, 46):  # tábuas
        d.line([x0, y, x1, y], fill=sh(parede, 0.9), width=3)
    telha = (150, 60, 44) if not n else (70, 30, 26)
    d.polygon([(x0 - 70, top + 10), ((x0 + x1) // 2, top - 330), (x1 + 70, top + 10)], fill=telha)
    for k in range(1, 7):  # fileiras de telhas
        y = top + 10 - k * 48
        f = k * 48 / 340
        xa, xb = x0 - 70 + (((x0 + x1) // 2) - (x0 - 70)) * f, x1 + 70 - ((x1 + 70) - ((x0 + x1) // 2)) * f
        d.line([xa, y, xb, y], fill=sh(telha, 0.75), width=5)
    d.rectangle([x1 - 150, top - 260, x1 - 90, top - 120], fill=(110, 90, 80))  # chaminé
    luz = (255, 214, 130)
    for (a, b) in ((x0 + 60, x0 + 280), (x1 - 280, x1 - 60)):
        acesa = n and (a < E.BW // 2 or p.get("luz") != "apagada")
        d.rectangle([a, top + 120, b, top + 380], fill=luz if acesa else ((40, 50, 70) if n else (150, 190, 220)))
        d.rectangle([a, top + 120, b, top + 380], outline=(250, 245, 235) if not n else (60, 50, 44), width=12)
        d.line([(a + b) // 2, top + 120, (a + b) // 2, top + 380], fill=(250, 245, 235) if not n else (60, 50, 44), width=8)
        d.polygon([(a + 6, top + 126), (a + 60, top + 126), (a + 30, top + 374), (a + 6, top + 374)], fill=(170, 50, 60))
        d.polygon([(b - 6, top + 126), (b - 60, top + 126), (b - 30, top + 374), (b - 6, top + 374)], fill=(170, 50, 60))
        if acesa:
            E.glow(img, ((a + b) // 2, top + 250), 200, luz, 90)
            d = ImageDraw.Draw(img)
    dx = (x0 + x1) // 2
    d.rectangle([dx - 90, top + 260, dx + 90, 1430], fill=(_p(p, "porta", (110, 64, 40)) if not n else sh(_p(p, "porta", (110, 64, 40)), 0.55)))  # porta (porta = [r,g,b])
    d.ellipse([dx + 50, top + 520, dx + 70, top + 540], fill=(220, 190, 90))
    d.rectangle([x0 - 30, 1400, x1 + 30, 1440], fill=sh(parede, 0.7))  # degrau/varanda
    if p.get("texto"):
        d.rectangle([dx - 70, top + 190, dx + 70, top + 240], fill=(240, 235, 220))
        txt(d, (dx, top + 215), p["texto"], 130, 40, (40, 30, 20))
    for x in range(0, E.BW, 70):  # cerca
        d.polygon([(x, 1500), (x + 20, 1470), (x + 40, 1500), (x + 40, 1600), (x, 1600)], fill=(240, 238, 230) if not n else (80, 78, 76))
    d.rectangle([0, 1530, E.BW, 1546], fill=(240, 238, 230) if not n else (80, 78, 76))
    px = E.BW - 60
    d.rectangle([px, 760, px + 18, 1600], fill=(30, 30, 40))
    if n:
        E.glow(img, (px, 760), 190, (255, 214, 130), 120)
    return img



# ------------------------------------------------------------- escola (O Sombra da Sala 12)
GIZ = "/usr/share/fonts/truetype/google-fonts/ofl/comicrelief/ComicRelief-Bold.ttf"


def relogio_parede(img, cx, cy, r, hora):
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10], fill=(40, 40, 46))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 242, 230))
    for k in range(12):
        a = math.radians(k * 30)
        d.line([cx + math.sin(a) * r * 0.8, cy - math.cos(a) * r * 0.8, cx + math.sin(a) * r * 0.93, cy - math.cos(a) * r * 0.93],
               fill=(30, 30, 30), width=8 if k % 3 == 0 else 4)
    try:
        hh, mm = [int(v) for v in str(hora).split(":")]
    except Exception:
        hh, mm = 19, 0
    am = math.radians(mm * 6)
    ah = math.radians((hh % 12) * 30 + mm * 0.5)
    d.line([cx, cy, cx + math.sin(ah) * r * 0.5, cy - math.cos(ah) * r * 0.5], fill=(20, 20, 20), width=14)
    d.line([cx, cy, cx + math.sin(am) * r * 0.78, cy - math.cos(am) * r * 0.78], fill=(200, 30, 30), width=8)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(20, 20, 20))


def corredor_escola(p):
    """Corredor de escola em perspectiva: armários coloridos, porta da SALA 12, mural, luzes no teto e placa SAÍDA."""
    rng = random.Random(p.get("seed", 12))
    W_, H_ = E.BW, E.BH
    vx, vy = W_ // 2 + p.get("desvio", 0), 900
    bw, bh = 150, 200
    parede = _p(p, "cor", (214, 200, 160))
    faixa = (52, 110, 120)
    img = Image.new("RGBA", (W_, H_), sh(parede, 0.9))
    d = ImageDraw.Draw(img)
    d.polygon([(0, 0), (W_, 0), (vx + bw, vy - bh), (vx - bw, vy - bh)], fill=(200, 196, 184))  # teto
    d.polygon([(0, H_), (W_, H_), (vx + bw, vy + bh), (vx - bw, vy + bh)], fill=(150, 150, 146))  # chão
    for k in range(1, 9):  # rejunte do piso
        f = 1 - 1 / (1 + k * 0.45)
        y = H_ - (H_ - vy - bh) * f
        xl = 0 + (vx - bw) * f
        xr = W_ - (W_ - vx - bw) * f
        d.line([xl, y, xr, y], fill=(120, 120, 118), width=3)
    for x in range(-600, W_ + 700, 190):
        d.line([x, H_, vx + (x - W_ / 2) * 0.12, vy + bh], fill=(122, 122, 120), width=3)
    d.polygon([(0, 0), (vx - bw, vy - bh), (vx - bw, vy + bh), (0, H_)], fill=parede)  # parede esq
    d.polygon([(W_, 0), (vx + bw, vy - bh), (vx + bw, vy + bh), (W_, H_)], fill=sh(parede, 0.9))  # parede dir
    # faixa colorida na metade de baixo das paredes
    yb0 = 1250
    d.polygon([(0, yb0), (vx - bw, vy + bh * 0.25), (vx - bw, vy + bh), (0, H_)], fill=faixa)
    d.polygon([(W_, yb0), (vx + bw, vy + bh * 0.25), (vx + bw, vy + bh), (W_, H_)], fill=sh(faixa, 0.85))
    # parede do fundo com placa SAÍDA e janela
    d.rectangle([vx - bw, vy - bh, vx + bw, vy + bh], fill=sh(parede, 0.75))
    janela(img, (vx - 90, vy - 120, vx + 90, vy + 40), {"hora": "noite", "seed": 4})
    d = ImageDraw.Draw(img)
    d.rectangle([vx - 60, vy - 185, vx + 60, vy - 140], fill=(20, 140, 60))
    txt(d, (vx, vy - 162), "SAÍDA", 110, 34, (230, 255, 230))

    def ponto(lado, f, y0):
        """lado -1 esq, +1 dir; f 0 perto -> 1 fundo; y0 altura na borda da tela."""
        xe = 0 if lado < 0 else W_
        xf = vx - bw if lado < 0 else vx + bw
        yf = vy + (y0 - H_ / 2) / (H_ / 2) * bh
        return (xe + (xf - xe) * f, y0 + (yf - y0) * f)

    def quad(lado, f0, f1, ya, yb, cor, borda=(30, 30, 34), w=5):
        pts = [ponto(lado, f0, ya), ponto(lado, f1, ya), ponto(lado, f1, yb), ponto(lado, f0, yb)]
        d.polygon(pts, fill=cor, outline=borda, width=w)
        return pts

    # armários na parede da esquerda
    cores = [(200, 60, 50), (40, 90, 170), (230, 170, 40), (50, 140, 90)]
    fs = [1 - 1 / (1 + k * 0.22) for k in range(0, 26)]
    for k in range(len(fs) - 1):
        cor = cores[(k // 3) % len(cores)]
        pts = quad(-1, fs[k], fs[k + 1], 560, 1700, cor, w=4)
        if fs[k + 1] - fs[k] > 0.03:
            for j in range(3):
                a = ponto(-1, fs[k] + (fs[k + 1] - fs[k]) * 0.2, 680 + j * 40)
                b = ponto(-1, fs[k] + (fs[k + 1] - fs[k]) * 0.8, 680 + j * 40)
                d.line([a, b], fill=sh(cor, 0.6), width=5)
            c = ponto(-1, fs[k] + (fs[k + 1] - fs[k]) * 0.8, 1120)
            d.ellipse([c[0] - 8, c[1] - 8, c[0] + 8, c[1] + 8], fill=(220, 220, 220))
    # parede da direita: mural de avisos perto, porta SALA 11 e porta SALA 12 mais longe
    quad(1, 0.0, 0.17, 420, 1050, (150, 100, 60), (90, 60, 30), 10)
    for j in range(4):
        f = 0.025 + j * 0.036
        a, b = ponto(1, f, 480 + (j % 2) * 120), ponto(1, f + 0.03, 640 + (j % 2) * 120)
        d.polygon([a, (b[0], a[1] + (b[1] - a[1]) * 0.1), b, (a[0], b[1])], fill=rng.choice([(250, 250, 240), (255, 230, 120), (180, 220, 255), (255, 190, 200)]))
    for f0, f1, nome in ((0.25, 0.4, p.get("texto", "SALA 12")), (0.6, 0.7, p.get("porta_longe", "SALA 13"))):
        quad(1, f0, f1, 520, 1640, (120, 70, 40), (50, 28, 14), 8)
        quad(1, f0 + (f1 - f0) * 0.2, f0 + (f1 - f0) * 0.8, 640, 900, (150, 190, 210), (50, 28, 14), 5)
        c = ponto(1, f0 + (f1 - f0) * 0.18, 1120)
        d.ellipse([c[0] - 10, c[1] - 10, c[0] + 10, c[1] + 10], fill=(230, 200, 90))
        pa, pb = ponto(1, f0, 400), ponto(1, f1, 480)
        d.rectangle([min(pa[0], pb[0]) - 10, pa[1] - 10, max(pa[0], pb[0]) + 10, pb[1]], fill=(250, 250, 240), outline=(40, 40, 40), width=4)
        txt(d, ((pa[0] + pb[0]) / 2, (pa[1] - 10 + pb[1]) / 2), nome, abs(pb[0] - pa[0]) + 10, 60 * (1 - f0 * 0.7), (30, 30, 30))
    # luzes fluorescentes no teto
    acesa = p.get("luz", "acesa") != "apagada"
    for f in (0.15, 0.45, 0.68, 0.82):
        y = (vy - bh) * f
        hw = (W_ / 2 - bw) * (1 - f) * 0.5 + 40
        d.rectangle([vx - hw, y + 10, vx + hw, y + 10 + 40 * (1 - f) + 8], fill=(250, 250, 235) if acesa else (90, 92, 100))
        if acesa:
            E.glow(img, (vx, int(y + 30)), int(220 * (1 - f) + 60), (255, 250, 220), 70)
            d = ImageDraw.Draw(img)
    if not acesa and p.get("lanterna", True):
        pass
    return img


def sala_escola(p):
    """Sala de aula vista da frente: lousa grande (texto em giz), relógio de ponteiro, janela, armário do fundo, carteiras."""
    img = sala(p, (196, 184, 150), (120, 86, 60), 1480)
    d = ImageDraw.Draw(img)
    W_ = E.BW
    # placa da sala e relógio em cima da lousa
    d.rounded_rectangle([W_ // 2 - 150, 380, W_ // 2 + 150, 460], 12, fill=(250, 250, 240), outline=(40, 40, 40), width=5)
    txt(d, (W_ // 2, 420), p.get("placa", "SALA 12"), 280, 54, (30, 30, 30))
    relogio_parede(img, W_ - 210, 400, 85, p.get("relogio_hora", "19:00"))
    # lousa
    x0, y0, x1, y1 = 90, 540, W_ - 90, 1130
    d.rectangle([x0 - 26, y0 - 26, x1 + 26, y1 + 26], fill=(130, 84, 46))
    d.rectangle([x0, y0, x1, y1], fill=(34, 70, 52))
    rng = random.Random(p.get("seed", 7))
    for _ in range(14):  # marcas de apagador
        x, y = rng.randint(x0 + 40, x1 - 300), rng.randint(y0 + 30, y1 - 80)
        d.rounded_rectangle([x, y, x + rng.randint(160, 320), y + 40], 18, fill=(44, 82, 62))
    d.rectangle([x0 - 10, y1 + 26, x1 + 10, y1 + 50], fill=(110, 70, 40))
    d.rectangle([x0 + 120, y1 + 14, x0 + 180, y1 + 30], fill=(80, 140, 230))  # giz azul
    d.rectangle([x0 + 210, y1 + 14, x0 + 260, y1 + 30], fill=(240, 240, 230))
    texto = p.get("texto", p.get("board", ""))
    if texto:
        linhas = str(texto).split("\n")
        size = 120
        f = E.font(GIZ, size)
        while size > 50 and max(f.getlength(l) for l in linhas) > (x1 - x0 - 80):
            size -= 6
            f = E.font(GIZ, size)
        tot = len(linhas) * size * 1.15
        for i, l in enumerate(linhas):
            yy = (y0 + y1) / 2 - tot / 2 + size * 0.58 + i * size * 1.15
            d.text((W_ // 2, yy), l, font=f, fill=_p(p, "giz", (225, 232, 255)), anchor="mm")
    janela(img, (W_ - 320, 1190, W_ - 70, 1450), {"hora": p.get("hora", "noite"), "seed": 5})
    d = ImageDraw.Draw(img)
    # armário do fundo (madeira)
    d.rectangle([60, 1190, 300, 1480], fill=(110, 70, 40), outline=(50, 30, 16), width=8)
    d.line([180, 1195, 180, 1475], fill=(50, 30, 16), width=6)
    for x in (160, 200):
        d.ellipse([x - 9, 1330, x + 9, 1348], fill=(220, 190, 90))
    # carteiras em primeiro plano
    for cx, cy, s in ((200, 1600, 1.0), (W_ - 230, 1600, 1.0), (W_ // 2, 1700, 1.15)):
        w = 230 * s
        d.polygon([(cx - w, cy), (cx + w, cy), (cx + w * 0.9, cy - 70 * s), (cx - w * 0.9, cy - 70 * s)], fill=(190, 140, 80), outline=(80, 50, 24))
        d.rectangle([cx - w * 0.8, cy, cx - w * 0.8 + 20, cy + 300], fill=(70, 70, 76))
        d.rectangle([cx + w * 0.8 - 20, cy, cx + w * 0.8, cy + 300], fill=(70, 70, 76))
    acesa = p.get("luz", "acesa") != "apagada"
    if acesa:
        E.glow(img, (W_ // 2, 60), 380, (255, 250, 225), 80)
    return img


FUNCOES = {
    "cozinha": cozinha, "sala_estar": sala_estar, "banheiro": banheiro, "porao": porao, "sotao": sotao,
    "hospital_quarto": hospital, "delegacia": delegacia, "escritorio": escritorio, "biblioteca": biblioteca,
    "mercadinho": mercadinho, "lanchonete": lanchonete, "laboratorio": laboratorio, "nave_espacial": nave,
    "recepcao_hotel": hotel, "gabinete": gabinete, "ginasio": ginasio, "teatro": teatro,
    "estacao_metro": metro, "caverna": caverna, "ponte": ponte, "rio": rio, "praia": praia, "praca": praca,
    "parque_diversoes": parque_diversoes, "estrada": estrada, "posto_gasolina": posto, "cemiterio": cemiterio,
    "beco": beco, "telhado": telhado, "fazenda": fazenda, "casa": casa,
    "corredor_escola": corredor_escola, "sala_escola": sala_escola,
}

CENARIOS = {
    "cozinha": {"o_que": "cozinha com azulejos, armários, janela e fogão", "extras": ""},
    "sala_estar": {"o_que": "sala com sofá, TV, cortinas, janela e quadro", "extras": "texto = escrito no quadro"},
    "banheiro": {"o_que": "banheiro com espelho grande e pia", "extras": "texto = escrito no espelho (vermelho)"},
    "porao": {"o_que": "porão de tijolos com escada, caixas e lâmpada pendurada", "extras": "texto = escrito na caixa"},
    "sotao": {"o_que": "sótão de madeira com janela redonda, baú e móvel coberto", "extras": ""},
    "hospital_quarto": {"o_que": "quarto de hospital com cama, monitor cardíaco e soro", "extras": ""},
    "delegacia": {"o_que": "delegacia com quadro de suspeitos ligados por fio vermelho e mesa", "extras": "texto = título do quadro"},
    "escritorio": {"o_que": "escritório com janelão para a cidade e computadores", "extras": "texto = nome da empresa"},
    "biblioteca": {"o_que": "biblioteca com estantes de livros coloridos", "extras": ""},
    "mercadinho": {"o_que": "mercadinho com prateleiras e letreiro", "extras": "texto = letreiro (padrão MERCADINHO)"},
    "lanchonete": {"o_que": "lanchonete anos 50 com letreiro neon, balcão e chão xadrez", "extras": "texto = neon (padrão LANCHES 24H); cor = cor do neon"},
    "laboratorio": {"o_que": "laboratório com telão, bancada e frascos brilhando", "extras": "texto = escrito no telão; cor = cor da tela"},
    "nave_espacial": {"o_que": "nave espacial com janela para o espaço, planeta e painel", "extras": "texto = aviso no painel; cor = cor do planeta"},
    "recepcao_hotel": {"o_que": "recepção de hotel antigo com quadro de chaves e balcão", "extras": "texto = placa (padrão RECEPÇÃO)"},
    "gabinete": {"o_que": "gabinete (prefeito, diretor, chefe) com bandeira, retrato e mesa grande", "extras": "texto = plaquinha na mesa; cor = cor da bandeira"},
    "ginasio": {"o_que": "ginásio com arquibancada, placar e quadra", "extras": "texto = placar (padrão CASA 0 x 0 VISITA)"},
    "teatro": {"o_que": "palco de teatro com cortina e holofote", "extras": "texto = título no alto; cor = cor da cortina"},
    "estacao_metro": {"o_que": "plataforma de metrô com placa e trilhos", "extras": "texto = nome da estação; cor = faixa da parede"},
    "caverna": {"o_que": "caverna com estalactites, túnel escuro e luz de tocha", "extras": "luz_cor = cor da tocha"},
    "ponte": {"o_que": "ponte suspensa de madeira entre penhascos, rio lá embaixo", "extras": "quebrada = true (ponte caída); texto = placa"},
    "rio": {"o_que": "margem de rio com árvores e pedras", "extras": "texto = placa"},
    "praia": {"o_que": "praia com mar, coqueiro e guarda-sol", "extras": "texto = escrito na areia; cor = guarda-sol"},
    "praca": {"o_que": "praça com coreto, bancos, árvores e poste", "extras": "texto = placa (padrão PRAÇA); relogio = true (torre do relógio, relogio_hora \"17:58\" com ponteiro vermelho); ceu_espelho = true (a cidade de cabeça pra baixo no céu, com gente)"},
    "parque_diversoes": {"o_que": "parque de diversões com roda-gigante e barraca listrada", "extras": "texto = nome na barraca; cor = listras"},
    "estrada": {"o_que": "estrada deserta até o horizonte com placa", "extras": "texto = placa (padrão KM 47)"},
    "posto_gasolina": {"o_que": "posto de gasolina com bombas e painel de preços", "extras": "texto = nome do posto; cor = cobertura"},
    "cemiterio": {"o_que": "cemitério com lápides, grade e árvore seca", "extras": "texto = escrito no portão"},
    "beco": {"o_que": "beco entre prédios com escada de incêndio, caçamba e pichação", "extras": "texto = pichação (padrão NÃO OLHE); cor = paredes"},
    "telhado": {"o_que": "telhado de prédio com caixa d'água e cidade ao fundo", "extras": "texto = escrito na caixa d'água"},
    "fazenda": {"o_que": "fazenda com celeiro, cerca e campo", "extras": "texto = nome no celeiro; cor = celeiro"},
    "corredor_escola": {"o_que": "corredor de escola com armários coloridos, mural de avisos, portas numeradas, luzes no teto e placa SAÍDA", "extras": "texto = placa da porta em destaque (padrão SALA 12); porta_longe = placa da porta do fundo (padrão SALA 13); desvio = desloca o ponto de fuga em px"},
    "sala_escola": {"o_que": "sala de aula vista da frente: lousa verde com texto em giz, relógio de ponteiro, janela, armário do fundo e carteiras", "extras": "texto = escrito na lousa (use \\n para quebrar linha); relogio_hora \"19:22\" (ponteiros); placa (padrão SALA 12); giz = cor do giz"},
    "casa": {"o_que": "casa de rua com telhado, varanda, janelas com cortina, cerca, árvore e poste", "extras": "texto = número da casa; cor = parede; porta = cor da porta; luz apagada = janela da direita apagada"},
}


def fundos(engine_mod):
    """Devolve {nome: função(params)} para registrar em engine.BACKGROUNDS."""
    global E
    E = engine_mod
    return {nome: (lambda f: (lambda p: acabamento(f(p or {}), p or {})))(f) for nome, f in FUNCOES.items()}
