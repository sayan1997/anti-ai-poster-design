# Catalog of "AI-poster tells"

Evidence base for the rules in `SKILL.md`. Read this when you need the *reason* behind a rule, when auditing an existing poster, or when a user asks "what exactly is wrong with this?".

**Contents**
1. Source material and honest caveats
2. The core diagnosis
3. Measured differences
4. Catalog of tells: Typography, Color, Decoration, Imagery, Layout, Copy, Text-rendering errors
5. What the human-designed reference set does differently
6. Per-poster notes

---

## 1. Source material and honest caveats

- **12 posters labelled "AI-generated"** by the person who supplied them: photographs of street banners (tea stall, bread-and-cream stall, biryani restaurants, a food-court billboard, jewellers, a pharmacy/clinic, a music academy, a resort, an IT-services shop, festival/puja committees) in West Bengal, India. The labels are the supplier's judgment, not a verified fact.
- **8 posters labelled "not AI"**: mostly modern social-media templates (shoe, headphone, burger, chicken, restaurant, biryani, an article cover). Several still carry template placeholder text, so they are *designer-template* work, not hand-made print work.

Keep in mind when using the findings:

1. **Selection bias.** Both sets are small. Read the percentages as "frequent in this sample", not as laws.
2. **Photographs vs. clean files.** The AI set was photographed outdoors (glare, creases, cables, motion blur), which inflates "busyness" numbers. The direction of the differences matched what is visible by eye, but do not use the exact values as thresholds for clean renders.
3. **Some tells are really "cheap flex-print culture".** Border frames, a pill behind every line and a phone-number strip are common in low-cost banner printing whether or not an AI was involved. They are included because the supplier experienced them as part of the "AI look", and because they share one cause: filling a template to the brim.
4. **The reference set is itself template-flavored.** Type-behind-subject, checkerboards and blob shapes are fashionable template tropes now. Borrow the *principles* (section 5), not the look.
5. One reference poster (a dark biryani composite with levitating ingredients) leans on tropes that also appear in generated imagery. Only its single-word giant headline and single hero subject were counted as good practice.

6. **Regional scope.** The sample is from West Bengal, so the specific motifs (puja banners, Bengali display type) are Bengal-flavored. The principles (hierarchy, restraint, no invented facts) are language-independent; Hindi/Devanagari guidance was added from typographic practice, not from a sampled set.

Fonts below are identified **by eye, by class** ("looks like an inscriptional Roman cap"), not by exact name.

---

## 2. The core diagnosis

The sampled AI posters are not bad because of any single ingredient. They are bad because **nothing is ever left out.**

1. **Additive generation.** Each "richness" cue (gold, filigree, glow, icon, badge, flame, leaf) is added independently and nothing subtracts. Result: maximalism without hierarchy.
2. **Container-itis.** Almost every line of text sits inside its own pill, ribbon, plaque or cartouche. When everything is framed, nothing is emphasized.
3. **Averaged style.** Each category gets its statistical-average costume: *premium food = gold + maroon + filigree + steam; health = pale gradient + stethoscope + heart-ECG + circle icons; resort = palm tree + sunset + script tagline; jeweller = gold coins + bridal model + parchment list.* The costume replaces an idea.
4. **Texture everywhere.** Gloss, glow, bokeh, vignette and gradient are applied to the whole canvas, leaving no calm area for the eye or for the text.

If you remember one thing: **a human designer's most-used tool is deletion.**

---

## 3. Measured differences

Quick image statistics on the two sets (thumbnails at <=400 px):

| Metric | AI set (n=12) | Reference set (n=8) |
|---|---|---|
| Edge density (share of pixels on a strong edge, i.e. "busyness") | **0.31** (0.24-0.37) | **0.16** (0.08-0.22) |
| Distinct colors each covering >=1.5% of the image | **17.7** (10-25) | **9.1** (5-13) |
| Hue families holding >=5% of saturated pixels | **3.2** (2-8) | **2.3** (1-4) |
| Mean saturation | 0.34 | 0.38 |
| Mean brightness | 0.58 | 0.76 |

Reading: AI posters carry roughly **twice the visual edges, twice the distinct colors and about one more hue family**, and are darker overall. Saturation alone does *not* separate the sets. Loudness is not the problem, *uncontrolled* loudness is.

