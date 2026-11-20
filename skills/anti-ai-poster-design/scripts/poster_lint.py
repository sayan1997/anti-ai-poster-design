#!/usr/bin/env python3
"""poster_lint.py - static audit of an HTML or SVG poster for "AI-look" tells.

Usage:
    python poster_lint.py poster.html            # human-readable report
    python poster_lint.py poster.svg --json      # machine-readable
    python poster_lint.py poster.html --strict   # warnings also fail (exit 1)

Standard library only. Checks are heuristics: they catch the common, objective tells
(see references/ai-tells-catalog.md for IDs). They cannot judge taste. Always also run
the squint / three-second tests from SKILL.md on the rendered image.

Exit code: 0 = no FAIL, 1 = at least one FAIL (or WARN with --strict), 2 = usage error.
"""
import argparse
import colorsys
import html as htmllib
import json
import re
import sys
from collections import Counter
from pathlib import Path

GENERIC_FONTS = {
    "serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-sans-serif",
    "ui-serif", "ui-monospace", "inherit", "initial", "unset", "-apple-system",
    "blinkmacsystemfont", "emoji", "math", "fangsong",
}

# Over-used in generated "premium / festive" posters (T1, T5, T6). Warn, not forbid.
CLICHE_FONTS = [
    "cinzel", "trajan", "playfair", "pacifico", "lobster", "dancing script", "great vibes",
    "sacramento", "allura", "alex brush", "parisienne", "satisfy", "papyrus", "brush script",
    "comic sans", "kaushan", "cookie", "yellowtail", "tangerine",
]

CLICHE_PHRASES = [
    "elevate your", "unleash", "discover the", "experience the", "seamless", "crafted with passion",
    "fresh & pure", "fresh and pure", "pure delight", "every bite", "real taste", "your health, our priority",
    "your health our priority", "good food good mood", "nature stays here", "premium quality",
    "world-class", "world class", "state-of-the-art", "taste the difference", "where flavor meets",
    "where flavour meets", "culinary journey", "a symphony of", "tapestry", "redefin", "next level",
    "unparalleled", "your one-stop", "your one stop", "authentic taste", "mouth-watering",
    "mouthwatering", "finger-licking", "best in town", "100% pure", "heritage of", "since 18", "since 19",
]

ORNAMENT_CHARS = "❖✦✧❀❁✿❃❋☙❧⁂✺✹✸❂☸✥✤✣❦❥❤♛♔✪✫✬✭✮✯✰❄❅❆"
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]")

PILL_CLASS_RE = re.compile(
    r"\b(badge|ribbon|pill|plaque|cartouche|seal|medallion|stamp|banner-?strip|label)\b", re.I)

NAMED_GOLDISH = {"gold", "goldenrod", "darkgoldenrod", "gold-gradient", "metallic"}


# ----------------------------------------------------------------------------- helpers
def parse_color_tokens(text):
    """Return list of (r,g,b) 0-255 from hex / rgb() / hsl() tokens."""
    out = []
    for m in re.finditer(r"#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b", text):
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        out.append(tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)))
    for m in re.finditer(r"rgba?\(\s*([\d.]+%?)[\s,]+([\d.]+%?)[\s,]+([\d.]+%?)", text):
        vals = []
        for g in m.groups():
            vals.append(float(g[:-1]) * 2.55 if g.endswith("%") else float(g))
        out.append(tuple(int(max(0, min(255, v))) for v in vals))
    for m in re.finditer(r"hsla?\(\s*([\d.]+)(?:deg)?[\s,]+([\d.]+)%[\s,]+([\d.]+)%", text):
        h, s, l = float(m.group(1)) / 360.0, float(m.group(2)) / 100.0, float(m.group(3)) / 100.0
        r, g, b = colorsys.hls_to_rgb(h % 1.0, l, s)
        out.append((int(r * 255), int(g * 255), int(b * 255)))
    return out


