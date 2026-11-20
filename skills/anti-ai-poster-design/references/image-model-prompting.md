# Using image-generation models without getting "the AI poster"

Use this file when the only tool available is an image generator (Midjourney, DALL-E, Stable Diffusion, Imagen, Ideogram, Firefly, Flux, etc.) or when you must write a prompt for someone else to paste in.

**Contents**
1. The two-stage rule
2. Stage 1: generate the hero image only
3. Stage 2: compose the text separately
4. Prompt template
5. Words to avoid and words to use
6. Negative prompt
7. If you must generate the whole poster in one shot
8. Checking the result

---

## 1. The two-stage rule

Image generators are good at *pictures* and unreliable at *typography and layout*. Every serious tell in the catalog that involves text (garbled taglines, misspellings, wrong conjuncts, fake seals) comes from asking the generator to do both at once.

**Stage 1**: generate a text-free image of the hero subject on a simple background.
**Stage 2**: place real text on it using HTML/SVG, Canva, Figma, Photopea, PowerPoint, or any layout tool.

If no layout tool exists, output the copy and the layout spec for a human to apply (see Mode C in `SKILL.md`).

## 2. Stage 1: generate the hero image only

Ask for:
- **One subject** (one dish, one product, one person).
- **A plain, quiet background** that leaves a large empty area for type. State where the empty area is ("empty space on the upper left").
- **A believable light source**: a single window light or soft overcast daylight.
- **Real-photography imperfection**: slightly uneven plating, a few crumbs, natural shine only where oil really shines.
- **Real context for the region**: the actual vessel, leaf or plate used locally (a steel plate, a kulhad, a banana leaf), not a generic "luxury" prop.
- **No text, no logo, no watermark.**

## 3. Stage 2: compose the text separately

- Use the layout skeleton, palette and type rules in `design-system.md`.
- Pull the accent color from the image (eyedrop the dominant warm tone) and reuse it for one text element.
- Cut out the subject only if the edge is clean; otherwise crop to a rectangle and align it to the grid.
- Proofread all copy yourself, in every script.

## 4. Prompt template

```
[Subject: one specific dish/product, with its real context], photographed from
[angle: 45 degrees / top-down / eye level], on [plain surface: matte cream
tablecloth / steel counter / plain terracotta tile], soft single window light
from the left, natural shadows, slightly uneven plating, a few crumbs,
true-to-life color, no steam, no glow, no garnish props.
Composition: subject in the [lower right], large empty area on the [upper left]
for text. Muted, matte, editorial food photography, 85mm lens, shallow but
realistic depth of field. No text, no letters, no logo, no watermark.
```

Adapt for non-food: replace the subject and surface; keep light, imperfection and empty-area instructions.

For a **flat illustration** instead of a photo:

```
Flat vector illustration of [single subject], bold simple shapes, [2-3 named
colors from the palette], no gradients, no outlines thicker than 6px, no
shadows, plain [color] background, large empty area on [side]. No text.
```

## 5. Words to avoid and words to use

| Avoid (pushes toward the AI look) | Prefer |
|---|---|
| "ultra detailed", "hyper-realistic", "8k", "masterpiece" | "natural", "documentary", "editorial" |
| "cinematic lighting", "dramatic", "glowing", "golden hour glow" | "soft window light", "overcast daylight" |
| "luxury", "premium", "royal", "opulent", "ornate" | name the real material: "brass", "enamel", "terracotta" |
| "steam rising", "sizzling", "bokeh", "lens flare" | "matte surface", "plain background" |
| "gold lettering", "decorative border", "filigree", "arabesque" | "no border, no ornament" |
| "vibrant", "mouth-watering", "delicious looking" | "true-to-life color" |
| "poster design", "advertisement" (invites templates, badges and fake text) | "photograph" or "illustration" |

## 6. Negative prompt

For models that support one:

```
text, letters, typography, watermark, logo, border, frame, filigree, ornament,
gold gradient, glow, bokeh, lens flare, sparkles, steam, smoke, vignette,
oversaturated, oily highlights, plastic skin, airbrushed, extra fingers,
cluttered background, multiple dishes, props, icons, badges, ribbons
```

For models without a negative prompt, add one sentence at the end: *"Plain, restrained, uncluttered. No decoration, no text, no glow."*

## 7. If you must generate the whole poster in one shot

Use a model that renders text well, and constrain it hard:

1. **At most 3 text items**, each **<= 4 words**, with the exact string in quotes.
2. Say **"one dominant headline, large; everything else small; flat background; no borders; no icons; no decorative elements"**.
3. State the palette by **hex codes** and say "no other colors".
4. State **"two typefaces only"**.
5. **Never** request fine print, taglines, addresses or phone numbers in the image. Add them afterwards.
6. Generate 4 variants, choose the one with the *least* going on, and still proofread every character.

## 8. Checking the result

Run the audit in `SKILL.md` (squint test, three-second test, count colors/fonts/containers). If the image fails, **do not add more**; regenerate with *fewer* instructions or switch to a type-only layout.
