"""Read displayed matrices independently, replay entire banks, use engine grader."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('row_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')
def matrices(text):
    return [[[x.strip() for x in row.split('&')] for row in block.split(r'\\')] for block in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def numeric(m):return [[int(x) for x in row] for row in m]
def parsed_operation(text):
    match=re.search(r'\$\{R\}_\{(\d)\}:=\{R\}_\{\1\}([+-])(\d)\{R\}_\{(\d)\}\$',text)
    assert match,text
    t,sign,k,s=match.groups();return int(t)-1,int(s)-1,int(k)*(1 if sign=='+' else -1)
def fingerprint(q):
    m=numeric(matrices(q[':question/problem'])[0]);t,s,k=parsed_operation(q[':question/problem'])
    return hashlib.sha256(json.dumps([m[s],m[t],k],separators=(',',':')).encode()).hexdigest()
def check(rec):
    q=rec['question'];p=rec['generation']['parameters'];profile=rec['generation']['profile'];g.validate_parameters(p,profile)
    assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    assert q[':question/difficulty']==':question.difficulty/moderate'
    m=numeric(matrices(q[':question/problem'])[0]);t,s,k=parsed_operation(q[':question/problem'])
    assert (m,t,s,k)==(p['matrix'],p['target'],p['source'],p['k'])
    answer=copy.deepcopy(m)
    for j in range(3):answer[t][j]=m[t][j]+k*m[s][j]
    f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
    assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    choices=f[':answer-field/choices'];assert len(choices)==5
    values=[numeric(matrices(a[':answer/value'])[0]) for a in choices]
    assert len({json.dumps(v) for v in values})==5 and values.count(answer)==1
    selected=[v for a,v in zip(choices,values) if a[':answer/id']==f[':answer-field/correct'][1]];assert selected==[answer]
    assert set(map(json.dumps,values))==set(map(lambda x:json.dumps([[int(v) for v in r] for r in x]),g.bank(p,profile)))
    sol=q[':question/worked-solution'];assert parsed_operation(sol)==(t,s,k)
    stages=matrices(sol);assert len(stages)==3
    assert numeric(stages[0])==m and numeric(stages[2])==answer
    for i in range(3):
        for j in range(3):
            text=stages[1][i][j]
            if i==t:
                match=re.fullmatch(r'(-?\d+)\+\((-?\d+)\)\((-?\d+)\)',text);assert match,text
                a,b,c=map(int,match.groups());assert (a,b,c)==(m[t][j],k,m[s][j]) and a+b*c==answer[i][j]
            else:assert int(text)==m[i][j]
    assert ['first','second','third'][s]+' row to the '+['first','second','third'][t]+' row' in sol
    assert rec['generation']['mathematical_fingerprint']==fingerprint(q)
    assert q[':question/id']==str(g.uuid.uuid5(g.uuid.UUID(g.GENERATOR_UUID),q[':question/problem']+'|'+profile+'|'+g.VERSION))
    assert f[':answer-field/id']==str(g.uuid.uuid5(g.uuid.UUID(q[':question/id']),'selection'))
    for a in choices:
        assert a[':answer/id']==str(g.uuid.uuid5(g.uuid.UUID(f[':answer-field/id']),a[':answer/value']))
        assert a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value']
    for text in [q[':question/problem'],sol]+[a[':answer/value'] for a in choices]:
        assert text.count('$')%2==0
        depth=0
        for c in text:depth+=int(c=='{')-int(c=='}');assert depth>=0
        assert depth==0
    return answer
def native(rec,label):
    f=rec['question'][':question/answer-fields'][0]
    return {'label':label,'record':rec,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all five matrix options through actual radio grader'} for a in f[':answer-field/choices']]}
def main():
    replay=[];review=[];engine=[];coverage={};samples=[]
    for profile,p in g.CASES.items():
        r=g.generate(seed=0,profile=profile,parameters=p);check(r);q=r['question'];old=g.SOURCES[profile]
        assert q[':question/problem']==old[':question/problem']
        expected=sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])
        for field in old[':question/answer-fields']:
            assert expected==sorted(a[':answer/value'] for a in field[':answer-field/choices'])
            if ':answer-field/correct' in field:assert numeric(matrices(field[':answer-field/correct'][':answer/value'])[0])==check(r)
            replay.append({'source':profile,'field_id':field[':answer-field/id'],'matched_options':5,'total_options':5,'missing':[],'extra':[],'correct_designation':'matched' if ':answer-field/correct' in field else 'source missing; excluded legacy field','prompt_exact':True,'solution_stages':'single operation meaning, original matrix, component arithmetic, final matrix','solution_correction':'q-10248 source negates unchanged first row in intermediate matrix; generated retains it' if profile=='q-10248' else None})
        review.append((profile,old,r));engine.append(native(r,'replay '+profile))
        roles=set();multipliers=set();positions=set();fps=set()
        for seed in range(240):
            r=g.generate(seed=seed,profile=profile);check(r);assert r==g.generate(seed=seed,profile=profile)
            other=g.generate(seed=seed+7,profile=profile,parameters=r['generation']['parameters']);check(other)
            assert r['question'][':question/id']==other['question'][':question/id']
            p=r['generation']['parameters'];roles.add((p['source'],p['target']));multipliers.add(p['k']);fps.add(fingerprint(r['question']))
            f=r['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
            engine.append(native(r,profile+' seed '+str(seed)))
            if seed<3:samples.append(r)
        assert roles=={(s,t) for s in range(3) for t in range(3) if s!=t};assert len(multipliers)==4 and positions==set(range(5));assert len(fps)==240
        coverage[profile]={'tested':240,'distinct_tasks':240,'row_roles':sorted(roles),'multipliers':sorted(multipliers),'correct_option_positions':sorted(positions)}
        # Hold all numbers constant and change only the target to another eligible
        # cancellation row. Parsing the actual solution catches stale references.
        p={'matrix':[[-1,2,4],[3,5,6],[3,-1,9]],'source':0,'target':1,'k':3,'name':'M'} if profile=='q-10248' else {'matrix':[[1,2,1],[3,-1,1],[3,3,2]],'source':0,'target':1,'k':-3,'name':'X'}
        a=g.generate(profile=profile,parameters=p);check(a);p['target']=2;b=g.generate(profile=profile,parameters=p);check(b)
        assert a['question'][':question/problem']!=b['question'][':question/problem'] and check(a)!=check(b)
        engine.extend([native(a,profile+' fixed-matrix target 2'),native(b,profile+' fixed-matrix target 3')]);samples.extend([a,b])
    rejected=0
    for change in ({'target':0},{'k':0},{'matrix':[[1,2],[3,4],[5,6]]},{'k':-3}):
        p=copy.deepcopy(g.CASES['q-10248']);p.update(change)
        try:g.generate(profile='q-10248',parameters=p)
        except ValueError:rejected+=1
        else:raise AssertionError('Invalid parameters accepted')
    for level in ('easy','hard'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('Unimplemented band accepted')
    save('source-replay.json',replay);save('samples.json',samples);save('engine-input.json',engine)
    binary=HERE/'reference/check-engine'
    subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'native-grading.json')],check=True)
    save('validation.json',{'passed':True,'source_basis':2366,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'native_binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'source_banks_matched':3,'source_options_matched':15,'coverage':coverage,'changed_target_with_matrix_fixed':True,'rejected_invalid_cases':rejected,'supported_levels':['moderate'],'unimplemented_levels':['easy','hard'],'correctness':'independent displayed operation and every arithmetic stage','grading':'real engine radio grade_field; every option of 486 records','fidelity':'complete moderate banks and prompt bytes; source correction and minor equivalent solution notation documented'})
    md=['# Original and generated review','Basis 2366. Source records are preserved. Moderate one-row addition; five matrix choices; no plots.']
    for profile,old,r in review:md+=['## '+profile,'### Original',old[':question/problem'],old[':question/worked-solution'],'### Parameterized source replay',g.markdown(r)]
    for r in samples:md+=['## Variant '+r['generation']['profile'],json.dumps(r['generation']['parameters']),g.markdown(r)]
    (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
    print(json.dumps({'passed':True,'profiles':coverage,'banks_matched':3,'options_matched':15}))
if __name__=='__main__':main()
