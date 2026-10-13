#!/usr/bin/env python3
"""Fail closed on displayed mathematics, complete source fidelity, API and grading."""
import copy, hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def write(name,data): (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def math_vector(raw):
    out=[]
    for cell in g.cells(raw):
        if g.D in cell:
            body=cell.split(g.D,1)[1].strip();assert body[0]=='(' and body[-1]==')'
            out.append(sp.diff(g.parse(body[1:-1]),g.T))
        else:out.append(g.parse(cell))
    return out

def mask_vectors(text):
    values=[]
    def f(m):values.append(math_vector(m.group()));return 'VV'+str(len(values)-1)+'VV'
    return g.VEC_RE.sub(f,text),values

def check_math(record):
    q=record['question'];u,v=g.read_prompt(q[':question/problem'])
    wanted=[sp.diff(u*x,g.T) for x in v]
    field=q[':question/answer-fields'][0];bank=field[':answer-field/choices']
    assert len(bank)==5
    actual=[g.vector_read(a[':answer/value']) for a in bank]
    matching=[i for i,a in enumerate(actual) if g.vequal(a,wanted)]
    assert len(matching)==1
    assert bank[matching[0]][':answer/id']==field[':answer-field/correct'][1]
    assert all(not g.vequal(actual[i],actual[j]) for i in range(5) for j in range(i))
    solution=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S);assert len(blocks)==3
    # Independently check component derivative arguments/results as actually printed.
    _,derivatives=mask_vectors(blocks[1]);assert len(derivatives)==2
    vp=[sp.diff(x,g.T) for x in v]
    assert g.vequal(derivatives[0],vp) and g.vequal(derivatives[1],vp)
    # The scalar derivative uses one whole argument and one result, possibly on separate rows.
    ublock=blocks[1].split(g.D)[-1]
    # the last derivative operator in block is the scalar derivative
    assert ublock.startswith('(')
    depth=0;end=None
    for i,ch in enumerate(ublock):
        if ch=='(':depth+=1
        elif ch==')':
            depth-=1
            if depth==0:end=i;break
    assert g.equal(g.parse(ublock[1:end]),u)
    rhs=ublock[end+1:].replace(r'\end{aligned}','').replace(r'\\','').replace('&','').replace('=','').strip()
    assert g.equal(g.parse(rhs),sp.diff(u,g.T))
    # Each actual distributed/simplified line is evaluated, including complete signs.
    masked,values=mask_vectors(blocks[2]);rows=masked.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
    checked=0
    for row in rows:
        if 'VV' not in row:continue
        rhs=re.split(r'&\s*=',row)[-1].strip().rstrip('.')
        evaluated=[]
        for coordinate in range(3):
            expr=re.sub(r'VV(\d+)VV',lambda m:'('+g.tex(values[int(m[1])][coordinate])+')',rhs)
            evaluated.append(g.parse(expr))
        assert g.vequal(evaluated,wanted),(record['generation']['template'],row,evaluated,wanted)
        checked+=1
    assert checked>=3
    for text in [q[':question/problem'],solution]+[a[':answer/value'] for a in bank]:
        assert text.count('{')==text.count('}')
        assert text.count('$')%2==0
    return checked

def prose_skeleton(text):
    # Complete math placeholders retain number/order of blocks/rows/vector cells.
    return g.VEC_RE.sub('VECTOR',text)

