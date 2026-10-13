# Classification

Snapshot: math, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is the unmodified capture wrapper. Nine practice questions: eight easy, one moderate; no unrated or fieldless originals. All use one radio field, key `selection`, five text choices. No plots or image assets occur; plot rating is **none** for every family.

| Level | Source | Template | Assessed operation |
|---|---|---|---|
| easy | q-140631 | power_easy | power derivative; false exponent/coefficient assertion; substitute ny/x |
| easy | q-141078 | exp_true | exponential chain derivative; substitute ky; omit redundant substitution row |
| easy | q-141080 | sin_none | reciprocal amplitude and trig chain factor; false derivative and ODE |
| easy | q-141081 | cos_i | cosine chain derivative; compare derivative with cosine squared |
| easy | q-141082 | log_all | logarithmic derivative; exponential/log cancellation |
| easy | q-141084 | inverse_none | signed negative power derivative; denominator-power substitution |
| easy | q-141086 | exp_none | signed exponential derivative; unequal ODE coefficient |
| easy | q-141088 | log_scaled | outer log scale; divided exponent; six ordered substitution rows |
| moderate | q-141089 | power_moderate | nonunit signed coefficient; explicit coefficient-times-power-rule row |
| hard (authored) | none | affine_log | affine log chain derivative; divided exponential substitution |

These are separate presentation/value templates because the derivative and substitution sequences differ. The categorical bank profiles are separately identified by `<source-id>_bank`; `masks.json` gives every complete bank profile. `source-cases.json` assigns all nine originals to explicitly raw `raw_<source-id>_bank` evidence profiles; their unprefixed counterparts use normal interval wording. No source question is omitted.

The lesson route, reconstructed from `:activity/first-step` and `:step/next`, is introduction (17592186101706), this KP (17592186101707), checking multiple proposed solutions (17592186101812), then initial value problems (17592186101795). Pull array order would put the last two in the wrong order. The introduction explicitly teaches derivative/substitution and defers solving ODEs. This generator checks one function and never solves an ODE or applies an initial condition.

The canonical e-525 checks 1/x in y'=-y/x using the same three statements. Key prerequisites are power differentiation, introductory ODEs, exponential chain differentiation, logarithmic differentiation, and trig chain differentiation. Hard is an authored difficulty claim: replacing x by bx+c in the observed scaled-log/exponential substitution introduces the nonunit inner derivative and an affine positive domain, while keeping one proposed function, one derivative claim, and the same substitution/conclusion operation. It does not adopt the sibling KP's multiple-function or IVP demands.

## Source teaching-domain repair

The common opening in the canonical example and every practice worked solution says to satisfy the ODE for every x in the equation's domain. For the logarithmic cases the proposed function has a smaller interval of definition; the ODE RHS does not impose that x restriction. The actual ordered lesson introduction supports derivative/substitution verification and does not require extending a proposed function outside its domain. Normal solutions therefore make the smallest wording correction: satisfy the equation “for all values of $x$ in an interval where the function is defined and the equation is valid.” Normal `log_all` prompts explicitly state x+h>0, and `log_scaled` prompts state x>0; hard already states bx+c>0. No derivative/substitution stages or banks change.

All nine original prompts and complete solutions remain byte-exact through the public parameterized raw profiles. Raw records carry `evidence_only=true`, `eligible_for_learning=false`, and `raw_evidence_profile=true`. Normal records carry the opposite flags and list their wording/domain repairs separately. This is a source teaching-wording anomaly, not an algebraic bank correction.


## Current classification at basis 2001 (2026-10-13)

The live math lineage is unchanged. All nine practice questions now have three checkbox fields, keys I, II, III; each owns the complete two-value text bank false/true and one correct value. This supersedes the historical radio-field classification above. Eight sources remain easy and q-141089 remains moderate. The nine mathematical/presentation templates and their plot ratings (none) are unchanged. Every original worked solution remains unchanged in the database; source prompt changes only label the three statements and request selection of all applicable statements. Current exact EDN is retained in reference/initial/kp.edn. The nine prompt/solution replays, all 27 complete field banks, 54 values and 27 correct designations pass validate-current.py.

The moderate family retains f=a*x^n, y'=n*y/x on x != 0, with the displayed derivative assertion (a-n)*x^(n-1), a=-5..-2 and n=2..5. The case a=-2,n=2 is excluded because its asserted derivative is correct and would alter the observed truth pattern. Fifteen mathematical tasks remain in the bounded domain; seed, IDs, profiles and choice order do not increase this count. Inventory is deduplicated against every current source/practice task and the canonical example, and excludes retained learner presentations and reservations. The source moderate task is already shown, leaving zero available at basis 2001. Only this job's moderate shortage is replenished. Hard remains an authored design with no source rating evidence; no hard inventory is generated or declared filled here.
