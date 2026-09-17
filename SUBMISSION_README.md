# RAKSHANEX — ARC Prize 2026 Submission (ARC-AGI-2 track)

**Calibration-Free Consistency-Ambiguity Gating for Safe, Zero-Hallucination Rule Induction**

Org: RAKSHANEX TECHNOLOGIES · License: MIT-0 (see `LICENSE`) · Self-contained (numpy only).

---

## What this is
A program-synthesis ARC solver whose defining feature is **safe abstention**: it answers
only when all train-consistent candidate programs agree on the test output, else abstains.
Result on ARC-AGI-1 public training: **40 solved, 0 wrong (100% answered-precision)**.
The same principle holds on ARC-AGI-2 and four non-ARC domains (see paper).

## Files
- `arc_prize_submission.py` — self-contained Kaggle submission script (no internet/LLM).
- `ARC_PRIZE_2026_PAPER.md` — the paper (rubric format).
- `LICENSE` — MIT-0.
- Supporting research trail: `RAKSHANEX_*.md`, `rakshanex_*.py` (phases, audits, cross-domain).

## How it works (1-paragraph)
Generate candidate grid-transformation programs (geometry, object ops, parameterized +
learned local rules; depth-1/2 compositions) → keep only those consistent with ALL train
pairs → run them on the test input → if they produce exactly ONE distinct output, answer
it; otherwise abstain. No confidence calibration, no thresholds. See paper §Approach.

## Reproduce locally
Requirements: Python 3.10+, numpy.
```
# ARC-AGI-1 (expects arc_full/data/training/*.json  — github.com/fchollet/ARC-AGI)
# ARC-AGI-2 (expects arc_agi2/data/training/*.json — github.com/arcprize/ARC-AGI-2)
python3 arc_prize_submission.py     # dry-run: writes a sample submission.json, prints counts
```
To score the safety metric (solved / wrong / abstain, all test pairs), see
`rakshanex_phase11_varlocal.py` (full solver) and `verify_safety_module.py`.

## Kaggle submission
On Kaggle, the notebook reads the competition test file from `/kaggle/input/...` and
writes `submission.json` to `/kaggle/working/`. `arc_prize_submission.py:main()` auto-
detects the input path. No internet/API is used (rule-compliant).

## Honest scope
- Coverage is modest (~10% ARC-AGI-1); this is intentional — the contribution is the
  **reliability layer** (0 confident-error), not raw coverage.
- Coverage plateau is documented (hand-coded DSL ceiling; needs learned DSL — future work).
- All numbers are reproducible and were independently audited during development
  (see `RAKSHANEX_phase*_results.md`).

## Citation
RAKSHANEX TECHNOLOGIES (2026). "Calibration-Free Consistency-Ambiguity Gating for Safe,
Zero-Hallucination Rule Induction on ARC-AGI." ARC Prize 2026 Paper Prize submission.
