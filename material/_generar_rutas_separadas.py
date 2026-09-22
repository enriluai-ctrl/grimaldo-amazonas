# -*- coding: utf-8 -*-
"""
Genera dos imágenes verticales optimizadas para celular (1080 x 1920):
1. ruta-salud.png     -> Ruta de Salud (Telemedicina y Postas Conectadas) en 5 pasos verticales
2. ruta-educacion.png -> Ruta de Educación (Maestros y Colegios Técnicos) en 5 pasos verticales

Estilo:
- Moderno, tipo banner tecnológico / MLOps (fondo azul marino oscuro, bordes neón brillantes, tarjetas con nodos numerados)
- Lenguaje 100% claro y popular (generalizado, para que lo entienda cualquier vecino o padre de familia)
- Formato vertical para lectura natural en celular sin necesidad de rotar la pantalla
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONDO = (4, 18, 26)         # Azul oscuro profundo
FONDO_CARD = (8, 28, 38)    # Tarjeta interior
AZUL_CIAN = (0, 194, 255)   # Cian brillante
VERDE_NEON = (0, 229, 163)  # Verde menta neón
AMBAR_NEON = (255, 183, 77) # Ámbar neón
BLANCO = (255, 255, 255)
GRIS_CLARO = (215, 230, 238)
GRIS_MEDIO = (130, 155, 168)
AMARILLO = (255, 220, 90)

W = 1080
H = 1920

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

def dib_badge(d, x, y, texto, accent_color, icono=""):
    f = F(18, bold=True)
    t = f"{icono}  {texto}" if icono else texto
    w = d.textlength(t, font=f) + 28
    h = 36
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=(10, 32, 44), outline=accent_color, width=2)
    d.text((x + 14, y + 8), t, font=f, fill=BLANCO)
    return w

def generar_ruta(nombre_archivo, config):
    im = Image.new("RGBA", (W, H), FONDO)
    d = ImageDraw.Draw(im)
    accent = config["accent"]
    glow_color = config["glow"]

    # 1. Resplandor superior
    for r in range(240, 0, -12):
        alpha = int(16 * (1 - r / 240))
        d.ellipse([W//2 - r*2, -r + 20, W//2 + r*2, r*2], fill=(glow_color[0], glow_color[1], glow_color[2], alpha))

    # 2. Badges superiores
    bx = 50
    by = 40
    for b in config["badges"]:
        bw = dib_badge(d, bx, by, b["texto"], accent, b.get("icono", ""))
        bx += bw + 14

    # 3. Encabezado
    # Tag superior
    d.text((50, 96), config["tag_superior"], font=F(17, bold=True), fill=accent)
    # Título enorme
    d.text((50, 122), config["titulo"], font=F(46, bold=True), fill=BLANCO)
    # Subtítulo explicativo
    d.text((50, 184), config["subtitulo"], font=F(23), fill=GRIS_CLARO)

    # Mini insignia lateral profesor Grimaldo + Símbolo marcado con X
    cedula_path = os.path.join(BASE, "cedula-voto-x.png")
    box_w = 310
    box_x = W - 50 - box_w
    box_y = 96
    d.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + 115], radius=16, fill=(10, 32, 44), outline=(229, 36, 36), width=3)
    
    if os.path.exists(cedula_path):
        ced_im = Image.open(cedula_path).resize((90, 90), Image.Resampling.LANCZOS)
        im.paste(ced_im, (box_x + 14, box_y + 12), ced_im)
        txt_x = box_x + 114
        d.text((txt_x, box_y + 16), "SOLUCIÓN REGIONAL", font=F(13, bold=True), fill=accent)
        d.text((txt_x, box_y + 36), "MARCA LA X", font=F(22, bold=True), fill=(255, 60, 60))
        d.text((txt_x, box_y + 66), "Victoria Amazonense", font=F(15, bold=True), fill=BLANCO)
        d.text((txt_x, box_y + 88), "Prof. Grimaldo", font=F(13), fill=AMARILLO)
    else:
        d.text((box_x + box_w//2, box_y + 12), "PROPUESTA DE GESTIÓN", font=F(14, bold=True), fill=accent, anchor="mt")
        d.text((box_x + box_w//2, box_y + 34), "PROFESOR GRIMALDO", font=F(18, bold=True), fill=BLANCO, anchor="mt")
        d.text((box_x + box_w//2, box_y + 66), "⛰️ Amazonas para todos", font=F(14), fill=AMARILLO, anchor="mt")

    # Línea horizontal separadora
    d.line([(50, 230), (W - 50, 230)], fill=(20, 55, 70), width=2)

    # 4. Los 5 Pasos Verticales (con línea conectora tipo pipeline)
    line_x = 98
    start_y = 260
    step_gap = 210

    # Dibujar línea vertical conectora de fondo con brillo
    d.line([(line_x, start_y + 30), (line_x, start_y + 4 * step_gap + 30)], fill=(15, 60, 75), width=6)
    d.line([(line_x, start_y + 30), (line_x, start_y + 4 * step_gap + 30)], fill=accent, width=2)

    for i, p in enumerate(config["pasos"]):
        cy = start_y + i * step_gap

        # Tarjeta del paso
        card_x = 150
        card_w = W - 50 - card_x
        card_h = 186
        d.rounded_rectangle([card_x, cy, card_x + card_w, cy + card_h],
                            radius=18, fill=FONDO_CARD, outline=accent if i in [0, 4] else AZUL_CIAN, width=2)

        # Círculo numerado en la línea conectora (estilo MLOps)
        node_r = 28
        d.ellipse([line_x - node_r, cy + 32 - node_r, line_x + node_r, cy + 32 + node_r],
                  fill=(12, 38, 48), outline=accent, width=3)
        d.text((line_x, cy + 32), str(i + 1), font=F(26, bold=True), fill=BLANCO, anchor="mm")

        # Conector pequeño del círculo a la tarjeta
        d.line([(line_x + node_r, cy + 32), (card_x, cy + 32)], fill=accent, width=2)

        # Contenido de la tarjeta
        # Título del paso
        d.text((card_x + 22, cy + 18), p["titulo"], font=F(22, bold=True), fill=BLANCO)
        d.text((card_x + 22, cy + 48), p["sub"], font=F(15, bold=True), fill=accent)

        # Viñetas claras
        by = cy + 76
        for b in p["bullets"]:
            # Icono viñeta
            d.ellipse([card_x + 22, by + 5, card_x + 30, by + 13], fill=accent)
            lines = wrap(d, b, F(17), card_w - 60)
            ty = by
            for l in lines:
                d.text((card_x + 40, ty), l, font=F(17), fill=GRIS_CLARO)
                ty += 24
            by = ty + 6

    # 5. Gran Slogan Inferior
    slogan_y = 1380
    d.rounded_rectangle([50, slogan_y, W - 50, slogan_y + 350],
                        radius=24, fill=(8, 30, 42), outline=accent, width=3)

    d.text((W//2, slogan_y + 24), config["slogan_top"], font=F(18, bold=True), fill=accent, anchor="mt")
    d.text((W//2, slogan_y + 56), config["slogan_tit"], font=F(30, bold=True), fill=BLANCO, anchor="mt")

    # Caja dorada de métrica
    met_y = slogan_y + 115
    d.rounded_rectangle([80, met_y, W - 80, met_y + 74], radius=16, fill=(18, 48, 40) if accent == VERDE_NEON else (45, 38, 15), outline=AMARILLO, width=2)
    d.text((W//2, met_y + 12), config["metrica_destacada"], font=F(22, bold=True), fill=AMARILLO, anchor="mt")
    d.text((W//2, met_y + 42), config["metrica_sub"], font=F(15), fill=BLANCO, anchor="mt")

    # Cita del profesor
    d.text((W//2, slogan_y + 215), "“Educación y salud es la columna vertebral del desarrollo de cualquier pueblo”",
           font=F(18, bold=True), fill=GRIS_CLARO, anchor="mt")
    d.text((W//2, slogan_y + 250), "— Prof. Augusto Grimaldo", font=F(16), fill=accent, anchor="mt")

    # Nota de alcance
    d.text((W//2, slogan_y + 295), config["pie_alcance"], font=F(15, bold=True), fill=BLANCO, anchor="mt")

    # 6. Pie de página
    d.text((W//2, H - 90), "🔬 PLAN DE GESTIÓN TÉCNICO, MEDIBLE Y CON PRESUPUESTO SUSTENTADO", font=F(16, bold=True), fill=AZUL_CIAN, anchor="mt")
    d.text((W//2, H - 60), "Amazonas: Bagua · Bongará · Chachapoyas · Condorcanqui · Luya · Rodríguez de Mendoza · Utcubamba", font=F(14), fill=GRIS_MEDIO, anchor="mt")

    dst_path = os.path.join(BASE, nombre_archivo)
    im.convert("RGB").save(dst_path, "PNG", optimize=True)
    print(f"OK -> {dst_path} ({os.path.getsize(dst_path)} bytes)")


# ==============================================================================
# CONFIGURACIÓN 1: RUTA DE SALUD
# ==============================================================================
config_salud = {
    "accent": VERDE_NEON,
    "glow": (0, 229, 163),
    "badges": [
        {"texto": "SALUD AMAZONAS", "icono": "🏥"},
        {"texto": "475 POSTAS RURALES", "icono": "📍"},
        {"texto": "SIN INTERNET", "icono": "⚡"},
    ],
    "tag_superior": "PLAN INTEGRAL DE SALUD RURAL",
    "titulo": "RUTA DE SALUD",
    "subtitulo": "La posta más lejana con médico presente para tu familia",
    "pasos": [
        {
            "titulo": "KITS MÉDICOS BLUETOOTH",
            "sub": "Herramientas simples y universales",
            "bullets": [
                "Oxímetro, tensiómetro y termómetro conectados al celular común.",
                "Cero computadoras caras ni trámites complicados."
            ]
        },
        {
            "titulo": "100% OPERATIVO SIN SEÑAL",
            "sub": "Funciona en cualquier comunidad",
            "bullets": [
                "No depende de internet ni de antenas que se caen con la lluvia.",
                "La app guarda la consulta y sincroniza cuando hay señal."
            ]
        },
        {
            "titulo": "ASISTENTE INTELIGENTE 24/7",
            "sub": "Guía clínica al instante",
            "bullets": [
                "Orienta al personal de la posta en segundos ante urgencias.",
                "Respuestas rápidas en mordeduras, fiebres y emergencias."
            ]
        },
        {
            "titulo": "TELECONSULTA CON EL MÉDICO",
            "sub": "El especialista atiende a distancia",
            "bullets": [
                "Médicos de la Red de Salud validan diagnósticos y recetas.",
                "Tratamiento seguro y supervisado por profesionales."
            ]
        },
        {
            "titulo": "ATENCIÓN EN TU PROPIO PUEBLO",
            "sub": "Salud oportuna para las familias",
            "bullets": [
                "Se acabaron los viajes de días en lancha o trocha al hospital.",
                "Familias protegidas y atendidas con dignidad en su lugar."
            ]
        }
    ],
    "slogan_top": "SOLUCIÓN REAL Y COMPROBADA",
    "slogan_tit": "SALUD DIGNA EN CADA RINCÓN DE AMAZONAS",
    "metrica_destacada": "69% MÁS BARATO QUE LA TELEMEDICINA TRADICIONAL",
    "metrica_sub": "Con el mismo presupuesto equipamos al triple de postas en la región",
    "pie_alcance": "475 postas médicas y centros de salud en las 7 provincias",
}

# ==============================================================================
# CONFIGURACIÓN 2: RUTA DE EDUCACIÓN
# ==============================================================================
config_educacion = {
    "accent": AMBAR_NEON,
    "glow": (255, 183, 77),
    "badges": [
        {"texto": "EDUCACIÓN AMAZONAS", "icono": "🎓"},
        {"texto": "8,131 DOCENTES RURALES", "icono": "📚"},
        {"texto": "153,616 ESTUDIANTES", "icono": "👦"},
    ],
    "tag_superior": "PLAN INTEGRAL DE EDUCACIÓN Y TRABAJO",
    "titulo": "RUTA DE EDUCACIÓN",
    "subtitulo": "Maestros capacitados y carreras técnicas para los jóvenes",
    "pasos": [
        {
            "titulo": "ESTUDIO EN LA COMUNIDAD",
            "sub": "Capacitación docente sin internet permanente",
            "bullets": [
                "El maestro descarga los cursos con cualquier señal ocasional.",
                "Estudia offline en su celular sin gastar en datos."
            ]
        },
        {
            "titulo": "UNIVERSIDADES LIMEÑAS AL CAMPO",
            "sub": "Misma calidad de las mejores aulas",
            "bullets": [
                "Cursos de la Católica, Cantuta, Villarreal y Agraria.",
                "Contenidos pedagógicos modernos directo al teléfono del profesor."
            ]
        },
        {
            "titulo": "EL MAESTRO NO DEJA SU AULA",
            "sub": "Cero gastos de traslado y viáticos",
            "bullets": [
                "El docente se actualiza sin abandonar a sus alumnos.",
                "Certificación oficial con valor académico y puntaje."
            ]
        },
        {
            "titulo": "COLEGIOS TÉCNICOS POR PROVINCIA",
            "sub": "Secundarias con vocación productiva real",
            "bullets": [
                "Especialidades según la riqueza local: café, cacao, agro y madera.",
                "Talleres prácticos y convenios con institutos de la zona."
            ]
        },
        {
            "titulo": "FUTURO Y EMPLEO EN SU TIERRA",
            "sub": "Jóvenes graduados con trabajo digno",
            "bullets": [
                "Nuestros hijos se quedan a producir y progresar en Amazonas.",
                "Transformamos materias primas con técnicos propios."
            ]
        }
    ],
    "slogan_top": "FORMACIÓN CON VISIÓN DE FUTURO",
    "slogan_tit": "EDUCACIÓN DE CALIDAD SIN SALIR DE TU REGIÓN",
    "metrica_destacada": "69% MÁS BARATO QUE TRASLADAR DOCENTES A LA CAPITAL",
    "metrica_sub": "Con el mismo presupuesto capacitamos a 3 veces más maestros y jóvenes",
    "pie_alcance": "4,879 colegios y servicios educativos en las 7 provincias",
}

if __name__ == "__main__":
    generar_ruta("ruta-salud.png", config_salud)
    generar_ruta("ruta-educacion.png", config_educacion)
