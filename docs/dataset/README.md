# ContextGuard staged office dataset

Status: **Session S01 recorded on 2026-11-20** (10 clips; the only FYP-1 dataset, D29).
This folder holds the procedures and templates. The footage itself is never stored
in this public repository; it is in `~/contextguard-data/raw/S01/` on the project
laptop. What was recorded, and how it deviates from the protocol, is in
[RECORDING_PROTOCOL.md § 8](RECORDING_PROTOCOL.md#8-s01-as-recorded-2026-11-20).

| File | Purpose |
| --- | --- |
| [RECORDING_PROTOCOL.md](RECORDING_PROTOCOL.md) | Camera set-up, shot list (SC01–SC08, optional SC09), naming, storage, session-based tuning/evaluation split, session log |
| [CONSENT_FORM_TEMPLATE.md](CONSENT_FORM_TEMPLATE.md) | Participant consent template (check university requirements first) |
| [ground_truth_template.csv](ground_truth_template.csv) | Simple per-second labelling sheet for the scenario clips |

## How to label a clip (draft)

The CSV is a draft working template, not a versioned schema. Columns may change
until the evaluation plan is fixed, and any change is logged in `PROGRESS.md`.

Label once per second of video (`time_s` = 0, 1, 2, …). Watch the frame at that second and record:

- `persons_visible`: the number of people you can see, even partially.
- `laptop_visible` / `backpack_visible`: 1 if any part is visible, otherwise 0.
- `laptop_occluded` / `backpack_occluded`: 1 if that object is in the room but
  hidden (for example behind a person), otherwise 0. An object carried out of the
  room is `*_visible = 0` and `*_occluded = 0`; note it in `notes`.
- `notes`: anything unusual (person half out of frame, motion blur…).

For FYP-1, label the S01 scenario clips **SC01–SC08** (D30). DOC01/DOC02 are
exploratory and are not labelled. Label each clip **before watching the pipeline's
annotated output** for it. Because S01 is also used for tuning, results computed
from these labels are **development results**, never a held-out evaluation (D30).
The matching rules and metrics are fixed in writing before any results are computed.
(If a later held-out session is recorded, only its clips count as evaluation.)
