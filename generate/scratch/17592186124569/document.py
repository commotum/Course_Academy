from pathlib import Path
import importlib.util,json
H=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
intro=f'''# Classification at math basis {g.SOURCE['basis']}

KP {g.KP}: {g.TITLE}. Lineage `{g.SOURCE['lineage']}`. All 14 source practice questions and the canonical example were read together at this basis; the complete evidence is `reference/initial/source.json` and its exact EDB query/result.

All 13 rated practice questions are easy: 12 single radio fields with five whole-function equations, and one single blank expecting only the potential before `+C`. The remaining radio question is unrated, lacks a correct reference, and has no worked solution. There are no moderate or hard sources. The shared method integrates the x component with an arbitrary g(y), differentiates with respect to y, matches the second component, integrates g′, and substitutes. Distinct operations/primitive structures and the blank response shape remain separate templates. All prompts, banks and solutions have no plots or image references. Plot rating **none**.

The canonical example f=x²y−3y+C supports the method and easy classification; it is excluded from practice counts. Sources q-37346 and q-37343 are excluded from generator support with reasons below, never changed in EDB. q-168602 requires a preceding part that is absent from the standalone prompt. Its solution explicitly supplies F=(y³−1,3xy²+1); this premise is added only to new generated instances. The original standalone source is not counted as usable practice.

| Source | Difficulty | Response | Mathematical backbone / support |
|---|---|---|---|
'''
for name,q in g.QUESTIONS.items():
 f=q[':question/answer-fields'][0];level=q.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1]
 desc=g.EXCLUDED.get(name,'; '.join(g.CASES[name][:4]) if name in g.CASES else '')
 intro+=f"| {name} / {q[':db/id']} | {level} | {f[':answer-field/type'][':db/ident'].split('/')[-1]} ({len(f[':answer-field/choices'])} choices) | {desc} |\n"
(H/'classification.md').write_text(intro)
text='''# Template and complete-bank extraction

The generator supports 12 separate template/profile pairs, with one blank and eleven five-choice radio banks. Every source option, given derivative, primitive, and residual is explicitly mapped below. Choice-bank interpretation is deliberately literal: recipe j is k times the complete original potential expression B_j, followed by +C for radio equations. It is an exact structural expression recipe, not an inferred psychological error. For constants in distractors, k scales that explicit constant as well. The whole selected profile is used; recipes are never pooled across sources.

The sole variable is a common nonzero integer scale k in {-4,-3,-2,-1,1,2,3,4}. This is a conservative same-method generalization, not an observed independent coefficient domain. It scales the supplied vector field, x primitive, y residual, final potential, and complete choice bank together. The integration/differentiation operators, degrees, trig/exponential arguments, function arity, variable roles, and response layout remain fixed because altering them would change the observed method or workload. Negative scales introduce signs only, within the easy algebra used by the source. k=1 replays the complete original bank; all eight values are exhaustively validated. Different seeds and choice orders never expand this finite domain.

Each new solution preserves the shared source explanatory sentences and six ordered mathematical stages: gradient definition, the two derivative equations, x integration with g(y), y differentiation, residual matching/integration of g, and final substitution. Notation and aligned equations are normalized. Source replay fidelity is mathematical and field/bank fidelity, not byte-identical Markdown; the validation report distinguishes this from correctness and grading.

q-168602 is generated as a standalone question by supplying its explicitly recorded vector field. Its field key stays field-1, and the answer fragment excludes f(x,y)= and +C. Other supported sources retain key selection and five complete equations. q-81737 has y≠0; a potential is defined on either connected half-plane, with an independent arbitrary constant on each. Generated prompts explicitly state this domain. All other domains are R².

'''
for name,raw in g.CASES.items():
 q=g.QUESTIONS[name];f=q[':question/answer-fields'][0];ci=f[':answer-field/correct'][':answer/id']
 text+=f"## {name} / {q[':db/id']}\n\nOriginal prompt:\n\n"+q[':question/problem']+f"\n\nGiven P=`{raw[0]}`, Q=`{raw[1]}`; x primitive A=`{raw[2]}`; remaining H(y)=`{raw[3]}`. Original k=1; generated P=kP₀, Q=kQ₀, A=kA₀, H=kH₀. Profile `{name}-complete-bank`.\n\n| Option | Original exact answer | Recipe at k | Correct |\n|---|---|---|---|\n"
 for i,(a,b) in enumerate(zip(f[':answer-field/choices'],raw[4])):
  text+=f"| {i+1} | ${a[':answer/value']}$ | `k*({b})` {'(fragment)' if name=='q-168602' else 'then +C'} | {a[':answer/id']==ci} |\n"
 text+='\nOriginal worked solution, retained as fidelity evidence:\n\n'+q[':question/worked-solution']+'\n\n'
