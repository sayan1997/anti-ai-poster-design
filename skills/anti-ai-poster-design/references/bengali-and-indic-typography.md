# Bengali and other Indic scripts on posters

Applies to Bengali first, and in principle to Devanagari, Gurmukhi, Gujarati, Odia, Tamil, Telugu, Kannada, Malayalam. Generated posters tend to treat these scripts as decoration; treat them as real typography.

**Contents**
1. Rendering rules
2. Sizing and spacing
3. Pairing with Latin
4. Bilingual layout
5. Numerals, currency, phone numbers
6. Cultural and religious imagery
7. A restrained motif vocabulary for Bengal
8. Proofreading

---

## 1. Rendering rules

1. **Use real, shaped text.** Render Bengali through a proper font with a shaping engine (a browser, Pango, HarfBuzz). Never draw it with a toy text API or paint it into a generated image, because conjuncts (যুক্তাক্ষর such as ক্ষ, জ্ঞ, ষ্ণ, ন্ত) and vowel signs (কার) will break.
2. **One Indic family per poster, two weights at most.** The AI sample mixed 3+ Bengali styles on a single banner (bevelled display, brush style, plain serif).
3. **No effects**: no outline stroke, shadow, bevel, gradient or glow. Heavy strokes fill the counters of conjuncts and make them unreadable at distance.
4. **No synthetic bold or italic.** Use a font that ships the weight. Indic scripts have no true italic; slanting looks wrong.
5. **No letter-spacing** (set it to 0). Tracking breaks the joins between letters and the matra line.
6. **No all-caps equivalent.** Create emphasis through size and weight only.
7. **Check the glyphs.** Missing glyphs show as empty boxes. Test the exact string before delivering.

## 2. Sizing and spacing

- Bengali glyphs look **smaller than Latin at the same font-size**. When setting the two next to each other, make the Bengali about **1.10-1.15x** the Latin size.
- **Line-height 1.35-1.6** for Bengali (matras above and descenders below need room). Display lines can go down to 1.15 only if they are one line.
- Give Bengali headlines **more space around them** than Latin ones; the visual mass is heavier.
- Minimum size: Bengali body text no smaller than **2.8% of canvas height**, because small Bengali degrades faster than Latin.

## 3. Pairing with Latin

| Situation | Bengali | Latin |
|---|---|---|
| Bold street poster | Anek Bangla ExtraBold or Baloo Da 2 ExtraBold | Bebas Neue / Oswald for display, Inter for details |
| Editorial / bookish | Tiro Bangla or Noto Serif Bengali | Fraunces or DM Serif Display |
| Clean information poster | Hind Siliguri Medium | Inter |

Match **weight and x-height** more than "style". If the Latin is condensed and tall, avoid a very wide Bengali display.

## 4. Bilingual layout

- **Pick a primary language** for the headline (usually the language of the street/audience). The second language is secondary and small.
- **Do not repeat the same sentence in both scripts.** Repeating it doubles the copy and halves the hierarchy. Use the second language for *different* information (e.g. English for address and phone, Bengali for the offer).
- A bilingual poster still has **one** headline.
- Keep each line in a single script where possible; avoid mid-line switches except for brand names, units and numbers.

## 5. Numerals, currency, phone numbers

- Choose **Bengali (০১২৩৪৫৬৭৮৯) or Western digits (0-9) once** per poster, by audience. Mixing both looks accidental.
- **Phone numbers in Western digits** are easier to dial from a distance. Group as 5 + 5 (`98XXX XXXXX`).
- Currency: `₹` before the figure (`₹120`). Do not add the word "ONLY"; do not add a strike-through old price unless the client supplied one.
- Dates: write the month name (`১৭ নভেম্বর`) to avoid day/month confusion.

## 6. Cultural and religious imagery

Festival and puja banners are an important part of local print culture. Be respectful and disciplined:

- **Do not synthesize deity faces** with an image generator. Results are often uncanny and can read as disrespectful. Use a real photograph of the actual idol or pandal, licensed traditional artwork, or a **type-led layout** with a simple flat motif.
- Respect colors and symbols the community treats as meaningful; do not mix deities, symbols or festivals decoratively.
- Names of people and committees: use exactly the spelling supplied. Never improvise names, titles or office-bearer lists.
- Put the **name of the puja, the date and the place** in the hierarchy first; ornament is last.

## 7. A restrained motif vocabulary for Bengal

If a motif is wanted, use **one**, **flat**, **in one color**, **large or as a single band**:

- **Alpona** (rice-paste floor patterns): lotus, conch, footprint motifs as outline or solid shapes.
- **Kantha** stitch lines: running stitch as a dotted/dashed rule, or a quilt-like grid.
- **Terracotta temple panels** (Bishnupur-style): relief-like repeating borders reduced to a flat tone.
- **Patachitra / Kalighat pat**: bold outlines and flat colors, simplified.
- **Hand-painted shop signs and tram-era lettering**: flat sign-painter letterforms, one color on one ground.
- **Shola/ daker saj** geometry: simple symmetrical cut-paper shapes.
- **Tiles and jali geometry**: a repeated pattern at low contrast as a background band.

Do not combine more than one motif family on one poster.

## 8. Proofreading

Machine-written Bengali often contains wrong conjunct spelling, missing hasanta, wrong vowel signs, or a stray Latin lookalike character. Before delivering:

1. Copy every Bengali string and read it aloud.
2. Check that each string appears **exactly as the client wrote it** if they supplied it.
3. If unsure of a word, **use a placeholder** such as `[নাম]` instead of guessing.
4. Confirm the render (no boxes, no broken conjuncts) by looking at the actual output image.
