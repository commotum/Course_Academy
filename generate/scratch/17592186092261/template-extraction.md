# Template extraction

## 1. Specific observations

q-48565 uses 3^(2x²), f notation, and four chain rows: formal operator product, substituted outer/inner factors, coefficient product with u retained, restored exponent. Its two captured radio banks have the same five values but different order and log spelling. The original field lacks a correct ref; the newer field designates 4x·3^(2x²)·ln(3).

q-48631 uses 3^(6x²-4), y notation and a five-choice bank. No worked solution, difficulty or correct ref was captured. The authoritative widget confirms its single radio layout. Its normal easy assignment, correct designation and complete solution are authored/inferred completions, independently checked against the prompt.

q-107458 uses 2^(3-x³), f notation, no fields and the four-row composite/derivative/chain sequence. q-71881 uses 2·5^(x+x³), no fields, and preserves the extra outside-scale distribution from (1+3x²)·2 to (2+6x²) in its final derivative. The separate full derivative blanks are normal authored completions.

q-107459 uses 3·4^(x²-1), y notation and only **three** chain rows: formal product, substituted factors and final restored expression. It does not have an extra product-with-u row. q-107461 uses 6^(1-4x), f notation, four rows, including a grouped negative inner derivative. q-1952 uses 2^(9x), y notation, four rows with the logarithm placed before the base power in the product and final rows.

q-312462 uses 5^(x³+1), f notation, and supplies ·5^(x³+1) outside the blank. Its answer is **3x²·ln(5)**; the complete derivative has the wrong response shape. The four solution rows preserve coefficient/log-first ordering.

q-340969 uses 5^(x-x³) at x=1. Its three-row chain is followed by four slope evaluation rows: derivative restricted to the point, explicit substitution, evaluated polynomial components and base exponent, and final slope. q-48659 uses 4^(7x) at x=1/7. Its four chain rows and three evaluation rows are followed by an explicit final “Therefore” sentence containing both the actual point and slope.

Decoded string evidence is in `decoded-notation.json`. The different ln/operatorname spellings and actual U+2061 characters are real decoded text. Runs of two backslash bytes are valid aligned row separators. JSON serialization is not evidence of doubled TeX commands. Normal output standardizes ln spelling and removes invisible application characters. Raw replay retains their exact original bytes.

## 2. Shared mathematical demand

Write y=c·b^u with u a familiar polynomial, differentiate the outer function including **ln(b)** and the inner polynomial, multiply the factors, and restore u. Moderate asks for the resulting derivative at a supplied familiar point. The fragment blank asks only for the coefficient of the supplied exponential factor. No integration, inverse solving, critical-point search or tangent-equation construction belongs here.

## 3. Every original component and complete bank

`choice-map.json` lists every captured field/choice, original UUID/value, rendered parameterized pattern at its anchor, exact mathematical value and original designation (null means absent). This covers **37/37 values in 9/9 field banks**, including the legacy duplicate. The following whole banks explain the parameterized patterns used together. Let u=a·x^n+l·x+d, D=u', B=b^u and L=ln(b); c is the outside coefficient. Order below follows the older capture where q-48565 has two fields.

| Source profile | Complete pattern bank | Interpretation limits |
|---|---|---|
| q-48565 | a·b^(ax)·L; D·B; ax·B; D·B·L; x·b^(ax)·L | Altered linear-exponent patterns are opaque historical forms. Newer field has the same bank, reordered. |
| q-48631 | D·B; D·B·L; (D+d)·B; (D+d)·B·L; (na·x^(n+1))·b^(na·x)·L | Final compound power pattern is opaque. Missing correct ref is independently inferred only for normal output. |
| q-107459 | -D·B·L; -cD·B·L; cD·B·L; D·B·L; cx·B·L | Complete observed sign/scale/power-factor patterns. |
| q-107461 | (-a/2)·B·L; -a·B·L; -ab·B·L; a·B·L; ab·B·L | Half-coefficient and base-scaled coefficient patterns underdetermine historical intent. |
| q-1952 | a·B; u; B; a·L·B; L·B | Observed exponent-as-answer and omitted-factor patterns. |
| q-48659 | u(t); a·L; a·b^u(t)·L; b^u(t); b^u(t)·L | Whole scalar patterns at the familiar reciprocal point; not arbitrary coefficient perturbations. |
| q-312462 | D·L | Supplied exponential factor stays outside the blank. |
| q-340969 | cD(t)·b^u(t)·L | Slope, with supplied x value substituted. |

