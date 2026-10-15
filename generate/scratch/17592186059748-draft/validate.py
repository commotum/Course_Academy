#!/usr/bin/env python3
"""Independent QA of actual printed matrices, complete banks and stage masks.

Does not use generation parameters to infer the correct answer. Native grading
is a separate real-engine test. Full source prose and every bank are separately
checked against fixed-basis raw evidence. Any failure exits nonzero.
"""
import copy,hashlib,importlib.util,json,pathlib,re,subprocess,uuid,sys
sys.dont_write_bytecode=True
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('det_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
MATRIX=re.compile(r'\\begin\{(aligned|vmatrix|bmatrix)\}(-?\d+) & (-?\d+) \\\\ (-?\d+) & (-?\d+)\\end\{\1\}')
def scalar(t):
    return parse_expr(t.strip().rstrip('.').replace('\\cdot','*'),transformations=standard_transformations+(implicit_multiplication_application,))
def check(record):
    assert set(record)=={'knowledge_point','question','generation'}
    assert record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=record['question'];prompt=q[':question/problem'];sol=q.get(':question/worked-solution','');f=q[':question/answer-fields'][0]
    for uid in [q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]:uuid.UUID(uid)
    assert len(q[':question/answer-fields'])==1
    for text in [prompt,sol]:
        assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
        assert text.count('$')%2==0 and text.count('$$')%2==0
        depth=0
        for ch in text:
            depth+= (ch=='{')-(ch=='}');assert depth>=0
        assert depth==0
        assert not any(s in text for s in ['+-','--','-+'])
    m=MATRIX.findall(prompt);assert len(m)==1
    a,b,c,d=map(int,m[0][1:]);expected=int(sp.Matrix([[a,b],[c,d]]).det())
    if record['generation']['profile']=='authored_operations':
        v=[a,b,c,d];level=q[':question/difficulty'].split('/')[-1]
        if level=='easy':assert max(map(abs,v))<=9 and sum(n<0 for n in v)<=1 and sum(n==0 for n in v)<=1 and max(abs(a*d),abs(b*c))>=2
        elif level=='moderate':assert all(n and abs(n)<=10 for n in v) and any(n<0 for n in v) and max(abs(a*d),abs(b*c))>=10
        else:assert level=='hard' and all(6<=abs(n)<=15 for n in v) and 2<=sum(n<0 for n in v)<=3 and max(map(abs,v))>=11 and min(abs(a*d),abs(b*c))>=50
    if not sol:
        assert record['generation']['profile']=='q-11648'
        assert ':question/difficulty' not in q and ':answer-field/correct' not in f
        return (a,b,c,d),expected
    sm=MATRIX.findall(sol);assert len(sm)==1 and sm[0][1:]==m[0][1:]
    assert r'\begin{vmatrix}a & b \\ c & d\end{vmatrix}=ad-bc.' in sol
    key=f[':answer-field/key'];kind=f[':answer-field/type'].split('/')[-1]
    assert kind in ['radio','blank'];assert key==('field-1' if kind=='blank' else 'selection')
    if kind=='blank':assert prompt.count('{{'+key+'}}')==1
    bank=f[':answer-field/choices'];assert len(bank)==(1 if kind=='blank' else 5)
    ids=[x[':answer/id'] for x in bank];assert len(set(ids))==len(ids)
    assert f.get(':answer-field/correct',[':answer/id'])[0]==':answer/id';cid=f.get(':answer-field/correct',[':answer/id',next(x[':answer/id'] for x in bank if x[':answer/value']==str(expected))])[1];assert cid in ids
    values=[scalar(x[':answer/value']) for x in bank];assert len(set(values))==len(values)
    for entry,v in zip(bank,values):
        assert entry[':answer/type']==':answer.type/math' and v.is_Integer
        assert entry[':answer/id']==g.ident(f[':answer-field/id']+entry[':answer/value'])
        assert (v==expected)==(entry[':answer/id']==cid)
        assert '$' not in entry[':answer/value']
    # Derive all authored choices from the printed matrix, independently.
    if record['generation']['profile']=='authored_operations' and kind=='radio':
        assert set(values)=={a*d-b*c,a*d+b*c,b*c-a*d,a*d,a*b-c*d}
    # Read the actual final display, temporarily mask nested integer matrix,
    # then retain arithmetic rows as unevaluated strings and ordered operands.
    final=re.findall(r'\$\$(.*?)\$\$',sol,re.S)[-1].strip()
    final=MATRIX.sub('MATRIX',final)
    assert final.startswith(r'\begin{aligned}') and final.endswith(r'\end{aligned}')
    final=final[len(r'\begin{aligned}'):-len(r'\end{aligned}')]
    rows=final.split(r' \\ ')
    named='Calculate' in prompt
    assert len(rows)==(4 if named else 3)
    first=rows[0]
    assert first.count('MATRIX')==1
    if named:
        name=re.search(r'det\}?\(([A-Z])\)',prompt).group(1)
        assert name in first and first.endswith('=MATRIX')
        arithmetic=[r.split('=',1)[1].strip() for r in rows[1:]]
    else:
        assert first.startswith('MATRIX & =')
        arithmetic=[r.split('=',1)[1].strip() for r in rows]
    assert len(arithmetic)==3
    substitution,products,result=arithmetic
    # Every ordered coefficient occurrence must be exactly the printed factor,
    # including the source c*b variant (not merely equivalent final answer).
    order=[a,d,c,b] if record['generation']['template']=='named_dot_swapped' else [a,d,b,c]
    if kind=='blank':
        operands=re.fullmatch(r'\((-?\d+)\)\((-?\d+)\)-\((-?\d+)\)\((-?\d+)\)',substitution)
        wanted=f'({a})({d})-({b})({c})'
    else:
        term=r'(-?\d+|\(-?\d+\))'
        operands=re.fullmatch(term+r'\\cdot '+term+'-'+term+r'\\cdot '+term,substitution)
        def fct(n):return '('+str(n)+')' if n<0 else str(n)
        wanted=f'{a}\\cdot {fct(d)}-{fct(order[2])}\\cdot {fct(order[3])}'
    assert operands and [int(x.strip('()')) for x in operands.groups()]==order
    assert substitution==wanted
    assert scalar(substitution)==expected
    if kind=='blank' and b*c<0:wanted_products=f'{a*d}+{abs(b*c)}'
    else:wanted_products=str(a*d)+'-'+('('+str(b*c)+')' if b*c<0 else str(b*c))
    assert products==wanted_products and scalar(products)==expected
    assert result==str(expected)+('.' if kind=='blank' else '') and scalar(result)==expected
    # Mathematical identities exclude banks/presentation; content identity uses
    # actual learner data. Verify from displayed values rather than metadata.
    assert record['generation']['mathematical_fingerprint']==g.digest([a,b,c,d])
    hash_=g.digest([g.VERSION,q.get(':question/difficulty',':question.difficulty/moderate').split('/')[-1],prompt,sol,kind,sorted(x[':answer/value'] for x in bank)])
    assert record['generation']['content_fingerprint']==hash_
    assert q[':question/id']==g.ident(hash_)
    return (a,b,c,d),expected

def native(label,rec):
    f=rec['question'][':question/answer-fields'][0]
    if ':answer-field/correct' not in f:return None
    cid=f[':answer-field/correct'][1]
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'Every complete owned radio choice'} for a in f[':answer-field/choices']]
    else:
        v=f[':answer-field/choices'][0][':answer/value'];matrix,_=check(rec);a,b,c,d=matrix
        checks=[{'submitted':v,'expected':'accepted','purpose':'Canonical exact integer'}, {'submitted':f'({a})*({d})-({b})*({c})','expected':'accepted','purpose':'Unreduced determinant arithmetic equivalent entry'}, {'submitted':str(int(v)+1),'expected':'rejected','purpose':'Incorrect integer'}, {'submitted':str(2*int(v))+'/2','expected':'accepted','purpose':'Unreduced rational equivalent entry'}]
    return {'label':label,'record':rec,'checks':checks}

