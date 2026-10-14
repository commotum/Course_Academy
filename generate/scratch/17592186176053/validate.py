#!/usr/bin/env python3
"""Independent displayed-semantic, source, identity and native-grade checks."""
import hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from PIL import Image
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('csc',ROOT.with_suffix('.py')); g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def coefficient(tex):
    s=tex.replace('π',r'\pi').replace(' ','')
    m=re.fullmatch(r'(-?)\\frac\{(-?\d*)\\pi\}\{2\}',s)
    if m:return sp.Rational(int((m[1] or '')+(m[2] if m[2] not in ('','-') else m[2]+'1')),2)
    m=re.fullmatch(r'(-?\d*)\\pi',s)
    if m:return sp.Integer(m[1] if m[1] not in ('','-') else m[1]+'1')
    raise AssertionError(('unparsed coefficient',tex))
def independent(record):
    q=record['question'];text=q[':question/problem'];t=record['generation']['template']
    if t=='basic_properties':
        claims=[line for line in text.splitlines() if line.startswith('- **')]; truths=[]
        true={v[0] for v in g.PROPERTIES}; false={v[1] for v in g.PROPERTIES}
        for c in claims:
            v=c.split('** ',1)[1];assert v in true|false;truths.append(v in true)
    elif t=='indexed_properties':
        point=re.search(r'The point \$\((.*?),(-?\d)\)\$',text);c=coefficient(point[1]);y=int(point[2]);truths=[sp.sin(sp.pi*c)!=0 and 1/sp.sin(sp.pi*c)==y]
        asym=re.search(r'\$x=(.*?)\$ is a vertical asymptote',text);truths.append(bool(coefficient(asym[1]).is_integer))
        dom=re.search(r'\$x=(.*?)\$ is in the domain',text);truths.append(not bool(coefficient(dom[1]).is_integer))
        solution=q[':question/worked-solution']; displayed=int(re.search(r'takes the value \$(-?\d)\$',solution)[1]);assert displayed==1/sp.sin(sp.pi*c)
        assert str(truths[0]).lower() in solution.split('Hence, statement I is ')[1].split('.')[0]
    elif t=='q-42912':
        m=re.search(r'point \$\((.*?),(-?\d)\)\$',text);c=coefficient(m[1]);y=int(m[2]);v=int(re.search(r'value \$y = (-?\d+)\$',text)[1]);truths=[sp.sin(sp.pi*c)==0 or 1/sp.sin(sp.pi*c)!=y,True,abs(v)>=1]
    elif t=='q-65310':
        c=coefficient(re.search(r'zero at \$x = (.*?)\$',text)[1]);assert sp.sin(sp.pi*c)!=0
        assert r'x =-\frac{π}{2} + 2nπ' in text
        truths=[True,False,True]
    elif t in ('q-103811','q-65307'):
        c=coefficient(re.search(r'\$x=(.*?)\$ is a vertical asymptote',text)[1]);truths=[False,bool(c.is_integer),True]
        if t=='q-103811':
            shifts=[int(v.replace(' ','')) for v in re.findall(r'x([+-]\d+)\\pi',text)];assert len(shifts)==2 and (shifts[0]-shifts[1])%2==0
            solution=q.get(':question/worked-solution','');assert all(f'x{v:+d}\\pi ' in solution for v in shifts)
    elif t=='q-103814':
        c=coefficient(re.search(r'\$x=(.*?)\$ is a vertical asymptote',text)[1]);m=re.search(r'takes the value \$(-?1)\$ at \$x=(.*?)\$',text);angle=m[2].split('+2n')[0]; truths=[False,bool(c.is_integer),1/sp.sin(sp.pi*coefficient(angle))==int(m[1])]
        solution=q[':question/worked-solution'];assert f'takes the value ${m[1]}$' in solution
    elif t=='q-65308':
        c=coefficient(re.search(r'\$x=(.*?)\$ is in the domain',text)[1]);shift=int(re.search(r'x([+-]\d+)\\pi',text)[1]);truths=[False,shift%2==0,not bool(c.is_integer)]
        solution=q[':question/worked-solution'];n=int(re.search(r'n=(-?\d+),',solution)[1]);assert 2*n==shift;assert re.search(r'so \$(.*?)\$ is not in',solution)[1].strip()==re.search(r'\$x=(.*?)\$ is in',text)[1].strip()
    else:
        c=coefficient(re.search(r'III\.\*\* \$x=(.*?)\$ is in',text)[1]);truths=[False,False,not bool(c.is_integer)]
    solution=q.get(':question/worked-solution','')
    indices={'I':0,'II':1,'III':2}
    assertions=re.findall(r'statement (III|II|I) is (true|false)',solution,re.I)
    for index,value in assertions: assert bool(truths[indices[index.upper()]])==(value.lower()=='true')
    if 'statements I and II are both false' in solution: assert not truths[0] and not truths[1]
    if solution and t not in ('q-42912','q-65310'): assert len(assertions)==3 or (t=='q-103812' and len(assertions)==1)
    mask=sum(1<<i for i,v in enumerate(truths) if v);assert mask==record['generation']['truth_mask']
    fields=q[':question/answer-fields'];assert len(fields)==3
    assert [f[':answer-field/key'] for f in fields]==['I','II','III']
    for i,f in enumerate(fields):
        assert f[':answer-field/type']==':answer-field.type/checkbox'
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
        correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        assert correct[':answer/value']==str(bool(truths[i])).lower()
    if not record['generation']['evidence_only']:
        assert text.count('$')%2==0 and '$$' not in text
        for v in (text,q[':question/worked-solution']): assert v.count('{')==v.count('}') and v.count('$')%2==0
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    return mask

