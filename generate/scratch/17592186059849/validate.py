#!/usr/bin/env python3
"""Independent math, complete observed-bank fidelity and native learner grading."""
import collections, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
from hard_practice_validation import check_record as check_mixed_hard, validate as validate_mixed_hard
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
    if record['generation']['matrix_recipe']==g.HARD_MIXED_PROFILE:
        check_mixed_hard(g,record)
        return True
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
    ids=set();fieldids=set();selected_atoms=[];displayed_atoms=[]
    for f in q[':question/answer-fields']:
        assert f[':answer-field/id'] not in fieldids;fieldids.add(f[':answer-field/id'])
        correct=f[':answer-field/correct'][1];answers=f[':answer-field/choices'];keys=[];good=[]
        for ans in answers:
            assert ans[':answer/id'] not in ids;ids.add(ans[':answer/id'])
            # Mathematics outside inline prose uses delimiter-free values.
            if ans[':answer/type']==':answer.type/math':assert '$' not in ans[':answer/value']
            if f[':answer-field/type'].endswith('/checkbox'):
                label=f[':answer-field/key']
                raw=re.search(r'^- \*\*'+re.escape(label)+r'\.\*\* \$([^$]+)\$',q[':question/problem'],re.M)[1]
                atom=g.parse_math(raw.split('=',1)[1])
                truth=any(eq(atom,root) for root in expected)
                assert ans[':answer/type']==':answer.type/text' and ans[':answer/value'] in ('true','false')
                keys.append(ans[':answer/value'])
                if ans[':answer/value']==str(truth).lower():good.append(ans[':answer/id'])
                continue
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
        assert len(answers)==(5 if d['kind']=='radio' else 2 if d['kind']=='checkbox' else 1)
        if d['kind']=='checkbox':
            displayed_atoms.append(atom)
            if truth:selected_atoms.append(atom)
    if d['kind']=='checkbox':
        assert len(displayed_atoms)==len(set(map(sp.srepr,displayed_atoms)))
        assert key(selected_atoms)==key(expected)
        labels=re.findall(r'^- \*\*([IVX]+)\.\*\*',q[':question/problem'],re.M)
        assert labels==[f[':answer-field/key'] for f in q[':question/answer-fields']]
        assert labels==list(g.ROMAN[:len(labels)])
        assert q[':question/problem'].count('Select all that apply.')==1
        assert 'If none apply, leave all boxes unchecked.' in q[':question/problem']
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
    if ':question/worked-solution' in original and sid not in g.LEVEL_REPAIRS:
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
        answer_value=lambda text:text if d['kind']=='checkbox' else key(value(text))
        bank=[(a[':answer/type'][':db/ident'],answer_value(a[':answer/value'])) for a in f[':answer-field/choices']]
        got=[(a[':answer/type'],answer_value(a[':answer/value'])) for a in generated[':answer-field/choices']]
        assert collections.Counter(bank)==collections.Counter(got),(sid,bank,got)
        count['source_options']+=len(bank);count['source_fields']+=1
        if d['kind']=='radio':count['source_distractors']+=len(bank)-1
        if ':answer-field/correct' in f:
            origcorrect=f[':answer-field/correct'][':answer/value'];correct=next(a[':answer/value'] for a in generated[':answer-field/choices'] if a[':answer/id']==generated[':answer-field/correct'][1]);assert answer_value(origcorrect)==answer_value(correct);count['known_correct_designations']+=1
        else:count['missing_correct_designations']+=1
        row['fields'].append({'key':f[':answer-field/key'],'matched_options':len(bank),'total_options':len(bank),'known_original_correct':':answer-field/correct' in f})
    details.append(row)

