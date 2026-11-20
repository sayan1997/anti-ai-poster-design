---
name: anti-ai-poster-design
description: Design advertisement posters, banners, flyers, flex/hoarding artwork, menu boards, festival or puja banners, sale/offer graphics and social-media creatives that look deliberately human-designed instead of the stereotypical "AI-generated" look (gold gradient lettering, ornate filigree frames, a pill or ribbon behind every line, glossy glowing stock food, icon-in-circle grids, five fonts at once, garbled text). Use whenever the user asks to make, generate, design, redesign, critique or audit a poster, banner, flyer, ad creative or announcement graphic, or asks for an image-generation prompt for one, even if they never mention "AI look". Works with any model, producing HTML/SVG, an image-model prompt, or a written design spec.
---

# Anti-AI Poster Design

Posters made by default-settings generators share a fingerprint: **everything is added, nothing is removed.** Gold gradient type, filigree borders, a pill behind every line, glowing food, icon grids, three scripts, and fine print, all at the same volume. Nothing is emphasized, so the eye has nowhere to land, and viewers read it as machine-made.

A human designer works the other way around: **one idea, one hero, one action, then delete.** This skill makes that process explicit so any model can follow it.

> **The rule in one line:** one idea, one hero, one action; at most 3 hue families, 2 type voices (+1 per extra script), 3 type sizes, 1 filled container, ~25 words, and at least 30% calm space.

Evidence for every rule lives in `references/ai-tells-catalog.md` (analysis of 12 AI-style street banners vs. 8 human-designed references). Read it when you need the reason behind a rule or are asked to explain a critique.

## Workflow

### 1. Intake: decide, don't interrogate
Gather (ask at most 3 short questions, only for what is truly missing; otherwise state assumptions in one line and proceed):
- **Offer**: what is being sold or announced, and the single thing the viewer should do.
- **Where it will be seen**: street banner read from 10 m, phone feed, A4 print. This sets the minimum text size.
- **Language(s) and script(s)**, **size**, and **assets supplied** (logo, photo, colors, text).

**Never invent facts.** Phone numbers, addresses, prices, founding years ("since 1857"), certifications, committee or person names, and awards must come from the client. If missing, write a visible bracketed placeholder such as `[PHONE]` or `[ঠিকানা]`. Invented heritage claims and fake seals are a signature of AI posters.

### 2. Write the copy first
A poster has three layers of text and no more:
1. **Headline**: 1-5 words. The hook, the item, or the event.
2. **Offer / proof**: one line, ideally with a specific (price, time, place, item name).
3. **Action + contact**: one call-to-action and one contact line.

Total target: **<= 25 words** (hard ceiling 40). Specific beats generic: *"Kosha mangsho + paratha, Rs.120"* beats *"Authentic taste experience"*. Avoid the clichés listed in the catalog (P1): "fresh & pure", "every bite pure delight", "real taste", "your health, our priority", "nature stays here", "premium quality". Do not repeat the brand or offer, and do not translate every line into a second language (see Indic section).

### 3. Pick one layout skeleton
Choose exactly one from `references/design-system.md`:
- **A. Giant Word**: the headline is the picture (food stalls, sales, events).
- **B. Hero + Corner**: one real hero image bleeding off an edge, headline opposite.
- **C. Split**: two halves divided by color (two offers, date + place).
- **D. Type Only**: no image; typographic hierarchy plus at most one flat shape. *Always better than a bad generated image.*
- **E. Ledger**: information-heavy posters; clean two-column list, max 6 rows, no icons.

### 4. Set the system before drawing
- **Palette**: take one of the ten in `design-system.md` or derive one: 60% ground, 30% support, 10% accent, plus ink. Flat fills only. Echo the subject's color in one type element or the call-to-action.
- **Type**: one display face + one text face (+ one family per additional script). Sizes: display (9-45% of canvas height), support (3.5-6%), detail (2.8-4%), meta (2-2.6%). Nothing below 2%.
- **Margins**: 6-8% of the short side. Align everything to one edge.

### 5. Build, using whichever mode your tools allow

**Mode A, you can write and render code (preferred).**
1. Copy `assets/template.html` (Giant Word skeleton with tokens) or start from an example in `examples/`.
2. Fill the palette, fonts and copy. Delete what you don't need; add nothing decorative.
3. Render with `python scripts/render_poster.py poster.html poster.png --width W --height H` (or screenshot in any browser).
4. Look at the actual PNG. Never judge a poster from the code alone.

**Mode B, you can only call an image-generation model.** Follow `references/image-model-prompting.md`: generate the *hero image only, with no text*, then add the text in any layout tool. If you must generate the whole poster, constrain it to <= 3 short text items, hex-coded palette, two typefaces, no ornaments. Always proofread every character.

**Mode C, no tools.** Deliver a design spec: layout skeleton name, ASCII wireframe, exact hex colors, font names, sizes as % of canvas height, the final copy, and any placeholders. Include HTML/SVG if you can write it.

