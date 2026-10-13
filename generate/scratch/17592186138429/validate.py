#!/usr/bin/env python3
"""Independent actual-output math, full bank replay, format, native grading QA."""
import concurrent.futures, hashlib, importlib.util, json, random, re, subprocess, tempfile
from pathlib import Path
import sys
sys.dont_write_bytecode=True
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('kp',HERE.with_suffix('.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def write(name,data): (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
def check(r):
    q=r['question'];g=r['generation'];name=g['template'];f=q[':question/answer-fields'][0]
    assert set(r['knowledge_point'])=={'db_id','id','title'} and r['knowledge_point']['db_id']==m.KP_ID
    assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    assert len(f[':answer-field/choices'])==5 and len({a[':answer/id'] for a in f[':answer-field/choices']})==5
    prompt=q[':question/problem'];worked=q[':question/worked-solution']; path=HERE/re.search(r'!\[\]\((.*?)\)',prompt)[1]
    assert path.exists() and path.read_bytes().startswith(b'\x89PNG')
    # Derive from the mathematical data of the graph actually linked in prompt,
    # rather than trusting generation.parameters or stored correct values.
    if path.with_suffix('.json').exists():
        plot=json.loads(path.with_suffix('.json').read_text());p=plot['parameters'];assert plot['template']==name
        for key in ('a','b'):
            endpoints=plot['plotted_line_endpoints'][key]
            for xx,yy in endpoints:assert sp.Rational(yy)==sp.Rational(p[key+'0'])+sp.Rational(p[key+'1'])*sp.Rational(xx)
        assert plot['numbered_x_ticks']==[v for v in plot['grid_x_ticks'] if v and v%p['xlabel_step']==0]
    else:
        extracted={'cars':(80,'-3/4',40,'-1/4'),'trucks':(0,50,750,-75),'pools':(150,50,775,-75)}
        p=dict(zip(('a0','a1','b0','b1'),extracted[name]));p.update(g['parameters'])
        # Captured PNG fidelity is hashed against the inspected original below.
        assert tuple(str(p[k]) for k in ('a0','a1','b0','b1'))==tuple(map(str,extracted[name]))
    x=sp.Symbol('x'); A=sp.Rational(p['a0'])+sp.Rational(p['a1'])*x;B=sp.Rational(p['b0'])+sp.Rational(p['b1'])*x
    t=sp.solve(A-B,x)[0];y=A.subs(x,t);assert y==B.subs(x,t)
    assert t.is_integer and y.is_integer and t>0 and y>0
    allvals=[];corrects=[]
    for a in f[':answer-field/choices']:
        text=a[':answer/value'];assert not '$' in text
        assert re.fullmatch(r'\d+h' if name=='trucks' else r'\d+',text)
        v=sp.Integer(text[:-1] if name=='trucks' else text);allvals.append(v)
        assert 0<v<=sp.Rational(g['parameters']['xmax'])
        if v==t: corrects.append(a[':answer/id'])
    assert len(set(allvals))==5 and corrects==[f[':answer-field/correct'][1]]
    solpath=HERE/re.findall(r'!\[\]\((.*?)\)',worked)[0]
    solplot=json.loads(solpath.with_suffix('.json').read_text());assert list(map(sp.Rational,solplot['annotation_point']))==[t,y]
    point=re.search(r'point \$\((\d+),(\d+)\)\$',worked);assert point and (int(point[1]),int(point[2]))==(t,y)
    assert len(re.findall(r'!\[\]',worked))==1 and worked.index('graphs intersect.')<worked.index('![]')<worked.index('In this case')<worked.index('So, both')
    assert worked==m.solution(name,g['parameters'],g['plot_assets'])
    unit={'cars':'km/h','trucks':'miles','pools':'L'}[name];assert f'${y}\\,\\textrm{{{unit}}}$' in worked
    if name=='cars':assert f'${t}$ meters' in worked
    else:assert f'$t={t}$ '+('hours' if name=='trucks' else 'days') in worked
    for text in (prompt,worked):
        assert text.count('$')%2==0 and '\\begin' not in text
        assert text.count('{')==text.count('}') and '--' not in text and '+-' not in text
    assert q[':question/id']==m.generate(TEMPLATES[name],seed=999,template=name,parameters=g['parameters'],profile=g['bank_profile'])['question'][':question/id']
    return int(t),int(y)

TEMPLATES=m.TEMPLATES
source=json.loads((HERE/'source.json').read_text());cases=json.loads((HERE/'source-cases.json').read_text());originals=source['record'][':knowledge-point/questions'];records=[];fidelity=[]
for c,s in zip(cases,originals):
    r=m.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);records.append(r);check(r)
    f=r['question'][':question/answer-fields'][0];sf=s[':question/answer-fields'][0]
    raw=[a[':answer/value'] for a in sf[':answer-field/choices']];got=[a[':answer/value'] for a in f[':answer-field/choices']]
    assert sorted(raw)==sorted(got) and r['question'][':question/problem']==s[':question/problem']
    assert ':answer-field/correct' not in sf and ':question/worked-solution' not in s and ':question/difficulty' not in s
    original=Path('/home/jake/Developer/MA/DATA/Lessons/2225/Source/Images')/(c['source_id']+'.png');copied=HERE/m.ORIGINAL_ASSETS[c['template']];assert original.read_bytes()==copied.read_bytes()
    fidelity.append({'source_id':c['source_id'],'prompt_exact':True,'all_choices_matched':5,'distractors_matched':4,'correct_designation':'missing original; independently inferred','solution':'missing original; authored canonical-method adaptation','plot':'captured PNG exact'})
# Canonical prose/sequence and values are independently checked, not practice count.
canonical=m.generate('moderate',template='pools',parameters=m.SOURCE_PARAMETERS['pools']);check(canonical)
raw=source['record'][':knowledge-point/canonical-example'][':question/worked-solution']
norm=lambda s:re.sub(r'!\[\]\(.*?\)','<PLOT>',s)
assert norm(canonical['question'][':question/worked-solution'])==norm(raw)
review=records.copy();generated=[]
for level in ('easy','moderate','hard'):
    for seed in (21,22,23,24):
        r=m.generate(level,seed);check(r);generated.append(r)
        if seed in (21,22):review.append(r)
# Content identity separates banks but mathematical fingerprints do not.
cars=m.generate('hard',template='cars',parameters=m.SOURCE_PARAMETERS['cars'])
assert cars['question'][':question/id']!=records[0]['question'][':question/id']
assert cars['generation']['parameter_fingerprint']==records[0]['generation']['parameter_fingerprint']
# Equivalent rational spellings keep both identities.
p=m.SOURCE_PARAMETERS['cars'].copy();p['a1']='-6/8';p['b1']='-2/8'
equiv=m.generate('hard',template='cars',parameters=p,profile='observed_car_ratios')
assert equiv['question'][':question/id']==records[0]['question'][':question/id']
assert equiv['generation']['parameter_fingerprint']==records[0]['generation']['parameter_fingerprint']
# Source-expression profiles change graph data normally; bank formulas are explicit.
for c in cases:
    p=c['parameters'].copy();p['a0']+=20 if c['template']=='cars' else 0;p['b0']+=20 if c['template']=='cars' else 0
    if c['template']=='cars':p['ymax']+=20
    else:p['a1']=100;p['b0']=1050;p['b1']=-75;p['ymax']=1300
    r=m.generate(c['level'],template=c['template'],parameters=p,profile=c['bank_profile']);check(r);generated.append(r)
variety={}
for name,level in m.TEMPLATES.items():
    ps=[m.sample(name,random.Random(i)) for i in range(200)];assert len({m.digest([p['a0'],p['a1'],p['b0'],p['b1']]) for p in ps})>=20
    for p in ps:m.guard(name,p,'adjacent_grid')
    variety[level]={'sampled_seeds':200,'unique_line_tasks':len({m.digest([p['a0'],p['a1'],p['b0'],p['b1']]) for p in ps})}
# Explicit bad bounds/branches/bank collisions and simplified workload must fail.
invalid=0
for level in m.TEMPLATES.values():
    r=next(v for v in generated if v['question'][':question/difficulty'].endswith('/'+level));name=r['generation']['template'];p=r['generation']['parameters']
    for key,bad in (('a1',0),('dx',0),('xlabel_step',3),('xmax',1),('b0',-1),('a0',-1)):
        pp=p.copy();pp[key]=bad
        try:m.generate(level,template=name,parameters=pp)
        except ValueError:invalid+=1
        else:raise AssertionError('Invalid explicit input accepted')
# Blank entries are inapplicable: all observed and authored fields are radio.
engine=[]
for i,r in enumerate(records+generated+[canonical]):
    f=r['question'][':question/answer-fields'][0];engine.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned displayed choice; independent numerical/plot check above'} for a in f[':answer-field/choices']]})
write('engine-input.json',engine);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
# Fresh concurrent renders: same and different graphs use separate task inputs.
renderinputs=[];targets=[]
for i,r in enumerate([generated[0],generated[0],generated[4],generated[8]]):
    data={**r['generation']['plot_assets']['solution']['geometry'],'annotated':True};target=HERE/'qa-fresh'/('concurrent-'+str(i)+'.png');target.parent.mkdir(exist_ok=True)
    inp=HERE/('qa-render-input-'+str(i)+'.json');inp.write_text(json.dumps({'spec':data,'output':str(target)}));renderinputs.append(inp);targets.append((target,data))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(lambda p:subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE/'render.py'),str(p)],check=True,capture_output=True,text=True),renderinputs))