def hsv(rgb):
    h, s, v = colorsys.rgb_to_hsv(*(c / 255.0 for c in rgb))
    return h * 360.0, s, v


def is_neutral(rgb):
    _, s, v = hsv(rgb)
    return s < 0.14 or v < 0.10


def hue_family(rgb):
    return int(hsv(rgb)[0] // 30) % 12


def is_goldish(rgb):
    h, s, v = hsv(rgb)
    return 36 <= h <= 52 and 0.45 <= s <= 0.95 and v >= 0.65


def strip_comments(src):
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S)
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    return src


def visible_text(src):
    src = re.sub(r"<(style|script|title|head)\b.*?</\1>", " ", src, flags=re.S | re.I)
    src = re.sub(r"<[^>]+>", " ", src)
    src = re.sub(r"&nbsp;|&amp;|&[a-z]+;", " ", src)
    return re.sub(r"\s+", " ", src).strip()


def canvas_height(src):
    m = re.search(r"viewBox\s*=\s*[\"']\s*[\d.\-]+[\s,]+[\d.\-]+[\s,]+[\d.]+[\s,]+([\d.]+)", src)
    if m:
        return float(m.group(1))
    m = re.search(r"@page\s*\{[^}]*size\s*:\s*([\d.]+)px\s+([\d.]+)px", src, re.S)
    if m:
        return float(m.group(2))
    m = re.search(r"\.poster\s*\{[^}]*?height\s*:\s*([\d.]+)px", src, re.S)
    if m:
        return float(m.group(1))
    m = re.search(r"<svg[^>]*\sheight\s*=\s*[\"']([\d.]+)", src)
    if m:
        return float(m.group(1))
    return None


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, tid, msg, fix=None):
        self.items.append({"level": level, "id": tid, "message": msg, "fix": fix})

    def count(self, level):
        return sum(1 for i in self.items if i["level"] == level)


