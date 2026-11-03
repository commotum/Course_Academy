# Inverse reciprocal function notation

Applied at math **T12355** on 2026-11-03. The lesson is topic **17592186049402**, “Differentiating Inverse Reciprocal Trigonometric Functions,” covering KPs **17592186115398–17592186115401**.

Reported question **17592186247132** is imported **q-110510**. Its problem and solution stored `arccscx` as plain letters. Other imports stored undefined joined commands such as `\arcsecx`, or bare powered names such as `{arcsec}^{2}`. MathJax can render the plain-letter form without an error while displaying six italic variables rather than a function name.

The original saved source contains complete named MathML nodes such as `<mi>arccsc</mi>` and `<mi>arcsec</mi>`. The conversion did not consistently preserve their operator role, particularly for names not covered by standard TeX commands or an application-marker rule. `source-evidence.json` retains the source path, hash and actual neighboring nodes. No source archive was edited.

All **61 questions/examples** were audited: **33 imported practice questions**, **24 generated practice questions**, and **4 canonical examples**. The 24 generated questions already used proper inverse operator notation. The repair changed **37 imported questions/examples**, **67 answer values**, and **one tutorial**: **135 text attributes** in total. Existing question, field and answer identities, correct links, difficulty, pool membership, generator registrations and learner history were preserved.

Every changed question passed the actual learner UI, including upright operator glyph checks; four representative questions also passed a 390px phone preview. The reported question was visually checked after repair. The retained before-preview demonstrates both failure modes: plain italic letters without a parse error and an undefined legacy macro.

The follow-up [database-wide repair](../2026-11-03-operator-notation-database/README.md) fixes the same defects elsewhere and extends prevention to the shared import/publication paths. Its live verification checked every complete practice question in this lesson: **50 questions and 150 grading checks**, with no saved attempts. Seven partial imports were preserved without inventing missing keys.

Evidence: `capture.json`, `source-evidence.json`, `audit.json`, `proposals.json`, `render-verification.json`, `extractor-verification.json`, and `verification.json`. `publication/` retains the exact CAS request, receipt and full readback. `build.py`, `render.py`, `deploy.py`, and `check-extractors.cjs` reproduce the work.
