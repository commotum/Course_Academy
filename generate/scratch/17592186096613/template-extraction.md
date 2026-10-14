# Template extraction

## 1. Specific source descriptions

q-11909 displays y = 7\ln x with dy/dx notation, five choices, no rating, correct reference or solution. q-11910 uses the same spaced prompt with coefficient 2/3 and a different complete five-choice bank. q-101604 displays -9ln⁡x, text-d notation and a radio; q-101600 displays 2eln⁡x with the corresponding Euler bank. Both have the reciprocal identity and four worked rows, with explicit `\cdot` before the formal derivative in row two. q-339941 uses -11\operatorname{ln}x, and q-308849 uses 8ln⁡x; both append derivative equals then `{{field-1}}` and one canonical blank entry. q-339949 and q-339950 use 11/4 and -7/3 with the same blank layout and two equivalent accepted entries. Their row two has implicit coefficient multiplication. q-70881 displays 2\operatorname{ln}x and the same four-row implicit solution, but has no fields or placeholder. Original decoded strings have no C0 or TeX brace defects; the Unicode application marker is preserved in raw evidence, normalized in normal practice.

`source.json` gives every exact field/value/string. `template-extraction.json` maps every original option individually to a recipe, source field, parameters and complete profile. No source question is discarded.

## 2. Generalized mathematical and instructional backbone

Given y=c ln x for real x>0, find the derivative RHS. Recall D(ln x)=1/x; apply the formal derivative to the original expression; pull the entire constant out; replace D(ln x) by 1/x; collect c/x. Each instance has one fixed worked solution independent of learner input. Prompt argument x, output y, reciprocal rule and ordered stages are fixed because they define this KP. No function composition or product rule is needed.

## 3. Components and complete banks

Parameters are reduced signed numerator n, positive denominator d, and fixed Euler exponent k. c=(n/d)e^k. Source k is 0 or 1. Complete observed profiles are selected before parameters:

| Bank | Complete ordered mathematical recipe list | Conditions |
|---|---|---|
| integer | 1/x; -c/x; 1/(cx); x/c; c/x | d=1,k=0, |n|≥2 |
| fraction | c/x; 1/(dx); n/x; d/x; d/(nx) | d>1,k=0,n≥2, gcd(n,d)=1 |
| euler | e/(nx); n/(ex); ne/x; n+e/x; e+n/x | d=1,k=1, |n|≥2 |
| canonical | c/x | one accepted blank entry |
| equivalent-entry | c/x; exact plain n/(dx) spelling | d>1,k=0; both entries accepted |
| none | no field or bank | raw fieldless source only |

Integer choices reproduce dropping the coefficient, changing its sign, inverting it, inverting the reciprocal function, and the correct rule. Fraction choices reproduce omitted numerator, omitted denominator, denominator used as coefficient, reciprocal coefficient, and correct rule. Euler profiles reproduce reciprocal factors and splitting the constant product into a sum. Those interpretations are inferred; the complete operations and anchor values are observed and defensibly parameterized. No opaque profile is promoted to default. Whole radio instances are rejected when any pair is equivalent or more than one choice is correct. Blank aliases are deliberately equivalent, not radio ambiguities.

## 4. Reusable masks, variable slots and constraints

The source-recipe builder masks the **complete original derivative quotient first**, then the complete original coefficient. Thus all prompt, formal operator, pulled-out coefficient, reciprocal multiplication and final quotient occurrences change together. Raw source masks preserve surrounding bytes and omit absent attributes. At anchors they do not return literal payloads: the normal public API executes the same masks and bank recipes used for changed inputs. An independent validator reads the actual learner prompt, all solution rows and all bank expressions rather than trusting parameter metadata.

The dependent slots are coefficient appearance and derivative quotient; each original mathematical notation stays in raw replay. Normal observed-family presentation replaces only natural-log typography with `\ln`. Legacy solutions, absent in source, use the canonical introduction and four formal stages. Fieldless raw evidence remains fieldless; supported normal questions are separate completed layouts. Moderate and hard are authored blanks with the same worked backbone and normal ln notation, using the disjoint forms and bounds documented in classification.md. Explicit inputs obey identical guards to samplers. Every domain is finite and enumerable; coefficient signs, reduced denominators and fixed exponents affect math fingerprints. Bank/profile/layout aliases and shuffles do not.

Presentation identity hashes actual prompt, fixed solution, difficulty presence/value, field layout, complete bank and correct-reference presence. It does not depend on seed or option order. Mathematical identity canonicalizes the actual displayed coefficient and x>0 and excludes layout and banks. Missing ratings remain absent in raw replay; every raw/evidence record has explicit evidence_only and eligible_for_learning flags.

## Source findings and fidelity denominators

All 26 displayed source values are mathematically correct or legitimate wrong radio values. The two blank banks each carry two equivalent answers intentionally. Eight complete source banks replay exactly; six supplied correct designations match; two missing designations are preserved as missing, while normal practice infers c/x independently. Seven supplied worked solutions replay exactly, including q-70881. Nine prompts and all key-presence sets match. No mathematical source repair is required. Three incomplete assessment records remain evidence only. Source typography normalization in normal practice is separate from exact raw replay.

No plots or plot assets exist, so plot extraction and generation are not applicable.