for inp in renderinputs:inp.unlink()
for target,data in targets:
    side=json.loads(target.with_suffix('.json').read_text());assert all(side[k]==v for k,v in data.items());assert target.stat().st_size>10000
assert targets[0][0].read_bytes()==targets[1][0].read_bytes()
assert not list(HERE.glob('qa-render-input-*.json'))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    concurrent_records=list(pool.map(lambda pair:m.generate(*pair),[('easy',101),('easy',101),('moderate',102),('hard',103)]))
for r in concurrent_records:check(r)
assert concurrent_records[0]['question'][':question/id']==concurrent_records[1]['question'][':question/id']
assert concurrent_records[0]['generation']['plot_assets']==concurrent_records[1]['generation']['plot_assets']
write('review.json',review+generated[-2:])
chunks=['# Review\n\nOriginal practice records have missing levels, correct designations and solutions. Source replays below retain exact prompts/banks/plots; solutions and refs are explicitly authored repairs. Generated examples use authored level bands and adjacent_grid bank.']
for i,r in enumerate(review):
    label=('Original '+cases[i]['source_id']+' replay — correct ref/solution/level authored' if i<2 else 'Generated authored '+r['question'][':question/difficulty'].split('/')[-1]+' variant')
    chunks.append('## '+label+'\n\n'+m.markdown(r))