text+='''## Explicit exclusions and capability limits

q-37346 has no source level, key, or solution. Its bank is retained in source evidence but is not supported in this generator. q-37343 has a keyed equation x²y+y³+C and a competing equation x²y+y³ with the same gradient. No duplicate answer family is admitted. These are exclusions, not successful bank replays.

Moderate and hard are unsupported in this version: no rated source, separate response contract, or greater-workload template supports assigning those bands. Larger scales do not justify relabeling easy tasks. Each has nominal shortage five, filled=false, and classification reopens on new rated evidence or a separately reviewed template. The bounded generator has 96 distinct vector-field tasks before existing-content, presentation-history and reservation exclusions. That finite policy is not a claim of mathematical impossibility beyond the package.
'''
(H/'template-extraction.md').write_text(text)
(H/'plot-extraction.md').write_text('# Plot decision\n\nAll 14 source prompts, answer banks and worked solutions contain zero image/plot references. No plots carry input or solution information. All supported templates have rating none, and require no plot extraction, generation or publication.\n')
exceptions=[{'difficulty':l,'status':'unsupported','bounded_scope':g.VERSION,'evidence':f'All 13 rated practice sources at basis {g.SOURCE["basis"]} are easy. No source-backed {l} method or field layout; numerical rescaling does not establish a higher difficulty.','nominal_shortage':5,'filled':False,'reopen_on':'New rated evidence or separately reviewed template'} for l in ['moderate','hard']]
(H/'capabilities.json').write_text(json.dumps({'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'finite_variant_limit':96,'scale_domain':list(g.SCALES),'templates':list(g.CASES),'excluded_source_profiles':g.EXCLUDED,'exceptions':exceptions},indent=2)+'\n')
(H/'README.md').write_text('''# Reconstructing a potential from its planar gradient

Validated easy generator: `generate/scratch/17592186124569.py`. Run from the repository root:

```bash
.venv/bin/python generate/scratch/17592186124569.py --level easy --seed 7 --count 5 --output /tmp/potential-questions.json
.venv/bin/python generate/scratch/17592186124569/validate.py
.venv/bin/python generate/scratch/17592186124569/replenish.py --prepare
.venv/bin/python generate/scratch/17592186124569/replenish.py --commit
```

Python/SymPy generate exact questions. JSON includes field-owned stable UUIDs, complete equations or the exact blank fragment, concrete worked solution, source template/profile, scale, seed, domain, dependency version and generator version. Local review Markdown compares unchanged source parameters with changed signs/scales. The validator reads the rendered field, all answer values, and all six solution stages, exhausts the 96 distinct tasks, replays all 12 supported source banks, and exercises the real application grader. It keeps the two excluded source profiles and unsupported levels visible.

Replenishment rechecks the native inventory and this KP's complete bank at one basis, excludes historical presentations and reservations, mathematically validates current usable sources, and prepares only a shortage at easy. An already sufficient pool needs registration only. All EDB writes are additive through the existing integration and configured application contributor. The application api.lock is held from the final inventory read through exact-basis receipt/readback. Exact requests, receipts, contributor checks and verification are retained under reference/replenishment. No source question or learner state is modified.
''')
# Compact side-by-side review covering all profiles and both scale signs.
lines=['# Originals and variants\n']
for name in g.CASES:
 lines.append('## '+name+'\n\nOriginal:\n\n'+g.QUESTIONS[name][':question/problem'])
 for k in [-2,3]:
  r=g.generate('easy',17,name,{'scale':k});q=r['question'];lines+=['\nScale '+str(k)+':\n\n'+q[':question/problem']]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]+['\n'+q[':question/worked-solution']]
(H/'review.md').write_text('\n\n'.join(lines))
