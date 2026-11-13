# ContextGuard staged office dataset

Status: **PLANNED. No recordings exist yet.** This folder holds the procedures and
templates. The footage itself is never stored in this public repository.

| File | Purpose |
| --- | --- |
| [RECORDING_PROTOCOL.md](RECORDING_PROTOCOL.md) | Camera set-up, shot list (SC01–SC08), naming, storage, tuning/evaluation split, session log |
| [CONSENT_FORM_TEMPLATE.md](CONSENT_FORM_TEMPLATE.md) | Participant consent template (check university requirements first) |
| [ground_truth_template.csv](ground_truth_template.csv) | Simple per-second labelling sheet for evaluation clips |

## How to label an evaluation clip (draft)

Label once per second of video (`time_s` = 0, 1, 2, …). Watch the frame at that second and record:

- `persons_visible`: the number of people you can see, even partially.
- `laptop_visible` / `backpack_visible`: 1 if any part is visible, otherwise 0.
- `laptop_occluded`: 1 if the laptop is in the room but hidden (for example behind
  a person), otherwise 0.
- `notes`: anything unusual (person half out of frame, motion blur…).

Label only **evaluation** takes (takes 2–3), and label them before looking at the
model's output for those clips. The matching rules and metrics will be fixed in the
evaluation plan before any results are computed.