---

## 4. Catalog of tells

IDs are used by `scripts/poster_lint.py` and by the checklist in `SKILL.md`. "Seen in" refers to poster numbers in section 6.

### Typography

| ID | Tell | Seen in | Why it reads as AI / template-filled | Do instead |
|---|---|---|---|---|
| T1 | **Gold-gradient lettering**: metallic or embossed headline, often bevelled, on dark maroon/brown/black | 2, 3, 5, 8, 12 | The "luxury" cue applied by default; fake dimensionality fights legibility | Flat single-color type. If gold is wanted, use one flat ochre (e.g. `#C8962E`), never a gradient |
| T2 | **Thick white/cream outline + soft drop shadow** around headline | 4, 6 | A patch for poor contrast against a busy background | Fix contrast at the source: a calm background area or a solid shape behind the text |
| T3 | **Brush-stroke swatch behind text**, and **starburst rays flanking a word** | 1, 9 | Decorative "paint" used instead of hierarchy | Let size and weight make the headline; use at most one burst, for a price |
| T4 | **3-5 different type voices** on one poster (heavy serif + script + rounded sans + condensed caps + tiny serif) | 2, 3, 9, 10, 11 | Each block was styled separately; no system | Max 2 families (+1 per extra script); vary size/weight within a family |
| T5 | **Connected script italics for taglines** ("Nature Stays Here...") | 2, 9, 10, 11 | The "friendly/artisanal" shortcut | Tagline in the text face, small, sentence case |
| T6 | **Inscriptional Roman caps / high-contrast display serifs in gold** for "heritage" | 3, 5, 12 | Statistical shorthand for tradition | A sturdy grotesque or a warm text serif; heritage comes from copy and craft, not costume |
| T7 | **Decorated display Bengali** (bevel, inner shadow, gradient) and **mixing 3+ Bengali styles** | 4, 5, 7, 8 | Effects substitute for design; conjuncts get muddy | One Bengali family, 2 weights, no effects (see `bengali-and-indic-typography.md`) |
| T8 | **Micro-text** (credentials, taglines, descriptions) unreadable from the street | 2, 6, 9, 12 | Added to look "complete" | Anything under ~2% of canvas height gets deleted or promoted |
| T9 | **ALL CAPS + ellipsis + exclamation everywhere**, "39 ONLY" | 2, 3, 6 | Shouting replaces ranking | Caps only for 1-2 short labels; one emphasized thing per poster |
| T10 | **Everything centered** with equal visual weight | 4, 9, 12 | No axis, no tension | Align to one edge; let one element break the grid on purpose |

### Color

| ID | Tell | Seen in | Do instead |
|---|---|---|---|
| C1 | **Gold + maroon/brown/black "premium" palette** | 2, 3, 5, 8, 12 | Choose the palette from the idea (see `design-system.md`); if a dark ground is right, use one warm accent, flat |
| C2 | **Primary triad pile-up**: saturated yellow + red + blue (+ green) in one frame | 1, 4, 5, 7 | 1 dominant + 1 neutral + 1 accent (60/30/10) |
| C3 | **4+ hue families**, e.g. blue skin, red, yellow, pink, green, saffron together | 7, 4, 11 | Cap at 3 hue families *including* the photo |
| C4 | **Gradients on text, skies and radial "burst" backgrounds** | 4, 5, 7, 11 | Flat fills; at most one subtle gradient on the background |
| C5 | **Glow, bloom, bokeh sparkles, lens flare** | 2, 3, 5, 7, 10, 12 | None. Light comes from one believable source |
| C6 | **Dark vignette with warm spotlight on the food** | 2, 3, 12 | Evenly lit, matte, real-looking food on a plain surface |
| C7 | **Category-costume gradients**: pale cyan/green wash for health; blue sky + palm green + sunset orange for resort | 9, 11 | Pick a color from the *product* or the *place*, not the category |

### Decoration