Opaque patterns are public `observed:<qid>` or `historical:<qid>` evidence profiles and **ineligible for learner defaults**. They are parameterized expression patterns, not literal source payload returns or inferred author intentions. Historical replay uses the original complete bank as one unit. It never pools distractors from other profiles.

Normal radio defaults use a separately authored whole chain-rule operation bank: correct cD·B·L; omitted logarithm cD·B; omitted inner derivative cB·L; reversed inner sign -cD·B·L; treating b^u as a power-rule expression cD·u·b^(u-1). Slope fields evaluate those same expressions at the displayed point. Blank fields use the correct requested fragment or slope only. The family/profile is chosen before parameters; any duplicate/equivalent answer rejects the whole instance. No learner-facing distractor diagnoses are added.

## 4. Reusable masks, boundaries and authored hard scope

Source masks replace complete powers, complete inner/outer derivative components, complete evaluation rows, full points and the complete concluding slope. Replacements occur simultaneously in longest-component order. They do not recursively replace short numbers or letters. Source term ordering, prose and operative stage sequence are retained at changed inputs. Normal notation adds an explicit multiplication operator where a coefficient meets a numeric base (the source x3^u means x·3^u; adjacent numeric factors must never become 43^u). Multi-term outside coefficients remain grouped.

All source families use integer bases 2..6, outside scale 2..5 where observed (unit scale where absent), signed inner coefficients of magnitude 1..9, and powers fixed per family (1, 2 or 3). Source-specific absent terms remain absent. Shifted quadratic constants are nonzero, and the source cubic+linear family requires both nonconstant terms. Easy remains a derivative computation, with an explicitly authored supported full-answer field where the original field was absent.

Moderate linear slope uses a=2..9 and the supplied familiar point t=1/a, so the exponent evaluates to 1. Moderate cubic+linear uses nonzero a,l of magnitude <=3, point +/-1, and |u(t)|<=2; the slope must be nonzero. Its outside scale remains 1. These are repeated variations of the observed point-evaluation method.

Hard has no observed source. The lesson route is Introduction → linear e exponent (KP92260) → nonlinear e exponent (KP92263) → general-base exponent (this KP), determined by first-step/next links. The canonical example already includes a nonunit outside scale and negative inner derivative; q-71881 establishes sum-of-polynomial inner functions, and the two moderate sources establish slope evaluation. Prerequisites are differentiating exponential functions and the chain rule. Authored hard therefore combines the **existing slope criterion** with a nonunit outside scale and three nonzero cubic/quadratic/linear terms. Each task differentiates those three components, multiplies by the same outer exponential/log factor, and evaluates at +/-1. It uses c=2..4, |a,k,l|=1..3, |d|<=5, and u(t) in {-1,0,1,2}; zero slopes are rejected. The extra bookkeeping is uniform within hard, with no progression or new topic. Explicit inputs and samplers enforce the same bounds.

Mathematical fingerprints use the actual derivative (or requested coefficient fragment) and supplied point/criterion, independent of bank/notation/seed. The supplied fragment's unused exponent constant does not inflate task counts. Content UUIDs additionally depend on actual displayed prompt, fixed solution, complete unordered bank, difficulty and version. Shuffling choices cannot change content identity. Historical aliases and incidental metadata do not create new IDs.

`variety.py` enumerates the default sampling support without counting bank aliases or unused fragment offsets. Its exact normalization reduces 4=2² and factors the multiplicative constant from an exponent offset. The default domains contain 41/434/217/1048/1656/40/37/41 distinct easy tasks across the eight source masks; moderate contains 864 cubic/linear point tasks and 40 reciprocal-linear tasks; hard contains 19,244 distinct bounded three-term point tasks. Those are domain cardinalities, not claims that every instance was engine-tested. The displayed-math sampler, source replay and native checks are separately counted in `validation.json`.
