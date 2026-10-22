# Extracted backbones and slots

Each question asks which of three displayed differential equations is Bernoulli,
using independently gradable checkbox fields I, II, III. All fields own exactly
two text answers, `false` and `true`. The current five source banks have 30 total
values and 15 correct designations. There are no inferred distractor recipes or
mixed profiles; each bank is the whole Boolean profile. The exact original
values and owner identities remain in the captured Pull, and component maps
are in `source-cases.json`.

| Source | Derivative multipliers, in order | Supplied left terms | Supplied right terms | Key |
|---|---|---|---|---|
| q-108911 | 1,1,1 | -sqrt(x)y; tan(x)y; -ln(x)y² | x³/y; -sqrt(x)y^(3/2); y⁶ | true,true,false |
| q-108913 | 1,1,1 | x^(-2)y³; -exp(x)y; ln(x)y⁴ | sin(y); x²y⁵; -xy³ | false,true,false |
| q-108914 | 1,1,1 | sqrt(x)y; x²y²; x²y | x²ln(y); xy³; sqrt(x)y^(-1/2) | false,false,true |
| q-108916 | y²,y,1 | -xy⁵; -x sqrt(y); ln(x)y | y⁴; x²; x ln(y) | false,false,false |
| q-108918 | 1,y³,y | -exp(x)y²; ln(x)y⁴; x sin(y) | sqrt(y); sqrt(y); cos²(y) | false,true,false |

These are specific observed components, not an unrestricted differential
equation sampler. Multiplying each supplied left term by A_i and right term
by B_i gives `m_i y' + A_i a_i = B_i b_i`. Six independent scalar slots are
integers 1..5, with original replay A_i=B_i=1. All are positive and nonzero;
source signs remain. This finite sampling policy permits 5^6 coefficient tuples
per template before mathematical deduplication. No global scalar multiplies
the whole equation. A changed coefficient changes the differential equation,
rather than its seed, identity, label, or choice order.

Derivative multipliers, number forms, x-function families, y-exponents and
nonpower functions stay fixed within each template to retain its specific
recognition and normalization workload. Easy radicals remain radicals;
moderate templates retain their two normalization stages. The x powers and
y powers are observed values, not claimed essential properties of every
possible Bernoulli exercise; broadening them is deferred beyond this bounded
policy. The row order is a deliberately narrow presentation policy, not a
mathematical constraint. It is excluded from the uniqueness fingerprint.
There is no requested target-location slot in these recognition questions.

Compute normalized left/right terms by dividing by the derivative multiplier.
Two distinct pure powers qualify when one exponent is 1; either side can supply
the linear term, with corresponding signs moved consistently. Nonexamples
retain two nonunit powers or a sine, cosine, or logarithm of y. Source monomials
are checked symbolically on positive-domain intervals. The independent validator
parses the rendered equations and uses each term's logarithmic derivative to
verify that the exponent is constant.

Solution sequence: state standard form; examine I, II, III; show normalized
equations whenever the derivative multiplier is not 1; identify p(x), q(x), n
for positive examples or the precise obstruction for negative examples; state
the selected labels or none. The source's operative sentences (standard form,
examination, classification, coefficient identification, final selection) are
parameterized together. This is one fixed worked solution for the instance,
independent of the learner's submitted checkboxes.

Fidelity is separate from correctness: all five source equation sets are replayed
at unit scalars and compared as complete normalized equations; every original
Boolean bank and correct designation must match. Rendering intentionally repairs
the source defects listed in `classification.md`; it does not claim literal
Markdown equality. The two incomplete radio sources cannot establish complete
source-bank fidelity or grading and are explicitly excluded, not repaired in EDB.

Stable identities derive from the mathematical normalized equation multiset,
then field key and answer value. Seed, choice order, labels and whole-equation
scaling are absent from the mathematical deduplication key. Existing question
content and canonical examples are checked against the same mathematical form.
