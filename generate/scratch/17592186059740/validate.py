#!/usr/bin/env python3
"""Fail-closed source/display/native verification for scalar-matrix-v1.
Reads actual printed TeX, independent of metadata and generator math helpers.
Writes local artifacts only; the real native grader uses memory-only fixtures.
"""
from __future__ import annotations
import copy
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from collections import Counter
from fractions import Fraction
import sympy as sp

HERE=Path(__file__).resolve().parent
SCRIPT=HERE.with_suffix('.py')
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('scalar_matrix',SCRIPT)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def write(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def ensure(condition,message):
    if not condition:raise AssertionError(message)
def fraction_tex(s):
    """Restricted independent readback grammar: exact rational arithmetic only."""
    s=s.strip()
    pattern=r'\\frac\{(-?\d+)\}\{(\d+)\}'
    s=re.sub(pattern,lambda m:'('+m[1]+'/'+m[2]+')',s)
    s=s.replace(r'\cdot','*').replace(' ','')
    ensure(bool(re.fullmatch(r'[\d()*/+\-]+',s)),'Unexpected printed entry grammar: '+s)
    import ast
    def parse(n):
        if isinstance(n,ast.Constant) and type(n.value)==int:return Fraction(n.value)
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -parse(n.operand)
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.UAdd):return parse(n.operand)
        if isinstance(n,ast.BinOp):
            a,b=parse(n.left),parse(n.right)
            if isinstance(n.op,ast.Mult):return a*b
            if isinstance(n.op,ast.Div):return a/b
            if isinstance(n.op,ast.Add):return a+b
            if isinstance(n.op,ast.Sub):return a-b
        raise AssertionError('Unsupported AST')
    return parse(ast.parse(s,mode='eval').body)
def matrices(s):
    return [([[fraction_tex(a) for a in row.split('&')] for row in body.split(r'\\')],body) for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)]
def displayed_instance(record):
    P=record['question'][':question/problem'];found=matrices(P)
    ensure(len(found)==1,'Prompt must provide one matrix.')
    A=found[0][0]
    if P.startswith('What is $'):scalar=P.split('$')[1].split(r'\begin')[0]
    elif P.startswith('$'):scalar=P[1:].split(r'\begin')[0]
    else:scalar=re.search(r'Calculate \$([^$]+)\$',P)[1][:-1]
    return fraction_tex(scalar),A

def format_text(s):
    ensure(not any(ord(c)<32 and c not in '\n\t\r' for c in s),'Unexpected C0 control character.')
    ensure(s.count('$')%2==0,'Unbalanced dollar delimiters.')
    n=0
    for c in s:
        if c=='{':n+=1
        elif c=='}':n-=1
        ensure(n>=0,'Unbalanced TeX brace closing.')
    ensure(n==0,'Unbalanced TeX brace opening.')