# Every observed bank gets a changed-geometry variant too.
for r in generated[-2:]:chunks.append('## Generated variant of observed-expression replay profile; intent unknown\n\n'+m.markdown(r))
(HERE/'review.md').write_text('\n\n---\n\n'.join(chunks)+'\n')
engine_report=json.loads((HERE/'engine-report.json').read_text())
if (HERE/'visual-review.json').exists():
    visual=json.loads((HERE/'visual-review.json').read_text())
    assert visual['status']=='passed' and visual['renderer_sha256']==hashlib.sha256((HERE/'render.py').read_bytes()).hexdigest()
    for item in visual['inspected_final_assets']:assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256']
report={'status':'passed','source_provenance':m.SOURCE,'source_questions':2,'unrated_sources':2,'missing_correct_refs':2,'missing_practice_solutions':2,'source_fidelity':fidelity,'complete_banks_matched':2,'choices_matched':10,'distractors_matched':8,'original_correct_designations_matched':{'matched':0,'total_available':0,'inferred':2},'practice_solution_fidelity':{'matched':0,'total_available':0,'authored':2},'canonical_solution_sequence_and_normalized_prose':'passed','source_format_repairs':['independently derived correct refs','authored practice solutions','authored level assignments'],'mathematical_actual_outputs_checked':len(records)+len(generated)+1,'sampling_variety':variety,'invalid_explicit_inputs_rejected':invalid,'native_grader':engine_report,'blank_equivalent_entries':'not applicable; radio only','concurrency':'4 fresh renderer calls plus 4 concurrent API calls; identical and different geometry sidecars checked; same pixels and identities for same geometry','visual_review':json.loads((HERE/'visual-review.json').read_text()) if (HERE/'visual-review.json').exists() else 'pending final inspection','scope':'graph intersection horizontal-coordinate contextual reading only','freeze':{'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256((HERE/'render.py').read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()},'unresolved_findings':['Original distractor intent unknown; explicit observed expression profiles, excluded from defaults','No original difficulty/designations/practice solutions exist; cannot claim matches']}
write('validation.json',report)
print(json.dumps({k:report[k] for k in ('status','complete_banks_matched','choices_matched','distractors_matched','sampling_variety')},indent=2))
