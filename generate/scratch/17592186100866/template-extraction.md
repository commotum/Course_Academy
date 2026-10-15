# Multiplying a 2x2 matrix by a column vector

Source capture: math basis 2655, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Exact source fields, prompts, solutions and every choice mapping are in template-extraction.json.

The fixed backbone is two row dot products: multiply row one by the supplied column vector, retain its first result while evaluating row two, then display the full two-component column vector. All questions request the entire product. Row and column roles and vector dimension remain fixed because changing them changes the assessed operation or workload. There is no queried-cell slot.

Keep four easy templates separate: named matrix and vector with radio answer, inline product with radio answer, named product with two scalar blanks in a table, and inline product with two scalar blanks in a table. The unrated “What is” template remains evidence-only. Both blank keys denote output rows, independent of source field storage order. Labels vary together throughout named prompts and solutions but are excluded from distinctness.

Slots a,b,c,d are integers in [-11,11]; u,v are signed nonzero integers in [-9,9]. These bounds conservatively extend observed integer inputs, including zero matrix entries, equal vector entries and negative inputs. Sampling does not introduce fractions, extra dimensions, extra operations or new reasoning stages. Matrix labels A,Z,X,H and vector labels x,y,n,a are observed labels sampled independently. Every original parameter is replayed.

Each complete radio bank is selected by source profile before parameter sampling. Reject whole colliding banks. The original author's intended error is unknown: the formulas below are observed-value-preserving generalizations, not claims about cognitive errors. The unresolved irregular bank is withheld rather than inventing its extension.

With A=[[a,b],[c,d]], x=[u,v], r=a*u+b*v, s=c*u+d*v:
- q-13564: (r,s), (-r,-s), (r,-s), (-r,s), (v,u).
- q-126511: (r,s), (a+b,c+d), (-a-b,-c-d), (s,r), (a,c).
- q-13555: (r,s), (r,r), (r,-s), (-r,-s), (-r,s).
- q-13565: (r,s), (-s,-r), (r,-s), (-r,-s), (-s,r).
- q-13629: (r,s), (r+1,s), (r,s-1), (r,s+1), (r-1,s-1).
- q-13560: (r,s), (r+1,s), (s,r), (r,r), (s,s).
- q-126512: original bank only: (1,-2),(10,-12),(-8,6),(-4,4),(-44,14). Underlying errors unresolved; no parameterized normal sampling.
- q-13566: original bank only: (21,12),(21,-12),(-21,-12),(12,21),(19,12). Missing source key and solution; replay evidence only.
- Blanks: field-1=r, field-2=s. Canonical answers remain field-owned.

All generated math is delimiter-free inside answer values. Source radio matrices have double-escaped begin/end commands; generated values use canonical single LaTeX commands. Bank replay compares complete integer vectors after this documented notation correction. Other source defects remain unchanged: q-13564 has duplicate selection fields and a missing key; q-13566 has no difficulty, key or solution.

The parameterized worked solution retains source wording, first-row and second-row accumulated matrix displays, and the final named or inline conclusion. Parenthesize negative factors consistently; the original q-275589 sometimes omits those optional parentheses. This is a notation normalization, not a new stage. Every displayed row expression and resulting vector is independently read back and checked.

Practice matrices are LaTeX, not plots. Canonical example PNGs are matrix notation. Stages 5 and 7 require no generated assets. The generator uses exact SymPy matrices. Slot coverage includes all sampled integer values, labels, signs, zero matrix entries and equal/unequal vector components. Holding coefficients fixed while renaming labels verifies references; mathematical row roles remain fixed.

A content fingerprint ignores seed, identities, option order, labels, response format and source bank. It canonicalizes a simultaneous column/vector-coordinate permutation, preserving output row roles. Existing operands, including the canonical example [1,3;7,-2]*[2,5], cannot become new content by rendering or seeding again.

Moderate and hard have no source-backed templates. Larger numbers alone do not establish a new difficulty, and extra dimensions or operations would leave this KP backbone. Each nominal five-item band remains explicitly unfilled pending new source evidence; this is a bounded package capability exception, not proof that this mathematics can never have harder exercises.
