# Native determinant mnemonic

**Superseded:** The user chose faithful source replication. The original illustration is restored by the [follow-up transaction](../2026-10-26-restore-determinant-source-diagram/README.md); the earlier equation repairs remain. This folder retains the history of the native reconstruction, not the desired final representation.

Replaced the remaining raster diagram in tutorial **17592186060931** with authored display LaTeX, committed at **T8086**. The preceding formula-recovery repair intentionally retained this illustration; this follow-up removes that image reference from the tutorial content.

The replacement preserves the four colored matrix entries, determinant fences, crossed blue/red diagonal cues, and matching colored `det(A) = ad - bc` expression. It uses the existing MathJax `enclose` extension; no UI dependency or rendering code changed. Both diagonal strokes are solid in the native version.

The exact image occurrence was replaced once, with all other tutorial content preserved. An old-value CAS guarded the transaction. Native speculative validation, exact receipt datoms, and committed readback passed. The actual UI renderer produced zero MathJax errors, two native diagonal strokes, and zero image elements; the rendered diagram was visually inspected. Answer entities and learner history were untouched.

See [LaTeX source](diagram.tex), [rendered diagram](diagram.png), [transaction](transaction.edn), [render verification](render-verification.json), and [commit verification](verification.json).