| ID | Tell | Seen in | Do instead |
|---|---|---|---|
| D1 | **Filigree/arabesque corners and frame borders** | 2, 3, 4, 5, 7, 8, 12 | No frame. If tradition demands ornament, use one flat, single-color motif band (see Traditional Mode in `SKILL.md`) |
| D2 | **Swirl dividers** (line with centre diamond) under headlines | 2, 3, 4, 12 | Whitespace is the divider |
| D3 | **A container behind every line**: pill, ribbon, plaque, cartouche, scroll | 3, 4, 5, 7, 8, 9, 10, 11 | At most one container, and only for the call-to-action or price |
| D4 | **Fake heritage seal / medallion** with laurel, flames or stars; invented years and "60 years of tradition" | 3, 8, 12 | Do not invent facts. If a real logo exists, use it as supplied |
| D5 | **Flame, sparkle, leaf-sprig, lotus, hibiscus-garland** clip-art | 1, 3, 4, 7, 9, 11 | Remove. If a motif is essential, use one, large, flat |
| D6 | **Icon-in-colored-circle grids**, a different color per icon | 9, 10 | Plain typographic list with thin rules; icons only if they genuinely clarify, in one color |
| D7 | **Circular phone / WhatsApp / pin glyph repeated per contact line** | 3, 4, 9, 10, 11, 12 | One contact line, number in large plain type |
| D8 | **Arrow call-outs** ("shop this way") | 3 | Put the address in words |
| D9 | **Tilted "polaroid" photo frames with ribbon captions** | 11 | One photograph, full-bleed or cleanly cropped |
| D10 | **Prop piles** (coins, pots, lamps, extra bowls, a tea glass) used as filler | 2, 5, 6 | One hero object |
| D11 | **Steam wisps over every hot dish** | 1, 3 | Omit; if steam is the point, draw one clean shape |

### Imagery

| ID | Tell | Seen in | Do instead |
|---|---|---|---|
| I1 | **Hyper-glossy "hero food"**: over-sharpened, oily highlights, impossible garnish (mint + star anise + egg-like potato), identical glossy look across dishes | 1, 2, 3, 6, 12 | Real photography with natural imperfections, a simple flat illustration, or no image |
| I2 | **Airbrushed faces** (people, deities): symmetrical, large-eyed, plastic skin | 4, 5, 7, 8 | Use real photographs of the actual idol/person, licensed art, or a type-only layout. Avoid generated deity faces: they look uncanny and can offend |
| I3 | **Eight dishes on one table**, no hero | 6 | Choose one dish, show it large |
| I4 | **Dark wood / leather / parchment textures** as backgrounds | 2, 5, 6, 12 | Flat color, or paper grain at <=5% |
| I5 | **Cartoon vector + photographic elements mixed** | 9, 10 | One image language per poster |
| I6 | **Category props instead of an idea** (stethoscope, palm tree + sunset, coin heap, microphone + instrument) | 5, 9, 10, 11 | Ask: what is the *one thing* this customer should feel or do? Show that |
| I7 | **Image fills the whole canvas**; no calm area | most | Reserve at least ~30% of the canvas as quiet space |

### Layout

| ID | Tell | Seen in | Do instead |
|---|---|---|---|
| L1 | **No dominant element**: 3+ things at similar scale | nearly all | Headline >= 2.5x the size of the next level |
| L2 | **Zero whitespace**; margins eaten by borders | nearly all | Margins >= 6% of the short side; unframed |
| L3 | **Stacked horizontal bands** (title band / pill subtitle / info band / footer strip) | 4, 9, 12 | Compose with one axis and one focal area |
| L4 | **Brand name repeated 2-3x**, or the same offer in two languages line by line | 2, 3, 8 | State it once, large |
| L5 | **Information dumping**: 10-row price list, 9 symptoms, 6 services + 3 levels + admission | 5, 9, 10 | Top 3 items on the poster; the rest goes on a menu, QR code or "ask us" |
| L6 | **Contact strip** as a full-width band with small numbers | 3, 4, 9, 10, 11, 12 | One line, big, bottom-aligned |
| L7 | **Competing calls-to-action** | 3, 5, 9 | One action |

### Copy

| ID | Tell | Seen in | Do instead |
|---|---|---|---|
| P1 | **Generic superlatives and paired slogans**: "Fresh & Pure Ingredients", "Every Bite Pure Delight", "Real Taste Real Biryani", "Good Food Good Mood", "Your Health Our Priority", "Nature Stays Here..." | 2, 3, 6, 9, 11 | Specific beats generic: name the dish, the price, the hour, the street |
| P2 | **Unverifiable prestige claims** ("authentic", "heritage", invented founding year) | 3, 8, 12 | Only claims the client supplied |
| P3 | **Same message in two scripts, line for line** | 2, 3, 12 | Primary language large; secondary language small and carrying *different* information |
| P4 | **Over-long copy**: 60-120 words | 2, 5, 9, 10 | <= 25 words |

