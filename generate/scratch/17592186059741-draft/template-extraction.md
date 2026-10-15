# Extraction in four stages

## 1. Specific observed records

q-981 gives A=[-1,-3,8], kA=[-7,-21,56], selects the leftmost element and solves -k=-7. q-69670 gives S=[-9,4;0,8], kS=[63,-28;0,-56], selects top-left and solves -9k=63. q-11442 gives G=[1,0;2,6], kG=[5,0;10,30], with no worked solution, level or correct reference. q-320536 gives B=[11,12;-4,-8], kB=[33,36;-12,-24], selects bottom-left and solves -4k=-12; its first two printed solution matrices incorrectly use +4. q-320551 gives W=[1,0,0;0,4,-3;2,-2,5], kW=[5,0,0;0,20,-15;10,-10,25], selects the third-row leftmost entries and solves 2k=10. q-320563 gives B=[24,-12,6], kB=[8,-4,2], selects rightmost and solves 6k=2. q-139431 gives an increased-bet payoff matrix [0,-6,6;6,0,-6;-6,6,0]; its solution supplies P=[0,-2,2;2,0,-2;-2,2,0], selects top-right and solves 2k=6. Raw prompt lacks P; normal standalone presentation supplies it. The source-cases records contain the full parameterized replay; source.json contains immutable originals including DB identities.

## 2. Shared pattern and instructional purpose

Given M and kM, recover the unique nonzero scalar by equating corresponding nonzero entries, then divide. Expand kM entrywise, equate the resulting symbolic matrix to the supplied product matrix, identify one eligible cell, solve its one-step equation and note that other eligible cells give the same result. A target cell is a solution slot, not an extra assessed demand. Direct radio answers include the complete equation k=value; blanks expect only its RHS. No feedback is added.

## 3. Complete component and bank mapping

`choice-recipes.json` enumerates every source field and complete displayed bank, including the missing original designation. Scalar s is recovered from the supplied pair. q-981's observed ordered bank is [s-3,s,s-1,s-4,s-2]; q-69670 is [s+5,0,s,s+4,s+1]; q-11442 is [s-2,s-3,s,s-5,s-1], in captured order. These are empirical numerical profiles, not inferred learner-error explanations. Raw profiles are publicly replayable at original and changed inputs but always evidence_only=true, eligible_for_learning=false. The zero option remains zero. A collision rejects the whole profile instance.

Normal radio banks are separately authored complete operations on the actual selected corresponding entries a,b: [b/a,a/b,ab,b-a,b+a]. The quotient is computed first; reciprocal division, multiplication instead of division, and subtraction/addition instead of division supply four wrong values. The bank is chosen before parameters; any collision rejects the whole instance. No first-valid distractor pools are used. These banks reflect the actual one-step equation and are never represented as recovered source banks.

Blank banks contain just b/a, rendered as a scalar fragment. The original field types, keys and answer shapes are retained; UUIDs are local content identities owned by the field. No source database IDs are reused.

## 4. Parameterized backbone and constraints

Variable slots: all nonzero matrix entries retain the source sign/zero pattern; nonzero integer source entries have magnitude at most144, product entries integral with magnitude at most864. Normal samplers use entry magnitude1..12 times the scalar's reduced denominator. Scalar domains follow classification.md and apply to explicit parameters as well as random generation. All nonzero cell positions are eligible solution targets. Target changes update the descriptive selection sentence, its two operands and the ordered final aligned equation. Source target phrases remain verbatim at original positions; other positions use explicit row/column language. The payoff family fixes P's zero-sum game matrix and varies positive integral multipliers2..9; its eligible six nonzero cells all have equal workload.

Fixed: supplied pair shapes and names; direct or payoff prompt context; radio/blank field contract; full source prose; entrywise expansion → matrix equation → corresponding-cell equality → scalar isolation → closing note. The canonical example uses a reciprocal scalar and validates this one-step method. No additional algebraic stages are introduced for hard.

Source replay uses exactly the same slot calculation and rendering functions; no branch returns a literal original payload. Raw q-320536 explicitly retains its captured incorrect first two signs and is ineligible. Normal source-shaped output corrects them. Raw q-11442 omits missing attributes; normal supplies an inferred key, authored easy label and source-shaped worked solution. Raw payoff prompt retains its context omission; normal inserts P. All other full original worked solutions reproduce exactly, including matrix cell notation, row counts, shared sentences and final periods.

IDs follow shared normalization of prose, matrices and bare math before hashing and include version, difficulty, prompt, worked solution, full bank and field type. Answer shuffling does not change IDs. Mathematical fingerprints include normalized matrix ratios and scalar, exclude bank/profile/notation, target solution-choice and uniform matrix scaling. They deduplicate equivalent displayed supplied-pair tasks; context availability is retained as an instructional distinction.

Validation reads actual displayed matrix cells into exact fractions independently, checks each expanded matrix and scalar operand, selected-cell prose and both ordered isolation rows, complete normal banks, all original values/correct designation presence and full prose skeletons. Held-data target tests cover every eligible cell; mutation controls corrupt cells, scalar factors, target prose or stages while leaving the final key unchanged. At least100 distinct assessed tasks per normal level and default family coverage are required across160 seeds. Native grading separately checks exact and independently unreduced equivalent fractions and every radio option.

No plots occur; mathematical matrices are formatted with shared matrix_tex rather than raster assets. No plot extraction or rendering dependency is required.
