# Baseline Observations

Recorded before `decisive-frame-v1` exists.

- No `decisive-frame-v1` skill exists locally or globally.
- Existing Gathered Scenes trials exposed three relevant failure classes: dense foliage, over-photocopied photographic anchors, and literal or scattered color tracing.
- A generic image-editing request has no reusable gate that forces 2–3 same-mode candidates before generation.
- A generic selective-color prompt has no deterministic check for 16:9 output, excessive chroma, or disconnected color leakage.
- Fresh independent subagent pressure tests were not run because active environment policy forbids delegation.
- Behavioral forward tests will therefore use live candidate cards, real image edits, visual inspection, and deterministic output analysis in the current task.

## RED Condition

The baseline fails because neither `skills/decisive-frame-v1` nor the user's global Codex skills directory contains `decisive-frame-v1`, so the approved workflow is not deployable.

## 2026-08-24 White-Ground Regression

- A live DFT-01 preview preserved only the selected iced drink and passed the existing 16:9 and chroma checks.
- The same preview retained continuous photographic grayscale across the table, tray, sea, and window, so it read as a desaturated photograph rather than an ink reconstruction.
- The user rejected this behavior and specified a clean white base, broad negative space, ink diffusion, and permission to discard unimportant detail.
- Deterministic evidence for the rejected preview: `chromatic_fraction=0.007969`, `component_count=2`, no warnings, but only `0.043437` strict-white pixels and `0.247483` near-white pixels.
- DF-08 therefore fails under the current skill and analyzer: the visual contract mentions omission, but does not make white-ground reconstruction structural or detect insufficient contiguous white field.

## 2026-08-25 Anchor-Support Regression

- The corrected DFT-01 preview passed the white-field and chroma analyzer, but its thick black window mullion became the strongest thumbnail subject and the tray retained more descriptive detail than the decisive drink needed.
- The colored drink had no shaped local support, so it appeared placed on top of the ink world rather than visually held by it.
- The user requested a lighter overall ink hierarchy plus one softly dissolved ink-drop, brush, wash, or scene-derived frame deformation behind the anchor.
- DF-09 therefore fails under the previous contract: it permits a soft boundary bleed but does not require an adaptive support strategy or prevent a dark structural stroke from outranking the color anchor.

## 2026-08-25 Human-Anchor Regression

- Live cyclist, runner, and seaside-person previews followed the existing identity-preservation wording and kept each person as the only color anchor.
- Repeated image edits nevertheless regenerated photorealistic facial and body detail, producing visible changes to faces, proportions, and anatomy compared with the supplied photographs.
- The user preferred deliberate abstraction over uncanny false fidelity: a human anchor should become an intentional sketch-like line-and-wash figure rather than a damaged photographic cutout.
- DF-10 therefore fails under the previous contract: it asks image generation to preserve a face and body photorealistically but offers no scale-aware human rendering branch that converts unavoidable identity uncertainty into a coherent drawing language.
