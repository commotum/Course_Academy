# Four-stage extraction

## 1. Specific observations

q-136614 supplies 7 and asks csc(-x), no solution/difficulty/correct ref. q-136605 supplies -6 and asks csc(-x+10π), with the same omissions. Their source fonts use `\csc`, Unicode π, and spaced expressions. The three labeled easy sources use `\operatorname{csc}⁡a`: -3, 11/4, and √5. Their common solution recalls the unchanged cosecant graph, explains origin rotational symmetry and 180° rotation, states oddness, then substitutes. The negative supplied value has a distinct double-negative substitution row and final arithmetic row; the positive fraction and radical go directly to their negative value.

Hard q-158069 supplies -4 and asks 3 csc(-x-18π)-7. Its solution recalls the graph; states period and oddness; displays -x-2π·9 → -x; displays -csc x → -(-4) → 4; then displays 3(4)-7 → 12-7 → 5. Hard q-158071 supplies 7/6 and asks 4 csc(-x+6π)+1: -x+2π·3 → -x; -csc x → -7/6; then 4(-7/6)+1 → -14/3+1 → -11/3. Neither arithmetic stage is collapsed in normal variants.

## 2. Generalized pattern

Given csc(u)=v, negate the angle, optionally remove a signed integer number of full 2π periods, apply csc(-u)=-csc(u), and, at hard, evaluate a nonunit outer multiplier and nonzero signed offset. Response is always one scalar radio choice. The angle remains symbolic in the cosecant domain; no inverse trig or exact-angle evaluation is needed.

## 3. Complete component/bank mapping

Each row lists the entire simultaneous five-option bank; original order is immaterial to mathematical comparison, and no choice is omitted. `v` is the supplied value; `C=-av+b`; `n` is the signed period multiplier.

| Source | Parameters | Five displayed values as operations | Correct designation | Interpretation |
|---|---|---|---|---|
| q-136605 | v=-6,n=5,a=1,b=0 | -v+2nπ; v+2nπ; v; 0; -v | absent, inferred 6 | output-shift / unchanged / zero / oddness operations; evidence only |
| q-136614 | v=7,n=0,a=1,b=0 | v; 0; -v; 1/v; -1/v | absent, inferred -7 | direct sign/reciprocal complete bank |
| q-136554 | v=-3,n=0,a=1,b=0 | v; -1/v; -v; 0; 1/v | 3 | same complete sign/reciprocal bank |
| q-158065 | v=11/4 | v-1; 1/v; 1-v; -v; v | -11/4 | subtract-unit values exactly mapped; intended error source unresolved, raw evidence only |
| q-158066 | v=√5 | -v; v; 1; -v²; v² | -√5 | sign/square/unit complete bank |
| q-158069 | v=-4,n=-9,a=3,b=-7 | 9C/5; -3C; 2C/5; C; -19C/5 | 5 | opaque proportional evidence masks, no inferred error mechanism |
| q-158071 | v=7/6,n=3,a=4,b=1 | C; -C/22; -17C/11; 15C/22; 5C/22 | -11/3 | opaque proportional evidence masks, no inferred error mechanism |

The last two rows are transparent replay parametrizations of observed values, not recovered author algorithms or plausible learner error models. They are explicitly public, evidence-only, and never selected by normal sampling. Their limitation is preserved even after native grading succeeds. They reproduce every numeric option, not only the correct answer, but cannot support claims of distractor intent.

Normal authored hard bank is `[C, av+b, -av-b, -v+b, -a/v+b]`: correct, omitted oddness, reversed offset, omitted multiplier, and reciprocal confusion. It is derived from the actual displayed operations. Normal rational easy uses the supported direct sign/reciprocal bank, not the unresolved subtract-unit bank. Normal moderate uses the complete observed shifted-value bank above with a mathematically inferred correct designation. No learner-facing diagnosis is added.

## 4. Reusable masks and constraints

Fixed prose is extracted from the actual easy and hard source opening blocks. Complete scalar/angle components are substituted into explicit masks; no global short-token replacements are used. Periodicity rows retain the signed shift, factor 2π·|n|, and reduction. Oddness retains the formal rule, substitution, and optional negative-input arithmetic row. Outer hard rows retain grouped signed values, evaluated product, offset arithmetic, and the conclusion. Raw legacy prompt punctuation and Unicode π are preserved; normal families retain source notation.

A family and complete bank are selected before sampling parameters; every bank is constructed in full and the whole instance is rejected if any pair is equivalent or any value is invalid. Explicit parameter calls use the same guards and never resample. Radio order is seeded and shuffled after correct identity is recorded. Mathematical fingerprints normalize supplied values, outer coefficients, and level workload while excluding seed, variable names, bank/profile aliases, and whole-period shifts. Content identity includes displayed prompt, fixed solution, complete bank, field shape and actual difficulty presence.

Decoded source answer byte inspection found zero adjacent-backslash pairs in all 35 option values. `\frac` starts with bytes `[92,102,114,97,99]`; there is no TeX escaping repair. Raw field and enum shape is normalized into established local records; attribute presence, field order/type/key, complete answer fragments and correct designation are compared individually. Missing correct refs are inferred only in completed normal output, and never count toward observed designation fidelity.
