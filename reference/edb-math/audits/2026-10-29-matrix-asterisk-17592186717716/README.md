# Matrix asterisk provenance check

Read-only live review at math basis T11487 on 2026-10-29.

Question 17592186717716 is generated, moderate, UUID 0241b95f-2b75-5cc3-97c9-9862fe4bf540. It belongs to KP 17592186115226, Calculating a Matrix Product Using the Distributive Law. It has no Math Academy source ID; its prompt follows the generated record builder in `reference/edb-math/repairs/2026-10-27-linear-algebra-audit/group-2/generator-17592186115226.py.txt`, lines 43–49: nonrequested cells default to `\ast`; supplied numerical entries are an explicit alternative.

All 21 imported practice questions and the canonical example were reviewed. None uses an asterisk to mark an unrequested entry. Nine practice questions use partial 3x3 answer matrices and supply actual numerical values in noninput cells. Nine use whole-matrix radio choices. Three request all four entries of a 2x2 matrix.

Examples: q-275515 (17592186292858) supplies six entries and requests three; q-275518 (17592186292859) does the same, including supplied radical values; q-319917 (17592186299807) supplies five zero entries and requests four entries.

Thus selecting only some cells has imported precedent, but substituting asterisks for the remaining values is a generator-authored presentation choice. The underlying distributive-law structure is source-supported: this question has C−A=−3I, so BC−BA=−3B. No generator or database records were changed.

Full captured question, canonical example, and imported records are in evidence.json. Imported layouts describe their current database representation.
