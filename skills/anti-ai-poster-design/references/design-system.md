# Design system for human-looking posters

Concrete numbers so any model can build a restrained poster without guessing.

**Contents**
1. Canvas sizes
2. Layout skeletons
3. Type system
4. Palettes
5. Font pairings
6. Depth and texture without gloss
7. Spacing and alignment
8. Quality tests

---

## 1. Canvas sizes

| Use | Size (px) | Ratio |
|---|---|---|
| Instagram/Facebook portrait post | 1080 x 1350 | 4:5 |
| Square post | 1080 x 1080 | 1:1 |
| Story / Reel cover / WhatsApp status | 1080 x 1920 | 9:16 |
| Landscape banner / flex (3 x 2 ft) | 1800 x 1200 | 3:2 |
| Wide hoarding | 2400 x 800 | 3:1 |
| A4 / A3 print poster | 2480 x 3508 (A4 @300dpi) | 1:1.414 |

For street banners read from 5-20 metres, treat the canvas as a **three-second read**: the headline must survive at 1/5 size.

---

## 2. Layout skeletons

Pick exactly one. Each has one focal area and at least ~30% calm space. Percentages are of canvas width (W) and height (H).

### A. Giant Word
The headline *is* the picture. 1-2 words, 35-55% of H. Everything else small and aligned to the same left edge.
```
+----------------------+
| brand            date|   <- meta row, ~2.2% H text
|                      |
| CHA                  |   <- display, 40-50% H
| kochuri . dalpuri    |   <- support, 5% H
|                      |
| [ CTA ]       98XXX..|   <- one action + one contact
+----------------------+
```
Best for: food stalls, sales, events, anything with a strong one-word hook.

### B. Hero + Corner
One hero subject occupies 45-60% of the canvas, bleeding off one edge. Headline in the opposite quadrant.
```
+----------------------+
| Headline             |
| two lines            |
|        +-------------+
| offer  |    HERO     |
|        |   (bleeds)  |
| CTA    +-------------+
+----------------------+
```
Best for: a single product or dish with a real photo or clean illustration.

### C. Split
Two halves: 50/50 or 60/40, divided by color, not by a drawn line. One half image or big type, the other half information.
Best for: before/after, two-offer posters, events with date + place.

### D. Type Only
No image at all. A strict typographic hierarchy, optionally one flat shape (circle, band, arch) in the accent color.
Best for: festivals, notices, admissions, anything where no good photo exists. **Always better than a bad generated image.**

### E. Ledger
For information-heavy posters (classes, menus, services). One headline, then a clean 2-column list with thin rules between rows. Maximum **6 rows**. No icons. Prices/times right-aligned.
Best for: academies, clinics, price lists.

---

## 3. Type system

**Three sizes only**, plus one optional micro size for the meta row.

| Role | Size (share of canvas height H) | Weight | Notes |
|---|---|---|---|
| Display (headline) | 9-45% of H (min 2.5x the support size) | Bold/Black or Condensed | 1-5 words |
| Support (offer, subline) | 3.5-6% of H | Medium/Regular | max 2 lines |
| Detail (contact, hours) | 2.8-4% of H | Medium | one line |
| Meta (brand, date, handle) | 2.0-2.6% of H | Regular/Medium | only at edges |

Rules:
- **Nothing smaller than 2% of H.** If it needs to be smaller, it does not belong on a street poster.
- **Scale contrast of at least 2.5:1** between display and support. Timid ratios (1.3, 1.5) read as "everything equal".
- **Line length**: <= 28 characters per headline line, <= 45 for support.
- **Leading**: Latin display 0.9-1.0, Latin text 1.25-1.4, Bengali/Indic 1.35-1.6 (see `bengali-and-indic-typography.md`).
- **Letter-spacing**: Latin caps +2% to +6%; Latin display lowercase 0 to -2%; Indic scripts always 0.
- **Case**: sentence case for everything except at most one short caps label.
- **Alignment**: one left edge (or one right edge). Center only a poster with a single short element.
- **Numbers**: prices and phone numbers in tabular/lining figures at Detail size or larger.
- **No effects on text**: no stroke, shadow, glow, bevel, gradient, texture.

---

## 4. Palettes

Each palette: **Ground** (60%), **Support/neutral** (30%), **Accent** (10%), **Ink** (text). Contrast of Ink on Ground >= 7:1 for headlines, >= 4.5:1 for small text. Use flat fills.

