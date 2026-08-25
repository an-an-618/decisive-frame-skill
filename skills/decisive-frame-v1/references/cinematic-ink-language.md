# Cinematic Ink Language

## Contents

1. Source-Fidelity Lock
2. 16:9 Recomposition
3. White-Ground Ink Reconstruction
4. Unique Color Anchor
5. Human Anchor Line-and-Wash
6. Adaptive Anchor Support
7. Film Material
8. Optional Time
9. Prompt Compiler
10. Hard Avoids

## 1. Source-Fidelity Lock

Treat the supplied photograph as the edit target. Preserve the approved semantic minimum and name visible invariants explicitly: pose, face direction, object identity, horizon, perspective, relative position, path, architectural rhythm, and defining silhouette.

Do not replace the scene with a generic ink landscape. Truthfulness means preserving the semantic minimum and spatial invariants, not preserving every photographic detail. Simplification may remove most detail but may not change who is present, what they are doing, or how the core subjects occupy space.

## 2. 16:9 Recomposition

- For landscape sources, crop conservatively around the dominant gesture and quiet zone.
- For portrait or square sources, recompose rather than stretch. Use credible environmental continuation and scene-derived ink space.
- Never mirror, clone, or repeat people, buildings, trees, furniture, shoreline, or clouds to fill the frame.
- Apply element-area limits to the final 16:9 composition, not the source crop.
- Build negative space from real scene materials, then allow those materials to dissolve into a clean white field rather than inventing filler scenery.

The result is a full-bleed film still, not a photograph pasted onto a larger canvas.

## 3. White-Ground Ink Reconstruction

The unapproved world is not the original photograph with color removed. Rebuild it on a clean white base as a sparse contemporary ink image. The white is an active compositional mass, not a highlight trapped inside a full grayscale exposure.

Before prompting, assign every visible source region to exactly one operation:

1. **Retain:** keep only the defining structural strokes needed for identity, perspective, gesture, or eye path. Render them as concentrated black silhouettes, broken contours, or dry-brush anchors.
2. **Merge:** collapse secondary scenery into one to three broad wet-ink or mineral-grey masses. Do not preserve object-by-object photographic shading.
3. **Omit:** remove tertiary detail entirely: repeated leaves, road furniture, table reflections, utensils, tiny windows, signage, crowds, stones, textures, and clutter unless they carry the semantic minimum.
4. **Expose:** open at least one broad contiguous white field around or beyond the anchor. Prefer roughly 30–60% clean white or near-white ground when the source permits. Let edges feather, bloom, evaporate, or stop abruptly into white.

Use a restrained neutral hierarchy. Most of the reconstructed world should remain pale or mid-value; reserve true deep black for a tiny source-defining accent only when essential:

- **Deep black:** zero or one small structural accent; never a thick bar or mass that outranks the color anchor.
- **Mid wash:** compressed distance, atmosphere, secondary architecture, water, foliage, or ground.
- **Mist gray:** soft transition from the retained structure toward disappearance.
- **Clean white:** the dominant breathing field and visual silence.

The base must read as clean white, never yellow parchment, aged paper, torn fiber, or a grey photographic plate. Fine texture may live inside ink and the color anchor, but it must not dirty the white field.

At thumbnail scale, the source should remain recognizable through spatial rhythm and the decisive anchor even though many literal details have vanished. If the unapproved world still reads as a fully exposed black-and-white photograph, the transformation has failed.

## 4. Unique Color Anchor

- Retain only the approved element or local color region.
- Preserve the source hue family; allow moderate purification, deepening, and value correction.
- Preserve internal light, texture, volume, and material character.
- Desaturate every unapproved occurrence of the same hue.
- Add no second accent, colored rim, chromatic aberration, colored flare, or colored shadow.
- Allow a restrained neutral ink bleed or soft halation at the boundary so the anchor belongs to the white-ground ink world without becoming a sticker.

The color is successful only when it organizes entry, balance, direction, depth, or meaning.

