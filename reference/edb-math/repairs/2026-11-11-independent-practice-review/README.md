# Independent-practice question and generator repairs

Completed and independently read back at **math EDB basis 14220**. Two gpt-6.1-sol agents with high reasoning implemented the repairs; a third performed a source-first independent review, and the primary agent inspected the changes, actual mobile views, publication paths and final database state.

| Scope | Stored repair | Future generation |
| --- | --- | --- |
| Normal-line KP `17592186092240` | Repaired 11 authored prompts: five supplied assessed work and six used the awkward coefficient-dot layout. Includes reported question `17592186710391`. | Registered immutable package `2dad35d505965ce58f224701b7f4ca5db306cc23475610593ecb06f7f76b9908`. Easy questions require differentiation and normal-slope recall; coefficient blanks use labeled equations. |
| Vector KP `17592186235285` | Repaired reported question `17592186735164`. Its clean grid shows only the original vectors; auxiliary path, length and direction reasoning now appear in the solution. | Registered immutable package `61c2af93a404592ba4e52ae454bbf307eefacb918697db13dc1dfb6087486e12`. Easy practice has no supplied auxiliary construction. Outward label placement keeps the original vectors distinguishable. |

Both replacement packages have verified easy, moderate and hard approvals and package-bound refill checks for the repaired behavior. Registration added **zero questions**. Existing question IDs, owned fields, answer keys and learner records are preserved. Both old immutable packages remain intact.

The audit covered all **63 stored questions** in these pools. All **34 imported questions** are unchanged. The 12 other authored vector questions were already free of this scaffolding and remain unchanged. Question `17592186757021` (Gaussian elimination) is unchanged in its entirety; its echelon-only endpoint is supported by imported questions in its KP.

## Verification

- Normal: 90 actual delivered survivors across all bands; 584 native accepted/wrong-response checks including the 11 repaired stored questions; 72 actual player presentations. Seven generated UI representatives exactly match delivered survivor JSON; all 11 stored renderings match committed content. Independent checks covered another 108 mathematical instances and 18 refill controls.
- Vector: 36 actual delivered survivors across all bands; native controls on survivors and the repaired stored question; deterministic relocated outputs and referenced image bytes. Final UI evidence covers 24 actual delivered presentations and four stored-question presentations. Independent checks covered 54 mathematical instances and 30 refill controls. A label ambiguity found in review was corrected before approval; evidence from earlier assets was superseded.
- Primary-agent final readback confirms the exact 12 changed question IDs and permitted attributes, imported content and Gaussian preservation, both current registrations, immutable package bytes and all three approval bands. Five independently inspected mobile screenshots retain matching byte identities.
- Validation exposed a missing production plotting dependency. Restored `matplotlib==3.11.2` and declared it in `pyproject.toml`/`uv.lock` so environment synchronization preserves it. Dependency consistency, lockfile consistency and actual plotting passed. Concurrent unrelated project/CLI work was preserved.

These are scoped content and generator repairs; no general generator campaign or service setting was changed. The checks establish the repaired cases and sampled behavior, not empirical difficulty calibration or universal absence of future defects.

## Evidence

- [Primary-agent final live verification](live-verification.json), [visual review](root-visual-review.json), [runtime verification](runtime-verification.json)
- [Independent source-only checkpoint](source-only.json), [normal review](normal-independent-review.json), [vector review](vector-independent-review.json)
- [Normal implementation, receipts and evidence](../2026-11-11-normal-independent-practice/README.md)
- [Vector implementation, receipts and evidence](../2026-11-11-vector-independent-practice/README.md)
