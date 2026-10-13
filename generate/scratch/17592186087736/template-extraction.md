# Template extraction

The four stages below are based on all 16 practice records at basis 1356. `source.json` retains every original field and snapshot provenance; `review.md` displays all original prompts, banks, layouts and complete worked solutions. `source-cases.json` replays every original through the normal parameterized renderer. No source payload is returned as a special-case answer lookup.

## 1. Describe each source specifically

All coordinates are x=a cos θ+h and y=b sin θ+k, with θ∈[0,2π). The source inventory in `classification.md` lists every signed/rational coefficient, shift, response layout and per-coordinate row count. Radio prompts have no embedded field token and conclude with the pair of ranges; blank prompts retain every original {{field-N}} placement, endpoint slot, relation slot, and key order and omit that final summary as observed. The original Unicode function application marker, `operatorname` notation, whitespace and shift-first forms are retained in source replay.

Each coordinate solution starts with its trig range. A positive nonunit scale adds a multiplication row. A negative scale adds reversed inequalities and then an ascending reordered row. A nonzero shift adds one unevaluated endpoint-translation row. The final row names x/y, followed by the original “So, we can conclude” sentence. Unit scaling rows are omitted exactly as in the sources. No new stage is appended to make rescaling convenient.

## 2. Generalized mathematical pattern

Determine two independent coordinate ranges by applying signed scale and additive translation to the known sine/cosine interval [-1,1]. Return the complete ordered closed interval pair or the six supplied endpoint/inequality fragments. The complete pair is assessed; comparison never checks only one coordinate or only an endpoint.

## 3. Components and every observed choice

Let a,b,h,k denote displayed parameters; A=|a|, B=|b|. Let C=(h−A,h+A,k−B,k+B)=(l,u,m,n), and interpret each four-tuple as xmin≤x≤xmax, ymin≤y≤ymax. The exact complete observed bank formulas are below (the branch order is the original database choice order). This is an explicit expression-pattern replay mapping. Its identities and numerical values are independently checked against displayed choices at every original, and its parameterized variants are checked for valid intervals and collisions.

```python
def observed_bank(sid,p):
 a,b,h,k=[p[v] for v in 'abhk']; A,B=abs(a),abs(b); C=result(p); l,u,m,n=C
 if sid=='q-16201':return [(1,1,1,1),(-B,B,-A,A),C,(0,B,0,A),(0,A,0,B)]
 if sid=='q-123777':return [(-h,h,m,n),C,(-u,-l,-n,-m),(-h,h,-1,1),(l,u,-1,1)]
 if sid=='q-123773':return [(-u,-l,-n,-m),(-1,1,m,n),(-1,1,-n,-m),(l,u,-k,k),C]
 if sid=='q-123775':return [(-1/A,1/A,-n,-m),(-1/A,1/A,-k,k),(l,u,-k,k),C,(k-2*B,k,m,n)]
 if sid=='q-70341':return [(0,A-h,k,k+B),(h-A,-A-h,-B-k,0),(l,0,-k,n),C,(A+h,A-h,m,n)]
 if sid=='q-70523':return [(A,h,k-2*A,k+h),(-2*A,B-k,h-2*A,-k),C,(0,h,k,0),(-h-A,0,1,-k)]
 if sid=='q-73626':return [(B,B-k,-k-B,B-k),C,(h,2*B,k+B,B-k),(h,3*B,m,n),(l,0,m,0)]
 if sid=='q-73632':return [(-A,-h,-h,h+A),(-A-h,h,-A,h),C,(h,A+h,-h,n),(l,A,m,A+h)]
 raise ValueError('No observed radio bank for '+sid)
```

Supported method hypotheses (not learner-facing diagnosis): q-16201 swaps amplitudes or uses [0,1] for each trig function, including a compound swapped-amplitude plus nonnegative-range option. q-123777 and q-123773 include negation of complete translated ranges, omitted shifts/unit bounds, and treating a shift as an amplitude. q-123775 includes reciprocal x amplitude and negated translated y range, including the compound reciprocal-plus-negation option, and treating the y shift as its amplitude. These operations can account for the complete values at the source parameters but cannot prove author intent.

**Residual underidentified patterns:** q-16201's degenerate (1,1,1,1) option; q-123775's cross-coordinate (k−2B,k,m,n); all four wrong choices of q-70523 and q-73632; the mixed-endpoint distractors of q-73626 and q-70341. Their complete expression patterns are preserved only in explicitly selected observed profiles, not promoted to default error-method banks. Their formulas are one bounded replay extension consistent with the captured values; the evidence does not identify unique generalization or author intent. This distinction is not a mathematical-fidelity failure: complete source values still match. It limits the pedagogical interpretation and use of those profiles.