## 5. Human Anchor Line-and-Wash

If the approved decisive element is a person, do not rebuild that person as a photorealistic cutout. Render the complete figure as one intentional source-aware gesture drawing with translucent source-color wash. This converts uncertain facial synthesis into a coherent visual decision while keeping the person's action and presence truthful.

Build the human anchor in this order:

1. **Gesture lock:** preserve the source silhouette, pose, head angle, shoulder and hip axis, limb count, joint positions, body proportions, clothing outline, hair mass, and distinctive accessories.
2. **Structural line:** use broken graphite, charcoal, dry-brush, or fine ink contours with visible searching lines. Concentrate marks at joints, garment folds, hair boundary, and the action-bearing edge; leave quiet gaps elsewhere.
3. **Scale-aware face:** use the facial abstraction tier from `decisive-selection.md`. Describe only brow direction, nose bridge, mouth interval, jaw, and hair boundary when the scale supports them. A small figure may use a blank face plane plus one or two directional marks.
4. **Source-color wash:** place restrained translucent source-derived color inside the sketched figure—skin, hair, clothing, shoes, and carried items—while allowing white paper and linework to remain visible. Keep it painterly and volumetric, never a flat fill.
5. **Edge integration:** let a few figure contours taper or bleed into the neutral support, but keep the action-bearing silhouette legible and keep all chroma inside the approved person.

The whole person must share one drawing language. Do not combine a photoreal face, hand, or patch of skin with a painterly body. Do not invent individual eyelashes, pupils, teeth, pores, finger detail, musculature, or beauty-retouched anatomy. Do not alter body type, height, shoulder width, leg length, or pose to make the figure more elegant.

If the approved anchor is not human, skip this branch and preserve the object's source material, internal light, texture, and volume as defined in Unique Color Anchor.

## 6. Adaptive Anchor Support

When the colored anchor loses separation against the pale ink world, give it exactly one local neutral support. The support is not a sticker, outline, or second subject; it is a quiet compositional pressure that makes the anchor arrive first.

Choose one family:

1. **Scene-derived frame:** bend, widen, or partially dissolve a nearby tray edge, rail, window line, shoreline, rock platform, shadow, or architectural contour into a cradle behind or side-behind the anchor.
2. **Shaped ink cradle:** place one irregular light-to-mid gray brush wash or wet-ink bloom behind or side-behind the anchor. Follow the anchor's silhouette, gesture, or direction rather than using a reusable splash shape.
3. **Negative-space halo:** clear a white breathing halo around the anchor and define only part of its outer boundary with a pale broken ink arc.

Support rules:

- Use it only when it improves thumbnail separation; otherwise state `none` in the candidate.
- Keep the support local, roughly 1.3–2 times the anchor's bounding area, never a half-frame backdrop.
- Use about 10–35% neutral black with transparency and visible paper-white breathing through it; never use pitch black.
- Place it behind or side-behind, preserving the anchor's face, silhouette, internal light, material, and colored detail.
- Feather, bloom, break, taper, or dissolve the edge. Avoid a hard rectangle, ring, contour sticker, or uniformly blurred halo.
- Keep it one visual level quieter than the anchor. If the support or a source-derived black structure becomes the first thumbnail read, lighten, thin, or omit it.

## 7. Film Material

Use a quiet film-still texture:

- fine irregular silver-halide grain;
- restrained highlight halation;
- deep blacks with non-digital tonal separation;
- slight vignette and exposure breathing;
- barely perceptible gate or scan instability;
- optional minimal hairline scratches only when the scene benefits.

Apply texture primarily inside ink masses and the color anchor. Keep the broad white field clean. Texture stays below subject recognition and ink hierarchy; nostalgia must never become the subject.

## 8. Optional Time

If and only if the user supplies a time string:

- reproduce it verbatim;
- place it at a lower edge or quiet corner safe area;
- use tiny neutral gray, silver white, or low-contrast mechanical lettering;
- add no date, place, sequence number, caption, title, poem, or inferred metadata.