### Text-rendering errors (generator signature)

Image generators routinely fail at small text. In the sample:

- Misspelled or invented words in small taglines (a "Delicious Destination" line garbled into near-words; "Beginner" misspelled; a "Good Mood" line that reads as a different word).
- Duplicated words/logos, half-formed seal text, unreadable credentials.
- **Semantic misfits**: a camera/"photo" item in a list of music classes.
- Strike-through prices and tiny sub-lines smeared into the texture.

**Rule:** never let an image generator render text that must be correct. Compose text separately (see `image-model-prompting.md`) and proofread every word.

---

## 5. What the human-designed reference set does differently

1. **One dominant headline**: a big word or two-word stack that *is* the poster (`NEW PRODUCT`, `MEGA BURGER`, `CHICKEN & FRIES`, `BIRIYANI`).
2. **One hero subject**, cleanly isolated or cropped.
3. **A simple ground**: flat or very soft one-hue background.
4. **Two fonts at most**: a strong display (condensed grotesque or high-contrast serif) plus a small clean sans for details.
5. **A palette of 2-3 colors with echoes**: the subject's color repeats in type or button (yellow shoes -> yellow button; orange burger -> orange headline; blue checkerboard -> blue headline).
6. **Generous margins; metadata at the edges**: brand top-left, handle/date top-right, URL bottom. Small, quiet, aligned.
7. **One call-to-action**, drawn as a plain shape.
8. **Devices with jobs**: a checkerboard gives rhythm and frames the plate; one starburst carries only the price; a blob shape holds one photo.
9. **Depth from layering, not gloss**: type behind the subject, overlap, a single soft shadow under the object.
10. **Short copy**: roughly 5-25 words in total.

---

## 6. Per-poster notes

Identifiers are neutral (no business names or contact details). Tells refer to the IDs above.

| # | Poster | Main tells |
|---|---|---|
| 1 | Tea-stall menu banner (two panels) | T3 brush swatches and starburst rays, C2 yellow/red/blue/green, D5 leaf sprigs, D11 steam, I1 glossy food, D3 pills for each line |
| 2 | Bread-and-cream stall billboard | T1, T4, T5, T8, T9, C1, C6, C5, D10, I1, I4, P1 "Organic / Fresh & Pure", L4 "Organic" twice, smeared sub-line |
| 3 | Biryani restaurant banners (horizontal + vertical) | T1, T6, C1, D1, D4 seal + flames, D5, D7, D8, D11, I1, L4 name 3x, L5, P1 |
| 4 | IT shop + goddess festival banner | T2, T4, C2, C3, C4, D1, D3 five stacked pills, I2, L3, L6 |
| 5 | Jeweller festive-offer banner | T1, T7, C1, C5, D1, D3, D10 coin heap, I2, I6, L5 ten-row list, L7, P4 |
| 6 | Food-court billboard | T2 chalk-style outline, T4, T8 garbled taglines and micro-footer, C6, D10, I3 eight dishes, I4 |
| 7 | Goddess festival banner with office-bearer boxes | C3 six hue families, C4, D1 floral frame, D3 x8, D5 hibiscus/lamps, I2, T7, L4 |
| 8 | Jeweller pillar/column ad | T1, T7, C1, D1, D3, I2, I6, L4 name top and bottom |
| 9 | Pharmacy/clinic banner | T4, T5, C7, D3 x10, D5, D6 circle icons, D7, I5, I6, L3, L5 nine items, P1 paired English slogans, T8 micro-credentials |
| 10 | Music-academy banner | T4, T5, C5 sparkles, D3, D6, I5, I6, L5, T8 "Beginner" misspelled, semantic misfit "Photo" in a music list |
| 11 | Resort banner | T5, C4, C7, D5, D9 polaroid frames, I6 palm + sunset, P1 "Nature Stays Here...", L4 |
| 12 | Heritage-style dish banner (paratha + curry) | T1, C1, C5 bokeh, D1, D2, D4 fake seal with year, D7, I1, I4, P2 |
