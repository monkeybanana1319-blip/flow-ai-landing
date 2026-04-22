"""Convert the original JPG logo into two PNG variants:
- assets/logo.png         — transparent background (white removed)
- assets/logo-white.png   — inverted colors for use on dark backgrounds
- assets/og-image.jpg     — 1200x630 social preview image
- assets/favicon.png      — 192x192 favicon
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageChops

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "logo-original.jpg"

img = Image.open(SRC).convert("RGBA")
# Resize to retina-friendly width (2x the largest on-screen height of 140px)
img.thumbnail((560, 560), Image.LANCZOS)

# 1) Transparent version: fuzzy white -> alpha
pixels = img.load()
w, h = img.size
THRESHOLD = 235  # near-white becomes transparent
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        if r >= THRESHOLD and g >= THRESHOLD and b >= THRESHOLD:
            # Full transparency for pure white
            pixels[x, y] = (r, g, b, 0)
        elif r >= 220 and g >= 220 and b >= 220:
            # Soft-edge: partial transparency based on distance from white
            avg = (r + g + b) / 3
            alpha = int(max(0, min(255, (255 - avg) * 10)))
            pixels[x, y] = (r, g, b, alpha)

img.save(ROOT / "assets" / "logo.png", "PNG", optimize=True)
print(f"logo.png -> {(ROOT/'assets'/'logo.png').stat().st_size // 1024} KB")

# 2) White-on-dark version: invert RGB of non-transparent pixels
img_white = img.copy()
pixels = img_white.load()
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        if a > 0:
            pixels[x, y] = (255 - r, 255 - g, 255 - b, a)
img_white.save(ROOT / "assets" / "logo-white.png", "PNG", optimize=True)
print(f"logo-white.png -> {(ROOT/'assets'/'logo-white.png').stat().st_size // 1024} KB")

# 3) Favicon (192x192)
fav = Image.open(SRC).convert("RGBA")
fav.thumbnail((192, 192))
# center on square canvas with cream bg
canvas = Image.new("RGBA", (192, 192), (245, 241, 234, 255))
off = ((192 - fav.width) // 2, (192 - fav.height) // 2)
canvas.paste(fav, off)
canvas.save(ROOT / "assets" / "favicon.png", "PNG", optimize=True)
print("favicon.png saved")

# 4) OG image (1200x630) — cream background with centered logo + tagline bar
og = Image.new("RGB", (1200, 630), (245, 241, 234))
logo_for_og = Image.open(SRC).convert("RGBA")
logo_for_og.thumbnail((500, 500))
pos = ((1200 - logo_for_og.width) // 2, (630 - logo_for_og.height) // 2 - 20)
og.paste(logo_for_og, pos, logo_for_og if logo_for_og.mode == "RGBA" else None)
og.save(ROOT / "assets" / "og-image.jpg", "JPEG", quality=88, optimize=True)
print("og-image.jpg saved")

print("All variants generated.")
