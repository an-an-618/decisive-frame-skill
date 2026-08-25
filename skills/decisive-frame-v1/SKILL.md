---
name: decisive-frame-v1
description: Use when transforming a supplied photograph into a cinematic, poetic, selective-color 16:9 image with monochrome ink-wash surroundings, active negative space, and one approved source-derived color anchor.
---

# 决定性一帧 · Decisive Frame v1

## Overview

Direct a supplied photo into a truthful 16:9 film still where exactly one approved local element or color region retains source-derived color and the remaining world is reconstructed as sparse ink on a clean white field. Candidate selection precedes every generation.

## Required Resources

Read all three references completely before analyzing the photo:

- `references/decisive-selection.md`
- `references/cinematic-ink-language.md`
- `references/quality-gate.md`

**REQUIRED SUB-SKILL:** Use `imagegen` after the user selects a candidate. Treat the supplied photo as the edit target and preserve invariants aggressively.

## Non-Negotiable Contract

| Requirement | Contract |
|---|---|
| Mode | Choose Decisive Element or Decisive Color, never both |
| Candidate gate | Return 2–3 same-mode candidates and stop before generation |
| Element size | Target 5–30%; allow 30–45% only exceptionally; reject 50% or more |
| Color mode | Retain one narratively useful local region, not every matching hue |
| Frame | Deliver 16:9 without stretching, mirroring, or cloning source content |
| Ink world | Reconstruct on a clean white field; never use the source as a continuous grayscale photographic plate |
| Detail | Keep defining structure, merge secondary masses, omit low-value detail, and expose broad white space |
| Anchor support | When separation is needed, use exactly one local light-to-mid neutral support; keep it softer and quieter than the color anchor |
| Human anchor | Render the complete person as a coherent source-aware line-and-wash figure; preserve pose and proportions, but never regenerate a photorealistic face |
| Text | Add no text unless the user supplies an exact edge time |
| Output | Preview first; save only after explicit approval |

## Workflow

1. Inspect the source and build the Frame Card defined in `decisive-selection.md`.
2. Apply the mode gate. Choose exactly one mode before creating candidates.
3. Write 2–3 candidates with the required fields below. Keep every candidate in the chosen mode.
4. End the response with the non-blocking time line and stop. Do not call image generation in the candidate turn.
5. After the user selects a candidate, treat an omitted time as an instruction to use no text. Do not ask again.
6. Load the local source with the image viewer when necessary, then use built-in image generation in edit mode.
7. Classify the approved anchor as human or non-human. Human anchors use the scale-aware line-and-wash branch; non-human anchors keep material-faithful rendering.
8. Compile five compact visible-pixel prompt sections using `cinematic-ink-language.md`, including an explicit keep / merge / omit / expose map and the selected anchor-support strategy.
9. Generate one preview. Inspect it at normal and thumbnail scale using `quality-gate.md`.
10. When a local output path exists, run `scripts/analyze_selective_color.py`. Treat its report as evidence, not aesthetic judgment.
11. Apply at most one correction addressing only the observed failure. Recheck the result.
12. Show the preview with one brief Chinese rationale. Ask whether to save; do not save merely because generation succeeded.

## Candidate Output

Use this exact shape for each candidate:

```markdown
### 方案 A · [short name]
- Mode: [决定性元素 / 决定性色彩]
- Anchor: [specific element or local color region]
- Why: [why it is decisive]
- Color extent: [location and estimated final-frame share]
- 16:9 direction: [crop, placement, breathing room]
- Ink translation: [retained structure / merged washes / omitted detail / contiguous white field]
- Anchor support: [scene-derived frame / shaped ink cradle / white halo / none, with tone and edge behavior]
- Anchor rendering: [human line-and-wash with facial abstraction tier / non-human material-faithful rendering]
- Emotional proposition: [internal proposition; never image text]
```

Finish with:

```text
请选择方案 A、B 或 C。如需在边缘记录时间，请同时提供具体时间；未注明则不添加。
```

If only two credible proposals exist, provide two. Never fabricate a weak anchor to reach three.

## Prompt Shape After Selection

Compile only visible outcomes:

1. 16:9 canvas, attention geometry, and source invariants.
2. Approved unique color anchor, exact location, area, source-faithful color treatment, rendering branch, and one adaptive support strategy when separation is needed. For a person, state the scale-aware facial abstraction and line-and-wash recipe explicitly.
3. White-ground ink reconstruction with explicit retain / merge / omit / expose decisions and a restrained light-to-mid tonal hierarchy; say that it is not a desaturated photo.
4. Restrained film material and optional exact time.
5. Hard exclusions, especially all unapproved color and automatic text.

Repeat the approved anchor and source invariants in every correction prompt.

## Privacy and Delivery

- Use the supplied photo only for the requested task.
- Do not browse, share, upload, commit, or copy it into a project unless the user explicitly authorizes that action.
- Do not expose the full generation prompt unless requested.
- If the preview still fails after one targeted correction, show it as a preview with the concrete failure; do not call it a finished result.
