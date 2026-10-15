# Extracted templates and recipes

source-components.json records every rated question, exact original matrices,
field keys, answer shapes and original correct values. source.json retains
complete original Markdown, every choice and worked-solution stage. The six
radio banks are implemented separately in bank(profile, matrices), including
every option, without merging or selecting distractors from a pooled list.
source-bank-replay.json establishes full mathematical-object equality at original
parameters, including correct designation. Blanks have no distractor profile.

Fixed backbone: the source expression and matrix dimensions; supplied and
requested roles; the distributive factorization; the sparse or scalar identity
simplification; final multiplication; field count and field types; source
instructional prose and ordered solution stages. These constraints preserve the
method and workload. Exact matrix components are dependent data. The source
solution is a parameterized template: all matrix occurrences are mapped to the
supplied matrices, their sum/difference, or the final product. Scalar identity
coefficients remain the observed values for that profile.

Variable slots: entries of the common matrix preserve original zeros and
rational/radical forms while multiplying each nonzero by a signed integer in
{-3,-2,-1,1,2,3}. This conservative same-method extension preserves exactness,
sparsity and the factorization. For q-319890 the common E21 stays fixed (its
row-selection role is the method); the active first row of the summed matrix
varies instead. Its radical difference is chosen from sqrt(2), sqrt(3), sqrt(5),
sqrt(7) minus the original corresponding entry. This retains cancellation and
three-term row multiplication. Other summands remain original parameters, a
narrower policy which avoids adding cancellation complexity.

Table blank positions can vary over all cells of the same number-form role
(zero, rational nonzero, radical), without replacement, preserving each field's
workload. All supplied entries, keys and final solution derive from one product.
q-138783 requests every 2x2 entry, so all four roles remain fixed. Source replay
uses original positions. Coverage records sampled positions and explicit
changed-target checks with the matrices held constant; stale answer keys fail.

Radio recipes, in source option order (F is common matrix, I identity, J reverse
identity, Z zero):
q-42263: F,-F,Z,-2F,-I.
q-130269: first row (F23,F12,F13), second row F's first row, third row F's
third row; F; J; I; Z. The first recipe's psychological interpretation is
unresolved; the observed entry mapping is explicit and retained.
q-75635: -2F,2F,Z,F with centre replaced by 4,4F. The centre replacement's
interpretation is unresolved; it is the observed constant-4 pattern, not a
claim about a learner misconception.
q-130259: F12,F22 placed in cells (2,1),(2,2), others zero; Z;
F12,F22 scattered into cells (1,2),(2,2); F's first row placed in row 2;
F's second row placed in row 2.
q-130275: 5J; F with diagonal multiplied by 5;
[[F11,5F12,5F13],[F21,F22,5F21],[5F31,F32,F33]];5F;-5I.
The third recipe preserves its compound source entry mapping, without claiming
a simpler systematic error.
q-75612:3F,Z,diagonal(3F),-F,F.

Reject a bank if any objects collide or a distractor equals the answer. Seed,
UUID and choice ordering are excluded from task fingerprints. Different source
banks cannot collide in identity. Never claim seed-only changes are fresh.

The canonical SVG is unchanged mathematical notation. Practice templates have
no plots, so stages 5 and 7 require no generated assets. Source notation and
prose remain intact, with normalized matrix whitespace and compact blank table
markup; replay fidelity and exact mathematics are reported separately.
