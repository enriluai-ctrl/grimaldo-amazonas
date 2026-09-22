# Infografia "Propuesta Integral" — Salud + Educacion Amazonas (Prof. Grimaldo)
# Genera material/propuesta-integral.png (1080 px de ancho, vertical, para celular)
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(BASE, "propuesta-integral.png")

W = 1080
MARGEN = 56
CONTENIDO = W - MARGEN * 2
PAD = 36
TEXTO_W = CONTENIDO - PAD * 2

# Paleta (misma identidad que el hub)
VERDE_OSC = (7, 40, 29)
VERDE = (14, 122, 95)
VERDE_CLARO = (217, 242, 231)
CREMA = (244, 239, 227)
TINTA = (29, 42, 37)
GRIS = (90, 107, 100)
AMBAR = (185, 122, 20)
BLANCO = (255, 255, 255)


def F(ruta, tam):
    for cand in ruta:
        p = "C:/Windows/Fonts/" + cand
        if os.path.exists(p):
            return ImageFont.truetype(p, tam)
    return ImageFont.load_default()


def bold(t): return F(["segoeuib.ttf", "arialbd.ttf", "arial.ttf"], t)
def reg(t): return F(["segoui.ttf", "segoeui.ttf", "arial.ttf"], t)
def semi(t): return F(["segouisb.ttf", "segoeuib.ttf", "arialbd.ttf"], t)


def wrap(drawer, texto, font, max_w):
    palabras, lineas, actual = texto.split(), [], ""
    for p in palabras:
        prueba = (actual + " " + p).strip()
        if drawer.textlength(prueba, font=font) <= max_w:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    return lineas or [""]


def tarjeta_sombra(im, caja, radius=26):
    """Sombra suave debajo de la tarjeta."""
    capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    x0, y0, x1, y1 = caja
    d.rounded_rectangle([x0 + 4, y0 + 14, x1 + 4, y1 + 14], radius=radius, fill=(7, 40, 29, 70))
    capa = capa.filter(ImageFilter.GaussianBlur(10))
    im.alpha_composite(capa)


def dib_tarjeta(im, y, titulo, accent, stats, bullets):
    """Dibuja una tarjeta blanca con encabezado, estadisticas grandes y vinetas. Devuelve la nueva y."""
    d = ImageDraw.Draw(im)
    tb = bold(40)
    num_f = bold(74)
    lbl_f = reg(27)
    bul_f = reg(29)

    # medir altura de vinetas (cada una con sangria para el punto)
    bw = TEXTO_W - 40
    bloques = [wrap(d, b, bul_f, bw) for b in bullets]
    n_lineas = sum(len(b) for b in bloques)
    h_stats = 150 if stats else 0
    h = PAD + 64 + 14 + (h_stats + 18 if stats else 0) + n_lineas * 40 + len(bloques) * 12 + PAD - 6

    caja = (MARGEN, y, MARGEN + CONTENIDO, y + h)
    tarjeta_sombra(im, caja)
    d.rounded_rectangle(caja, radius=26, fill=BLANCO)

    # barra de acento izquierda + titulo
    d.rounded_rectangle([caja[0], caja[1] + PAD, caja[0] + 10, caja[1] + PAD + 46], radius=5, fill=accent)
    d.text((caja[0] + PAD + 8, caja[1] + PAD + 2), titulo, font=tb, fill=TINTA)

    cy = caja[1] + PAD + 64 + 14

    # estadisticas: dos columnas
    if stats:
        colw = (TEXTO_W - 24) // len(stats)
        for i, (num, lbl) in enumerate(stats):
            cx = caja[0] + PAD + i * (colw + 24)
            d.text((cx, cy), num, font=num_f, fill=accent)
            ly = cy + 88
            for ln in wrap(d, lbl, lbl_f, colw):
                d.text((cx, ly), ln, font=lbl_f, fill=GRIS)
                ly += 34
        cy += h_stats + 18

    # vinetas
    for lineas in bloques:
        d.ellipse([caja[0] + PAD + 2, cy + 12, caja[0] + PAD + 16, cy + 26], fill=accent)
        ty = cy
        for ln in lineas:
            d.text((caja[0] + PAD + 40, ty), ln, font=bul_f, fill=TINTA)
            ty += 40
        cy = ty + 12
    return y + h