def checks(r):
    independent(r)
    return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each checkbox correct and incorrect Boolean'} for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]

def main():
    records=[];replays=[]
    for t,q in g.SOURCES.items():
        raw=g.generate('moderate',template=t,parameters=g.ORIGINAL[t],profile='observed:'+t);independent(raw)
        assert raw['question'][':question/problem']==q[':question/problem']
        assert raw['question'][':question/worked-solution']==q[':question/worked-solution']
        for f,rf in zip(q[':question/answer-fields'],raw['question'][':question/answer-fields']):
            assert f[':answer-field/key']==rf[':answer-field/key']
            assert f[':answer-field/type'][':db/ident']==rf[':answer-field/type']
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
            assert f[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
        replays.append({'source':t,'complete_banks':'3/3','values':'6/6','correct_designations':'3/3','prompt_and_solution_exact':True,'difficulty_inference':':question/difficulty' not in q})
        for seed in range(40):
            r=g.generate_moderate(seed,template=t);independent(r);records.append(r)
    for trio,mask in itertools.product(range(10),range(8)):
        r=g.generate_easy(parameters={'trio':trio,'mask':mask});independent(r);records.append(r)
    hard_count=0
    for k,y,a,d in itertools.product([-11,-9,-7,-5,5,7,9,11],[-1,1],list(range(-15,-1))+list(range(2,16)),list(range(-15,-1))+list(range(2,16))):
        independent(g.generate_hard(parameters={'point':k,'ordinate':y,'asymptote':a,'domain':d}));hard_count+=1
    for seed in range(100):
        r=g.generate_hard(seed);independent(r);records.append(r)
    assert {g.generate_moderate(i)['generation']['template'] for i in range(100)}==set(g.SOURCES)
    for r in records:
        same=g.generate(r['question'][':question/difficulty'].split('/')[-1],999,template=r['generation']['template'],parameters=r['generation']['parameters'])
        assert r['question']==same['question']
    coverage={}
    for t,defaults in g.ORIGINAL.items():
        coverage[t]={}
        for key in defaults:
            seen=set()
            for seed in range(200):
                sample=g.sample(t,__import__('random').Random(seed));params=dict(defaults);params[key]=sample[key]
                if t=='q-103811' and params['left']==params['right']:continue
                independent(g.generate_moderate(template=t,parameters=params));seen.add(params[key])
            coverage[t][key]=sorted(seen)
    # Independently read changed numeric target with the other mathematical data fixed.
    fixed={'point':5,'ordinate':1,'asymptote':2,'domain':3}
    changed={**fixed,'point':7}
    first=g.generate_hard(parameters=fixed);second=g.generate_hard(parameters=changed)
    independent(first);independent(second)
    assert first['generation']['truth_mask']!=second['generation']['truth_mask']
    assert first['question'][':question/problem']!=second['question'][':question/problem']
    import copy
    broken=copy.deepcopy(second);broken['question'][':question/answer-fields'][0][':answer-field/correct']=broken['question'][':question/answer-fields'][0][':answer-field/choices'][1][':answer/id']
    try:independent(broken)
    except (AssertionError,StopIteration):pass
    else:raise AssertionError('stale field key was not caught')
    engine=[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records]
    (ROOT/'engine-input.json').write_text(json.dumps(engine));subprocess.run(['generate/runs/current/check-engine',str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
    report={'status':'pass','source_basis':g.SNAPSHOT['basis'],'source_replays':replays,'complete_banks':'21/21','source_values':'42/42','source_correct_designations':'21/21','independent_easy_tasks':80,'independent_hard_tasks':hard_count,'changed_source_variants':280,'normal_default_family_coverage':'7/7','moderate_slot_coverage':coverage,'changed_target_constant_data_check':True,'native':json.loads((ROOT/'engine-report.json').read_text()),'generator_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'limitations':['Finite catalogs; parameter aliases and option order are not new tasks.','Easy and hard are authored difficulty workloads, not observed source labels.','Two unrated templates are assigned moderate for new generated content only.','Malformed source TeX in q-103814 is repaired only in generated normal output.']}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    review=[g.generate(l,seed) for l in g.SUPPORTED_LEVELS for seed in (6,17)]
    (ROOT/'review.json').write_text(json.dumps(review,indent=2));(ROOT/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in review))
    print(json.dumps({k:v for k,v in report.items() if k!='native'},indent=2))
if __name__=='__main__':main()
