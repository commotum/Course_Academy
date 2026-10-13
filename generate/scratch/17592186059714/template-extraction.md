# Vector-magnitude extraction

Source basis 2064; lineage and complete original identities are retained in source.json. Every source question remains unchanged in the database.

## Specific originals

q-1325: `If $v = ⟨4,-1⟩$, then what is the magnitude of $v$?` followed by the scientific-calculator blockquote; `requires-calculator=true`. Positive first and negative second integer components; sum of squares 17, irreducible radical. One `selection` radio field, five math choices; correct key, difficulty, and worked solution absent.

q-18046: `Let $a = ⟨ - 12, 3⟩$. Find $\mid a \mid$.` and the same calculator blockquote/fact. Negative first and positive second integer components; sum 153=9*17, simplified magnitude 3 sqrt(17). One `selection` radio field, five math choices; key, difficulty, and solution absent.

q-18047: `Let $a=⟨5,9⟩.$ Find $|\,a\,|.$`; easy. Formula, signed coordinate substitution, squared integers, sqrt(106), with no simplification. Fields absent; original response format unresolved.

q-18048: `if $a=⟨-4,8⟩$, then  what is the magnitude of  $a?$`; easy. Formula, substitution, 16+64, sqrt(80), sqrt(16*5), 4 sqrt(5). Fields absent; original response format unresolved.

Canonical e-4297: `Let $\mathbf{a}=\langle -4, 6 \rangle$. Find $\mid \,\mathbf{a}\, \mid$.` Formula, substitution, 16+36, 2 sqrt(13). No fields. Used only for solution support and distinctness exclusion.

## General pattern and component mapping

Compute the nonnegative Euclidean norm of a nonzero vector with two signed integer components. The source method is sqrt(x²+y²), with exact radical simplification. This is direct formula use; no angles, projections, dimension changes, symbolic coordinates, or new prerequisites occur.

Each complete bank remains a separate profile. `templates.json` maps every original choice to its source UUID/field, source value, squared value, parameterized recipe, and reproduced value. Correct designations are derived from the prompt and checked independently; there is no original designation to replay. Distractor intent is unknown and is not presented to learners.

| Template | Source vector | Original bank, in observed order | Positive-scale recipe |
|---|---|---|---|
| q-1325 | (4,-1) | 5, 3, sqrt(17), sqrt(5), sqrt(7) | k times each entire observed value |
| q-18046 | (-12,3) | 3 sqrt(19), sqrt(152), 3 sqrt(15), 3 sqrt(17), sqrt(157) | k times each entire observed value |

At k=1 all five values and their notation reproduce exactly. The original bank count is retained. The unique correct options are sqrt(17) and 3 sqrt(17), respectively; the other four differ by their squared values. No guessed component-error recipes, literal distractors held fixed at changed vectors, pooled banks, or bank mixing are used.

## Reusable templates and bounded extension

Fixed: each complete source's wording, variable, magnitude notation, calculator notice/fact, field type/key, choice count, and bank profile. Variable: vector coordinates become k times source coordinates; answers become k times complete source values. Domain: k positive integer 1..8 (q-1325) or 1..3 (q-18046). Optional: final simplification line when sqrt(sum) simplifies. No plots or assets; plot extraction/generation stages are vacuous and rated none.

Observed scales: 1 only. Proposed sampling: 1..8 for q-1325, 1..3 for q-18046, explicitly an authored homothety extension, preserving the signs and number of components. Max coordinate size 36. This remains two integer squarings, addition, square root; the source calculator allowance is retained. No empirical misconception intent is inferred from a sparse bank. The mathematical generalization is instead proven by norm(kv)=k norm(v) for positive k. Distinctness and incorrectness of every option are preserved by multiplication by nonzero k.

Original radio worked solutions are absent. Authored completion uses the fixed sentence `Using the formula, we have` and the canonical/rated easy sequence: formula, parenthesized signed substitution, squared components, square root of the sum, optional simplified radical. The generator does not claim original solution-text fidelity. Missing fields on q-18047/48 are neither repaired nor copied into generated content.

Generate 11 profile/scale pairs. Deduplicating by exact squared norm leaves 9 distinct tasks: q-1325 scale 3/6 collides with q-18046 scale 1/2. Equal magnitudes, even from differently signed coordinates or another bank, do not create another available exercise. Original practice and canonical tasks are excluded before committing. The local catalog has a finite limit; changing a seed, UUID, profile, or choice order does not bypass it.

Full replay: 10/10 source options, 8/8 distractors, 2/2 complete banks; no unmatched/extra choices. Preserve original evidence for authored repairs. Native grader checks every option of every bounded variant. Boundary, deterministic replay, negative-input rejection, rendered solution arithmetic, and corrupted-key/answer/solution rejection are checked independently in validate.py.
