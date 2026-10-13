# Affine equation classification templates

Each equation has the form `a*x+b=c*x+d` over the reals. `source-cases.json` records all original integer quadruples, variables, template assignments and difficulty provenance. `source.json` preserves every original field, value, prompt and solution. `review.md` presents each complete source replay beside changed-coefficient variants.

| Source | Variable | Ordered coefficient/constant quadruples `(a,b,c,d)` | Ordered mathematical status | Solution sequence |
|---|---|---|---|---|
| q-287964 | x | (2,0,1,1); (2,1,2,1); (2,1,2,3) | unique x=1; identity; contradiction 1=3 | spaced prompt; one reduction sentence |
| q-288058 | x | (4,-2,4,3); (3,4,3,4); (5,0,2,6) | contradiction -2=3; identity; unique x=2 | spaced prompt; one reduction sentence |
| q-288066 | u | (-3,4,-3,-1); (2,5,2,8); (6,-2,3,1) | contradiction 4=-1; contradiction 5=8; unique u=1 | cancellation, coefficient equation, division |
| q-288070 | y | (-4,2,-4,-5); (6,3,6,-1); (5,-7,2,1) | contradiction 2=-5; contradiction 3=-1; unique y=8/3 | cancellation, coefficient equation, division |
| q-288072 | z | (2,-4,2,1); (5,6,5,6); (3,2,1,4) | contradiction -4=1; identity; unique z=1 | cancellation, coefficient equation, division |
| q-288073 | w | (3,2,2,2); (4,-7,4,-7); (6,5,6,9) | unique w=0; identity; contradiction 5=9 | cancellation directly isolates w; no division row |
| q-288074 | v | (9,-5,4,2); (2,3,2,7); (5,-1,5,-1) | unique v=7/5; contradiction 3=7; identity | cancellation, coefficient equation, division |

The shared instructional purpose is to distinguish inconsistent equations from identities and equations with one real solution. The required response is an independently checked finite subset of three labeled equations. The answer is not the value of the uniquely solved variable.

Fixed components are the opening question, the select-all instruction, three Roman labels, their field keys, and the boolean response banks. Variable components are the common variable name and the four integer coefficients/constants for each equation. Zero constant terms and unit coefficient numerals are omitted; signs are rendered consistently. The summary-spaced template uses spaces around binary operations and equals signs; detailed templates preserve the compact source notation.

For equal coefficients, subtract that common variable term from both sides, leaving `b=d`. Equal constants give an identity; unequal constants give a contradiction. For unequal coefficients, subtract `c*x` and `b` from both sides, giving `(a-c)*x=d-b`; the exact solution is `(d-b)/(a-c)`. The detailed-scaled template shows this coefficient equation and division; detailed-unit requires `a-c=1` and omits the redundant coefficient row. The summary template renders each result in its source prose sequence and requires one contradiction and one identity. One fixed worked solution is built per instance from the same parameters as the prompt and correct fields.

Every current field bank has the observed pair of literal text values `false` and `true`. These are authored checkbox states, not numerical error distractors. Each source value is mapped explicitly in `choice-mapping.json`; the correct recipe is `a=c and b!=d`. Full source replay matches both values and their correct designation for every field. The original number of fields, field keys and field-owned answer shape are preserved.

Observed bounds are coefficients -4 through 9 and constants -7 through 9, including zero constants, repeated constants, repeated coefficients, and rational final solutions. The sampling policy extends signed nonzero coefficients and constants to [-9,9] on either side; this is an explicit same-demand extension. It samples only the four observed ordered status patterns UIN, NIU, NNU and UNI. Input fractions, distribution, nonlinear equations and unobserved difficulties are excluded from this version. Source-bank fidelity and correctness are reported separately in `validation.json`.

Task fingerprints normalize variable names and common integer scaling of both complete equation sides. They retain the ordered mathematical coefficients and constants. Source and canonical fingerprints are excluded when selecting new production. Seeds, IDs, answer ordering and changing only the variable name do not create inventory. No finite total capability claim is inferred from the demonstrated 100-task batch; each request is bounded to 1,000 candidates and fails rather than padding with duplicates.