def inspect_record(record,allow_raw_error=False):
    ensure(set(record['knowledge_point'])=={'db_id','id','title'},'Wrong outer KP shape.')
    ensure(record['knowledge_point']['db_id']==g.KP_ID,'Wrong KP.')
    q=record['question'];meta=record['generation'];raw=meta['evidence_only']
    ensure(meta['eligible_for_learning']==(not raw),'Evidence eligibility contract.')
    k,A=displayed_instance(record)
    ensure(A and all(len(row)==len(A[0]) for row in A),'Printed matrix nonrectangular.')
    expected=[[k*a for a in row] for row in A]
    for s in [q[':question/problem'],q.get(':question/worked-solution','')]:format_text(s)
    mp=meta['parameters']
    ensure(k==Fraction(mp['k']) and A==[[Fraction(a) for a in row] for row in mp['matrix']],'Prompt does not agree with slots.')
    flat=sum(A,[])
    if not raw:
        if meta['template']=='entries_2x2':
            table=q[':question/problem'].splitlines()[-3:]
            row1=table[0].split('|')[1:-1];row2=table[2].split('|')[1:-1]
            ensure(len(row1)==len(row2)==5,'Blank table width.')
            ensure([i for i,c in enumerate(row1) if '{{' in c]==[i for i,c in enumerate(row2) if '{{' in c]==[2,3],'Normal blank rows must align by semantic position.')
        level=meta['difficulty']
        # Independent arithmetic workloads on printed reduced numbers.
        if level=='easy':
            ensure(k.denominator==1 and (k==0 or 2<=abs(k)<=7),'Easy scalar scope.')
            ensure(all(abs(a)<=7 and a.denominator<=7 for a in flat),'Easy entries scope.')
            ensure(sum(a.denominator!=1 for a in flat)<=1,'Easy fraction count.')
        elif level=='moderate':
            ensure(len(flat)==6 and abs(k)==Fraction(1,2),'Moderate product count/scalar.')
            ensure(all(a and a.denominator==1 and abs(a)<=9 for a in flat),'Moderate entries.')
            ensure(sum(abs(a.numerator)%2==1 for a in flat)==3,'Moderate exactly three half products.')
        elif level=='hard':
            ensure(len(flat)==6 and abs(k) in [Fraction(2,3),Fraction(3,4),Fraction(2,5),Fraction(3,5)],'Hard scalar.')
            ensure(all(1<=abs(a.numerator)<=5 and 2<=a.denominator<=5 and abs(a)<4 for a in flat),'Hard fraction slots.')
            ensure(sum(math.gcd(abs(k.numerator*a.numerator),k.denominator*a.denominator)>1 for a in flat)==3,'Hard cancellation workload.')
            ensure(sum((k*a).denominator>1 for a in flat)>=4,'Hard fractional results.')
        else:raise AssertionError('Unsupported level')
    if ':question/worked-solution' in q:
        S=q[':question/worked-solution'];ms=matrices(S)
        ensure(len(ms)==3,'Solution must retain input, unevaluated products, evaluated result.')
        ensure(ms[0][0]==A,'Solution input matrix mismatch.')
        ensure(ms[1][0]==expected and ms[2][0]==expected,'Independently evaluated printed stages.')
        ensure(ms[1][1].count(r'\cdot')==len(flat),'Missing unevaluated cell product stage.')
        for cell in re.split(r'&|\\\\',ms[1][1]):
            ensure(cell.count(r'\cdot')==1,'Each intermediate entry has exactly one product.')
            lhs,rhs=cell.split(r'\cdot')
            ensure(fraction_tex(lhs)==k,'Intermediate scalar mismatch.')
        rhs_entries=[fraction_tex(cell.split(r'\cdot')[1]) for cell in re.split(r'&|\\\\',ms[1][1])]
        ensure(rhs_entries==flat,'Product entry order mismatch.')
        row_count=2 if meta['template']=='direct' else 3
        ensure(S.count('& =')==row_count,'Family aligned row count mismatch.')
        prose=re.search(r'by \$([^$]+)\$',S)[1].rstrip(',')
        if meta['profile']=='raw_320075' and allow_raw_error:ensure(fraction_tex(prose)==3,'Raw error changed.')
        else:ensure(fraction_tex(prose)==k,'Incorrect scalar in solution prose.')
    else:ensure(raw and meta['profile'] in ['raw_979','raw_986'],'Normal output missing worked solution.')
    fields=q[':question/answer-fields'];all_ids=[]
    for f in fields:
        key=f[':answer-field/key'];kind=f[':answer-field/type'].rsplit('/',1)[-1]
        choices=f[':answer-field/choices'];ensure(choices,'Empty bank.')
        uuid=f[':answer-field/id'];__import__('uuid').UUID(uuid)
        vals=[];correct=f.get(':answer-field/correct',[None,None])[1]
        for a in choices:
            __import__('uuid').UUID(a[':answer/id']);all_ids.append(a[':answer/id'])
            ensure(a[':answer/type']==':answer.type/math','Wrong answer type.')
            ensure('$' not in a[':answer/value'],'Math value must be delimiter-free.')
            ensure(':answer/feedback' not in a,'Invented feedback.')
            format_text(a[':answer/value'])
            value=matrices(a[':answer/value'])[0][0] if kind=='radio' else fraction_tex(a[':answer/value'])
            vals.append(value)
            if a[':answer/id']==correct:
                ensure(value==(expected if kind=='radio' else sum(expected,[])[int(key.split('-')[1])-1]),'Selected answer wrong.')
        ensure(len(all_ids)==len(set(all_ids)),'Field-owned UUID collision.')
        if kind=='radio':
            ensure(len(choices)==5,'Source five-option contract.')
            ensure(all((len(v),len(v[0]))==(len(A),len(A[0])) for v in vals),'Wrong option matrix size.')
            ensure(all(vals[i]!=vals[j] for i in range(len(vals)) for j in range(i)),'Pairwise whole-bank ambiguity including wrong/wrong.')
            ensure(sum(v==expected for v in vals)==1,'Radio needs exactly one mathematical answer.')
        else:
            ensure(len(choices)==1 and '{{'+key+'}}' in q[':question/problem'],'Blank contract/placeholder.')
        if not correct:ensure(raw and meta['profile'] in ['raw_979','raw_986'],'Missing normal correct ref.')
        else:ensure(any(a[':answer/id']==correct for a in choices),'Correct ownership.')
    return k,A

