#!/usr/bin/env python3
"""Executable retained findings against the current generator's visible records.
Run with the job Python and -B. Writes only evidence; no runtime edits/services/DB.
"""
import hashlib
import itertools
import json
import math
import os
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import generator as G
import validate as T

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
REPO = Path('/home/jake/Developer/Course_Academy')
OUT = ROOT / 'evidence/repair-4'
OUT.mkdir(parents=True, exist_ok=True)
T.OUT = OUT
OMISSIONS = ((0,1),(1,0),(1,1),(2,0),(2,1))

def save(name, value):
    (OUT/name).write_text(json.dumps(value,indent=2)+'\n')

def field(r): return r['question'][':question/answer-fields'][0]

def visible(r):
    """Read expressions actually served; no bank_terms/answer_terms witnesses."""
    i=r['generation']['parameters']; x=T.V[i['variable']]
    rows=[]
    for a in field(r)[':answer-field/choices']:
        val=T.S.expand(T.tex(a[':answer/value'])-T.V['C'])
        linear=val.coeff(x,1)
        rest=T.S.simplify(val-linear*x)
        rows.append({'id':a[':answer/id'], 'linear':F(str(linear)),
                     'power':F(str(rest.subs(x,1))), 'length':len(a[':answer/value'])})
    return rows

def witnesses(r):
    T.verify(r)
    if field(r)[':answer-field/type'].endswith('/blank'):
        q=r['question']; assert 'zero constant term' not in q[':question/problem']
        assert 'zero constant term' not in q[':question/worked-solution']
        assert 'additive constant' in q[':question/worked-solution']
        a=T.tex(T.correct_value(r)); assert a.subs(T.V['t'],0)==0
        return
    rows=visible(r); key=field(r)[':answer-field/correct'][1]
    assert all(1<=abs(z['linear'])<=6 for z in rows)
    assert len({z['linear'] for z in rows})==3
    assert len({z['linear']>0 for z in rows})==1
    # Historical typography defect: changing only coefficient magnitude must
    # not leave a lone well-formed fraction after the constant is integrated.
    correct=next(z for z in rows if z['id']==key)
    matched=[z for z in rows if z['linear']==correct['linear']]
    assert len({z['length'] for z in matched})==1
    assert len({(abs(z['power']).numerator==1 if r['generation']['parameters']['profile']=='P' else abs(z['power']).numerator<10, abs(z['power'])<1,
                 z['power'].denominator==1) for z in matched})==1


def probes(records):
    groups=defaultdict(list)
    for r in records:
        i=r['generation']['parameters']
        if i['profile']=='B': continue
        rows=visible(r); key=field(r)[':answer-field/correct'][1]
        correct=next(z for z in rows if z['id']==key)
        count=Counter(z['linear'] for z in rows)
        power_count=Counter(z['power'] for z in rows)
        matched=[z for z in rows if z['linear']==correct['linear']]
        # Integrating the constant is legitimate. Other cues must not identify
        # the remaining coefficient systematically; handle singleton cases.
        candidates={
            'range_6':[z for z in rows if abs(z['linear'])<=6],
            'eliminate_singleton':[z for z in rows if count[z['linear']]>1],
            'choose_singleton':[z for z in rows if count[z['linear']]==1],
            'min_constant':[z for z in rows if abs(z['linear'])==min(abs(t['linear']) for t in rows)],
            'max_constant':[z for z in rows if abs(z['linear'])==max(abs(t['linear']) for t in rows)],
            'shortest':[z for z in rows if z['length']==min(t['length'] for t in rows)],
            'longest':[z for z in rows if z['length']==max(t['length'] for t in rows)],
            'constant_then_max_power':[z for z in matched if abs(z['power'])==max(abs(t['power']) for t in matched)],
            'constant_then_min_power':[z for z in matched if abs(z['power'])==min(abs(t['power']) for t in matched)],
            'constant_then_most_frequent':[z for z in matched if power_count[z['power']]==max(power_count[t['power']] for t in matched)],
            'constant_then_least_frequent':[z for z in matched if power_count[z['power']]==min(power_count[t['power']] for t in matched)],
        }
        for j in range(5): candidates['position_'+str(j)]=[rows[j]]
        trial={'id':r['question'][':question/id'],'singleton_key':count[correct['linear']]==1,
               'constant_candidates':len(matched), 'strategies':{
                 k:{'tie_expected':float(F(sum(z['id']==key for z in zs),len(zs))),
                    'success':zs[0]['id']==key, 'selected':zs[0]['id']}
                 for k,zs in candidates.items()}}
        assert len(candidates['range_6'])==5
        for group in (i['profile'],f"{i['profile']}:n={i['n']}",
                      f"{i['profile']}:n={i['n']}:s={i['s']}:order={i['constant_first']}"):
            groups[group].append(trial)
    summary={}
    for group,ts in groups.items():
        summary[group]={'attempts':len(ts),'singleton_keys':sum(t['singleton_key'] for t in ts),
                       'constant_only_baseline':sum(1/t['constant_candidates'] for t in ts)/len(ts),
                       'strategies':{k:{'wins':sum(t['strategies'][k]['success'] for t in ts),
                          'tie_averaged_rate':sum(t['strategies'][k]['tie_expected'] for t in ts)/len(ts)}
                          for k in ts[0]['strategies']}}
    return {'groups':summary,'trials':dict(groups)}


