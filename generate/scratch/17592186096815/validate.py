#!/usr/bin/env python3
"""Fail on source/format/math/scope/identity/native grading failures."""
import hashlib, importlib.util, json, math, re, subprocess, uuid, sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('kp',ROOT.with_suffix('.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def save(name,data): (ROOT/name).write_text(json.dumps(data,indent=2)+'\n')
def latex(s):
    """Small independent recursive reader for displayed arithmetic TeX."""
    s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','')
    def group(i):
        assert s[i]=='{';out,j=seq(i+1,'}');return out,j
    def seq(i=0,end=None):
        out=''
        while i<len(s) and s[i]!=end:
            if s.startswith(r'\sqrt',i):
                arg,i=group(i+5);out+='sqrt('+arg+')'
            elif s.startswith(r'\frac',i):
                n,i=group(i+5);d,i=group(i);out+='(('+n+')/('+d+'))'
            elif s[i]=='{':
                arg,i=group(i);out+='('+arg+')'
            else:out+=s[i];i+=1
        return out,i+1 if end else i
    result,_=seq()
    from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
    return parse_expr(result.replace('^','**'),transformations=standard_transformations+(implicit_multiplication_application,))

def from_prompt(text):
    if 'has magnitude' in text:
        vals=[int(x) for x in re.findall(r'has magnitude \$(\d+)\$',text)]
        dirs=re.findall(r'is directed (.*?) and has magnitude',text)
    else:
        vals=[int(x) for x in re.findall(r'\\mid [ab]\|= (\d+)',text)]
        dirs=re.findall(r'is directed (.*?) and \$',text)
    vectors={'horizontally to the right':(1,0),'horizontally to the left':(-1,0),'vertically down':(0,-1),'vertically up':(0,1),'due north-east':(1,1),'due south-east':(1,-1),'due north-west':(-1,1),'due south-west':(-1,-1)}
    assert len(vals)==len(dirs)==2,(vals,dirs)
    u,v=[vectors[x] for x in dirs]; dot=sum(x*y for x,y in zip(u,v));assert dot==0
    # Actual resultant geometry independently; no source/generation coefficients.
    a,b=vals; av=[a*x/sp.sqrt(sum(t*t for t in u)) for x in u];bv=[b*x/sp.sqrt(sum(t*t for t in v)) for x in v]
    N=sp.simplify(sum((x+y)**2 for x,y in zip(av,bv)))
    return a,b,N

def check(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];g=r['generation']; f=q[':question/answer-fields'][0];a,b,N=from_prompt(q[':question/problem'])
    uuid.UUID(q[':question/id']);uuid.UUID(f[':answer-field/id'])
    assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    assert len(q[':question/answer-fields'])==1
    assert len(f[':answer-field/choices'])==5
    vals=[];correct=[]
    for choice in f[':answer-field/choices']:
        uuid.UUID(choice[':answer/id']);assert choice[':answer/type']==':answer.type/math'
        value=choice[':answer/value'];assert value.endswith('(a + b)')
        c=latex(value[:-7]);vals.append(c)
        if sp.simplify(c*c*N)==1:correct.append(choice[':answer/id'])
    assert len(set(vals))==5 and len(correct)==1
    if g['bank_profile'].endswith('_raw'):
        assert ':answer-field/correct' not in f
    else:assert f[':answer-field/correct']==[':answer/id',correct[0]]
    if g['evidence_only']:
        assert not g['eligible_for_learning'];assert ':question/worked-solution' not in q and ':question/difficulty' not in q
    else:
        assert g['eligible_for_learning'];s=q[':question/worked-solution'];n=int(N)
        # Every displayed formal/substitution/squared/addition/final stage is
        # checked against the printed question, with exact ordered node masks.
        mathblocks=re.findall(r'\$\$\n(.*?)\n\$\$',s,re.S);assert len(mathblocks)==4
        assert mathblocks[0]==r'u=\frac{a+b}{|a+b|}'
        rows=mathblocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split('\\\\\n')
        assert rows==[r'|a+b|^2&=|a|^2+|b|^2',f'&={a}^2+{b}^2',f'&={a*a}+{b*b}',f'&={n}']
        for row in rows[1:]:assert sp.simplify(latex(row[2:])-N)==0
        mag=mathblocks[2].split('=');assert mag[0]=='|a+b|' and len(mag)==3
        for rhs in mag[1:]: assert sp.simplify(latex(rhs)**2-N)==0
        rows=mathblocks[3].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split('\\\\\n')
        assert len(rows)==2 and rows[0]==r'u&=\frac{a+b}{|a+b|}'
        final=latex(rows[1][2:]);A,B=sp.symbols('a b');coeff=sp.simplify(final/(A+B));assert sp.simplify(coeff*sp.sqrt(N))==1
    for s in [q[':question/problem'],q.get(':question/worked-solution','')]+[x[':answer/value'] for x in f[':answer-field/choices']]:
        assert s.count('$')%2==0
        assert s.count('{')==s.count('}')
        assert '\\\\frac' not in s # actual adjacent raw bytes, not serialized repr
    return correct[0]

source=json.loads((ROOT/'source.json').read_text())
cases=[{'source_id':'q-12184','template':'cardinal_sum','level':'easy','parameters':{'a':3,'b':4,'orientation':0},'bank_profile':'observed_cardinal_raw'}, {'source_id':'q-12185','template':'compass_sum','level':'hard','parameters':{'a':20,'b':13,'orientation':0},'bank_profile':'observed_compass_raw'}]
save('source-cases.json',cases)
source_records=[]; engine=[]; mapping=[]
for case,original in zip(cases,source['record'][':knowledge-point/questions']):
    r=m.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']); check(r);source_records.append(r)
    assert original[':question/problem']==r['question'][':question/problem']
    ov=[x[':answer/value'] for x in original[':question/answer-fields'][0][':answer-field/choices']]
    gv=[x[':answer/value'] for x in r['question'][':question/answer-fields'][0][':answer-field/choices']]
    assert sorted(ov)==sorted(gv)
    for value in ov:mapping.append({'source_id':case['source_id'],'field_key':'selection','field_type':'radio','value':value,'exact_replay':True,'coefficient':str(latex(value[:-7])),'recipe':'opaque similarity scaling of denominator by new_norm / original_norm','interpretation':'unresolved; evidence only'})
    repaired=m.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'].replace('_raw','_inferred'));check(repaired)
    engine.append({'label':case['source_id']+' inferred designation (original designation missing)','record':repaired,'checks':[{'submitted_answer_id':x[':answer/id'],'expected':'accepted' if x[':answer/id']==check(repaired) else 'rejected','purpose':'inferred correct option/full observed bank native ID grading'} for x in repaired['question'][':question/answer-fields'][0][':answer-field/choices']]})
    changed=m.generate(case['level'],template=case['template'],parameters={'a':8,'b':15,'orientation':1},profile=case['bank_profile']);check(changed);source_records.append(changed)
records=[];unique={}
for level in ['easy','moderate','hard']:
    tasks=set()
    for seed in range(100):
        r=m.generate(level,seed);cid=check(r);tasks.add(r['generation']['parameter_fingerprint'])
        if seed<2:records.append(r)
        if seed<10:engine.append({'label':level+str(seed),'record':r,'checks':[{'submitted_answer_id':x[':answer/id'],'expected':'accepted' if x[':answer/id']==cid else 'rejected','purpose':'complete authored bank native grading'} for x in r['question'][':question/answer-fields'][0][':answer-field/choices']]})
        other=m.generate(level,seed+909,template=r['generation']['template'],parameters=r['generation']['parameters'])
        assert r['question'][':question/id']==other['question'][':question/id']
        assert r['generation']['parameter_fingerprint']==other['generation']['parameter_fingerprint']
    unique[level]=len(tasks)
# The level guard rejects every explicit boundary violation, not just samplers.
invalid=[('easy',{'a':3,'b':5,'orientation':0}),('moderate',{'a':3,'b':4,'orientation':0}),('moderate',{'a':13,'b':2,'orientation':0}),('hard',{'a':3,'b':4,'orientation':0}),('hard',{'a':15,'b':20,'orientation':0}),('hard',{'a':26,'b':13,'orientation':0})]
for level,p in invalid:
    try:m.generate(level,parameters=p)
    except ValueError:pass
    else:raise AssertionError(('scope',level,p))
# Bank/presentation identity distinct; task identity excludes bank/orientation.
x=m.generate('easy',parameters={'a':3,'b':4,'orientation':0})
y=m.generate('easy',parameters={'a':3,'b':4,'orientation':1})
z=m.generate('easy',parameters={'a':3,'b':4,'orientation':0},profile='observed_cardinal_inferred')
assert x['generation']['parameter_fingerprint']==y['generation']['parameter_fingerprint']==z['generation']['parameter_fingerprint']
assert len({x['question'][':question/id'],y['question'][':question/id'],z['question'][':question/id']})==3
# Exhaust all finite authored magnitude domains with every orientation.
finite={}
for level,kind,lo,hi in [('easy','cardinal',2,30),('moderate','cardinal',2,12),('hard','compass',10,25)]:
    count=0;tasks=set()
    for a in range(lo,hi+1):
        for b in range(a+1,hi+1):
            try:m.valid(level,kind,{'a':a,'b':b,'orientation':0})
            except ValueError:continue
            for o in range(len(m.directions(kind))):
                r=m.generate(level,parameters={'a':a,'b':b,'orientation':o});check(r);count+=1;tasks.add(r['generation']['parameter_fingerprint'])
    finite[level]={'mathematical_tasks':len(tasks),'all_oriented_instances_checked':count}
assert [finite[x]['mathematical_tasks'] for x in ['easy','moderate','hard']]==[13,51,115]
save('bank-mapping.json',mapping);save('review.json',source_records+records);save('native-input.json',engine)
proc=subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],capture_output=True,text=True);assert proc.returncode==0,proc.stderr
report={'status':'passed','source_provenance':m.SOURCE,'source_questions':2,'complete_raw_banks_exact':{'matched':2,'total':2},'displayed_options_exact':{'matched':10,'total':10},'source_prompts_exact':{'matched':2,'total':2},'original_correct_designations':{'matched':0,'present':0,'missing':2},'inferred_supported_correct_designations':2,'source_worked_solutions':{'present':0,'raw_omission_preserved':2},'source_difficulty_labels':{'present':0,'raw_omission_preserved':2},'normal_authored_instances_checked':300,'finite_authored_domain_validation':finite,'unique_mathematical_tasks_in_100_seeds':unique,'opaque_profiles':'evidence only; raw and inferred excluded from learning','raw_parallel_criterion':'allows either sign; one eligible option in each complete source bank','normal_direction_clarification_needed':False,'native_grading':json.loads((ROOT/'native-report.json').read_text()),'engine_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'decoded_source_adjacent_backslash_pairs':{c['source_id']:sum(a==b=='\\' for a,b in zip(q[':question/problem'],q[':question/problem'][1:])) for c,q in zip(cases,source['record'][':knowledge-point/questions'])}}
save('validation.json',report)
review=['# Originals and labeled variants','Source: math basis1356; all observed ratings, solutions, and correct refs are absent. Correct refs below are inferred only in native fixtures.']
for c,q in zip(cases,source['record'][':knowledge-point/questions']):
    review+=['\n## Original '+c['source_id'],q[':question/problem']]+['- $'+x[':answer/value']+'$' for x in q[':question/answer-fields'][0][':answer-field/choices']]
for i,r in enumerate(source_records+records):
    review+=['\n## '+('Observed raw bank replay/parameterized evidence variant' if r['generation']['evidence_only'] else 'Authored '+r['generation']['authored_level']+' variant')+' '+str(i+1),m.markdown(r)]
(ROOT/'review.md').write_text('\n\n'.join(review)+'\n')
print(proc.stdout.strip());print('PASS: 2/2 raw source banks, 10/10 values, 300 authored instances; no original designation claimed.')
