from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import warnings

from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    PROJECT_ROOT
    / "skills"
    / "decisive-frame-v1"
    / "scripts"
    / "analyze_selective_color.py"
)

if not SCRIPT_PATH.exists():
    raise ModuleNotFoundError(f"Production analyzer does not exist: {SCRIPT_PATH}")

SPEC = importlib.util.spec_from_file_location("analyze_selective_color", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load analyzer module: {SCRIPT_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
analyze_image = MODULE.analyze_image


class AnalyzeSelectiveColorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.temp_path = Path(self.tempdir.name)

    def write_image(self, image: Image.Image, name: str) -> Path:
        path = self.temp_path / name
        image.save(path)
        return path

    def test_reports_single_small_chromatic_region(self) -> None:
        image = Image.new("RGB", (160, 90), "#777777")
        draw = ImageDraw.Draw(image)
        draw.rectangle((16, 18, 31, 35), fill="#d02020")
        path = self.write_image(image, "single.png")

        report = analyze_image(path)

        self.assertTrue(report["is_16_9"])
        self.assertEqual(report["component_count"], 1)
        self.assertAlmostEqual(report["chromatic_fraction"], 288 / 14400, places=3)
        self.assertAlmostEqual(
            report["largest_component_fraction"], 288 / 14400, places=3
        )
        self.assertEqual(report["chromatic_bbox"], [16, 18, 31, 35])
        self.assertEqual(report["white_field_fraction"], 0.0)
        self.assertEqual(report["largest_white_field_fraction"], 0.0)
        self.assertIn("insufficient_white_field", report["warnings"])

    def test_accepts_one_large_contiguous_white_field(self) -> None:
        image = Image.new("RGB", (160, 90), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 39, 89), fill="#111111")
        draw.rectangle((64, 36, 79, 53), fill="#d02020")
        path = self.write_image(image, "white-field.png")

        report = analyze_image(path)

        self.assertGreater(report["white_field_fraction"], 0.70)
        self.assertGreater(report["largest_white_field_fraction"], 0.70)
        self.assertNotIn("insufficient_white_field", report["warnings"])

    def test_rejects_dense_grayscale_as_an_ink_white_field(self) -> None:
        image = Image.new("RGB", (160, 90), "#777777")
        draw = ImageDraw.Draw(image)
        draw.rectangle((64, 36, 79, 53), fill="#d02020")
        path = self.write_image(image, "dense-grayscale.png")

        report = analyze_image(path)

        self.assertEqual(report["white_field_fraction"], 0.0)
        self.assertEqual(report["largest_white_field_fraction"], 0.0)
        self.assertIn("insufficient_white_field", report["warnings"])

    def test_warns_for_scattered_color_regions(self) -> None:
        image = Image.new("RGB", (160, 90), "#777777")
        draw = ImageDraw.Draw(image)
        for x in (8, 48, 88, 128):
            draw.rectangle((x, 20, x + 7, 27), fill="#0055ff")
        path = self.write_image(image, "scattered.png")

        report = analyze_image(path)

        self.assertEqual(report["component_count"], 4)
        self.assertIn("scattered_chroma", report["warnings"])

    def test_warns_when_ratio_is_not_16_9(self) -> None:
        image = Image.new("RGB", (100, 100), "#777777")
        path = self.write_image(image, "square.png")

        report = analyze_image(path)

        self.assertFalse(report["is_16_9"])
        self.assertIn("not_16_9", report["warnings"])

    def test_warns_when_chromatic_area_exceeds_one_quarter(self) -> None:
        image = Image.new("RGB", (160, 90), "#e02020")
        path = self.write_image(image, "excessive.png")

        report = analyze_image(path)

        self.assertEqual(report["chromatic_fraction"], 1.0)
        self.assertIn("excessive_chroma", report["warnings"])

    def test_neutral_ink_values_are_not_counted_as_chromatic(self) -> None:
        image = Image.new("RGB", (160, 90), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 52, 89), fill="#111111")
        draw.rectangle((53, 0, 105, 89), fill="#777777")
        path = self.write_image(image, "neutral.png")

        report = analyze_image(path)

        self.assertEqual(report["chromatic_fraction"], 0.0)
        self.assertEqual(report["component_count"], 0)
        self.assertEqual(report["chromatic_bbox"], None)
        self.assertIn("no_decisive_chroma", report["warnings"])

    def test_cli_prints_json_without_modifying_source(self) -> None:
        image = Image.new("RGB", (160, 90), "#777777")
        draw = ImageDraw.Draw(image)
        draw.rectangle((20, 20, 39, 39), fill="#e0a000")
        path = self.write_image(image, "cli.png")
        before = hashlib.sha256(path.read_bytes()).hexdigest()

        completed = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(path)],
            check=False,
            capture_output=True,
            text=True,
        )

        after = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["width"], 160)
        self.assertEqual(payload["height"], 90)
        self.assertEqual(before, after)

    def test_analysis_emits_no_deprecation_warning(self) -> None:
        image = Image.new("RGB", (160, 90), "#777777")
        path = self.write_image(image, "no-warning.png")

        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            analyze_image(path)


if __name__ == "__main__":
    unittest.main()
