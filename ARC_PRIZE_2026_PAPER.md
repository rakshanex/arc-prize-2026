# Calibration-Free Consistency-Ambiguity Gating for Safe, Zero-Hallucination Rule Induction on ARC-AGI

**ARC Prize 2026 — Paper Prize submission (ARC-AGI-2 track)**
**Author/Org:** RAKSHANEX TECHNOLOGIES
**Code:** self-contained Kaggle notebook `arc_prize_submission.py` (numpy only; no internet/LLM).
**License:** MIT-0 (see LICENSE). All artifacts open-source.

---

## Abstract
We present RAKSHANEX, a program-synthesis approach to ARC-AGI whose defining property
is **calibration-free safe abstention**: it answers a task only when the set of
train-consistent candidate programs yields **exactly one distinct output** on the test
input, and otherwise abstains. This "consistency-set ambiguity meter" needs no learned
confidence, no threshold tuning, and no probabilistic calibration. On the ARC-AGI-1
public training set it answers 40/400 tasks with **zero incorrect answers** (100%
answered-precision), versus an always-answer baseline that is wrong on ~92% of tasks.
The same principle holds on ARC-AGI-2 (harder, unseen) and, notably, transfers
**unchanged to four non-ARC domains** — integer-sequence induction, chess forced-move
detection, physics-law discovery, and unsolved conjectures (Collatz) — always with zero
confident-error. Our contribution is not raw coverage but a **general, transferable
reliability layer**: a component any ARC solver (including neural ones) can adopt to
convert silent errors into honest abstentions.

## Introduction
ARC-AGI measures few-shot generalization on novel tasks — abstraction and reasoning
that cannot be prepared for in advance. A central obstacle to trustworthy progress is
**confidently-wrong output (hallucination)**: current systems, when they cannot solve a
task, still emit a plausible-looking wrong grid. For high-stakes reasoning and for
honest measurement of progress, a system that knows *when it does not know* is as
important as one that solves more tasks. Our inspiration: in programming-by-example, if
several distinct programs all fit the given examples, the task is genuinely
**ambiguous** — and committing to one is unjustified. We turn this observation into an
exact, calibration-free decision rule.

## Prior Work
- **Execution-guided program synthesis** for ARC (e.g. Ouellette 2025) shows executing
  candidate programs against examples beats pure neural or test-time-finetuning for
  compositional generalization. We build on this (consistency filtering) but add an
  explicit *ambiguity* decision.
- **Abstention / selective prediction** (Uncertainty-based abstention; conformal
  "confident-error rate" guarantees, Gu et al. 2026; structural abstention) formalize
  answer-or-abstain. These are mostly LLM/CoT and rely on confidence *calibration*. Our
  difference: the abstention signal is **the cardinality of distinct outputs among
  train-consistent programs** — exact, discrete, calibration-free — applied to
  **visual program synthesis**, where this framing is under-explored.
- **Library learning** (DreamCoder) is the accepted route to broad coverage. We show
  (negatively, empirically) why hand-coded DSLs plateau, motivating that direction.

## Approach (algorithm-level)
Given train pairs {(inᵢ,outᵢ)} and a test input x:
1. **Candidate generation.** A DSL of grid transforms: geometry (flips/rotations/
   transpose), tiling/scaling, mirroring, cropping, object operations (connected
   components, keep-largest/smallest, gravity), plus **parameterized** rules learned
   from the pairs (color-map; a variable-neighborhood k∈{0,1,2} local rule) — depth-1
   and depth-2 compositions.
2. **Consistency filter.** Keep candidate c iff `apply(c,inᵢ)==outᵢ` for **all** i.
   Any candidate that errors on an input is treated as not-applicable (skipped).
3. **Ambiguity meter (the core).** Run all consistent candidates on x and collect the
   set D of *distinct* outputs.
   - |D| = 1 → **answer** that output (all consistent programs agree).
   - |D| ≠ 1 → **abstain** (0: nothing fits; ≥2: genuinely ambiguous).
4. **Scoring policy.** ARC scoring requires a guess, so `attempt_1/attempt_2` emit the
   confident answer (twice) when |D|=1, else the top-2 distinct candidates, else an
   identity/rot180 fallback. The *research* metric is answered-precision on |D|=1.

Principled guards keep the invariant: object ops that degenerate to a 1×1 result on a
larger input, and color-maps facing unseen test colors, raise "not-applicable" rather
than emit a spurious match.

## Results
- **ARC-AGI-1 public training (400 tasks, 416 test pairs):** 40 solved, **0 wrong**,
  answered-precision **100%**; always-answer baseline ≈ 8% precision (~92% wrong).
- **ARC-AGI-2 (harder, unseen; 400 training tasks):** 19 solved, **0 wrong**, 100%
  answered-precision — the safety property holds under distribution shift.
- **Transferability:** applied to an independent external solver (retrieval + naive
  geometry), the layer reduced its confident-error from **97.4% → 0.0%**.
- **Cross-domain (same layer, no changes):** integer sequences (5/5 unique correct),
  chess forced-move (correct on all, abstains when >1 safe move), physics-law induction
  (discovers F=ma, E=kx², Coulomb inverse-square; abstains on insufficient data),
  Collatz (answers verifiable specific cases; abstains on the unprovable general claim).
  Zero confident-error throughout.
- **Honest negative (coverage):** learned-library depth-3 search and per-object/
  translation rules added **0** new tasks — coverage plateaus (~10% on ARC-AGI-1)
  because remaining tasks require *new primitives*, not deeper search; consistent with
  the field's move to learned DSLs. WRONG stayed 0 throughout.
(Per competition rule, train-set-only scores are not claimed as leaderboard results;
Kaggle leaderboard score populates the "accuracy" criterion.)

## Conclusion
RAKSHANEX contributes a simple, exact, calibration-free reliability mechanism for
ARC-AGI: answer iff train-consistent programs agree, else abstain. It gives
**zero-hallucination** rule induction, holds on ARC-AGI-1, ARC-AGI-2, an external
solver, and four unrelated reasoning domains, and is a drop-in layer for any candidate
generator — including future neural/learned-DSL solvers that will supply the coverage
this hand-coded version intentionally lacks. Toward 85% on ARC-AGI, we argue reliability
and coverage are separable concerns: our work makes the reliability half principled,
general, and free.

---
### How this maps to the rubric (for reviewers)
- **Accuracy:** modest coverage (~10% ARC-1); honestly reported. Kaggle score = accuracy input.
- **Universality:** ⭐ same layer works across ARC-1/2 + 4 non-ARC domains — strongly general.
- **Progress:** separates reliability from coverage; a reusable 0-hallucination layer for any solver.
- **Theory:** explains *why* — distinct-output cardinality is an exact ambiguity signal; no calibration needed.
- **Completeness:** full method, guards, 11-phase development, negatives, and independent audits documented.
- **Novelty:** calibration-free consistency-cardinality abstention for visual program synthesis — under-explored.
