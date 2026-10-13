# Extracted template

Given `y=c ln x`, ask for dy/dx. On x>0 use (ln x)'=1/x, pull out c, substitute c*(1/x), and simplify to c/x. Keep the four worked rows and fixed explanatory sentences. Blanks append the equation RHS placeholder `{{field-1}}`; radios keep the selection field separate. The immutable source record and `template-extraction.json` retain each prompt, full bank, field, values, supplied solution and mapped recipe.

The observed complete radio profiles are:

- Integer, c=n: `1/x`, `-n/x`, `1/(n*x)`, `x/n`, `n/x`. q-11909 has n=7; q-101604 has n=-9. Each retains five options. The signed reciprocal and reciprocal derivative recipes reproduce complete expressions, not only sign labels.
- Fraction, c=n/d: `n/(d*x)`, `1/(d*x)`, `n/x`, `d/x`, `d/(n*x)`. q-11910 has n=2,d=3. Omitting n, omitting d, using d, and inverting c are observed expression recipes; pedagogical interpretations are inferred.
- Euler multiple, c=n*e: `e/(n*x)`, `n/(e*x)`, `n*e/x`, `n+e/x`, `e+n/x`. q-101600 has n=2. The final two values keep one factor undifferentiated as an added constant, a different complete bank from the integer profile.

Blank canonical banks contain only c/x. q-339941 uses c=-11; q-308849 c=8. q-339949 uses c=11/4 and q-339950 c=-7/3, each with a second equivalent value `n/(d*x)` recorded without explicit multiplication in its original plain notation. Replay preserves both values; default fresh blank output has one canonical value unless the complete equivalent-entry profile is selected. These are not incorrect choices.

Observed c values are 7, 2/3, -11, 2, 2e, -9, 8, 11/4, -7/3; canonical c=5. The missing-field c=2 prompt is evidence only. Sampling uses reduced rational c=n/d, 2<=|n|<=30,1<=d<=12, plus signed integer multiples n*e. This covers all observed complete-bank values. Coefficient and bank arithmetic are exact SymPy expressions. Larger magnitudes, negative legacy fractions and negative Euler multiples are explicit, boundary-tested parameter extensions; c=0, unit numerator, zero denominator and unreduced parameter identities are excluded. The finite set is recorded in capabilities.json. Different field, bank, seed, ID or choice order for the same c still counts as one mathematical question for inventory.

Sampling selects a whole eligible bank before rendering. Integer and Euler profiles require d=1; fractional and equivalent-entry profiles require d>1. Coprimality and |n|>=2 avoid profile bank collisions. Source replay requires equal cardinality, one-to-one matching of complete mathematical values, correct designation where observed, exact prompts and exact supplied worked strings. Missing legacy worked strings are explicitly authored and never claimed as source fidelity. All native blank equivalents and wrong-entry tests must resolve through learning::grade_field.

Plots: none. No source image paths, no generated assets, no publication stage.
