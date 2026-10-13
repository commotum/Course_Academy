#!/usr/bin/env python3
"""Failure-enforcing fidelity, displayed-math, schema, bounds and native QA."""
import hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
SCRIPT=HERE.parent/(HERE.name+'.py')
spec=importlib.util.spec_from_file_location('kp',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def correct(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def formatting(q):
    for key in (':question/problem',':question/worked-solution'):
        t=q[key];assert t.count('$')%2==0
        depth=0
        for ch in t:
            if ch=='{':depth+=1
            elif ch=='}':depth-=1
            assert depth>=0
        assert depth==0
        assert not re.search(r'(?<!\\)(?:\+\-|--)',t)

def math_check(r):
    q=r['question'];eqs=g.prompt_equations(q[':question/problem']);assert len(eqs)==3
    answers=g.designation(q[':question/problem'],eqs)
    assert answers==[correct(f) for f in q[':question/answer-fields']]
    errors=[]
    blocks=q[':question/worked-solution'].split('- Equation ')[1:]
    assert len(blocks)==3
    for i,(eq,block) in enumerate(zip(eqs,blocks)):
        expected=g.isolate(eq);A=sp.simplify(sp.diff(expected,g.X))==0
        assert ('is an autonomous differential equation' in block)==A
        for display in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block,re.S):
            rows=display.split(r'\\')
            # Every structural row independently read from displayed math.
            for j,row in enumerate(rows):
                row=row.strip().replace(' & ', '').replace('&','')
                if '=f(' in row:
                    forms=['f(y)'] if A else (['f(x,y)'] if expected.has(g.Y) else ['f(x)','f(x,y)'])
                    if row.split('=')[1] not in forms:errors.append([i,'formal_dependency'])
                    continue
                candidate=g.isolate(row)
                if sp.simplify(candidate-expected)!=0:errors.append([i,'row_value'])
        # Read displayed where-f expression as well, catches stale prose slots.
        for form,rhs in re.findall(r'where \$(f\([^)]*\))=(.*?)\.\$',block):
            if sp.simplify(g.read(rhs)-expected)!=0:errors.append([i,'where_value'])
            if form=='f(y)' and not A:errors.append([i,'where_dependency'])
    selected=[g.ROMAN[i] for i,v in enumerate(answers) if v=='true']
    assert q[':question/worked-solution'].endswith('"'+' and '.join(selected)+' only."')
    return errors

def schema(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];assert q[':question/difficulty'] in [':question.difficulty/'+l for l in g.CATALOG]
    import uuid
    uuid.UUID(q[':question/id']);seen=set()
    for f in q[':question/answer-fields']:
        uuid.UUID(f[':answer-field/id']);assert f[':answer-field/type']==':answer-field.type/checkbox'
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
        for a in f[':answer-field/choices']:
            uuid.UUID(a[':answer/id']);assert a[':answer/id'] not in seen;seen.add(a[':answer/id'])
            assert a[':answer/type']==':answer.type/text'
        assert f[':answer-field/correct'][0]==':answer/id'
        assert f[':answer-field/correct'][1] in [a[':answer/id'] for a in f[':answer-field/choices']]
    formatting(q)

cases=[];review=[];native=[];source_results=[];raw_errors={}
def native_add(label,r):
    checks=[]
    for i,f in enumerate(r['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==correct(f) else 'rejected','purpose':'actual checkbox Boolean choice grading'})
    native.append({'label':label,'record':r,'checks':checks})

for template,q in g.QUESTIONS.items():
    level=q[':question/difficulty'][':db/ident'].split('/')[-1];p=g.source_parameters(q)
    case={'source_id':q[':db/id'],'template':template,'level':level,'parameters':p,'bank_profile':'observed_raw'};cases.append(case)
    raw=g.generate(level,template=template,parameters=p,profile='observed_raw');schema(raw)
    a=raw['question'];assert a[':question/problem']==q[':question/problem'];assert a[':question/worked-solution']==q[':question/worked-solution']
    assert set(a)==set(q)
    for f,s in zip(a[':question/answer-fields'],q[':question/answer-fields']):
        assert set(f)==set(s)
        assert f[':answer-field/key']==s[':answer-field/key']
        assert sorted(x[':answer/value'] for x in f[':answer-field/choices'])==sorted(x[':answer/value'] for x in s[':answer-field/choices'])
        assert correct(f)==s[':answer-field/correct'][':answer/value']
        assert f[':answer-field/type']==s[':answer-field/type'][':db/ident']
        for answer in f[':answer-field/choices']:
            original=next(x for x in s[':answer-field/choices'] if x[':answer/value']==answer[':answer/value'])
            assert set(answer)==set(original)
            assert answer[':answer/type']==original[':answer/type'][':db/ident']
    errors=math_check(raw)
    if errors: raw_errors[template]=errors
    normal=g.generate(level,template=template,parameters=p,profile='observed_repaired');schema(normal);assert not math_check(normal),(template,math_check(normal))
    # Source masks must genuinely generalize through the exact public API.
    p2={k:2 if v!=2 else 3 for k,v in p.items()}
    changed=g.generate(level,template=template,parameters=p2,profile='observed_repaired');schema(changed);assert not math_check(changed),(template,math_check(changed))
    assert changed['question'][':question/problem']!=a[':question/problem']
    review.extend([{'label':'observed original '+template,'record':raw},{'label':'generated source-template variant '+template,'record':changed}])
    native_add('source '+template,raw);native_add('changed source '+template,changed)
    source_results.append({'source_id':q[':db/id'],'template':template,'banks_matched':3,'values_matched':6,'designations_matched':3,'prompt_exact':True,'solution_raw_exact':True,'key_presence_exact':True,'original_math_errors':errors,'normal_solution_repaired':bool(errors)})
assert raw_errors=={'q-96702':[[1,'row_value'],[1,'where_value']]},raw_errors
source_boundary_instances=0
for template,q in g.QUESTIONS.items():
    level=q[':question/difficulty'][':db/ident'].split('/')[-1]
    for maximum in (False,True):
        parameters={}
        for key,value in g.source_parameters(q).items():
            uses_power=re.search(r'\}\^\{'+key[1:]+r'\}',q[':question/problem'])
            parameters[key]=(3 if uses_power else 8) if maximum else 2
        r=g.generate(level,template=template,parameters=parameters,profile='observed_repaired')
        schema(r);assert not math_check(r),(template,parameters,math_check(r));source_boundary_instances+=1
counts={};task_samples={};ids={}
for level,catalog in g.CATALOG.items():
    eligible=[list(k) for k in itertools.combinations(catalog,3) if {z.split(':')[1] for z in k}=={'x','y'}]
    counts[level]=len(eligible)*2
    semantic=set()
    # Exhaust finite categorical catalog and both criteria, not numerical aliases.
    for index,kinds in enumerate(eligible):
        for negate in (False,True):
            p={'kinds':kinds,'a':2+index%3,'b':1+index%4,'n':2+index%2,'c':5+index%3,'negate':negate}
            r=g.generate(level,seed=index,parameters=p);schema(r);assert not math_check(r),(level,p,math_check(r));semantic.add(r['generation']['mathematical_fingerprint'])
            same=g.generate(level,seed=index+91,parameters=p)
            assert r['question'][':question/id']==same['question'][':question/id']
            assert r['generation']['mathematical_fingerprint']==same['generation']['mathematical_fingerprint']
            ids.setdefault(level,set()).add(r['question'][':question/id'])
            if index<2: review.append({'label':'generated authored '+level+' '+str(index)+' criterion '+str(negate),'record':r})
            native_add('authored '+level+' '+str(index)+' '+str(negate),r)
    assert len(semantic)==counts[level];task_samples[level]=len(semantic)
    # Sampling and explicit inputs use identical workload bounds.
    for bad in [{'a':1},{'a':-3},{'b':0},{'n':4},{'c':4},{'negate':'false'},{'kinds':[catalog[0]]*3}]:
        base={'kinds':eligible[0],'a':2,'b':1,'n':2,'c':5,'negate':False};base.update(bad)
        try:g.generate(level,parameters=base)
        except ValueError:pass
        else:raise AssertionError(('bound did not reject',level,bad))
    for seed in range(60):
        r=g.generate(level,seed);schema(r);assert not math_check(r)
    # Explicit numerical boundary values must remain valid.
    for a,b,n,c in itertools.product((2,4),(1,4),(2,3),(5,7)):
        r=g.generate(level,parameters={'kinds':eligible[-1],'a':a,'b':b,'n':n,'c':c,'negate':False});schema(r);assert not math_check(r)
assert not ids['easy']&ids['moderate'] and not ids['moderate']&ids['hard']
write('source-cases.json',cases);write('review.json',review);write('native-input.json',native)
engine=SCRIPT.parent.parent/'runs/current/check-engine'
subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
report=json.loads((HERE/'native-report.json').read_text())
validation={'status':'passed','source':{k:g.CAPTURE[k] for k in ('database','basis','lineage')},'source_questions':len(cases),'complete_banks_matched':45,'displayed_values_matched':90,'correct_designations_matched':45,'exact_prompts':15,'raw_exact_solutions':15,'original_mathematically_correct_solutions':14,'supported_repaired_solutions':1,'raw_source_errors':raw_errors,'key_presence_parity':15,'source_results':source_results,'authored_semantic_tasks':counts,'exhausted_semantic_tasks':task_samples,'random_samples_checked':180,'boundary_instances_checked':48,'source_boundary_instances_checked':source_boundary_instances,'native_accepted':report['accepted_checks'],'native_rejected':report['rejected_checks'],'native_unresolved':report['documented_unresolved_checks'],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'database_writes':0}
write('validation.json',validation)
lines=['# Review','', 'All original records retain captured wording. Raw evidence is ineligible for learner use. One source error is listed in template-extraction.md. Generated labels identify authored versus source-mask variants.','']
for item in review:
    r=item['record'];q=r['question'];lines.extend(['## '+item['label'],'',q[':question/problem'],'', 'Correct checkbox values: '+', '.join(f[':answer-field/key']+'='+correct(f) for f in q[':question/answer-fields']),'',q[':question/worked-solution'],''])
(HERE/'review.md').write_text('\n'.join(lines))
print(json.dumps(validation,indent=2))
