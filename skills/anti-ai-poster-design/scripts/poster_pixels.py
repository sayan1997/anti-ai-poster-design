#!/usr/bin/env python3
"""poster_pixels.py - measure the "busyness" of a rendered poster image.

Usage:
    python poster_pixels.py poster.png
    python poster_pixels.py poster.png --json

Requires: Pillow and numpy  (pip install pillow numpy)

Four measurements (computed on a <=400 px thumbnail):
  calm      share of 20x20 blocks that are almost flat (empty space for the eye)
  edge      share of pixels lying on a strong edge (visual busyness)
  palette   number of distinct colors each covering >= 1.5% of the image
  hues      number of hue families holding >= 5% of the saturated pixels

Calibration (see references/ai-tells-catalog.md, section 3): in a sample of 12 photographed
AI-style banners, calm was 0.00-0.08, edge 0.24-0.37, palette 10-25. In 8 human-designed
reference posters, calm was 0.05-0.54, edge 0.08-0.22, palette 5-13. Clean renders from this
skill measure calm ~0.5, edge ~0.06-0.11, palette 2-3.

These are heuristics for CLEAN RENDERS. Photographs of printed posters are noisier and will
read as busier than they are. A pass does not mean the design is good; a fail means look again.

Exit code: 0 = no FAIL, 1 = at least one FAIL.
"""
import argparse
import json
import sys

try:
    import numpy as np
    from PIL import Image, ImageFilter
except ImportError:
    print("Needs Pillow and numpy:  pip install pillow numpy", file=sys.stderr)
    sys.exit(2)


def measure(path):
    im = Image.open(path).convert("RGB")
    im.thumbnail((400, 400))
    hsv = np.asarray(im.convert("HSV")) / 255.0
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    mask = (s > 0.25) & (v > 0.2)
    hist = np.histogram(h[mask] * 360, bins=12, range=(0, 360))[0]
    hues = int((hist / max(int(mask.sum()), 1) > 0.05).sum())

    g = np.asarray(im.convert("L").filter(ImageFilter.FIND_EDGES)) / 255.0
    edge = float((g > 0.12).mean())

    q = (np.asarray(im) // 48).reshape(-1, 3)
    keys = q[:, 0] * 100 + q[:, 1] * 10 + q[:, 2]
    _, counts = np.unique(keys, return_counts=True)
    palette = int((counts / len(keys) > 0.015).sum())

    lum = np.asarray(im.convert("L")).astype(float)
    hh, ww = lum.shape
    b = 20
    stds = [lum[y:y + b, x:x + b].std() for y in range(0, hh - b, b) for x in range(0, ww - b, b)]
    calm = float((np.array(stds) < 4).mean()) if stds else 0.0
    return {"calm": round(calm, 3), "edge": round(edge, 3), "palette": palette, "hues": hues}


def judge(m):
    items = []

    def add(level, key, msg, fix):
        items.append({"level": level, "metric": key, "message": msg, "fix": fix})

    if m["calm"] < 0.03:
        add("FAIL", "calm", f"Almost no empty space (calm={m['calm']}). Every area is busy.",
            "Delete elements until at least ~30% of the canvas is quiet.")
    elif m["calm"] < 0.12:
        add("WARN", "calm", f"Little empty space (calm={m['calm']}).", "Remove a decoration or enlarge the margins.")
    if m["edge"] > 0.30:
        add("FAIL", "edge", f"Very busy edges (edge={m['edge']}).", "Remove borders, textures, icons and small text.")
    elif m["edge"] > 0.22:
        add("WARN", "edge", f"Busy edges (edge={m['edge']}).", "Simplify the background and cut decorative shapes.")
    if m["palette"] > 16:
        add("FAIL", "palette", f"{m['palette']} significant colors.", "Reduce to 1 dominant + 1 support + 1 accent (+ neutrals).")
    elif m["palette"] > 12:
        add("WARN", "palette", f"{m['palette']} significant colors.", "Trim the palette.")
    if m["hues"] > 4:
        add("FAIL", "hues", f"{m['hues']} hue families.", "Maximum 3 hue families including any photo.")
    elif m["hues"] > 3:
        add("WARN", "hues", f"{m['hues']} hue families.", "Merge two hues.")
    return items


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    m = measure(a.image)
    items = judge(m)
    fails = sum(1 for i in items if i["level"] == "FAIL")
    if a.json:
        print(json.dumps({"file": a.image, "metrics": m, "items": items}, indent=2))
    else:
        print(f"poster_pixels: {a.image}")
        print(f"  calm={m['calm']}  edge={m['edge']}  palette={m['palette']}  hues={m['hues']}")
        for i in items:
            print(f"  [{i['level']}] {i['metric']}: {i['message']}\n         -> {i['fix']}")
        print("\n  " + ("PASS" if not items else f"{fails} fail, {len(items) - fails} warn  =>  LOOK AGAIN"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
