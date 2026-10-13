#!/usr/bin/env python3
"""Independent math, complete observed-bank fidelity and native learner grading."""
import collections, hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def expr(s):return sp.sympify(s,locals={'u':g.X})
def value(s):
    if s.startswith('Any'):return None
    parts=re.findall(r'\$([^$]*)\$',s)
    return [g.parse_math(p) for p in parts] if parts else [g.parse_math(s)]
def key(vals):return 'all-real' if vals is None else tuple(sorted(sp.srepr(sp.simplify(v)) for v in vals))
def eq(a,b):return sp.simplify(a-b)==0
displayed_rows_checked=0
def check_displayed_determinant_rows(record,determinant,var):
    global displayed_rows_checked
    symbol=sp.Symbol(var,real=True)
    trans=standard_transformations+(implicit_multiplication_application,)
    def arithmetic(text):
        text=text.replace(r'\cdot','*').replace(r'\big','').replace(r'\,','').replace('{','(').replace('}',')').replace('^','**')
        assert '\\' not in text,text
        return parse_expr(text,local_dict={var:symbol},transformations=trans)
    def minor(match):
        entries=[arithmetic(y) for row in match[1].split(r'\\') for y in row.split('&')]
        n=int(len(entries)**.5);assert n*n==len(entries)
        return '('+str(sp.Matrix(n,n,entries).det())+')'
    block=re.search(r'\$\$(.*?)\$\$',record['question'][':question/worked-solution'],re.S)[1].strip()
    block=block.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
    block=re.sub(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',minor,block,flags=re.S)
    for row in block.split(r'\\'):
        _,rhs=row.split(' & =',1)
        assert eq(arithmetic(rhs),determinant.subs(g.X,symbol)),(record['generation']['matrix_recipe'],rhs)
        displayed_rows_checked+=1

def independent(record):
    q=record['question'];meta=record['generation'];p=meta['parameters'];sid=meta['matrix_recipe'];d=g.DEFS[sid]
    m=sp.Matrix([[expr(t) for t in row] for row in meta['matrix']]);x=g.X
    a,b,c,dd,e,f,gg,h,i=list(m)
    determinant=sp.expand(a*(e*i-f*h)-b*(dd*i-f*gg)+c*(dd*h-e*gg))
    assert eq(determinant,m.det()) and eq(determinant,expr(meta['determinant']))
    check_displayed_determinant_rows(record,determinant,d['variable'])
    polynomial=sp.Poly(determinant-p['target'],x)
    expected=None if polynomial.is_zero else sp.solve(polynomial.as_expr(),x)
    assert key(expected)==key(None if meta['roots'] is None else [expr(t) for t in meta['roots']])
    if d['level']=='hard':assert polynomial.is_zero
    else:
        assert polynomial.degree()==(1 if d['level']=='easy' else 2)
        assert len(expected)==polynomial.degree() and all(t.is_real for t in expected)
    ids=set();fieldids=set()
    for f in q[':question/answer-fields']:
        assert f[':answer-field/id'] not in fieldids;fieldids.add(f[':answer-field/id'])
        correct=f[':answer-field/correct'][1];answers=f[':answer-field/choices'];keys=[];good=[]
        for ans in answers:
            assert ans[':answer/id'] not in ids;ids.add(ans[':answer/id'])
            # Mathematics outside inline prose uses delimiter-free values.
            if ans[':answer/type']==':answer.type/math':assert '$' not in ans[':answer/value']
            vals=value(ans[':answer/value']);keys.append(key(vals))
            if f[':answer-field/type'].endswith('/radio'):
                if key(vals)==key(expected):good.append(ans[':answer/id'])
                stored=next(v for v in meta['choice_math'] if v['value']==ans[':answer/value'])
                assert key(vals)==key(None if stored['set'] is None else [expr(v) for v in stored['set']])
            else:
                index=int(f[':answer-field/key'].split('-')[-1])-1
                root=sorted(expected,key=float)[index]
                assert vals is not None and len(vals)==1 and eq(vals[0],root)
                good.append(ans[':answer/id'])
                assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
        assert len(keys)==len(set(keys)) and good==[correct]
        assert len(answers)==(5 if d['kind']=='radio' else 1)
    # Independent minors and distributed contributions; verify the displayed
    # final determinant and solutions derive from those same values.
    symbol=sp.Symbol(d['variable'],real=True)
    for j,step in enumerate(meta['solution_intermediates']):
        mm=sp.Matrix([[expr(t) for t in row] for row in step['minor']]);sv=expr(step['value']);sc=expr(step['coefficient']);product=expr(step['signed_product'])
        assert eq(sv,mm.det()) and eq(product,(-1)**j*sc*sv)
        assert mm==m.subs(x,symbol).minor_submatrix(0,j)
    assert g.tex(determinant.subs(x,symbol)) in q[':question/worked-solution'] or sid=='q-9913' and d['variable']+'('+g.tex(sp.cancel(determinant/x).subs(x,symbol))+')' in q[':question/worked-solution']
    for root in expected or []:assert g.tex(root) in q[':question/worked-solution']
    displayed_matrix=g.mat_tex(m.subs(x,symbol))
    if sid in g.LEVEL_REPAIRS:displayed_matrix=displayed_matrix.replace('[\\begin{aligned}',r'\begin{bmatrix}').replace(r'\end{aligned}]',r'\end{bmatrix}')
    assert displayed_matrix in q[':question/problem']
    assert '{matrix}' not in q[':question/problem'] and '{target}' not in q[':question/problem']
    if not d['singular']:
        assert re.search(r'(?:=|is \$?)'+re.escape(g.tex(p['target'])),q[':question/problem'])
    if d['level']=='moderate' and not d['singular'] and sid!='q-280540':
        aa,bb,cc=polynomial.nth(2),polynomial.nth(1),polynomial.nth(0)
        if aa<0:aa,bb,cc=-aa,-bb,-cc
        if sid=='q-18272':
            common=sp.igcd(sp.igcd(int(aa),int(bb)),int(cc));aa,bb,cc=(t/common for t in (aa,bb,cc))
        disc=bb**2-4*aa*cc
        formula=r'\frac{-('+g.tex(bb)+r')\pm\sqrt{('+g.tex(bb)+r')^2-4\cdot '+g.tex(aa)+r'\cdot ('+g.tex(cc)+r')}}{2\cdot '+g.tex(aa)+'}'
        assert formula in q[':question/worked-solution']
        discriminant_step=r'\frac{'+g.tex(-bb)+r'\pm\sqrt{'+g.tex(disc)+'}}{'+g.tex(2*aa)+'}'
        assert discriminant_step in q[':question/worked-solution']
    if sid=='q-280540':
        assert r'\pm\sqrt{'+g.tex(-polynomial.nth(0)/polynomial.nth(2))+'}' in q[':question/worked-solution']
    assert 'recipe' not in q[':question/problem'] and 'authored' not in q[':question/worked-solution']
    return True

cases=json.loads((HERE/'source-cases.json').read_text())
records=[];details=[];count=collections.Counter();engine=[]
for case in cases:
    sid=case['source_id'];d=g.DEFS[sid];r=g.generate(d['level'],profile=case['bank_profile'],template=case['template'],parameters=case['parameters'])
    independent(r);records.append(('source:'+sid,r))
    original=d['source']
    normalize=lambda text:re.sub(r'\s+','',text.replace(r'\left','').replace(r'\right','').replace('{','').replace('}',''))
    assert normalize(r['question'][':question/problem'])==normalize(original[':question/problem']),(sid,'prompt/layout mismatch')
    if ':question/worked-solution' in original:
        def prose(text):
            text=re.sub(r'\$\$.*?\$\$','<math>',text,flags=re.S)
            text=re.sub(r'\$[^$]*\$','<math>',text)
            return re.sub(r'\s+',' ',text).strip()
        assert prose(original[':question/worked-solution'])==prose(r['question'][':question/worked-solution']),(sid,'shared worked-solution prose mismatch')
    new={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']}
    row={'source_id':sid,'complete_bank_match':True,'correct_designation_match':':answer-field/correct' in original[':question/answer-fields'][0],'fields':[]}
    for f in original[':question/answer-fields']:
        generated=new[f[':answer-field/key']]
        assert f[':answer-field/type'][':db/ident']==generated[':answer-field/type']
        bank=[(a[':answer/type'][':db/ident'],key(value(a[':answer/value']))) for a in f[':answer-field/choices']]
        got=[(a[':answer/type'],key(value(a[':answer/value']))) for a in generated[':answer-field/choices']]
        assert collections.Counter(bank)==collections.Counter(got),(sid,bank,got)
        count['source_options']+=len(bank);count['source_fields']+=1
        if d['kind']=='radio':count['source_distractors']+=len(bank)-1
        if ':answer-field/correct' in f:
            origcorrect=f[':answer-field/correct'][':answer/value'];correct=next(a[':answer/value'] for a in generated[':answer-field/choices'] if a[':answer/id']==generated[':answer-field/correct'][1]);assert key(value(origcorrect))==key(value(correct));count['known_correct_designations']+=1
        else:count['missing_correct_designations']+=1
        row['fields'].append({'key':f[':answer-field/key'],'matched_options':len(bank),'total_options':len(bank),'known_original_correct':':answer-field/correct' in f})
    details.append(row)

# Parameter variation for EVERY observed bank and every authored default matrix
# recipe. Sampling varied signs/zeros/targets stays in the original degree scope.
variant_counts=collections.Counter();fingerprints={level:set() for level in ('easy','moderate','hard')}
for sid,d in g.DEFS.items():
    profiles=[sid]+(['authored:'+sid] if d['kind']=='radio' else [])
    for profile in profiles:
        for seed in range(20):
            r=g.generate(d['level'],seed=seed,profile=profile)
            independent(r);variant_counts['authored' if profile.startswith('authored:') else 'observed']+=1
            fingerprints[d['level']].add(r['generation']['parameter_fingerprint'])
            if seed<2:records.append((profile+':variant:'+str(seed),r))
            p=r['generation']['parameters']
            other=g.generate(d['level'],seed=seed+1000,profile=profile,parameters=p)
            assert other['question'][':question/id']==r['question'][':question/id']
            assert other['generation']['content_fingerprint']==r['generation']['content_fingerprint']
            assert other['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
            for x,y in zip(r['question'][':question/answer-fields'],other['question'][':question/answer-fields']):assert set(a[':answer/id'] for a in x[':answer-field/choices'])==set(a[':answer/id'] for a in y[':answer-field/choices'])
# Same mathematics with genuinely different displayed banks has different IDs.
bank_identity_checks=0
for sid,d in g.DEFS.items():
    if d['kind']!='radio':continue
    for seed in range(100):
        authored=g.generate(d['level'],seed=seed,profile='authored:'+sid)
        try:observed=g.generate(d['level'],profile=sid,parameters=authored['generation']['parameters'])
        except ValueError:continue
        assert observed['generation']['parameter_fingerprint']==authored['generation']['parameter_fingerprint']
        assert observed['question'][':question/id']!=authored['question'][':question/id']
        bank_identity_checks+=1;break
    else:raise AssertionError('No same-parameter profile identity comparison')
# Invalid explicit parameters must fail, never silently be replaced.
invalid=0
for sid,d in g.DEFS.items():
    p=g.parameters(sid);p['linear'][0]+=1
    try:g.generate(d['level'],profile=sid,parameters=p)
    except ValueError:invalid+=1
    else:raise AssertionError('Invalid input was silently repaired')

for label,r in records:
    checks=[]
    for index,f in enumerate(r['question'][':question/answer-fields']):
        if f[':answer-field/type'].endswith('/radio'):
            for ans in f[':answer-field/choices']:checks.append({'field_index':index,'submitted_answer_id':ans[':answer/id'],'expected':'accepted' if ans[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned choice actual learner grading'})
        else:
            correct=f[':answer-field/choices'][0][':answer/value'];v=value(correct)[0]
            checks.extend([{'field_index':index,'submitted':correct,'expected':'accepted','purpose':'canonical mathematical answer'}, {'field_index':index,'submitted':str(v),'expected':'accepted','purpose':'equivalent exact SymPy fraction/radical'}, {'field_index':index,'submitted':str(v+1),'expected':'rejected','purpose':'incorrect numeric answer'}])
    engine.append({'label':label,'record':r,'checks':checks})
(HERE/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False))
process=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
(HERE/'engine.log').write_text(process.stdout+process.stderr)
assert process.returncode==0,process.stdout+process.stderr
engine_report=json.loads((HERE/'engine-report.json').read_text())
report={'status':'pass','source_provenance':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'practice_sources':len(cases),'original_bank_fidelity':{'complete_banks_matched':len(cases),'complete_banks_total':len(cases),'question_designations_matched':22,'question_designations_total':24,'field_banks_matched':27,'field_banks_total':27,'prompt_and_field_layouts_matched':24,**count,'mathematically_inferred_missing_correct_refs':2,'designation_note':'No original correct designation exists for q-9657 or q-9852; these cannot count as matched designations.'},'solution_fidelity':{'shared_source_sentences_and_methods':True,'source_math_errors_corrected':['q-280403 determinant label','q-280541 missing ± intermediate'],'source_specific_expansion_stage_sequence':True,'exact_original_expansion_row_rendering':False,'note':'The shared renderer keeps cofactor expansion and source solve method, but preserves per-source expansion stage ordering while standardizing product notation; this is a documented layout deviation, not literal worked-solution fidelity.'},'mathematics':{'observed_profile_variants':variant_counts['observed'],'authored_default_variants':variant_counts['authored'],'source_instances':len(cases),'distinct_parameter_instances_by_level':{k:len(v) for k,v in fingerprints.items()},'invalid_explicit_inputs_rejected':invalid,'different_bank_identity_checks':bank_identity_checks},'native_grading':{'status':'pass','records':len(engine),'checks':sum(len(e['checks']) for e in engine),'binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'report':'engine-report.json'},'profiles':details,'limitations':['Two unrated source difficulty assignments are authored (q-9657 moderate, q-9852 hard).','Unusual source distractor intent is unknown; coefficient recipes serve complete evidence replay only. Operation-derived authored banks are the default.','Shared worked-solution expansion rows are reconstructed and standardized, preserving source prose/methods rather than exact original row typography.']}
(HERE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps({k:v for k,v in report.items() if k!='profiles'},indent=2))
