"""
Architectural Render Enhancement Script
Improves realism and advertising quality of architectural visualizations.
Usage: python enhance_render.py <input_image_path>
"""

import sys
import os
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import numpy as np

def enhance_sky(img_array):
    """Replace washed-out sky with a vibrant blue gradient."""
    h, w = img_array.shape[:2]
    result = img_array.copy().astype(np.float32)

    # Sky occupies roughly the top 15% of the image
    sky_height = int(h * 0.15)

    for y in range(sky_height):
        t = y / sky_height  # 0 = top, 1 = horizon
        # Deep azure at top -> soft horizon blue
        sky_top    = np.array([100, 160, 220], dtype=np.float32)
        sky_bottom = np.array([195, 220, 240], dtype=np.float32)
        sky_color  = sky_top * (1 - t) + sky_bottom * t

        # Blend: keep original clouds (bright pixels), replace dull sky
        orig_row   = img_array[y].astype(np.float32)
        brightness = orig_row.mean(axis=1, keepdims=True)
        cloud_mask = np.clip((brightness - 180) / 60, 0, 1)  # 1 = cloud, 0 = sky

        result[y] = orig_row * cloud_mask + sky_color * (1 - cloud_mask)

    return np.clip(result, 0, 255).astype(np.uint8)


def remove_sepia_cast(img_array):
    """Neutralise the warm yellowish-sepia cast."""
    result = img_array.astype(np.float32)
    # Reduce red/green channel slightly, lift blue
    result[:, :, 0] *= 0.92   # red   down
    result[:, :, 1] *= 0.96   # green slightly down
    result[:, :, 2] *= 1.18   # blue  up
    return np.clip(result, 0, 255).astype(np.uint8)


def boost_greenery(img_array):
    """Make vegetation more vivid and natural."""
    result = img_array.astype(np.float32)
    r, g, b = result[:,:,0], result[:,:,1], result[:,:,2]

    # Detect green pixels (grass, trees)
    green_mask = (g > r * 1.05) & (g > b * 1.05) & (g > 60)

    result[:,:,1][green_mask] = np.clip(result[:,:,1][green_mask] * 1.25, 0, 255)
    result[:,:,0][green_mask] = np.clip(result[:,:,0][green_mask] * 0.88, 0, 255)
    result[:,:,2][green_mask] = np.clip(result[:,:,2][green_mask] * 0.90, 0, 255)

    return np.clip(result, 0, 255).astype(np.uint8)


def add_ambient_occlusion_hint(img_array):
    """Darken shadowed/lower building areas subtly for depth."""
    result = img_array.astype(np.float32)
    h, w = result.shape[:2]

    # Buildings sit roughly in the middle vertical band
    for y in range(int(h * 0.15), h):
        depth_factor = 1.0 - 0.04 * ((y - h * 0.15) / (h * 0.85)) ** 0.5
        result[y] *= depth_factor

    return np.clip(result, 0, 255).astype(np.uint8)


def add_vignette(img_array, strength=0.35):
    """Add a subtle vignette to focus the eye on the development."""
    h, w = img_array.shape[:2]
    cx, cy = w / 2, h / 2

    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt(((X - cx) / cx) ** 2 + ((Y - cy) / cy) ** 2)
    vignette = 1 - strength * np.clip(dist, 0, 1) ** 1.6

    result = img_array.astype(np.float32) * vignette[:, :, np.newaxis]
    return np.clip(result, 0, 255).astype(np.uint8)


def enhance_building_materials(img_array):
    """Add subtle warm light on building facades (golden-hour feel)."""
    result = img_array.astype(np.float32)
    r, g, b = result[:,:,0], result[:,:,1], result[:,:,2]

    # Detect light-coloured building surfaces (beige/white)
    building_mask = (
        (r > 160) & (g > 150) & (b > 130) &
        (r > b) &                            # warmer than blue
        (np.abs(r.astype(int) - g.astype(int)) < 35)
    )

    # Warm the facades with a golden-hour tint
    result[:,:,0][building_mask] = np.clip(result[:,:,0][building_mask] * 1.08, 0, 255)
    result[:,:,1][building_mask] = np.clip(result[:,:,1][building_mask] * 1.04, 0, 255)
    result[:,:,2][building_mask] = np.clip(result[:,:,2][building_mask] * 0.94, 0, 255)

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_pil_enhancements(img):
    """PIL-based contrast, colour, sharpness pipeline."""
    img = ImageEnhance.Contrast(img).enhance(1.30)
    img = ImageEnhance.Color(img).enhance(1.55)
    img = ImageEnhance.Brightness(img).enhance(1.08)
    img = ImageEnhance.Sharpness(img).enhance(2.20)

    # Extra sharpening pass
    img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=3))
    return img


def main(input_path):
    print(f"Loading: {input_path}")
    img = Image.open(input_path).convert("RGB")

    orig_size = img.size
    print(f"Original size: {orig_size[0]}x{orig_size[1]}")

    # ── Upscale 2x for higher output resolution ──
    scale = 2
    large = img.resize((orig_size[0] * scale, orig_size[1] * scale), Image.LANCZOS)
    arr   = np.array(large)

    print("Applying enhancements...")
    arr = remove_sepia_cast(arr)
    arr = enhance_sky(arr)
    arr = boost_greenery(arr)
    arr = enhance_building_materials(arr)
    arr = add_ambient_occlusion_hint(arr)
    arr = add_vignette(arr, strength=0.30)

    enhanced = Image.fromarray(arr)
    enhanced = apply_pil_enhancements(enhanced)

    # ── Save ──
    base, ext = os.path.splitext(input_path)
    output_path = base + "_enhanced.jpg"
    enhanced.save(output_path, "JPEG", quality=97, subsampling=0)
    print(f"\nSaved → {output_path}")
    print(f"Output size: {enhanced.size[0]}x{enhanced.size[1]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python enhance_render.py <path_to_image>")
        sys.exit(1)
    main(sys.argv[1])
