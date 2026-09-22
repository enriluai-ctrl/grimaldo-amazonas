# -*- coding: utf-8 -*-
"""
Genera la infografía estilo 'Pipeline / Ruta de Desarrollo' inspirada en el banner MLOps:
- Fondo oscuro azul-verdoso elegante
- Badges brillantes arriba
- Gran titular 'AMAZONAS INTEGRAL'
- Flujo secuencial de 5 pasos en cajas con borde brillante, números 1..5 y flechas
- Lenguaje 100% claro y popular (para que lo entienda cualquiera: campesino, madre, profesor)
- Sin menciones sectoriales (se generaliza a todos los pueblos y provincias)
- Gran lema de impacto abajo con Prof. Augusto Grimaldo
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(BASE, "ruta-desarrollo.png")

W = 1400
H = 1400

# Paleta estilo banner de alta tecnología accesible
FONDO = (4, 18, 26)        # Azul oscuro profundo
FONDO_CARD = (8, 28, 38)   # Fondo de tarjeta
BORDE_NEON = (0, 229, 163) # Verde menta / neon
AZUL_CIAN = (0, 194, 255)  # Cian eléctrico
BLANCO = (255, 255, 255)
GRIS_CLARO = (200, 218, 226)
GRIS_TENUE = (120, 145, 155)
AMARILLO = (255, 213, 79)

def F(tam, bold=False):
    cands = ["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]
    for c in cands:
        p = os.path.join("C:/Windows/Fonts", c)
        if os.path.exists(p):
            return ImageFont.truetype(p, tam)
    return ImageFont.load_default()

def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def dib_badge(d, x, y, texto, icono=""):
    f = F(20, bold=True)
    t = f"{icono}  {texto}" if icono else texto
    w = d.textlength(t, font=f) + 32
    h = 42
    # Fondo con borde suave
    d.rounded_rectangle([x, y, x + w, y + h], radius=21, fill=(12, 38, 48), outline=AZUL_CIAN, width=2)
    d.text((x + 16, y + 9), t, font=f, fill=BLANCO)
    return w

def dibujar():
    im = Image.new("RGBA", (W, H), FONDO)
    d = ImageDraw.Draw(im)

    # 1. Gradiente sutil y resplandor superior
    for r in range(260, 0, -10):
        alpha = int(18 * (1 - r / 260))
        d.ellipse([W//2 - r*2, -r, W//2 + r*2, r*2], fill=(0, 194, 255, alpha))

    # 2. Badges superiores
    b1_w = dib_badge(d, 80, 50, "PLAN AMAZONAS 2026", "🎓")
    b2_w = dib_badge(d, 80 + b1_w + 18, 50, "7 PROVINCIAS", "📍")
    b3_w = dib_badge(d, 80 + b1_w + 18 + b2_w + 18, 50, "100% OPERATIVO SIN INTERNET", "⚡")

    # Caja lateral de presentación (estilo 'INICIO 12 OCT' del banner)
    caja_der_w = 300
    caja_der_x = W - 80 - caja_der_w
    caja_der_y = 50
    d.rounded_rectangle([caja_der_x, caja_der_y, caja_der_x + caja_der_w, caja_der_y + 160],
                        radius=20, fill=(10, 32, 44), outline=AZUL_CIAN, width=3)
    d.text((caja_der_x + caja_der_w//2, caja_der_y + 20), "PROPUESTA DE GESTIÓN", font=F(17, bold=True), fill=AZUL_CIAN, anchor="mt")
    d.text((caja_der_x + caja_der_w//2, caja_der_y + 48), "PROFESOR", font=F(22, bold=True), fill=BLANCO, anchor="mt")
    d.text((caja_der_x + caja_der_w//2, caja_der_y + 80), "GRIMALDO", font=F(36, bold=True), fill=AMARILLO, anchor="mt")
    d.text((caja_der_x + caja_der_w//2, caja_der_y + 128), "⛰️ Para todas las familias", font=F(16), fill=GRIS_CLARO, anchor="mt")

    # 3. Gran Título Principal
    d.text((80, 110), "AMAZONAS INTEGRAL", font=F(64, bold=True), fill=BLANCO)
    d.text((80, 185), "Salud y Educación de Calidad al Alcance de Todos", font=F(32, bold=False), fill=BORDE_NEON)

    # 4. Los 5 Pasos del Flujo (Pipeline horizontal conectado con flechas)
    # Estructura: 5 columnas
    pasos = [
        {
            "num": "1",
            "titulo": "SIN BARRERAS",
            "sub": "Postas y escuelas",
            "bullets": [
                "Funciona 100% sin internet",
                "Cero cables ni antenas caras",
                "Listo en cualquier pueblo"
            ]
        },
        {
            "num": "2",
            "titulo": "TECNOLOGÍA SIMPLE",
            "sub": "Herramientas fáciles",
            "bullets": [
                "Usa el celular común",
                "Kits médicos bluetooth",
                "Cualquiera puede operarlo"
            ]
        },
        {
            "num": "3",
            "titulo": "ESPECIALISTAS",
            "sub": "Respaldo directo",
            "bullets": [
                "Asistente clínico 24/7",
                "Médicos validan en minutos",
                "Cursos de 4 universidades"
            ]
        },
        {
            "num": "4",
            "titulo": "ATENCIÓN REAL",
            "sub": "Resultados en el lugar",
            "bullets": [
                "Salud sin viajar días al hospital",
                "Docentes con certificación",
                "Familias protegidas hoy"
            ]
        },
        {
            "num": "5",
            "titulo": "FUTURO Y TRABAJO",
            "sub": "Desarrollo productivo",
            "bullets": [
                "Carreras técnicas por provincia",
                "Café, cacao, madera y campo",
                "Jóvenes con empleo local"
            ]
        }
    ]

    card_y = 280
    card_h = 580
    n_cards = len(pasos)
    margen_x = 70
    gap = 22
    card_w = (W - margen_x * 2 - (n_cards - 1) * gap) // n_cards

    for i, p in enumerate(pasos):
        cx = margen_x + i * (card_w + gap)

        # Tarjeta con borde neon/cian
        outline_color = BORDE_NEON if i in [0, 4] else AZUL_CIAN
        d.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h],
                            radius=18, fill=FONDO_CARD, outline=outline_color, width=3)

        # Círculo superior con el número (estilo MLOps)
        cir_r = 24
        cir_cx = cx + card_w // 2
        cir_cy = card_y + 40
        d.ellipse([cir_cx - cir_r, cir_cy - cir_r, cir_cx + cir_r, cir_cy + cir_r],
                  fill=(15, 50, 65), outline=outline_color, width=3)
        d.text((cir_cx, cir_cy), p["num"], font=F(26, bold=True), fill=BLANCO, anchor="mm")

        # Título del paso
        d.text((cir_cx, card_y + 86), p["titulo"], font=F(20, bold=True), fill=BLANCO, anchor="mt")
        d.text((cir_cx, card_y + 116), p["sub"], font=F(15), fill=outline_color, anchor="mt")

        # Línea divisoria suave
        d.line([(cx + 20, card_y + 148), (cx + card_w - 20, card_y + 148)], fill=(30, 65, 80), width=1)

        # Viñetas explicativas
        by = card_y + 175
        for b in p["bullets"]:
            # Icono check o punto brillante
            d.ellipse([cx + 18, by + 6, cx + 28, by + 16], fill=outline_color)
            lines = wrap(d, b, F(17), card_w - 50)
            ty = by
            for l in lines:
                d.text((cx + 36, ty), l, font=F(17), fill=GRIS_CLARO)
                ty += 26
            by = ty + 18

        # Flecha conectora entre pasos (excepto el último)
        if i < n_cards - 1:
            arrow_x = cx + card_w + gap // 2
            arrow_y = card_y + card_h // 2
            d.text((arrow_x, arrow_y), "➔", font=F(24, bold=True), fill=AZUL_CIAN, anchor="mm")

    # 5. Gran Slogan Inferior (como 'LLEVA TUS MODELOS...' del banner)
    slogan_y = 920
    # Fondo con brillo central para el lema
    for r in range(120, 0, -10):
        d.rounded_rectangle([100, slogan_y - 20, W - 100, slogan_y + 240], radius=30, fill=(6, 26, 36))

    d.rounded_rectangle([100, slogan_y, W - 100, slogan_y + 200],
                        radius=26, fill=(10, 36, 48), outline=BORDE_NEON, width=3)

    d.text((W//2, slogan_y + 36),
           "LLEVEMOS EL DESARROLLO DE LA PROMESA A LA REALIDAD",
           font=F(36, bold=True), fill=BLANCO, anchor="mt")

    d.text((W//2, slogan_y + 90),
           "69% MÁS BARATO  ·  CON EL MISMO PRESUPUESTO ATENDEMOS AL TRIPLE DE PUEBLOS",
           font=F(24, bold=True), fill=AMARILLO, anchor="mt")

    d.text((W//2, slogan_y + 140),
           "“Educación y salud es la columna vertebral del desarrollo de cualquier pueblo”",
           font=F(20), fill=GRIS_CLARO, anchor="mt")

    # 6. Pie de página
    d.text((W//2, H - 90), "🔬 PROPUESTAS REALES, MEDIBLES Y CON PRESUPUESTO COMPROBADO", font=F(19, bold=True), fill=AZUL_CIAN, anchor="mt")
    d.text((W//2, H - 55), "Para las 7 provincias de Amazonas: Bagua · Bongará · Chachapoyas · Condorcanqui · Luya · Rodríguez de Mendoza · Utcubamba", font=F(16), fill=GRIS_TENUE, anchor="mt")

    im.convert("RGB").save(DST, "PNG", optimize=True)
    print("OK ->", DST, os.path.getsize(DST), "bytes")

if __name__ == "__main__":
    dibujar()
