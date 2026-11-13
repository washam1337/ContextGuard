"""Deterministic zone geometry and configuration tests (no model, no video)."""

import json
import tempfile
import unittest
from pathlib import Path

from contextguard.geometry import anchor_point, point_in_polygon
from contextguard.zones import ZoneConfigError, load_zone_config, parse_zone_config

SQUARE = [(0, 0), (10, 0), (10, 10), (0, 10)]
L_SHAPE = [(0, 0), (10, 0), (10, 4), (4, 4), (4, 10), (0, 10)]  # concave


def config(**overrides):
    base = {
        "schema_version": "contextguard.zones.v1",
        "config_id": "test-v1",
        "reference_width": 100,
        "reference_height": 50,
        "membership_anchors": {"person": "bottom_center", "default": "center"},
        "zones": [
            {"id": "door", "kind": "entry", "polygon": [[0, 0], [20, 0], [20, 50], [0, 50]]},
            {"id": "floor", "kind": "general", "polygon": [[0, 40], [100, 40], [100, 50], [0, 50]]},
        ],
    }
    base.update(overrides)
    return base


class GeometryTests(unittest.TestCase):
    def test_inside_outside(self):
        self.assertTrue(point_in_polygon((5, 5), SQUARE))
        self.assertFalse(point_in_polygon((15, 5), SQUARE))
        self.assertFalse(point_in_polygon((-0.01, 5), SQUARE))

    def test_boundary_is_inclusive(self):
        for p in [(0, 5), (10, 10), (5, 0), (0, 0)]:
            self.assertTrue(point_in_polygon(p, SQUARE), p)

    def test_concave_polygon(self):
        self.assertTrue(point_in_polygon((2, 8), L_SHAPE))
        self.assertFalse(point_in_polygon((8, 8), L_SHAPE))  # inside the notch
        self.assertTrue(point_in_polygon((8, 2), L_SHAPE))

    def test_anchors(self):
        box = (10, 20, 30, 60)
        self.assertEqual(anchor_point(box, "bottom_center"), (20, 60))
        self.assertEqual(anchor_point(box, "center"), (20, 40))
        with self.assertRaises(ValueError):
            anchor_point(box, "top")


class ZoneConfigTests(unittest.TestCase):
    def test_membership_uses_class_anchor_and_allows_overlap(self):
        zc = parse_zone_config(config())
        person = (5, 10, 15, 45)  # feet at (10, 45): in door and floor; centre (10, 27.5) only in door
        self.assertEqual(zc.zones_for_box(person, "person"), ["door", "floor"])
        self.assertEqual(zc.zones_for_box(person, "laptop"), ["door"])
        self.assertEqual(zc.zones_for_box((60, 0, 80, 10), "person"), [])

    def test_validation_errors(self):
        bad = [
            config(schema_version="v0"),
            config(config_id=""),
            config(reference_width=0),
            config(boundary_policy="exclusive"),
            config(membership_anchors={"person": "head"}),
            config(zones=[]),
            config(zones=[{"id": "a", "polygon": [[0, 0], [1, 1]]}]),
            config(zones=[{"id": "a", "polygon": [[0, 0], [1, 0], [1, 1]]},
                          {"id": "a", "polygon": [[0, 0], [1, 0], [1, 1]]}]),
            config(zones=[{"id": "a", "kind": "alarm", "polygon": [[0, 0], [1, 0], [1, 1]]}]),
            config(zones=[{"id": "a", "polygon": [[0, 0], [101, 0], [1, 1]]}]),
            config(zones=[{"id": "a", "polygon": [[0, 0], [True, 0], [1, 1]]}]),
        ]
        for data in bad:
            with self.assertRaises(ZoneConfigError, msg=json.dumps(data)[:120]):
                parse_zone_config(data)

    def test_scaling_and_aspect_warning(self):
        zc = parse_zone_config(config())
        scaled, warnings = zc.scaled_for(200, 100)
        self.assertEqual(warnings, [])
        self.assertEqual(scaled.zones[0].polygon[1], (40.0, 0.0))
        self.assertEqual(scaled.scale, (2.0, 2.0))
        _, warnings = zc.scaled_for(200, 200)
        self.assertTrue(any("aspect ratio" in w for w in warnings))

    def test_load_records_checksum_and_template_is_valid(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "z.json"
            p.write_text(json.dumps(config()))
            zc = load_zone_config(p)
            self.assertEqual(len(zc.sha256), 64)
            self.assertEqual(zc.describe()["schema_version"], "contextguard.zones.v1")
        template = Path(__file__).resolve().parents[1] / "configs" / "zones" / "TEMPLATE_staged_office.json"
        self.assertTrue(load_zone_config(template).draft)


if __name__ == "__main__":
    unittest.main()
