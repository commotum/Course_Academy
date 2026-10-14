# Four extraction stages

## 1. Specific source descriptions

Exact original records, keys, field layouts, answer strings and all shared solution prose are retained in source.json and reviewed in review.md. The original parameter anchors are:

| Source | Object | Requested shape | Anchor |
|---|---|---|---|
| q-107293 | (3x+b)^5 | full derivative radio | b=4 |
| q-342804 | (4x+b)^5 | full derivative blank | b=3 |
| q-71954 | (8x+b)^4 | full derivative radio | b=-7 |
| q-71956 | (b-5x)^3 | full derivative radio | b=2 |
| q-342875 | (x^5-cx^4)^2 | inner derivative blank after supplied 2g | c=4 |
| q-342883 | sqrt(5x+b) | full derivative blank | b=-4 |
| q-342891 | 1/sqrt(2x^4-x^2+c) | numerator blank after supplied g^(-3/2) | c=5 |
| q-11414 | (3x^5-cx^2)^3 | full derivative radio, no original key | c=4 |
| q-48850 | 2/sqrt(2x^2+cx) | full derivative radio, no original key | c=3 |

q-11414 and q-48850 have no source solution or difficulty. The former wrong bank changes the first term of the inner derivative, the outer multiplier and the outer power. The latter bank changes the sign, factor2 and fractional power of the denominator.

## 2. Generalized instructional backbone

Decompose the displayed composite into inner g(x) and outer f(g). Differentiate the outer function at g(x), differentiate g at x, explicitly multiply f′(g(x))g′(x), and substitute/reduce to the derivative. Observed sources have two derivative rows followed by three chain-rule rows. Preserve the formal differentiated arguments and both evaluation points. Supplied-fragment questions require only the supplied blank component, independently checked by reinsertion into the actual prompt.

## 3. Components and complete bank recipes

`bank-recipes.json` enumerates every original option with exact original value and a formula in the source parameters. This inventory has 29 values in nine complete field banks. It distinguishes recovered mathematical mistakes from unresolved historical intent. Every original remains public through `profile="raw-<source>"` and normal generate; no private literal replay helper exists.

For q-107293 let I=3x+b, a=3,n=5. Its options are nI^(n-1), aI^n, 20I^(n-1), a²I^(n-1), anI^(n-1). The coefficient20 is not defensibly recoverable from these sparse observations: its raw expression pattern fixes20 while its argument changes with b; this is explicitly unresolved and ineligible. The a² recipe is a wrong outer multiplier a in place of n; the aI^n recipe both omits n and retains the original power. Its separately authored normal bank is [anI^(n-1), nI^(n-1), aI^n, aI^(n-1), anI^n], derived from omitted factors/power decrement.

q-71954 has complete bank [an(2ax+b)^(n-1), n²I^(n-1), n²(2ax+b)^(n-1), aI^(n-1), anI^(n-1)] for a=8,n=4. Errors double the inner slope in the evaluated argument, use the outer exponent in place of the inner derivative, combine those errors, or omit the outer multiplier. q-71956 keeps a=-5,n=3 and uses [an(b-ax)^(n-1), anI^n, -an(b-ax)^(n-1), -anI^(n-1), anI^(n-1)], representing reflected inner argument, unlowered exponent, and sign losses. b=0 is ineligible because reflected square banks collide.

q-11414 let I=3x^5-cx^2,D=15x^4-2cx. The complete bank is [3DI², 3(5x^5-2cx)I², -2cDI², 3DI³, 3(5x^4-2cx)I²]. These respectively give the correct derivative; omit coefficient3 and power decrement in the first inner term; use the second inner derivative coefficient in place of outer exponent; omit outer decrement; and omit coefficient3 alone. These identifiable wrong operations are retained in the normal authored-key completion.

q-48850 let I=2x²+cx,D=4x+c. The bank is [-D/I^(3/2), D/I^(3/2), -D/(2I^(3/2)), -D/I^(2/3), -2D/I^(3/2)]. They represent correct derivative, missing negative sign, forgetting the given outer numerator2, inversion of fractional exponent, and counting numerator2 twice. The positive-radicand differentiation domain is necessary and retained.

All blank sources have their exact complete fragment and correct designation. No invented feedback or learner-facing distractor diagnoses are added.

## 4. Reusable masks, constraints, identity and variety

Source masks replace complete affine arguments, polynomial terms and independently derived derivative components simultaneously. They never replace short numbers, function letters, or TeX commands globally. Raw reconstruction at anchors is exact for prompts, solution presence and text, ratings, keys, field types, answer types and all values. Under changed parameters, observed common prime stages and prose remain exact masks, independent of which answer is selected.

Each shift is an integer in -12..12, except the q-71956 shift excludes0. Each polynomial/quadratic constant/coefficient c is1..16. Raw profiles have the same supported bounds and preserve their omissions under changed inputs. Easy is a separately authored affine square with a in {-5,-4,-3,-2,2,3,4,5} and b in {-9..-1,1..9}. Its bank uses the correct derivative, omitted inner factor, omitted outer factor combined with unlowered exponent, unlowered outer exponent, and reversed affine shift. Select the complete profile before sampling any parameter. Reject the whole instance on any equivalent pair; no replacement distractor pool is used.

Finite normal enumeration contains72 easy tasks,99 moderate tasks and74 hard tasks after mathematical deduplication. Hard q-342891's additive constant c changes the displayed radicand but not its assessed numerator fragment, so it contributes exactly one mathematical task, not16. Easy sign-reversed pairs (a,b) and (-a,-b) define the same square and count only once; the144 presentations therefore represent72 tasks. The other families vary operative inner coefficients/arguments; symbol aliases, option order, evidence profiles and bank aliases do not inflate task counts. All parameter bounds also apply to explicit inputs. Hard radical domains require positive inner expressions. The reciprocal quartic radicand is 2(x²-1/4)²+c-1/8>0.

Mathematical fingerprints omit bank/profile/seed and q-342891's incidental constant. Full content identity includes actual prompt, solution, complete sorted displayed bank, correct value, domain, actual difficulty, generator version, Python and SymPy versions. Default/profile aliases collapse to identical IDs when their actual content agrees. Shuffling retains field and answer identities. Different actual banks have different content identities.

`registered-baseline.json` records all files and SHA256 values under the registered numeric script and evidence directory, including commit receipts and caches. Validation compares the complete before/after path set and hashes. Draft files do not change live behavior, register anything, or transact data.
