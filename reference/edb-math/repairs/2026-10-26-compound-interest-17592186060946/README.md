# Continuously compounded interest: lesson quality pass

Completed 2026-10-26. Topic **237**, “Continuously Compounded Interest,” has **five lesson steps**: two tutorials and three knowledge points/canonical examples. This pass also covers all **21 practice questions**, giving **24 question/example records**. Initial reads are pinned to **T8153**.

## Reported tutorial and root cause

Tutorial **17592186060946**, MA tutorial **3396**, currently stores the money amounts correctly as `$\$450\,000$` and `$\$563\,545$`. Actual player rendering confirms both dollar glyphs are visible and the surrounding formulas are intact. Its original T35 import contained corrupted legacy currency markers `\[math]` and `\[/math]`. Those were already repaired at **T6150**. The tutorial needed verification, not another content rewrite.

The remaining currency defect in this lesson was **ten imported text answer choices**: values such as `$$7889$` and `$$3.37$ per gallon`. The earliest retained answer assertion already has that malformed encoding. A source currency glyph was left unescaped inside an outer math wrapper, turning the beginning into `$$`. This is source conversion damage, not a shared UI failure to display valid escaped currency.

The legacy upstream Markdown wrapper still reproduced the defect directly: `wrap_math_inline("$3.37")` returned `$$3.37$`. See the [database-wide repair and prevention](../2026-10-26-currency-escaping/README.md).

The generated choices were checked by their actual character codes and rendering: their dollar and percent signs are correctly escaped. JSON's representation of backslashes was initially misread during investigation; those valid generated values and all three registered generator packages were preserved.

## Lesson repair: T8169

- Escaped the literal currency glyph in the ten malformed imported choices, preserving all numbers, units, answer types, IDs, bank membership, and history references.
- Repaired the final line of canonical example **17592186059595 / e-5166**. The source's MathML table column separator had become `\mid`, producing `&= P_0 \mid \approx 9899`; restored the source line `P_0 &\approx 9899`.
- Completed six imported practice questions that had answer banks but no correct link or worked solution. These are authored completions based on the existing canonical method and exact problem data; they are not claimed as recovered source answer annotations.

| Question | Derived existing correct choice |
| --- | --- |
| 17592186060056 / q-1434 | 24 years |
| 17592186060057 / q-1435 | 31% per minute |
| 17592186060058 / q-1442 | 3156 crimes |
| 17592186060059 / q-1445 | 791 people |
| 17592186060238 / q-24145 | $7889 |
| 17592186060389 / q-69937 | $3.27 per gallon |

The transaction changes **17 text attributes** and adds **six correct-answer links**. Its exact receipt contains only the intended 35 datoms including the transaction timestamp. All existing identities, source questions, numeric values, choices and learner history references remain in place. Both tutorials are unchanged.

## Verification

- Independently calculated the expected result for all **24 questions/examples**, accounting for growth/decay, rate/time units, percent conversion, and final-only rounding. Every completed practice bank has exactly one matching choice.
- Actual application grading checked all **21 practice questions**: 21 accepted correct choices and 84 rejected distractors, with zero unresolved checks and no learner/database writes.
- All **155 final lesson text/answer fields** render without MathJax or page errors. Each repaired currency label becomes one complete formula containing a literal dollar glyph. Both tutorials were included.
- Native speculative validation and exact committed readback at **T8169** passed for the full lesson.
- Verified the three active immutable generator packages and **30 fresh records** using the current shared publication validator. No generator package change was needed.

Evidence: [commit verification](verification.json), [transaction](transaction.edn), [completion derivations](completion-evidence.json), [exact calculations](independent-math.json), [native grading](native-grading.json), [final rendering](final-render.json), [generator checks](generator-verification.json), and [reported tutorial rendering](target-after.png).
