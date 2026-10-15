# Template extraction

## 1. Original descriptions

classification.md identifies each source's exact numerical roles and field contract. source.json retains every original prompt, complete bank, key, and full solution. choice-ledger.json maps all70 original choices to field and answer IDs, source parameters, explicit symbolic recipes, rendered recipe values, and complete-value replay comparisons. Each bank remains a separate source profile; no pooled distractor selection is used. The recipes' algebraic patterns are observed; psychological interpretations are not asserted.

Two defects are retained separately. In q-31395, ln4·log_4²(x)/2 and ln2·log_4²(x) are identical incorrect choices. In q-210752, ln2·ln|log_2(x²)| and ln2·ln|log_2(x)| differ by the constant (ln2)² on x>0,x≠1 and both are correct primitives. source-errors-and-repairs.json retains the generated original bank and supported single-choice sign repair. Raw captured text is never overwritten.

## 2. Shared pattern and purpose

Let L=log_b(a x^m), r=(k/d)ln(b)/m. The integrand is (k/d)L^n/x. Easy has a=m=1,n∈{1,2}; moderate has a=1,m∈{2,3,4},n=1; hard has m=1,n=-1. Substitute u=L, use du/dx=m/[x ln(b)], rearrange dx/x=ln(b)du/m, then integrate r u^n. The primitive is r u^(n+1)/(n+1)+C, or r ln|u|+C when n=-1; finally substitute L back.

## 3. Components and profiles

The source prompt is an indefinite integral followed by an equals sign. Each field is radio, key selection, five math answers, one key. The shared worked-solution sentences are “Let u=… . Differentiating, we get” and “Using the above, we can write the integral in terms of u and evaluate:”. The ordered mathematics is the substitution, derivative, reciprocal differential, split original integrand, u integral, constant extraction, primitive, and back-substitution. q-31395 adds the source's simplified u primitive before back-substitution. q-210781 retains its coefficient inside the split integrals before extracting it. Source and changed solutions preserve these stage sequences; notation is canonicalized mathematically, rather than replaying a literal captured payload.

All profiles select their entire expression list before parameter sampling. bank()/recipes() in the generator provide the explicit operation sequence for every option; the ledger stores each symbolic expression with b,a,m,n,k,d slots. This includes compound mistakes such as ln(x^b)·ln|log_b(a x)|; x ln(b)·ln|log_b(x^a)|; ln(a)·ln|log_b(x)|; altered bases b−1,b−2,b−3; and common log base10 inside another logarithm. No opaque observed expression is replaced by a plausible misconception. Repaired profiles are explicitly authored complete banks and never counted as extra source banks.

## 4. Slots and constraints

b is an integer2…9. A profile using b−2 as another base requires b≥4; b−1 requires b≥3; b−3 requires b≥5. a is a positive integer1…5 in scaled hard profiles; the unscaled hard profiles keep a=1 because that whole bank uses the unscaled argument subcase. m is1 for easy/hard and2…4 for moderate. n is1 or2 for easy,1 for moderate,−1 for hard. The n slot is sampled in the source power-family q-114020; the other easy source profiles retain their power1 bank subcase. Independent outer numerator k∈1…4 and denominator d∈1…3 preserve the observed small integer/rational workload. c=k/d and r, all keys, all dependent solution values and all bank options are derived from one instance. Equivalent k/d spellings do not create distinct mathematical tasks.

All original parameter tuples remain accepted in their observed profiles. The bounds extend observed small-number roles conservatively; they introduce no different integral operator, response shape, limits, new function family, integration method or instructional progression. Changing the hard scale includes a=1 and uses exactly the same substitution stages. Changing moderate m includes odd/even cases already present in the source, so the original real-domain distinctions are preserved.

For odd m, x>0; for even m, x≠0 and x^m>0, including the negative component. The hard family also excludes a x=1. The result is an antiderivative on each connected component of that real domain, with an arbitrary constant. The generator retains ln|u| and ln|L|; it does not replace them with ln(u), or use forced log identities. Independent comparison uses the real derivative of ln|g|, namely g′/g on g≠0. Whole profiles with duplicate/equivalent answers are rejected; documented erroneous originals are retained only as ineligible evidence.

Variation checks cover every source profile, two changed samples per profile, two separately authored repairs, and30 fresh batch tasks. Actual task identity is the canonical printed integrand and real domain, independent of seed, option ordering, profile, or field-bank content. Full content identities additionally distinguish banks. The CLI returns a JSON list; difficulty all,count1 returns exactly three records. Builtin integer seed/count checks and a bounded count guard reject malformed or oversized requests.

Parent QA narrowed each supported repair to one source choice: q-31395 fourth option becomes its negative; q-210752 first option becomes its negative. The other four original recipes and original correct designation stay intact. Normal source-parameter repair instances therefore preserve68/70 source choices, while all70 raw choices remain available as separately labeled evidence.
