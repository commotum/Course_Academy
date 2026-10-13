# Complete source-bank extraction

source-cases.json describes every original specifically: exact prompt, source rating, field and answer IDs, field key/type, every original answer, complete symbolic expression, worked solution when present, and supported/excluded status. source.json retains full source strings and correct designations, including two equivalent canonical aliases in blank q-350904. No source option is dropped or mixed with another bank.

The shared supported move is denominator substitution followed by integration of a logarithmic quotient. q-113997 additionally rewrites (u-1)/u as 1-1/u. Families remain separate for prompt structure, solution sequence and response type:

| Source | Substitution | Factor | Transformed integrand | Bounds | Response |
|---|---|---|---|---|---|
| q-49557 | sin(x) | 2 | 1/u | indefinite | five-option radio |
| q-113998 | csc(x)+2 | -2 | 1/u | indefinite | five-option radio |
| q-350887 | sin²(x)+3 | 1 | 1/u | 0 to pi/2; u=3 to 4 | exact blank |
| q-350901 | 8cos³(x)+5 | -1 | 1/u | pi/3 to pi/2; u=6 to 5 | exact blank |
| q-350904 | csc(x)+2 | -1 | 1/u | pi/6 to pi/2; u=4 to 3 | exact blank, two retained canonical aliases |
| q-73674 | sin(x²) | 1/2 | 1/u | indefinite | five-option radio |
| q-113997 | tan(x)+1 | 1 | 1-1/u | indefinite | five-option radio |

Observed amplitude m=1 is replayed exactly, including original variable names, Markdown, complete bank, field layout, and six existing solutions. Sampling is deliberately narrower than all possible trig quotients: positive integer m=2..12 multiplies the source integrand and every complete bank expression by m. It preserves the substitution and workload. This is an explicit transport policy; error intentions remain unresolved rather than inventing new misconceptions. Constants of integration remain arbitrary. The source-cases records carry a complete parameterized expression for every supported option; the recipes do not copy literals across unrelated families.

For variants, fixed instructional sentences retain substitution, differentiation, transformed integral, antiderivative and back-substitution; definite questions additionally retain the limits table, endpoint evaluation and final exact value. All values derive from the same exact SymPy instance. q-49557 has no source solution, so that fixed solution is authored. The original q-113997 solution absorbs a constant into K; generated answers use C and the solution retains an equivalent antiderivative, differing only by an arbitrary constant. Fidelity of m=1 and authored variant wording are reported separately.

Domains: connected real intervals excluding trig poles and denominator zeros. Log absolute values are used for indefinite antiderivatives. sin²+3 is at least 3, 8cos³+5 at least 5 on its stated interval, and csc+2 at least 3 on [pi/6,pi/2]. All definite logarithm arguments are positive. The defective q-10045 and q-10046 banks are explicit exclusions; no supported source-bank comparison is unresolved.

Identity and novelty depend on the parsed variable-normalized integrand, exact bounds, full source bank profile and field layout. Seeds and choice order cannot make a new mathematical task. Existing practice and canonical tasks are excluded from selection; original entities/history are never revised.
