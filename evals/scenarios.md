# Decisive Frame Behavior Scenarios

These scenarios are written before the skill implementation. They define the observable behavior the skill must teach.

| ID | Source class | Required behavior | Forbidden behavior |
|---|---|---|---|
| DF-01 | Small clear person or object | Choose Element Mode, offer 2–3 candidates, and keep the element below 50% of the final frame | Generate before selection or retain color across the whole scene |
| DF-02 | No clear element but one meaningful local hue | Choose Color Mode and isolate only one useful local region | Preserve every occurrence of the hue |
| DF-03 | Visually dominant object over half the final frame | Reject it as an element and choose another valid route | Keep an element occupying at least 50% |
| DF-04 | Portrait source | Recompose to 16:9 without stretching or cloning | Stretch, mirror, or duplicate scenery |
| DF-05 | Dense crowd, foliage, or interior | Merge detail into ink masses and prevent color leakage | Keep scattered colored pixels or dense tracing |
| DF-06 | Candidate selected without time | Generate immediately with no text | Ask again for time or invent metadata |
| DF-07 | Candidate selected with exact time | Render the supplied string exactly at a quiet edge | Rewrite, expand, or supplement the time |
| DF-08 | Selective-color output whose unapproved area still preserves continuous photographic grayscale | Reconstruct the unapproved world on a clean white field, keep only semantic structure, merge secondary masses into ink washes, and omit tertiary detail | Treat the source as a desaturated photographic plate or preserve full-scene grayscale texture |
| DF-09 | A small valid color anchor needs separation from a pale ink world | Use exactly one adaptive neutral support derived from nearby scene geometry or a shaped ink wash; keep it local, light-to-mid gray, softly dissolved, and quieter than the anchor | Omit support when the anchor disappears, add a pitch-black blob or hard sticker panel, obscure the anchor, or create a second focal subject |
| DF-10 | A person is selected as the decisive element, especially at small or medium scale | Render the complete person as one coherent source-aware gesture-line and translucent color-wash figure; preserve pose, proportions, limb geometry, clothing silhouette, hair mass, and source colors while simplifying the face according to final scale | Attempt a newly photorealistic face or body, mix a realistic face with a painted body, invent facial detail, distort anatomy, or turn the person into a cartoon or flat sticker |

## Candidate Contract

Every candidate must contain:

- Mode
- Anchor
- Why
- Color extent
- 16:9 direction
- Ink translation
- Anchor support
- Anchor rendering
- Emotional proposition

All candidates for one photo must use the same mode and differ meaningfully in at least two fields.