def main():
    # ---------- calcular altura total en 2 pasadas (dibujo en lienzo provisional) ----------
    prov = Image.new("RGBA", (W, 4000))
    dp = ImageDraw.Draw(prov)

    y = 0
    y += 236  # encabezado fijo

    stats_s = [("475", "postas y establecimientos de salud"), ("7", "provincias cubiertas")]
    bul_s = [
        "Equipos médicos Bluetooth plug & play: oxímetro, tensiómetro y termómetro sin configuración",
        "IA clínica 24/7 + médico validador de la RIS",
        "Funciona SIN señal en la posta más lejana (offline-first)",
        "69% más barato que la telemedicina tradicional",
    ]
    # medir tarjeta salud
    bw = TEXTO_W - 40
    bul_f = reg(29)
    n_s = sum(len(wrap(dp, b, bul_f, bw)) for b in bul_s)
    h_s = PAD + 64 + 14 + 168 + n_s * 40 + len(bul_s) * 12 + PAD - 6

    stats_e = [("8,131", "docentes rurales sin actualización"), ("153,616", "estudiantes en Amazonas")]
    bul_e = [
        "Cursos de la Católica, Cantuta, Villarreal y Agraria, en el celular del docente",
        "PWA offline: descarga con señal, estudia en su comunidad, certificado con valor académico",
        "Colegios técnicos con perfil productivo por provincia (arroz, café, ganadería, madera)",
        "Red Awajún-Wampis: formación en awajún y wampis",
        "69% más barato que la formación tradicional",
    ]
    n_e = sum(len(wrap(dp, b, bul_f, bw)) for b in bul_e)
    h_e = PAD + 64 + 14 + 168 + n_e * 40 + len(bul_e) * 12 + PAD - 6

    GAP = 34
    quote_f = semi(35)
    autor_f = reg(27)
    quote = "\u201cEducación y salud es la columna vertebral del desarrollo de cualquier pueblo.\u201d"
    qlines = wrap(dp, quote, quote_f, TEXTO_W - 40)
    h_q = PAD + 8 + len(qlines) * 48 + 16 + 40 + 18

    H = y + h_s + GAP + h_e + GAP + h_q + 26 + 30 + 10

    # ---------- lienzo real ----------
    im = Image.new("RGBA", (W, H), CREMA)
    d = ImageDraw.Draw(im)

    # encabezado verde degradado
    for i in range(236):
        t = i / 235
        c = tuple(int(VERDE_OSC[k] + (VERDE[k] - VERDE_OSC[k]) * t) for k in range(3))
        d.line([(0, i), (W, i)], fill=c)
    d.text((W / 2, 78), "PROPUESTA INTEGRAL", font=bold(58), fill=BLANCO, anchor="ma")
    d.text((W / 2, 150), "Salud + Educación para el desarrollo de Amazonas", font=reg(31), fill=(214, 240, 228), anchor="ma")
    d.text((W / 2, 196), "Prof. Augusto Grimaldo", font=semi(27), fill=(255, 222, 130), anchor="ma")

    cy = dib_tarjeta(im, y, "SALUD — Telemedicina rural", VERDE, stats_s, bul_s)
    cy = dib_tarjeta(im, cy + GAP, "EDUCACIÓN — Formación docente", AMBAR, stats_e, bul_e)

    # cita
    cy += GAP
    caja = (MARGEN, cy, MARGEN + CONTENIDO, cy + h_q)
    tarjeta_sombra(im, caja)
    d.rounded_rectangle(caja, radius=26, fill=VERDE_OSC)
    qy = cy + PAD + 8
    for ln in qlines:
        d.text((W / 2, qy), ln, font=quote_f, fill=CREMA, anchor="ma")
        qy += 48
    d.text((W / 2, qy + 16), "- Prof. Augusto Grimaldo", font=autor_f, fill=(158, 216, 190), anchor="ma")

    d.text((W / 2, H - 22), "enrilubo.github.io/salud-amazonas-landing  ·  enriluai-ctrl.github.io/educacion-amazonas", font=reg(21), fill=GRIS, anchor="ma")

    im.convert("RGB").save(DST, "PNG", optimize=True)
    print("OK", DST, im.size, os.path.getsize(DST), "bytes")


if __name__ == "__main__":
    main()