# ----------------------------------------------------------------------------- checks
def run_checks(path, max_fonts, max_words):
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    src = strip_comments(raw)
    rep = Report()
    is_svg = path.lower().endswith(".svg") or src.lstrip().startswith("<svg")

    # --- T4 / fonts -----------------------------------------------------------------
    fams = []
    for m in re.finditer(r"font-family\s*[:=]\s*([^;}>\"]+|\"[^\"]+\"|'[^']+')", src, re.I):
        decl = m.group(1)
        # take the first non-var, non-generic family of each declaration
        for part in decl.split(","):
            name = part.strip().strip("\"'").strip()
            if not name or name.lower().startswith("var("):
                continue
            if name.lower() in GENERIC_FONTS:
                continue
            fams.append(name.lower())
            break
    # CSS variables holding font stacks
    for m in re.finditer(r"--font[\w-]*\s*:\s*([^;]+);", src):
        first = m.group(1).split(",")[0].strip().strip("\"'").lower()
        if first and first not in GENERIC_FONTS:
            fams.append(first)
    uniq_fams = sorted(set(fams))
    if len(uniq_fams) > max_fonts:
        rep.add("FAIL", "T4", f"{len(uniq_fams)} font families in use ({', '.join(uniq_fams)}); max {max_fonts}.",
                "Keep display + text (+1 family per extra script). Vary size/weight instead of family.")
    elif len(uniq_fams) == max_fonts:
        rep.add("INFO", "T4", f"{len(uniq_fams)} font families ({', '.join(uniq_fams)}). At the limit; fine only if one is Indic.")
    for f in uniq_fams:
        for bad in CLICHE_FONTS:
            if bad in f:
                rep.add("WARN", "T1/T5/T6", f"Over-used 'AI look' typeface: {f}.",
                        "Prefer a sturdy grotesque or warm text serif; use script/inscriptional faces only on explicit request, flat.")

    # --- T1 / C4 gradients and gold -------------------------------------------------
    grads = re.findall(r"(?:linear|radial|conic)-gradient\s*\((?:[^()]|\([^()]*\))*\)", src, re.I)
    svg_grads = len(re.findall(r"<(?:linearGradient|radialGradient)\b", src))
    total_grads = len(grads) + svg_grads
    if total_grads > 2:
        rep.add("FAIL", "C4", f"{total_grads} gradients. Gradients are a core AI-look tell.",
                "Use flat fills. At most one subtle background gradient.")
    elif total_grads > 0:
        rep.add("WARN", "C4", f"{total_grads} gradient(s) found.", "Confirm each is subtle and not on text.")
    gold_grad = False
    for g in grads:
        cols = [c for c in parse_color_tokens(g) if is_goldish(c)]
        if len(cols) >= 2:
            gold_grad = True
    for blk in re.findall(r"<(?:linearGradient|radialGradient)\b.*?</(?:linearGradient|radialGradient)>", src, re.S):
        if len([c for c in parse_color_tokens(blk) if is_goldish(c)]) >= 2:
            gold_grad = True
    if gold_grad:
        rep.add("FAIL", "T1", "Gold gradient detected (metallic gold lettering/fills).",
                "Use one flat ochre such as #C8962E, never a gradient.")
    if re.search(r"background-clip\s*:\s*text|-webkit-background-clip\s*:\s*text", src, re.I):
        rep.add("FAIL", "T1", "Gradient/texture clipped into text (background-clip:text).", "Flat single-color text.")

    # --- T2 / C5 effects ------------------------------------------------------------
    n_text_shadow = len(re.findall(r"text-shadow\s*:", src, re.I))
    n_stroke = len(re.findall(r"-webkit-text-stroke\s*:|paint-order\s*:\s*stroke", src, re.I))
    n_svg_stroke_text = len(re.findall(r"<text\b[^>]*\sstroke\s*=\s*[\"'](?!none)", src, re.I))
    n_drop = len(re.findall(r"drop-shadow\s*\(", src, re.I))
    n_blur = len(re.findall(r"filter\s*:[^;]*blur\s*\(|<feGaussianBlur", src, re.I))
    big_box = len([m for m in re.finditer(r"box-shadow\s*:([^;]+);", src, re.I)
                   if re.search(r"\b(\d{2,3})px", m.group(1))])
    if n_text_shadow or n_stroke or n_svg_stroke_text:
        rep.add("FAIL", "T2", f"Text effects found (text-shadow x{n_text_shadow}, text-stroke x{n_stroke + n_svg_stroke_text}).",
                "Fix contrast with a calm background area or a solid shape, not outlines or shadows.")
    if n_drop + n_blur + big_box > 1:
        rep.add("WARN", "C5", f"Glow/blur/shadow effects (drop-shadow x{n_drop}, blur x{n_blur}, large box-shadow x{big_box}).",
                "Allow at most one soft contact shadow under the hero object.")
    if re.search(r"mix-blend-mode\s*:\s*(screen|color-dodge|overlay)", src, re.I):
        rep.add("WARN", "C5", "Light-blend modes (screen/dodge/overlay) often produce glow.", "Remove unless essential.")

    # --- Colors: C1/C2/C3 -----------------------------------------------------------
    color_src = re.sub(r"https?://\S+", " ", src)
    colors = parse_color_tokens(color_src)
    chroma = [c for c in colors if not is_neutral(c)]
    # merge near-duplicates (same hue family and similar lightness)
    merged = {}
    for c in chroma:
        h, s, v = hsv(c)
        merged[(hue_family(c), round(s * 4), round(v * 4))] = c
    families = sorted({hue_family(c) for c in chroma})
    # collapse adjacent hue bins (red wraps)
    fam_clusters = []
    for f in families:
        if fam_clusters and (f - fam_clusters[-1][-1]) % 12 == 1:
            fam_clusters[-1].append(f)
        else:
            fam_clusters.append([f])
    if len(fam_clusters) > 1 and (fam_clusters[0][0] - fam_clusters[-1][-1]) % 12 == 1:
        fam_clusters[0] = fam_clusters.pop() + fam_clusters[0]
    n_fam = len(fam_clusters)
    if n_fam > 4:
        rep.add("FAIL", "C3", f"{n_fam} distinct hue families in source colors; max 3 (neutrals excluded).",
                "Pick 1 dominant + 1 support + 1 accent hue. Use tints, not new hues.")
    elif n_fam > 3:
        rep.add("WARN", "C3", f"{n_fam} hue families; target is 3 including any photo.", "Merge two hues.")
    if len(merged) > 9:
        rep.add("WARN", "C2", f"{len(merged)} distinct chromatic colors; target <= 8 in total.", "Reduce the palette.")
    golds = [c for c in chroma if is_goldish(c)]
    dark_ground = any(sum(c) < 150 and (hue_family(c) in (0, 1, 11)) for c in colors)
    if golds and dark_ground and re.search(r"maroon|#[4-7][0-9a-f]0[0-9a-f]{3}", src, re.I) is None:
        pass  # kept simple: gold+maroon check below
    maroonish = [c for c in colors if 60 <= c[0] <= 140 and c[1] < 50 and c[2] < 60]
    if golds and maroonish:
        rep.add("WARN", "C1", "Gold + maroon/brown pairing (the default 'premium' costume).",
                "Choose the palette from the subject; if gold is required use one flat ochre as the single accent.")
    for nm in NAMED_GOLDISH:
        if re.search(rf"\b{nm}\b", color_src, re.I):
            rep.add("WARN", "C1", f"Named gold color '{nm}' used.", "Use a specific flat ochre hex.")
            break

    # --- Decoration: D1-D11 ---------------------------------------------------------
    decoded = htmllib.unescape(raw)
    orn = [ch for ch in decoded if ch in ORNAMENT_CHARS]
    emojis = EMOJI_RE.findall(htmllib.unescape(visible_text(raw)))
    if orn or emojis:
        rep.add("FAIL", "D5", f"Ornament/emoji characters used as decoration ({len(orn) + len(emojis)}).",
                "Remove; if a motif is essential, draw one flat shape.")
    classes = " ".join(re.findall(r"class\s*=\s*[\"']([^\"']+)", src, re.I))
    ids = " ".join(re.findall(r"\bid\s*=\s*[\"']([^\"']+)", src, re.I))
    pill_hits = PILL_CLASS_RE.findall(classes + " " + ids)
    radii = re.findall(r"border-radius\s*:\s*([\d.]+)(px|%|rem|em)?", src, re.I)
    pills = 0
    for val, unit in radii:
        v = float(val)
        if (unit in ("px", "") and v >= 40) or (unit == "%" and v >= 40) or (unit in ("rem", "em") and v >= 2.5):
            pills += 1
    if len(pill_hits) + pills > 3:
        rep.add("FAIL", "D3", f"Too many container shapes (pill/badge/ribbon-like: {len(pill_hits)} names, {pills} large radii).",
                "At most one filled container (the CTA or the price).")
    elif len(pill_hits) + pills > 1:
        rep.add("WARN", "D3", f"{len(pill_hits) + pills} container-like shapes; limit is 1.", "Let grouping and whitespace do the work.")
    if re.search(r"(filigree|arabesque|ornament|flourish|swirl|garland|corner)", classes + ids, re.I):
        rep.add("WARN", "D1/D2", "Class/id names suggest ornament (filigree, flourish, corner, swirl...).", "Remove frames, corners and dividers.")
    n_borders = len(re.findall(r"(?<![\w-])border(?:-[a-z]+)?\s*:\s*[^;]*\b(?:[3-9]|\d{2,})px", src, re.I))
    if n_borders > 3:
        rep.add("WARN", "D1", f"{n_borders} thick borders (>=3px).", "Avoid framing every block.")
    n_bg_img = len(re.findall(r"url\(\s*[\"']?(?!data:)", src, re.I))
    n_img = len(re.findall(r"<img\b|<image\b", src, re.I))
    if n_img + n_bg_img > 3:
        rep.add("WARN", "D9/I3", f"{n_img + n_bg_img} images referenced; one hero is enough.", "Keep one image language and one hero.")

    # --- Typography sizes and hierarchy: L1 / T8 ------------------------------------
    sizes = []
    for m in re.finditer(r"font-size\s*[:=]\s*[\"']?\s*([\d.]+)\s*(px|pt)?", src, re.I):
        v = float(m.group(1))
        if m.group(2) == "pt":
            v *= 1.3333
        sizes.append(v)
    ch = canvas_height(raw)
    if sizes:
        uniq_sizes = sorted(set(round(s) for s in sizes))
        if len(uniq_sizes) > 6:
            rep.add("WARN", "T4/L1", f"{len(uniq_sizes)} distinct font sizes ({uniq_sizes}); aim for 3-4.",
                    "Use a strict scale: display / support / detail / meta.")
        big, small = max(sizes), min(sizes)
        median = sorted(sizes)[len(sizes) // 2]
        if median > 0 and big / median < 2.2:
            rep.add("WARN", "L1", f"Weak hierarchy: largest text is only {big / median:.1f}x the median size (aim >= 2.5x).",
                    "Make the headline dramatically larger or the rest smaller.")
        if ch:
            if small / ch < 0.02:
                rep.add("FAIL", "T8", f"Smallest text is {small:.0f}px = {100 * small / ch:.1f}% of canvas height (<2%).",
                        "Delete it or promote it. Street posters have no fine print.")
            if big / ch < 0.07:
                rep.add("WARN", "L1", f"Largest text is only {100 * big / ch:.1f}% of canvas height.",
                        "A human-looking poster usually has a headline >= 9% of height.")

    # --- Copy: P1 / P4 / L4 ---------------------------------------------------------
    text = visible_text(raw) if not is_svg else " ".join(re.findall(r">([^<>]+)<", re.sub(r"<(style|script|defs)\b.*?</\1>", " ", raw, flags=re.S)))
    words = re.findall(r"[\w\u0980-\u09FF\u0900-\u097F₹@.+-]+", text)
    n_words = len(words)
    if n_words > max_words * 1.6:
        rep.add("FAIL", "P4", f"{n_words} words on the poster; target <= {max_words}.", "Cut to headline + offer + action. Move the rest to a menu/QR/DM.")
    elif n_words > max_words:
        rep.add("WARN", "P4", f"{n_words} words on the poster; target <= {max_words}.", "Cut.")
    low = text.lower()
    hits = [p for p in CLICHE_PHRASES if p in low]
    if hits:
        rep.add("WARN", "P1", "Cliche/generic copy: " + ", ".join(sorted(set(hits))[:6]) + ".",
                "Replace with specifics: the dish, the price, the hour, the street.")
    # repeated multi-letter tokens (brand name repeated 3x)
    toks = [w.lower() for w in re.findall(r"[A-Za-z\u0980-\u09FF]{4,}", text)]
    common = {"with", "from", "that", "this", "your", "have", "will", "free", "open", "call", "only", "from"}
    cnt = Counter(t for t in toks if t not in common)
    rep_tokens = [t for t, n in cnt.items() if n >= 3]
    if rep_tokens:
        rep.add("WARN", "L4", "Words repeated 3+ times: " + ", ".join(rep_tokens[:5]) + ".", "State the brand/offer once, large.")
    if re.search(r"\b\d+\s*only\b", low):
        rep.add("WARN", "T9", "'<price> ONLY' pattern.", "Show the price alone: Rs.120.")
    letters = re.sub(r"[^A-Za-z]", "", text)
    if len(letters) > 20 and sum(1 for c in letters if c.isupper()) / len(letters) > 0.6:
        rep.add("WARN", "T9", "Mostly ALL CAPS copy.", "Sentence case except for one short label.")
    if len(re.findall(r"!", text)) > 1 or "..." in text or "\u2026" in text:
        rep.add("WARN", "T9", "Multiple exclamation marks or ellipses.", "Calm, declarative copy.")

    # --- Indic: T7 ------------------------------------------------------------------
    for m in re.finditer(r"([^{}]*(?:\.bn\b|\bbengali\b|\[lang=[\"']?bn|:lang\(bn\))[^{}]*)\{([^}]*)\}", src, re.I):
        body = m.group(2)
        ls = re.search(r"letter-spacing\s*:\s*(-?[\d.]+)", body)
        if ls and float(ls.group(1)) != 0:
            rep.add("WARN", "T7", "Letter-spacing on Bengali/Indic text breaks conjunct joins.", "Set letter-spacing: 0.")
        if re.search(r"font-style\s*:\s*italic", body, re.I):
            rep.add("WARN", "T7", "Italic on Indic text (synthetic slant).", "Remove.")
    if re.search(r"[\u0980-\u09FF\u0900-\u097F]", raw) and not re.search(
            r"(bengali|bangla|siliguri|devanagari|hind|noto|mukta|tiro|baloo|anek|galada|atma|lohit|kalpurush|sarabun|poppins)", src, re.I):
        rep.add("WARN", "T7", "Indic text present but no Indic-capable font is named.",
                "Name a real font (e.g. Hind Siliguri, Anek Bangla) so shaping and glyph coverage are correct.")

    # --- Placeholders / facts: P2 ---------------------------------------------------
    if re.search(r"(?<!\d)\b(?:\+?91[\s-]?)?[6-9]\d{9}\b", visible_text(raw)):
        rep.add("INFO", "P2", "A phone number is present. Confirm the client supplied it (never invent contact details).")
    if re.search(r"\b(since|est\.?|established)\s*(?:in\s*)?(1[89]\d{2}|20[0-2]\d)\b", low):
        rep.add("WARN", "P2", "A founding year/heritage claim appears. Confirm the client supplied it.", "Remove if not supplied.")

    return rep, {
        "fonts": uniq_fams, "gradients": total_grads, "hue_families": n_fam,
        "chromatic_colors": len(merged), "words": n_words, "font_sizes": sorted(set(round(s) for s in sizes)),
        "canvas_height": ch,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="treat WARN as failure")
    ap.add_argument("--max-fonts", type=int, default=3, help="max font families (default 3: display + text + one Indic)")
    ap.add_argument("--max-words", type=int, default=30, help="word budget (default 30)")
    a = ap.parse_args()

    if not Path(a.file).exists():
        print(f"not found: {a.file}", file=sys.stderr)
        return 2
    rep, summary = run_checks(a.file, a.max_fonts, a.max_words)
    fails, warns = rep.count("FAIL"), rep.count("WARN")

    if a.json:
        print(json.dumps({"file": a.file, "fails": fails, "warns": warns, "summary": summary, "items": rep.items},
                         ensure_ascii=False, indent=2))
    else:
        print(f"poster_lint: {a.file}")
        print(f"  fonts={summary['fonts']}  gradients={summary['gradients']}  hue_families={summary['hue_families']}  "
              f"words={summary['words']}  sizes={summary['font_sizes']}")
        order = {"FAIL": 0, "WARN": 1, "INFO": 2}
        for it in sorted(rep.items, key=lambda i: order[i["level"]]):
            print(f"  [{it['level']}] {it['id']}: {it['message']}")
            if it["fix"] and it["level"] != "INFO":
                print(f"         -> {it['fix']}")
        verdict = "PASS" if fails == 0 and (warns == 0 or not a.strict) else "NEEDS WORK"
        print(f"\n  {fails} fail, {warns} warn  =>  {verdict}")
    return 1 if (fails or (a.strict and warns)) else 0


if __name__ == "__main__":
    sys.exit(main())
