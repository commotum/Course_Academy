# Template and bank extraction

The exact per-source record, complete original options and field identities are in `source.json`; the fixed rendered strings are retained by the generator. `source-replay.json` compares every supported option and the complete correct designation, separately from mathematics and grading.

q-10291 observes a=3, b=2 in f(x)=x^a+x^(-b)-x. Each summand has coefficient magnitude one. It asks for the first derivative in a single radio field `selection`. The solution states the sum rule, differentiates the three individual terms, applies power rules with explicit exponent subtraction, then simplifies negative powers into a reciprocal. Domain: real x != 0. Proposed bounds a=2..6, b=2..4 are an explicit exponent extension, not observed bounds. b=1 is excluded because the observed doubled-coefficient distractor would collide with the correct answer. No constant factor is introduced into f.

Let P=a*x^(a-1), R=b*x^(-b-1). The correct answer is P-R-1. The bank at the observed parameters contains:

| Source answer UUID | Complete recipe | Interpretation |
|---|---|---|
| 211bb0e5-3c78-5407-abe6-d36a7702b7f1 | a*x^a-R-1 | positive exponent not reduced |
| 2b721848-7e95-5033-9e18-09f6e8945fa2 | a*b*x^(a-1)-R-1 | observed altered positive coefficient; psychological interpretation unresolved |
| 32dca761-7920-51b0-b217-36a70a04fd20 | P-R+1 | sign of linear derivative reversed |
| 3f86bddf-d4bf-5ed2-9add-a90b0f3b1200 | P+R-1 | sign of reciprocal derivative reversed |
| ecf3d45d-887f-583c-a917-8a37435d41c4 | P-R-1 | correct |

These five recipes comprise one complete source profile; none is pooled with other banks. The altered coefficient a*b is a labeled extension inferred from the observed 6=3*2, not a claim about the source author's intended error mechanism. Complete bank replay must reproduce 5/5 options, 4/4 distractors at a=3,b=2.

q-339462 observes a=5 in f(x)=x^a+cuberoot(x^4). It uses two positive power functions, one whole-expression blank and no distractors. Its canonical value is a*x^(a-1)+(4/3)*x^(1/3), delimiter-free. The solution converts the cube root to power 4/3, applies each power rule, simplifies, and returns the root form in its final row. Proposed a=3..7 is an explicit integer-exponent extension; the fractional term and its notation remain fixed. Odd roots mean real roots. The derivative exists for all real x, including x=0; independent negative-branch checks accompany the positive-symbol algebra checks.

The source prompt, solution sentences, aligned rows, punctuation, field keys, option count and exact notation replay unchanged at source parameters. Parameters alter every linked exponent/coefficient in the prompt, answer bank and solution. Invalid or colliding banks fail validation. Two incomplete moderate structures (square root with a linear term; fifth root with a reciprocal) and the incomplete unrated cube-root subtraction source are captured but excluded. There are no source corrections or mutations.

# Plot extraction and generation

No source contains a graph or diagram. No plots or assets are created; plot rating is none. Stages 5 and 7 have no asset work.

# Finite capability

There are 15 radio and 5 blank mathematical tasks in these documented bounds, including the two original mathematical tasks. Identity and content fingerprints depend on mathematics; seed and choice order create no new task. Unsupported levels reject CLI calls. Requests beyond 20 variants fail with finite-limit; inventory additionally excludes any existing or canonical mathematical task.
