# Staged office recording protocol (FYP-1)

Status: **DRAFT, PLANNED**. No recordings exist yet. This protocol governs the
team-recorded, consented, staged footage used for the 2026-11-24 FYP-1
presentation (D20, D21). Synthetic test fixtures are not part of this dataset.

## 1. Before recording

- Every volunteer reads and signs the [consent form](CONSENT_FORM_TEMPLATE.md)
  **before** any camera is switched on. Keep signed forms on paper or in private
  storage, never in this repository.
- Give each volunteer an anonymous code (`V1`, `V2`, `V3`, …). Use codes, never
  names, in file names, logs and labels.
- The office occupant is **not** in the footage (all people are visitors, D02).
- Remove or cover anything private in view: screens, documents, notice boards,
  name plates.

## 2. Camera set-up (keep identical for every take)

| Setting | Value |
| --- | --- |
| Device | One phone or webcam. Write the model in the session log. |
| Mounting | Fixed: tripod or stable shelf, high in a corner, angled down |
| Field of view | Must include the **doorway** and the **desk**, with the laptop and backpack at their registered starting positions |
| Orientation | Landscape |
| Resolution / rate | 1920×1080 or 1280×720, 30 fps (constant frame rate if the app allows it) |
| Format | MP4 (H.264) |
| Focus / exposure | Locked (tap-and-hold on phones). No zoom. No filters, HDR or stabilisation. |
| Lighting | Even room light; avoid strong backlight from windows |
| Audio | Not needed; mute or ignore (audio is DEFERRED) |

Do **not** move the camera between takes. If it moves, start a new session ID.

Before the main session, record one 30–60 s **test clip**, named
`cg_<YYYYMMDD>_S00_TEST_t1.mp4` (section 4), and run the inspector (section 5) to
check placement.

## 3. Shot list

Each clip is 30–90 s. Start and end each clip with **3 s of the room as it is**.
Record each scenario **once in session S01 and twice in session S02** (section 6),
with volunteers paired differently where possible.

| Code | Scenario | Script | What it tests |
| --- | --- | --- | --- |
| SC01 | Empty room | 30 s, nobody, laptop and backpack in place | No false detections |
| SC02 | One visitor | V enters, sits ~20 s, leaves | Person detection and tracking |
| SC03 | Two visitors at once | V1 enters; V2 enters; both stay ≥20 s; both leave | Simultaneous count (relates to SYS-02) |
| SC04 | Brief second visitor | V1 inside; V2 enters, leaves within ~3 s | Brief exceedance (relates to SYS-07) |
| SC05 | Laptop carried out | V walks to desk, picks up laptop, leaves with it | Carried object (relates to SYS-03/04) |
| SC06 | Laptop occluded | V stands between camera and laptop ~5 s, moves away | Occlusion is not departure (relates to SYS-05) |
| SC07 | Backpack carried out | V picks up backpack, leaves with it | Second asset |
| SC08 | Laptop moved and returned | V moves laptop across desk, puts it back | Moved, not removed |
| SC09 *(optional)* | Restricted-area visit | V walks into the corner configured as the `restricted` zone (e.g. beside a cabinet), stays ~5 s, returns, leaves | Membership in a `restricted`-kind zone on real footage. Recorded as an observation only, **never a violation**. |

SC09 is optional (D26). Record it only if time allows, and decide which corner is
the restricted zone **before** recording.

The relations to SYS cases are for planning only. SYS-01–08 stay PLANNED / NOT RUN
until the later reasoning stage exists.

## 4. Files, naming and storage

- Store footage **outside this repository**, e.g. `~/contextguard-data/raw/`. It
  must never be committed; this repository is public.
- Name each file `cg_<YYYYMMDD>_<session>_<scenario>_t<take>.mp4`,
  e.g. `cg_20261117_S02_SC03_t2.mp4` (session S02, scenario SC03, take 2). A
  session (`S01`, `S02`…) is one continuous camera set-up.
- The placement **test clip** uses session `S00` and scenario `TEST`, e.g.
  `cg_20261117_S00_TEST_t1.mp4`. It belongs to neither S01 (tuning) nor S02
  (evaluation): it is used only to check camera placement, decoded frame size and
  timing, never for tuning thresholds or for reported results.
- **Never edit, trim or re-encode the originals.** Processing writes to new folders.
- Fill in the session log below for every session.

## 5. Placement check (CG-002 inspector)

```bash
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B scripts/inspect_video.py \
  --input ~/contextguard-data/raw/cg_20261117_S00_TEST_t1.mp4 \
  --output ~/contextguard-data/inspection/cg_20261117_S00_TEST_t1
```

Check the three exported frames: are the doorway, laptop and backpack visible and
large enough? Also watch the clip, because three frames cannot show everything.

## 6. Tuning versus evaluation split

The split is **by session** (D27), fixed **before** looking at any model results:

| Session | Purpose | What to record |
| --- | --- | --- |
| **S01: tuning** | Choose the model size, thresholds and zones; review failures | Every scenario, take 1 |
| **S02: evaluation** | Reported results only; never used for tuning | Every scenario, takes 1–2 |

How to make S02 a genuinely separate session:

- Record it at a **different time**: a few hours later or another day, so the
  lighting differs.
- Use **different volunteer pairings** or clothing from S01 wherever possible.
- **Keep the camera in exactly the same place**, so one zone configuration fits both
  sessions. If the camera moves, note it and a new zone configuration is drawn.
- Fill in a separate session log for S02.

**Known limitation:** with only 2–3 volunteers, the same people appear in both
sessions. This must be stated in the evaluation report.

**Fallback:** if S02 cannot be recorded before 2026-11-17, record three takes in one
session and split by take (take 1 for tuning, takes 2–3 for evaluation). Report this
as the weaker split.

Report the split, and every evaluation clip, including the failures.

## 7. Session log (copy for each session)

```text
Session ID:            S01
Date / time:
Location:              staged office room (no private details)
Camera device / app:
Resolution / fps:
Camera position notes: (photo of the set-up stored privately)
Laptop position:       (desk, left/right…)
Backpack position:
Lighting:
Volunteers present:    V1, V2, …   (consent forms signed: yes/no)
Clips recorded:        file name | scenario | take | notes
Problems:
```
