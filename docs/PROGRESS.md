# Progress — 2026-09-27

CG-001/CG-001A: repository/environment audits completed. Requirements documented;
no application functionality existed at CG-002 entry. Verified interpreter:
`/home/w4shm1337/miniconda3/envs/fyp/bin/python` (3.10.21).

CG-002: scope amendment recorded; headless recorded-video inspection implemented.
Verification results are recorded in [HANDOFF.md](HANDOFF.md).

| Component | Current status |
| --- | --- |
| Recorded-video inspection command | IMPLEMENTED; synthetic software validation only |
| Module A video ingestion | PARTIAL; offline decode/inspection only, no live capture or rolling evidence buffer |
| Representative review JPEGs and inspection JSON | IMPLEMENTED; not incident evidence or structured event storage |
| Detection/tracking, zones, interaction/asset state | PLANNED |
| Structured events, session context, anomaly rules, deterministic temporal reasoning | PLANNED |
| Evidence windows/clips, explanations, dashboard/API, feedback, evaluation | PLANNED |
| Audio and accessibility workflows | DEFERRED for current build by CG-002 working decision |
| Learned temporal modelling | PLANNED as an optional proposal, not an accepted implementation commitment |
| Custom research dataset | PLANNED; no real-video results or research metrics available |

The first complete vertical slice remains unimplemented. The next proposed task is
pilot recording and placement review using this utility, followed by a separately
scoped CPU pretrained perception baseline. No models were downloaded in CG-002.

## Repository presentation — 2026-09-27

Prepared the public repository documentation: branded README, portable setup
instructions, inspection reference, contribution guidance, issue/PR templates,
and a Python 3.10 GitHub Actions workflow. Ignore rules exclude local editor
settings, credentials, recordings, model weights, and inspection outputs.
The existing 10 software tests passed again in the verified fyp environment.
This packaging work does not change the implementation milestone or research status.

## FYP-1 scope approved; implementation pending — 2026-10-24

