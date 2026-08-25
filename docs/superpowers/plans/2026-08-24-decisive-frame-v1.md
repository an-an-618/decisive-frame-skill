# Decisive Frame v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, validate, preview-test, and prepare for publication a Codex skill that turns supplied photos into 16:9 monochrome ink-film frames with exactly one user-approved source-derived color anchor.

**Architecture:** Keep the installable skill concise and route detailed selection, visual-language, and quality rules into three one-level reference files. Add one deterministic Pillow-based analyzer that reports aspect ratio, high-chroma coverage, bounding box, and disconnected color regions without modifying pixels. Use a mandatory candidate-selection gate before image generation, then validate each preview visually and with the analyzer when a local output path is available.

**Tech Stack:** Markdown Agent Skill, Python 3.12 bundled Codex runtime, Pillow 12.3.0, `unittest`, built-in `image_gen`, Git, GitHub CLI.

**Spec:** `docs/specs/2026-08-24-decisive-frame-design.md`

## Global Constraints

- Skill name is exactly `decisive-frame-v1`; repository name is exactly `decisive-frame-skill`.
- Output is 16:9; do not stretch portrait or square sources.
- Decisive Element Mode and Decisive Color Mode are mutually exclusive per photo.
- Prefer Decisive Element Mode only when a valid element remains below 50% of the final frame; target 5–30%, allow 30–45% only as an exception.
- Use Decisive Color Mode only when no valid element exists; retain only the narratively useful local region, target 2–18% of the frame, and desaturate all other similar hues.
- Present 2–3 same-mode candidates and wait for the user's selection before any image generation.
- Ask for optional edge time in the same selection message; absence of a time is non-blocking and produces a text-free image.
- Add no automatic poem, title, location, number, sprocket holes, torn paper, yellow paper, or heavy vintage decoration.
- Preserve source identity, key pose, perspective, horizon, and spatial relationships.
- Preview before saving; save only after explicit user approval.
- Use earlier user photos for local testing; publish only examples individually approved by the user.
- License skill materials under PolyForm Noncommercial; example-photo permissions remain separate.
- Active environment policy forbids subagent delegation. Record that independent fresh-agent pressure testing was unavailable; do not claim it occurred.

---

### Task 1: Establish RED Evaluation Artifacts

**Files:**
- Create: `evals/scenarios.md`
- Create: `evals/baseline-observations.md`
- Create locally (gitignored): `evals/test-images.local.md`

**Interfaces:**
- Consumes: the approved design spec and a private, gitignored inventory of user-authorized local test photos.
- Produces: scenario IDs `DF-01` through `DF-07`, explicit expected behavior, and baseline evidence that the new skill is absent and the desired interaction is not yet deployable.

- [ ] **Step 1: Write the behavior scenarios before the skill exists**

Define these exact scenarios in `evals/scenarios.md`:

```markdown
| ID | Source class | Required behavior | Forbidden behavior |
|---|---|---|---|
| DF-01 | Small clear person/object | Choose Element Mode; offer 2–3 candidates; keep element under 50% | Generate before selection; color the whole scene |
| DF-02 | No clear element, one local meaningful hue | Choose Color Mode; isolate only one useful region | Preserve every occurrence of the hue |
| DF-03 | Visually dominant object over half the frame | Reject it as an element and choose another valid route | Keep an element occupying at least 50% |
| DF-04 | Portrait source | Recompose to 16:9 without stretching or cloning | Stretch, mirror, or duplicate scenery |
| DF-05 | Dense crowd/foliage/interior | Merge detail into ink masses and prevent color leakage | Keep scattered colored pixels or dense tracing |
| DF-06 | Candidate selected without time | Generate immediately with no text | Ask again for time or invent metadata |
| DF-07 | Candidate selected with exact time | Render the exact supplied string at a quiet edge | Rewrite, expand, or supplement the time |
```

- [ ] **Step 2: Verify the baseline fails for the intended reason**

Run:

```bash
test ! -d skills/decisive-frame-v1
test ! -d "${CODEX_HOME:-$HOME/.codex}/skills/decisive-frame-v1"
```

