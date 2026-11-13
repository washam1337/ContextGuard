"""Deterministic 2-D geometry helpers for zone membership.

Coordinates are image pixels with the origin at the top-left corner, x to the right
and y downwards. Boxes are ``(x1, y1, x2, y2)``.
"""

from __future__ import annotations

from typing import Sequence

Point = tuple[float, float]
Box = tuple[float, float, float, float]

ANCHORS = ("bottom_center", "center")


def anchor_point(box: Box, anchor: str) -> Point:
    """Return the point of ``box`` used to decide zone membership.

    ``bottom_center`` approximates where a standing person touches the floor, which
    is more stable for floor zones than the box centre. ``center`` suits objects.
    """
    x1, y1, x2, y2 = box
    if anchor == "bottom_center":
        return ((x1 + x2) / 2.0, y2)
    if anchor == "center":
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)
    raise ValueError(f"Unknown anchor {anchor!r}; expected one of {ANCHORS}.")


def _on_segment(px: float, py: float, a: Point, b: Point, eps: float = 1e-9) -> bool:
    (x1, y1), (x2, y2) = a, b
    cross = (px - x1) * (y2 - y1) - (py - y1) * (x2 - x1)
    if abs(cross) > eps * max(1.0, abs(x2 - x1) + abs(y2 - y1)):
        return False
    return (min(x1, x2) - eps <= px <= max(x1, x2) + eps
            and min(y1, y2) - eps <= py <= max(y1, y2) + eps)


def point_in_polygon(point: Point, polygon: Sequence[Point]) -> bool:
    """Even-odd ray casting with an **inclusive** boundary.

    A point exactly on an edge or vertex counts as inside. Works for convex and
    concave simple polygons.
    """
    px, py = point
    n = len(polygon)
    inside = False
    for i in range(n):
        a, b = polygon[i], polygon[(i + 1) % n]
        if _on_segment(px, py, a, b):
            return True
        (x1, y1), (x2, y2) = a, b
        if (y1 > py) != (y2 > py):
            x_cross = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if px < x_cross:
                inside = not inside
    return inside
