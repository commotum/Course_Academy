#!/usr/bin/env python3
"""Independent decoded-display parser and native grader validation; no DB writes."""
from pathlib import Path
import importlib.util,itertools,json,re,subprocess,sys
from functools import lru_cache
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py')); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
s,c=sp.symbols('s c',real=True)

def replace_group(text,command,arity):
    while command in text:
        start=text.index(command); i=start+len(command); groups=[]
        for _ in range(arity):
            while i<len(text) and text[i].isspace(): i+=1
            if text[i]!='{': raise AssertionError(('missing group',text))
            begin=i+1; depth=1; i+=1
            while depth:
                depth+=(text[i]=='{')-(text[i]=='}'); i+=1
            groups.append(text[begin:i-1])
        replacement=('('+transcribe(groups[0])+')/('+transcribe(groups[1])+')') if arity==2 else '('+transcribe(groups[0])+')'
        text=text[:start]+replacement+text[i:]
    return text

def transcribe(text):
    text=text.replace('⁡','').replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos').replace('{sin}',r'\sin').replace('{cos}',r'\cos')
    text=re.sub(r'\\(sin|cos)\s*(?:\^\s*(\{[23]\}|[23]))?\s*(?:\\theta|θ|x|t)',lambda m:' '+('s' if m[1]=='sin' else 'c')+('**'+m[2].strip('{}') if m[2] else '')+' ',text)
    text=replace_group(text,r'\frac',2)
    text=replace_group(text,r'\cancel',1)
    text=text.replace(r'\cdot','*').replace(r'\left','').replace(r'\right','').replace('{','(').replace('}',')').replace('^','**').strip().rstrip('.')
    if '\\' in text or 'sin' in text or 'cos' in text: raise AssertionError(('unparsed display',text))
    return text

@lru_cache(maxsize=None)
def parse(text): return parse_expr(transcribe(text),local_dict={'s':s,'c':c},transformations=standard_transformations+(implicit_multiplication_application,))
@lru_cache(maxsize=None)
def equivalent(a,b):
    n=sp.together(a-b).as_numer_denom()[0]
    return sp.rem(sp.Poly(sp.expand(n),c,s),sp.Poly(c*c+s*s-1,c,s)).as_expr()==0

def expression(q):
    math=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/problem'],re.S)[0]
    return parse(math.rstrip('=. '))
def stages(q):
    out=[]
    for block in re.findall(r'\$\$(.*?)\$\$',q.get(':question/worked-solution',''),re.S):
        block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
        for row in block.split(r'\\'):
            for part in row.replace('&','').split('='):
                if part.strip(): out.append(parse(part.strip()))
    return out

def check(record):
    q=record['question']; target=expression(q)
    meta=record['generation']; observed=meta['profile'] in ['observed_raw','observed_completed']
    assert meta['evidence_only']==observed and meta['eligible_for_learning']==(not observed)
    heading=g.markdown(record).splitlines()[0]
    assert ('evidence-only' in heading)==observed
    if meta['profile']=='observed_raw' and ':question/difficulty' not in q:
        assert 'Unrated' in heading and 'original difficulty absent' in heading and '### Easy' not in heading
    if meta['difficulty_origin']=='inferred completion': assert 'Inferred Easy' in heading and 'original difficulty absent' in heading
    if meta['template']=='cos_reciprocal' and not observed:
        selected=meta['bank_profile']; assert selected in g.COS_BANKS
        assert meta['parameters']['a'] in g.COS_BANKS[selected]['a_values']
        assert tuple(meta['bank_recipes'])==g.COS_BANKS[selected]['recipes']
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    field=q[':question/answer-fields'][0]; bank=[parse(a[':answer/value']) for a in field[':answer-field/choices']]
    assert len(bank)==5
    assert all(not equivalent(bank[i],bank[j]) for i in range(5) for j in range(i))
    matches=[i for i,a in enumerate(bank) if equivalent(a,target)]
    assert len(matches)==1,(q[':question/problem'],bank)
    if ':answer-field/correct' in field:
        assert field[':answer-field/choices'][matches[0]][':answer/id']==field[':answer-field/correct'][1]
    rows=stages(q)
    if record['generation']['profile']=='authored':
        blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)
        assert len(blocks)==4 and len(rows)==8
        if record['generation']['template'] in ['cross_single','cross_double']:
            distributed=transcribe(blocks[0].split('=')[1])
            assert len(re.findall(r's\s+c',distributed))==(2 if record['generation']['template']=='cross_double' else 1)
            assert distributed.count('s**2')==1 and distributed.count('c**2')==1
    assert all(equivalent(row,target) for row in rows),(q[':question/problem'],rows)
    texts=[q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in field[':answer-field/choices']]
    for t in texts:
        assert t.count('$')%2==0
        depth=0
        for ch in t:
            if ch=='{': depth+=1
            if ch=='}': depth-=1
            assert depth>=0
        assert depth==0
        assert '--' not in t and '+-' not in t
    return len(rows)

