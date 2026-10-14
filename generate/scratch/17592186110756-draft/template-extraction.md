# Extraction

## 1. Particular originals

| MA original | Given coordinate | Target | Supplied number form | Captured solution |
|---|---|---|---|---|
| q-124750 | y=1/5 | sec | rational unit numerator | identity, four root rows, positive cosine, reciprocal, four rationalization rows |
| q-65066 | y=3/5 | sec | rational; rational complement | absent; unrated and key absent |
| q-124743 | x=1/3 | csc | rational unit numerator | same stages with sine |
| q-65062 | y=√3/3 | sec | radical; numerator coefficient one | same stages; final fraction cancels factor 3 |
| q-65064 | x=√15/5 | csc | radical; numerator coefficient one | same stages; reciprocal display has aligned wrapper |
| q-85234 | y=√2/3 | sec | radical; numerator coefficient one | same stages; three rationalization rows (already reduced) |

Every source string and attribute-presence omission is preserved in source.json. source-cases.json supplies all six public raw-profile recipes. There are 30 choices; 5 present correct designations and one genuinely missing designation. No duplicate fields or feedback occur.

## 2. Shared mathematical backbone

Given k=√r/b with 0<k<1, identify given sine/cosine from axis. Use sin²+cos²=1, isolate the OTHER ratio, substitute k, square numerator/denominator, subtract, extract root, choose positive in QI. Then invert. If missing=c√s/b is irrational, rationalize by √s/√s and reduce b√s/(cs). The ordered formal and arithmetic rows and shared prose remain in normal generation. The worked solution does not depend on the selected error.

## 3. Component and bank mapping

Let d=b²−r, missing=√d/b=c√s/b, correct=b/√d. Complete banks below are listed in original captured order. Patterns with b+2, b+4, changed radicands, or isolated b are opaque observed compound-expression patterns; their numeric reproduction does NOT establish a learner error. They are only evidence profiles, never default banks.

| Bank | Complete parameterized recipes |
|---|---|
| q-124750 | (b+4)√s/c; b√s/(b+4); √s/c; correct; (b+2)√s/(cs) |
| q-65066 | d/b; b/d; d/b²; missing; correct |
| q-124743 | correct; c√(2b)/b; (b+2)√s/c; b√b/c; b/c |
| q-65062 | −√r/√d (unreduced shape retained); −correct; correct/b; √r/√d (unreduced retained); correct |
| q-65064 | correct; b√b/(cs); 2b√b/(cs); missing; b |
| q-85234 | d/r; √d/r; (b+2)/√d; correct; d/b |

Raw banks' unknown intent is unresolved, but complete expression-pattern fidelity is independently checked. q-65066's correct mathematical value is independently derived for authored completion, not counted as a matched observed key.

Normal complete bank `method-reciprocal`: correct; missing (omit inversion); 1/given (invert supplied ratio); 1/(1−given²) (omit square root); given/missing (use quotient instead of reciprocal). Normal `method-sign`: correct; −correct (wrong QI sign); missing; 1/given; 1/(1−given²). Both banks derive only from actual shown identity/coordinate/reciprocal, retain five options, add no feedback, and are selected before parameters. Entire instances are rejected if ANY pair is mathematically equal; no pooled first-valid options.

## 4. Stable masks and slots

Full scalar components, rather than digits/short substrings, are masked in source prompt and solution: known ratio; squared fraction r/b²; complementary fraction d/b²; simplified positive coordinate; unreduced reciprocal; rationalizing unit factor; intermediate b√s/(c·s); final reduced scalar. Source numerator/radical and rationalization row structures are retained independently; source formatting returns exactly at anchor without a payload-return branch. The duplicate-value stage precedence is explicit. Plot image reuse is conditional on identical mathematical point geometry; changed points get new Matplotlib renders. Axis is a family role; both axes are selected in normal defaults across all supported templates. Random seed affects sampling and choice order but fixed parameters/profile/level retain identity. Task fingerprints omit banks, profile, incidental image paths and common coordinate scaling; content identities include prompt, solution, complete displayed bank and level.

Original profile constraints retain rational-unit numerator vs radical-input vs rational-complement roles. Author-created normal scope and level guards are distinct from raw observed grade preservation. Source field and missing attribute parity is tested by the parent's root-source-fidelity F.check, separately from mathematics and native grading.
