# Template extraction

## 1. Specific originals

q-20407: 297x297 diagram, black c descends right; one blue unit scale spans two pale grid squares. Tail (2,4.5), tip (4,1) in a grid frame, displacement (2,-3.5). Requested scalar multiple of c, five radio choices. Correct value derived independently is 2c/sqrt(65). Raw source has no solution, correct reference or difficulty.

q-19276: 297x297 diagram; A at (1,2.5), joint at (3.5,1), B at (5,4); q=(2.5,-1.5), r=(1.5,3), resultant (4,1.5). Both arrows are head to tail, black q/r labels; blue unit scale is two squares. Five radio choices include single-r and separately scaled q/r expressions. Correct complete vector is 2(q+r)/sqrt(73). No solution/correct reference/difficulty captured. Owning local 1104 JSON confirms the complete radio widget and every choice; it supplies no missing worked solution or designation.

q-119805: 224x249 prompt/solution rasters. A=(1.5,1.5), joint=(2.5,1), B=(1,3.5) in a convenient origin frame, m=(1,-0.5), n=(-1.5,2.5). Resultant is (-0.5,2). Solution red dashed AH horizontal left and HB vertical up; red resultant points A to B. Formal stages: triangle addition; solution diagram; right angle and AH=0.5=1/2, BH=2; |m+n|=AB; square root of squares; substitute; evaluate individual squares; sqrt17/2; normalize, then 2(m+n)/sqrt17. No answer field captured. Source worked solution supports the authored field independently.

Canonical e-5181: single a from lower left to upper right with displacement (3,2); solution dashed red AH=3 horizontal and HB=2 vertical. This establishes the authored integer-leg easy workload.

## 2. Shared pattern

Read a nonzero displacement from a scaled grid, optionally identify the tail-to-final-head resultant of two slanted arrows; construct the right triangle; apply Pythagoras; divide the vector by its magnitude. The response is a complete scalar multiple of the displayed vector or vector sum. Parallel includes opposite direction mathematically: correctness checks use both parallelism and length one. Normal prompts minimally say to choose the same-direction unit vector; observed prompts retain their wording. There is no eligible negative unit-vector distractor in the observed banks.

## 3. Complete component and bank mapping

Similarity parameter s>0 multiplies each observed displacement. Opaque replay formulas generalize by similarity only, preserving original complete values; their constants are observed ratios, not recovered error operations.

|Bank|Every displayed choice at s=1|Parameterized complete value|Designation|
|---|---|---|---|
|observed_c|c/sqrt65|c/sqrt(65s²)|wrong|
|observed_c|c/sqrt55|c/sqrt(55s²)|wrong|
|observed_c|sqrt65 c/4|sqrt(65s²)c/4|wrong|
|observed_c|2c/sqrt55|2c/sqrt(55s²)|wrong|
|observed_c|2c/sqrt65|2c/sqrt(65s²)|inferred correct|
|observed_qr|r/sqrt29|r/sqrt(29s²)|wrong|
|observed_qr|(q+r)/5|(q+r)/(5s)|wrong|
|observed_qr|2q/sqrt13+r/sqrt29|2q/sqrt(13s²)+r/sqrt(29s²)|wrong|
|observed_qr|2(q+r)/sqrt73|2(q+r)/sqrt(73s²)|inferred correct|
|observed_qr|(q+r)/sqrt13|(q+r)/sqrt(13s²)|wrong|

No polynomial fit or inferred operation explanation is promoted to learner defaults. Both observed banks have evidence_only=true and eligible_for_learning=false. Note that the source sqrt13/sqrt29/sqrt55 denominators do not uniquely disclose their arithmetic errors. The source sqrt65 c/4 entry under changed s remains literal parameterized observed syntax; its varying effect is checked by whole-bank rejection.

Authored_method is one indivisible five-operation bank: v/L (correct); v/L² (omit square root); Lv (multiply by length); v/|horizontal leg| (omit the vertical contribution); 2v/L (wrong unit scale). Every whole instance is rejected if any pair is mathematically equivalent or another option satisfies unit parallelism. No pooled replacement options and no learner-facing error diagnoses.

## 4. Reusable templates and bounds

Single prompt keeps source opening and one image. Sum prompt identifies the vector sum from the diagram. Formal worked solutions keep the canonical right-triangle/Pythagorean and normalization sentences and ordered unevaluated substitution/square-evaluation rows. The hard observed solution uses a full extracted mask that preserves original prose and exact sequence; changed parameters fill complete mathematical components.

Easy: signed integer legs, absolute magnitudes 1..5, two nonzero components. Moderate: signed half-grid legs, magnitudes 0.5..4, at least one strictly half-integral leg. Hard: two slanted head-to-tail vectors; each nonzero half-grid component magnitude at most 4; at least one cancellation; both resultant components nonzero; at least one resultant component strictly half-integral. Levels contain unordered orientations and leg choices at their own workload. Explicit inputs enforce the same guards. These are author policies, not inferred labels.

Source profiles accept only their extracted geometry under positive similarity (c moderate, q+r hard). Mathematical fingerprints contain both geometric displacements, grid increment and template, excluding seed, names and bank/profile. Presentation identity hashes actual prompt, fixed solution and complete bank; shuffled order does not change identity.

Source repairs: infer the two absent correct refs from full actual geometry; assign authored unrated levels; author missing solutions from canonical instructional stages; author hard's missing radio field and method bank. Raw omissions are not called exact designation/field fidelity. No mathematical source errors were found after checking all ten complete observed choices against the actual criterion.

Public raw_c/raw_qr/raw_hard replay profiles derive the same parameterized objects/banks but retain every absent source assessment attribute: no fabricated rating, solution or correct reference for the two unrated radios, and no answer field for the hard record. Their original prompt/available solution image-reference spelling is preserved byte-for-byte at source parameters. source-cases.json identifies these original replay profiles separately from completion_profile. raw-review.json records those public raw results. Completed observed_c/observed_qr add inferred designations, authored ratings and worked solutions; observed_hard adds the authored field/bank. All raw profiles are evidence-only and ineligible for learning. Stable identities are checked across changed seeds for both raw and completed profiles.

Similarity scope is the bounded catalog s in {1,2}; the source originals have s=1. This preserves half-grid endpoint reading and excludes huge, tiny or quarter-grid explicit scales. Raw profiles enforce this same bound. Absolute image-root normalization is counted separately for completed source replay; public raw source prompts/available solution retain the exact original strings.
