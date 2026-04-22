"""Generate OG + square preview images from the portrait poster source.
Input : assets/og-source.jpg  (e.g. 1024x1536 portrait)
Output:
  assets/og-image.jpg         1200x630  — Facebook / WhatsApp / Twitter landscape
  assets/og-image-square.jpg  1080x1080 — IG / WhatsApp square
  assets/og-source-web.jpg    resized   — for fallback / social posting
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "og-source.jpg"

src = Image.open(SRC).convert("RGB")
W0, H0 = src.size
print(f"Source: {W0}x{H0}")

# ---------- 1) Horizontal OG 1200x630 ----------
# Strategy: upscale width to 1200 keeping aspect, then crop the most iconic
# vertical window (logo + title + portrait + service tags)
target_w, target_h = 1200, 630
scale_w = target_w / W0
scaled = src.resize((target_w, int(H0 * scale_w)), Image.LANCZOS)
# scaled height ≈ 1800 for a 1024x1536 source
sh = scaled.size[1]
# Crop vertical window starting a bit below top so the tagline is visible
# and going down enough to include the portrait + service pills
y0 = int(sh * 0.11)                 # just below top padding
y1 = y0 + target_h
if y1 > sh:
    y1 = sh
    y0 = sh - target_h
og = scaled.crop((0, y0, target_w, y1))
og.save(ROOT / "assets" / "og-image.jpg", "JPEG", quality=85, optimize=True, progressive=True)
print(f"og-image.jpg -> {(ROOT/'assets'/'og-image.jpg').stat().st_size // 1024} KB")

# ---------- 2) Square 1080x1080 ----------
target = 1080
scaled2 = src.resize((target, int(H0 * target / W0)), Image.LANCZOS)
sh2 = scaled2.size[1]
y0 = int(sh2 * 0.11)
y1 = y0 + target
if y1 > sh2:
    y1 = sh2
    y0 = sh2 - target
sq = scaled2.crop((0, y0, target, y1))
sq.save(ROOT / "assets" / "og-image-square.jpg", "JPEG", quality=85, optimize=True, progressive=True)
print(f"og-image-square.jpg -> {(ROOT/'assets'/'og-image-square.jpg').stat().st_size // 1024} KB")

# ---------- 3) Web-optimized source (for social posting, resizes from 1.7MB) ----------
web = src.copy()
web.thumbnail((1080, 1620), Image.LANCZOS)
web.save(ROOT / "assets" / "og-source-web.jpg", "JPEG", quality=85, optimize=True, progressive=True)
print(f"og-source-web.jpg -> {(ROOT/'assets'/'og-source-web.jpg').stat().st_size // 1024} KB")

print("Done.")
