# Extraction and bounded variation

The backbone is an indefinite integral of c(ax-b)^n for easy, or c(b-ax)^n with a>0 for moderate/hard. Substitute the complete affine base u, differentiate to obtain the signed reciprocal slope in dx, substitute both the function and differential, move constants out, apply the positive-integer power rule, simplify, back-substitute, then perform the source's complete chain-rule derivative check. Every ordered row and both shared instructional paragraphs come from the corresponding complete source template. Render a single concrete solution, independent of learner selection.

Only b is a sampling slot: a positive builtin integer from 1 through 80 inclusive. It is the constant magnitude in the linear base, not the arbitrary integration constant. Replace the entire original inner expression atomically in the prompt, substitution, full bank, every solution row and derivative check. This changes the translated polynomial being integrated. Slope, exponent, outside scale, operation count, sign/order of the base, response type, complete bank coefficients and row sequence remain fixed per profile. Fixing those components preserves every source bank recipe and workload rather than inventing arithmetic or new stages. Source b values remain directly replayable. No option shuffles, prose variants, C aliases or profile aliases count toward capacity.

The selected complete profile determines every option. templates.json contains source-specific problem, solution, ordered bank and key. bank-extraction.json maps every captured value, normalized value, coefficient and coefficient ratio to the correct primitive, retaining the original field/answer IDs and source ownership. The coefficient recipes are exact fixed rational coefficients multiplying the same shifted base to power n+1; their b dependence comes entirely from that base. The two incomplete legacy banks are retained separately, including q-12493's different distractor exponents, and cannot be selected as learning profiles.

| Profile | Grade | c | signed slope | n | observed b | correct primitive coefficient |
|---|---|---:|---:|---:|---:|---:|
| q-113486 | easy | 48 | 3 | 7 | 2 | 2 |
| q-113492 | moderate | 6 | -3 | 2 | 5 | -2/3 |
| q-113503 | moderate | 9 | -2 | 8 | 3 | -1/2 |
| q-113502 | moderate | 18 | -5 | 5 | 2 | -3/5 |
| q-72424 | moderate | 16 | -2 | 7 | 7 | -1 |
| authored-hard | hard, authored | 11 | -7 | 8 | 3 anchor | -11/63 |

Hard has no observed difficulty evidence. Its explicit authored calibration uses the q-113503 negative-slope n=8 sequence, changing the integer outside coefficient and integer slope to obtain an irreducible rational final coefficient. It adds no operator, branch, field, or solution stage. The lesson tutorial's general formula c/[a(n+1)] and canonical substitution/derivative check support it; the named prerequisites are the Constant Multiple Rule for Indefinite Integrals and the Chain Rule for Differentiation. The larger denominator is arithmetic practice within the same method. Its grade is an author calibration, not an observed MA claim.

All expressions are polynomials on the entire real line; there are no roots, logarithms, denominator-variable restrictions, or disconnected real branches. Primitives are compared modulo additive constants. Pairwise choices must have different derivatives, so C changes never create unique distractors. The source keys are mathematically correct and banks have no equivalent primitive duplicates. Doubled backslashes before legacy fraction commands are a capture typography error: source.json and raw API preserve them exactly, while normalized references and served learning values use canonical TeX. No mathematical source correction was necessary. Missing legacy keys/ratings/solutions remain missing in reference APIs.

Capacity is exactly easy80, moderate320, hard80 under this deliberately narrow domain. Each b gives a distinct translated polynomial; moderate backbones differ in degree or leading coefficient. Independent captured profiles, alternate banks and wording aliases are deduplicated by the expanded actual integrand. Hard and moderate n=8 differ in leading coefficient. The finite universe is modest and transparent; no claim is made that the subject itself is finite or that varying slopes/exponents has been implemented.