Expected: both commands exit `0`, proving no local or installed skill can yet satisfy the scenario contract.

- [ ] **Step 3: Record the baseline limitations honestly**

In `evals/baseline-observations.md`, record:

```markdown
- No `decisive-frame-v1` skill exists locally or globally.
- Existing Gathered Scenes trials showed three relevant failure classes: dense foliage, over-photocopied photographic anchors, and literal/scattered color tracing.
- Fresh independent subagent pressure tests were not run because active environment policy forbids delegation.
- Behavioral forward tests will therefore use live candidate cards, real image edits, visual inspection, and deterministic output analysis in the current task.
```

- [ ] **Step 4: Record the nine authorized test inputs without copying them**

Create the gitignored `evals/test-images.local.md` with an ID, absolute local path, orientation, and scene label for each photo. Never publish this inventory or copy unapproved images into the repository.

- [ ] **Step 5: Commit the RED artifacts after repository initialization in Task 5**

Stage these files in the first repository commit together with the design and implementation plan.

---

### Task 2: Build the Selective-Color Analyzer with TDD

**Files:**
- Create: `tests/test_analyze_selective_color.py`
- Create from official scaffold: `skills/decisive-frame-v1/SKILL.md`
- Create from official scaffold: `skills/decisive-frame-v1/agents/openai.yaml`
- Create: `skills/decisive-frame-v1/scripts/analyze_selective_color.py`

**Interfaces:**
- Consumes: `analyze_image(path: Path, saturation_threshold: int = 64, max_edge: int = 640) -> dict[str, object]`.
- Produces: a JSON-serializable report with `width`, `height`, `aspect_ratio`, `is_16_9`, `chromatic_fraction`, `component_count`, `largest_component_fraction`, `chromatic_bbox`, and `warnings`; CLI prints this report as JSON and never changes the source file.

- [ ] **Step 1: Write failing unit tests using generated fixtures**

Use `unittest`, `tempfile`, and Pillow. The tests must create their own images and assert literal expected behavior:

```python
def test_reports_single_small_chromatic_region(self):
    image = Image.new("RGB", (160, 90), "#777777")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 18, 31, 35), fill="#d02020")
    path = self.write_image(image, "single.png")

    report = analyze_image(path)

    self.assertTrue(report["is_16_9"])
    self.assertEqual(report["component_count"], 1)
    self.assertAlmostEqual(report["chromatic_fraction"], 288 / 14400, places=3)
    self.assertEqual(report["chromatic_bbox"], [16, 18, 31, 35])

def test_warns_for_scattered_color_regions(self):
    image = Image.new("RGB", (160, 90), "#777777")
    draw = ImageDraw.Draw(image)
    for x in (8, 48, 88, 128):
        draw.rectangle((x, 20, x + 7, 27), fill="#0055ff")
    path = self.write_image(image, "scattered.png")

    report = analyze_image(path)

    self.assertEqual(report["component_count"], 4)
    self.assertIn("scattered_chroma", report["warnings"])
```

Also cover incorrect aspect ratio, more than 25% high-chroma coverage, and neutral gray/black/white pixels not counted as chromatic.

- [ ] **Step 2: Run tests and watch them fail because the module is absent**

Run:

```bash
python3 -m unittest tests/test_analyze_selective_color.py -v
```

Expected: `ModuleNotFoundError` for `analyze_selective_color`.

- [ ] **Step 3: Initialize the official skill scaffold after RED**

Run:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/init_skill.py" \
  decisive-frame-v1 \
  --path skills \
  --resources scripts,references \
  --interface 'display_name=决定性一帧 · Decisive Frame' \
  --interface 'short_description=将照片导演为唯一局部留色的16:9水墨电影静帧' \
  --interface 'default_prompt=Use $decisive-frame-v1 to analyze this photo and offer 2–3 director candidates before generating a selective-color cinematic ink frame.'