def fidelity(source,cases):
    coverage=[]
    for case in cases:
        q=next(q for q in source['record'][':knowledge-point/questions'] if q[':question/math-academy-id']==case['source_id'])
        r=g.generate(case['level'],template=case['template'],profile=case['bank_profile'],parameters=case['parameters']);rq=r['question'];inspect_record(r,allow_raw_error=True)
        ensure(q[':question/problem']==rq[':question/problem'],'Exact prompt fidelity '+case['source_id'])
        for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:
            ensure((key in q)==(key in rq),'Source attribute-presence mismatch '+key)
        ensure(q.get(':question/worked-solution')==rq.get(':question/worked-solution'),'Full worked-solution exact fidelity.')
        fs=q[':question/answer-fields'];gs=rq[':question/answer-fields']
        ensure([f[':answer-field/key'] for f in fs]==[f[':answer-field/key'] for f in gs],'Raw Pull field order changed.')
        count=0
        for f,h in zip(fs,gs):
            ensure(f[':answer-field/type'][':db/ident']==h[':answer-field/type'],'Type fidelity.')
            ensure((':answer-field/correct' in f)==(':answer-field/correct' in h),'Correct presence fidelity.')
            source_values=sorted(a[':answer/value'] for a in f[':answer-field/choices']);generated_values=sorted(a[':answer/value'] for a in h[':answer-field/choices'])
            ensure(source_values==generated_values,'Every complete answer value exact fidelity.')
            if ':answer-field/correct' in f:
                ref=h[':answer-field/correct'][1];v=next(a[':answer/value'] for a in h[':answer-field/choices'] if a[':answer/id']==ref)
                ensure(v==f[':answer-field/correct'][':answer/value'],'Source designation fidelity.')
            count+=len(source_values)
        coverage.append({'source_id':case['source_id'],'exact_prompt':True,'exact_existing_solution':':question/worked-solution' in q,'values_matched':count,'fields':len(fs),'existing_correct_designations_matched':sum(':answer-field/correct' in f for f in fs),'raw_presence_parity':True,'raw_eligible_for_learning':False})
    return coverage

def native_input(record,label):
    checks=[]
    for i,f in enumerate(record['question'][':question/answer-fields']):
        correct=f[':answer-field/correct'][1];a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==correct)
        if f[':answer-field/type'].endswith('/radio'):
            for choice in f[':answer-field/choices']:
                checks.append({'field_index':i,'submitted_answer_id':choice[':answer/id'],'expected':'accepted' if choice[':answer/id']==correct else 'rejected','purpose':'owned option grading; displayed mathematics independently checked'})
        else:
            val=fraction_tex(a[':answer/value'])
            # Unreduced numerator/denominator is a genuinely distinct equivalent
            # learner expression, rather than a string already simplified by CAS.
            equiv=r'\frac{'+str(val.numerator*3)+'}{'+str(val.denominator*3)+'}'
            wrong=str(val+1)
            for submitted,expected,purpose in [(a[':answer/value'],'accepted','canonical entry'),(equiv,'accepted','unreduced equivalent rational entry'),(wrong,'rejected','wrong corresponding entry')]:
                checks.append({'field_index':i,'submitted':submitted,'expected':expected,'purpose':purpose})
    return {'label':label,'record':record,'checks':checks}

def expect_reject(callback):
    try:callback()
    except (AssertionError,ValueError):return
    raise AssertionError('Expected invalid mutation or parameter rejection.')

