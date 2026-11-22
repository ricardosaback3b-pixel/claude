"""Motor de vídeos @mundoemhistorias — histórias em partes, 1080x1920.
Uso: python3 engine.py roteiro.json saida_dir
Gera: video.mp4, capa.jpg, legenda.txt
"""
import json, math, os, random, subprocess, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FPS = 24
OV = 1.14  # sobra para movimento de câmera
BW, BH = int(W * OV), int(H * OV)
FONT_DIR = "/usr/share/fonts/truetype/google-fonts/ofl"
ANTON = f"{FONT_DIR}/anton/Anton-Regular.ttf"
MONT = f"{FONT_DIR}/montserrat/Montserrat[wght].ttf"
HANDLE = "@mundoemhistorias"
YELLOW = (255, 214, 0)
SR = 44100


def font(path, size, bold=False):
    f = ImageFont.truetype(path, size)
    if bold and "Montserrat" in path:
        try:
            f.set_variation_by_axes([800])
        except Exception:
            pass
    return f


# ---------------------------------------------------------------- fundos
def vgrad(w, h, top, bot):
    t = np.linspace(0, 1, h)[:, None, None]
    a = np.array(top, float)[None, None, :]
    b = np.array(bot, float)[None, None, :]
    arr = (a * (1 - t) + b * t).repeat(w, axis=1)
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def glow(img, xy, r, color, alpha=140):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x, y = xy
    d.ellipse([x - r, y - r, x + r, y + r], fill=color + (alpha,))
    lay = lay.filter(ImageFilter.GaussianBlur(r / 2.2))
    img.alpha_composite(lay)


def buildings(img, rng, base_y, palette, lit=(255, 200, 110), density=0.35):
    d = ImageDraw.Draw(img)
    x = -20
    while x < img.width:
        bw = rng.randint(140, 260)
        bh = rng.randint(500, 1150)
        col = rng.choice(palette)
        d.rectangle([x, base_y - bh, x + bw, base_y], fill=col)
        for wy in range(base_y - bh + 40, base_y - 60, 70):
            for wx in range(x + 22, x + bw - 40, 52):
                if rng.random() < density:
                    d.rectangle([wx, wy, wx + 26, wy + 38], fill=lit)
        x += bw + rng.randint(-10, 12)


