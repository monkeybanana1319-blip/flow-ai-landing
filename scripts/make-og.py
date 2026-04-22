"""Generate OG + square preview images from the brand poster source.
Handles both portrait and landscape sources with smart center-crop.

Input : assets/og-source.png  (preferred) or assets/og-source.jpg
Output:
  assets/og-image.jpg         1200x630  — Facebook / WhatsApp / Twitter landscape
  assets/og-image-square.jpg  1080x1080 — IG / WhatsApp square
  assets/og-source-web.jpg    resized   — web-optimized source for social posting
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

# Prefer PNG if present, fall back to JPG
png = ROOT / "assets" / "og-source.png"
jpg = ROOT / "assets" / "og-source.jpg"
SRC = png if png.exists() else jpg
print(f"Source: {SRC.name}")

src = Image.open(SRC).convert("RGB")
W0, H0 = src.size
ratio = W0 / H0
orientation = "landscape" if ratio > 1.2 else ("square" if 0.85 < ratio < 1.2 else "portrait")
print(f"Dimensions: {W0}x{H0}  ratio={ratio:.2f}  orientation={orientation}")


def smart_crop_to(img: Image.Image, target_w: int, target_h: int, vertical_bias: float = 0.5) -> Image.Image:
    """Resize and crop `img` to exactly (target_w, target_h).
    `vertical_bias`: 0.0 = top-aligned, 0.5 = center, 1.0 = bottom-aligned.
    (Only matters if the image needs vertical cropping, i.e. portrait sources.)
    """
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        # Source is wider than target -> scale by height, crop horizontally (center)
        new_h = target_h
        new_w = int(src_w * new_h / src_h)
        resized = img.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - target_w) // 2
        return resized.crop((left, 0, left + target_w, target_h))
    else:
        # Source is taller than target -> scale by width, crop vertically
        new_w = target_w
        new_h = int(src_h * new_w / src_w)
        resized = img.resize((new_w, new_h), Image.LANCZOS)
        top = int((new_h - target_h) * vertical_bias)
        return resized.crop((0, top, target_w, top + target_h))


# For portrait sources we want the upper-middle region (logo + headline).
# For landscape sources we center-crop horizontally (no vertical bias needed).
v_bias = 0.11 if orientation == "portrait" else 0.5

# ---------- 1) Horizontal OG 1200x630 ----------
og = smart_crop_to(src, 1200, 630, vertical_bias=v_bias)
og.save(ROOT / "assets" / "og-image.jpg", "JPEG", quality=85, optimize=True, progressive=True)
print(f"og-image.jpg         -> {(ROOT/'assets'/'og-image.jpg').stat().st_size // 1024} KB")

# ---------- 2) Square 1080x1080 ----------
sq = smart_crop_to(src, 1080, 1080, vertical_bias=v_bias)
sq.save(ROOT / "assets" / "og-image-square.jpg", "JPEG", quality=85, optimize=True, progressive=True)
print(f"og-image-square.jpg  -> {(ROOT/'assets'/'og-image-square.jpg').stat().st_size // 1024} KB")

# ---------- 3) Web-optimized source ----------
web = src.copy()
web.thumbnail((1600, 1600), Image.LANCZOS)
web.save(ROOT / "assets" / "og-source-web.jpg", "JPEG", quality=85, optimize=True, progressive=True)
print(f"og-source-web.jpg    -> {(ROOT/'assets'/'og-source-web.jpg').stat().st_size // 1024} KB")

print("Done.")