# Parameter variation for EVERY observed bank and every authored default matrix
# recipe. Sampling varied signs/zeros/targets stays in the original degree scope.
variant_counts=collections.Counter();fingerprints={level:set() for level in ('easy','moderate','hard')}
for sid,d in g.DEFS.items():
    profiles=[sid]+(['authored:'+sid] if d['kind'] in ('radio','checkbox') else [])
    for profile in profiles:
        for seed in range(20):
            r=g.generate(d['level'],seed=seed,profile=profile)
            independent(r);variant_counts['authored' if profile.startswith('authored:') else 'observed']+=1
            if profile=='authored:q-9961':
                options=r['question'][':question/answer-fields'][0][':answer-field/choices']
                assert sum(a[':answer/value']=='Any real number' for a in options)==1
                alternative=next(a for a in options if a[':answer/value']=='Any real number')
                assert alternative[':answer/type']==':answer.type/text'
                assert alternative[':answer/id']!=r['question'][':question/answer-fields'][0][':answer-field/correct'][1]
            fingerprints[d['level']].add(r['generation']['parameter_fingerprint'])
            if seed<2:records.append((profile+':variant:'+str(seed),r))
            p=r['generation']['parameters']
            other=g.generate(d['level'],seed=seed+1000,profile=profile,parameters=p)
            assert other['question'][':question/id']==r['question'][':question/id']
            assert other['generation']['content_fingerprint']==r['generation']['content_fingerprint']
            assert other['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
            for x,y in zip(r['question'][':question/answer-fields'],other['question'][':question/answer-fields']):assert set(a[':answer/id'] for a in x[':answer-field/choices'])==set(a[':answer/id'] for a in y[':answer-field/choices'])
# The hard default must require mathematics: every solution-set class occurs
# with the same prompt, field type, and complete option-bank shape.
mixed_hard_report,mixed_hard_records=validate_mixed_hard(g)
records.extend(mixed_hard_records)
mixed_invalid=0
base=g.generate('hard',seed=2)['generation']['parameters']
for change in ({'target':1},{'option_roots':[1,-1]},{'linear':[0]*9},
               {'constants':[1.5]*9},{'extra':True}):
    try:g.generate('hard',parameters={**base,**change})
    except ValueError:mixed_invalid+=1
    else:raise AssertionError('Invalid mixed-hard parameters were silently repaired')
assert g.generate('hard',seed=2,template=g.HARD_MIXED_TEMPLATE)==g.generate('hard',seed=2)
mixed_hard_report['invalid_explicit_inputs_rejected']=mixed_invalid

# Exercise the CLI through the same public interface users run, including the
# authored checkbox profile previously omitted from argparse choices.
cli_checks=[]
for difficulty,profile in (('moderate','authored:q-9911'),('easy','authored:q-9961'),('hard',None),('hard',g.HARD_MIXED_PROFILE)):
    command=[sys.executable,str(HERE.with_suffix('.py')),'--difficulty',difficulty,'--seed','10','--format','json']
    if profile is not None:command+=['--profile',profile]
    cli=subprocess.run(command,capture_output=True,text=True,check=True)
    records_from_cli=json.loads(cli.stdout)
    assert len(records_from_cli)==1
    expected=g.generate(difficulty,seed=10,profile=profile)
    assert records_from_cli[0]==json.loads(json.dumps(expected))
    independent(records_from_cli[0]);cli_checks.append({'profile':profile,'difficulty':difficulty,'status':'passed'})
# Same mathematics with genuinely different displayed banks has different IDs.
bank_identity_checks=0
for sid,d in g.DEFS.items():
    if d['kind'] not in ('radio','checkbox'):continue
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
        elif f[':answer-field/type'].endswith('/checkbox'):
            for answer in f[':answer-field/choices']:
                checks.append({'field_index':index,'submitted_answer_id':answer[':answer/id'],'expected':'accepted' if answer[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Boolean checkbox grading, including unchecked false'})
        else:
            correct=f[':answer-field/choices'][0][':answer/value'];v=value(correct)[0]
            checks.extend([{'field_index':index,'submitted':correct,'expected':'accepted','purpose':'canonical mathematical answer'}, {'field_index':index,'submitted':str(v),'expected':'accepted','purpose':'equivalent exact SymPy fraction/radical'}, {'field_index':index,'submitted':str(v+1),'expected':'rejected','purpose':'incorrect numeric answer'}])
    engine.append({'label':label,'record':r,'checks':checks})
(HERE/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False))
process=subprocess.run([str(HERE.parent/'source-refresh-2026-10-12/check-checkbox-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
(HERE/'engine.log').write_text(process.stdout+process.stderr)
assert process.returncode==0,process.stdout+process.stderr
engine_report=json.loads((HERE/'engine-report.json').read_text())
report={'status':'pass','source_provenance':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'practice_sources':len(cases),'original_bank_fidelity':{'complete_banks_matched':len(cases),'complete_banks_total':len(cases),'question_designations_matched':sum(row['correct_designation_match'] for row in details),'question_designations_total':len(cases),'field_banks_matched':count['source_fields'],'field_banks_total':count['source_fields'],'prompt_and_field_layouts_matched':24,**count,'mathematically_inferred_missing_correct_refs':count['missing_correct_designations'],'designation_note':'All current database designations are matched, including the repaired q-9657 and q-9852 keys.'},'solution_fidelity':{'shared_source_sentences_and_methods':True,'source_math_errors_corrected':['q-280403 determinant label','q-280541 missing ± intermediate'],'source_specific_expansion_stage_sequence':True,'full_generator_derivation_for_brief_authored_database_solutions':['q-9657','q-9852'],'exact_original_expansion_row_rendering':False,'note':'The shared renderer keeps cofactor expansion and source solve method, but preserves per-source expansion stage ordering while standardizing product notation; this is a documented layout deviation, not literal worked-solution fidelity.'},'mathematics':{'observed_profile_variants':variant_counts['observed'],'authored_default_variants':variant_counts['authored'],'source_instances':len(cases),'distinct_parameter_instances_by_level':{k:len(v) for k,v in fingerprints.items()},'invalid_explicit_inputs_rejected':invalid,'different_bank_identity_checks':bank_identity_checks},'native_grading':{'status':'pass','records':len(engine),'checks':sum(len(e['checks']) for e in engine),'binary_sha256':hashlib.sha256((HERE.parent/'source-refresh-2026-10-12/check-checkbox-engine').read_bytes()).hexdigest(),'report':'engine-report.json',**{key:engine_report[key] for key in ('whole_question_canonical_accepted','whole_question_flipped_checkboxes_rejected','whole_question_incomplete_rejected')}},'profiles':details,'limitations':['Two unrated source difficulty assignments are authored (q-9657 moderate, q-9852 hard).','Unusual source distractor intent is unknown; coefficient recipes serve complete evidence replay only. Operation-derived authored banks are the default.','Shared worked-solution expansion rows are reconstructed and standardized, preserving source prose/methods rather than exact original row typography.']}
report['cli_regressions']=cli_checks
report['generator_sha256']=hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()
report['default_bank_regressions']={'q-9961':'Any real number remains a text alternative, independently rejected for every sampled unique linear solution.'}
report['mixed_hard_practice']=mixed_hard_report
report['limitations']+=['Default hard practice is an authored identity/linear/quadratic mixture with a shared prompt and five-option bank; the original identity-only hard profiles remain explicit source replay. The authored hard assignment is not calibrated against a varied source hard bank.',
                       'Default banks are authored alternatives, not identical source distractor coverage. q-9961 retains its all-real alternative; complete captured banks remain available through explicit source profiles.',
                       'Easy/moderate coefficient sampling stays within observed structures, changing at most two nonzero constants and preserving variable coefficients and zero positions. Hard varies more constants while preserving its identity structure. Repeated roots, no-real-root cases and cubics are outside the captured source scope.']
(HERE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps({k:v for k,v in report.items() if k!='profiles'},indent=2))
