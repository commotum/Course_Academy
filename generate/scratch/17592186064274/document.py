"""Record extraction and bounded capabilities for this KP only."""
import collections,hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
import validate as v
p=Path(__file__).resolve().parent;g=v.g
snapshot=g.SNAPSHOT;kp=snapshot['rows'][0][0];templates=collections.defaultdict(list)
for mid,profile in g.PROFILES.items():templates[profile['kind']+'-'+profile['field_type'].split('/')[-1]].append(mid)
domain={g.task_fingerprint(g.parameters(mid,s,k)) for mid in g.PROFILES for s in range(1,13) for k in range(1,9)}
cap={'supported_levels':['moderate'],'unsupported_levels':['easy','hard'],'unsupported_levels_filled':False,'exceptions':[{'difficulty':l,'bounded_capability':'unsupported by this source-derived package','evidence':'All 23 rated sources, including unit coefficients, signed coefficients/frequencies, rational and pi bounds, radicals, cancellation, symmetry and nonzero lower bounds, are moderate. The package preserves one full IBP setup, a remaining elementary integral and exact endpoint evaluation. Larger/smaller coefficients do not establish a calibrated different band. Adding repeated IBP or deleting the assessed steps changes the extracted backbone. No independently validated easy/hard template is available. This is a bounded content capability, not a claim that such a level is mathematically impossible. New source evidence reopens classification.','target':5,'available':0,'shortage':5} for l in ('easy','hard')],'parameter_policy':{'scale':'positive integer 1..12','dilation':'positive integer 1..8','source_signs_and_shapes':'retained','scope':'finite conservative dilation of observed source integral and complete answer bank'},'raw_parameter_combinations':len(g.PROFILES)*96,'distinct_mathematical_tasks':len(domain),'finite_limit_behavior':'deduplicate against all original, canonical and generated tasks, never relabel/reshuffle/seed to fill a shortage; document residual shortage when the bounded domain is exhausted'}
(p/'capabilities.json').write_text(json.dumps(cap,indent=2)+'\n')
(p/'classification.md').write_text(f'''# Classification at basis {snapshot['basis']}

Lineage: 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. KP {g.KP_ID}: {kp[':knowledge-point/title']}.
Read all 23 source practice questions and the canonical example together, including complete fields, correct values, choices and worked solutions, in `source.edn`. No source generator was registered. The canonical example supports the sine backbone and is excluded from inventory.

All 23 sources are moderate: 15 radio fields (five choices, key selection) and eight blank fields (one exact math answer, key field-1). Each question has exactly one field. There are six mathematical/response templates, listed below. Wording variants (Evaluate; Evaluate the integral; equality; exact-entry instructions) stay attached to their source profiles. Each of the 15 radio banks is a separate observed profile; blanks have no distractor profile.

'''+ '\n'.join(f'- {t}: '+', '.join(mids)+'; plots **none**.' for t,mids in templates.items())+'''

No images or plots occur in prompts, choices or solutions. Plot extraction and generation are not applicable. No source mathematical discrepancies were found by independent definite integration and complete bank checks. Difficulty exceptions are bounded to this package and documented in capabilities.json; absence of source examples alone is not treated as impossibility.
''')
extraction={'basis':snapshot['basis'],'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','backbone':{'supplied':'definite integral c*x*f(b*x) with exact finite real bounds','requested':'entire exact scalar value of the definite integral','method':'u=c*x; differentiate u; integrate sine/cosine/exponential; IBP once; integrate remaining elementary function; substitute both endpoints; simplify','fields':'single radio with exactly five complete source options, or exact-value blank with one field-owned canonical answer','fixed_reason':'changing x to a higher power introduces repeated IBP; changing requested object or adding operations changes the assessed method','solution_prose':'the three instructional sentences are preserved; equivalent algebra rows are normalized rather than copying incidental line breaks'},'templates':dict(templates),'slots':{'profile':'choose an observed integral/bank and prompt variant before constructing the complete bank','scale':'integer 1..12, multiplies c0; source signed coefficient retained','dilation':'integer 1..8, multiplies b0 and divides both original bounds; preserves endpoint phases and branch/domain conditions','dependent_answer_and_bank':'every observed expression times scale/dilation²; derived from substitution t=dilation*x','solution':'all u, derivative, v, integrands, antiderivative and endpoint substitutions derive from those same parameters','target_variation':'not applicable: only the entire definite integral is queried'},'observed_sources':g.PROFILES,'conservative_generalization':'dilations and coefficient scaling of each observed source. This is an explicitly defined transported expression recipe, not an inferred cognitive-error model. Distinct source banks remain separate.','source_choice_accounting':'Every choice including distractors is retained in profiles.json with its exact TeX, parsed complete expression, source field profile and correct designation; source-replay.json contains matched/total values and missing/extra checks.','plot_specification':{'rating':'none','assets':[]},'finite_domain':cap['distinct_mathematical_tasks'],'source_errors':[]}
(p/'template-extraction.json').write_text(json.dumps(extraction,indent=2)+'\n')
(p/'README.md').write_text('''# Definite integration by parts

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186064274.py --seed 42 --profile q-349299 --json /tmp/ibp-preview.json
.venv/bin/python generate/scratch/17592186064274/validate.py
.venv/bin/python generate/scratch/17592186064274/replenish.py
```

Moderate only. The source-derived coefficient/frequency/bound slots and exact transported complete banks are documented in template-extraction.json and profiles.json. Generator output separates database content from provenance, recipes, seed and parameters. Blanks expect the full exact scalar value, without math delimiters. Math and distractors use SymPy; actual grading uses the existing application engine built in target/release. build-native.py copies only the read-only fixture harnesses into this KP package and records executable/library hashes. No application code is changed.

The public generator was executed for every source profile and four boundary/interior variants per profile. source-replay.json records mathematical/complete-bank fidelity; validation.json records independent displayed-math and grader checks. review.md pairs original-parameter replay with scale-only, dilation-only, combined and boundary variants. Original source prose/equations remain in source.edn. Source notation is normalized, and repeated arithmetic simplification rows may be combined; setup, parts substitution, remaining integration, endpoint evaluation and final simplification are retained.

Deduplicate by displayed integrand and bounds against source questions, canonical examples and all existing/generated content. A different seed, bank, answer UUID or option ordering never creates another task. Identity includes the bank profile to prevent collisions while preparation excludes task duplicates. Supported-level exhaustion is a finite-limit result; easy and hard remain explicit unfilled capability exceptions.

replenish.py uses the configured EDB integration and contributor, serializes with the application api.lock, recovers exact retained requests first, captures fresh inventory/basis, previews with installed native entity specs, persists the exact request, then submits with a basis guard and verifies the exact committed basis before releasing the lock. Source questions and learner facts are immutable.
''')
print('Templates',dict(templates),'finite distinct domain',len(domain))
