# Genera los iconos PWA (192/512/maskable/apple) con Pillow, sin dependencias externas.
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(BASE, "icons")
os.makedirs(DST, exist_ok=True)

VERDE_OSC = (7, 40, 29, 255)
VERDE = (14, 122, 95, 255)
CREMA = (244, 239, 227, 255)
SOL = (240, 196, 25, 255)

def fuente(tam):
    for ruta in (
        "C:/Windows/Fonts/seguisym.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ):
        if os.path.exists(ruta):
            try:
                return ImageFont.truetype(ruta, tam)
            except Exception:
                pass
    return ImageFont.load_default()

def icono_base(tam, con_fondo=True):
    im = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if con_fondo:
        d.rounded_rectangle([0, 0, tam - 1, tam - 1], radius=tam // 5, fill=VERDE_OSC)
    m = tam * 0.14
    # montanas: dos picos
    d.polygon([(m, tam * .68), (tam * .38, tam * .30), (tam * .58, tam * .68)], fill=CREMA)
    d.polygon([(tam * .44, tam * .68), (tam * .68, tam * .22), (tam - m, tam * .68)], fill=VERDE)
    # base
    d.rectangle([m, tam * .68, tam - m, tam * .80], fill=CREMA)
    # sol
    r = tam * 0.10
    cx, cy = tam * 0.76, tam * 0.24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SOL)
    # letra G
    f = fuente(int(tam * 0.30))
    d.text((tam * 0.5, tam * 0.855), "G", font=f, fill=CREMA, anchor="mm")
    return im

def icono_maskable(tam):
    # maskable: mismo dibujo con margen de seguridad (80% area util)
    im = Image.new("RGBA", (tam, tam), VERDE_OSC)
    base = icono_base(int(tam * 0.78), con_fondo=False)
    off = (tam - base.size[0]) // 2
    im.alpha_composite(base, (off, off))
    return im

icono_base(192).save(os.path.join(DST, "icon-192.png"))
icono_base(512).save(os.path.join(DST, "icon-512.png"))
icono_maskable(512).save(os.path.join(DST, "icon-maskable-512.png"))
icono_base(180).save(os.path.join(DST, "apple-touch-icon.png"))
print("iconos OK ->", DST)
