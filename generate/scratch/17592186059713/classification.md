# Classification at frozen basis 1356

Database `math`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The unchanged captured wrapper is `source.json`. Four practice questions, not the canonical example, form the fidelity denominator.

| Source | Captured level | Rendering mask | Fields/bank | Solution | Plot |
|---|---|---|---|---|---|
| q-1300 / 17592186233382 | easy | lower-case overset-arrow sum | attribute absent | 3 aligned rows | none |
| q-1324 / 17592186233395 | easy | upper-case overset-arrow sum | attribute absent | 3 aligned rows | none |
| q-1323 / 17592186060028 | attribute absent | historical arrow subtraction | radio, selection, 5 choices; correct ref absent | attribute absent | none |
| q-1386 / 17592186060041 | attribute absent | historical arrow scalar multiplication | radio, selection, 5 choices; correct ref absent | attribute absent | none |

There are four observed rendering masks, three mathematical families (the two sums differ only in letter case), and two observed complete banks. Easy contains two observed fieldless masks. Assigning the unrated single-operation questions to easy is an authored workload decision; raw public replay retains the omitted difficulty. Moderate and hard have zero observed practice templates and no inferred observed labels. Completed learning versions use the observed radio type, selection key, five math choices and one fixed solution. Raw replay keeps fieldlessness and every absent correct ref/solution.

## Widget and anomaly evidence

Read `/home/jake/Developer/MA/DATA/Lessons/244/Source/244.json` in full relevant question sections. Its final widgets q-1386 and q-1323 are multiple-choice, five choices, and match every captured EDB value independently of their order. Neither widget includes a captured correct indication or worked solution. Thus the source banks are retained and mathematical correct values are inferred only in the separately completed assessment: q-1323 is ⟨3,5⟩ and q-1386 is ⟨24,-21⟩. The owning capture does not include q-1300 or q-1324; its observed radio widgets support an explicitly authored five-choice completion, not a recovered original field. `raw-replay.json` and the public `raw-q-*` profiles preserve omissions; normal records label authorship and contain correct refs.

The decoded prompt strings were inspected using `ord(char)==92`: q-1323 and q-1386 have zero backslash characters; q-1300 and q-1324 have eight each and no adjacent backslashes. Therefore there is no claimed doubled-escape repair. The historical `v^(→)` serialization is preserved in evidence. Normal subtraction and scalar prompts use the actually observed, well-formed `\overset{\to }{v}` arrow notation. This is a notation normalization, not a mathematical correction or a change of vector representation. Normal sums reproduce their source prose and compact aligned stage sequence exactly at original parameters.

## Scope and levels

Follow the captured activity's `first-step` 17592186060584 through `next`: introduction → component form (59710) → angle/column tutorial → angle-bracket KP (59711) → column KP (59712) → common-notations tutorial (60589) → this KP (60590). Collection order was not used. The prerequisite topic is 1165, Two-Dimensional Vectors Expressed in Component Form. The common-notation tutorial explicitly permits arrow/vector labels; it cautions that hats often indicate unit vectors, so no arbitrary hat/unit-vector demands are added.

The canonical example has a+6b with a=(-3,2), b=(4,5); the earlier sibling column example already contains 2a-(b-5c). The authored extension stays with integer componentwise addition/scaling of two-dimensional vectors under arrow labels. No graph reading, dot/cross product, magnitude, direction, geometry, symbolic coordinates, fractions, extra dimensions, or another KP's representation is assessed.

Easy normal questions use one two-component sum or one nonunit scalar multiplication. Coordinates lie in -9…9; scalar magnitudes are 2–6 with either sign. Every complete bank must have five distinct values, with displayed component magnitude at most 120. Normal sampling covers both observed sum masks and the complete operation-derived scalar source bank. Historical subtraction is excluded from learner generation; raw replay retains its complete bank and missing attributes.

The prior moderate two-scaled-vector and hard nested-three-vector extensions are excluded. They introduce new operations and solution stages beyond the observed practice backbone. The canonical example includes graph extraction and a+6b, but does not provide an interchangeable source practice template/bank at a rated difficulty. Therefore moderate and hard are unsupported in this bounded package, with five-question reserves explicitly unfilled. New practice evidence can reopen either decision. No absence-only inference is used.

At the live recheck, basis 2193 has the same four source records, no registered generator, zero usable easy stock and an unclassified job. Classification source details above retain their original basis. Commit preparation rechecks source facts again under api.lock and records its own basis. `capabilities.json` and `validation.json` supersede the prior broader package's generation eligibility.