```

Expected: the official initializer creates the skill folder, `SKILL.md`, `agents/openai.yaml`, `scripts/`, and `references/` without creating example placeholders.

- [ ] **Step 4: Implement the minimal analyzer**

Implement the following behavior:

```python
def analyze_image(path, saturation_threshold=64, max_edge=640):
    original = Image.open(path).convert("RGB")
    width, height = original.size
    analysis = original.copy()
    analysis.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
    hsv = analysis.convert("HSV")
    mask = build_chroma_mask(hsv, saturation_threshold)
    components = connected_components(mask, analysis.width, analysis.height)
    return build_report(
        original_size=(width, height),
        analysis_size=analysis.size,
        mask=mask,
        components=components,
    )
```

Use 4-neighbor connectivity. Scale component bounding boxes back to original coordinates. Warn on `not_16_9`, `excessive_chroma` above `0.25`, `scattered_chroma` above three meaningful components, and `no_decisive_chroma` below `0.002`.

- [ ] **Step 5: Run tests and watch them pass**

Run the same `unittest` command. Expected: all analyzer tests pass with no warnings or errors from the test runner.

- [ ] **Step 6: Add and test the CLI boundary**

Add a test that invokes:

```bash
python skills/decisive-frame-v1/scripts/analyze_selective_color.py fixture.png
```

Assert exit code `0`, valid JSON, and that the fixture file hash is unchanged before and after execution.

- [ ] **Step 7: Refactor while keeping tests green**

Separate image loading, mask creation, connected-component analysis, report construction, and CLI parsing into focused functions. Re-run the full analyzer test module.

---

### Task 3: Scaffold and Author the Skill

**Files:**
- Modify: `skills/decisive-frame-v1/SKILL.md`
- Verify: `skills/decisive-frame-v1/agents/openai.yaml`
- Create: `skills/decisive-frame-v1/references/decisive-selection.md`
- Create: `skills/decisive-frame-v1/references/cinematic-ink-language.md`
- Create: `skills/decisive-frame-v1/references/quality-gate.md`

**Interfaces:**
- Consumes: scenario contract `DF-01`–`DF-07`, analyzer CLI, and the approved design spec.
- Produces: a discoverable skill whose candidate response has fields `Mode`, `Anchor`, `Why`, `Color extent`, `16:9 direction`, `Ink translation`, and `Emotional proposition`.

- [ ] **Step 1: Write the three focused references**

`decisive-selection.md` contains the mode gate, element eligibility, area limits, local-color rule, and candidate schema.

`cinematic-ink-language.md` contains 16:9 recomposition, source invariants, four-level ink hierarchy, unique color anchor, film material, and optional exact time.

`quality-gate.md` contains preflight checks, normal/thumbnail inspection, analyzer invocation, targeted corrections, stop conditions, and preview/save contract.

- [ ] **Step 2: Write the minimal SKILL.md around the observed failures**

Use exactly this metadata shape:

```yaml
---
name: decisive-frame-v1
description: Use when transforming a supplied photograph into a cinematic, poetic, selective-color 16:9 image with monochrome ink-wash surroundings, active negative space, and one approved source-derived color anchor.
---
```

The body must:

- require reading all three references before analysis;
- classify the source into exactly one mode;
- return 2–3 same-mode candidates and stop before generation;
- merge the optional-time prompt into candidate selection;
- use the supplied photo as an edit target after selection;
- compile five compact visible-pixel prompt sections;
- inspect normal and thumbnail scale;
- run the analyzer when a local output path exists;
- apply at most one targeted correction;
- preview first and save only after explicit approval.

- [ ] **Step 3: Validate metadata and reference paths**

Run:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/decisive-frame-v1
```

Expected: validation succeeds. Then open every linked reference path from `SKILL.md` and confirm it resolves one level deep.

- [ ] **Step 4: Run a manual scenario-contract review**

For each `DF-01`–`DF-07`, record in `evals/expected-behavior.md` the exact skill section that governs the expected behavior. Do not claim independent agent verification.

---

### Task 4: Add Repository Documentation and License

**Files:**
- Create: `README.md`
- Create: `README.zh-CN.md`
- Create: `LICENSE`
- Create: `examples/README.md`
- Create: `.gitignore`

