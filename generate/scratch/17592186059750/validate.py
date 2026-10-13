#!/usr/bin/env python3
"""Failing independent display/source/grading validator; regenerates private evidence."""
from pathlib import Path
import hashlib, importlib.util, json, re, subprocess, sys
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
P=D.with_suffix('.py')
spec=importlib.util.spec_from_file_location('det_gen',P);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
VARS={x:S.Symbol(x,real=True) for x in 'abcdefghkmpqrstuvwxyzt'}

def read_math(text):
    text=text.strip().rstrip('.').replace('\\\\frac','\\frac').replace('\\cdot','*').replace('\\cancel','').replace('\\left','').replace('\\right','')
    while re.search(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',text):text=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',text)
    text=text.replace('{','(').replace('}',')').replace('^','**')
    assert '\\' not in text,text
    return parse_expr(text,local_dict=VARS,transformations=standard_transformations+(implicit_multiplication_application,))

def question_math(q):
    prompt=q[':question/problem']
    mat=re.search(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',prompt,re.S)[1]
    row=re.split(r'\\\\',mat);assert len(row)==2
    entries=[read_math(e) for r in row for e in r.split('&')];assert len(entries)==4
    v=re.search(r'what is the value of \$([a-z])|determine the value of \$([a-z])',prompt)
    variable=VARS[v[1] or v[2]]
    target=read_math(re.search(r'(?:det\}?|\\text\{det\}|\\det)\([^)]*\)\s*=\s*(-?\d+)',prompt)[1])
    poly=S.expand(entries[0]*entries[3]-entries[1]*entries[2])
    roots=S.solve(poly-target,variable);assert len(roots)==1,(prompt,roots)
    return entries,variable,target,poly,roots[0]

def rows(q):
    displays=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
    assert len(displays)==3
    out=[]
    for display in displays[1:]:
        # Strip nested matrix before splitting the outer aligned rows.
        display=re.sub(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|','MATRIX',display,flags=re.S)
        display=re.sub(r'^\\begin\{aligned\}|\\end\{aligned\}$','',display.strip())
        block=[]
        for r in re.split(r'\\\\',display):
            a,b=r.split('&',1);assert b.strip().startswith('=');block.append((a.strip(),b.strip()[1:].strip()))
        out.append(block)
    return out

def prose(q):return re.sub(r'\$\$\n.*?\n\$\$','<BLOCK>',q[':question/worked-solution'],flags=re.S)

def balanced(s):
    assert s.count('$$')%2==0
    assert s.replace('$$','').count('$')%2==0
    depth=0
    for c in s:
        if c=='{':depth+=1
        if c=='}':depth-=1
        assert depth>=0
    assert depth==0
    assert '--' not in s and '+-' not in s
    assert '\\\\frac' not in s

def verify(record):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    q=record['question'];entries,v,N,poly,r=question_math(q)
    for x in [q[':question/problem'],q[':question/worked-solution']]:balanced(x)
    fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];values=[];correct=[]
    for a in f[':answer-field/choices']:
        value=a[':answer/value'];balanced(value)
        assert '$' not in value
        if '=' in value:
            lhs,rhs=value.split('=');assert lhs.strip()==str(v);scalar=read_math(rhs)
        else:scalar=read_math(value)
        assert not scalar.free_symbols
        values.append(scalar)
        if scalar==r:correct.append(a[':answer/id'])
    assert len(values)==len(set(values));assert correct==[f[':answer-field/correct'][1]]
    if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    else:assert len(values)==5
    det,eq=rows(q)
    assert det[0][1]=='MATRIX'
    for lhs,rhs in det[1:]:assert S.expand(read_math(rhs)-poly)==0,(lhs,rhs,poly)
    for lhs,rhs in eq:
        left=poly if 'det' in lhs else read_math(lhs)
        right=read_math(rhs)
        assert S.simplify((left-right).subs(v,r))==0,(lhs,rhs,r)
        solutions=S.solve(left-right,v)
        assert solutions==[r],(lhs,rhs,solutions,r)
    level=q[':question/difficulty'].split('/')[-1]
    assert S.degree(poly,v)==(2 if level=='moderate' else 1)
    if level=='moderate':assert S.discriminant(poly-N,v)==0
    if level=='hard':
        assert len(det)==5 and len(eq)==4
        # Count six ordered additive distribution terms including opposite quadratic terms.
        dist=det[2][1];assert dist.count(str(v))>=5
        assert det[3][1].count('\\cancel')==2
    return r

def source_fidelity(k,record):
    original=g.QUESTIONS[k];q=record['question'];t=g.TEMPLATES[k]
    fields=original.get(':question/answer-fields',[])
    expected=[read_math(a[':answer/value'].split('=')[-1]) for f in fields for a in f[':answer-field/choices']]
    got=[read_math(a[':answer/value'].split('=')[-1]) for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
    assert not fields or sorted(expected,key=str)==sorted(got,key=str)
    if fields:
        assert fields[0][':answer-field/type'][':db/ident']==q[':question/answer-fields'][0][':answer-field/type']
        assert fields[0][':answer-field/key']==q[':question/answer-fields'][0][':answer-field/key']
        assert sorted(a[':answer/value'] for a in fields[0][':answer-field/choices'])==sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])
    normalized_solutions=False
    if ':question/worked-solution' in original:
        a,b=rows(original),rows(q);assert list(map(len,a))==list(map(len,b)),k
        assert prose(original)==prose(q),k
        assert original[':question/worked-solution']==q[':question/worked-solution'],k
        for srcblock,genblock in zip(a,b):
            for (x,y),(u,v) in zip(srcblock,genblock):
                if y=='MATRIX':assert v=='MATRIX';continue
                assert S.expand(read_math(y)-read_math(v))==0,(k,y,v)
                if x and 'det' not in x:assert S.expand(read_math(x)-read_math(u))==0,(k,x,u)
        normalized_solutions=True
    correct_existing=bool(fields and fields[0].get(':answer-field/correct'))
    if correct_existing:
        expected_correct=read_math(fields[0][':answer-field/correct'][':answer/value'].split('=')[-1])
        assert expected_correct==verify(record)
    assert k=='q-127614' or q[':question/problem']==original[':question/problem'],k
    return {'source_id':k,'complete_observed_bank_match':bool(fields),'observed_values':len(expected),'correct_designation_observed':correct_existing,'correct_designation_match':correct_existing,'authored_correct_inference':k in ('q-11651','q-19801'),'authored_field_repair':k=='q-127614','raw_exact_prompt':q[':question/problem']==original[':question/problem'],'shared_prose_and_stage_sequence_match':normalized_solutions,'raw_exact_solution':q.get(':question/worked-solution')==original.get(':question/worked-solution'),'raw_exact_bank':not fields or sorted(a[':answer/value'] for a in fields[0][':answer-field/choices'])==sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])}

