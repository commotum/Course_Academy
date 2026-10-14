# Extracted templates and bounded slots

All supported templates assess the same method: slope equals derivative at the specified point; use a supplied or computed derivative, substitute the target, evaluate its terms, simplify, and state the slope. Preserve the one-field contract, exact scalar answer and source-specific differentiation stages. Expression ordering and whitespace are normalized; literal source-layout fidelity is not claimed.

| Source | Original parameters | Fixed backbone | Variable slots and policy |
|---|---|---|---|
| q-167637 | a=3,b=1,c=2,t=0 | k=a eˣ−b x³−c x; supplied k′; blank m; evaluate at zero | a∈2…6,c∈1…5. b=1 and t=0 fixed: b vanishes at the target and changing it alone gives no meaningful new assessment; nonzero targets introduce exponential numerical answers and change the easy workload. |
| q-10742 | a=1,b=6,c=2670,t=3 | a x⁷−b x⁵−c x; power rule and cancellation; radio slope | a∈{1,2},b∈4…7,t∈{2,3}; choose s∈−8…8, c=7at⁶−5bt⁴−s>0. This preserves the source's small exact answer after cancellation. Reject colliding banks. |
| q-1853 | a=3,b=6,t=2 | a x⁴−b x³+1/x; reciprocal-to-power rewrite, power rule, evaluate; radio | a∈2…4,b∈4…7,t∈{2,3,4}. t≠0. Reciprocal numerator 1 is fixed because it controls the source's exact scalar bank profile. |
| q-342107 | a=1,b=4,c=8,d=4,t=−1 | a x⁶−b x⁴+c x²−d; termwise power rule including zero constant derivative; blank m | a∈1…3,b∈3…5,c∈6…8,d=4 fixed (vertical shifts do not change the assessed derivative),t∈{−2,−1,1,2}. Correct the source's opening function identity. |
| q-342937 | a=2,h=2,t=3 | −a x²+1/(x−h)²; reciprocal chain derivative; blank m | a∈1…4,h∈1…3,t∈{2,3,4},t≠h. Fixed unit shift scale and numerator preserve derivative stages. |
| q-342942 | a=2,b=7,c=6,t=3 | a x⁴−b x³−c x²−1/x; termwise derivative; blank m | a∈1…3,b∈5…7,c∈4…6,t∈{2,3,4}. Reciprocal sign and numerator fixed to preserve source method. |

Observed values are the Original column; every proposed range is a bounded same-method generalization, not inferred empirical source coverage. All parameters occur in the curve, derivative, evaluation, answer or bank. Full source originals are in source.json; source-replay.json compares every supported complete bank, independent of choice order. The correction and context restoration are explicit and are never applied to existing sources.

q-342107's constant d does not affect slope, so it stays fixed at 4. Content deduplication uses the derivative as the assessed mathematical object and also excludes vertical shifts found in existing questions. Likewise easy b stays fixed. For all families deduplicate the derivative and target rather than identity, seed, option order or integration-constant-like vertical shifts.

## Complete choice banks

q-10742: s=7at⁶−5bt⁴−c. Original complete bank {4,5,3,−5,−3} corresponds respectively to {s+1,s+2,s,−(s+2),−s}; s is correct. All four distractors replay exactly. Offsets and sign recipes preserve observed mathematical values; the underlying learner mistakes behind offsets are unresolved. They are not presented as feedback.

q-1853: P=4at³−3bt², D=t², N=DP−1. Original s=95/4, N=95, D=4. Original bank {95/3,95/2,93/4,95/4,97/4} corresponds to {N/(D−1),N/(D−2),(N−2)/D,N/D,(N+2)/D}; N/D is correct. Each complete rational value replays, with no missing or extra distractor. D−1,D−2 must be nonzero; all values must differ. Error interpretation is unresolved beyond the observed numerator/denominator offsets. Profiles are never pooled or mixed.

Blanks: q-167637→1; q-342107→−6; q-342937→−14; q-342942→−80/9. Preserve numeric fragments rather than equations or extra fields. Grader validation accepts exact equivalent fractions and rejects wrong values.

## Plot extraction and generation

No source images, graph references or parameter-dependent diagrams occur. Plot rating none for every supported template. No assets generated; asset hash set empty.