**Interfaces:**
- Consumes: the public product definition and privacy decisions.
- Produces: install, usage, example-approval, attribution, and license guidance without duplicating the operational Skill instructions.

- [ ] **Step 1: Add the official PolyForm Noncommercial license text**

Use the standard current PolyForm Noncommercial license text from the official PolyForm project. Set the licensor/copyright notice to `an-an-618` and document the selected license version in README.

- [ ] **Step 2: Write bilingual repository READMEs**

Both READMEs must explain:

- `photo → choose mode → offer candidates → user selects → generate preview → approve save`;
- the difference between Decisive Element and Decisive Color modes;
- installation by copying `skills/decisive-frame-v1` into the Codex skills directory;
- the optional exact-time syntax;
- no automatic text and no public upload of user photos;
- example media permissions are separate from the code/document license.

- [ ] **Step 3: Create the example archive contract**

`examples/README.md` must require `source`, `candidate-card`, `result`, `observation-record`, and explicit publication approval for every public case. Leave the archive empty until the user approves individual cases.

- [ ] **Step 4: Add repository ignores**

Ignore generated previews, local test photos, Python caches, macOS metadata, and temporary reports:

```gitignore
.DS_Store
__pycache__/
*.pyc
output/
tmp/
evals/local/
```

---

### Task 5: Initialize Git and Verify the Package

**Files:**
- Modify: no content files unless verification finds a concrete defect.

**Interfaces:**
- Consumes: complete repository files from Tasks 1–4.
- Produces: a clean local Git history and verified installable skill package.

- [ ] **Step 1: Initialize the repository**

Run:

```bash
git init
git branch -M main
```

- [ ] **Step 2: Run all deterministic tests**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/decisive-frame-v1
python3 skills/decisive-frame-v1/scripts/analyze_selective_color.py \
  /path/to/local-test-image.png
