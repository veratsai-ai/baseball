"""Chroma-key removal + resize for baseball-slot UI assets.

Removes solid magenta (#FF00FF) background, with soft anti-alias edges,
then resizes to target output dimensions and saves as transparent PNG.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image


UI_DIR = Path(r"C:/Users/Tim/.claude/baseball-slot/assets/ui")


def chroma_key_magenta(img: Image.Image, tol: int = 60) -> Image.Image:
    """Make pixels close to pure magenta transparent, preserve everything else.

    Uses simple Manhattan distance in RGB; tol controls how forgiving the cut is.
    Pixels within tol are fully transparent; pixels with partial magenta cast
    get proportional alpha to keep AA edges clean.
    """
    img = img.convert("RGBA")
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, _ = pixels[x, y]
            # distance from pure magenta (255, 0, 255)
            d = abs(r - 255) + abs(g - 0) + abs(b - 255)
            if d <= tol:
                pixels[x, y] = (0, 0, 0, 0)
            elif d <= tol * 3:
                # soft edge: scale alpha based on how far we are from magenta
                a = int(255 * (d - tol) / (tol * 2))
                # subtract magenta contamination from RGB to clean fringing
                # bias toward keeping the gold; simple desaturation toward gray
                # of the magenta channel
                gr = max(0, min(255, r - max(0, 255 - g) // 2))
                gb = max(0, min(255, b - max(0, 255 - g) // 2))
                pixels[x, y] = (gr, g, gb, a)
    return img


def crop_to_content(img: Image.Image, alpha_threshold: int = 8) -> Image.Image:
    """Crop transparent margins, keeping a small breathing pad."""
    bbox = img.getbbox()
    if bbox is None:
        return img
    # tighten using alpha threshold
    alpha = img.split()[-1]
    mask = alpha.point(lambda a: 255 if a > alpha_threshold else 0)
    bbox = mask.getbbox() or bbox
    return img.crop(bbox)


def process_coin() -> Path:
    src = UI_DIR / "_raw_coin.png"
    dst = UI_DIR / "coin.png"
    img = Image.open(src)
    img = chroma_key_magenta(img, tol=100)
    img = crop_to_content(img, alpha_threshold=16)
    # square pad: ensure 1:1 with small padding
    w, h = img.size
    side = max(w, h)
    pad = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    pad.paste(img, ((side - w) // 2, (side - h) // 2), img)
    pad = pad.resize((128, 128), Image.LANCZOS)
    pad.save(dst, "PNG", optimize=True)
    return dst


def process_button() -> Path:
    src = UI_DIR / "_raw_btn_pitch.png"
    dst = UI_DIR / "btn-pitch.png"
    img = Image.open(src)
    # higher tol to kill purple fringing on bevel highlights
    img = chroma_key_magenta(img, tol=110)
    img = crop_to_content(img, alpha_threshold=16)
    # Crop to content first (auto-fits the actual button), then resize to
    # target 600x160 directly, padding transparent if aspect doesn't match
    # so we never cut off the lettering.
    target_w, target_h = 600, 160
    w, h = img.size
    target_ratio = target_w / target_h
    cur_ratio = w / h
    if cur_ratio > target_ratio:
        # button is wider -> scale by width, pad vertically
        new_w = target_w
        new_h = int(round(h * (target_w / w)))
        scaled = img.resize((new_w, new_h), Image.LANCZOS)
        canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        canvas.paste(scaled, (0, (target_h - new_h) // 2), scaled)
    else:
        # button is taller relative to target -> scale by height, pad horizontally
        new_h = target_h
        new_w = int(round(w * (target_h / h)))
        scaled = img.resize((new_w, new_h), Image.LANCZOS)
        canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        canvas.paste(scaled, ((target_w - new_w) // 2, 0), scaled)
    canvas.save(dst, "PNG", optimize=True)
    return dst


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target in ("coin", "all"):
        out = process_coin()
        print(f"coin -> {out} ({out.stat().st_size} bytes)")
    if target in ("btn", "all"):
        out = process_button()
        print(f"btn  -> {out} ({out.stat().st_size} bytes)")
