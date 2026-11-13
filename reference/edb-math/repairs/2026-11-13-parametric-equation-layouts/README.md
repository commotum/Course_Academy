# Parametric equation layout repair

Reported question: `17592186640734` (`q-236989`), in **The Parametric Equations of a Line**.

The prompt used a fixed-width 350px HTML table with a three-row-spanning interval cell. Production rendering clipped the interval after the answer control. This is an equation layout, not a data table. The previous matrix-specific normalization required matrix notation and did not cover these coordinate-equation rows. The November 11 table census retained this item as `other_table`; it was outside that matrix candidate set.

Repaired eleven matching questions in the lesson (nine Markdown tables and two HTML tables). Each now uses the existing borderless, braced equation-system layout, with its parameter interval underneath. All supplied expressions, field keys/IDs, correct answers, worked solutions, and other question attributes are preserved. The repair is committed at basis 14454 using compare-and-swap guards.

`scripts/question_capture/math_format.py` now normalizes this narrow x/y(/z) + t-interval pattern during import, for both HTML and Markdown, with code protection, duplicate-marker rejection, and idempotence. It leaves ordinary data tables untouched.

Verification: 54 math-format unit tests passed, all eleven unanswered question layouts rendered through the unmodified learning UI at 1100×900 and 390×844 (22 passing cases), and database readback at the committed basis confirmed that only question/problem changed. `before.png` and `after.png` show the reported question. The rendering smoke test alone passed the old clipped table; visual inspection was needed to identify its lost interval.