| Name | Ground | Support | Accent | Ink | Mood / when |
|---|---|---|---|---|---|
| Kulhad | `#F2E6D3` | `#C9633A` | `#2B5B4A` | `#2A1D17` | Tea, street food, terracotta warmth |
| Mustard Oil | `#F4C430` | `#1F1A14` | `#C3402A` | `#1F1A14` | Bold sales, one-word hooks (Giant Word) |
| Alpona | `#FBF7F0` | `#D8D1C4` | `#B3202A` | `#1E1B1A` | Festivals, red-and-white Bengal feel |
| Hilsa | `#E9EEF0` | `#9FB3BA` | `#E4572E` | `#14232A` | Seafood, cool and crisp |
| Monsoon | `#1E3A34` | `#E8E1CF` | `#E7B23A` | `#F3EEDF` | Dark ground with ONE flat ochre accent; sweets, evening events |
| Paper & Ink | `#F7F5F0` | `#D9D4C7` | `#1F4FD8` | `#111111` | Clinics, education, services; sober and clear |
| Cardamom | `#DDE5D0` | `#7A8F5C` | `#B5472C` | `#1F2A17` | Organic, grocery, wellness |
| Marigold Night | `#161616` | `#3A3A3A` | `#FF9F1C` | `#F5F1E8` | Music, nightlife, a single glow-free accent |
| Shiuli | `#FFFFFF` | `#F5D9C4` | `#E8743B` | `#2B2118` | Autumn festivals, light and airy |
| Kantha Blue | `#EAF0F7` | `#9DB4D3` | `#C23B3B` | `#0F2238` | Textiles, handloom, stationery |

How to apply:
- **Derive from the subject first.** The dish, the product or the place suggests the accent (a mango orange, a tea-leaf green). Echo it in a type color or the CTA.
- **Max 3 hue families on the whole poster, photo included.** Neutrals (white, black, cream, greys) do not count.
- **Tints are fine, new hues are not.** A lighter version of the accent is allowed; a fourth color is not.
- **Gold:** avoid as a gradient. If the brief demands gold, use a flat ochre such as `#C8962E` as the *single accent* on a dark or cream ground.
- **Never** place red text on saturated yellow, or yellow text on white.

---

## 5. Font pairings

All are free on Google Fonts, safe for public use. Use at most **two Latin families** (display + text) plus **one Indic family**.

### Display (pick one)
| Font | Character | Good for |
|---|---|---|
| Bebas Neue | Tall, condensed caps | Giant Word, sales, events |
| Oswald (600-700) | Condensed grotesque | Sturdy headlines |
| Anton | Very heavy condensed | Maximum impact, short words |
| Archivo (Black / Expanded) | Wide grotesque | Modern product posters |
| Fraunces (700) | Soft, warm serif | Food, bakery, gifts |
| DM Serif Display | High-contrast serif | Editorial, restaurants |
| Instrument Serif | Elegant narrow serif | Boutiques, galleries |
| Bricolage Grotesque | Quirky grotesque | Cafes, local brands |

### Text (pick one)
Inter, DM Sans, Work Sans, IBM Plex Sans, Source Sans 3.

### Bengali
| Role | Font |
|---|---|
| Display | Anek Bangla (ExtraBold), Baloo Da 2 (ExtraBold), Noto Serif Bengali (Bold) |
| Text | Hind Siliguri (Medium), Noto Sans Bengali, Anek Bangla (Regular) |
| Editorial serif | Tiro Bangla |

### Be cautious with (over-used in generated "premium" posters)
Cinzel / Trajan-style inscriptional caps; Playfair Display in gold; script faces such as Pacifico, Lobster, Dancing Script, Great Vibes, Sacramento; any bevelled or "3D gold" decorative display. They are not forbidden, but they are the default fingerprint of the AI look. Use them only when the client asks, and then flat, one at a time, with no effects.

---

## 6. Depth and texture without gloss

Allowed, one of each at most:
- **Overlap**: the subject covers part of the headline (type behind subject). Keep the headline readable.
- **One shadow**: a soft contact shadow under the object (offset 0/y, blur ~4% of object height, 15-25% black). Consistent direction across the whole poster.
- **One texture**: paper grain or halftone at 3-6% opacity over the whole canvas. Never wood, leather, parchment or metal.
- **One shape device** with a job: circle behind the hero, arch, band, checkerboard, or a single burst for the price. Not several.
- **Imperfection that feels printed**: slight misregistration of a second ink, a rough edge on a cut-out. Subtle, optional.

Forbidden: glow, bokeh, lens flare, vignette, bevel, emboss, outer glow, neon, animated-looking motion streaks.

---

## 7. Spacing and alignment

- **Outer margin**: 6-8% of the short side. Nothing but the hero image may cross it.
- **Spacing scale**: multiples of 8 px at 1080 wide (8, 16, 24, 40, 64, 96). Use the *same* gap between all items of the same type.
- **Grouping**: related items closer to each other than to anything else (proximity does the work containers did).
- **Axis**: pick one vertical axis (left edge) and hang everything on it; allow exactly one deliberate exception.
- **Edge metadata**: brand top-left, date/handle top-right, contact bottom. All at Meta/Detail size.

---

## 8. Quality tests

1. **Squint test** (blur or shrink to ~300 px wide): you must see one dominant shape and one secondary shape. If you see seven, delete.
2. **Three-second test**: can a stranger say *what is offered* and *what to do* in three seconds?
3. **Distance test**: headline readable at 1/5 size; contact readable at 1/3 size.
4. **Color count**: <= 3 hue families, <= 8 distinct colors total.
5. **Font count**: <= 2 Latin families + 1 per extra script, <= 4 sizes.
6. **Container count**: <= 1 filled shape behind text.
7. **Fact check**: every number, name, claim, year and address on the poster was supplied by the client. Unknowns are bracketed placeholders (`[PHONE]`).
8. **Proofread** every word in every script. Read it aloud.