### Exact field mapping at original parameters

#### q-16201

Parameters: {'a': 7, 'b': 3, 'h': 0, 'k': 0}. Template/profile: q-16201 / observed:q-16201.

Field `selection` (:answer-field.type/radio).

1. `1\le x\le 1,\,1\le y\le 1` — observed wrong; mapped to bank formula tuple 1.
2. `-3\le x\le 3,\,-7\le y\le 7` — observed wrong; mapped to bank formula tuple 2.
3. `-7\le x\le 7,\,-3\le y\le 3` — observed correct; mapped to bank formula tuple 3.
4. `0\le x\le 3,\,0\le y\le 7` — observed wrong; mapped to bank formula tuple 4.
5. `0\le x\le 7,\,0\le y\le 3` — observed wrong; mapped to bank formula tuple 5.

#### q-70341

Parameters: {'a': 3, 'b': 2, 'h': -1, 'k': 2}. Template/profile: q-70341 / observed:q-70341.

Field `selection` (:answer-field.type/radio).

1. `0 \le x \le 4, 2 \le y \le 4` — correct designation absent; mapped to bank formula tuple 1.
2. `-4 \le x \le - 2,-4 \le y \le 0` — correct designation absent; mapped to bank formula tuple 2.
3. `-4 \le x \le 0,-2 \le y \le 4` — correct designation absent; mapped to bank formula tuple 3.
4. `-4 \le x \le 2, 0 \le y \le 4` — correct designation absent; mapped to bank formula tuple 4.
5. `2 \le x \le 4, 0 \le y \le 4` — correct designation absent; mapped to bank formula tuple 5.

#### q-276258

Parameters: {'a': 4, 'b': 2, 'h': 0, 'k': 0}. Template/profile: q-276258 / none.

Field `field-1` (:answer-field.type/blank).

1. `-4` — observed correct; mapped to h−A.
Field `field-2` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-3` (:answer-field.type/blank).

1. `4` — observed correct; mapped to h+A.
Field `field-4` (:answer-field.type/blank).

1. `-2` — observed correct; mapped to k−B.
Field `field-5` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-6` (:answer-field.type/blank).

1. `2` — observed correct; mapped to k+B.

#### q-327882

Parameters: {'a': 5, 'b': 7, 'h': -3, 'k': 1}. Template/profile: q-327882 / none.

Field `field-1` (:answer-field.type/blank).

1. `-8` — observed correct; mapped to h−A.
Field `field-2` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-3` (:answer-field.type/blank).

1. `2` — observed correct; mapped to h+A.
Field `field-4` (:answer-field.type/blank).

1. `-6` — observed correct; mapped to k−B.
Field `field-5` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-6` (:answer-field.type/blank).

1. `8` — observed correct; mapped to k+B.

#### q-123777

Parameters: {'a': 1, 'b': 1, 'h': 3, 'k': -1}. Template/profile: q-123777 / observed:q-123777.

Field `selection` (:answer-field.type/radio).

1. `-3\le x\le 3,\,-2\le y\le 0` — observed wrong; mapped to bank formula tuple 1.
2. `2\le x\le 4,\,-2\le y\le 0` — observed correct; mapped to bank formula tuple 2.
3. `-4\le x\le -2,\,0\le y\le 2` — observed wrong; mapped to bank formula tuple 3.
4. `-3\le x\le 3,\,-1\le y\le 1` — observed wrong; mapped to bank formula tuple 4.
5. `2\le x\le 4,\,-1\le y\le 1` — observed wrong; mapped to bank formula tuple 5.

#### q-276261

Parameters: {'a': 3, 'b': -5, 'h': -2, 'k': 0}. Template/profile: q-276261 / none.

Field `field-1` (:answer-field.type/blank).

1. `-5` — observed correct; mapped to h−A.
Field `field-6` (:answer-field.type/blank).

1. `5` — observed correct; mapped to k+B.
Field `field-5` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-2` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-3` (:answer-field.type/blank).

1. `1` — observed correct; mapped to h+A.
Field `field-4` (:answer-field.type/blank).

1. `-5` — observed correct; mapped to k−B.

#### q-327861

Parameters: {'a': 6, 'b': -3, 'h': 0, 'k': 0}. Template/profile: q-327861 / none.

Field `field-5` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-2` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-4` (:answer-field.type/blank).

1. `-3` — observed correct; mapped to k−B.
Field `field-6` (:answer-field.type/blank).

1. `3` — observed correct; mapped to k+B.
Field `field-3` (:answer-field.type/blank).