```

Expected: tests pass, skill validation succeeds, analyzer prints valid JSON, and the unedited source predictably warns that the input is not yet a selective-color 16:9 output.

- [ ] **Step 3: Review tracked files for private images**

Run:

```bash
git status --short
git ls-files
```

Expected: no source photo or generated preview is tracked.

- [ ] **Step 4: Create the initial local commit**

Run:

```bash
git add .
git commit -m "feat: create decisive frame skill"
```

Do not create or push the GitHub repository yet.

---

### Task 6: Produce Candidate Cards for the Nine Authorized Photos

**Files:**
- Create: `evals/local/2026-08-24-candidate-cards.md` (ignored by Git)

**Interfaces:**
- Consumes: nine user-authorized local photos and the completed skill instructions.
- Produces: 2–3 same-mode candidate cards per image and one recommendation per image; no raster generation.

- [ ] **Step 1: Inspect every source image**

Use the built-in image viewer for each local path. Record the semantic minimum, source orientation, possible element eligibility, local color candidates, and 16:9 risks.

- [ ] **Step 2: Apply the mode gate**

For each photo, choose Element Mode if and only if at least one valid element remains below 50% in the final frame. Otherwise choose Color Mode.

- [ ] **Step 3: Write 2–3 candidate cards per image**

Use this exact shape:

```markdown
### Candidate N
- Mode:
- Anchor:
- Why:
- Color extent:
- 16:9 direction:
- Ink translation:
- Emotional proposition:
```

- [ ] **Step 4: Present the candidate set to the user**

Include a recommended candidate for every image and this non-blocking line:

```text
请按“1A、2B、3A……”选择；如需边缘时间，请在对应编号后写具体时间。未写时间的图片将无字生成。
```

Stop before image generation and wait for the user's selections.

---

### Task 7: Generate and Validate Preview Images After Selection

**Files:**
- Create only after user approval to save: `output/previews/<image-id>-decisive-frame.png`
- Create: `evals/local/2026-08-24-preview-results.md` (ignored by Git)

**Interfaces:**
- Consumes: user-selected candidate IDs and optional exact time strings.
- Produces: one built-in `image_gen` edit per selected photo, visual QA, analyzer report when a local path is available, and inline previews.

- [ ] **Step 1: Load each selected local image into the conversation**

Use `view_image` before editing so every filesystem image is available to built-in image generation.

- [ ] **Step 2: Compile one edit prompt per selected image**

Label the source as `edit target`, repeat invariants, specify the approved anchor, forbid all unapproved color, require 16:9, and include exact time only when supplied.

- [ ] **Step 3: Generate one preview per selected image**

Use built-in `image_gen`. Issue a separate call for each photo; do not use CLI fallback or batch substitution.

- [ ] **Step 4: Inspect and analyze every preview**

Inspect at normal and thumbnail scale. When a local path exists, run:

```bash
python3 skills/decisive-frame-v1/scripts/analyze_selective_color.py <preview-path>
```

Record ratio, chromatic fraction, component count, visual anchor size, source fidelity, ink hierarchy, text status, and observed failures.

- [ ] **Step 5: Apply at most one targeted correction per failing preview**

Repeat all invariants and change only the observed failure. Reinspect and rerun the analyzer.

- [ ] **Step 6: Render previews inline without saving to the repository**

Ask the user which previews are approved for local saving and which, if any, may later become public examples.

---

### Task 8: Refine and Revalidate the Skill from Real Preview Failures

**Files:**
- Modify only if evidence requires: `skills/decisive-frame-v1/SKILL.md`
- Modify only if evidence requires: `skills/decisive-frame-v1/references/*.md`
- Modify only if evidence requires: `skills/decisive-frame-v1/scripts/analyze_selective_color.py`
- Modify tests first when analyzer behavior changes: `tests/test_analyze_selective_color.py`

**Interfaces:**
- Consumes: concrete preview failure records.
- Produces: the smallest guidance or code change that prevents recurrence.

- [ ] **Step 1: Classify each failure**

Map failures to candidate gate, prompt shape, source invariant, ink hierarchy, color leakage, texture excess, time rendering, or analyzer false positive/negative.

- [ ] **Step 2: For analyzer defects, write a failing regression test first**

Run the isolated test and confirm the expected RED failure before editing production code.

- [ ] **Step 3: Apply the minimal correction**

Use positive output contracts for wrong-shaped behavior and hard prohibitions only for skipped non-negotiable gates.

- [ ] **Step 4: Re-run all tests and skill validation**

Run the commands from Task 5 Step 2. Expected: all pass cleanly.

- [ ] **Step 5: Commit verified refinements**

Run:

```bash
git add skills tests evals README.md README.zh-CN.md
git commit -m "test: refine decisive frame from preview trials"
```

Skip the commit if no tracked file changed.

---

### Task 9: Prepare Approved Public Examples and Publish

**Files:**
- Create only for individually approved cases: `examples/<case-slug>/source.<ext>`
- Create only for individually approved cases: `examples/<case-slug>/candidate-card.md`
- Create only for individually approved cases: `examples/<case-slug>/result.png`
- Create only for individually approved cases: `examples/<case-slug>/README.md`

**Interfaces:**
- Consumes: explicit per-case publication approval and verified local repository.
- Produces: public GitHub repository `an-an-618/decisive-frame-skill`.

- [ ] **Step 1: Confirm the exact approved public cases**

List every proposed source/result pair and obtain explicit user approval. Do not infer approval from local testing permission.

- [ ] **Step 2: Add only approved example media**

Each case README records mode, candidates, selected anchor, color extent, crop direction, ink translation, quality results, and publication approval date.

- [ ] **Step 3: Verify GitHub authentication and repository ownership**

Run:

```bash
gh auth status
gh api user --jq .login
```

Expected login: `an-an-618`. If it differs, stop before any remote mutation.

- [ ] **Step 4: Create and push the public repository**

After the identity check and final user approval, run:

```bash
gh repo create an-an-618/decisive-frame-skill --public --source=. --remote=origin --push
```

- [ ] **Step 5: Verify the remote repository**

Run:

```bash
git status --short
git remote -v
gh repo view an-an-618/decisive-frame-skill --json nameWithOwner,url,visibility
```

Expected: clean worktree, correct remote, `nameWithOwner` equals `an-an-618/decisive-frame-skill`, and visibility is `PUBLIC`.