### 6. Audit, then subtract
Run what exists, then do the manual pass.
- `python scripts/poster_lint.py poster.html`: static checks for fonts, gradients, effects, containers, colors, text size, word count and clichés.
- `python scripts/poster_pixels.py poster.png`: measures calm space, edge busyness, palette size and hue count on the render.
- **Squint test**: shrink to ~300 px wide. One dominant shape and one secondary shape should remain.
- **Three-second test**: can a stranger say what is offered and what to do?
- **Subtraction pass (mandatory)**: remove the least necessary 25-30% of elements, then check again. If you cannot name the job of an element, delete it.
- **Proofread** every word in every script, aloud.

### 7. Deliver
Give the file(s) plus **three lines**: what the focal point is, which palette/fonts were used, and which facts are placeholders. Do not lecture. Offer one alternative layout if useful.

## Hard bans (the tells, in short)
Full catalog with reasons and replacements: `references/ai-tells-catalog.md`.

| Area | Never do this | Instead |
|---|---|---|
| Type | Gold-gradient, bevelled or embossed lettering (T1); outline + drop shadow on text (T2); script/italic taglines (T5); 3+ type voices (T4); text smaller than ~2% of canvas height (T8); ALL CAPS shouting, "39 ONLY", ellipses (T9) | Flat single-color type; one display + one text face; scale contrast >= 2.5x |
| Color | Gold + maroon "premium" costume (C1); yellow/red/blue/green pile-up (C2); 4+ hue families (C3); gradients, glow, bokeh, lens flare, vignette (C4-C6) | 60/30/10 palette, flat fills, one believable light |
| Decoration | Filigree corners and borders (D1); swirl dividers (D2); a pill/ribbon/plaque behind every line (D3); fake seals and medallions (D4); flame/sparkle/leaf/lotus clip-art (D5); icon-in-circle grids (D6); phone icon on every contact line (D7); steam wisps (D11) | Whitespace and alignment; at most one container, for the CTA or price |
| Imagery | Glossy over-sharpened "hero food" (I1); airbrushed faces and generated deities (I2); eight dishes on one table (I3); wood/leather/parchment textures (I4); mixed cartoon + photo (I5); category props instead of an idea (I6) | One hero, real photo or simple flat illustration, or no image |
| Layout | No dominant element (L1); no whitespace (L2); stacked horizontal bands (L3); brand repeated 2-3x (L4); 6+ list items (L5); contact strip with tiny numbers (L6); several CTAs (L7) | One focal point, one axis, one action, one big contact line |
| Copy | Generic superlatives (P1); invented heritage claims (P2); same text in two scripts (P3); 40+ words (P4) | Specific, short, client-supplied facts |
| Text rendering | Letting an image model render text that must be correct | Compose text separately and proofread |

## What to do instead (the positive toolkit)
- **Hierarchy by scale**: the headline is 2.5x or more the size of the next level. Weight and color are secondary tools.
- **Whitespace is a design element**: leave a large quiet area on purpose. It is what the eye rests on and what the text sits in.
- **One axis**: align to one edge; allow exactly one deliberate exception.
- **Color echo**: repeat the subject's color in the headline or CTA.
- **Depth by layering**: overlap type and subject, or add one soft contact shadow, instead of gloss.
- **Edge metadata**: brand, date and handle small at the corners; everything else gets out of the way.
- **Texture only as paper**: grain or halftone at 3-6% opacity, or none.

## Traditional Mode (when the client explicitly wants an ornate or festive look)
Festival, puja, jeweller and wedding banners may legitimately carry tradition. Keep the tradition, drop the clutter:
- Allow **one** ornament device: a single flat motif band *or* a single border, never both, never in the corners as well.
- Draw it **flat in one color**; no bevel, gradient, glow or shine.
- Keep the same discipline: one headline, <= 2 colors + ground, <= 2 type voices, readable contact line.
- For deity or portrait imagery use real photographs or licensed artwork, or go type-only. Do not synthesize deity faces.
- See `examples/puja-banner.html` for a worked case.

## Indic and bilingual posters
Bengali and other Indic scripts need real shaped text, one family, no effects, no letter-spacing, roomier line height and about 1.1x size relative to Latin. Do not repeat the same sentence in both scripts: the primary language carries the headline, the second carries *different* information. Read `references/bengali-and-indic-typography.md` before setting any Indic text; it also covers numerals, fonts and a restrained motif vocabulary for Bengal.

## Reviewing an existing poster
When asked to critique rather than create: list the tells by ID with what you see, give three highest-impact removals first, then propose a restructured layout using one skeleton, and offer to rebuild it. Quote measurements from `poster_pixels.py` if an image is available. Be specific and kind; focus on the design, not on whether AI made it.

## Files
- `references/ai-tells-catalog.md`: the evidence and the full list of tells (T/C/D/I/L/P IDs).
- `references/design-system.md`: canvas sizes, five layout skeletons, type scale, ten palettes, font pairings, spacing, quality tests.
- `references/bengali-and-indic-typography.md`: Indic rendering, sizing, bilingual layout, numerals, cultural notes.
- `references/image-model-prompting.md`: two-stage workflow, prompt template, words to avoid, negative prompt.
- `assets/template.html`: starter poster (Giant Word, 1080x1350).
- `scripts/render_poster.py`, `scripts/poster_lint.py`, `scripts/poster_pixels.py`: render and audit.
- `examples/`: three worked posters (`tea-stall`, `puja-banner`, `music-ledger`), each as HTML source + PNG.
