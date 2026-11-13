"""ContextGuard perception package (FYP-1 combined pipeline, D21).

Observation only: detection, tracking, zone membership and visible counts.
No inference about interactions, departures, permissions or anomalies is made here.
"""

import os

# Ultralytics checks connectivity at import time. When online it may look for
# updates, auto-install missing requirements ("AutoUpdate") and send usage events.
# The project forbids unapproved installs and telemetry, so force offline mode
# before Ultralytics is ever imported. Weights must already be present locally.
os.environ.setdefault("YOLO_OFFLINE", "1")

__version__ = "0.1.0"
