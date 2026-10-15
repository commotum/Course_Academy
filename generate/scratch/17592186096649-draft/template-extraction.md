# Template extraction

## 1. Specific source descriptions

q-11324 depicts a black vector pointing30° above the horizontal, length approximately100 raster pixels. The prompt asks which diagram shows3a and−a. Five images label blue3a and orange−a. Two of the blue vectors have length3|a|, three have length|a|. Orange vectors include the true reversed base length, horizontal right base length, reversed double base length, and horizontal left double base length. The selection field contains five image values. Difficulty, correct and worked-solution attributes are absent, rather than empty. Full source bytes remain in source.json and public raw replay.

q-12140 depicts a black vector pointing60° above the horizontal, length approximately198 raster pixels. The prompt asks for−a/2. The five orange diagrams are reversed half length, reversed full length, horizontal right half length, horizontal left half length, and forward full length; all carry the requested−a/2 label. It has the same absent attributes. Its source prompt uses delimiter math with fraction TeX and has no answer placeholder requirement because the response is radio.

## 2. Generalized pattern

Given a nonzero vector diagram, construct the precise requested scalar multiple or pair of scalar multiples. Magnitude multiplies by the absolute scalar. Positive scales preserve direction; negative scales reverse it. Translation of arrows is incidental; length and direction must agree with the requested expression. A radio option is valid only if every labelled arrow is the specified multiple. Mere parallelism is insufficient, and no arbitrary representative parallel vector is assigned a unique key.

## 3. Component and entire bank map

Let a=L(cosθ,sinθ), and H(t)=(tL,0). Rows below are in capture order. Each label remains the requested scalar multiple, including when its drawn arrow is wrong. These are explicit geometric parameterized recipes; original error intentions are unresolved hypotheses. No fitted scalar perturbations are used.

| Source/profile | Parameters | Capture options1–5 | Exact matching value/path evidence | Key evidence |
| --- | --- | --- | --- | --- |
| q-11324 / observed_pair | θ30°,L1,m3,n−1 | (ma,na);(ma,H(−n));(a,2na);(a,na);(a,H(2n)) | all five original paths in source.json, measured tail/tip in source-raster-checks.json | option1 independently satisfies both labels; captured correct absent |
| q-12140 / observed_single | θ60°,L2,k−1/2 | ka;2ka;H(−k);H(k);−2ka | all five original paths in source.json, measured tail/tip in source-raster-checks.json | option1 independently satisfies label; captured correct absent |

The12-entry raster evidence records every original prompt and every answer separately, including sizes, hashes, pixel tail/tip coordinates, arrowhead directions and raster centerline support. Vector ratios compare under each prompt's own scale, with0.035 normalized-coordinate tolerance for integer pixel endpoint/antialias uncertainty. These are ungridded length/direction diagrams; the inferred exact30°/60° geometry is consistent with the full bank and familiar source drawing angles, not an invented coordinate-grid reading task.

Source field and answer attribute sets are exact under raw public replay. Only nested captured enums become strings in the established local interface. Original IDs and database attributes are preserved at original geometry. Raw missing attributes stay absent. Completed public profiles add explicitly inferred keys, solutions and authored call-level difficulty; these remain evidence-only and are checked separately by the real engine.

## 4. Reusable masks and policies

Paired prompt: image, blank line, `The vector $a$ is depicted above. Which of the following diagrams shows the vectors $[m]a$ and $[n]a$?` Single prompt: image, blank line, `The diagram above shows the vector $a$. Which of the following diagrams shows the vector $[k]a$?` Scalars1/−1 omit the numeric1; other integers/fractions use source notation. All five images belong to one full selected bank. Complete-bank collisions reject the whole instance before rendering; angle 0 raw pair is correctly rejected because its horizontal replacement equals the correct−a option.

There are no captured practice solutions to reproduce. The normal fixed solution is explicitly authored from canonical shared prose: parallel opening; Now/Next sections; magnitude sentence; sign/direction sentence for each requested vector; final correct diagram. It does not invent option-specific feedback. It does not add coordinate algebra or rows absent from this diagram skill. The complete source canonical discussion and image structure are retained as context in source.json. An already correct magnitude relation uses the absolute scalar regardless of sign.

Normal profile authored_operations (chosen before sampling) has five operations. Single: k·a, −k·a, (1/k)·a, −(1/k)·a, a. Pair: (ma,na), (−ma,na), (ma,−na), (a/m,na), (ma,a/n). These represent sign reversal, reciprocal length instead of scaling, and omission of scaling. They form complete banks, never a first-valid pool. All displayed labels are the requested values, so wrong diagram geometry cannot masquerade as a different label.

Finite bounds, identical for explicit and sampled inputs: orientation∈{0,30,60,120,210,300}°; base length∈{1,2}; positive integer scale∈{2,3,4}; negative rational scale∈{−1/2,−2/3,−3/2,−4/3}. Easy uses one positive integer; moderate one negative rational; hard a positive integer and negative rational together. These are source-familiar enlargement, fractional length and reversal operations, all requiring the same steps within each level. Inference replay additionally permits the observed paired−1 and always remains evidence-only.

Meaningful task fingerprints include orientation, specified reduced scale(s), arity and response criterion. Common base length, translations, option order and bank alias are incidental and excluded from task counts. There are18 easy,24 moderate,72 hard meaningful tasks (114 total); changing common base length doubles presentations, not mathematical tasks. Content identities include version, actual difficulty, full prompt, fixed solution and whole displayed bank; order/seed cannot change them. The observed raw question identifiers match the original snapshot only at original geometry; changed raw geometries receive generated identities.

Normal records retain the source image radio layout and five owned answers. Grading tests select every correct/incorrect owned UUID using the real application grader. This interface accepts image choices; it cannot accept a learner's independently drawn equivalent translated diagram. That representational limitation is documented without changing the engine or asserting mathematical uniqueness for underdetermined prompts.
