# Template extraction

Per-question particulars and every original choice appear in template-components.json with source IDs, exact expressions, field ownership, bounds, substitutions, bank profile, original Markdown and solution. All 32 source values and 24 distractors are accounted for without pooling banks. Six radio source profiles are distinct; blanks have none.

Shared mathematical pattern: integrate A*x^(n-1)*h(b*x^n) using the displayed inner expression as u, or the reciprocal sec-squared variant using u=1/x. The required response is one primitive plus arbitrary C or one exact definite value. This exercises recognizing the derivative factor, retaining its coefficient, and transforming bounds where present.

Fixed components: inner substitution, trig function/product, original bounds, source choice count, field type/key, prompt shape, solution sequence and complete source-bank profile. Variable component: positive outer amplitude multiplier m. Compute the correct primitive from the derivative ratio first; then transport every observed bank expression by m. All literal constants in distractors scale too. m=1 is an exact replay; m=2..12 is a deliberately narrow sampling policy. Arbitrary C remains arbitrary and is not treated as a fixed value.

Every recipe is m times the complete exact source expression listed in the component ledger. At m=1 it reproduces the whole source value. The source expressions are retained as observed patterns; no learner misconception is inferred. A complete bank is selected by source template before any answers are rendered. No choice mixing or source literals left unscaled.

Domains: real connected intervals excluding sec/csc/cot/tan poles and x=0 for reciprocal u. The definite sec*tan interval maps to [0,pi/3], which has no poles. Sine and cosine definite intervals are regular and monotone under positive x-squared substitutions. Positive nonzero m preserves all domain restrictions and bank equivalence relationships.

Source issues: q-13461 has no difficulty, correct marker or worked solution and malformed integral spacing; generated variants use a moderate label, mathematically derived marker, a fixed solution and repaired spacing. Seven supplied source solutions are retained exactly at replay. q-3038 has redundant nested aligned markup; variants use one balanced environment. No source facts are repaired in the database.

Fidelity is separate from correctness: all eight exact source prompts, all source fields/keys, all 32 bank values and seven provided solutions replay exactly. Variant LaTeX is normalized by SymPy and intermediate rows are shortened to substitution, transformed integral, primitive, bound evaluation/back-substitution and final value. This notation/layout normalization is explicit; original prose and evidence remain in the ledger.
