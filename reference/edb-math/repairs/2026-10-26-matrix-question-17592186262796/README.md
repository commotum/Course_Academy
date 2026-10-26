# Determinant matrix spacing and lesson completion

Completed 2026-10-26 using the EDB and q-completion skills. Scope: topic **152**, “The Determinant of a 2x2 Matrix,” containing **79 question records (76 practice questions and 3 canonical examples)**, three KPs and one introductory tutorial. Initial reads are pinned to **T8122**.

## Reported question and cause

Question **17592186262796** is imported Math Academy **q-127578**, not a generated question. Its earliest retained assertion at **T90**, attributed to `:org/Math-Academy`, already contains:

```tex
|\begin{aligned}5 & -9 \\ -3 & 7\end{aligned}|=
```

All four entries are present, and the correct answer is **8**. An `aligned` environment alternates right- and left-aligned equation columns without the matrix column spacing. Thus the first row visually resembles `5−9` and the second `−37`, while the literal bars fail to stretch around the two rows. This is a layout defect, not a lost entry or incorrect determinant. The later T5780 change only moved the expression into display math.

The historical MathML renderer maps a generic unruled `mtable` to `aligned`. Its old formula-rendering path did not subsequently normalize the enclosing matrix/determinant fences. A minimal original-shape MathML reproduction produces the same problem. The repaired formula uses `vmatrix` and retains all four entries unchanged. [Before](target-before.png) and [after](target-render/after.png) screenshots show the difference. Both representations have zero MathJax syntax errors: successful typesetting alone did not establish readable matrix layout.

## Committed changes

**T8127** repairs **103 mathematical blocks in 58 content fields across 45 questions** (33 imported and 12 older generated records). It changes fenced alignment tables to the corresponding actual matrix environments, preserving the ordered cells, arithmetic, original question markers, answer values and links. Genuine aligned derivations remain aligned. Changes comprise 13 problems and 45 worked solutions. [Preparation](format/preparation.json), [transaction](format/transaction.edn), and [verified receipt/readback](format/verification.json).

The structural review also found five incomplete practice questions. **T8129** completes them:

| Question | Completion |
| --- | --- |
| 17592186059981 / q-1088 | Added a worked solution and linked the existing correct choice `3\sqrt{2}-5`. |
| 17592186060000 / q-11648 | Added a worked solution and linked existing choice `6`. |
| 17592186060001 / q-11651 | Added a worked solution and linked existing choice `k = 9`. |
| 17592186060195 / q-19801 | Added a worked solution showing the repeated root `t = 3`, and linked existing choice `3`. |
| 17592186233379 / q-127614 | Retained its complete worked solution and added one mathematical blank for its unique answer `x = 4`. |

These solutions and the new blank are authored completions based on the displayed problems and matching canonical teaching templates; they are not claimed as recovered source interaction metadata. Existing choice banks, answer values, entity IDs, difficulties and learner history remain unchanged. The fieldless practice question received a new owned field/answer with stable UUIDs. [Template/derivation evidence](completion/template-evidence.json), [transaction](completion/transaction.edn), and [commit verification](completion/verification.json).

The introductory tutorial and its original determinant illustration are unchanged by either transaction.

## Verification and prevention

- Independently computed determinants and, where applicable, unique unknown values for **all 79 questions/examples** from their displayed ordered 2×2 matrices. Every existing designated answer agrees; all four newly linked choices agree uniquely. [Exact-math results](final-independent-math.json).
- Actual application `learning::grade_field` checked all **76 practice questions**, accepting 76 correct submissions and rejecting 202 incorrect submissions with zero unresolved results and no database writes. Radio checks cover every choice. [Native grading](native-grading.json).
- Rendered all **403 final lesson content/answer fields**, with zero MathJax or page errors. The reported question was visually inspected after repair. [Final render](final-render.json).
- Speculative native EDB validation and exact readback passed. The completion receipt contains exactly 20 intended datoms, including the transaction timestamp. Final readback at **T8129** verifies all 79 records, 76 complete practice fields, preserved answer identities/values and difficulties, and the unchanged tutorial. [Final verification](final-verification.json).
- Patched `scripts/import_historical_question_content.py` to run the existing source-TeX normalizer on the **complete formula**, after its fences are available. This retains equation alignment while converting fenced matrices to actual matrix environments. Two new regressions, three historical multistep tests and 27 shared math-format tests pass.
- Verified all three currently registered immutable generator packages. **94 fresh records**, covering every supported template/level at two seeds, pass independent exact-math and matrix-layout checks; all 188 generated problem/solution fields render without errors. Current generators already use the semantic normalizer, so their packages require no replacement. The malformed generated pool members came from older generators. [Generator checks](generator-check.json), [sample render checks](generator-render/render-verification.json).

No learner attempts, timing, XP, mastery, queue records, existing answer values, or source images were changed to test or apply these repairs.
