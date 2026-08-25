#!/usr/bin/env python3
"""Report selective-color and white-field distribution without editing pixels."""

from __future__ import annotations

import argparse
from collections import deque
import json
import math
from pathlib import Path
from typing import Iterable

from PIL import Image


TARGET_RATIO = 16 / 9
RATIO_TOLERANCE = 0.01
MIN_VISIBLE_VALUE = 32
MIN_COMPONENT_FRACTION = 0.0005
MIN_COMPONENT_PIXELS = 4
WHITE_MAX_SATURATION = 25
WHITE_MIN_VALUE = 218
MIN_CONTIGUOUS_WHITE_FIELD_FRACTION = 0.30


def build_chroma_mask(
    hsv_image: Image.Image, saturation_threshold: int
) -> list[bool]:
    return [
        saturation >= saturation_threshold and value >= MIN_VISIBLE_VALUE
        for _, saturation, value in hsv_image.get_flattened_data()
    ]


def build_white_field_mask(hsv_image: Image.Image) -> list[bool]:
    """Return pixels that can read as a clean neutral white ground."""
    return [
        saturation <= WHITE_MAX_SATURATION and value >= WHITE_MIN_VALUE
        for _, saturation, value in hsv_image.get_flattened_data()
    ]


def connected_components(
    mask: list[bool], width: int, height: int
) -> list[list[tuple[int, int]]]:
    visited = bytearray(len(mask))
    components: list[list[tuple[int, int]]] = []

    for start, active in enumerate(mask):
        if not active or visited[start]:
            continue

        visited[start] = 1
        queue = deque([start])
        component: list[tuple[int, int]] = []

        while queue:
            index = queue.popleft()
            x = index % width
            y = index // width
            component.append((x, y))

            for neighbor in _neighbors(index, x, y, width, height):
                if mask[neighbor] and not visited[neighbor]:
                    visited[neighbor] = 1
                    queue.append(neighbor)

        components.append(component)

    return components


def _neighbors(
    index: int, x: int, y: int, width: int, height: int
) -> Iterable[int]:
    if x > 0:
        yield index - 1
    if x + 1 < width:
        yield index + 1
    if y > 0:
        yield index - width
    if y + 1 < height:
        yield index + width


def _scaled_bbox(
    mask: list[bool],
    analysis_size: tuple[int, int],
    original_size: tuple[int, int],
) -> list[int] | None:
    analysis_width, analysis_height = analysis_size
    active = [index for index, enabled in enumerate(mask) if enabled]
    if not active:
        return None

    xs = [index % analysis_width for index in active]
    ys = [index // analysis_width for index in active]
    original_width, original_height = original_size
    scale_x = original_width / analysis_width
    scale_y = original_height / analysis_height

    return [
        math.floor(min(xs) * scale_x),
        math.floor(min(ys) * scale_y),
        min(original_width - 1, math.ceil((max(xs) + 1) * scale_x) - 1),
        min(original_height - 1, math.ceil((max(ys) + 1) * scale_y) - 1),
    ]


def build_report(
    original_size: tuple[int, int],
    analysis_size: tuple[int, int],
    chroma_mask: list[bool],
    chroma_components: list[list[tuple[int, int]]],
    white_field_mask: list[bool],
    white_field_components: list[list[tuple[int, int]]],
) -> dict[str, object]:
    width, height = original_size
    analysis_width, analysis_height = analysis_size
    total_pixels = analysis_width * analysis_height
    chromatic_pixels = sum(chroma_mask)
    chromatic_fraction = chromatic_pixels / total_pixels
    white_field_pixels = sum(white_field_mask)
    white_field_fraction = white_field_pixels / total_pixels
    minimum_component_size = max(
        MIN_COMPONENT_PIXELS, math.ceil(total_pixels * MIN_COMPONENT_FRACTION)
    )
    meaningful_components = [
        component
        for component in chroma_components
        if len(component) >= minimum_component_size
    ]
    largest_component = max(
        (len(component) for component in chroma_components), default=0
    )
    largest_white_field = max(
        (len(component) for component in white_field_components), default=0
    )
    largest_white_field_fraction = largest_white_field / total_pixels
    aspect_ratio = width / height
    is_16_9 = abs(aspect_ratio - TARGET_RATIO) <= RATIO_TOLERANCE

    warnings: list[str] = []
    if not is_16_9:
        warnings.append("not_16_9")
    if chromatic_fraction > 0.25:
        warnings.append("excessive_chroma")
    if len(meaningful_components) > 3:
        warnings.append("scattered_chroma")
    if chromatic_fraction < 0.002:
        warnings.append("no_decisive_chroma")
    if largest_white_field_fraction < MIN_CONTIGUOUS_WHITE_FIELD_FRACTION:
        warnings.append("insufficient_white_field")

    return {
        "width": width,
        "height": height,
        "aspect_ratio": round(aspect_ratio, 6),
        "is_16_9": is_16_9,
        "analysis_width": analysis_width,
        "analysis_height": analysis_height,
        "chromatic_fraction": round(chromatic_fraction, 6),
        "component_count": len(meaningful_components),
        "largest_component_fraction": round(largest_component / total_pixels, 6),
        "chromatic_bbox": _scaled_bbox(
            chroma_mask, analysis_size, original_size
        ),
        "white_field_fraction": round(white_field_fraction, 6),
        "largest_white_field_fraction": round(
            largest_white_field_fraction, 6
        ),
        "warnings": warnings,
    }


def analyze_image(
    path: Path | str, saturation_threshold: int = 64, max_edge: int = 640
) -> dict[str, object]:
    source_path = Path(path)
    with Image.open(source_path) as source:
        original = source.convert("RGB")

    original_size = original.size
    analysis = original.copy()
    analysis.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
    hsv = analysis.convert("HSV")
    chroma_mask = build_chroma_mask(hsv, saturation_threshold)
    chroma_components = connected_components(
        chroma_mask, analysis.width, analysis.height
    )
    white_field_mask = build_white_field_mask(hsv)
    white_field_components = connected_components(
        white_field_mask, analysis.width, analysis.height
    )
    return build_report(
        original_size,
        analysis.size,
        chroma_mask,
        chroma_components,
        white_field_mask,
        white_field_components,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect aspect ratio, high-chroma distribution, and contiguous "
            "white field without editing pixels."
        )
    )
    parser.add_argument("image", type=Path)
    parser.add_argument("--saturation-threshold", type=int, default=64)
    parser.add_argument("--max-edge", type=int, default=640)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = analyze_image(
        args.image,
        saturation_threshold=args.saturation_threshold,
        max_edge=args.max_edge,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
