import importlib.util,json,re,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
rows=[]
for template,q in g.SOURCES.items():
 f=q[':question/answer-fields'][0];level=q[':question/difficulty'][':db/ident'].split('/')[-1]
 rows.append(f"| {template} ({q[':db/id']}) | {level} | {f[':answer-field/type'][':db/ident'].split('/')[-1]} / `{f[':answer-field/key']}` | {'none (unchanged normalized assets)' if template in g.DATA else 'light; fixed line/normal diagram, unsupported missing field'} | {'observed-scaled:'+template if template in g.DATA else 'no choices; excluded'} |")
(H/'classification.md').write_text(f'''# Open-curve flux classification

Captured math basis {g.SNAPSHOT['basis']}, lineage {g.SNAPSHOT['lineage']}.
The complete KP pull, canonical example, all 13 practice prompts, fields, owned answer banks, correct keys, worked solutions and image references are retained in source.json and reference/initial/kp.edn. No generator existed. The supplied .generated path did not exist at capture; the commit runner rechecks it.

There are six moderate radio templates, six hard radio templates and one hard blank template. Each radio is conservatively separate because its expression structure, substitution/integration workload or supplied curve changes. Every radio has one selection field, five math choices and one complete source bank profile. The blank has one field-1 math answer and no distractors. No easy or unrated practice occurs. Canonical e-9574 has no practice answer fields and is evidence only.

| Source | Level | Field | New plot requirement | Profile |
|---|---|---|---|---|
'''+ '\n'.join(rows)+'''

The moderate sources supply r(t) and its interval; hard radio sources supply an implicit/explicit curve and endpoints requiring parameterization. All 12 radios ask for total flux with the normal shown. Their solutions use a clockwise right normal, parameterize/verify traversal when necessary, substitute P and Q, differentiate x and y, then integrate P y' - Q x'. The diagram-based blank has no definition of F in its prompt or inspected plot, although its solution uses (3xy²,-y³). This missing context prevents standalone generation or inventory counting. Preserve it unchanged.

Easy is unsupported by this bounded package. There is no observed easy bank, and omitting parameterization/substitution/integration would change the instructional task. This is an evidence-limited capability exception, not proof that easy questions can never exist; new sources reopen it.
''')
sections=[]
for template,d in g.DATA.items():
 p,q,a,b,lo,hi,level=d;src=g.SOURCES[template]
 sections.append(f'''## {template} — {level}

Original field: P={p}, Q={q}. Path x(t)={a}, y(t)={b}, t in [{lo},{hi}]. Original correct value: `{src[':question/answer-fields'][0][':answer-field/correct'][':answer/value']}`. The exact source strings, punctuation, delimiters, paragraph structure and every original choice are in source.json. No source choice is pooled across profiles.

The expression structure is {str(p),str(q)}; zero/unit constants, signs, powers, rational functions and exponential/logarithmic substitutions are retained in those positions. Parameter scale=1 replays the original; normal scale is a positive integer from 2 through 9. Scale multiplies both entire field components, every substituted component, integrand, primitive, evaluated flux and every original complete bank value. It leaves curve, endpoints, integration bounds, right-normal role, answer type/count and reasoning stages fixed.

The requested object is the flux of this entire given field across this given open curve. Geometry stays fixed because this package samples a conservative field-only slot and reuses orientation diagrams. Other geometry could be a future extension; repeated source positions are not evidence that geometry is mathematically immutable. Source scale=1 is observed; scales 2..9 are a bounded same-method extension. Domain has no curve poles, cusps or branch crossings inside the stated intervals. Logs have positive arguments.

Profile `observed-scaled:{template}` maps every original answer a to scale*a. This is the exact expression recipe, including compound constants and signs. It reproduces the full mathematical value at scale=1. Error psychology is unresolved and is not invented. Complete per-choice values, owned source identities and correct designations are written in source-choice-mapping.json; each profile retains its five options, with no mixing or invented feedback.
''')
(H/'template-extraction.md').write_text('''# Template extraction

Backbone: preserve supplied path form and requested total flux, identify clockwise right normal, substitute field, calculate the two derivatives, form P y′ − Q x′ and integrate on the supplied domain. Hard profiles add source parameterization and endpoint/orientation checks before substitution. No new operations or response types are introduced.

The complete original source descriptions and rendered solution sequences are retained in source.json. Source replay preserves them byte for byte. For sampled variants, the full formula/normal/parameterization/illustration prefix and operative instructional sentences are reused; the component substitution, derivative and integral chains are filled from one instance. Every instance has a concrete worked solution independent of learner response. Blanks are excluded and never converted to radio.

'''+ '\n'.join(sections)+'''
## Context-dependent blank q-169206

The diagram gives L from (0,0) to (√2,-√2), a clockwise normal and a dashed circle. The field is absent. The solution implies P=3xy² and Q=-y³ and evaluates -4, but that cannot establish what was supplied to the learner. Do not invent a prompt, count it as a usable standalone question, or generate variants. This does not block the six supported hard radio templates.
''')
assets=[]
for template,q in g.SOURCES.items():
 for role,key in [('prompt',':question/problem'),('solution',':question/worked-solution')]:
  for ref in re.findall(r'!\[.*?\]\((.*?)\)',q[key]):
   path=Path('/media/jake/SSD/EDB/math')/ref;digest=hashlib.sha256(path.read_bytes()).hexdigest();assert path.stem==digest
   assets.append({'source':template,'role':role,'reference':ref,'sha256':digest,'reuse':template in g.DATA})