1. `6` — observed correct; mapped to h+A.
Field `field-1` (:answer-field.type/blank).

1. `-6` — observed correct; mapped to h−A.

#### q-327866

Parameters: {'a': '-9/2', 'b': '5/3', 'h': 0, 'k': 0}. Template/profile: q-327866 / none.

Field `field-1` (:answer-field.type/blank).

1. `-\frac{9}{2}` — observed correct; mapped to h−A.
Field `field-3` (:answer-field.type/blank).

1. `\frac{9}{2}` — observed correct; mapped to h+A.
Field `field-2` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-5` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-4` (:answer-field.type/blank).

1. `-\frac{5}{3}` — observed correct; mapped to k−B.
Field `field-6` (:answer-field.type/blank).

1. `\frac{5}{3}` — observed correct; mapped to k+B.

#### q-327871

Parameters: {'a': '5/2', 'b': '3/4', 'h': 0, 'k': 2}. Template/profile: q-327871 / none.

Field `field-3` (:answer-field.type/blank).

1. `\frac{5}{2}` — observed correct; mapped to h+A.
Field `field-4` (:answer-field.type/blank).

1. `\frac{5}{4}` — observed correct; mapped to k−B.
Field `field-1` (:answer-field.type/blank).

1. `-\frac{5}{2}` — observed correct; mapped to h−A.
Field `field-5` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-2` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-6` (:answer-field.type/blank).

1. `\frac{11}{4}` — observed correct; mapped to k+B.

#### q-327880

Parameters: {'a': 4, 'b': '-7/2', 'h': 1, 'k': 0}. Template/profile: q-327880 / none.

Field `field-2` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-6` (:answer-field.type/blank).

1. `\frac{7}{2}` — observed correct; mapped to k+B.
Field `field-5` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-4` (:answer-field.type/blank).

1. `-\frac{7}{2}` — observed correct; mapped to k−B.
Field `field-3` (:answer-field.type/blank).

1. `5` — observed correct; mapped to h+A.
Field `field-1` (:answer-field.type/blank).

1. `-3` — observed correct; mapped to h−A.

#### q-327884

Parameters: {'a': '-4/3', 'b': '5/2', 'h': '1/3', 'k': '-7/3'}. Template/profile: q-327884 / none.

Field `field-4` (:answer-field.type/blank).

1. `-\frac{29}{6}` — observed correct; mapped to k−B.
Field `field-3` (:answer-field.type/blank).