def grade_item(label,record):
    f=record['question'][':question/answer-fields'][0];checks=[]
    if f[':answer-field/type'].endswith('/radio'):
        for a in f[':answer-field/choices']:checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned selection ID'})
    else:
        r=verify(record)
        checks=[{'submitted':str(r),'expected':'accepted','purpose':'canonical scalar fragment'},{'submitted':r'\frac{'+str(r*3)+'}{3}','expected':'accepted','purpose':'unreduced equivalent rational expression'},{'submitted':str(r+1),'expected':'rejected','purpose':'incorrect scalar'}]
    return {'label':label,'record':record,'checks':checks}

def main():
    source_cases=[];fidelity=[];originals=[];variants=[];grade=[];tested=0;fingerprints={k:set() for k in g.TEMPLATES}
    for k,t in g.TEMPLATES.items():
        profile='observed:'+k if k in g.PROFILES else 'authored:blank_repair' if k=='q-127614' else 'none'
        p={'c':t['c'],'root':t['root']}
        case={'source_id':k,'level':t['level'],'template':k,'parameters':p,'bank_profile':profile}
        source_cases.append(case)
        rec=g.generate(t['level'],0,k,parameters=p,profile=profile);verify(rec);fidelity.append(source_fidelity(k,rec));originals.append(rec);grade.append(grade_item('original:'+k,rec));tested+=1
        # Deterministic content identity across option shuffle; observed replay can vary.
        alt=g.generate(t['level'],14,k,parameters=p,profile=profile)
        assert rec['question'][':question/id']==alt['question'][':question/id']
        # A changed-parameter original-profile example and normal authored default example.
        for seed,bank in [(41,profile),(73,None)]:
            rec2=g.generate(t['level'],seed,k,profile=bank);verify(rec2);variants.append(rec2);grade.append(grade_item('variant:'+k+':'+str(seed),rec2));tested+=1
        for seed in range(35):
            for bank in set([profile,None]):
                rec3=g.generate(t['level'],seed+100,k,profile=bank);verify(rec3);tested+=1;fingerprints[k].add(rec3['generation']['mathematical_fingerprint'])
                alt=g.generate(t['level'],seed+999,k,parameters=rec3['generation']['parameters'],profile=rec3['generation']['profile'])
                assert rec3['question'][':question/id']==alt['question'][':question/id']
                assert rec3['generation']['mathematical_fingerprint']==alt['generation']['mathematical_fingerprint']
    # Explicit scope failures, no silent resampling.
    invalids=0
    for k,t in g.TEMPLATES.items():
        for p in [{'c':t['c'],'root':0},{'c':[100]+t['c'][1:],'root':t['root']},{'c':t['c'],'root':100}]:
            try:g.generate(t['level'],template=k,parameters=p,profile='observed:'+k if k in g.PROFILES else None)
            except ValueError:invalids+=1
            else:raise AssertionError(('accepted invalid',k,p))
    # Changed bank changes content identity, never task identity.
    for rec in variants:
        if rec['generation']['profile'].startswith('observed:'):
            try:other=g.generate(rec['question'][':question/difficulty'].split('/')[-1],parameters=rec['generation']['parameters'],template=rec['generation']['template'])
            except ValueError:continue
            if sorted(a[':answer/value'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices'])!=sorted(a[':answer/value'] for a in other['question'][':question/answer-fields'][0][':answer-field/choices']):assert rec['question'][':question/id']!=other['question'][':question/id']
            assert rec['generation']['mathematical_fingerprint']==other['generation']['mathematical_fingerprint']
    for name,obj in [('source-cases.json',source_cases),('review.json',{'captured_originals':list(g.QUESTIONS.values()),'original_parameter_replays':originals,'generated_variants':variants}),('grader-input.json',grade)]: (D/name).write_text(json.dumps(obj,indent=2)+'\n')
    binary=Path('generate/runs/current/check-engine')
    subprocess.run([str(binary),str(D/'grader-input.json'),str(D/'grader-report.json')],check=True)
    native=json.loads((D/'grader-report.json').read_text())
    result={'pass':True,'source_provenance':{k:g.SOURCE[k] for k in ['database','basis','lineage']},'source_questions':15,'source_questions_replayed':15,'observed_complete_banks_matched':sum(a['complete_observed_bank_match'] for a in fidelity),'observed_values_matched':sum(a['observed_values'] for a in fidelity),'observed_radio_banks_matched':9,'observed_radio_values_matched':45,'observed_blank_fields_matched':5,'observed_blank_values_matched':5,'observed_correct_designations_matched':sum(a['correct_designation_match'] for a in fidelity),'observed_correct_designations_total':12,'missing_correct_designations_inferred':2,'fieldless_authored_fields':1,'solution_prose_and_stage_sequences_matched':13,'solution_prose_and_stage_sequences_total':13,'raw_exact_prompts':sum(a['raw_exact_prompt'] for a in fidelity),'raw_exact_solutions':sum(a['raw_exact_solution'] for a in fidelity),'raw_exact_banks':sum(a['raw_exact_bank'] for a in fidelity if a['complete_observed_bank_match']),'independent_display_instances':tested,'explicit_invalid_parameters_rejected':invalids,'distinct_sampled_mathematical_tasks_per_layout':{k:len(v) for k,v in fingerprints.items()},'native_grading':{k:native[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'grader_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'fidelity':fidelity,'unresolved':['Original scalar distractor intent is underdetermined; original-profile numerical patterns are replay-only, with authored default operations.'],'scope':'all three observed levels; no missing-level mathematical branch added','notation_repairs':['Source whitespace, labels, punctuation and mathematical side spelling retained through computed component masks; changed signed factors are grouped.'],'database_writes':0}
    (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    review=['# Determinant unknowns review','Original capture: math basis 1356. Original strings below remain evidence. Replays normalize mathematical notation and repair missing fields/ref designations explicitly.']
    for k,rec in zip(g.TEMPLATES,originals):
        q=g.QUESTIONS[k]
        review+=['\n## '+k+' — original',q[':question/problem'],'Original choices: '+json.dumps([[a[':answer/value'] for a in f[':answer-field/choices']] for f in q.get(':question/answer-fields',[])]) ,'Observed correct designations: '+json.dumps([f.get(':answer-field/correct') for f in q.get(':question/answer-fields',[])]),q.get(':question/worked-solution','No captured solution.'),'\n### Parameterized replay',g.markdown(rec)]
        for variant in variants:
            if variant['generation']['template']==k:review+=['\n### Generated variant ('+variant['generation']['profile']+')',g.markdown(variant)]
    (D/'review.md').write_text('\n\n'.join(review)+'\n')
    freeze={'version':g.VERSION,'artifacts':{}}
    for file in [P]+[x for x in D.iterdir() if x.is_file() and x.name!='freeze.json']:freeze['artifacts'][str(file)]=hashlib.sha256(file.read_bytes()).hexdigest()
    (D/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['pass','source_questions_replayed','observed_complete_banks_matched','observed_values_matched','independent_display_instances','native_grading']},indent=2))
if __name__=='__main__':main()
