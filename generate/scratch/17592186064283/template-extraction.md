# Template extraction

The task is to differentiate c T(x)^n by first setting u=T(x), applying d(c u^n)/du=c n u^(n-1), then substituting the trig inner derivative. Source-analysis.json retains each specific prompt, solution, numerical features, variable roles, field keys, and every original answer. contract.json stores source-specific fixed instructional sentences and parameterized Markdown. review.md places originals, exact replay, and variants side by side.

The generator bank(t,c,n) is the executable component mapping below. Set m=n-1 and k=c*n. S=sin(x), C=cos(x). Each row lists the full bank in generated order, beginning with the canonical answer; original order is retained in source-analysis.json. Recipes are observed complete expressions, with learner error interpretations unresolved. No inferred error labels or feedback enter the learner presentation.

| Profile | Observed (c,n) | Full mathematical bank |
|---|---|---|
| cos-unit / q-48385 | (1,4) | -n C^m S; -n S^m; n C S^m; n C^m S; n C^m |
| sin-unit / q-48560 | (1,2) | 2SC; -SC; -2C^2; -2SC; C^2 |
| sin-scaled / q-72154 | (9,2) | kSC; -cSC; -cC^2; kSC^2; kS |
| cos-scaled-a / q-72156 | (5,8) | -k C^m S; -c S^m; c C S^m; -k C S^m; k C^m |
| cos-scaled-b / q-72157 | (4,7) | -k C^m S; -k C S^m; -k S^m; c C S^m; c C^m |
| sin-blank / q-342420 | (1,7) | n S^m C |
| cos-blank / q-342424 | (-4,5) | -k C^m S |

Every complete original bank replays with exact values, count, correct designation, prompt, and worked solution. The two cosine scaled banks remain separate profiles; no bank is pooled or mixed. Blanks have no distractors and preserve the full derivative expression response shape and field-1 placeholder.

All variables are real, and sine/cosine expressions are defined for every x. Powers are positive integers. Bounded sampling is explicitly narrower than arbitrary powers or coefficients: cosine radio n=3..9 (n=2 makes required distractors collide), sine square radio n=2, sine blank n=2..9, positive scaled radio c=2..9, negative cosine blank c=-9..-2. cos-unit c=1 and sin-unit is a singleton (1,2). Unit sine square overlaps the sine-blank task and adds no mathematical novelty. Negative cosine values are observed features, not discarded. No fractional or larger powers, alternate inner functions, or negative sine coefficient extension is claimed.

Fixed components include source sentences, field type/key, and unit trig argument. Variable components are c,n,m,k,-k and all their appearances in powers, coefficients, composite function, derivatives, multiplication, substitution, final line, and answer bank. No plots or optional learner feedback are added. An earlier draft failed to parameterize some signed final coefficients; extract.py now maps both k and -k, and independent rendered-function/solution checks reject that failure.

Distinct tasks use the exact derivative fingerprint of the displayed input function; changing profile, answer shape, identity, seed, or choice order does not create new mathematical inventory. All current practice and canonical sine/cosine tasks are excluded from generation by that fingerprint, including unrated/text-answer sources. A mathematically correct question still needs the actual learner grader: native-grading.json checks all radio choices and canonical, reordered equivalent, wrong-sign, and missing-factor blank entries over the entire bounded domain.
