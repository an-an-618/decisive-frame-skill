# Quality Gate

## Contents

1. Preflight
2. Normal-Scale Inspection
3. Thumbnail Inspection
4. Deterministic Analyzer
5. Targeted Correction
6. Stop and Delivery Rules

## 1. Preflight

Before generation, verify:

- the user selected one offered candidate;
- all candidates and the selected candidate use one mode;
- Element Mode remains below 50% in the intended 16:9 frame;
- Color Mode retains one local occurrence rather than a global hue;
- source invariants and discard decisions are explicit;
- retain / merge / omit / expose decisions are explicit, including one broad contiguous white field;
- the candidate states one adaptive anchor-support strategy or explicitly states none;
- any support is local, scene-responsive, light-to-mid neutral, soft-edged, and behind or side-behind the anchor;
- the anchor is classified as human or non-human; a human candidate states figure-height tier, line medium, facial mark limit, and source-color wash;
- absent time means “no text anywhere” and does not trigger another question;
- no automatic poem, title, place, date, sequence, or pseudo-metadata entered the prompt.

If any item fails, fix the prompt before generation.

## 2. Normal-Scale Inspection

Inspect the rendered preview for:

- source identity, pose, facial direction, object identity, perspective, and horizon;
- credible 16:9 recomposition without stretching, mirroring, or cloned fillers;
- approved anchor contour, internal light, texture, volume, and source hue;
- for a human anchor, source pose, head angle, limb count, joint positions, body proportions, clothing silhouette, hair mass, and distinctive accessories remain stable;
- the complete human figure uses one coherent line-and-wash language with scale-appropriate facial abstraction and no photoreal skin patches;
- human source colors remain as translucent wash inside the figure instead of flat fill or color leakage;
- a visibly clean white base with deep black, broad wash, mist gray, and empty-space hierarchy;
- purposeful omission: low-value detail is truly absent rather than preserved in gray;
- broken, dissolved, or washed ink edges instead of continuous photographic tonal modeling;
- credible ink-to-color boundary without a sticker rim;
- any support preserves the anchor's silhouette and internal detail, has a softly broken transition, and remains quieter than the anchor;
- no thick black structural stroke or dark wash becomes a competing subject;
- exact optional time, or complete absence of text;
- restrained film texture below content hierarchy.

## 3. Thumbnail Inspection

At thumbnail scale, verify:

- one clear color entry and no competing colored flecks;
- the color anchor reads first, its support second, and every neutral structure later;
- a human anchor reads as an intentional drawing rather than a failed photographic likeness, generic cartoon, or mannequin;
- the decisive element does not dominate half the image;
- one broad contiguous white field reads as one of the composition's largest masses;
- the eye path enters, meets the anchor, and exits through a quiet zone;
- grain, vignette, scratches, and halation do not become a second subject;
- the frame reads as a white-ground ink film still rather than a black-and-white photograph, paper poster, or filter preset.

## 4. Deterministic Analyzer

When the preview has a local path and Pillow is available, run:

```bash
python3 <skill-directory>/scripts/analyze_selective_color.py <preview-path>
```

Use the report as supporting evidence:

- `is_16_9` must be true;
- `chromatic_fraction` above `0.25` is a strong leakage or oversized-anchor warning;
- `component_count` above `3` suggests scattered color leakage;
- `chromatic_bbox` helps compare the colored extent with the approved anchor;
- `no_decisive_chroma` suggests the anchor disappeared or became too muted.
- `white_field_fraction` estimates all clean neutral white pixels;
- `largest_white_field_fraction` estimates whether one contiguous white field reaches the target;
- `insufficient_white_field` means the largest clean field is below 30% and requires visual review or correction.

The analyzer detects saturation, not semantic correctness. A passing report cannot prove that the right object retained color. A warning may be acceptable only when visual inspection explains it and all non-negotiable constraints still pass.

The script is read-only. If the local path or Pillow is unavailable, do not install dependencies silently. Complete visual inspection and record that deterministic analysis was skipped.

## 5. Targeted Correction

Regenerate at most once. Repeat every source invariant and approved-anchor constraint, then change only the observed failure:

| Failure | One correction |
|---|---|
| Color leakage | Convert every named leak outside the approved anchor to neutral ink |
| Element at least 50% | Reduce its final-frame scale and enlarge directional breathing room |
| Global hue retention | Keep only the approved local occurrence; neutralize matching hues elsewhere |
| Black-and-white photographic plate | Reconstruct from the source on clean white; retain named structure, merge secondary scenery into one to three washes, omit tertiary detail, and expose one broad white field |
| Generic ink landscape | Restore source-specific geometry, perspective, and spatial invariants |
| Sticker-like anchor | Restore internal light, material, and a restrained neutral transition |
| Anchor lacks separation | Add one light-to-mid scene-derived frame, shaped ink cradle, or partial white halo behind it |
| Support is too dark, hard, or obscuring | Lower it to a translucent light-to-mid gray, reduce its area, and feather or break the edge |
| Support looks like a generic splash | Rebuild its shape from adjacent source geometry or the anchor's gesture |
| Heavy black structure competes with anchor | Thin, lighten, break, or omit the structure until the colored anchor reads first |
| Dense foliage/crowd/food | Remove repeated marks and compress them into one or two broad masses |
| Excessive film texture | Reduce grain, vignette, scratches, and halation |
| Wrong or invented text | Restore the exact supplied time or remove all text |
| Source drift | Restore the missing pose, object identity, horizon, or relationship |
| Photoreal human face or body drifts | Convert the complete person—not only the face—to the approved line-and-wash recipe while restoring source gesture and proportions |
| Small face contains invented detail | Reduce it to the permitted number of directional marks or a blank face plane |
| Realistic face sits on a painted body | Unify face, hands, skin, clothing, and body under one drawing language |
| Human becomes generic or anatomically wrong | Restore source silhouette, head angle, shoulder–hip axis, limb count, joints, proportions, clothing outline, hair mass, and carried items |
| Human sketch loses decisive color | Add back restrained translucent source-color wash inside the figure only |

## 6. Stop and Delivery Rules

- Do not make a second automatic correction.
- If the corrected preview still fails, show it as a preview and name the failure plainly.
- Return one brief Chinese rationale describing the selected anchor, ink hierarchy, and eye path.
- Do not reveal the full prompt unless requested.
- Ask whether to save. Save only after explicit approval.
- Public example permission is separate from local-save approval and must be obtained per case.
