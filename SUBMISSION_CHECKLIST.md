# RAKSHANEX — ARC Prize 2026 Submission Checklist & Timeline

Org: RAKSHANEX TECHNOLOGIES · Track: Paper Prize (linked to ARC-AGI-2)

═══════════════════════════════════════════════════════════════════

## KEY DATES (from arcprize.org/competitions/2026)
| Date | Event |
|---|---|
| Mar 25, 2026 | Competition started |
| Nov 2, 2026 | **Code submissions due** (Kaggle) |
| **Nov 8, 2026** | **Papers due** ← our target |
| Dec 4, 2026 | Results announced |

Aaj (~Sep 17, 2026): **~7 weeks / 52 din bache.** Time kaafi hai.

═══════════════════════════════════════════════════════════════════

## WHAT'S READY (is package mein)
- [x] Self-contained Kaggle solver: `arc_prize_submission.py` (numpy only, no internet/LLM ✓ rule-compliant)
- [x] Paper (rubric format): `ARC_PRIZE_2026_PAPER.md`
- [x] Open-source license: `LICENSE` (MIT-0 ✓ required)
- [x] Submission README: `SUBMISSION_README.md`
- [x] Full reproducible research trail + independent audits

## WHAT YOU (user) MUST DO MANUALLY
Ye main aapke liye nahi kar sakta (account/identity + external sites chahiye):

1. **Kaggle account** banao (free): kaggle.com
2. **Competition join karo:** "ARC Prize 2026 - ARC-AGI-2" (aur "Paper Track")
   - kaggle.com/competitions/arc-prize-2026-arc-agi-2
   - kaggle.com/competitions/arc-prize-2026-paper-track
3. **Notebook banao Kaggle par:** `arc_prize_submission.py` ka code ek Kaggle notebook
   mein paste karo. Wo `/kaggle/input/...` se test file padhega, `submission.json`
   `/kaggle/working/` mein likhega. "Submit" dabao (Code submission, before Nov 2).
4. **Open-source karo:** code ko public GitHub repo mein daalo with `LICENSE` (MIT-0).
   (Rule: leading participants must open-source to be eligible.)
5. **Paper submit karo:** `ARC_PRIZE_2026_PAPER.md` ko PDF banao (koi bhi md→pdf tool),
   aur Paper Track par upload karo, apni Kaggle code submission se link karke (before Nov 8).

## PRE-SUBMIT CHECKLIST
- [ ] Kaggle notebook runs end-to-end, writes valid `submission.json` (format verified locally ✓)
- [ ] No internet/API calls in notebook (verified: pure numpy ✓)
- [ ] GitHub repo public + `LICENSE` (MIT-0) present
- [ ] Paper PDF: author = RAKSHANEX TECHNOLOGIES (+ aapka naam jo daalna ho)
- [ ] Paper links to the Kaggle submission
- [ ] Submitted before deadlines (code Nov 2, paper Nov 8)

═══════════════════════════════════════════════════════════════════

## HONEST EXPECTATIONS (main sach bolta hoon)
- **Top Paper ($75K):** bahut competitive (SOTA teams). Realistically hamari coverage
  (~10%) ke saath ye mushkil hai.
- **Outstanding Papers Pool ($375K, rubric ≥4.5):** yahan hamara best shot hai —
  hamari **universality (6 domains), theory, novelty** strong hain. Par ye bhi
  guarantee NAHI — judges ka discretion hai.
- **Sabse realistic value:** ek real, open-source, published research artifact aapke
  naam par; feedback; credibility; aur seekhne ka experience. Paisa **possible** hai,
  **guaranteed nahi**. Koi bhi "pakka jeet" kahe to galat.

## AGAR COVERAGE BADHANI HO (optional, prize chance badhane ke liye)
- Learned/neural DSL (GPU chahiye — Kaggle/Colab free GPU se try). Ye bada kaam hai,
  par accuracy criterion aur solve-rate seedha badhata hai. 52 din mein basic version
  possible, par uncertain.

## BOTTOM LINE
Package **submission-ready** hai. Aapko sirf Kaggle/GitHub par upload + paper PDF
banakar submit karna hai (steps upar). Deadline door hai, quality par focus kar sakte
ho. Ye ek honest, real, paisa-potential raasta hai — bina kisi jhooth ke.