If the user selects a candidate without a time, generate immediately and keep the image completely text-free. Do not ask again.

## 9. Prompt Compiler

Write five compact visible-pixel sections.

### 1. Canvas and invariants

State 16:9, full-bleed cinematic still, approved crop, source pose, spatial relationships, horizon, perspective, and what cannot change.

### 2. Unique color anchor and rendering branch

State the approved mode, exact anchor, final-frame location, estimated area, source hue, permitted purification, and the instruction that no other chromatic region may survive. For a person, state the figure-height tier, gesture lock, facial mark limit, coherent line medium, and translucent source-color wash. For a non-human anchor, state material-faithful rendering.

### 3. White-ground ink reconstruction and anchor support

Begin with the positive instruction: “Reconstruct every unapproved region on a clean white field; do not desaturate the photograph.” Then state the retain / merge / omit / expose map, the restrained pale-to-mid hierarchy, the contiguous white-field direction, and the exact details that must disappear. Add the chosen support family, scene-derived shape, position, area, value, edge behavior, and the requirement that it remain quieter than the anchor.

### 4. Film and time

State the restrained grain, halation, vignette, exposure behavior, and the exact optional time. Say “no text anywhere” when time is absent.

### 5. Exclusions

Forbid continuous photographic grayscale, full-scene tonal tracing, color leakage, global hue preservation, oversized colored subject, stretching, cloning, generic landscape replacement, yellow paper, torn paper, sprocket holes, heavy leaks, poster typography, captions, logos, watermarks, HDR, plastic skin, and excessive sharpening.

### Compact example

```text
Edit the supplied photograph into a full-bleed 16:9 cinematic still. Preserve the person's exact pose, facing direction, shoreline relationship, horizon, and camera perspective; recompose without stretching or cloning.

Approved mode: Decisive Element. Render the complete small person as one coherent broken-graphite and translucent watercolor figure. Preserve the exact pose, head angle, proportions, red coat silhouette, folds, and hair mass. Because the figure is below 20% frame height, reduce the face to three to six gestural marks and do not generate photoreal eyes, teeth, or skin. Keep only the person's source-derived skin, hair, coat, and clothing colors as thin wash, with the red coat moderately purified and deepened. No other chromatic pixels or colored effects anywhere.

Reconstruct every other region on a clean white field; do not desaturate or preserve the photographic tonal map. Retain only the shoreline gesture and one small broken foreground accent. Merge the sea into one diluted horizontal wash, omit leaf-by-leaf detail and scattered objects entirely, and expose a broad contiguous white field through the sky and around the figure. Let the ink edges bloom and dissolve into white. Bend one nearby shoreline stroke into a light-gray crescent cradle behind the coat, about 1.5 times its area, with wet feathered edges; keep it quieter than the red and do not cover the figure.

Use fine irregular silver-halide grain, restrained highlight halation, deep separated blacks, and a slight vignette. No text anywhere.

No yellow paper, torn paper, sprocket holes, film-strip border, orange light leak, chromatic aberration, copied scenery, commercial poster lighting, logo, caption, or watermark.
```

## 10. Hard Avoids

Avoid simple desaturation filters, continuous black-and-white photographic plates, full-scene tonal tracing, photoreal human cutouts, regenerated realistic faces, detailed miniature faces, realistic-face/painterly-body hybrids, invented facial features, beauty-filter anatomy, distorted limbs, extra fingers, cartoon or chibi people, flat color stickers, decorative isolated color, multiple accents, overlarge colored masses, pitch-black support blobs, hard backplates, contour halos, reusable generic splashes, thick black structures that outrank the anchor, dense botanical marks, uniform gray, dirty white fields, fake sumi scenery, copied objects, mirrored backgrounds, vintage paper, torn fibers, film-strip frames, heavy dust, dramatic light leaks, title cards, automatic poetry, fake metadata, illegible time, logos, and watermarks.
