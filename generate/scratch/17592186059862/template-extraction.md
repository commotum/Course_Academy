# Source extraction and fidelity exceptions

q-1214: f(x)=6x^6, radio selection, values 36x^7, 36x^6, 36x^5, 42x^7, x^5. Unique mathematical derivative 36x^5. Complete profile maps respectively to cn*x^(n+1), cn*x^n, cn*x^(n-1), c(n+1)*x^(n+1), x^(n-1). Every value reproduced at c=6,n=6. Mistake interpretations are inferred, not shown to learners.

q-272: f(x)=4x^3, radio selection, values 12x^2, 12x^3, 24x, 7x^2, 4x^4/3. Unique derivative 12x^2. Complete profile maps respectively to cn*x^(n-1), cn*x^n, cn(n-1)*x^(n-2), (c+n)*x^(n-1), (c/n)*x^(n+1). The final recipe's interpretation is unresolved; it preserves the exact observed divisor n, without replacing it by a more plausible integration mistake. All values reproduced at c=4,n=3.

q-10289: rated easy, f(x)=4x^6, no captured fields. Its solution uses derivative -> factor constant -> power rule cn*x^(n-1) -> simplify. Canonical e-138 supplies shared wording and four-line layout. Generated radio solutions reuse that exact fixed prose and sequence; missing source radio solutions cannot be replayed. No new blank layout is inferred for easy.

q-142993: rated moderate blank field-1, answer 1/(3sqrt(x)); missing function in prompt. Worked solution explicitly differentiates (2/3)sqrt(x)+3. It mislabels the derivative f rather than h and uses dy/dx as an operator. Generated inputs restore the expression from this evidence and consistently use g and d/dx. Preserve the six-line sum/constant/power rule sequence. No distractors added.

q-167561: rated moderate blank field-1, answer 1/sqrt(x); missing defining g(x), excess captured whitespace. Solution differentiates 2sqrt(x)-1. Generated input restores this definition, normalizes irrelevant whitespace and corrects dy/dx operator. Replay both blank answers and source coefficient/constant combinations exactly.

Sampling is an explicit bounded extension: integer c=2..12,n=2..9 for easy, rational c=k/3 for k=1..36 and source constant 3 for moderate. Source -1 is replayable. Easy candidates with c+n=cn are rejected as equivalent choices. No signed/fractional easy or other root exponents are claimed. Candidate recipes are tested as entire banks; profiles never mix. Only power coefficient/exponent or root coefficient establishes a new mathematical problem. Source constants, profiles, seeds and order do not inflate inventory.

Missing metadata and omitted prompt content are fidelity exceptions, not full literal source replay. Full five-option mathematical source-bank coverage is required and verified for both supported radio profiles. Blank answers, accepted equivalent fractions, incorrect entries, deterministic regeneration and all bounded candidates are checked with SymPy and the actual application grader. No original content or learner history is repaired here.

Plot extraction/generation: not applicable; no assets. Instances include repository generator version, SymPy dependency version, seed, parameters, profile, domain and source IDs, outside EDB question representations. Identity uses stable KP-derived UUIDs and field-owned answer UUIDs. Existing generator identity will be reused if present at preparation.
