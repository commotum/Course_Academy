# Template extraction

## 1. Specific observed questions

The exact source payload is preserved in `source.json`; every prompt, worked solution, field, option, and correct-presence attribute is reproduced through public `generate(..., profile="observed-raw", parameters={"n":1})`. `source-cases.json` maps all nine practice sources. `bank-map.json` records every original option separately, including both q-16400 banks and their full expressions.

q-16400 has leading 2, moved cosine coefficient 3, constant 1 and moved sine-y coefficient 4. q-8359 supplies the already isolated derivative (2x-y)/x and requires a quotient split before collection. q-103349 has e^(2x), 2e^x and forcing x. q-103354 divides cosine and uses sin(2x)=2sin(x)cos(x), keeping the uncancelled quotient. q-16396 supplies a common nonzero y and a quadratic y²x term; factoring/cancellation reveals the linear equation. q-79697 has reciprocal derivative coefficient 1/x² and quotient (x+y)/x. q-79699 has 5y², -ye^(-x) times the derivative and forcing y, with y≠0. q-8360 supplies cotangent coefficient 2 and forcing sin(2x) on the left. q-16401 has matching y²cos² terms and the square (1-ycos x)².

## 2. Shared purpose

Write the supplied ODE as derivative + P(x)y = Q(x), using algebra only. The derivative coefficient is exactly one; P and Q do not depend on y. Preserve each family's supplied arrangement and ordered algebraic operations, rather than introducing an integrating factor or solving for y(x).

## 3. Components and complete banks

`bank-map.json` contains the original field IDs, field type/key, full answer fragments, correct presence, original correct ID, and a coordinate-component recipe for every option. A raw profile transforms complete algebraic x components to nx consistently in the prompt, bank, intermediate rows and conclusion. Complete derivatives and formal P(x)/Q(x) labels are protected; bare trigonometric arguments such as sin(2x) become sin(2nx), not a product of sin(2) and nx. n=1 is an ordinary recipe parameter and does not trigger a copied-output branch. No original option is dropped.

This coordinate recipe is a faithful symbolic extension of an observed expression, not an inferred learner-error explanation. Historical bank intention is underdetermined, especially q-16396 and q-79697. All raw profiles are evidence-only and ineligible for learner sampling. The normal `profile=<source-id>` reuses the previous symbolic source-bank patterns; it is also evidence-only because some patterns have opaque intent. The default method-derived bank has explicit, method-grounded wrong operations and is eligible.

Normal complete method banks, selected with the family before parameter sampling:

- q-16400: correct; omit all constant division; omit division of constant forcing only; fail to change moved y sign; fail to change moved cosine sign.
- q-8359: correct; isolate y; leave forcing on left with zero right; leave derivative coefficient x; leave y term on right. All share the same ODE, but only one satisfies strict standard form.
- q-103349: correct; omit division of both remaining terms; reverse both exponent subtractions; omit division of forcing only; omit coefficient 2.
- q-103354: correct; omit dividing by cosine; invert tangent ratio; wrong forcing sign; wrong y coefficient sign.
- q-16396: correct; wrong moved y sign; wrong forcing sign; use x² in the y coefficient; omit y coefficient.
- q-79697: correct; fail inverse multiplication by x²; wrong moved y sign; cancel an extra forcing x; multiply y coefficient by x² rather than x.
- q-79699: correct; fail to invert exponential; wrong y sign; wrong forcing sign; omit exponential multiplication on both remaining terms.
- q-8360: correct; leave forcing on left and y on right; isolate derivative; isolate y coefficient; solve algebraically for y. These ineligible response forms retain the observed complete bank.
- q-16401: correct; omit cross-term factor 2; double it to 4; omit cross term; wrong sign of cross term.
- rational-collect: correct; add rather than subtract right-side y coefficient; wrong moved forcing sign; omit division of forcing; omit division of the collected y coefficient.

There is one fixed worked solution per instance, independent of the chosen wrong option. There is no learner-facing distractor diagnosis. A complete-bank collision rejects the entire instance; explicit invalid parameters raise rather than being silently changed.

## 4. Backbone, slots and bounds

Normal source-shaped samplers preserve positive integer number forms. q-16400: a=2..5, b,c=1..5, h=1..8. q-8359: k=1..8. q-103349/q-103354: frequency n=1..8. q-16396/q-79697: k=1..8. q-79699: k=2..8. q-8360: k=1..8. Hard: a=1..6, b=1..4, n=1..6. Raw coordinate-component slot n=1..8 is explicitly evidence-only. Authored moderate: a=2..8; b,c,d,h=1..8. The moderate prompt is ax y′ + bx y - hx = c + dy; the two coefficients are (bx-d)/(ax) and (c+hx)/(ax). c,d>0 keep both denominator tasks nontrivial. All bounds apply to explicit calls as well as sampling.

Easy variation changes coefficients/frequencies inside each observed operative family; each sampled instance has its family's same rows and operators. Moderate requires two symbolic coefficient divisions after collection and excludes expansion/cancellation. Hard always starts with a quadratic square, explicitly expands the constant/quadratic/cross terms, cancels the matching quadratic term and moves the linear term. Its four row stages are frozen at changed inputs. The family is not reduced to an easy supplied-linear-equation question.

Normal source stage masks preserve quotient split, inverse multiplication, common-factor extraction, uncancelled trigonometric quotient, expansion and cancellation before collection. Annotations occur once; final unannotated rows stay distinct where present in the original. Source shared prose is retained. Normal notation/grouping is normalized and empty source displays omitted; raw-exact source replay is counted separately.

Domain restrictions are attached before CAS cancellation: x≠0 for reciprocal-x and authored moderate; y≠0 for common-y cancellation; cos(nx)≠0 for cosine division; sin(x)≠0 for cotangent. Exponentials have no real zero. Correct coefficients, wrong bank, all rows and final P/Q come from the same exact integer/Rational instance.

Mathematical fingerprints use normalized P,Q, domain and the supplied operative workload. They exclude bank, profile, seed, notation and whole-equation constant scaling. Q's actual coefficients remain meaningful for conversion; changing forcing is not discarded as an arbitrary y-scaling alias. Content identities use actual prompt, fixed solution, difficulty and complete bank. Option shuffling cannot create identity.

Meaningful normal tasks: q-16400 has at most 800 coefficient tuples before common scaling aliases; the smaller fixed-format easy families have 7–8 values each, for 836 distinct normal easy tasks after common coefficient scaling is removed. Moderate has 7·8⁴=28,672 tuples and 27,871 distinct tasks after common scaling aliases, with no additional arithmetic operators. Hard has 6·4·6=144 distinct tasks. These are bounded catalogs, not unlimited source recovery claims. `variety.json` independently enumerates normalized task counts without option order or bank aliases.
