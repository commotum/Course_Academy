> Historical extraction retained for the exact observed source banks. Its translation-only production policy has been replaced by the coefficient-role specification in [instructional-account.md](../instructional-account.md). In particular, q-109029 is now generated normally, and numerical coefficients and the qualifying formula are no longer fixed. The original per-choice mapping in template-extraction.json is still used for exact replay.

# Parameterized source banks

The complete specific descriptions, original equations, original worked solutions, every source answer ID/value/designation, and slot dependencies are in template-extraction.json. Every profile maps all five expressions, with four distractors and one key. The recipe is the observed complete expression evaluated at u=x+h; no distractor interpretation or mixed bank is invented.

Fixed components: Bernoulli exponent n, coefficient forms, supplied equation versus rearrangement, field key/type, bank size, Bernoulli recognition, divide by y^n, substitute z=y^(1-n), differentiate, put the linear equation in standard form, integrating factor, integration, recover y. These carry the assessed method and workload. Variable component: the coefficient argument u=x+h, h in {-6,...,-1,1,...,6}. All related mathematical x occurrences change together; derivative coordinates dx, function names such as P(x), and integration prose still use x. No new plots or mathematical operations are introduced.

Observed h=0 is retained solely for exact source replay. Normal generation uses nonzero h and excludes autonomous q-109029. The real coordinate u is positive; denominators are nonzero; Bernoulli division assumes y nonzero. For fractional powers q-109170 and q-109177, y and z are positive. For signed square root q-109028, both nonzero real branches are retained. Constant redefinitions already present in the source are preserved.

Fidelity is checked separately from correctness. Every complete source bank is replayed exactly at h=0, ignoring option ordering only. Independent parsing reads the rendered ODE and each option, derives p,q,n, and verifies the linear residual for y^(1-n). Distractors require a nonzero residual and a numerical witness. Every declared h is exercised; equation fingerprints eliminate unchanged tasks and source equivalents. Radio selection is checked with the actual learner grade_field function.

No source plots appear in these practice templates, so Plot Extraction and Plot Generator require no assets. All source Markdown is retained, and original/changed examples are shown in review.md.