(H/'reference/assets.json').write_text(json.dumps(assets,indent=2))
(H/'plot-extraction.md').write_text('''# Qualitative diagram extraction

Every referenced source asset was opened locally and inspected in contact sheets. All 12 radio prompt plots show coordinate axes, a blue curve with traversal arrows/endpoints, a gray qualitative vector field and an orange right normal n. Their solution plots add a pink tangent T and a 90° clockwise relationship. No axes ticks, reference vector magnitude or color magnitude scale are supplied. The parabolic, reciprocal, logarithmic, straight, cubic and exponential paths match their stated domains. Normal directions match (y′,-x′) for the stated traversal, including the left/down normal on descending paths and upper/right normal on x=-ln(y).

Fixed components: background, unlabeled coordinate scale, path topology and endpoints, curve direction, normal placement, tangent and clockwise angle illustration. Variable field slot: one common positive scale. Since arrows are qualitative and use no magnitude calibration, common positive scaling leaves their directions and relative magnitudes unchanged; the same normalized visualization represents every variant. Thus this bounded package requires no new plots. Geometry and normal are never independently resampled. Zero or negative scale is rejected: it would invalidate the source field-direction cues. New geometry or independent component changes would require synchronized Matplotlib/TikZ plots and fresh visual validation.

The hard blank diagram contains L, its endpoint (√2,-√2), a right normal and a dashed circle; no field expression or field arrows supply F. It is an explicit missing-context exception.

reference/assets.json retains all 25 references, their prompt/solution roles and verified SHA-256 bytes in the existing content-addressed database store. No assets were modified or republished. Exact source-image order is retained by the generator. Source diagrams carry orientation information, so the supported sampling policy is intentionally narrow.
''')
caps={'supported_levels':list(g.SUPPORTED_LEVELS),'normal_variants_per_level':{'moderate':48,'hard':48},'source_replays_per_level':{'moderate':6,'hard':6},'exceptions':[{'level':'easy','status':'unsupported','nominal_shortage':5,'reason':'No easy source evidence; reducing required flux stages or inventing banks exceeds this bounded package. New source evidence reopens classification.'},{'source':'q-169206','status':'unsupported','reason':g.EXCLUDED['q-169206']},{'scope':'variation','status':'finite-limit','limits':{'moderate':48,'hard':48},'reason':'Twelve source profiles times eight positive scales. No duplicate seeds, identities or order permutations; curves and normal fixed for asset fidelity.'}],'unsupported_levels_filled':False}
(H/'capabilities.json').write_text(json.dumps(caps,indent=2))
(H/'README.md').write_text('''# Open-curve flux generator

Script: ../17592186179746.py. Validate with `.venv/bin/python generate/scratch/17592186179746/validate.py`; preview with `--difficulty moderate --seed 0 --count 5 --format json` (or markdown). Moderate and hard each support 48 bounded positive-field variants, separately from six source replays. Easy and the context-dependent blank are explicitly unsupported. No source content is changed.

The package records full source classification, field/choice extraction, diagram inspection, finite capability, source-bank replay, independent exact mathematics, stale-value mutation checks and actual learner grading. review.md displays originals beside scales 2 and 5. Replenishment rechecks native inventory, current/historical usage and source stability under api.lock. It reuses the existing registered generator UUID when present, preserves exact guarded requests and receipts under reference/replenishment, and verifies exact-basis attribution, scope and source preservation before writing the requested job result. Only this KP’s generator registration and additive generated content are permitted.
''')