def main():
    # A failing run must replace any stale successful validation artifact.
    write('validation.json',{'status':'running','qa_passed':False})
    source=json.loads((HERE/'source.json').read_text());cases=json.loads((HERE/'source-cases.json').read_text())
    immutable=ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186059740.json'
    ensure((HERE/'source.json').read_bytes()==immutable.read_bytes(),'Immutable wrapper changed.')
    coverage=fidelity(source,cases)
    records=[];catalog=[];samples=[];native=[];seen=Counter();fingerprints={l:set() for l in ['easy','moderate','hard']};firstpositions=set()
    for level in ['easy','moderate','hard']:
        for seed in range(220):
            r=g.generate(level,seed);inspect_record(r);ensure(r==g.generate(level,seed),'Deterministic rerun failed.')
            seen[(level,r['generation']['template'],r['generation']['profile'])]+=1;fingerprints[level].add(r['generation']['mathematical_fingerprint'])
            samples.append(r)
            if seed<2:
                catalog.append({'label':f'generated {level} seed{seed}','record':r});native.append(native_input(r,f'{level}-seed{seed}'))
            f=r['question'][':question/answer-fields'][0]
            if f[':answer-field/type'].endswith('/radio'):firstpositions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
    ensure(len(firstpositions)==5,'Correct radio choice does not vary through all positions.')
    for level in ['easy','moderate','hard']:
        ensure(set(t for l,t,p in seen if l==level)==set(t for t,p in g.defaults(level)),'Default family coverage failure.')
        ensure(len(fingerprints[level])>=140,'Too little meaningful sampled variety.')
    # Every source family/bank reviewed at original and changed parameters,
    # raw public evidence at original and changed parameters both math-tested.
    for case in cases:
        raw=g.generate('easy',profile=case['bank_profile'],parameters=case['parameters']);catalog.append({'label':'ORIGINAL raw replay '+case['source_id'],'captured_original':next(q for q in source['record'][':knowledge-point/questions'] if q[':question/math-academy-id']==case['source_id']),'record':raw})
        fixture=copy.deepcopy(raw)
        for f in fixture['question'][':question/answer-fields']:
            if ':answer-field/correct' not in f:
                fk,fA=displayed_instance(fixture);true_value=[[fk*a for a in row] for row in fA]
                match=next(a for a in f[':answer-field/choices'] if matrices(a[':answer/value'])[0][0]==true_value)
                f[':answer-field/correct']=[':answer/id',match[':answer/id']]
                fixture['generation']['fixture_inferred_correct']='memory-only source-key completion; raw API output remains unchanged'
        native.append(native_input(fixture,'source-bank-'+case['source_id']+(' inferred-key fixture' if case['source_id'] in ['q-979','q-986'] else ' existing-key')))
        raw_p=copy.deepcopy(case['parameters']);raw_p['name']='R'
        if raw_p['k']!=0:raw_p['k']=raw_p['k']+1 if raw_p['k']>0 else raw_p['k']-1
        else:raw_p['matrix'][0][0]=2
        changed=g.generate('easy',profile=case['bank_profile'],parameters=raw_p);inspect_record(changed,allow_raw_error=True);catalog.append({'label':'CHANGED raw evidence recipe '+case['source_id'],'record':changed})
        normal_profile={'raw_979':'observed_979','raw_986':'method_named_3x2','raw_125885':'observed_zero','raw_980':'observed_980'}.get(case['bank_profile'],'entries')
        normal=g.generate('easy',profile=normal_profile,parameters=case['parameters']);inspect_record(normal);catalog.append({'label':'NORMAL original parameters '+case['source_id'],'record':normal});native.append(native_input(normal,'normal-'+case['source_id']))
        original=next(q for q in source['record'][':knowledge-point/questions'] if q[':question/math-academy-id']==case['source_id'])
        if ':question/worked-solution' in original:
            expected_solution=original[':question/worked-solution']
            if case['source_id']=='q-320075':expected_solution=expected_solution.replace('by $3,$','by $-7,$',1)
            ensure(normal['question'][':question/worked-solution']==expected_solution,'Normal full solution fidelity beyond raw replay.')
        variant=g.generate('easy',seed=19,profile=normal_profile);inspect_record(variant);catalog.append({'label':'GENERATED same family '+case['source_id'],'record':variant});native.append(native_input(variant,'changed-'+case['source_id']))
        # Fixed params/template/profile retains content identity across option order.
        a=g.generate('easy',seed=0,profile=normal_profile,parameters=case['parameters']);b=g.generate('easy',seed=15,profile=normal_profile,parameters=case['parameters'])
        ensure(a['question'][':question/id']==b['question'][':question/id'],'Seed/order changed content identity.')
        ensure(a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'],'Seed changed task fingerprint.')
    # All normal supported complete profiles exercised under public conditions.
    for profile,(template,bank_kind,raw,*_) in g.PROFILES.items():
        if raw:continue
        for level in ['easy']+(['moderate','hard'] if profile.startswith('method_') and template not in ['what_2x2'] else []):
            for seed in range(10):inspect_record(g.generate(level,seed,profile=profile))
    # Cosmetically renamed matrices and zero-scalar irrelevant entries deduplicate.
    base=g.generate('easy',profile='entries',parameters={'k':2,'matrix':[[1,2],[3,4]],'name':'A'})
    rename=g.generate('easy',profile='entries',parameters={'k':2,'matrix':[[1,2],[3,4]],'name':'C'})
    ensure(base['generation']['mathematical_fingerprint']==rename['generation']['mathematical_fingerprint'],'Cosmetic name inflated math identity.')
    zero_a=g.generate('easy',profile='observed_zero',parameters={'k':0,'matrix':[[1,-1,-3],[-5,0,2]],'name':'W'})
    zero_b=g.generate('easy',profile='observed_zero',parameters={'k':0,'matrix':[[2,-2,-4],[-6,1,3]],'name':'W'})
    ensure(zero_a['generation']['mathematical_fingerprint']==zero_b['generation']['mathematical_fingerprint'],'Zero input entries inflated math task capacity.')
    method=g.generate('easy',profile='method_what',parameters=g.RAW_PARAMS['raw_979'])
    observed=g.generate('easy',profile='observed_979',parameters=g.RAW_PARAMS['raw_979'])
    ensure(method['question'][':question/id']!=observed['question'][':question/id'],'Different displayed banks share identity.')
    ensure(method['generation']['mathematical_fingerprint']==observed['generation']['mathematical_fingerprint'],'Bank inflated math fingerprint.')
    # Math-stage and prose mutations fail even when final answers remain correct.
    for mutation in ['products','scalarprose','control','correct','wrongwrong','placeholder','final']:
        r=copy.deepcopy(base)
        if mutation=='products':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(r'2\cdot 1','2',1)
        elif mutation=='scalarprose':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('by $2,','by $3,')
        elif mutation=='control':r['question'][':question/problem']+='\x0c'
        elif mutation=='correct':r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='3'
        elif mutation=='placeholder':r['question'][':question/problem']=r['question'][':question/problem'].replace('{{field-3}}','')
        elif mutation=='final':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('2 & 4','2 & 5')
        else:
            r=copy.deepcopy(method);f=r['question'][':question/answer-fields'][0];wrong=[a for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1]];wrong[0][':answer/value']=wrong[1][':answer/value']
        expect_reject(lambda:inspect_record(r))
    explicit_failures=[('easy','entries',{'k':8,'matrix':[[1,2],[3,4]]}),('moderate','method_named_2x3',{'k':'1/2','matrix':[[1,2,3],[4,5,11]]}),('moderate','method_named_2x3',{'k':2,'matrix':[[1,2,3],[4,5,6]]}),('hard','method_named_2x3',{'k':'2/3','matrix':[['1/2']*3,['1/2']*3]}),('hard','method_named_3x2',{'k':'1/3','matrix':[['1/2']*2]*3}),('easy','observed_979',{'k':2,'matrix':[[1,0],[0,2]]})]
    for l,p,params in explicit_failures:expect_reject(lambda:g.generate(l,profile=p,parameters=params))
    fraction_blank=g.generate('easy',profile='entries',parameters={'k':3,'matrix':[['1/2',-2],[3,0]],'name':'M'})
    inspect_record(fraction_blank);catalog.append({'label':'GENERATED easy fractional blank boundary','record':fraction_blank});native.append(native_input(fraction_blank,'fractional-blank-boundary'))
    write('review.json',catalog);write('native-input.json',native)
    engine=ROOT/'generate/runs/current/check-engine';out=HERE/'native-grading.json'
    result=subprocess.run([str(engine),str(HERE/'native-input.json'),str(out)],capture_output=True,text=True)
    ensure(result.returncode==0,'Actual native grading failed: '+result.stdout+result.stderr)
    grade=json.loads(out.read_text());ensure(grade['documented_unresolved_checks']==0,'Unexpected native unresolved.')
    review=['# Scalar multiplication review','All ORIGINAL rows below are public parameterized raw evidence profiles. They preserve absent fields and q320075 source error; evidence profiles are ineligible. NORMAL rows infer missing information and repair prose. Generated levels are authored where absent.']
    for row in catalog:review+=['\n## '+row['label'],g.markdown(row['record'])]
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    # Meaningful capacity conservative lower bounds from actual allowed finite slots.
    # M: fix+half, 2x3, odd positions3, three signed odd numbers and even numbers,
    # require both signs by assigning first odd negative and first even positive.
    moderate_lower=math.comb(6,3)*5**3*4**3
    hard_domains={}
    for k in [Fraction(2,3),Fraction(3,4),Fraction(2,5),Fraction(3,5)]:
        domain={Fraction(n,d) for n in range(1,6) for d in range(2,6) if Fraction(n,d).denominator>1 and Fraction(n,d)<4}
        c=[a for a in domain if math.gcd(k.numerator*a.numerator,k.denominator*a.denominator)>1 and (k*a).denominator>1]
        n=[a for a in domain if math.gcd(k.numerator*a.numerator,k.denominator*a.denominator)==1 and (k*a).denominator>1]
        hard_domains[str(k)]={'cancellation_entries':len(c),'noncancellation_entries':len(n),'2x3_positive_scalar_fixed_mixed_sign_lower_bound':math.comb(6,3)*len(c)**3*len(n)**3}
    report={'status':'passed worker validation; parent independent QA pending','qa_passed':False,'source':g.SOURCE,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'hashes':{'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'source_fidelity':{'practice_originals':7,'exact_prompts':'7/7','complete_banks':'7/7','radio_choices':'20/20','blank_values':'12/12','distractors':'16/16','present_designations':'14/14','missing_designations':2,'existing_complete_solutions_exact':'5/5','mathematically_sound_existing_solutions':'4/5','normal_repaired_existing_solutions':'5/5','absent_worked_solutions':2,'unrated_originals':2,'attribute_presence_parity':'7/7','cases':coverage},'source_native_fixtures':{'complete_original_banks':7,'original_missing_key_memory_only_inferences':2,'raw_generator_omissions_remain_unchanged':True},'source_errors':[{'source_id':'q-320075','evidence':'prose says3; prompt and all calculation rows use-7','normal_correction':'derive prose coefficient from actual scalar','raw_profile':'raw_320075','raw_eligible_for_learning':False}], 'presentation_repairs':[{'sources':['q-320045','q-320075','q-320082'],'raw':'lower-row blanks incolumns2/3 versus upper-row3/4','normal':'move bottom-row padding so both rows usecolumns3/4; field1..4 remain row-major'}], 'source_interpretation_limits':[{'source_id':'q-986','detail':'Last-row(-2,10) underidentifies historical intent; explicit sign/add recipe numerically reproduces it, evidence-only. Normal method bank uses omitted rows/scalar and reversed scalar sign.'}],'sampled_math_display_checks':len(samples),'default_coverage':[{'level':l,'template':t,'profile':p,'count':v} for (l,t,p),v in sorted(seen.items())],'sampled_meaningful_tasks':{l:len(v) for l,v in fingerprints.items()},'capacity_lower_bounds':{'easy_nonzero_what_family':12*4*6*6,'easy_zero_2x3_tasks':1,'moderate_2x3':moderate_lower,'hard_2x3':sum(d['2x3_positive_scalar_fixed_mixed_sign_lower_bound'] for d in hard_domains.values()),'hard_fraction_slot_domains':hard_domains,'policy':'Conservative guaranteed valid subset; excludes labels, profiles, scalar0 irrelevant operands and option order.'},'native_grading':{k:grade[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks','database_writes']},'mutation_checks':7,'explicit_rejection_checks':len(explicit_failures),'plots':'none','calculator_requirement':'unknown; absent captured attribute is not a false flag','unresolved':['Historical author intent for q986 compound last-row distractor remains underidentified; public raw evidence is ineligible.','Moderate and hard difficulty labels are authored scope claims, not recovered observations.','Parent independent QA pending.']}
    write('validation.json',report)
    print(json.dumps({k:report[k] for k in ['status','source_fidelity','sampled_meaningful_tasks','native_grading','capacity_lower_bounds']},indent=2))
if __name__=='__main__':
    try:main()
    except Exception as exc:
        write('validation.json',{'status':'failed','qa_passed':False,'error':str(exc)})
        raise