def native_item(record,label):
    field=record['question'][':question/answer-fields'][0]
    return {'label':label,'record':record,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'independently verified complete displayed bank'} for a in field[':answer-field/choices']]}

def main():
    # Preserve every previously frozen question's ID, prompt, solution and complete bank.
    # Choice-order changes on a different sampler path do not alter question data.
    old_review=json.loads((ROOT/'review.json').read_text()) if (ROOT/'review.json').exists() else []
    preserved=0
    def canonical_question(q):
        q=json.loads(json.dumps(q))
        for f in q.get(':question/answer-fields',[]): f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
        return q
    for old in old_review:
        meta=old['generation']; new=g.generate(meta['level'],meta['seed'],template=meta['template'],profile=meta['profile'],parameters=meta['parameters'])
        assert canonical_question(old['question'])==canonical_question(new['question'])
        preserved+=1
    (ROOT/'revision-question-preservation.json').write_text(json.dumps({'previous_review_questions_preserved':preserved,'comparison':'exact learner question data and identities, ignoring option order only'},indent=2)+'\n')
    source_cases=[]; review=[]; native=[]; totals={'source_questions':7,'raw_exact_prompts':0,'raw_exact_banks':0,'raw_exact_existing_solutions':0,'raw_exact_attribute_presence':0,'matched_existing_correct_designations':0,'missing_designations':2,'original_options':35,'matched_options':0,'normal_records_checked':0,'displayed_math_stages':0}
    byte_audit=[]
    for name,q in g.OBSERVED.items():
        p=dict(a=1,b=1,d=1,angle={'paired_squares':'x','cos_ratio':'θ','linear_cos':'t','linear_sin':'t'}.get(name,r'\theta'))
        case={'source_id':q[':question/math-academy-id'],'template':name,'parameters':p,'bank_profile':'observed_raw','assigned_level':'easy','assignment_origin':'observed' if ':question/difficulty' in q else 'authored supported assignment; source unrated'}; source_cases.append(case)
        raw=g.generate('easy',template=name,parameters=p,profile='observed_raw'); rq=raw['question']; check(raw)
        assert rq[':question/problem']==q[':question/problem']; totals['raw_exact_prompts']+=1
        original=sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']); generated=sorted(a[':answer/value'] for a in rq[':question/answer-fields'][0][':answer-field/choices']); assert original==generated; totals['raw_exact_banks']+=1; totals['matched_options']+=5
        for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:
            assert (key in q)==(key in rq)
        of=q[':question/answer-fields'][0]; rf=rq[':question/answer-fields'][0]
        assert (':answer-field/correct' in of)==(':answer-field/correct' in rf); totals['raw_exact_attribute_presence']+=1
        if ':question/worked-solution' in q:
            assert rq[':question/worked-solution']==q[':question/worked-solution']; totals['raw_exact_existing_solutions']+=1
        if ':answer-field/correct' in of: totals['matched_existing_correct_designations']+=1
        byte_audit.append({'source_id':case['source_id'],'decoded_backslash_runs':{key:[len(m[0]) for m in re.finditer(r'\\+',q.get(key,''))] for key in [':question/problem',':question/worked-solution']},'note':'single slash commands; double slash only aligned row separators; no TeX repair inferred from serialization'})
        completed=g.generate('easy',template=name,parameters=p,profile='observed_completed'); check(completed); native.append(native_item(completed,case['source_id']+' supported completion'))
        review.append(raw); review.append(completed)
        scaled=g.generate('easy',template=name,parameters=dict(a=3,b=1,d=1,angle='x'),profile='observed_raw'); check(scaled); review.append(scaled)
        scaled_completed=g.generate('easy',template=name,parameters=dict(a=3,b=1,d=1,angle='x'),profile='observed_completed'); check(scaled_completed); native.append(native_item(scaled_completed,name+' source scale3'))
        for seed in [31,92]:
            r=g.generate('easy',seed,template=name); totals['displayed_math_stages']+=check(r); totals['normal_records_checked']+=1; review.append(r); native.append(native_item(r,name+str(seed)))
    for level in ['easy','moderate','hard']:
        for seed in range(80):
            r=g.generate(level,seed); totals['displayed_math_stages']+=check(r); totals['normal_records_checked']+=1
            same=g.generate(level,seed+1000,template=r['generation']['template'],parameters=r['generation']['parameters'])
            assert r['question'][':question/id']==same['question'][':question/id']
            if seed<2 and level!='easy': review.append(r)
            if seed<8: native.append(native_item(r,level+str(seed)))
    # All finite coefficient domains: task aliases and unused parameter values omitted.
    variety={}
    for level,names in g.LEVELS.items():
        fingerprints=set()
        for name in names:
            aa=range(1,7) if level=='easy' else ([*range(-8,-1),*range(2,9)] if level=='moderate' else [*range(-6,-1),*range(2,7)])
            used=['a'] if name in g.NAMES[:5] else ['a','b'] if name!='cross_double' else ['a','b','d']
            bb=range(1,7) if 'b' in used else [1]
            for a,b in itertools.product(aa,bb):
                dd=[d for d in [*range(-6,-1),*range(2,7)] if a*d>0] if level=='hard' else [1]
                for d in dd:
                    r=g.generate(level,template=name,parameters=dict(a=a,b=b,d=d,angle='x')); check(r)
                    fingerprints.add(r['generation']['mathematical_fingerprint'])
        variety[level]=len(fingerprints)
    # Named complete profiles are selected before sampling, constrained for explicit
    # calls, deterministic, and aliases never alter content identities.
    profile_checks=0
    for bank in g.COS_BANKS:
        for seed in range(40):
            r=g.generate('easy',seed,template='cos_reciprocal',profile=bank); check(r)
            assert r==g.generate('easy',seed,template='cos_reciprocal',profile=bank)
            explicit=g.generate('easy',seed,template='cos_reciprocal',profile=bank,parameters=r['generation']['parameters'])
            automatic=g.generate('easy',seed,template='cos_reciprocal',parameters=r['generation']['parameters'])
            assert explicit['question']==automatic['question']
            assert explicit['generation']['bank_profile']==automatic['generation']['bank_profile']==bank
            profile_checks+=1
            if seed==0: native.append(native_item(explicit,bank+' explicit named profile'))
        wrong_a=2 if bank=='cos_reciprocal_unit' else 1
        try: g.generate('easy',template='cos_reciprocal',profile=bank,parameters=dict(a=wrong_a,b=1,d=1,angle='x'))
        except ValueError: profile_checks+=1
        else: raise AssertionError('ineligible named bank silently switched')
    # Both explicit inputs and samplers enforce the same domain/workload guards.
    invalid=[('easy','linear_cos',dict(a=7,b=1,d=1,angle='x')),('moderate','cross_single',dict(a=1,b=1,d=1,angle='x')),('moderate','cross_single',dict(a=-9,b=1,d=1,angle='x')),('hard','cross_double',dict(a=2,b=1,d=-2,angle='x')),('hard','cross_double',dict(a=0,b=1,d=2,angle='x'))]
    for level,name,p in invalid:
        try: g.generate(level,template=name,parameters=p)
        except ValueError: pass
        else: raise AssertionError('accepted invalid explicit workload')
    for file,data in [('source-cases.json',source_cases),('review.json',review),('decoded-byte-audit.json',byte_audit),('native-input.json',native)]: (ROOT/file).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    proc=subprocess.run(['generate/runs/current/check-engine',str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],capture_output=True,text=True)
    assert proc.returncode==0,proc.stderr
    report=json.loads((ROOT/'native-report.json').read_text())
    result={'status':'passed','basis':1356,'source_fidelity':totals,'variety':variety,'native_grading':{k:report[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'explicit_guard_rejections':len(invalid),'named_profile_checks':profile_checks,'prior_question_data_preserved':preserved,'observed_replay_eligibility':'all evidence-only; authored defaults eligible','limits':['Two originals have no correct designation, difficulty or worked solution. Infer correct values2 and1 only in supported completion; no matched-designation claim for either.','Raw replay parameterizes complete angle slots and a common scalar1–6 across every mathematical object/stage/bank; normal inside-coefficient variation and new solutions are separately authored.','Observed scalar/mixed banks do not establish recovered misconception intent.','No plots or database writes.']}
    (ROOT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'review.md').write_text('# Original evidence and generated variants\n\nBasis1356. Raw records retain original omissions; completed repairs and authored coefficients are labeled. Angle aliases do not count as distinct math tasks.\n\n'+'\n\n'.join(g.markdown(r) for r in review)+'\n')
    print(json.dumps(result,indent=2)); print(proc.stdout.strip())
if __name__=='__main__':main()
