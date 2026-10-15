"""Build the auditable extraction maps and concise side-by-side review."""
import sys
sys.dont_write_bytecode=True
import hashlib,importlib.util,json,re,shutil
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sys.path.insert(0,str(D));import texmath as tm
sp=importlib.util.spec_from_file_location('partial_docs',D.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def write(name,data):
    (D/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
for rel in ['generate/principles.md','generate/runs/current/worker-instructions.md',*[f'generate/docs/{name}.md' for name in ['3-classify','4-template-extraction','5-plot-extraction','6-template-generator','7-plot-generator']]]:
    shutil.copyfile(ROOT/rel,D/'reference'/Path(rel).name)
source_patterns={
 'tan-reciprocal':['V-V²/U²','1-V/U²','V²-U²','V/U²','C'],
 'base-exponential-tan':['C','1/ln(2)','T1','ln(2)-1','2T1-pi/2'],
 'sin-cos-linear':['-C','-T1+T2','C','V²-T1','-T1-V²'],
 'power-log-root':['T1','C','T1*V','-2T2','U+V'],
 'exp-log-power':['exp(V/U)+T2','C','exp(V)+T2','U*exp(V)+T2','T1'],
 'polynomial':['T1','V','N','U','C'],
 'sec-power':['C','2T2','T2','C/2','T1'],
 'root-reciprocal':['C/2','(T1-T2)/2','T1-T2','C','T1+2T2'],
 'cross-roots':['T2','sqrt(V)','C','T1','T1+T2/2'],
 'cos-log-sin':['-4V','U','C','2V','-T1-V'],
 'cot-polynomial':['T2','-2T1-T2','-3T2','C','-T1+2T2'],
 'log-power-exp':['-T1*T2','T1-N','T1*exp(V)','C','T1+T2/exp(V)']
}
banks=[];solutions=[];specific=[];domains=[]
for key,f in g.FAMILIES.items():
    domain={'template':key,'level':f['level'],'source_id':f['source'],'differentiated_role':'u = target independent variable','held_role':'v = other independent variable','function':str(f['h1']*f['g1']+f['sign']*f['h2']*f['g2']),'active_coordinate_domain':[str(z) for z in f['coords'][0]],'held_coordinate_domain':[str(z) for z in f['coords'][1]],'a_b_domain':'positive integers 1..4','n_domain':list(f['ns']),'m_domain':list(f['ms']),'target_domain':['x','y'],'point_order':'x coordinate first, y coordinate second, independent of target','normal_bank':['T1+T2','T1-T2','-T1+T2','T1','T2'],'normal_whole_bank_eligibility':'Every pair must be mathematically unequal; both term contributions nonzero; no replacing a failed member','source_profile_eligibility':'anchor-only and evidence-only because opaque wrong operations are underdetermined' if f['source'] else None}
    domains.append(domain)
    if not f['source']:continue
    q=g.ORIGINALS[f['source']];original_values=q[':question/answer-fields'][0][':answer-field/choices'];sol=q.get(':question/worked-solution');rows=tm.rows(sol) if sol else []
    banks.append({'source_id':f['source'],'template':key,'profile':'observed-'+f['source'],'field':'selection','field_type':'radio','source_correct_present':':answer-field/correct' in q[':question/answer-fields'][0],'interpretation':'Expression-pattern reproduction, not a claim to have recovered the learner error intent. Restrict profile to source anchor; normal variants use explicit method bank.','choices':[{'source_answer_id':a[':answer/id'],'raw_value':a[':answer/value'],'expression_pattern':pat,'role':'source correct' if a[':answer/id']==q[':question/answer-fields'][0].get(':answer-field/correct',{}).get(':answer/id') else ('key omitted in source' if ':answer-field/correct' not in q[':question/answer-fields'][0] else 'source distractor'),'inferred_intent':'unresolved except directly recognizable correct, sign and omission patterns'} for a,pat in zip(original_values,source_patterns[key])]})
    solutions.append({'source_id':f['source'],'source_solution_present':bool(sol),'original_worked_solution':sol,'ordered_source_rhs':[[text for text,_ in section] for section in rows],'stage_names':['differentiate whole sum','rewrite reciprocal as negative power','split derivative over sum','hold other variable coefficient constant','apply elementary derivative','collect derivative'] if key=='root-reciprocal' else ['differentiate whole sum','split derivative over sum','hold other variable coefficient constant','apply elementary derivative','collect derivative'],'evaluation_stage_names':(['substitute ordered point','final exact value'] if f['eval_kind']=='omit' else ['substitute ordered point','evaluate source operands','final exact value']),'source_format_normalization':'Canonical shared math normalization; ordinary TeX function commands and parenthesized coordinates replace alternate operatorname/Unicode glyph spellings. No source mathematical rule is repaired.','changed_parameter_operations':'Same family-specific rewrite, csc² or sec*tan derivative identity, and source-specific two/three evaluation-row sequence; all variable names, coefficients, exponents and point references are derived anew.'})
    specific.append('| '+f['source']+' | '+(q.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1])+' | '+q[':question/problem'].replace('|','\\|')+' | '+str(sum(len(z) for z in rows) if rows else 'missing')+' |')
write('bank-map.json',{'notation':'u active, v held; U,V their coordinates; T1 and T2 are signed derivative-term contributions at the point, C=T1+T2, N active polynomial exponent','source_banks':banks,'authored_default_bank':{'profile':'method-sum-bank','values':['T1+T2','T1-T2','-T1+T2','T1','T2'],'operations':['correct full derivative','wrong sign on second differentiated summand','wrong sign on first differentiated summand','omit second differentiated summand','omit first differentiated summand'],'learner_feedback':'none; absent in sources and never invented'}})
write('solution-map.json',solutions);write('domains.json',domains)
(D/'classification.md').write_text('''# Classification

Frozen source: math basis 2275, lineage `'''+g.SOURCE['lineage']+'''`. The exact refresh wrapper is `source.json`; topic and lesson wrappers are retained separately. There are 12 MA-identified practice originals: six moderate, four hard, two unrated. All use one five-choice radio field named `selection`. Ten have keyed worked solutions. q-132257 and q-159604 omit the key, difficulty and worked solution. Their raw public replay preserves all three omissions; normal records are completed authored variants. No independently authored captured inventory exists. The fieldless canonical e-11049 is a separate evidence row, never counted as a practice source.

The 12 practice families are separate because their functional structures, elementary derivatives or answer notation differ. Each has one observed complete bank profile. The six moderate and four rated hard labels are observed; the two unrated families receive an explicitly authored hard assignment. Easy is an authored two-monomial extension. Every family has plot rating **none**: no source asset occurs in a prompt, choice or solution. TeX rendering is mathematical typesetting, not plot generation.

| Original | Observed level | Original prompt | Total solution rows |
|---|---|---|---|
'''+ '\n'.join(specific)+'\n')
(D/'template-extraction.md').write_text('''# Template extraction

## 1. Describe originals before generalizing

`classification.md` reproduces every original prompt and its observed rating. `source-maps.json` retains each complete original beside its API replay. The canonical is distinct in `canonical-validation.json`. Each original contains a two-term sum/difference of separable functions; the requested partial derivative is either fraction notation at a stated ordered point, or subscript notation with the point inside the function call. All fields are scalar radio banks, with no source distractor feedback. Reciprocal, root, logarithm, base/e exponential and trigonometric operators remain different families. q159587 additionally rewrites a reciprocal to a negative power; q159597 and q159599 omit a redundant numerical intermediate row. Source notation ∂ and f_x/f_y is retained by family. The source's csc² cotangent derivative and separate sec/tan evaluations are preserved, rather than CAS-expanded identities.

q132257 and q159604 have no original worked solution or correct designation. Their mathematically derived correct values are 4-2/pi² and 2 ln(2)-1/2. These are inferred locally, never called matched source keys. Their missing ratings are not observed hard evidence. Unicode pi/function-application glyphs and alternative TeX function spelling are presentation-normalized in generated records; raw decoded bytes are preserved unchanged. Numeric coefficients before Euler e use visible multiplication in generated answers and solution conclusions. The separate synthetic blank diagnostic preserves the source 2e+1 bytes and reproduces the current native scientific-notation interpretation; this does not change the original radio response contract.

## 2. Shared instructional backbone

Given f of two independent variables and one ordered point, differentiate with respect to the requested variable while holding the other independent variable constant. Only then substitute both point coordinates and evaluate exactly. The supplied function, target independent variable, held independent variable, active coordinate and held coordinate have separate roles. A target swap consistently renames the role-defined function and reverses the role-to-physical-coordinate map; it is permitted at unchanged workload and is not counted as a new mathematical task merely for changing letters.

The two-term structure, first-order partial derivative, exact scalar response and five-choice radio contract are fixed. New chain/product/quotient-rule structure, higher derivatives, three variables, implicit differentiation, limits and approximate-angle evaluation are outside this generator. One concrete worked solution is computed per question, independent of the learner's selection. No error-specific learner feedback is added.

## 3. Map every component and full bank

`bank-map.json` lists all 60 original choices, their owning field, exact original values, expression patterns and profiles. The signed derivative contributions T1,T2 come from h1(v)g1'(u) and sign*h2(v)g2'(u), evaluated at (U,V); C=T1+T2. Profiles preserve the entire observed bank together. The numerical mistakes are often underdetermined: a pattern matching a source scalar does not recover its historical error intent. Therefore these explicit source profiles are anchor-only, evidence-only and unavailable to normal sampling. Their public API replay still constructs a parameterized function and derivative and determines correctness mathematically; it never returns a literal completed source payload or looks up a correct answer.

Normal variants select the separately authored complete method bank before parameters: C, T1-T2, -T1+T2, T1, T2. The four wrong operations are wrong signs on a differentiated summand or omission of a differentiated summand. Every pair, including wrong/wrong pairs, must be unequal. A zero contribution or collision rejects the whole instance. No first-valid fallback or mixing of profiles is allowed. No feedback is inferred from these metadata recipes.

`solution-map.json` records all original prose/math and ordered RHS stages, including the reciprocal rewrite and two-versus-three evaluation-row differences. Fidelity compares complete prose and each mathematical stage, not merely its final answer or row count. Notation normalization is reported separately from raw-byte reproduction.

## 4. Reusable templates and slots

`domains.json` is the complete per-family slot contract. Each family fixes g1,g2 and the held-variable factors while allowing positive coefficients a,b from 1..4 and the listed small integer powers. U,V vary over explicitly listed familiar exact inputs: positive perfect squares for roots, familiar pi angles away from singularities, simple positive log inputs and exact exponential/log inverse values. Every explicit call uses the same bounds as sampling. No undefined roots, nonpositive logarithm inputs or trigonometric poles are admitted. The point is always printed in physical (x,y) order.

The derivative chain is: derivative of the whole two-term expression; optional observed reciprocal rewrite; sum/difference of derivatives; pull out factors depending only on the held variable; apply elementary derivatives; collect the derivative. Its point chain substitutes the complete coordinates, evaluates the family's observed operand structure where present, then collects the exact scalar. The cotangent family uses -csc², the secant family evaluates sec and tan separately, and negative inserted factors are grouped. The source omits the intermediate numerical row in two families; it stays omitted.

Easy has no rated source example. The lesson route, reconstructed from activity/first-step and step/next, is introduction → difference quotient → computing partial derivatives tutorial → finding two-variable partial derivatives → this KP. The tutorial explicitly differentiates xy²+e^y while holding y fixed and introduces point notation. The canonical uses a two-term polynomial/trigonometric sum. The authored easy family retains two nonzero monomial contributions with active powers two and one, positive integer inputs and no transcendental/root/reciprocal evaluation. All easy questions have the same two elementary derivative and substitution demands. Moderate preserves the six observed families, with familiar roots/logs/exponentials or active polynomial powers three to five. Hard preserves all four rated hard families plus the two explicitly authored unrated assignments; its trigonometric or non-e-base derivative and exact special-value calculations remain within those families. These are independent repeated-practice instances, not a progression within a level.

No logarithm-combining simplification is used for learner values: for example 32 ln(2) stays a coefficient times a familiar logarithm, rather than becoming ln(4294967296). The complete finite same-method domain has 5,217 eligible role tasks (see finite-domain-counts.json), with target letters, profile aliases and option orders excluded. Source-family controls are selected before parameter sampling, and defaults must serve every eligible family. Mathematical fingerprints normalize the complete function in active/held roles and both coordinate values; targets, bank/profile aliases, unused exponent parameters, seeds and choice order do not inflate task counts. Presentation identities use normalized actual prompt, solution, difficulty and the complete displayed bank; every answer ID belongs to its field.
''')
(D/'plot-extraction.md').write_text('No plots occur in the 12 originals, canonical, authored easy extension or any supported variant. Plot rating: none. No image assets, SVG construction, Matplotlib or image models are used. Actual player MathJax rendering is verified separately.\n')
(D/'README.md').write_text('''# Local partial-derivative generator draft

Script: `../17592186124644-draft.py`. Source wrapper is frozen math basis2275. No EDB reads/writes, registration, engine changes or commits occur. Numeric script/tree/cache and sibling pyc absence is captured before imports and rechecked. The generator sets `sys.dont_write_bytecode=True` before third-party/shared imports.

```sh
.venv/bin/python -B generate/scratch/17592186124644-draft.py --difficulty all --seed 7 --count 2 --format json
.venv/bin/python -B generate/scratch/17592186124644-draft/validate.py
.venv/bin/python -B generate/scratch/17592186124644-draft/build-docs.py
.venv/bin/python -B generate/scratch/17592186124644-draft/render.py
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and the three difficulty wrappers. `parameters` uses a,b,n,m,U,V,target. `observed-q-…` replays complete original banks at documented anchors and preserves missing attributes; these are explicitly ineligible evidence. `method-sum-bank` is the normal default complete bank. See `domains.json` for every explicit-input guard. API JSON is review data, never transaction data.

Read `validation.json` for separate source-fidelity/math/native denominators and `scalar-native-report.json` for the Euler-e semantic probes and explicitly reproduced raw-source parser limitation, `render-report.json` and `renders/` for actual player controls and full solutions, and `freeze-manifest.json` for final owned hashes. Root approval remains pending.
''')
reviews=json.loads((D/'review.json').read_text()) if (D/'review.json').exists() else []
text=['# Original and generated review','Original source records are immutable in source.json. The source-facing replay uses normalized TeX and preserves every original absent attribute. Generated examples below use the method-derived complete bank and are eligible for local review.']
for sid,q in g.ORIGINALS.items():
    text.extend(['## Original '+sid,q[':question/problem'],'Bank: '+', '.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']),q.get(':question/worked-solution','No original solution or correct designation.' )])
    key=g.SOURCE_FAMILY[sid]
    for item in reviews:
        if item['template']==key:text.extend(['### Generated variant ('+item['level']+')',g.markdown(item['record'])])
for item in reviews:
    if item['level']=='easy':text.extend(['## Authored easy generated variant',g.markdown(item['record'])])
(D/'review.md').write_text('\n\n'.join(text)+'\n')
write('reference/capture-hashes.json',{str((D/name).relative_to(ROOT)):hashlib.sha256((D/name).read_bytes()).hexdigest() for name in ['source.json','topics.json','lessons.json']})
print('Built extraction, all 60-choice bank map, solution masks, domains and original/variant review.')