Recorded the user/coordinator-approved [FYP-1 amendment](../MASTER_PLAN.md#fyp-1-scope-amendment--2026-10-24)
and updated working decisions. This is documentation work only; no detection,
tracking, zones, counting or reasoning code was implemented. The original master
specification and CG-002 amendment remain unchanged; CG-002 remains completed.

| Milestone/deliverable | Current status and next evidence |
| --- | --- |
| CG-002 recorded-video inspection | IMPLEMENTED; existing inspector/schema/tests preserved. Ten automated inspection tests passed during the 2026-10-24 audit using synthetic fixtures, not research recordings. |
| CG-003 person detection/tracking | PLANNED; consented pilot/placement review, CPU pretrained baseline, anonymous tracks, frame observations and annotated preview. Replaces the earlier pilot-only CG-003 proposal. |
| CG-004 counting/zones | PLANNED; manually configured polygons, visible/per-zone counts, separate occupancy semantics and boundary/track-loss validation. |
| CG-005 office-object detection/tracking | PLANNED; laptop/backpack baseline and stationary/movement/occlusion evaluation. Document detection remains EXPERIMENTAL in scope only; no prototype exists. |
| CG-006 integration/testing/evaluation | PLANNED; reproducible recorded-video demo producing annotated video and aligned structured output, with honest evaluation and limitations. |
| Complete workflow diagram and architecture | PLANNED update; must cover user configuration/storage, processing/reasoning, evidence and separately stored feedback with implementation boundaries. Existing conceptual diagrams do not complete this deliverable. |
| Dataset and pretrained-model documentation | PLANNED; no collected research dataset, selected model/weights or office-video metrics are claimed. |
| SYS-01–SYS-08 | Definitions recorded in the amendment; all PLANNED / NOT RUN. Separate from CG-002 automated tests. |
| Updated milestones and roadmap | Phase scope and exit criteria documented; detailed implementation/evaluation protocols and revised dates remain pending. |

FYP-1's executable path ends at annotated video and structured observations.
Interaction/asset state, contextual/temporal reasoning, incidents, evidence clips,
dashboard/API, feedback persistence and comparative reasoning evaluation remain
later PLANNED work. Audio/accessibility remain DEFERRED; learned temporal modelling
remains optional/proposed. Visible-person counts must not be reported as inferred
office occupancy without an explicit validated policy.

Next milestone is CG-003, beginning with consented pilot collection and camera
placement review using the preserved inspector. Pending decisions include model
selection, schema/timing and zone/count policies, occupancy duration semantics,
affirmative departure evidence and quantitative acceptance targets. Supervisor
communication remains pending; approval and past presentation outcomes are not
asserted. No milestone implementation or system-level pass is claimed here.

## Claude Code handoff — 2026-11-13

Documentation and knowledge-transfer work only. No code, schema, dependency, model,
dataset or milestone changes. CG-003 has not started.

- Read-only audit by Claude Code: 10/10 CG-002 tests pass (1.63 s, `fyp` interpreter);
  CI passed on both pushes; `MASTER_PLAN.md` confirmed append-only (original and
  CG-002 versions are exact byte prefixes); orphan `local-preparation` branch
  identified as a byte-identical, unpushed copy of `dd765fe`.
- With owner permission, read all five local Codex transcripts and archived curated,
  sanitised summaries (raw transcripts not committed).
- Added: `CLAUDE.md`, `docs/CURRENT_STATE.md`, `docs/history/README.md`,
  `docs/history/TIMELINE.md`, `docs/history/chatgpt/README.md` and five
  `docs/history/codex/*.md` session summaries. Appended D17–D19 to `DECISIONS.md`
  and this entry.
- Recovered and recorded previously undocumented context: the supervisor feedback, the
  presentation requirement and the 2026-12-31 completion target.
- Not changed, pending owner approval: `README.md` (stale; proposal shown to owner),
  `CONTRIBUTING.md`, the orphan branch.

Next: owner review of these changes; owner-arranged consented pilot recording; then,
on approval, a CG-003 plan before any implementation. See
[CURRENT_STATE.md § 9](CURRENT_STATE.md#9-exact-next-recommended-action).

## README brought up to date — 2026-11-13

With owner approval, the handoff commit `f2969af` was pushed and `README.md` was
updated for the FYP-1 phase: status box, capabilities table, CG-003–CG-006 roadmap,
governing-scope links and documentation table. The README diagram and
`CONTRIBUTING.md` are unchanged. `CLAUDE.md` and `docs/CURRENT_STATE.md` were
updated to match. Documentation only; CG-003 has not started.

## Combined perception pipeline started — 2026-11-13

Owner decisions D20–D23: presentation on 2026-11-24; CG-003–CG-005 combined into one
pipeline; Ultralytics YOLO route (AGPL-3.0 accepted); CPU installs approved.

- Installed `torch 2.14.1+cpu`, `torchvision 0.29.2+cpu`, `ultralytics 8.4.212`,
  `lap 0.5.14` into `fyp`. The dry run showed additions only, and no existing
  package changed; `pip check` clean. Pinned in `requirements.txt`. Ultralytics
  telemetry disabled.
- Downloaded candidate weights yolo26n/s and yolo11n/s to git-ignored `weights/`,
  with SHA-256 in [MODELS.md](MODELS.md). The one-image CPU smoke test is recorded
  there and is not a benchmark.
- Added the recording protocol, consent template and labelling template in
  [dataset/](dataset/README.md).
- No pipeline code yet; no footage; no accuracy measured. CG-002 tests: 10/10 pass.

## Combined perception pipeline implemented (synthetic validation) — 2026-11-13

Built the observation-only pipeline for D21, documented in [PIPELINE.md](PIPELINE.md):

- New `contextguard/` package: geometry, zones (`contextguard.zones.v1`), perception
  adapters (YOLO detector plus one ByteTrack tracker per class), observation records
  (`contextguard.observation.v1`, observed vs predicted boxes, count policy v1,
  inferred occupancy always null), video I/O, annotation and pipeline with a
  `contextguard.run_manifest.v1` provenance file.
- New `scripts/run_pipeline.py` and `scripts/benchmark_models.py`;
  `configs/tracker/bytetrack.json`; a draft zones template.
- Tests: 31 pass (CG-002 ×10 plus 21 new). One is a real YOLO26n smoke test that
  skips without weights.
- End-to-end on a synthetic 90-frame clip with YOLO26n: 172/172 expected person
  detections, 2 track IDs, an 8-frame occlusion handled as lost/predicted then
  re-found under the same ID, records and annotated frames aligned, 14.7 frames/s
  overall. Randomised CPU benchmark of the four candidates recorded in
  [MODELS.md](MODELS.md).
- Status: PARTIAL. No office footage, laptop or backpack validation yet; the owner
  records footage by 2026-11-17.

## Documentation accuracy review — 2026-11-15

An owner-requested review of the docs at `d2f2cfa`, each point verified against the
files and test output:

- `CURRENT_STATE.md` corrected:
  - implementation status;
  - D-number range (D01–D24);
  - test result (31 run, 31 pass, 0 skipped with weights present);
  - footage/weights rows;
  - Deliverable 4 → PARTIAL;
  - commits and CI rows;
  - consent marked resolved (D24);
  - perception-pipeline decisions settled on 2026-11-13 moved out of "open".
- Re-checked known gap 7: tests still need the repo root. From `/tmp`, 8 test modules
  fail to import `contextguard`/`scripts`, which are not installed packages.
- `docs/dataset/ground_truth_template.csv`: added a `backpack_occluded` column (for
  SC07), with matching labelling instructions. The CSV is a **draft working
  template, not a versioned schema**, so no version bump. No labels have been
  recorded with the old layout.
- Proposed, not applied (awaiting owner approval):
  - README update;
  - AGPL-3.0 LICENSE;
  - CONTRIBUTING fix;
  - optional SC09 restricted-zone scenario;
  - session-based evaluation split;
  - options for the personal details in `MASTER_PLAN.md`.

## Review follow-up applied — 2026-11-15

The review that triggered the entry above came from a **Claude cloud session**
reading the GitHub repository, relayed by the owner. The owner delegated the fixes:

- Added `LICENSE`: GNU AGPL-3.0, an exact copy of the text shipped with Ultralytics
  8.4.212 (SHA-256 `0d96a4ff…abcb0`) (D25).
- `README.md` updated:
  - pipeline status as partial, synthetic tests only;
  - capabilities table;
  - run instructions with a one-time weights download and checksum check;
  - diagram with implemented/partial/planned nodes;
  - roadmap, 31-test breakdown and file tree;
  - licence section and badges.
- `CONTRIBUTING.md`: points to `CURRENT_STATE.md`, the FYP-1 amendment and
  `CLAUDE.md`; says to run tests from the repo root; notes the AGPL licence; adds
  "no frames or videos of people" to the commit rules.
- Recording protocol:
  - optional scenario **SC09** (restricted-area visit, observation only) (D26);
  - tuning/evaluation split changed to **by session**, S01 tuning and S02 evaluation,
    with the by-take fallback (D27).
- Status lines updated to match: `CLAUDE.md`, `CURRENT_STATE.md`, `MODELS.md` and
  `dataset/README.md`.
- Still waiting for the owner: what to do about the personal details in
  `MASTER_PLAN.md` lines 84–85.
- Owner decision on the personal details in `MASTER_PLAN.md`: leave them as they are (D28).

### 2026-11-15: second review follow-up (cloud review of `881d44a`)

- `CURRENT_STATE.md`: decision-log range now D01–D28; commits row names `881d44a`;
  CI row names run 43729300017.
- Recording protocol: naming example changed to an S02 file; added the placement
  test-clip rule `cg_<YYYYMMDD>_S00_TEST_t1.mp4` (session S00, neither tuning nor
  evaluation); inspector example uses the test clip. Labelling template example rows
  now use an S02 file.
- Checked YOLO26 NMS behaviour in Ultralytics 8.4.212: the default `.pt` predict path
  uses NMS for both YOLO26 and YOLO11, so `--iou` applies to both. Recorded in
  `MODELS.md`.
- Confirmed by code reading: zones are not re-scaled to the decoded frame size when
  the reported size differs from both the decoded size and the zone reference size
  (`pipeline.py`). Fix proposed, awaiting owner approval.
- Waiting for footage: decoded vs reported size, timing drift and the seated-person
  anchor check.

### 2026-11-15: zone-scaling fix (owner approved)

- `contextguard/pipeline.py`: zones are now scaled from the zone reference size to
  the **decoded** frame size, never the reported metadata size. Warnings are added
  when the decoded size differs from the reported size and when the frame size
  changes mid-video. No schema change (`zones.applied_scale` already existed).
- New test `test_zones_scale_to_decoded_size_not_reported_size` (reported 320×240,
  decoded 160×120, reference 640×480). It fails on the old code (scale 0.5) and
  passes with the fix (scale 0.25).
- Tests: 32 run, 32 pass, 0 skipped.
- `CURRENT_STATE.md` gap 11 marked fixed; `PIPELINE.md` scaling note and test count updated; `README.md` test count 31→32 (owner approved).


### 2026-11-21: session S01 received and checked (no model results)

Footage: 10 clips recorded 2026-11-20 in `~/contextguard-data/raw/S01/` (outside Git).
All checks were read-only; SHA-256 of every original was verified unchanged afterwards.

- **Files vs log:** SC01–SC08, DOC01, DOC02 present. No separate S00 test clip (SC01
  served as the placement check). SC09 not recorded.
- **Technical (CG-002 inspector, a container parser and an OpenCV frame pass):**
  - all 10 decode fully;
  - H.264 1920×1080, no rotation, plus an AAC audio track;
  - effectively constant 30.0 fps (2–7 frames per clip last 35 ms instead of 33.3 ms);
  - 15.1–33.1 s per clip (452–994 frames);
  - decoded size equals reported size;
  - `estimated_seconds` vs decoder timestamps differ by ≤ 10 ms;
  - SC02 has an edit list (631 stored, 611 decoded frames), which OpenCV honours.
- **Camera:** SC01–SC08 within ~3 px of each other (one zone configuration fits);
  DOC01/DOC02 shifted ~220 px (camera moved slightly).
- **Content:** scenario-by-scenario observations and deviations are recorded in
  `dataset/RECORDING_PROTOCOL.md` § 8 and the private session log. Notably, SC04 shows
  no brief exceedance, and in SC08 the laptop is placed on the PC tower out of view and
  not returned within the clip.
- **Correction:** in the first footage report Claude said SC06–SC08 showed a different
  laptop. A full-resolution crop showed the same laptop and sticker, moved slightly and
  angled differently; the owner confirmed one laptop.
- **Documents (exploratory, D32):** results recorded in `MODELS.md`. The desk stack is a
  weak `book` detection; the document on the PC tower is not detected.
- **Owner decisions:** D29 (S01 only), D30 (development results only), D31 (audio never
  used), D32 (documents EXPERIMENTAL).
- **Session log:** completed by Claude Code from the owner's answers; the owner's draft
  is kept as `session_log_S01.owner_draft.txt`.
- **Docs updated:** `CURRENT_STATE.md`, `DECISIONS.md`, `PIPELINE.md`, `MODELS.md`,
  `dataset/RECORDING_PROTOCOL.md` (status line, § 6 note, new § 8),
  `dataset/README.md` and `ground_truth_template.csv` (now label S01 SC01–SC08).
- **Not done:**
  - `chmod a-w` on the originals and deleting the `Zone.Identifier` file were approved
    by the owner but blocked by Claude Code's permission system; the owner runs them;
  - no pipeline run, model choice or result on footage yet.
- Owner (2026-11-21): due on Nov 24 is a presentation plus code preparation showing the
  FYP about 30–40% working. Next session starts with the S01 zone configuration.
- The owner ran the blocked step: S01 originals are now read-only and the
  `Zone.Identifier` file is deleted; all 10 checksums re-verified unchanged.

### 2026-11-23: S01 zones approved; results plan drafted; labelling material made

- **Zones (D33):** `configs/zones/S01_office_v1.json` drawn on SC01 frame 0 and checked
  against yolo26n detections at conf ≥ 0.25 on every 10th frame of SC01–SC08:
  - all 464 laptop detections fall in `desk_area`;
  - of 554 person detections, 391 are in `foreground` (box bottom at the frame
    edge), 132 in `doorway` and 18 in `desk_area` (people standing behind the desk
    or the PC tower with their lower body hidden, checked visually in SC07); 13 are in
    no zone (walking across open floor).

  The owner approved the zones from an overlay picture of the empty room (no
  detections shown, to avoid biasing the labels).
- **Early observation (not a result):** in that sample yolo26n detected the backpack only
  4 times, all while it was carried at the door, and never on the armchair (dark
  backpack on a dark chair). All four models are compared under the plan.
- **Results plan:** `docs/S01_RESULTS_PLAN.md` written before any labels exist. It
  fixes the labelling rules, matching rule, metrics, settings, all-four-models
  reporting and the demo-model rule. Awaiting owner approval.
- **Labelling material** (outside the repository):
  - 202 stills, one per second of SC01–SC08, at decoded frame
    `round(t × reported_fps)`, in `~/contextguard-data/labelling/S01/`;
  - a pre-filled sheet, `~/contextguard-data/labels/S01_labels.csv`.
- **Runs started:** all four models × SC01–SC08, plan settings, no video, into
  `~/contextguard-data/runs/S01/`. No comparison with labels yet.
- Owner approved the results plan (D34), before labelling started. The stills and
  sheet were copied to the owner's Windows Desktop (`ContextGuard_labelling`) for
  labelling; the completed sheet is copied back to
  `~/contextguard-data/labels/S01_labels.csv`.

