from __future__ import annotations

import json
from pathlib import Path
import unittest

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SHOWCASE_ROOT = PROJECT_ROOT / "examples" / "showcase"
MANIFEST_PATH = SHOWCASE_ROOT / "manifest.json"
EXPECTED_SLUGS = {
    "tree-lane-cyclist",
    "coastal-field-runner",
    "seaside-piano-gesture",
    "orange-city-facade",
    "tallest-palm",
    "hyeopjae-turquoise-line",
    "cliffside-witness",
}


class ShowcaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_manifest_contains_exactly_the_seven_approved_cases(self) -> None:
        cases = self.manifest["cases"]
        self.assertEqual(len(cases), 7)
        self.assertEqual({case["slug"] for case in cases}, EXPECTED_SLUGS)

    def test_every_case_is_a_before_after_pair_with_publication_approval(self) -> None:
        for case in self.manifest["cases"]:
            with self.subTest(case=case["slug"]):
                self.assertEqual(case["publication_approval"], "2026-08-25")
                self.assertIn(case["mode"], {"decisive-element", "decisive-color"})
                self.assertTrue(case["anchor_zh"])

                before = PROJECT_ROOT / case["before"]
                after = PROJECT_ROOT / case["after"]
                self.assertTrue(before.is_file(), before)
                self.assertTrue(after.is_file(), after)

                with Image.open(before) as image:
                    self.assertGreater(image.width, 0)
                    self.assertGreater(image.height, 0)

                with Image.open(after) as image:
                    self.assertAlmostEqual(image.width / image.height, 16 / 9, delta=0.01)

    def test_gallery_references_every_pair(self) -> None:
        gallery = (PROJECT_ROOT / "examples" / "README.md").read_text(encoding="utf-8")
        for case in self.manifest["cases"]:
            with self.subTest(case=case["slug"]):
                self.assertIn(case["before"].removeprefix("examples/"), gallery)
                self.assertIn(case["after"].removeprefix("examples/"), gallery)


if __name__ == "__main__":
    unittest.main()