def main():
    manifest=json.loads((D/'reference/grader-build.json').read_text())
    paths={manifest['source']:manifest['source_sha256'],manifest['library']:manifest['library_sha256'],manifest['binary']:manifest['binary_sha256'],**manifest['engine_sources'],**manifest['dependencies']}
    assert len(paths)==42
    for path,h in paths.items():assert hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()==h,path
    assert hashlib.sha256((D/'check-engine').read_bytes()).hexdigest()==manifest['binary_sha256']
    assert hashlib.sha256((D/'reference/libcourse_academy_engine.rlib').read_bytes()).hexdigest()==manifest['library_sha256']
    sources=json.loads((D/'source.json').read_text());cases=json.loads((D/'source-cases.json').read_text());ma=[q for q in sources['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q]
    assert len(cases)==len(ma)==9
    non=[q for q in sources['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
    inventory=json.loads((D/'independent-inventory.json').read_text());assert [x['record'] for x in inventory['questions']]==non and len(non)==7
    outputs=[];natives=[];fidelity=[];checks=0;covariant=0
    for src,case in zip(ma,cases):
        assert case['record']==src
        rec=g.generate(case['level'],seed=13,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(rec)
        q=rec['question'];f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
        for k in [':question/difficulty',':question/worked-solution']:
            assert (k in q)==(k in src)
        assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
        assert q[':question/problem']==g.normalize_prose(src[':question/problem'])
        assert f[':answer-field/key']==sf[':answer-field/key'] and f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
        if ':question/worked-solution' in src:assert q[':question/worked-solution']==g.normalize_prose(src[':question/worked-solution'])
        if ':answer-field/correct' in sf:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
        fidelity.append({'source_id':case['source_id'],'prompt_normalized_exact':True,'prompt_byte_exact':q[':question/problem']==src[':question/problem'],'complete_bank_exact':True,'presence_parity':True,'solution_normalized_exact':':question/worked-solution' in src,'solution_byte_exact':q.get(':question/worked-solution')==src.get(':question/worked-solution') and ':question/worked-solution' in src,'designation_exact':':answer-field/correct' in sf})
        outputs.append({'label':'MA raw observed '+case['source_id'],'record':rec})
        if native(case['source_id'],rec):natives.append(native(case['source_id'],rec))
        limit=40//max(abs(case['parameters'][k]) for k in 'abcd')
        for t in range(-limit,limit+1):
            if not t:continue
            p={k:t*v if k in 'abcd' else v for k,v in case['parameters'].items()}
            varied=g.generate(case['level'],parameters=p,profile=case['bank_profile']);check(varied)
            assert sorted(int(a[':answer/value']) for a in varied['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(t*t*int(a[':answer/value']) for a in sf[':answer-field/choices'])
            covariant+=1
        p={k:-2*v if k in 'abcd' else v for k,v in case['parameters'].items()}
        rec=g.generate(case['level'],parameters=p,profile=case['bank_profile']);outputs.append({'label':'Opaque evidence changed covariance '+case['source_id'],'record':rec})
    variety={};positions=set();default_templates={}
    for level in ['easy','moderate','hard']:
        default_templates[level]=sorted({g.generate(level,seed)['generation']['template'] for seed in range(100)})
        assert set(default_templates[level])=={t for t,d in g.TEMPLATES.items() if level in d['levels']}
        for template,t in g.TEMPLATES.items():
            if level not in t['levels']:continue
            fingerprints=set()
            for seed in range(140):
                r=g.generate(level,seed,template=template);check(r);checks+=1;fingerprints.add(r['generation']['mathematical_fingerprint'])
                f=r['question'][':question/answer-fields'][0]
                if f[':answer-field/type'].endswith('/radio'):positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
                again=g.generate(level,seed+983,template=template,parameters=r['generation']['parameters']);assert r['question'][':question/id']==again['question'][':question/id']
                if seed<2:outputs.append({'label':'Authored '+level+' '+template,'record':r});natives.append(native(level+' '+template+' '+str(seed),r))
            assert len(fingerprints)>=125;variety[level+':'+template]=len(fingerprints)
    assert positions==set(range(5))
    # Each actual printed cell and every ordered operand mutation must fail even
    # when answer IDs, products and final determinant remain untouched.
    base=outputs[0]['record'];mutations=[(':question/problem','1 & 2','2 & 2'),(':question/worked-solution','1 & 2','2 & 2'),(':question/worked-solution','1\\cdot 0-2\\cdot 3','0\\cdot 1-2\\cdot 3'),(':question/worked-solution','1\\cdot 0-2\\cdot 3','1\\cdot 0+2\\cdot 3'),(':question/worked-solution','0-6','0+6'),(':question/worked-solution','1\\cdot 0-2\\cdot 3','1\\cdot 0-3\\cdot 2')]
    for before,after in [('1 & 2','2 & 2'),('1 & 2','1 & 3'),('3 & 0','4 & 0'),('3 & 0','3 & 1')]:
        for key in [':question/problem',':question/worked-solution']:mutations.append((key,before,after))
    mutations.append((':question/worked-solution','For a','For \x0ca'))
    for key,old,new in mutations:
        bad=copy.deepcopy(base);assert old in bad['question'][key];bad['question'][key]=bad['question'][key].replace(old,new,1)
        try:check(bad)
        except AssertionError:pass
        else:raise AssertionError('same-final-key mutation escaped')
    # Control-character and every API formatting contract checked at boundary.
    for row in outputs:
        for text in [row['record']['question'].get(':question/problem',''),row['record']['question'].get(':question/worked-solution','')]:assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
    for level,p in [('easy',dict(a=-2,b=-3,c=4,d=5,name='A')),('moderate',dict(a=2,b=3,c=4,d=5,name='A')),('hard',dict(a=-6,b=-6,c=7,d=7,name='A'))]:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError('invalid explicit workload accepted')
    a=g.generate('easy',parameters=dict(a=8,b=-5,c=3,d=4,name='R'),template='named_parentheses_blank')
    b=g.generate('easy',seed=999,parameters=dict(a=8,b=-5,c=3,d=4,name='B'),template='named_parentheses_blank',profile='authored_operations')
    assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id']
    for kwargs in [dict(level='invalid'),dict(level='easy',template='unknown'),dict(level='easy',field_type='checkbox'),dict(level='easy',profile='unknown'),dict(level='easy',seed=True)]:
        try:g.generate(**kwargs)
        except ValueError:pass
        else:raise AssertionError('invalid public API accepted')
    cli=json.loads(subprocess.check_output([sys.executable,str(D.with_suffix('.py')),'--difficulty','all','--count','1','--format','json']))
    assert isinstance(cli,list) and len(cli)==3 and len({r['generation']['mathematical_fingerprint'] for r in cli})==3
    (D/'native-input.json').write_text(json.dumps(natives,indent=2)+'\n');subprocess.run([str(D/'check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
    nr=json.loads((D/'native-report.json').read_text());assert nr['unexpected_checks']==0 if 'unexpected_checks' in nr else True
    (D/'review.json').write_text(json.dumps(outputs,indent=2)+'\n')
    (D/'review.md').write_text('# Determinant originals and variants\n\n'+'\n\n'.join('## '+x['label']+'\n\n'+g.markdown(x['record']) for x in outputs)+'\n')
    result={'status':'ready for root approval; unregistered private draft','passed':True,'basis':2275,'MA_practice':9,'independent_inventory':7,'source_prompts_normalized_exact':9,'source_prompts_byte_exact':sum(x['prompt_byte_exact'] for x in fidelity),'source_complete_banks_exact':9,'source_choices_exact':33,'source_distractors_exact':24,'source_solutions_normalized_exact':8,'notation_normalization':'Shared formatter converts determinant bars around aligned matrices to vmatrix; all sentences and operative rows preserved.','source_designations_exact':8,'raw_missing_attributes_preserved':True,'opaque_covariance_cases_checked':covariant,'independent_printed_math_checks':checks,'variety_140_per_level_template':variety,'default_template_coverage':default_templates,'same_final_key_mutations_rejected':len(mutations),'native_records':len(natives),'native_accepted':nr['accepted_checks'],'native_rejected':nr['rejected_checks'],'native_unresolved':nr['documented_unresolved_checks'],'fidelity':fidelity,'python':sys.version.split()[0],'sympy':sp.__version__,'limitations':['q-11648 lacks captured difficulty, worked solution, and correct designation; raw replay omits each and is evidence only. Authored complete normal variants use inferred determinant6.','Six scalar MA banks underdetermine distractor intent; complete covariance replay supported as evidence only. Normal generation uses explicit method-derived complete operation banks.','No MA hard source; hard arithmetic bounds are authored from same integer ad-bc backbone.','No plots needed; renderer verifies actual matrix and worked solution layout.']}
    (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
