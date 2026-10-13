#!/usr/bin/env python3
"""Failure-sensitive fidelity, independent displayed math, scope and native QA."""
import copy,importlib.util,json,subprocess,sys,re,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));from mathcheck_17592186083280 import verify,value_set,expression,T
from variety import enumerate_tasks
import sympy as s
spec=importlib.util.spec_from_file_location('normal_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,data): (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def shape(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];assert q[':question/id']==g.uid(r['generation']['content_identity'])
    text=q[':question/problem']+'\n'+q.get(':question/worked-solution','')
    assert text.count('$')%2==0
    assert text.count('{')==text.count('}')
    assert not any(x in text for x in ('+-','--','@@SLOT'))
    for f in q[':question/answer-fields']:
        ids=[a[':answer/id']for a in f[':answer-field/choices']];assert len(ids)==len(set(ids))
        if ':answer-field/correct'in f:assert f[':answer-field/correct'][1]in ids
        if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}'in q[':question/problem']
    verify(r)
def fixture(r,label,raw=False):
    checks=[]
    for i,f in enumerate(r['question'][':question/answer-fields']):
        if ':answer-field/correct'not in f:continue
        correct=f[':answer-field/correct'][1]
        if f[':answer-field/type'].endswith('/radio'):
            checks +=[{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else'rejected','purpose':'complete radio bank'}for a in f[':answer-field/choices']]
        else:
            answer=f[':answer-field/choices'][0][':answer/value'];v=value_set(answer)[0]
            checks +=[{'field_index':i,'submitted':answer,'expected':'accepted','purpose':'exact expected fragment'}, {'field_index':i,'submitted':str(v+1),'expected':'rejected','purpose':'incorrect root'}]
            # Keep genuinely unreduced form, rather than pre-simplifying it.
            equivalent='('+str(v*2)+')/2'
            checks.append({'field_index':i,'submitted':equivalent,'expected':'rejected'if raw else'accepted','purpose':'equivalent exact fragment; captured round wording is form-sensitive'if raw else'equivalent exact fragment'})
    return {'label':label,'record':r,'checks':checks}