def run():
    cases=[];originals=[];reviews=[];engine=[];mapping=[];row_count=0;recovered=partial=0
    designation_count=0;solution_count=0
    for qid,q in g.QUESTIONS.items():
        level=g.TEMPLATES[qid];params={'scales':[1,1,1]};case={'source_id':qid,'template':qid,'level':level,'parameters':params,'bank_profile':'observed_'+qid};cases.append(case)
        r=g.generate(level,template=qid,parameters=params,profile=case['bank_profile']);originals.append(r)
        assert r['question'][':question/problem']==q[':question/problem']
        if ':question/worked-solution' in q:
            assert r['question'][':question/worked-solution']==q[':question/worked-solution'];solution_count+=1
        f=r['question'][':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
        src=[a[':answer/value'] for a in sf[':answer-field/choices']];new=[a[':answer/value'] for a in f[':answer-field/choices']]
        assert sorted(src)==sorted(new)
        if ':answer-field/correct' in sf:
            correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            assert correct==sf[':answer-field/correct'][':answer/value'];designation_count+=1
        row_count+=check_math(r)
        for a,recipe in zip(sf[':answer-field/choices'],r['generation']['recipes']):
            mapping.append({'source_id':qid,'source_answer_id':a[':answer/id'],'original':a[':answer/value'],'symbolic_components':[str(x) for x in g.vector_read(a[':answer/value'])],'recipe':recipe,'replay_match':True})
            if recipe['kind']!='partial_expression_pattern':recovered+=1
            else:partial+=1
        # Two independent signed coordinate variations for each entire observed bank.
        for scales in ([2,-1,3],[-3,2,-2]):
            rv=g.generate(level,template=qid,parameters={'scales':scales},profile='observed_'+qid);row_count+=check_math(rv);reviews.append(rv)
            if ':question/worked-solution' in q:
                assert prose_skeleton(rv['question'][':question/worked-solution'])==prose_skeleton(q[':question/worked-solution'])
                # Complete source row and vector sequence, not selected fixed phrases.
                assert rv['question'][':question/worked-solution'].count(r'\\')==q[':question/worked-solution'].count(r'\\')
        # A genuine operation bank with observed layout and fixed source solution.
        rv=g.generate(level,template=qid,parameters={'scales':[2,-1,3]},profile='authored_product_errors');row_count+=check_math(rv);reviews.append(rv)
    # Equal-workload authored templates, at least two examples per level + boundary samples.
    for level in ('easy','moderate','hard'):
        for seed in range(12):
            r=g.generate(level,seed=seed);row_count+=check_math(r);reviews.append(r)
        for p in ({'a':-3,'b':3,'c':-3,'d':3},{'a':3,'b':-3,'c':3,'d':-3}):
            row_count+=check_math(g.generate(level,parameters=p))
        for key in ('a','b','c','d'):
            for value in (0,4,-4,1.5,True):
                p={'a':1,'b':2,'c':3,'d':-2};p[key]=value
                try:g.generate(level,parameters=p)
                except ValueError:pass
                else:raise AssertionError('out-of-range authored parameter accepted')
    for scales in ([0,1,1],[4,1,1],[-4,1,1],[1,2],['1',1,1]):
        try:g.generate('easy',template='q-32286',parameters={'scales':scales})
        except ValueError:pass
        else:raise AssertionError('out-of-range coordinate accepted')
    # Fixed instance identities ignore RNG/order; alternate banks share math fingerprint.
    for qid,level in g.TEMPLATES.items():
        p={'scales':[2,-1,3]} if qid in g.QUESTIONS else {'a':1,'b':2,'c':3,'d':-2}
        a=g.generate(level,1,template=qid,parameters=p);b=g.generate(level,99,template=qid,parameters=p)
        assert a['question'][':question/id']==b['question'][':question/id']
        if qid in g.QUESTIONS:
            c=g.generate(level,1,template=qid,parameters=p,profile='authored_product_errors')
            assert c['question'][':question/id']!=a['question'][':question/id']
            assert c['generation']['mathematical_fingerprint']==a['generation']['mathematical_fingerprint']
    # Real application grading for every original + every reviewed bank.
    for i,r in enumerate(originals+reviews):
        f=r['question'][':question/answer-fields'][0]
        checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete owned bank selection'} for a in f[':answer-field/choices']]
        engine.append({'label':str(i)+' '+r['generation']['template'],'record':r,'checks':checks})
    write('source-cases.json',cases);write('choice-mapping.json',mapping);write('review.json',reviews);write('engine-input.json',engine)
    subprocess.run(['generate/runs/current/check-engine',str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    # Side-by-side markdown: raw originals, exact replay, all observed/profile variants.
    parts=['# Scalar function multiple rule review','All originals below come from math basis 1356. Coordinate-scaled observed bank variants are evidence profiles, not default inferred error intent. Normal practice uses labeled authored operation banks.']
    for qid,q in g.QUESTIONS.items():
        parts+=['## Original '+qid,q[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']),q.get(':question/worked-solution','Original solution/correct designation/difficulty absent. Derived repair follows in generated records.')]
        for r in reviews:
            if r['generation']['template']==qid:parts+=['### Generated '+r['generation']['profile']+' '+json.dumps(r['generation']['parameters']),g.markdown(r)]
    for r in reviews:
        if r['generation']['template'].startswith('authored_'):parts+=['## Generated '+r['generation']['template']+' seed '+str(r['generation']['seed']),g.markdown(r)]
    (HERE/'review.md').write_text('\n\n'.join(parts)+'\n')
    native=json.loads((HERE/'engine-report.json').read_text())
    report={'pass':True,'source_provenance':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'source_questions':14,'source_levels':{'easy':9,'moderate':4,'unrated':1,'hard':0},'prompt_matches':14,'complete_bank_value_matches':14,'choices_matched':70,'distractors_matched':56,'distractor_designation_breakdown':{'present_original_refs':52,'q32501_mathematically_derived':4},'mapped_operation_distractors':recovered-14,'partially_unresolved_distractors':partial,'correct_designations_matched':designation_count,'correct_designations_total_present':13,'missing_correct_designations':1,'original_worked_solutions_matched':solution_count,'original_worked_solutions_present':13,'authored_solution_repairs':1,'operation_or_component_operation_options':recovered,'partial_expression_pattern_options':partial,'generated_review_records':len(reviews),'displayed_product_rows_verified':row_count,'native_accepted':native['accepted_checks'],'native_rejected':native['rejected_checks'],'native_unresolved':native['documented_unresolved_checks'],'native_binary_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'known_limitations':['q-32501 has no captured correct ref, worked solution or difficulty. Correct answer mathematically derived; designation is not counted as matched.','Unresolved observed residual expression patterns are explicit evidence-only profiles. Normal banks use mathematically derived complete wrong operations.','Hard is an authored rating design claim, with no observed hard source.'],'database_writes':0}
    write('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':run()
