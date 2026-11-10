# Inline math scrollbar repair

Fixed in the shared lesson/history stylesheet, `ui/learning.css`. The running application serves the updated file (see `live-stylesheet.json`). Reload an already-open page to load it.

MathJax SVG brackets and punctuation can paint beyond the SVG's measured width. Making each inline math element horizontally scrollable therefore created a one-pixel scroll range even for tiny vectors. The repaired style reserves a small trailing paint allowance while retaining horizontal scrolling for genuinely wide formulas. No lesson data, answers, or learner history was changed.

The audit used current database content at **basis 13643**: all **19 topics**, **6,021 visible content fields**, **791 canonical/practice questions**, and **56 tutorials**. It included question prompts, worked solutions, answer options, checkbox labels, and tutorials.

## Verification

- **12,042 desktop/mobile field renders**, at 1100px and 390px, containing **34,086 rendered math nodes**.
- Unnecessary scrollbars: **640 before → 0 after**, across the same content and viewport cases. The issue had appeared in **17 topics**.
- The inventory of **504 genuinely wide formula cases is exactly unchanged**; no new wide-formula scrollbar cases were introduced.
- Zero outer content-card overflows or MathJax errors after the fix.
- **380 focused regression renders** cover the reported vectors and additional punctuation cases, seven font sizes from 14px to 30px, tutorial/choice/feedback contexts, and a genuinely wide inline equation.
- The two reported entities, `17592186088928` and `17592186088149`, were checked visually in saved desktop/mobile screenshots.

The earlier content checks detected mathematical/TeX errors and card overflow but did not reject a short inline SVG's one-pixel scroll range. The new regression checks explicitly detect scrolling on formulas whose SVG already fits.

## Evidence

- [Combined verification](verification.json)
- [Current database snapshot scope](snapshot.json)
- [Before](before.json) and [after](after.json) per-field results
- [Focused regressions](regressions.json)
- [Mobile tutorial screenshot](after-visual/17592186088928-tutorial-content-390.png)
- [Worked solution screenshot](after-visual/17592186088149-question-worked-solution-1100.png)
- Regression tool: `scripts/check_inline_math_overflow.py`

## Per-topic check

| Topic | Unnecessary scrollbar cases before | After |
| --- | ---: | ---: |
| Euler's Formula | 76 | 0 |
| Introduction to Linear Transformations | 44 | 0 |
| Differential Operators | 0 | 0 |
| Linear Differential Operators | 8 | 0 |
| Introduction to Second-Order Linear ODEs | 6 | 0 |
| The Superposition Principle | 2 | 0 |
| Linear Dependence and Independence | 10 | 0 |
| Linear Independence in Abstract Vector Spaces | 0 | 0 |
| Linear Independence of Solutions to Homogeneous ODEs | 30 | 0 |
| Reduction of Order | 6 | 0 |
| Abel's Identity | 4 | 0 |
| General Solutions of First-Order Linear ODEs | 400 | 0 |
| General Solutions of Linear ODEs | 18 | 0 |
| Second-Order Homogeneous ODEs: Characteristic Equations With Distinct Real Roots | 2 | 0 |
| Cauchy-Euler Equations: Characteristic Equations With Distinct Real Roots | 10 | 0 |
| Second-Order Homogeneous ODEs: Characteristic Equations With Complex Roots | 6 | 0 |
| Second-Order Homogeneous ODEs: Characteristic Equations With Repeated Roots | 2 | 0 |
| Cauchy-Euler Equations: Characteristic Equations With Repeated Roots | 10 | 0 |
| Second-Order Homogeneous Initial Value Problems | 6 | 0 |