1. `\frac{5}{3}` — observed correct; mapped to h+A.
Field `field-2` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-5` (:answer-field.type/blank).

1. `\le ` — observed correct; mapped to \le (left/upper relation according to original placement).
Field `field-6` (:answer-field.type/blank).

1. `\frac{1}{6}` — observed correct; mapped to k+B.
Field `field-1` (:answer-field.type/blank).

1. `-1` — observed correct; mapped to h−A.

#### q-70523

Parameters: {'a': 1, 'b': 6, 'h': 5, 'k': -7}. Template/profile: q-70523 / observed:q-70523.

Field `selection` (:answer-field.type/radio).

1. `1\le x\le 5,\,-9\le y\le -2` — observed wrong; mapped to bank formula tuple 1.
2. `-2\le x\le 13,\,3\le y\le 7` — observed wrong; mapped to bank formula tuple 2.
3. `4\le x\le 6,\,-13\le y\le -1` — observed correct; mapped to bank formula tuple 3.
4. `0\le x\le 5,\,-7\le y\le 0` — observed wrong; mapped to bank formula tuple 4.
5. `-6\le x\le 0,\,1\le y\le 7` — observed wrong; mapped to bank formula tuple 5.

#### q-73626

Parameters: {'a': -2, 'b': 2, 'h': 1, 'k': -3}. Template/profile: q-73626 / observed:q-73626.

Field `selection` (:answer-field.type/radio).

1. `2\le x\le 5,\,1\le y\le 5` — observed wrong; mapped to bank formula tuple 1.
2. `-1\le x\le 3,\,-5\le y\le -1` — observed correct; mapped to bank formula tuple 2.
3. `1\le x\le 4,\,-1\le y\le 5` — observed wrong; mapped to bank formula tuple 3.
4. `1\le x\le 6,\,-5\le y\le -1` — observed wrong; mapped to bank formula tuple 4.
5. `-1\le x\le 0,\,-5\le y\le 0` — observed wrong; mapped to bank formula tuple 5.

#### q-73632

Parameters: {'a': 2, 'b': '1/2', 'h': 1, 'k': '3/2'}. Template/profile: q-73632 / observed:q-73632.

Field `selection` (:answer-field.type/radio).

1. `-2\le x\le -1,\,-1\le y\le 3` — observed wrong; mapped to bank formula tuple 1.
2. `-3\le x\le 1,\,-2\le y\le 1` — observed wrong; mapped to bank formula tuple 2.
3. `-1\le x\le 3,\,1\le y\le 2` — observed correct; mapped to bank formula tuple 3.
4. `1\le x\le 3,\,-1\le y\le 2` — observed wrong; mapped to bank formula tuple 4.
5. `-1\le x\le 2,\,1\le y\le 3` — observed wrong; mapped to bank formula tuple 5.

#### q-123773

Parameters: {'a': -1, 'b': 1, 'h': 1, 'k': 2}. Template/profile: q-123773 / observed:q-123773.

Field `selection` (:answer-field.type/radio).

1. `-2\le x\le 0,\,-3\le y\le -1` — observed wrong; mapped to bank formula tuple 1.
2. `-1\le x\le 1,\,1\le y\le 3` — observed wrong; mapped to bank formula tuple 2.
3. `-1\le x\le 1,\,-3\le y\le -1` — observed wrong; mapped to bank formula tuple 3.
4. `0\le x\le 2,\,-2\le y\le 2` — observed wrong; mapped to bank formula tuple 4.
5. `0\le x\le 2,\,1\le y\le 3` — observed correct; mapped to bank formula tuple 5.

#### q-123775

Parameters: {'a': '1/2', 'b': 1, 'h': 0, 'k': 3}. Template/profile: q-123775 / observed:q-123775.

Field `selection` (:answer-field.type/radio).

1. `-2\le x\le 2,\,-4\le y\le -2` — observed wrong; mapped to bank formula tuple 1.
2. `-2\le x\le 2,\,-3\le y\le 3` — observed wrong; mapped to bank formula tuple 2.
3. `-\frac{1}{2}\le x\le \frac{1}{2},\,-3\le y\le 3` — observed wrong; mapped to bank formula tuple 3.
4. `-\frac{1}{2}\le x\le \frac{1}{2},\,2\le y\le 4` — observed correct; mapped to bank formula tuple 4.
5. `1\le x\le 3,\,2\le y\le 4` — observed wrong; mapped to bank formula tuple 5.

## 4. Reusable template, constraints and calculations

Fixed: parameter domain 0≤θ<2π, sine/cosine roles, independent coordinate method, source field ownership, radio count=5, blank count=6, exact math answer type and fragment shape. Variable slots are the **whole coordinate formula**, **whole aligned row block**, and **whole concluded coordinate interval**. Coordinate text is rendered directly from current parameters into the unchanged prose skeleton. Slots never globally replace a short numeral/function/variable across unrelated prose. First-shift notation, sign reversal and omission of unit scaling are conditioned on extracted source structure; explicit guards preserve these regimes.

For each coordinate compute L=d−|c| and U=d+|c| exactly with SymPy Rational. Every printed intermediate inequality is independently parsed and checked against the actual displayed coordinate formula over trig value [-1,1]. The domain remains half-open in θ while output endpoints remain attained/closed. Source replay compares complete prompt and worked solution byte-for-byte, plus every field's type/key/bank/correct designation mathematically, allowing harmless answer whitespace/fraction notation normalization. q-70341's missing solution/designation is excluded only from those absent-value denominators, not from prompt/bank coverage.

Normal radio generation chooses one complete authored method bank. If h=k=0 the five entries are: C, restricting both trig functions to [0,1], doubling both amplitudes, halving both amplitudes, swapping amplitudes. If at least one shift is nonzero they are: C, omitting both shifts, doubling both amplitudes, halving both amplitudes, negating both complete ranges. These are separately labeled bank extensions; their cardinality matches the sources. Every option is computed before validation; the whole instance is rejected for reversed ranges, equivalence, a correct distractor or collisions. There is no first-valid candidate pool or post-hoc replacement of a wrong option.

Observed profiles are selected explicitly by `observed:<source-id>`, preserving their complete bank. Invalid explicit inputs raise; random sampling rejects and resamples the whole instance under the already chosen complete profile. Blanks never acquire distractors. One fixed solution is generated independent of selected wrong options.

Presentation identity hashes version, level, template, complete bank/profile/layout, canonical parameters, displayed prompt and fixed solution, excluding seed and choice order. Mathematical-task fingerprint separately canonicalizes the actual two affine trig formulas and fixed domain, excluding layouts and profiles. Hence radio/blank presentations of the same assessed formulas deduplicate mathematically while differing display banks remain separate content records.
