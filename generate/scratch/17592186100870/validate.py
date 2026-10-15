"""Independent rendered-shape checks, complete source replay and native grading."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def fingerprint(q): return g.task_key(q)
def object_value(value):
    if value=='The product is undefined':return None
    found=re.fullmatch(r'(\d+)\s*\\(?:times|cdot)\s*(\d+)',value)
    return tuple(map(int,found.groups())) if found else int(value)

def independent(rec):
    q=rec['question'];meta=rec['generation']
    assert rec==g.generate(q[':question/difficulty'].split('/')[-1],meta['seed'],meta['template'],meta['parameters'],meta['bank_profile'])
    text=q[':question/problem'];solution=q[':question/worked-solution']
    factors=re.findall(r'\$([A-Z])\$ is a\s*\$(\d+)\\times (\d+)\$',text)
    assert len(factors)==2, text
    dims={label:(int(r),int(c)) for label,r,c in factors}
    target=re.search(r'\$([A-Z]{2})\??\$',text)[1]
    first,second=target
    a,b=dims[first],dims[second]
    assert a[1]==b[0]
    expected=(sp.MatrixSymbol(first,*a)*sp.MatrixSymbol(second,*b)).shape
    fields=q[':question/answer-fields']
    for f in fields:
        choices=f[':answer-field/choices']
        values=[object_value(c[':answer/value']) for c in choices]
        correct=next(object_value(c[':answer/value']) for c in choices if c[':answer/id']==f[':answer-field/correct'][1])
        answer=expected[0 if f[':answer-field/key']=='field-1' else 1] if f[':answer-field/type']==':answer-field.type/blank' else expected
        assert correct==answer,(text,correct,answer)
        assert len(set(values))==len(values) and values.count(answer)==1
        assert len(set(c[':answer/id'] for c in choices))==len(choices)
        if f[':answer-field/type']==':answer-field.type/blank':
            assert text.count('{{'+f[':answer-field/key']+'}}')==1 and len(choices)==1
    assert f'There are ${a[1]}$ columns in ${first}$ and ${b[0]}$ rows in ${second}.$' in solution
    assert f'${target}$ is a ${a[0]}\\times {b[1]}$ matrix:' in solution
    # Read the actual displayed matrix-shape chain independently of metadata.
    display=solution.split('$$')[1]
    lhs, rhs=display.split('=')
    displayed_factors=re.findall(r'\{([A-Z])\}_',lhs)
    assert displayed_factors==[first,second],(text,display)
    numeric=list(map(int,re.findall(r'\d+',display)))
    assert numeric==[a[0],a[1],b[0],b[1],a[0],b[1]],display
    assert rhs.startswith('{'+target+'}_'),rhs
    for textpart in (text,solution):
        assert textpart.count('$')%2==0 and textpart.count('{')==textpart.count('}')
    assert ':question/math-academy-id' not in q

def checks(rec):
    out=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        if f[':answer-field/type']==':answer-field.type/radio':
            out += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every option in complete observed bank'} for a in f[':answer-field/choices']]
        else:
            answer=f[':answer-field/choices'][0][':answer/value']
            out += [{'field_index':i,'submitted':v,'expected':e,'purpose':'Canonical/equivalent/wrong dimension'} for v,e in [(answer,'accepted'),('('+answer+')+0','accepted'),(answer+'.0','accepted'),(str(int(answer)+1),'rejected'),('0','rejected')]]
    return out

def main():
    replays=[];cases=[];review=[];engine_cases=[];all_ids={};positions={};checked=0;collisions={}
    for template,p in g.DEFAULTS.items():
        old=g.SOURCES[template];rec=g.generate(g.level_of(template),template=template,parameters=p);independent(rec)
        q=rec['question'];assert q[':question/problem']==old[':question/problem']
        assert q[':question/worked-solution']==g.corrected_solution(template)
        matched=0
        for f in q[':question/answer-fields']:
            oldf=next(o for o in old[':question/answer-fields'] if o[':answer-field/key']==f[':answer-field/key'])
            pairs=sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])
            original=sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in oldf[':answer-field/choices'])
            assert pairs==original
            correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            assert correct==oldf[':answer-field/correct'][':answer/value']
            matched+=len(pairs)
        cases.append({'source':template,'profile':template,'matched_values':matched,'total_values':matched,'complete_bank':True,'missing':[],'extra':[],'exact_prompt':True,'solution_correction':template=='q-70702'})
        replays.append(rec);engine_cases.append(rec)
        review.append('## Source '+template+'\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\n### Replay\n\n'+g.markdown(rec))
        slots={k:set() for k in p}
        collisions[template]=0
        for triple in itertools.permutations(range(1,11),3):
            params=dict(zip(('m','n','p'),triple))
            try:r=g.generate(g.level_of(template),13,template,params)
            except ValueError as error:
                assert str(error).startswith('bank_collision:');collisions[template]+=1;continue
            independent(r);checked+=1
            for k,v in params.items():slots[k].add(v)
            identity=r['question'][':question/id'];payload=json.dumps(r['question'],sort_keys=True)
            assert identity not in all_ids or all_ids[identity]==payload
            all_ids[identity]=payload
        positions[template]={k:sorted(v) for k,v in slots.items()}
        for slot,values in positions[template].items():
            excluded=([5] if template=='q-129461' and slot=='p' else [3] if template=='q-70702' and slot=='m' else [])
            assert values==[v for v in range(1,11) if v not in excluded]
        # Change each dimension alone, holding the two other dimensions fixed.
        changed=[]
        for slot in p:
            params=dict(p);params[slot]=next(v for v in range(1,11) if v not in p.values())
            r=g.generate(g.level_of(template),14,template,params);independent(r);engine_cases.append(r);changed.append(r)
        review.append('### One dimension changed at a time\n\n'+'\n\n---\n\n'.join(g.markdown(r) for r in changed))
    for level in g.SUPPORTED_LEVELS:
        records=g.batch(level,24,2636);assert records==g.batch(level,24,2636)
        assert len({fingerprint(r['question']) for r in records})==24
        assert not ({fingerprint(r['question']) for r in records}&{fingerprint(q) for q in g.SOURCES.values()})
        for r in records:independent(r)
        engine_cases.extend(records)
    invalid=0
    for params in [dict(m=0,n=2,p=3),dict(m=11,n=2,p=3),dict(m=2,n=2,p=3),dict(m=2.0,n=3,p=4)]:
        try:g.generate('easy',parameters=params)
        except ValueError:invalid+=1
    assert invalid==4
    try:g.batch('hard',1)
    except ValueError:invalid+=1
    assert invalid==5
    save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(engine_cases)])
    binary=ROOT/'generate/runs/current/check-engine'
    r=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
    (HERE/'engine.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    save('source-cases.json',cases);save('slot-coverage.json',positions)
    save('review.json',{'replays':replays,'engine_cases':engine_cases});(HERE/'review.md').write_text('\n\n---\n\n'.join(review))
    save('validation.json',{'status':'pass','source_basis':g.SNAPSHOT['basis'],'complete_source_banks':len(cases),
         'matched_values':sum(c['matched_values'] for c in cases),'missing_options':[],'extra_options':[],
         'bounded_domain_checks':checked,'rejected_bank_collisions':collisions,'single_slot_checks':27,'deterministic_batches':2,'rejected_invalid_inputs':invalid,
         'fidelity':'Exact complete banks, types, correct designations, prompts and solutions; q-70702 display labels corrected with evidence. Two incomplete unrated sources excluded.',
         'correctness':'Independent prompt, ordered matrix shape, answer objects, prose, display labels and dimensions checked throughout full declared domain.',
         'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},
         'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',binary]}})
    print(json.dumps({'status':'pass','bounded_checks':checked,'engine':{k:v for k,v in engine.items() if k!='records'}}))

if __name__=='__main__':main()