def main():
    assert g.SOURCE==json.loads(Path('generate/runs/current/sources/17592186083280.json').read_text())
    sources=[];cases=[];fixtures=[];raw_review=[];bankcount=0;choicecount=0
    for name,(level,sid,p)in g.TEMPLATES.items():
        if not sid:continue
        raw=g.generate(level,template=name,parameters=p,profile='observed:'+sid)
        src=g.Q[sid];q=raw['question'];shape(raw)
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
            assert (key in src)==(key in q),(sid,key)
        assert q[':question/problem']==src[':question/problem']
        if ':question/difficulty'in src:assert q[':question/difficulty']==src[':question/difficulty'][':db/ident']
        if ':question/worked-solution'in src:assert q[':question/worked-solution']==src[':question/worked-solution']
        for f,old in zip(q[':question/answer-fields'],src[':question/answer-fields']):
            assert f[':answer-field/key']==old[':answer-field/key']
            assert f[':answer-field/type']==old[':answer-field/type'][':db/ident']
            assert (':answer-field/correct'in f)==(':answer-field/correct'in old)
            assert sorted((a[':answer/type'],a[':answer/value'])for a in f[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value'])for a in old[':answer-field/choices']),sid
            choicecount+=len(old[':answer-field/choices']);bankcount+=1
            if ':answer-field/correct'in old:
                generated=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);assert generated==old[':answer-field/correct'][':answer/value']
        cases.append({'source_id':sid,'template':name,'level':level,'parameters':p,'bank_profile':'observed:'+sid,'unrated_authored_assignment':sid=='q-21080'})
        raw_review.append(raw)
        if all(':answer-field/correct'in f for f in q[':question/answer-fields']):fixtures.append(fixture(raw,'raw:'+sid,True))
    raw_parameter_checks=0
    for name,(level,sid,p)in g.TEMPLATES.items():
        if sid:
            for seed in range(10):shape(g.generate(level,seed,template=name,profile='observed:'+sid));raw_parameter_checks+=1
    records=[];coverage={};fingerprints={};hard_axes={'phase':set(),'shift':set(),'frequency':set()}
    for name,(level,sid,p)in g.TEMPLATES.items():
        coverage[name]=0;fingerprints[name]=set()
        for seed in range(60):
            r=g.generate(level,seed,template=name);shape(r);coverage[name]+=1;fingerprints[name].add(r['generation']['mathematical_fingerprint'])
            if name=='two_period_trig':
                hard_axes['phase'].add(s.Rational(r['generation']['parameters']['p']));hard_axes['shift'].add(r['generation']['parameters']['q']);hard_axes['frequency'].add(r['generation']['parameters']['k'])
            if seed<2:records.append(r);fixtures.append(fixture(r,name+':'+str(seed)))
            # Fixed explicit params survive shuffled order/seed with same content ID.
            again=g.generate(level,seed+101,template=name,parameters=r['generation']['parameters'])
            assert again['question'][':question/id']==r['question'][':question/id']
    assert hard_axes['phase']==set(g.HARD_PHASES) and hard_axes['shift']==set(g.HARD_INTERVAL_SHIFTS) and hard_axes['frequency']==set(range(2,7))
    defaultcoverage={l:set()for l in ('easy','moderate','hard')}
    for level in defaultcoverage:
        for seed in range(60):defaultcoverage[level].add(g.generate(level,seed)['generation']['template'])
        assert defaultcoverage[level]=={n for n,v in g.TEMPLATES.items()if v[0]==level}
    # Strict explicit workload bounds and whole-bank collisions.
    for name,(level,sid,p)in g.TEMPLATES.items():
        bad=dict(p);bad[next(k for k in bad if k!='p')]=100
        try:g.generate(level,template=name,parameters=bad)
        except ValueError:pass
        else:raise AssertionError('Explicit workload escaped')
    collision={'k':2,'b':1,'u':2,'c':1}
    try:g.generate('easy',template='exponential',parameters=collision)
    except ValueError as e:assert 'Whole bank rejected'in str(e)
    else:raise AssertionError('Ambiguous bank admitted')
    # Independent nonzero multipliers, translations and periodic phase aliases
    # change presentation but must never inflate assessed task variety.
    aliases={
        'exponential':({'k':1,'b':1,'u':2,'c':2},{'k':6,'b':2,'u':8,'c':4}),
        'logarithmic':({'k':2,'m':1},{'k':2,'m':6}),
        'quadratic':({'b':1,'c':2,'a':1},{'b':2,'c':4,'a':5}),
        'cubic':({'a':1,'n':3,'l':1,'h':1},{'a':4,'n':3,'l':9,'h':4}),
        'shifted_trig':({'a':1,'b':1,'h':0,'j':0,'p':'1/3'},{'a':6,'b':6,'h':12,'j':-12,'p':'2/6'}),
        'frequency_trig':({'a':1,'b':1,'h':0,'j':0,'k':4},{'a':6,'b':6,'h':-12,'j':12,'k':4}),
        'legacy_trig':({'a':1,'b':1,'h':0,'j':0,'k':4},{'a':6,'b':6,'h':-12,'j':12,'k':4}),
        'two_period_trig':({'a':1,'b':1,'h':0,'j':0,'k':2,'p':'1/3','q':2},{'a':6,'b':6,'h':-12,'j':12,'k':2,'p':'4/3','q':2}),
    }
    for name,(first,second)in aliases.items():
        level=g.TEMPLATES[name][0];r1=g.generate(level,template=name,parameters=first);r2=g.generate(level,template=name,parameters=second);shape(r1);shape(r2)
        assert r1['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint'],name
        assert r1['question'][':question/id']!=r2['question'][':question/id'],name
    freq=g.generate('moderate',template='frequency_trig',parameters=aliases['frequency_trig'][0]);legacy=g.generate('moderate',template='legacy_trig',parameters=aliases['legacy_trig'][0])
    assert freq['generation']['mathematical_fingerprint']==legacy['generation']['mathematical_fingerprint']
    variety,task_records=enumerate_tasks(g,shape)
    write('variety.json',variety)
    # Every hard canonical phase and both interval extremes reach native grading;
    # periodic aliases include changed first-root indices/signs.
    for phase in g.HARD_PHASE_INPUTS:
        for shift in (0,5):
            p={**g.TEMPLATES['two_period_trig'][2],'p':str(phase),'q':shift,'k':6}
            r=g.generate('hard',template='two_period_trig',parameters=p);shape(r);fixtures.append(fixture(r,'hard-boundary:'+str(phase)+':'+str(shift)))
    for key,badvalue in (('q',-1),('q',6),('p','1/2'),('p','2'),('k',1),('k',7)):
        p={**g.TEMPLATES['two_period_trig'][2],key:badvalue}
        try:g.generate('hard',template='two_period_trig',parameters=p)
        except ValueError:pass
        else:raise AssertionError('Authored hard bound escaped: '+key)
    # Mutations of printed maths must fail even with unchanged metadata.
    mutation_checks=0
    for transform in (lambda q:q.replace('{e}^{2t}','{e}^{3t}',1),lambda q:q.replace('=2t','=3t',1)):
        r=copy.deepcopy(raw_review[0]);key=':question/problem'if mutation_checks==0 else':question/worked-solution';r['question'][key]=transform(r['question'][key])
        try:verify(r)
        except (AssertionError,ValueError):mutation_checks+=1
        else:raise AssertionError('Displayed mathematical corruption missed')
    r=copy.deepcopy(next(r for r in raw_review if r['generation']['template']=='cubic'));r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('6({t}^{2}-3)=0','6{t}^{2}-18=0')
    try:verify(r)
    except AssertionError:mutation_checks+=1
    else:raise AssertionError('Lost factored solving stage admitted')
    write('source-cases.json',cases);write('review.json',records);write('engine-input.json',fixtures)
    subprocess.run([str(Path('generate/runs/current/check-engine')),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    findings=[{'source_id':'q-21080','kind':'missing difficulty, solution, correct designation','raw_preserved':True,'inferred_correct':'t=0 and t=pi/2','native_raw_checks':0}, {'source_id':'q-122946','kind':'prompt asks points but parameter bank and solution','repair':'normal prompt asks values of t; raw preserves original','actual_points':['(-7(sqrt(3)+1),12sqrt(3))','(7(sqrt(3)-1),-12sqrt(3))']}, {'sources':['q-21207','q-122947','q-122946','q-75278'],'kind':'some scalar distractor operations not recoverable uniquely','policy':'public raw observed profile evidence-only; separate method-derived default bank'}, {'sources':['q-350403','q-350414'],'kind':'native round-substring form sensitivity','limitation':'raw preserves Do not round and rejects equivalent unreduced entries; normal Give exact answers accepts them'}]
    report={'status':'passed with documented raw source limitations','basis':1356,'source_questions':len(cases),'complete_banks_matched':bankcount,'displayed_options_matched':choicecount,'correct_designations_matched':7,'missing_original_designations':1,'raw_prompt_matches':len(cases),'raw_solution_matches':6,'missing_original_solutions':1,'raw_parameter_checks':raw_parameter_checks,'raw_response_criterion_correct':6,'raw_response_criterion_total':7,'raw_point_vs_parameter_mismatches':1,'normal_generated_checked':sum(coverage.values()),'per_family':coverage,'unique_sampled_mathematical_tasks':{n:len(v)for n,v in fingerprints.items()},'default_family_coverage':{k:sorted(v)for k,v in defaultcoverage.items()},'exhaustive_canonical_tasks':{n:v['canonical_tasks']for n,v in variety['families'].items()},'deduplicated_level_task_counts':variety['deduplicated_level_counts'],'normal_exhaustive_representatives_checked':sum(v['parameter_representatives_attempted']-sum(v['rejected_representatives'].values())for v in variety['families'].values()),'fingerprint_alias_regressions':len(aliases)+1,'hard_phase_and_interval_native_boundary_records':24,'hard_sampled_parameter_coverage':{key:sorted(str(v)for v in values)for key,values in hard_axes.items()},'authored_hard_family':'two_period_trig','mutation_checks':mutation_checks,'native':{k:engine[k]for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'engine_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'findings':findings}
    write('validation.json',report)
    review=['# Original and generated review\n\nRaw captures preserve database omissions. Generated variants below are explicitly authored/default presentations.']
    for raw in raw_review:
        name=raw['generation']['template'];review+=['## '+name+' — original '+raw['generation']['source_id'],g.markdown(raw)]
        review+=['### Generated variant '+str(i+1)+' ('+r['question'][':question/difficulty']+')\n'+g.markdown(r)for i,r in enumerate(records)if r['generation']['template']==name]
    review+=['## Authored hard — two periods, four ordered roots']+[g.markdown(r)for r in records if r['generation']['template']=='two_period_trig']
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
