# Two-pivot Gauss–Jordan generator repair

The learner constructs the augmented matrix, uses Gaussian elimination to expose
two unit pivots, and clears the entry above the second pivot. For solution-vector
questions the learner then discards the identity 0=0 and expresses x and y in
terms of free variable z. The response is one of five radio options, with exactly
one correct matrix or general solution vector. All 17 assessed sources are hard;
easy and moderate are unsupported. No diagrams occur or are needed.

Source evidence is the supplied source.json, material.kp.questions, captured at
basis 5370; evidence/assessed-source.json retains every complete assessed record.
Tutorial 3949, “Using the Gauss-Jordan Method on a 3x3 System With Two Pivots,”
requires echelon reduction with unit pivots, then says to make the entry above
a22 zero “if a12 != 0.” Thus clearing that entry is conditional, not an obligatory
extra operation. The canonical e-6233 (283e9a4a-443f-579f-b272-248446d3a49f)
explains the zero equation and basic versus free variables. Prerequisite topic
1374 supplies Gaussian elimination and interpreting singular-system solutions.
The adjacent one-pivot and inconsistent-system examples establish topic
boundaries, not additional generated families.

q-74625 (8e9b3735-f721-557c-bd19-98de1fb72ed8) already has its second unit
pivot; eliminating row 3 and adding 3 R2 to R1 yields rows [1,0,-5,8],
[0,1,-2,3], [0,0,0,0]. q-131634
(c0791632-977c-5714-8eb6-2845fc127f35) needs second-pivot normalization
but no backward clearing; its RREF has rows [1,0,3,3], [0,1,1,2], [0,0,0,0].
Both profiles were omitted from the old 15-record snapshot. This is a registry
completeness defect, not a mathematical exception. Repair the snapshot from all
supplied assessed records and verify exact external source-ID coverage so a stale
subset cannot silently define its own coverage obligations. Preserve the existing
15 records, complete banks, solution prose, formatter, and authored sampler.

Fixed features have instructional reasons: three equations in three variables
keep the assessed dimension; rank two and consistency give one free variable;
pivots in columns x and y implement tutorial 3949's particular algorithm; five
radio choices retain the observed response contract. Original matrix versus
vector commands remain separate response families. All source banks replay,
including text distractors and higher-rank wrong matrices. Source q-74627's
scaling label mistakenly names R3 after the swap; the existing correction to R2
must remain. Augmented-matrix formatting normalization is also retained.

The existing authored extension uses five distinct affine tuples
(sx,sy,bx,by), representing x=sx*z+bx and y=sy*z+by. It chooses the correct
slot first, then exchangeable tuples, then constructs the equations with the
selected source's first two coefficient columns. The construction preserves
rank, dependence, forward elimination workload, and any conditional backward
step. Slopes -3..3 and intercepts -4..4 bound arithmetic without introducing a
new method. These bounds are an authored practice domain, not limits on exact
source replay (some original slopes are larger). Distractors in sampled records
are other affine solutions, an existing conservative extension rather than
claimed reconstructions of every source misconception. Their exchangeability
avoids a unique shape or sign advertising the answer. Row permutation and signs
are supported controlled presentation parameters; ordinary sampling retains the
source coefficient layout. No new bank design or domain change is needed here.

The answer-bearing role is the affine tuple agreeing with the equations, and its
assignment can be any of the five displayed candidates within every profile.
Varying that assignment with the bank fixed must change the prompt, key, and
worked reduction together. Permuting or negating equations must preserve the
solution and selected option. Coverage obligations are all 17 source IDs and
complete replay banks; sampled generation for every profile; both response
families; all correct slots; positive, negative and zero affine parameters;
unit-pivot, scaled-pivot, swap, and already-cleared backward cases. Numerical
changes preserve the reduction method rather than adding topics. Check visible
systems, answers, and worked matrices independently; use the native grader for
every candidate in affected and representative cases. Compare shortcut probes
before and after the actual delivery filter. Original source questions in the
inventory must not be reclassified as generated; missing replay capability alone
does not demonstrate a defective stored generated instance. Missing generation
metadata limits historical seed reproduction and live selection claims.
