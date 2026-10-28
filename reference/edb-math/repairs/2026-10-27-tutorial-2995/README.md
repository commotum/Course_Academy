# Identity-matrix tutorial 17592186101961

Compared the current tutorial with Math Academy tutorial 2995 in the archived lesson 1171. All six matrices match the source cell-for-cell, and independently evaluating the nine expanded product entries returns the stated matrix A. All 22 formulas render.

The visible defect was the general identity rule: Markdown blockquote markers were passed into MathJax, producing `> A·I_n = I_n·A = A >`. These are valid TeX relation symbols, so the broken presentation generated no MathJax errors. This Markdown-container failure was outside the earlier structural equation signatures.

The importer had emitted a quoted display formula by T127. The prose normalizer subsequently moved its closing display delimiter outside the quote by T2857. The UI protected math before Markdown parsing and preserved the interior quote markers as mathematical symbols.

Updated `ui/math-protection.js` to remove exactly the enclosing Markdown quote depth from math continuation lines. Nested quotes, genuine greater-than signs and unquoted equations are preserved. Updated `normalize_prose` to keep quote markers outside TeX and retain the closing delimiter inside its quote. Six JavaScript protection tests and 33 formatting tests pass.

Committed one exact-CAS content repair at **T8976**, restoring the quoted closing delimiter. No matrix entries, equations, IDs, links or learner records changed. Native preview and exact committed readback passed; see [verification.json](verification.json).

The current UI serves these files from disk with revalidation, so reloading the lesson loads the renderer fix. [Baseline](baseline.png) and [repaired rendering](after.png) show the difference. [Source verification](source-verification.json) records the independent matrix checks.
