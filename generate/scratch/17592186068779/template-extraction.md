# Four extraction stages

## 1. Specific source observations

All ten questions say “Which of the following is the graph of” a supplied transformed reciprocal. q-16508 uses y=-2/(x+1); q-98003 uses y=-1/(2x)+1 and both omit solutions and correct refs. Four rated moderate examples supply a rational/integer scale multiplying1/x plus a vertical integer offset; four rated hard examples supply a rational/integer scale multiplying1/(x-h), with h=±1 or2. Full source prompts and solutions remain in source.json and review.md.

The moderate solution stages are opening → signed unit reciprocal → vertical stretch → vertical translation. Three sources illustrate every stage, while q-98013 illustrates only the final graph. Hard stages are opening → signed unit reciprocal → horizontal translation → vertical stretch. Each profile has its own exact source prose skeleton, punctuation, image order, and omitted attributes. Raw masks replace complete equation nodes and scalar nodes in their original order, with sign/direction-dependent prose. Introductory stale offsets are explicit parameter slots in raw evidence; they are corrected independently in normal output.

## 2. Shared pattern and response

Recognize the complete graph of y=a/(x-h)+k from the supplied equation, by base-curve sign, translation and scale. Five-image radio contract; one fixed worked solution per instance, no response-dependent diagnosis. A nonzero shift is compulsory; pure stretches belong to earlier sibling KPs. No coefficient solving, intersections, domain/range questions, or new functions are introduced.

## 3. Complete observed banks

The following tuples are (a,h,k), in original option order. Values with a coherent pair of marked coordinates are determined **within the shown reciprocal-family shape** by the marked points and labelled asymptotes. These are geometric recipes; author error intention is inferred only where a visible operation supports it. All options, including wrong-wrong pairs, are compared as complete displayed graphs.

| Profile | Complete bank | Pattern supported by whole bank |
|---|---|---|
| q-16508 | (-1,-1,0),(2,-1,0),(-2,1,0),(-2,-1,0),(-1,1,0) | correct; omitted stretch; reversed sign; reversed horizontal shift; reversed shift with omitted stretch |
| q-98003 | (-1/2,0,1),(-1,0,1),(-1/2,1,0),(1/2,0,1),(1/2,1,0) | correct; omitted stretch; vertical offset moved to horizontal shift; reversed sign; compounded sign/horizontal-offset error |
| q-113372 | (4/5,0,3),(-4/5,0,3),(4/5,0,0),(-4/5,0,0),opaque fifth graph | correct; reversed sign; omitted vertical translation; both; fifth graph has x=-3 and inconsistent y labels (not a recovered tuple) |
| q-113466 | (-1,2,0),(2,2,0),(-2,2,0),(2,-2,0),(-2,-2,0) | omitted stretch; reversed sign; correct; both sign/shift reversal; shift reversal |
| q-98013 | (5/2,-2,0),(-5/2,0,2),(5/2,0,2),(-5/2,0,-2),(5/2,0,-2) | vertical shift moved to horizontal; sign and vertical-shift reversals; reversed vertical shift; reversed sign; correct |
| q-98017 | (1/4,0,1),(-1/4,0,-1),(1/4,0,-1),(1,0,-1),(-1/4,0,1) | reversed vertical shift; reversed sign; correct; omitted stretch; both reversals |
| q-98022 | (-2,1,0),(2,-1,0),(-2,-1,0),(2,1,0),(1,1,0) | reversed sign; reversed horizontal shift; both; correct; omitted stretch |
| q-113369 | (-5,0,2),(5,-2,0),(-5,-2,0),(-5,0,0),(-5,0,-2) | correct; shift moved horizontal and sign reversal; shift moved horizontal; omitted vertical shift; reversed vertical shift |
| q-113463 | (3/4,-1,0),(-3/4,-1,0),(3/4,1,0),(1,1,0),(-3/4,1,0) | reversed shift; both sign/shift; correct; omitted stretch; reversed sign |
| q-98004 | (1,-1,0),(-1/2,-1,0),(1/2,1,0),(1/2,-1,0),(-1/2,1,0) | omitted stretch; reversed sign; reversed shift; correct; both |

The geometric continuation multiplies each observed coefficient by its anchor ratio to a, except signed unit curves represent omitted stretch; nonzero h or k components use the corresponding assessed shift and its observed sign. This parameterization is declared before sampling. It is a defensible continuation of the visible bank, not a claim to recover original generator code. The opaque fifth option is a declared evidence-only model continuation (a_model=5a,h_model=-k,k_model=0), preserving its raw image at the anchor; the anchor coefficient and y-scale remain uncertain. It is never normal sampled.

## 4. Backbone, slots and constraints

Fixed: complete reciprocal graph request; variable x and output y; base sign curve; five image choices; source profile's ordered stages and optional image layout. Variable: exact reduced coefficient a, nonzero signed integer shift h or k, sign/direction grammar, labelled points at h±1 and derived outputs, all dependent curve/asymptote geometry. Source q-98013's horizontal distractor uses h±1/2; the opaque q-113372 model uses h±4/5. Those original point-placement roles are retained when source profiles change.

Parameter bounds apply equally to explicit inputs and sampling. Normal easy |a|=1 and exactly one translation. Moderate h=0,k≠0, |a|≠1. Hard h≠0,k=0, |a|≠1. Magnitudes of integer shifts are1–4; coefficient reduced numerator/denominator are at most5. Complete banks are selected before parameters and rejected together on any duplicate graph. No first-valid distractor pool is used. Normal sampling serves all nine eligible original-shaped banks and the authored bank, with coverage checked over default seeds.

Authored bank operations: easy uses correct, sign reversal, shift reversal, omitted translation, and compounded sign/shift reversal. Moderate uses correct, sign reversal, omitted vertical translation, vertical reversal, and moving the offset into the denominator. Hard uses correct, sign reversal, denominator shift reversal, omitted stretch, and omitted horizontal translation. Every distractor comes from the displayed transformation method.

Identity is based on version, actual prompt, fixed solution, complete sorted bank, correct value/presence and actual difficulty/presence; seed and option order are excluded. The mathematical fingerprint is the canonical complete reciprocal function and assessed supplied information, excluding profiles and bank contents. Different levels cannot admit the same normal task under these bounds. Raw omission profiles can represent the same mathematics with incomplete evidence.