def bg_street(night=True, sign="RUA 9", seed=3):
    rng = random.Random(seed)
    if night:
        img = vgrad(BW, BH, (8, 10, 32), (52, 24, 70)).convert("RGBA")
        pal = [(16, 16, 34), (22, 20, 44), (12, 14, 28)]
        lit = (255, 196, 102)
    else:
        img = vgrad(BW, BH, (255, 150, 92), (255, 216, 160)).convert("RGBA")
        pal = [(120, 70, 90), (140, 84, 100), (104, 60, 84)]
        lit = (255, 236, 170)
    d = ImageDraw.Draw(img)
    if night:
        for _ in range(70):
            sx, sy = rng.randint(0, BW), rng.randint(0, 700)
            d.ellipse([sx, sy, sx + 3, sy + 3], fill=(230, 230, 255))
        d.ellipse([BW - 330, 170, BW - 170, 330], fill=(240, 236, 210))
    else:
        glow(img, (BW // 2, 1150), 330, (255, 240, 200), 230)
    gy = 1500
    buildings(img, rng, gy, pal, lit, 0.3 if night else 0.15)
    d = ImageDraw.Draw(img)
    d.rectangle([0, gy, BW, gy + 90], fill=(40, 40, 56) if night else (150, 110, 110))
    d.rectangle([0, gy + 90, BW, BH], fill=(22, 22, 30) if night else (96, 70, 80))
    for x in range(40, BW, 260):
        d.rectangle([x, gy + 380, x + 140, gy + 400], fill=(210, 200, 120))
    # poste e ponto
    px = 170
    d.rectangle([px, 700, px + 22, gy + 40], fill=(30, 30, 40))
    d.rectangle([px, 700, px + 170, 722], fill=(30, 30, 40))
    if night:
        glow(img, (px + 160, 740), 200, (255, 214, 130), 120)
        d = ImageDraw.Draw(img)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).polygon([(px + 140, 730), (px + 180, 730), (px + 420, gy + 90), (px - 100, gy + 90)], fill=(255, 220, 150, 40))
        img.alpha_composite(lay)
        d = ImageDraw.Draw(img)
    sx = BW - 300
    d.rectangle([sx, 980, sx + 16, gy + 40], fill=(60, 60, 70))
    d.rounded_rectangle([sx - 90, 930, sx + 110, 1040], 14, fill=(20, 90, 60), outline=(240, 240, 240), width=6)
    f = font(ANTON, 58)
    d.text((sx + 8, 985), sign, font=f, fill=(255, 255, 255), anchor="mm")
    return img


def bg_bus_inside(seed=5, outside=(18, 30, 70)):
    rng = random.Random(seed)
    img = vgrad(BW, BH, (20, 46, 52), (8, 18, 22)).convert("RGBA")
    d = ImageDraw.Draw(img)
    # janelas
    for i in range(3):
        x0 = 60 + i * 400
        d.rounded_rectangle([x0, 330, x0 + 360, 900], 30, fill=outside, outline=(10, 14, 16), width=14)
        for _ in range(7):
            yy = rng.randint(360, 860)
            d.line([x0 + 20, yy, x0 + 340, yy - 30], fill=(255, 200, 120), width=3)
    # luzes do teto
    for x0 in range(80, BW, 330):
        d.rounded_rectangle([x0, 150, x0 + 220, 185], 10, fill=(200, 255, 230))
        glow(img, (x0 + 110, 170), 120, (170, 255, 220), 70)
    d = ImageDraw.Draw(img)
    # bancos
    for i in range(3):
        x0 = 80 + i * 400
        d.rounded_rectangle([x0, 1080, x0 + 300, 1420], 30, fill=(110, 30, 40), outline=(20, 10, 12), width=8)
        d.rounded_rectangle([x0 - 10, 1380, x0 + 320, 1480], 24, fill=(90, 24, 34), outline=(20, 10, 12), width=8)
    # barras
    for x0 in (360, 760):
        d.rectangle([x0, 120, x0 + 22, BH], fill=(230, 190, 40))
    d.rectangle([0, 250, BW, 270], fill=(230, 190, 40))
    d.rectangle([0, 1520, BW, BH], fill=(30, 34, 36))
    return img


def bg_bus_outside(number="", seed=3):
    img = bg_street(True, "RUA 9", seed)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 120, 1000, BW - 40, 1620
    d.rounded_rectangle([x0, y0, x1, y1], 50, fill=(200, 200, 190), outline=(20, 20, 24), width=12)
    d.rectangle([x0 + 10, y0 + 40, x1 - 10, y0 + 120], fill=(14, 14, 16))
    f = font(ANTON, 70)
    d.text(((x0 + x1) // 2, y0 + 80), number if number else "- - -", font=f, fill=(255, 140, 40) if number else (90, 90, 90), anchor="mm")
    for i in range(4):
        wx = x0 + 40 + i * 240
        d.rounded_rectangle([wx, y0 + 160, wx + 200, y0 + 380], 18, fill=(150, 255, 200))
    d.rectangle([x0, y0 + 430, x1, y0 + 460], fill=(160, 30, 40))
    for wx in (x0 + 150, x1 - 200):
        d.ellipse([wx - 70, y1 - 60, wx + 70, y1 + 80], fill=(16, 16, 18))
        d.ellipse([wx - 30, y1 - 20, wx + 30, y1 + 40], fill=(120, 120, 120))
    glow(img, (x0 + 30, y1 - 100), 90, (255, 250, 200), 200)
    return img


def bg_house(seed=8):
    rng = random.Random(seed)
    img = vgrad(BW, BH, (10, 12, 30), (30, 22, 50)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1450, BW, BH], fill=(16, 28, 20))
    hx, hy = 220, 700
    d.polygon([(hx - 60, hy + 200), (hx + 400, hy - 120), (hx + 860, hy + 200)], fill=(60, 30, 34))
    d.rectangle([hx, hy + 200, hx + 800, 1460], fill=(110, 90, 80), outline=(30, 20, 20), width=10)
    d.rectangle([hx + 90, hy + 340, hx + 330, hy + 600], fill=(255, 210, 120), outline=(30, 20, 20), width=10)
    d.rectangle([hx + 480, hy + 340, hx + 720, hy + 600], fill=(30, 30, 40), outline=(30, 20, 20), width=10)
    d.rectangle([hx + 330, hy + 560, hx + 470, 1460], fill=(70, 40, 30))
    glow(img, (hx + 210, hy + 470), 200, (255, 200, 110), 90)
    return img


def bg_dark(color=(10, 10, 16), spot=True):
    img = Image.new("RGBA", (BW, BH), color + (255,))
    if spot:
        glow(img, (BW // 2, BH // 2 - 100), 520, (90, 90, 120), 120)
    return img


def window_frame(img):
    """Moldura de janela de ônibus por cima (vista de dentro para fora)."""
    lay = Image.new("RGBA", img.size, (12, 30, 34, 255))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([90, 260, BW - 90, BH - 420], 70, fill=(0, 0, 0, 0))
    lay2 = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay2).rounded_rectangle([90, 260, BW - 90, BH - 420], 70, outline=(6, 10, 12, 255), width=26)
    img.alpha_composite(lay)
    img.alpha_composite(lay2)
    ImageDraw.Draw(img).rectangle([BW // 2 - 10, 260, BW // 2 + 10, BH - 420], fill=(6, 10, 12))


BACKGROUNDS = {
    "rua_noite": lambda p: bg_street(True, p.get("sign", "RUA 9")),
    "rua_amanhecer": lambda p: bg_street(False, p.get("sign", "RUA 9")),
    "onibus_dentro": lambda p: bg_bus_inside(),
    "onibus_fora": lambda p: bg_bus_outside(p.get("number", "")),
    "casa_noite": lambda p: bg_house(),
    "escuro": lambda p: bg_dark(),
}


def bg_corridor(seed=11):
    """Corredor de prédio com portas (perspectiva)."""
    img = vgrad(BW, BH, (40, 36, 30), (14, 12, 10)).convert("RGBA")
    d = ImageDraw.Draw(img)
    vx, vy = BW // 2, 900
    d.polygon([(0, 0), (BW, 0), (vx + 120, vy - 160), (vx - 120, vy - 160)], fill=(30, 28, 24))
    d.polygon([(0, BH), (BW, BH), (vx + 120, vy + 160), (vx - 120, vy + 160)], fill=(70, 40, 34))
    d.polygon([(0, 0), (vx - 120, vy - 160), (vx - 120, vy + 160), (0, BH)], fill=(120, 108, 84))
    d.polygon([(BW, 0), (vx + 120, vy - 160), (vx + 120, vy + 160), (BW, BH)], fill=(104, 94, 72))
    d.rectangle([vx - 120, vy - 160, vx + 120, vy + 160], fill=(10, 10, 12))
    for k, f in enumerate((0.15, 0.45, 0.7)):
        for side in (-1, 1):
            x = vx + side * (120 + (BW / 2 - 120) * (1 - f))
            w = 140 * (1 - f) + 30
            top = vy - 160 - (vy - 160) * (1 - f) * 0.55
            bot = vy + 160 + (BH - vy - 160) * (1 - f) * 0.45
            x0, x1 = sorted([x, x - side * w])
            d.rectangle([x0, top, x1, bot], fill=(60, 34, 24), outline=(20, 12, 8), width=6)
    for f in (0.2, 0.5, 0.75):
        y = (vy - 160) * f
        glow(img, (vx, int(y + 40)), int(140 * (1 - f) + 40), (255, 230, 160), 120)
    return img


def bg_elevator(floor="-1", seed=12):
    img = vgrad(BW, BH, (70, 72, 76), (40, 40, 44)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rectangle([140, 300, BW - 140, 1700], fill=(150, 152, 156), outline=(60, 60, 64), width=12)
    d.line([BW // 2, 300, BW // 2, 1700], fill=(60, 60, 64), width=10)
    d.rectangle([BW - 130, 700, BW - 30, 1100], fill=(40, 40, 44))
    for i in range(6):
        d.ellipse([BW - 105, 730 + i * 60, BW - 55, 780 + i * 60], fill=(200, 160, 60) if i == 2 else (90, 90, 96))
    d.rounded_rectangle([BW // 2 - 160, 150, BW // 2 + 160, 260], 20, fill=(10, 10, 10))
    d.text((BW // 2, 205), str(floor), font=font(ANTON, 80), fill=(255, 60, 40), anchor="mm")
    d.rectangle([0, 1700, BW, BH], fill=(30, 30, 32))
    glow(img, (BW // 2, 80), 300, (255, 255, 230), 110)
    return img


def bg_bedroom(seed=13):
    img = vgrad(BW, BH, (34, 30, 60), (18, 16, 30)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1500, BW, BH], fill=(60, 40, 34))
    d.rectangle([700, 360, 1080, 820], fill=(16, 22, 50), outline=(20, 14, 12), width=14)
    d.line([890, 360, 890, 820], fill=(20, 14, 12), width=10)
    d.ellipse([930, 420, 1010, 500], fill=(240, 236, 210))
    d.rounded_rectangle([60, 1180, 760, 1560], 30, fill=(70, 90, 150), outline=(20, 14, 12), width=10)
    d.rounded_rectangle([90, 1120, 330, 1240], 30, fill=(230, 230, 240), outline=(20, 14, 12), width=8)
    d.rectangle([880, 1300, 1120, 1520], fill=(110, 70, 44), outline=(20, 14, 12), width=8)
    d.polygon([(930, 1300), (1070, 1300), (1040, 1180), (960, 1180)], fill=(250, 220, 140))
    glow(img, (1000, 1240), 220, (255, 210, 120), 110)
    return img


def bg_forest(seed=14):
    rng = random.Random(seed)
    img = vgrad(BW, BH, (12, 26, 30), (4, 10, 12)).convert("RGBA")
    d = ImageDraw.Draw(img)
    glow(img, (BW // 2, 500), 380, (120, 160, 170), 90)
    d = ImageDraw.Draw(img)
    for layer, col in enumerate([(20, 40, 40), (12, 26, 26), (6, 14, 14)]):
        for _ in range(9):
            x = rng.randint(-100, BW + 100)
            w = rng.randint(40, 90) + layer * 25
            d.rectangle([x, 0, x + w, BH], fill=col)
    d.rectangle([0, 1600, BW, BH], fill=(8, 16, 10))
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).rectangle([0, 1100, BW, 1700], fill=(170, 190, 200, 50))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(80)))
    return img


def bg_school(seed=15, board="PROVA"):
    img = vgrad(BW, BH, (190, 170, 130), (150, 130, 100)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rectangle([90, 300, BW - 90, 900], fill=(30, 60, 44), outline=(110, 70, 40), width=24)
    d.text((BW // 2, 600), board, font=font(ANTON, 140 if len(board) <= 8 else max(60, int(1100 / max(1, len(board)) * 1.6))), fill=(230, 230, 220), anchor="mm")
    d.rectangle([0, 1450, BW, BH], fill=(110, 80, 60))
    for x in (60, 640):
        d.rectangle([x, 1250, x + 480, 1320], fill=(150, 100, 60), outline=(60, 40, 20), width=8)
        d.rectangle([x + 30, 1320, x + 60, 1560], fill=(60, 60, 64))
        d.rectangle([x + 420, 1320, x + 450, 1560], fill=(60, 60, 64))
    return img


BACKGROUNDS.update({
    "corredor_predio": lambda p: bg_corridor(),
    "elevador": lambda p: bg_elevator(p.get("floor", "-1")),
    "quarto_noite": lambda p: bg_bedroom(),
    "floresta_noite": lambda p: bg_forest(),
    "sala_aula": lambda p: bg_school(board=p.get("board", "PROVA")),
})


# ---------------------------------------------------------------- personagens
def draw_char(spec, s=1.0, mouth_state=None, blink=False):
    """Personagem cartoon. Com "sprite": usa a cartela do dono (assets/personagens) com expressões."""
    if spec.get("sprite"):
        import sprites
        eyes = "fechado" if blink else spec.get("eyes", "normal")
        mo = mouth_state or {"o": "o", "triste": "triste"}.get(spec.get("mouth", ""), "idle")
        modo = spec.get("enquadramento") or sprites.enquadramento_padrao(spec["sprite"])
        alt = int({"busto": 1850, "medio": 1300}.get(modo, 900) * s)
        im = sprites.render(spec["sprite"], alt, eyes, mo, spec.get("brows"), spec.get("flip", False),
                            "corpo" if modo == "medio" else modo)
        if spec.get("escuro"):
            r, g, b, a = im.split()
            dk = Image.merge("RGB", (r, g, b)).point(lambda v: int(v * 0.45))
            im = Image.merge("RGBA", (*dk.split(), a))
            dd = ImageDraw.Draw(im)
        return im
    cw, ch = int(560 * s), int(980 * s)
    im = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ol = (14, 12, 16)
    lw = max(3, int(9 * s))
    skin = tuple(spec.get("skin", (236, 188, 150)))
    cloth = tuple(spec.get("cloth", (60, 90, 170)))
    hair = tuple(spec.get("hair", (40, 26, 20)))
    cx = cw // 2
    # pernas
    d.rounded_rectangle([cx - 110 * s, 760 * s, cx - 20 * s, 975 * s], 30 * s, fill=(34, 34, 44), outline=ol, width=lw)
    d.rounded_rectangle([cx + 20 * s, 760 * s, cx + 110 * s, 975 * s], 30 * s, fill=(34, 34, 44), outline=ol, width=lw)
    # corpo
    d.rounded_rectangle([cx - 160 * s, 430 * s, cx + 160 * s, 800 * s], 90 * s, fill=cloth, outline=ol, width=lw)
    # braços
    d.rounded_rectangle([cx - 215 * s, 460 * s, cx - 130 * s, 740 * s], 40 * s, fill=cloth, outline=ol, width=lw)
    d.rounded_rectangle([cx + 130 * s, 460 * s, cx + 215 * s, 740 * s], 40 * s, fill=cloth, outline=ol, width=lw)
    d.ellipse([cx - 220 * s, 700 * s, cx - 140 * s, 780 * s], fill=skin, outline=ol, width=lw)
    d.ellipse([cx + 140 * s, 700 * s, cx + 220 * s, 780 * s], fill=skin, outline=ol, width=lw)
    if spec.get("uniform"):
        d.polygon([(cx - 50 * s, 440 * s), (cx, 540 * s), (cx + 50 * s, 440 * s)], fill=(240, 240, 240), outline=ol)
    if spec.get("jaleco"):
        d.polygon([(cx - 60 * s, 440 * s), (cx, 600 * s), (cx + 60 * s, 440 * s)], fill=tuple(spec.get("camisa", (110, 150, 200))), outline=ol)
        d.line([cx - 60 * s, 440 * s, cx - 20 * s, 640 * s], fill=ol, width=lw)
        d.line([cx + 60 * s, 440 * s, cx + 20 * s, 640 * s], fill=ol, width=lw)
        d.line([cx - 110 * s, 480 * s, cx - 70 * s, 640 * s], fill=(110, 120, 140), width=max(2, lw // 2))
        d.rectangle([cx + 55 * s, 560 * s, cx + 125 * s, 610 * s], fill=(250, 250, 250), outline=ol, width=max(2, lw // 2))
        d.rectangle([cx + 68 * s, 572 * s, cx + 100 * s, 598 * s], fill=(120, 150, 190))
    if spec.get("farda"):
        d.polygon([(cx - 40 * s, 440 * s), (cx, 500 * s), (cx + 40 * s, 440 * s)], fill=(230, 230, 220), outline=ol)
        for yy in (540, 600, 660):
            d.ellipse([cx - 9 * s, yy * s - 9 * s, cx + 9 * s, yy * s + 9 * s], fill=(200, 170, 80), outline=ol)
        d.rectangle([cx - 120 * s, 520 * s, cx - 50 * s, 560 * s], outline=ol, width=max(2, lw // 2))
        d.rectangle([cx + 50 * s, 520 * s, cx + 120 * s, 560 * s], outline=ol, width=max(2, lw // 2))
    if spec.get("moletom"):
        d.rounded_rectangle([cx - 120 * s, 420 * s, cx + 120 * s, 480 * s], 30 * s, fill=tuple(spec.get("cloth")), outline=ol, width=lw)
        d.line([cx - 35 * s, 470 * s, cx - 40 * s, 600 * s], fill=(235, 235, 235), width=max(3, int(10 * s)))
        d.line([cx + 35 * s, 470 * s, cx + 40 * s, 600 * s], fill=(235, 235, 235), width=max(3, int(10 * s)))
        d.rounded_rectangle([cx - 100 * s, 680 * s, cx + 100 * s, 780 * s], 20 * s, fill=tuple(int(c * 0.85) for c in spec.get("cloth")), outline=ol, width=max(2, lw // 2))
    if spec.get("mochila"):
        st = tuple(spec.get("mochila"))
        d.rounded_rectangle([cx - 130 * s, 440 * s, cx - 95 * s, 790 * s], 12 * s, fill=st, outline=ol, width=max(2, lw // 2))
        d.rounded_rectangle([cx + 95 * s, 440 * s, cx + 130 * s, 790 * s], 12 * s, fill=st, outline=ol, width=max(2, lw // 2))
    if spec.get("prop") == "papel":
        d.rectangle([cx + 150 * s, 640 * s, cx + 250 * s, 760 * s], fill=(245, 240, 220), outline=ol, width=lw)
    # cabeça
    hr = 175 * s
    hy = 255 * s
    style = spec.get("hairstyle", "curto")
    if style == "longo":
        d.rounded_rectangle([cx - hr - 20 * s, hy - hr, cx + hr + 20 * s, hy + hr + 150 * s], 120 * s, fill=hair, outline=ol, width=lw)
    if style == "capuz":
        d.ellipse([cx - hr - 40 * s, hy - hr - 40 * s, cx + hr + 40 * s, hy + hr + 50 * s], fill=cloth, outline=ol, width=lw)
    face = (20, 20, 26) if spec.get("shadow_face") else skin
    if spec.get("orelhas"):
        for sx in (-1, 1):
            ex = cx + sx * hr * 0.98
            d.ellipse([ex - 38 * s, hy - 10 * s, ex + 38 * s, hy + 70 * s], fill=face, outline=ol, width=lw)
    d.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=face, outline=ol, width=lw)
    if style in ("curto", "longo", "coque"):
        d.chord([cx - hr, hy - hr, cx + hr, hy + hr * 0.7], 180, 360, fill=hair, outline=ol, width=lw)
        if style == "coque":
            d.ellipse([cx - 60 * s, hy - hr - 90 * s, cx + 60 * s, hy - hr + 20 * s], fill=hair, outline=ol, width=lw)
    if style == "bone":
        cap = tuple(spec.get("cap", (30, 50, 110)))
        d.chord([cx - hr, hy - hr - 10 * s, cx + hr, hy + hr * 0.5], 180, 360, fill=cap, outline=ol, width=lw)
        d.rounded_rectangle([cx - hr - 10 * s, hy - 40 * s, cx + hr + 60 * s, hy - 5 * s], 15 * s, fill=cap, outline=ol, width=lw)
    if style == "careca":
        d.arc([cx - hr * 0.9, hy - hr * 0.2, cx - hr * 0.3, hy + hr * 0.5], 120, 240, fill=(220, 220, 220), width=int(30 * s))
        d.arc([cx + hr * 0.3, hy - hr * 0.2, cx + hr * 0.9, hy + hr * 0.5], 300, 60, fill=(220, 220, 220), width=int(30 * s))
    if style == "tigela":
        d.chord([cx - hr * 1.04, hy - hr * 1.08, cx + hr * 1.04, hy + hr * 0.62], 180, 360, fill=hair, outline=ol, width=lw)
        d.rectangle([cx - hr * 1.02, hy - hr * 0.25, cx + hr * 1.02, hy - hr * 0.2], fill=hair)
        d.line([cx - hr * 1.0, hy - hr * 0.2, cx + hr * 1.0, hy - hr * 0.2], fill=ol, width=lw)
    if style == "quepe":
        cap = tuple(spec.get("cap", (90, 100, 60)))
        d.chord([cx - hr * 0.95, hy - hr * 1.12, cx + hr * 0.95, hy + hr * 0.2], 180, 360, fill=cap, outline=ol, width=lw)
        d.rectangle([cx - hr * 1.0, hy - hr * 0.48, cx + hr * 1.0, hy - hr * 0.3], fill=tuple(int(c * 0.8) for c in cap), outline=ol, width=max(2, lw // 2))
        d.chord([cx - hr * 0.9, hy - hr * 0.5, cx + hr * 0.9, hy - hr * 0.1], 0, 180, fill=tuple(int(c * 0.7) for c in cap), outline=ol, width=max(2, lw // 2))
    brows = spec.get("brows")
    if brows and not spec.get("shadow_face"):
        by = hy - 60 * s
        for sx in (-1, 1):
            ex = cx + sx * 62 * s
            if brows == "preocupado":
                d.line([ex - 40 * s, by - sx * 0 - (12 * s if sx < 0 else -12 * s) * -1, ex + 40 * s, by + (12 * s if sx < 0 else -12 * s) * -1], fill=ol, width=int(lw * 1.6))
            elif brows == "bravo":
                d.line([ex - 40 * s, by - (12 * s if sx > 0 else -12 * s), ex + 40 * s, by + (12 * s if sx > 0 else -12 * s)], fill=ol, width=int(lw * 1.6))
            else:
                d.line([ex - 40 * s, by, ex + 40 * s, by], fill=ol, width=int(lw * 1.6))
    # olhos
    eyes = spec.get("eyes", "normal")
    ey = hy + 10 * s
    for sx in (-1, 1):
        ex = cx + sx * 62 * s
        if spec.get("shadow_face"):
            d.ellipse([ex - 18 * s, ey - 10 * s, ex + 18 * s, ey + 10 * s], fill=(255, 250, 200))
            continue
        if eyes == "fechado":
            d.arc([ex - 30 * s, ey - 20 * s, ex + 30 * s, ey + 20 * s], 20, 160, fill=ol, width=lw)
            continue
        r = 44 * s if eyes == "arregalado" else 34 * s
        d.ellipse([ex - r * 0.8, ey - r, ex + r * 0.8, ey + r], fill=(255, 255, 255), outline=ol, width=lw)
        pr = 13 * s if eyes == "arregalado" else 16 * s
        off = spec.get("look", 0) * 10 * s
        d.ellipse([ex - pr + off, ey - pr, ex + pr + off, ey + pr], fill=ol)
    if spec.get("age"):
        for sx in (-1, 1):
            ex = cx + sx * 62 * s
            d.arc([ex - 40 * s, ey + 30 * s, ex + 40 * s, ey + 60 * s], 20, 160, fill=(150, 100, 80), width=max(2, int(4 * s)))
    # boca
    if not spec.get("shadow_face"):
        mouth = spec.get("mouth", "neutra")
        my = hy + 100 * s
        if mouth == "o":
            d.ellipse([cx - 22 * s, my - 26 * s, cx + 22 * s, my + 26 * s], fill=(60, 16, 20), outline=ol, width=lw)
        elif mouth == "sorriso":
            d.arc([cx - 55 * s, my - 45 * s, cx + 55 * s, my + 25 * s], 20, 160, fill=ol, width=lw)
        elif mouth == "triste":
            d.arc([cx - 45 * s, my, cx + 45 * s, my + 50 * s], 200, 340, fill=ol, width=lw)
        else:
            d.line([cx - 36 * s, my, cx + 36 * s, my], fill=ol, width=lw)
    if spec.get("bigode") and not spec.get("shadow_face"):
        my = hy + 72 * s
        d.chord([cx - 60 * s, my - 18 * s, cx + 60 * s, my + 26 * s], 180, 360, fill=tuple(spec.get("bigode")), outline=ol, width=max(2, lw // 2))
    if spec.get("flip"):
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im


# ---------------------------------------------------------------- objetos
def prop_layer(prop):
    lay = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
    if not prop:
        return lay
    d = ImageDraw.Draw(lay)
    kind = prop["type"]
    if kind in ("lista", "bilhete", "carta"):
        pw, ph = (760, 980) if kind != "bilhete" else (700, 520)
        x0, y0 = (BW - pw) // 2, 520
        d.rectangle([x0 + 18, y0 + 18, x0 + pw + 18, y0 + ph + 18], fill=(0, 0, 0, 120))
        d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=(240, 232, 206), outline=(60, 50, 40), width=6)
        f = font(MONT, 46, True)
        ft = font(ANTON, 70)
        y = y0 + 50
        if prop.get("title"):
            d.text((x0 + pw // 2, y + 30), prop["title"], font=ft, fill=(40, 30, 30), anchor="mm")
            y += 120
        for line in prop.get("lines", []):
            hl = line.startswith("!")
            txt = line.lstrip("!")
            col = (190, 20, 30) if hl else (50, 40, 40)
            d.text((x0 + 60, y), txt, font=f, fill=col)
            if line.startswith("~"):
                d.line([x0 + 50, y + 30, x0 + pw - 60, y + 30], fill=(40, 30, 30), width=6)
            y += 78
    elif kind == "celular":
        x0, y0, pw, ph = BW // 2 - 280, 460, 560, 1040
        d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], 60, fill=(14, 14, 18), outline=(80, 80, 90), width=10)
        d.rounded_rectangle([x0 + 26, y0 + 70, x0 + pw - 26, y0 + ph - 60], 30, fill=(30, 36, 50))
        f = font(MONT, 52, True)
        ft = font(ANTON, 84)
        d.text((x0 + pw // 2, y0 + 300), prop.get("title", ""), font=ft, fill=(255, 255, 255), anchor="mm")
        for i, line in enumerate(prop.get("lines", [])):
            d.text((x0 + pw // 2, y0 + 440 + i * 80), line, font=f, fill=(200, 210, 230), anchor="mm")
        d.ellipse([x0 + 90, y0 + ph - 240, x0 + 230, y0 + ph - 100], fill=(220, 50, 50))
        d.ellipse([x0 + pw - 230, y0 + ph - 240, x0 + pw - 90, y0 + ph - 100], fill=(40, 200, 90))
    elif kind == "placa":
        x0, y0 = 120, 500
        d.rounded_rectangle([x0, y0, BW - 120, y0 + 330], 30, fill=(12, 12, 14), outline=(255, 140, 40), width=10)
        f = font(ANTON, 110)
        d.text((BW // 2, y0 + 165), prop.get("title", ""), font=f, fill=(255, 140, 40), anchor="mm")
    return lay


# ---------------------------------------------------------------- texto
def split_chunks(text):
    """Legenda em blocos de 1 a 3 palavras. *palavra* = destaque."""
    words = text.split()
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        clean = w.strip("*")
        end = clean[-1:] in ".!?…:,"
        if len(cur) >= 3 or end or (len(cur) >= 2 and len(clean) > 7):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for c in chunks:
        n = sum(1 for _ in c)
        last = c[-1].strip("*")
        dur = 0.2 + 0.27 * n
        if last[-1:] in ".!?…":
            dur += 0.38
        elif last[-1:] in ",:":
            dur += 0.15
        out.append((c, dur))
    return out


_cap_cache = {}


def caption_img_ep(words):
    """Legenda dos episódios: letra normal, branca, contorno azul-marinho, palavra-chave amarela."""
    key = ("ep",) + tuple(words)
    if key in _cap_cache:
        return _cap_cache[key]
    f = font(MONT, 92, True)
    parts = [(w.replace("*", ""), w.startswith("*")) for w in words]
    lines, cur, curw = [], [], 0
    for txt, hl in parts:
        tw = f.getlength(txt + " ")
        if cur and curw + tw > W - 140:
            lines.append(cur); cur, curw = [], 0
        cur.append((txt, hl)); curw += tw
    lines.append(cur)
    lh = 112
    im = Image.new("RGBA", (W, lh * len(lines) + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for li, line in enumerate(lines):
        total = sum(f.getlength(t + " ") for t, _ in line) - f.getlength(" ")
        x = (W - total) / 2
        y = 30 + li * lh
        for t, hl in line:
            d.text((x, y), t, font=f, fill=YELLOW if hl else (255, 255, 255), stroke_width=11, stroke_fill=(22, 40, 92))
            x += f.getlength(t + " ")
    _cap_cache[key] = im
    return im


def caption_img(words, color_hl=YELLOW):
    key = tuple(words)
    if key in _cap_cache:
        return _cap_cache[key]
    f = font(ANTON, 118)
    parts = []
    for w in words:
        hl = w.startswith("*") and w.rstrip(".,!?…:").endswith("*")
        txt = w.replace("*", "").upper()
        parts.append((txt, hl))
    # quebra em até 2 linhas
    lines, cur, curw = [], [], 0
    for txt, hl in parts:
        tw = f.getlength(txt + " ")
        if cur and curw + tw > W - 140:
            lines.append(cur)
            cur, curw = [], 0
        cur.append((txt, hl))
        curw += tw
    lines.append(cur)
    lh = 140
    im = Image.new("RGBA", (W, lh * len(lines) + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for li, line in enumerate(lines):
        total = sum(f.getlength(t + " ") for t, _ in line) - f.getlength(" ")
        x = (W - total) / 2
        y = 30 + li * lh
        for t, hl in line:
            d.text((x, y), t, font=f, fill=color_hl if hl else (255, 255, 255), stroke_width=12, stroke_fill=(0, 0, 0))
            x += f.getlength(t + " ")
    _cap_cache[key] = im
    return im


# ---------------------------------------------------------------- cena
def build_scene(sc):
    p = sc.get("bg_params", {})
    img = BACKGROUNDS[sc["bg"]](p)
    if sc.get("window"):
        window_frame(img)
    for c in sc.get("chars", []):
        if c.get("sprite"):
            continue  # cartela: desenhado quadro a quadro (boca, piscada, respiração)
        ci = draw_char(c, c.get("scale", 1.0))
        x = int(c.get("x", 0.5) * BW - ci.width / 2)
        y = int((c.get("y", 0.86) - 0.07) * BH - ci.height)
        img.alpha_composite(ci, (x, y))
    img.alpha_composite(prop_layer(sc.get("prop")))
    # vinheta
    v = Image.new("L", (BW, BH), 0)
    ImageDraw.Draw(v).ellipse([-BW * 0.25, -BH * 0.15, BW * 1.25, BH * 1.15], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(160))
    dark = Image.new("RGBA", (BW, BH), (0, 0, 0, 255))
    dark.putalpha(Image.eval(v, lambda a: int((255 - a) * 0.75)))
    img.alpha_composite(dark)
    if sc.get("tint"):
        t = Image.new("RGBA", (BW, BH), tuple(sc["tint"]) + (60,))
        img.alpha_composite(t)
    return img.convert("RGB")


def camera(img, cam, t):
    """t de 0 a 1 dentro da cena."""
    e = 0.5 - 0.5 * math.cos(math.pi * t)
    z0, z1 = {"in": (1.0, 1.1), "out": (1.1, 1.0), "zoom_forte": (1.0, 1.3)}.get(cam, (1.03, 1.03))
    z = z0 + (z1 - z0) * e
    cw = W / z
    chh = H / z
    cx, cy = BW / 2, BH / 2
    mx = (BW - cw) / 2
    if cam == "pan_l":
        cx = BW / 2 + mx * (1 - 2 * e) * 0.9
    elif cam == "pan_r":
        cx = BW / 2 - mx * (1 - 2 * e) * 0.9
    if cam == "shake":
        cx += math.sin(t * 90) * 14
        cy += math.cos(t * 70) * 10
    x0 = min(max(cx - cw / 2, 0), BW - cw)
    y0 = min(max(cy - chh / 2, 0), BH - chh)
    return img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + chh))


_tv_lines = None


def filtro_tv(frame, ft, rng=np.random.default_rng(7)):
    """Filtro de câmera de segurança / TV velha: cor lavada, linhas, chiado, faixa rolando, CAM e REC."""
    global _tv_lines
    a = np.asarray(frame.convert("RGB")).astype(np.float32)
    g = a.mean(axis=2, keepdims=True)
    a = a * 0.45 + g * 0.55
    a[..., 1] *= 1.06
    a[..., 2] *= 0.92
    if _tv_lines is None:
        _tv_lines = np.ones((H, 1, 1), np.float32)
        _tv_lines[::4] = 0.72
        _tv_lines[1::4] = 0.86
    a *= _tv_lines
    a += rng.normal(0, 14, (H // 2, W // 2, 1)).repeat(2, 0).repeat(2, 1)
    yb = int((ft * 260) % (H + 200)) - 100
    a[max(0, yb):max(0, yb + 60)] += 22
    a = np.roll(a, 3, axis=1) * 0.5 + a * 0.5
    yy, xx = np.ogrid[:H, :W]
    vig = 1 - 0.45 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    a *= np.clip(vig, 0.35, 1)[..., None]
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(out)
    f = font(MONT, 40, True)
    d.text((50, 320), "CAM 03", font=f, fill=(235, 235, 235))
    if int(ft * 2) % 2 == 0:
        d.ellipse([W - 230, 312, W - 200, 342], fill=(230, 40, 40))
    d.text((W - 185, 327), "REC", font=f, fill=(235, 235, 235), anchor="lm")
    seg = int(ft) % 60
    d.text((50, 380), f"23:59:{seg:02d}", font=font(MONT, 34, True), fill=(220, 220, 220))
    return out


def overlay_static_ep(meta):
    """Topo dos episódios: @ no canto, faixa branca 'PARTE N · ...' e faixa amarela de votação."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((40, 200), HANDLE, font=font(MONT, 36, True), fill=(255, 255, 255, 235), anchor="lm",
           stroke_width=3, stroke_fill=(0, 0, 0, 140))
    y = 455
    f1 = font(MONT, 46, True)
    t1 = meta.get("faixa") or f"PARTE {meta['part']} · {meta['title'].upper()}"
    while f1.getlength(t1) > W - 160 and f1.size > 30:
        f1 = font(MONT, f1.size - 2, True)
    tw = f1.getlength(t1)
    d.rounded_rectangle([W / 2 - tw / 2 - 30, y - 42, W / 2 + tw / 2 + 30, y + 42], 20, fill=(248, 248, 248, 250))
    d.text((W / 2, y), t1, font=f1, fill=(28, 28, 34), anchor="mm")
    if meta.get("vote"):
        y += 92
        t2 = "NO FINAL VOCÊ DECIDE: A ou B"
        f2 = font(MONT, 44, True)
        tw = f2.getlength(t2)
        d.rounded_rectangle([W / 2 - tw / 2 - 30, y - 40, W / 2 + tw / 2 + 30, y + 40], 20, fill=(246, 206, 72, 250))
        d.text((W / 2, y), t2, font=f2, fill=(28, 28, 34), anchor="mm")
    return lay


def overlay_static(meta):
    if meta.get("estilo") == "andar":
        return overlay_static_ep(meta)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = font(ANTON, 52)
    label = f"PARTE {meta['part']}/{meta['total']}" if meta.get("total") else f"PARTE {meta['part']}"
    tw = f.getlength(label)
    d.rounded_rectangle([W / 2 - tw / 2 - 30, 110, W / 2 + tw / 2 + 30, 190], 40, fill=(200, 20, 40, 230))
    d.text((W / 2, 150), label, font=f, fill=(255, 255, 255), anchor="mm")
    ft = font(MONT, 40, True)
    d.text((W / 2, 235), meta["title"].upper(), font=ft, fill=(255, 255, 255, 230), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    fh = font(MONT, 34, True)
    d.text((W - 40, 560), HANDLE, font=fh, fill=(255, 255, 255, 170), anchor="rm", stroke_width=3, stroke_fill=(0, 0, 0, 170))
    return lay


def end_card(meta, base):
    im = base.copy().convert("RGBA")
    im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 175)))
    d = ImageDraw.Draw(im)
    fs = font(MONT, 52, True)
    fb = font(ANTON, 80)
    nxt = meta["part"] + 1
    if meta.get("final"):
        f = font(ANTON, 210)
        d.text((W / 2, 700), "FIM.", font=f, fill=YELLOW, anchor="mm", stroke_width=14, stroke_fill=(0, 0, 0))
        y = 880
        for line in ["Tem história nova toda hora", "no perfil"]:
            d.text((W / 2, y), line, font=fs, fill=(255, 255, 255), anchor="mm")
            y += 70
        y += 40
    else:
        top = 620 if meta.get("vote") else 700
        f = font(ANTON, 190 if meta.get("vote") else 210)
        big = "A OU B?" if meta.get("vote") else f"PARTE {nxt}"
        d.text((W / 2, top), big, font=f, fill=YELLOW, anchor="mm", stroke_width=14, stroke_fill=(0, 0, 0))
        y = top + 160
        if meta.get("vote"):
            d.text((W / 2, y), f"Comenta! A mais votada decide a Parte {nxt}", font=font(MONT, 42, True), fill=(255, 255, 255), anchor="mm")
            y += 75
            fo = font(MONT, 46, True)
            for lab, opt in zip("AB", meta.get("options", [])):
                for k, line in enumerate(wrap(f"{lab}) {opt}", fo, W - 200)):
                    d.text((W / 2, y), line, font=fo, fill=YELLOW if k == 0 else (255, 255, 255), anchor="mm")
                    y += 60
                y += 10
            y += 20
        d.text((W / 2, y), f"A Parte {nxt} fica no perfil", font=fs, fill=(255, 255, 255), anchor="mm")
        y += 85
        d.text((W / 2, y), HANDLE, font=font(ANTON, 92), fill=YELLOW, anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
        y += 85
        d.text((W / 2, y), "Ainda não saiu? Chega em até 24h", font=font(MONT, 40, True), fill=(220, 220, 220), anchor="mm")
        y += 80
    d.rounded_rectangle([140, y, W - 140, y + 150], 75, fill=(200, 20, 40))
    d.text((W / 2, y + 75), "SEGUE PRA NÃO PERDER", font=fb, fill=(255, 255, 255), anchor="mm")
    return im.convert("RGB")


def wrap(text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if f.getlength(t) > maxw and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- áudio
def synth_audio(total, cuts, hooks, end_t, mood="suspense", seed=1):
    rng = np.random.default_rng(seed)
    n = int(total * SR)
    t = np.arange(n) / SR
    base = {"suspense": 55.0, "triste": 65.4, "tensao": 49.0}.get(mood, 55.0)
    drone = np.zeros(n)
    for k, (mult, amp) in enumerate([(1, 0.5), (1.5, 0.22), (2.0, 0.16), (2.997, 0.06)]):
        f = base * mult
        drone += amp * np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.07 * t * (k + 1)))
    drone *= 0.55 + 0.45 * np.sin(2 * np.pi * 0.11 * t) ** 2
    # batida de coração
    beat = np.zeros(n)
    period = 0.85
    for st in np.arange(0.4, total, period):
        for off, a in ((0, 1.0), (0.22, 0.65)):
            i0 = int((st + off) * SR)
            ln = int(0.18 * SR)
            if i0 + ln < n:
                tt = np.arange(ln) / SR
                beat[i0:i0 + ln] += a * np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 28)
    sfx = np.zeros(n)
    for c in cuts:
        i0 = int(c * SR)
        ln = int(0.45 * SR)
        if i0 + ln < n:
            nz = rng.standard_normal(ln)
            nz = np.convolve(nz, np.ones(25) / 25, mode="same")
            env = np.sin(np.linspace(0, np.pi, ln)) ** 2
            sfx[i0:i0 + ln] += 0.6 * nz * env
    for h in hooks:
        i0 = int(h * SR)
        ln = int(1.6 * SR)
        if i0 + ln < n:
            tt = np.arange(ln) / SR
            sfx[i0:i0 + ln] += 0.9 * np.sin(2 * np.pi * (60 - 25 * tt) * tt) * np.exp(-tt * 2.2)
    # subida final
    i0 = int(max(0, end_t - 3.0) * SR)
    i1 = int(end_t * SR)
    if i1 > i0:
        tt = np.arange(i1 - i0) / SR
        nz = rng.standard_normal(i1 - i0)
        sfx[i0:i1] += 0.35 * nz * (tt / tt[-1]) ** 2 + 0.2 * np.sin(2 * np.pi * (200 + 300 * tt) * tt) * (tt / tt[-1])
    mix = 0.35 * drone + 0.55 * beat + sfx
    fade = int(0.8 * SR)
    mix[:fade] *= np.linspace(0, 1, fade)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.85
    st = np.stack([mix, mix * 0.97], axis=1)
    return (st * 32767).astype(np.int16)


# ---------------------------------------------------------------- render
def speaker_tag_ep(name):
    key = ("tagep", name)
    if key in _cap_cache:
        return _cap_cache[key]
    f = font(MONT, 46, True)
    tw = int(f.getlength(name.upper()))
    im = Image.new("RGBA", (tw + 64, 74), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, tw + 63, 73], 37, fill=(150, 200, 240, 245))
    d.text(((tw + 64) / 2, 37), name.upper(), font=f, fill=(22, 40, 92), anchor="mm")
    _cap_cache[key] = im
    return im


def speaker_tag(name, color):
    key = ("tag", name, tuple(color))
    if key in _cap_cache:
        return _cap_cache[key]
    f = font(ANTON, 54)
    tw = int(f.getlength(name.upper()))
    im = Image.new("RGBA", (tw + 60, 84), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, tw + 59, 83], 40, fill=tuple(color) + (235,), outline=(0, 0, 0), width=5)
    d.text(((tw + 60) / 2, 42), name.upper(), font=f, fill=(255, 255, 255), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    _cap_cache[key] = im
    return im


def build_timeline(meta, scenes):
    """Retorna (timeline, voz_track, t_fim). timeline: [(si, start, dur, eventos)]
    eventos: [(palavras, inicio, dur, nome_falante, cor)]."""
    use_voice = not meta.get("sem_voz")
    vozes = meta.get("vozes", {})
    nomes = meta.get("nomes", {})
    cores = meta.get("cores", {})
    narr = meta.get("narrador")
    clips = []
    timeline = []
    t = 0.0
    for i, sc in enumerate(scenes):
        lines = sc.get("linhas") or [{"voz": narr, "texto": sc["text"]}]
        start = t
        pos = t + 0.15
        events = []
        for ln in lines:
            who = ln.get("voz") or narr
            chunks = split_chunks(ln["texto"])
            if use_voice:
                import tts
                spec = vozes.get(who) or {"voz": "kokoro:pm_alex"}
                a = tts.synth(spec, ln["texto"])
                ldur = len(a) / SR
                clips.append((pos, a, who, who != narr or bool(ln.get("fala"))))
                w = [sum(len(x.strip("*")) for x in c) + 2 for c, _ in chunks]
                tot = sum(w)
                cs = pos
                for (c, _), wi in zip(chunks, w):
                    cd = ldur * wi / tot
                    label = nomes.get(who) if who and who != narr else None
                    events.append((c, cs, cd, label, cores.get(who, (200, 20, 40))))
                    cs += cd
                pos += ldur + 0.28
            else:
                for c, cd in chunks:
                    label = nomes.get(who) if who and who != narr else None
                    events.append((c, pos, cd, label, cores.get(who, (200, 20, 40))))
                    pos += cd
        dur = max(1.6, pos - start + sc.get("hold", 0.15))
        timeline.append((i, start, dur, events))
        t = start + dur
    voice = np.zeros(int((t + 6) * SR), dtype=np.float32)
    for st, a, _, _ in clips:
        i0 = int(st * SR)
        voice[i0:i0 + len(a)] += a[: len(voice) - i0]
    # envelope de fala por personagem (para mexer a boca), um valor por quadro
    nfr = int((t + 6) * FPS)
    env = {}
    hop = SR // FPS
    for st, a, who, anim in clips:
        if not anim or not who:
            continue
        arr = env.setdefault(who, np.zeros(nfr, dtype=np.float32))
        f0 = int(st * FPS)
        for k in range(len(a) // hop):
            seg = a[k * hop:(k + 1) * hop]
            if f0 + k < nfr:
                arr[f0 + k] = max(arr[f0 + k], float(np.sqrt(np.mean(seg * seg))))
    meta["_env"] = env
    return timeline, voice, t


def render(script, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    meta = script["meta"]
    scenes = script["scenes"]
    timeline, voice, t = build_timeline(meta, scenes)
    end_len = 4.5 if meta.get("vote") else 3.0
    total = t + end_len
    imgs = [build_scene(sc) for sc in scenes]
    over = overlay_static(meta)
    cuts = [st for _, st, _, _ in timeline[1:]]
    hooks = [st for i, st, _, _ in timeline if scenes[i].get("hook")]
    bg = synth_audio(total, cuts, hooks, t, meta.get("mood", "suspense"), seed=meta.get("part", 1)).astype(np.float32) / 32767
    n = bg.shape[0]
    v = voice[:n]
    if len(v) < n:
        v = np.pad(v, (0, n - len(v)))
    has_voice = np.max(np.abs(v)) > 0.01
    gain = 0.32 if has_voice else 1.0
    mix = bg * gain + v[:, None] * 0.95
    mix = mix / max(1.0, float(np.max(np.abs(mix))) / 0.97)
    audio = (mix * 32767).astype(np.int16)
    wav = os.path.join(out_dir, "audio.wav")
    with wave.open(wav, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(audio.tobytes())
    mp4 = os.path.join(out_dir, "video.mp4")
    proc = subprocess.Popen([
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    nframes = int(total * FPS)
    sprite_cache = {}
    last_frame = None
    cover_frame = None
    for fi in range(nframes):
        ft = fi / FPS
        if ft >= t:
            if last_frame is None:
                continue
            proc.stdin.write(end_card(meta, last_frame).tobytes())
            continue
        k = max(j for j, (_, st, _, _) in enumerate(timeline) if st <= ft)
        si, st, dur, events = timeline[k]
        sc = scenes[si]
        src = imgs[si]
        dyn = [c for c in sc.get("chars", []) if c.get("sprite")]
        if dyn:
            src = src.copy()
            for ci_, c in enumerate(dyn):
                ref = c.get("_ref")
                env = meta.get("_env", {}).get(ref)
                lvl = float(env[fi]) if env is not None and fi < len(env) else 0.0
                ms = "aberta" if lvl > 0.16 else ("meia" if lvl > 0.05 else None)
                if ms is None and env is not None and fi < len(env) and float(env[max(0, fi - 2):fi + 3].max()) > 0.05:
                    ms = "fechada"
                ph = (hash(ref or ci_) % 100) / 100 * 3.0
                blink = ((ft + ph) % 3.6) < 0.12
                key = (si, ci_, ms, blink)
                if key not in sprite_cache:
                    sprite_cache[key] = draw_char(c, c.get("scale", 1.0), mouth_state=ms, blink=blink)
                spr = sprite_cache[key]
                bob = math.sin(ft * 2.2 + ph) * 5
                import sprites as _sp
                x = int(c.get("x", 0.5) * BW - spr.width / 2)
                _md = c.get("enquadramento") or _sp.enquadramento_padrao(c["sprite"])
                if _md == "medio":  # plano médio dos episódios: cabeça em ~31% da tela, pernas saem por baixo
                    y = int(BH * c.get("y", 0.325) + bob)
                elif _sp.e_busto(c["sprite"], c.get("enquadramento")):  # busto: encostado na base da tela, como nos vídeos originais
                    y = int(BH * c.get("y", 0.25) + bob)  # topo do busto; rosto perto do meio da tela
                else:
                    y = int((c.get("y", 0.86) - 0.07) * BH - spr.height + bob)
                src.paste(spr, (x, y), spr)
        frame = camera(src, sc.get("cam", "in"), (ft - st) / dur).convert("RGBA")
        if sc.get("filtro") == "tv":
            frame = filtro_tv(frame, ft)
        if ft - st < 0.12 and k > 0:
            frame.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(110 * (1 - (ft - st) / 0.12)))))
        frame.alpha_composite(over)
        for words, es, ed, label, col in events:
            if es <= ft < es + ed:
                ep = meta.get("estilo") == "andar"
                ci = caption_img_ep(words) if ep else caption_img(words)
                age = ft - es
                sc_ = 1.0 + max(0.0, 0.18 * (1 - age / 0.12))
                if sc_ > 1.001:
                    ci = ci.resize((int(ci.width * sc_), int(ci.height * sc_)), Image.BILINEAR)
                cy = int(1450 - ci.height / 2)
                frame.alpha_composite(ci, (int(W / 2 - ci.width / 2), cy))
                if label:
                    tg = speaker_tag_ep(label) if ep else speaker_tag(label, col)
                    frame.alpha_composite(tg, (int(W / 2 - tg.width / 2), cy - 70))
                break
        rgb = frame.convert("RGB")
        last_frame = rgb
        if sc.get("cover") and cover_frame is None and ft - st > dur * 0.5:
            cover_frame = camera(src, sc.get("cam", "in"), 0.5)
        proc.stdin.write(rgb.tobytes())
    proc.stdin.close()
    proc.wait()
    os.remove(wav)
    make_cover(meta, cover_frame or camera(imgs[0], "in", 0.5), os.path.join(out_dir, "capa.jpg"))
    with open(os.path.join(out_dir, "legenda.txt"), "w") as f:
        f.write(script["caption"])
    return mp4, total


def make_cover(meta, base, path):
    """Capa: título da história + frase da parte + PARTE N. Tudo dentro do recorte 3:4 do feed (y 240–1680)."""
    im = base.convert("RGBA")
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for y in range(0, 1150):
        gd.line([0, y, W, y], fill=(0, 0, 0, int(max(0, 215 - y / 5.4))))
    im.alpha_composite(g)
    d = ImageDraw.Draw(im)
    ft = font(ANTON, 118)
    y = 330
    for line in wrap(meta["title"].upper(), ft, W - 120):
        d.text((W / 2, y), line, font=ft, fill=YELLOW, anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
        y += 128
    y += 10
    fp = font(ANTON, 96)
    label = f"PARTE {meta['part']}" + (" · FINAL" if meta.get("final") else "")
    tw = fp.getlength(label)
    d.rounded_rectangle([W / 2 - tw / 2 - 44, y - 62, W / 2 + tw / 2 + 44, y + 70], 60, fill=(200, 20, 40), outline=(0, 0, 0), width=6)
    d.text((W / 2, y + 4), label, font=fp, fill=(255, 255, 255), anchor="mm")
    y += 150
    fc = font(ANTON, 92)
    for line in wrap(meta["cover_text"].upper(), fc, W - 140):
        d.text((W / 2, y), line, font=fc, fill=(255, 255, 255), anchor="mm", stroke_width=9, stroke_fill=(0, 0, 0))
        y += 104
    im.convert("RGB").save(path, quality=90)


if __name__ == "__main__":
    with open(sys.argv[1]) as fh:
        sc = json.load(fh)
    mp4, dur = render(sc, sys.argv[2])
    print(mp4, round(dur, 1), "s")
