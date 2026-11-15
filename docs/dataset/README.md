# ContextGuard staged office dataset

Status: **PLANNED. No recordings exist yet.** This folder holds the procedures and
templates. The footage itself is never stored in this public repository.

| File | Purpose |
| --- | --- |
| [RECORDING_PROTOCOL.md](RECORDING_PROTOCOL.md) | Camera set-up, shot list (SC01–SC08, optional SC09), naming, storage, session-based tuning/evaluation split, session log |
| [CONSENT_FORM_TEMPLATE.md](CONSENT_FORM_TEMPLATE.md) | Participant consent template (check university requirements first) |
| [ground_truth_template.csv](ground_truth_template.csv) | Simple per-second labelling sheet for evaluation clips |

## How to label an evaluation clip (draft)

The CSV is a draft working template, not a versioned schema. Columns may change
until the evaluation plan is fixed, and any change is logged in `PROGRESS.md`.

Label once per second of video (`time_s` = 0, 1, 2, …). Watch the frame at that second and record:

- `persons_visible`: the number of people you can see, even partially.
- `laptop_visible` / `backpack_visible`: 1 if any part is visible, otherwise 0.
- `laptop_occluded` / `backpack_occluded`: 1 if that object is in the room but
  hidden (for example behind a person), otherwise 0. An object carried out of the
  room is `*_visible = 0` and `*_occluded = 0`; note it in `notes`.
- `notes`: anything unusual (person half out of frame, motion blur…).

Label only **evaluation** clips (session S02, or takes 2–3 under the fallback split),
and label them before looking at the model's output for those clips. The matching rules and metrics will be fixed in the
evaluation plan before any results are computed.
