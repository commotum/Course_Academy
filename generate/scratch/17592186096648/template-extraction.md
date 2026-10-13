# Four-stage extraction

## 1. Original questions specifically

q-12135 displays `4a - 12b` then `λ(a - 3b)`, declares them equal nonzero vectors and asks for λ. The five displayed choices are math 4, math 3, text `No such $λ$`, math −4, math 2. One radio field named selection. No rating, correct-ref or worked solution exists in the captured record. Independent factoring gives 4. The authoritative local widget `/home/jake/Developer/MA/DATA/Lessons/1103/Source/1103.json`, lesson index 8, confirms this prompt/layout and complete bank, with a different incidental option order.

q-12139 displays `λ(-0.5a + 6b)` then `a - 12b`, declares equality of nonzero vectors and asks for λ. The complete bank is math 2, math 0, text `No such $λ$`, math `-\frac{1}{2}`, math −2. Same radio field; all three attributes again absent. Independent ratios 1/(−0.5) and (−12)/6 both give −2. Local authoritative widget lesson index 7 confirms the presentation. The absence of correct ref is never counted as a matched designation.

Canonical e-4279 has `7a+14b` and `λ(3a+6b)`, factor 7/3. Its fixed prose is “Notice that”, followed by the factorization equation, then “Therefore,” and λ=7/3. It is not counted as a practice question. Canonical assumptions a,b nonzero do not exclude 3a+6b=0; its uniqueness premise is therefore underspecified. Normal output uses the practice originals' stronger declared nonzero vector equality. Raw canonical evidence remains in source.json; canonical prose and rational workload, not the underspecified premise, anchor authored solutions.

## 2. Shared pattern

Given target vector k(ua+vb) and a displayed scaled vector λ(ua+vb), both equal and nonzero, identify the unique scalar factor from two equal coefficient ratios. Either side may appear first. Positive and negative factors both express parallelism. The requested response is the scalar λ, so “No such λ” is false in this stated equality setting.

## 3. Components and complete choice mapping

`u,v` are the displayed base coefficients; target coefficients are `ku,kv`. Variable vector labels are fixed a,b. Whole linear-expression slots construct both prompts. No substring substitution is used.

| Profile | Choice type/value at source | Parameterized operation | Interpretation status |
|---|---|---|---|
| raw_12135 | math 4 | k | independently correct |
| raw_12135 | math 3 | abs(v) | observed base-coefficient shape; intention opaque |
| raw_12135 | text No such λ | fixed categorical denial | false because equality is given |
| raw_12135 | math −4 | −k | reverse factor sign |
| raw_12135 | math 2 | k/2 | halving shape; intention opaque |
| raw_12139 | math 2 | −k | reverse factor sign |
| raw_12139 | math 0 | zero factor | contradicts declared nonzero equality |
| raw_12139 | text No such λ | fixed categorical denial | false because equality is given |
| raw_12139 | math −1/2 | 1/k | reverse ordered ratio |
| raw_12139 | math −2 | k | independently correct |

These historical profiles are public parameterized evidence recipes, not literal payload lookups. The underdetermined q-12135 recipes remain ineligible for learners. They are not promoted as recovered author intent. Raw changes can use any exact nonzero u,v,k within coefficient ceiling 54, but collisions reject the whole bank. The decimal raw presentation additionally allows denominators 2,4,5 only. All observed math values and text answer types/shape replay exactly at source parameters, and missing raw attributes remain missing.

The separately authored default complete bank is k, −k, 1/k, −1/k, No such λ. The four numerical operations correspond respectively to correct target/base division, ignoring the sign, reversing the ordered ratio, and reversing both order/sign. k excludes 0 and ±1 so all four numerical values are distinct. This bank is selected before sampling; complete collisions reject an explicit instance, never replace one option.

## 4. Reusable template, stages and bounds

Prompt mask: `Given that $TARGET$ and $λ(BASE)$ are equal (non-zero) vectors, find the scale factor $λ$.`, or the observed reversed layout. Moderate base uses terminating decimal notation, as q-12139; easy/hard use integer coefficients. Normal worked solution is separately authored because original practice solutions are absent. It preserves canonical common “Notice that” / “Therefore,” prose and adds: formal λ distribution → two ordered target/base coefficient substitutions with exact reductions → whole-vector factorization → final λ and direction/parallel conclusion. One fixed solution per question, independent of chosen error; no learner-facing distractor diagnosis.

| Authored level | Exact allowed workload |
|---|---|
| easy | u,v,k integers; 1≤abs(u)≤4, 1≤abs(v)≤6, 2≤abs(k)≤8; target coefficients ≤48 |
| moderate | u=±1/d, d∈{2,4,5}; integer 1≤abs(v)≤6 and 2≤abs(k)≤6; ku integer; target coefficients ≤36 |
| hard | integer u=dm,v=dn, reduced k=p/d with d∈{2,3,4,5}, 2≤abs(p)≤9 and gcd(abs(p),d)=1; 1≤abs(m)≤4,1≤abs(n)≤6; target coefficients ≤54 |

All constraints apply to explicit API calls. Signed factors/components are unordered variations. Domains are enumerated before deterministic sampling, with no first-valid pool. Shared scalar scaling and sign of both vectors leave the task unchanged, so mathematical fingerprints retain only k and v/u. The complete prompt, fixed solution, displayed bank, actual difficulty and version form separate presentation identity. Layout, option order, variable aliases, bank aliases and common scaling do not inflate mathematical counts. Option shuffling changes no content UUID.

The finite meaningful task counts are recorded by executable enumeration in validation.json. This preserves coefficient-division workload (including the reduced factor) rather than claiming infinite diversity through scale/letter changes. All source field omissions, complete banks, canonical assumption caveat and opaque operations are reported separately from supported authored correctness and actual native radio grading.