def coverage(records):
    result={}
    for p in ('P','R','B'):
        rs=[r for r in records if r['generation']['parameters']['profile']==p]
        ps=[r['generation']['parameters'] for r in rs]
        result[p]={'records':len(rs),'semantic_instances':len({T.semantic(r) for r in rs}),
                   **{k:sorted({i[k] for i in ps}) for k in ('n','s','k','variable','constant_first')}}
        if p!='B':
            result[p]['omissions']=sorted({(i['omitted_row'],i['omitted_col']) for i in ps})
            result[p]['key_positions']=dict(Counter(next(j for j,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==field(r)[':answer-field/correct'][1]) for r in rs))
    return result


def core():
    source=T.source_checks()
    assert json.loads((ROOT/'source-data.json').read_text())==json.loads(Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-priority-17592186050321/jobs/17592186184153/source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
    controls=[]; exact={}
    # Historical singleton, rank and typography repairs: complete decision-role
    # product, including the new valid singleton key. All coefficients read from
    # actual choice text. The finite exponent groups are separately checked.
    for profile,ns in [('P',range(2,7)),('R',(3,7))]:
        for n in ns:
            rs=[]
            above=next(f for f in G.factor_domain(profile,n) if f>1)
            below=next(f for f in G.factor_domain(profile,n) if f<1)
            for rank,side,(row,col) in itertools.product(range(3),(above,below),OMISSIONS):
                constants=(-1,-3,-6)
                k=constants[rank]; others=[c for c in constants if c!=k]
                i=G.instance(profile,n,1,k,'x',True,offset=others[0]-k,
                    second_offset=others[1]-k,factors=[side],omitted_row=row,omitted_col=col)
                r=G.build(i,random.Random(913)); witnesses(r);rs.append(r)
            probe=probes(rs)['groups'][profile]
            for name in ('range_6','eliminate_singleton','choose_singleton','min_constant','max_constant','shortest','longest'):
                assert abs(probe['strategies'][name]['tie_averaged_rate']-.2)<1e-12, (profile,n,name)
            for name in ('constant_then_max_power','constant_then_min_power','constant_then_most_frequent','constant_then_least_frequent'):
                assert abs(probe['strategies'][name]['tie_averaged_rate']-probe['constant_only_baseline'])<1e-12
            assert probe['singleton_keys']==6 and probe['attempts']==30
            exact[f'{profile}:{n}']=probe
            controls.extend(rs)
    # Entire new constant-triple domain, one omission each, alternating signs
    # and order. Constant rule is shared by P and R and independent of exponent.
    constant_controls=[]
    for j,triple in enumerate(itertools.combinations(range(1,7),3)):
        for rank in range(3):
            sign=(-1 if j%2 else 1); k=sign*triple[rank]
            others=[sign*c for c in triple if sign*c!=k]
            row,col=OMISSIONS[(j+rank)%5]
            r=G.build(G.instance('P',4,-1,k,'t',bool(j%2),offset=others[0]-k,
                second_offset=others[1]-k,omitted_row=row,omitted_col=col))
            witnesses(r)
            assert {abs(z['linear']) for z in visible(r)}==set(triple)
            constant_controls.append(r)
    # Exact latest counterexample must fail for an explicit mathematical reason;
    # retain its integrand with a fully supported alternative bank.
    try:
        G.build(dict(profile='R',n=3,s=-1,k=-5,variable='t',constant_first=False,
            offset=-3,second_offset=-2,factors=[2],omitted_row=0,omitted_col=1))
    except ValueError: pass
    else: raise AssertionError('Reported asymmetric -5/-8/-7 bank remains reachable')
    reproduced=G.build(G.instance('R',3,-1,-5,'t',False,offset=1,second_offset=2,
                  factors=[2],omitted_row=0,omitted_col=1))
    witnesses(reproduced)
    save('repaired-counterexample.json',reproduced)
    # Changed relevant evidence with all other data, including full answer bank,
    # held fixed. Relabel the three constants as correct in turn.
    counterfactuals=[]
    for profile,n in [('P',3),('R',3),('B',6)]:
        v='t' if profile=='B' else 'x'
        base=G.instance(profile,n,1,4,v,True,offset=-1,second_offset=None if profile=='B' else 1)
        a=G.build(base,random.Random(45)); witnesses(a)
        for name,delta,relevant in [('sign',{'s':-1},True),('exponent',{'n':n+1 if profile!='R' else 7,'factors':[F(5,3)] if profile=='R' else base['factors']},True),
                                   ('constant',{'k':-4,'offset':1,'second_offset':None if profile=='B' else -1},True),('order',{'constant_first':False},False)]:
            # A new polynomial exponent needs a compatible wrong divisor.
            if name=='exponent' and profile=='P':delta['factors']=[F(n+2,2)]
            if name=='exponent' and profile=='B': delta={'n':5}
            z=G.build(base|delta,random.Random(45));witnesses(z)
            eq=T.S.simplify(T.tex(T.correct_value(a))-T.tex(T.correct_value(z)))==0
            assert eq != relevant
            assert (a['question'][':question/problem']!=z['question'][':question/problem'])
            assert (a['question'][':question/worked-solution']!=z['question'][':question/worked-solution'])
            counterfactuals.append({'change':name,'relevant':relevant,'base':a,'changed':z})
    save('counterfactuals.json',counterfactuals)
    # Small original-seed regression, shared delivery checks below.
    sample=G.generate(count=128,seed=85290173)
    for r in sample: witnesses(r)
    # Target the historical biased quadratic sampler specifically. Profile and
    # exponent forced; all bank assignments remain current generator draws.
    Original=random.Random
    class QuadraticRandom(Original):
        def choice(self,seq):
            if tuple(seq)==('P','R','B'): return 'P'
            if tuple(seq)==(2,3,4,5,6): return 2
            return super().choice(seq)
    old_random=G.random
    try:
        G.random=SimpleNamespace(Random=QuadraticRandom)
        rank_sample=G.generate(count=64,seed=94172863)
    finally: G.random=old_random
    for r in rank_sample:witnesses(r)
    rank_probe=probes(rank_sample)['groups']['P']
    trials=[t for t in probes(rank_sample)['trials']['P'] if t['constant_candidates']==2]
    wins=sum(t['strategies']['constant_then_max_power']['success'] for t in trials)
    n=len(trials); p=min(1,2*sum(math.comb(n,j) for j in range(min(wins,n-wins)+1))/2**n)
    assert p>.001,(wins,n,p)
    save('quadratic-sampler.json',{'records':rank_sample,'wins':wins,'non_singleton_trials':n,'two_sided_binomial_p':p,'probe':rank_probe})
    # Blank regression includes the exact reported 5+t^6 shift and both signs.
    blanks=[G.build(G.instance('B',n,s,k,'t',order)) for n,s,k,order in
            [(6,1,5,True),(2,-1,-6,False),(5,1,-1,False),(3,-1,6,True)]]
    for r in blanks:witnesses(r)
    replay=[r for r in G.replay_sources() if not r.get('math_only')]
    all_checks=controls+constant_controls+[reproduced]+sample+rank_sample+blanks
    save('controls.json',controls+constant_controls+[reproduced]+blanks)
    save('sample.json',sample)
    save('rank-sample.json',rank_sample)
    native=[T.make_checks(r,'current '+str(j)) for j,r in enumerate(all_checks)]
    native.extend(T.make_checks(r,'source '+str(j)) for j,r in enumerate(replay)
                  if not field(r)[':answer-field/type'].endswith('/blank'))
    for r in blanks+[r for r in replay if field(r)[':answer-field/type'].endswith('/blank')]:
        value=T.tex(T.correct_value(r));x=T.V['t']
        assert T.S.diff(value+1,x)==T.S.diff(value,x)
        assert value.subs(x,0)==0 and (value+1).subs(x,0)!=0
        # The engine now grades the family modulo the externally displayed C.
        native.append({'label':'valid antiderivative family','record':r,'checks':[
            {'submitted':str(value).replace('**','^'),'expected':'accepted'},
            {'submitted':str(T.S.factor(value)).replace('**','^'),'expected':'accepted'},
            {'submitted':str(value+1).replace('**','^'),'expected':'accepted','purpose':'additive constant absorbed by C'},
            {'submitted':str(value-3).replace('**','^'),'expected':'accepted','purpose':'additive constant absorbed by C'},
            {'submitted':str(value+x).replace('**','^'),'expected':'rejected','purpose':'incorrect derivative'}]})
    for cf in counterfactuals:
        a,z=cf['base'],cf['changed'];f=field(z)
        native.append(T.make_checks(z,'counterfactual '+cf['change']))
        if f[':answer-field/type'].endswith('/blank'):
            native.append({'label':'prior response under '+cf['change'],'record':z,'checks':[
                {'submitted':T.correct_value(a),'expected':'rejected' if cf['relevant'] else 'accepted'}]})
        else:
            # Radios submit a current choice UUID, never arbitrary math text.
            matching=[choice for choice in f[':answer-field/choices'] if choice[':answer/value']==T.correct_value(a)]
            if matching:
                native.append({'label':'prior response under '+cf['change'],'record':z,'checks':[
                    {'submitted_answer_id':matching[0][':answer/id'],'expected':'rejected' if cf['relevant'] else 'accepted'}]})
    save('grader-input.json',native)
    save('shortcuts-raw.json',probes(sample))
    save('exact-role-probes.json',exact)
    save('coverage-raw.json',coverage(sample))
    save('regressions.json',{'passed':True,'source':source,'visible_role_controls':len(controls),
       'constant_domain_controls':len(constant_controls),'fresh':len(sample),'targeted_quadratic':len(rank_sample),
       'counterfactual_pairs':len(counterfactuals),'blank_boundary_records':len(blanks),
       'latest_counterexample':'original bank rejected; same integrand remains supported with -5/-4/-3 constants',
       'source_evidence_changed':False,'history_file':'not supplied; no finding IDs in feedback',
       'native_cases':len(native),'rank_probe':{'wins':wins,'trials':n,'binomial_p':p}})
    return sample


def run_tool(args, log):
    with (OUT/log).open('w') as f:
        p=subprocess.run(list(map(str,args)),cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
    assert p.returncode==0,f'{args[0]} failed: {OUT/log}'


def delivery_and_grading():
    for name in ('sample','controls','rank-sample'):
        run_tool([sys.executable,REPO/'generate/pipeline/check_delivery.py','--input',OUT/(name+'.json'),
          '--source','/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-priority-17592186050321/jobs/17592186184153/source/source.json','--inventory','/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-priority-17592186050321/jobs/17592186184153/source/inventory.json',
          '--difficulty','moderate','--output',OUT/(name+'-delivery'),
          '--asset-root',OUT,'--math-root','/media/jake/SSD/EDB/math'],name+'-delivery.log')
    run_tool([REPO/'generate/runs/current/check-engine',OUT/'grader-input.json',OUT/'grading.json'],'grading.log')
    delivered=json.loads((OUT/'sample-delivery/accepted.json').read_text())
    raw=json.loads((OUT/'sample.json').read_text())
    assert {T.semantic(r) for r in raw}=={T.semantic(r) for r in delivered}
    for name in ('sample','controls','rank-sample'):
        accepted=json.loads((OUT/(name+'-delivery')/'accepted.json').read_text())
        for r in accepted:witnesses(r)
        save('shortcuts-'+name+'-delivered.json',probes(accepted))
    # Every constant-rank/side/omission group must survive shared delivery.
    ctrl=json.loads((OUT/'controls-delivery/accepted.json').read_text())
    for profile,ns in [('P',range(2,7)),('R',(3,7))]:
        for n in ns:
            rs=[r for r in ctrl if r['generation']['parameters']['profile']==profile and r['generation']['parameters']['n']==n]
            assert len({(i['omitted_row'],i['omitted_col']) for i in [r['generation']['parameters'] for r in rs]})==5
    save('coverage-delivered.json',coverage(delivered))
    # Positive-moderate selector, identical to SHA256 within-band selection;
    # synthetic sorted UUID order only (DB ordering/live policy unavailable).
    pool=sorted(delivered,key=lambda r:r['question'][':question/id']); draws=[]
    for j in range(512):
        d=hashlib.sha256(f'course-academy/question-selection/v1/repair4-{j}'.encode()).digest()
        u=(int.from_bytes(d[8:16],'big')>>11)/(2**53)
        draws.append(pool[int(u*len(pool))])
    save('shortcuts-selection.json',probes(draws))
    save('coverage-selection.json',coverage(draws))
    save('selection.json',{'draws':len(draws),'pool':len(pool),'unique_selected':len({r['question'][':question/id'] for r in draws}),
        'controls_added_to_pool':False,'rule':'question_selection.rs select(): all generated candidates moderate with positive moderate weight',
        'limits':['Synthetic UUID sorting substitutes for unavailable database entity IDs.',
        'No live learner history/policy, database identity collisions or inventory changes are available.',
        'Zero moderate weight excludes this pool; an unconfigured policy selects smallest database ID.']})
    # Native cue-selected responses after normalization and selection, batched.
    lookup={r['question'][':question/id']:r for r in delivered}
    cue_cases=[]
    for name,records in [('delivered',delivered),('selected',list({r['question'][':question/id']:r for r in draws}.values()))]:
        p=probes(records)
        for profile in ('P','R'):
            for t in p['trials'].get(profile,[]):
                r=lookup[t['id']]; key=field(r)[':answer-field/correct'][1]
                cue_cases.append({'label':name+' cue responses','record':r,'checks':[
                    {'submitted_answer_id':v['selected'],'expected':'accepted' if v['selected']==key else 'rejected'}
                    for v in t['strategies'].values()]})
    save('delivered-grader-input.json',cue_cases)
    run_tool([REPO/'generate/runs/current/check-engine',OUT/'delivered-grader-input.json',OUT/'delivered-grading.json'],'delivered-grading.log')


def runtime():
    manifest=json.loads((ROOT/'package.json').read_text())
    assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{}}
    with tempfile.TemporaryDirectory(prefix='repair4-relocated-',dir=OUT) as d:
        for f in manifest['files']:shutil.copy(ROOT/f,d)
        p=subprocess.run([sys.executable,'-B','generator.py','--difficulty','moderate','--count','5',
            '--seed','3932190450','--format','json'],cwd=d,capture_output=True,text=True,check=True)
        expected=G.generate(count=5,seed=3932190450)
        assert json.loads(p.stdout)==expected==G.generate(count=5,seed=3932190450)
    save('runner-sample.json',expected)
    for band in ('easy','hard'):
        try:G.generate(band,1,0)
        except ValueError:pass
        else:raise AssertionError(band)
    save('runtime.json',{'deterministic':True,'relocation':True,'dependencies':manifest['dependencies'],
         'unsupported_bands':['easy','hard'],'runtime_files':manifest['files'],
         'sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in manifest['files']}})

if __name__=='__main__':
    core();delivery_and_grading();runtime()
    print(json.dumps({'passed':True,'regressions':'evidence/repair-4/regressions.json',
                     'grading':'evidence/repair-4/grading.json','delivery':'evidence/repair-4/sample-delivery/delivery.json'}))
