"""Independent read-only review. Run with context Python -B audit.py."""
import collections
import copy
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = Path('/home/jake/Developer/Course_Academy')
JOB = HERE.parent
PKG = JOB/'workspace'
PY = REPO/'.venv/bin/python'
sys.dont_write_bytecode = True
sys.path.insert(0, str(PKG))
import generator as gen

def save(name, obj):
    (HERE/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')

def field(r): return r['question'][':question/answer-fields'][0]
def choices(r): return field(r)[':answer-field/choices']
def correct(r):
    key = field(r)[':answer-field/correct'][1]
    return next(c[':answer/value'] for c in choices(r) if c[':answer/id']==key)

def affine(s):
    if 'k' not in s: return 0,int(s)
    m=re.fullmatch(r'(-?\d*)k([+-]\d+)?',s)
    assert m, s
    t=m[1]
    return (1 if t=='' else -1 if t=='-' else int(t)),int(m[2] or 0)

def prompt_data(r):
    """Read visible prompt only. Never consult generation parameters or keys."""
    text=r['question'][':question/problem']
    givens=re.findall(r'\\log_\{(\d+)\}\\left\(([xy])\\right\)=(-?\d+|k)',text)
    assert len(givens)==2, text
    target=re.search(r'then \$\\log_\{(\d+)\}\\left\(x(?:\^\{(\d+)\})?y(?:\^\{(\d+)\})?\\right\)=\$',text)
    assert target,text
    assert {int(g[0]) for g in givens}=={int(target[1])}
    a,b=int(target[2] or 1),int(target[3] or 1)
    values={z:val for _,z,val in givens}
    t=c=0
    for z,p in [('x',a),('y',b)]:
        if values[z]=='k': t+=p
        else:c+=p*int(values[z])
    return dict(base=int(target[1]),a=a,b=b,givens=values,expected=(t,c),family='symbolic' if t else 'numeric',reverse=givens[0][1]=='y')

def audit_record(r):
    p=prompt_data(r);expected=p['expected']
    vals=[affine(c[':answer/value']) for c in choices(r)]
    assert len(vals)==len(set(vals))==5
    assert vals.count(expected)==1
    assert affine(correct(r))==expected
    sol=r['question'][':question/worked-solution']
    # Independently derive the exact expansion and substitution text expected in solution.
    log=lambda z: rf'\log_{{{p["base"]}}}\left({z}\right)'
    expanded=''.join((('' if e==1 else str(e))+log(z)+('+' if z=='x' else '')) for z,e in [('x',p['a']),('y',p['b'])])
    assert expanded in sol
    if not expected[0]:
        dot=lambda e,n:rf'{e}\cdot '+(f'({n})' if n<0 else str(n))
        subst=dot(p['a'],int(p['givens']['x']))+'+'+dot(p['b'],int(p['givens']['y']))
    else:
        symbol=next(z for z,v in p['givens'].items() if v=='k')
        other='y' if symbol=='x' else 'x'
        n=int(p['givens'][other]); w=p['b'] if other=='y' else p['a']
        sym=('' if expected[0]==1 else str(expected[0]))+'k'
        num=(rf'{w}\cdot ' if w!=1 else '')+(f'({n})' if n<0 else str(n))
        subst=sym+'+'+num if symbol=='x' else num+'+'+sym
    assert expanded+'='+subst+'='+correct(r)+'.' in sol
    assert sol.endswith('='+correct(r)+'.\n$$')
    assert p['base'] in (2,3,5,7,10)
    assert r['question'][':question/difficulty']==':question.difficulty/hard'
    return p

def canon(s):
    s=s.replace('⁡','').replace('\\left','').replace('\\right','')
    s=s.replace('${log}', '$\\log').replace('{log}', '\\log')
    s=re.sub(r'\s+','',s)
    return s.replace('{','').replace('}','')

def run(cmd, label):
    r=subprocess.run([str(s) for s in cmd],capture_output=True,text=True,cwd=HERE,env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1'})
    save(label,{'command':[str(s) for s in cmd],'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    assert r.returncode==0,(label,r.stderr[-2000:])
    return r

seeds=[2026101917,618037,930127,440231]
samples=[];stats={}
for seed in seeds:
    rng=random.Random(seed)
    for i in range(40):
        r=gen.generate(rng,stats=stats)
        r['generation'].update(review_seed=seed,review_index=i)
        samples.append(r)
save('samples.json',samples)
batch=json.loads((JOB/'samples.json').read_text());save('runner-batch.json',batch)

# Exercise every sign and factor-role subgroup with five different keys and an identical visible bank.
controlled=[];groups=[]
for su,sv in itertools.product((-1,1),repeat=2):
    roles=[dict(a=2,b=3,u=su*i,v=sv*2,base=5,reverse=False) for i in range(1,6)]
    groups.append(('numeric '+str((su,sv)), 'numeric',roles))
for symbol,powered,sign in itertools.product('xy','xy',(-1,1)):
    roles=[dict(a=(i if powered=='x' else 1),b=(i if powered=='y' else 1),symbol=symbol,n=sign*2,base=3,reverse=False) for i in range(2,6)]
    # Fifth role changes the numeric given, preserving subgroup while keeping distinct answers.
    roles.append(dict(roles[0],n=sign*6))
    groups.append((f'symbolic symbol={symbol} powered={powered} sign={sign}','symbolic',roles))
group_reports=[]
for name,fam,roles in groups:
    start=len(controlled)
    records=[gen.build_role_bank(fam,roles,key) for key in range(5)]
    for r in records:audit_record(r)
    assert len({tuple(c[':answer/value'] for c in choices(r)) for r in records})==1
    assert len({correct(r) for r in records})==5
    controlled.extend(records)
    group_reports.append({'group':name,'indices':list(range(start,start+5)),'parameters':roles,'correct_values':[correct(r) for r in records], 'fixed_bank_position_correct':1,'total':5})
save('controlled-bank-records.json',controlled);save('controlled-bank-tests.json',{'command':f'{PY} -B {HERE}/audit.py','groups':group_reports})

# Minimal relevant and irrelevant changes, with complete records and expected relationships.
pairs=[];pair_records=[]
def pair(label,kind,before,after,relationship):
    a,b=audit_record(before),audit_record(after)
    if relationship=='same':assert a['expected']==b['expected']
    else:assert a['expected']!=b['expected']
    start=len(pair_records);pair_records.extend([before,after])
    pairs.append({'label':label,'kind':kind,'relationship':relationship,'indices':[start,start+1], 'before':a,'after':b,'before_correct':correct(before),'after_correct':correct(after),'passed':True})
roles=groups[0][2]
pair('numeric: change only u from -1 to -2, identical bank','relevant',gen.build_role_bank('numeric',roles,0),gen.build_role_bank('numeric',roles,1),'different')
for symbol in 'xy':
    name,fam,roles=next(g for g in groups if g[0]==f'symbolic symbol={symbol} powered={symbol} sign=-1')
    pair(f'symbolic {symbol}: change only exponent 2 to 3, identical bank','relevant',gen.build_role_bank(fam,roles,0),gen.build_role_bank(fam,roles,1),'different')
roles=[dict(a=2,b=3,u=2,v=i,base=5,reverse=False) for i in range(1,6)]
pair('numeric: change only y exponent; both answers available','relevant',gen.build_role_bank('numeric',roles,0),gen.build_role_bank('numeric',[dict(r,b=4) for r in roles],0),'different')
for family,roles in [('numeric',groups[1][2]),('symbolic',groups[7][2])]:
    r=gen.build_role_bank(family,roles,0)
    for label,roles2 in [('base',[dict(p,base=7) for p in roles]),('given order',[dict(p,reverse=True) for p in roles])]:
        pair(f'{family}: change only {label}','irrelevant',r,gen.build_role_bank(family,roles2,0),'same')
    pair(f'{family}: reverse choice order','irrelevant',r,gen.build_role_bank(family,roles,0,[4,3,2,1,0]),'same')
# Swap which given is symbolic while preserving the exponent assignments.
ra=[dict(a=1,b=3,symbol='x',n=i,base=2) for i in range(1,6)]
rb=[dict(a=1,b=3,symbol='y',n=i,base=2) for i in range(1,6)]
pair('move symbolic given x to y with fixed exponents and n','relevant',gen.build_role_bank('symbolic',ra,1),gen.build_role_bank('symbolic',rb,1),'different')
save('counterfactual-records.json',pair_records);save('counterfactual-tests.json',{'pairs':pairs})

# Replay the captured four complete banks at original parameters, without trusting author tests.
source=json.loads((JOB/'source/source.json').read_text())['material']['kp']
specs=[('expand',dict(c=5,z='p',p=3)),('condense',dict(a=3,b=2,base=2)),('numeric',dict(a=2,b=3,u=3,v=2,base=5)),('symbolic',dict(a=1,b=3,symbol='x',n=4,base=2))]
replays=[];replay_report=[]
for src,(family,p) in zip(source[':knowledge-point/questions'],specs):
    r=gen.build(family,p);replays.append(r)
    sf=src[':question/answer-fields'][0]
    assert canon(src[':question/problem'])==canon(r['question'][':question/problem'])
    expected_bank=[canon(c[':answer/value']) for c in sf[':answer-field/choices']]
    assert expected_bank==[canon(c[':answer/value']) for c in choices(r)]
    if ':answer-field/correct' in sf:
        assert canon(sf[':answer-field/correct'][':answer/value'])==canon(correct(r));audit_record(r)
    else:
        assert canon(correct(r))==canon('\\log (5) + 3\\log (p)' if family=='expand' else '\\log_{2} (x^{3}y^{2})')
    replay_report.append({'source_id':src[':question/id'],'ma_id':src[':question/math-academy-id'],'family':family,'prompt_match':True,'bank_match':5,'recorded_key':':answer-field/correct' in sf,'correct':correct(r),'solution_assessment':'Hard solutions retain same three-law list, expansion, substitution and conclusion; expansion/condensation solutions independently derived because source omitted them.'})
save('source-replay-records.json',replays)
save('source-replay-tests.json',{'cases':replay_report,'canonical_example':'e-4082 is a lesson demonstration with no captured answer bank/field; constant-plus-variable condensation is not sampled or separately replayable via this generator. Its power/product reasoning is represented, but do not claim an exact e-4082 record replay.','unsupported':'Unrated expand/condense are source-only; easy/moderate unsupported.'})

allhard=samples+batch+controlled+pair_records+replays[2:]
details=[audit_record(r) for r in allhard]
coverage=collections.Counter()
for r,p in zip(samples,details):
    coverage[p['family']]+=1;coverage[f'base={p["base"]}']+=1;coverage[f'reverse={p["reverse"]}']+=1
    if p['family']=='numeric':
        coverage[f'numeric signs={(int(p["givens"]["x"])>0,int(p["givens"]["y"])>0)}']+=1
        for z in 'xy':coverage[f'given={p["givens"][z]}']+=1
        coverage[f'exponents={p["a"],p["b"]}']+=1
    else:
        symbol=next(z for z,v in p['givens'].items() if v=='k');powered='x' if p['a']>1 else 'y'
        n=int(next(v for v in p['givens'].values() if v!='k'))
        coverage[f'symbolic symbol={symbol} powered={powered} sign={n>0}']+=1
        coverage[f'given={n}']+=1
save('math-tests.json',{'command':f'{PY} -B {HERE}/audit.py','passed':True,'hard_records':len(allhard),'method':'Parse visible givens and target independently; exact integer affine pairs for all five options, unique equivalence, independent expansion and substitution checks on worked solution. No generator true_pair/answer_pairs used for expectations.','coverage':dict(coverage),'stats':stats})

# Real native grader: all five visible choices, expected outcomes from parsed mathematics.
grader=[]
for i,r in enumerate(allhard+replays[:2]):
    expected=prompt_data(r)['expected'] if i<len(allhard) else None
    checks=[]
    for c in choices(r):
        yes=affine(c[':answer/value'])==expected if expected is not None else c[':answer/value']==correct(r)
        checks.append({'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if yes else 'rejected','purpose':'Visible mathematical equivalence, independently calculated; all four distractors tested.'})
    grader.append({'label':f'independent-{i}', 'record':r,'checks':checks})
save('grader-input.json',grader)

# Boundary and package relocation checks use only a copy under evidence_root.
runtime={'python':sys.version.split()[0],'third_party_runtime_imports':[],'dependencies':json.loads((PKG/'package.json').read_text())['dependencies']}
assert runtime['python']==runtime['dependencies']['python']
assert runtime['dependencies']['packages']=={}
reloc=HERE/'relocated';reloc.mkdir(exist_ok=True)
for f in ('generator.py','math_format.py','package.json'):shutil.copyfile(PKG/f,reloc/f)
checks=[]
for count in (0,1,1000):
    cmd=[PY,'-B',PKG/'generator.py','--seed','823771','--count',str(count),'--difficulty','hard']
    r=run(cmd,f'cli-{count}.json');out=json.loads(r.stdout);assert len(out)==count
    if count==1000:
        for record in out:audit_record(record)
    checks.append({'count':count,'records':len(out),'passed':True})
orig=run([PY,'-B',PKG/'generator.py','--seed','771923','--count','7'],'determinism-original.json')
repeat=run([PY,'-B',PKG/'generator.py','--seed','771923','--count','7'],'determinism-repeat.json')
rel=run([PY,'-B',reloc/'generator.py','--seed','771923','--count','7'],'determinism-relocated.json')
assert orig.stdout==repeat.stdout==rel.stdout
for flag,value in [('--difficulty','easy'),('--difficulty','moderate'),('--count','-1'),('--count','1001')]:
    cmd=[str(PY),'-B',str(PKG/'generator.py'),flag,value];r=subprocess.run(cmd,capture_output=True,text=True,env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1'})
    assert r.returncode!=0 and not r.stdout
    checks.append({'command':cmd,'returncode':r.returncode,'stderr':r.stderr,'passed':True})
save('packaging-tests.json',{'runtime':runtime,'boundary_checks':checks,'determinism_and_relocation':True,'assets':'No generated assets, external paths, runtime dependencies or external outputs; imports are stdlib plus declared local math_format.py.','resampling':'draw_role_bank rejects repeated exact affine pairs, up to 1000 attempts; selected key drawn only after five distinct candidates. 1000 independently parsed boundary records plus seeded samples produced five distinct valid alternatives each.'})
save('scope-tests.json',{'passed':True,'basis':['q-79453','q-98925','tutorial 2796'],'observations':'All sampled hard records use two factors, integer positive exponents 1..5, one product/power expansion, supplied numeric or symbolic logarithms, short signed arithmetic, five radio choices. Negative given logarithms are valid because x=b^u>0, y=b^v>0. They add signed arithmetic but no new logarithm operation or solution stage. The alternative banks contain answers of the same numeric/affine type.','restrictions':'x/y/k labels fixed and base>1 conservative finite base set: renaming labels is incidental, not a missing decision case. Numeric keeps two nonunit unequal exponents; symbolic keeps one unit exponent and one symbolic given, matching two observed hard workload profiles. Both symbolic and powered-factor assignments vary independently.'})
save('commands.json',{'main':[str(PY),'-B',str(HERE/'audit.py')],'seeds':seeds,'count_per_seed':40,'role_groups':'Explicit parameters in controlled-bank-tests.json','counterfactuals':'counterfactual-records.json and counterfactual-tests.json','writes':'All scripts, sample files, temporary relocated package and results stay inside evidence_root; original package only read.'})
(HERE/'session-state.md').write_text('Milestone 2: independent four-bank replay, 160 fresh samples, 60 controlled role-bank records, 22 counterfactual records, 1000-count boundary math, relocation and deterministic replay passed. Native grader input prepared; delivery, native grader, actual UI and learner-selection checks remain. Package untouched.\n')
print(json.dumps({'samples':len(samples),'controlled':len(controlled),'counterfactual_records':len(pair_records),'hard_checked':len(allhard),'source_replays':len(replays),'grader_checks':len(grader)*5,'coverage':dict(coverage)},indent=2))
