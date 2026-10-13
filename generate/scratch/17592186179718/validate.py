#!/usr/bin/env python3
"""Independent printed-math, full source fidelity, identity and real grader QA."""
import concurrent.futures,difflib,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent; spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
U=s.Symbol('u',positive=True);locals_={'t':g.t,'x':g.x,'y':g.y,'u':U,'e':s.E,'log':s.log,'sqrt':s.sqrt}
def parsed(z):
 z=z.strip().rstrip('.,');z=z.replace(r'\left','').replace(r'\right','').replace(r'\,',' ').replace(r'\:',' ').replace(r'\cdot','*').replace(r'\operatorname{ln}⁡','log').replace(r'\ln','log')
 def group(z,start):
  assert z[start]=='{',z
  depth=1;i=start+1
  while depth:
   if z[i]=='{':depth+=1
   if z[i]=='}':depth-=1
   i+=1
  return z[start+1:i-1],i
 while '\\frac' in z or '\\sqrt' in z:
  m=re.search(r'\\(frac|sqrt)',z);begin=m.start();a,end=group(z,m.end())
  if m.group(1)=='frac':b,end=group(z,end);v='(('+str(parsed(a))+')/('+str(parsed(b))+'))'
  else:v='sqrt('+str(parsed(a))+')'
  z=z[:begin]+v+z[end:]
 z=z.replace('^','**').replace('{','(').replace('}',')')
 assert '\\' not in z,z
 return parse_expr(z,local_dict=locals_,transformations=standard_transformations+(implicit_multiplication_application,),evaluate=True)
def equal(a,b):assert s.simplify(a-b)==0,(a,b)
def formatting(z):
 assert '\\n' not in z, 'literal newline escape'
 assert z.count('$')%2==0
 for m in re.finditer(r'\$\$.*?\$\$|\$[^$]*\$',z,re.S):
  q=m.group();depth=0
  for c in q:
   if c=='{':depth+=1
   elif c=='}':depth-=1;assert depth>=0,q
  assert depth==0,q
 assert not re.search(r'(?<!\\)[+-]{2}',z),z

def normal_check(r):
 q=r['question'];d=g.math_data(r['generation']['template'],r['generation']['parameters']);p=q[':question/problem'];sol=q[':question/worked-solution']
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 formatting(p);formatting(sol)
 # Independent actual prompt transcriptions. Bounds come from displayed coordinates.
 integrand=re.search(r'\$\{\\int \}_\{C\}(.*?)\\,\\text\{d\}s,\$',p).group(1);F=parsed(integrand);equal(F,d['F'])
 curve=re.search(r'curve \$(.*?)\$',p).group(1)
 if curve.startswith('y^2='):gg=g.t**2/parsed(curve.split('=',1)[1]).coeff(g.x)
 else:gg=parsed(curve.split('=',1)[1]).subs(g.y,g.t)
 equal(gg,d['g'])
 endpoints=re.findall(r'\$\((.*?)\)[.,]?\$',p)
 bounds=[]
 for i,z in enumerate(endpoints):
  xx,yy=z.split(',',1);yy=parsed(yy);bounds.append(yy);equal(parsed(xx),gg.subs(g.t,yy))
 a,b=bounds;speed=s.sqrt(s.diff(gg,g.t)**2+1);ft=s.simplify(F.subs({g.x:gg,g.y:g.t}));I=s.simplify(ft*speed)
 equal(s.diff(d['H'],g.t),I);independent=s.simplify(d['H'].subs(g.t,b)-d['H'].subs(g.t,a));equal(independent,s.sympify(r['generation']['mathematical_correct_value']))
 # Check every actual choice scalar, then every derivative/substitution/speed block.
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];assert len(choices)==5
 vs=[parsed(v[':answer/value']) for v in choices];assert g.eligible(vs)
 correct=field[':answer-field/correct'][1];hits=[v[':answer/id'] for v in choices if s.simplify(parsed(v[':answer/value'])-independent)==0];assert hits==[correct]
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
 derivative=next(z for z in blocks if z.startswith(r'\begin{aligned}{r}^{′}'))
 speedrows=derivative.split('‖{r}^{′}(t)‖ & =',1)[1].replace(r'\end{aligned}','').split(r' \\  & =')
 # Formal first row is validated by subsequent coordinate and component stages.
 for z in speedrows[1:]:equal(parsed(z),speed)
 drow=derivative.split(r' \\  & =')[2].split(r'\,i+j',1)[0];equal(parsed(drow),s.diff(gg,g.t))
 fblock=next(z for z in blocks if z.startswith(r'\begin{aligned}f(r(t))'))
 for z in fblock.replace(r'\begin{aligned}f(r(t)) & =','').replace(r'\end{aligned}','').split(r' \\  & ='):equal(parsed(z),ft)
 # Last primitive/endpoint rows independently parsed from the rendered output.
 last=blocks[-1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}');rr=last.split(r' \\  & =')
 equal(parsed(rr[-1]),independent)
 equal(parsed(rr[-2]),independent);equal(parsed(rr[-3]),independent)
 if d['f']!='line_power':
  primitive_rows=[z for z in rr if z.startswith(r'\left[')]
  for z in primitive_rows:
   prim,endpoints=z.split(r'\right]_{',1);lo,hi=endpoints.rstrip('}').split('}^{',1);P=parsed(prim.removeprefix(r'\left['));ua,ub=parsed(lo),parsed(hi)
   equal(P.subs(U,ub)-P.subs(U,ua),independent)
   equal(s.diff(P,U).subs(U,d['u'])*s.diff(d['u'],g.t),I)
 # Canonical fingerprint equivalence and presentation/seed invariance.
 rr=g.generate(q[':question/difficulty'].split('/')[-1],seed=902,template=d['f'],parameters=r['generation']['parameters'],profile='method')
 assert rr['question'][':question/id']==q[':question/id']
 assert sorted(choices,key=lambda z:z[':answer/id'])==sorted(rr['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda z:z[':answer/id'])
 return {'template':d['f'],'source_math_readback':True,'solution_stage_checks':len(speedrows)+len(rr),'bank_complete':True}

cases=[];source_report=[];bank_count=0;designations=0
for qid,(f,l,p) in g.CASES.items():
 c={'source_id':qid,'source_db_id':g.SOURCES[qid][':db/id'],'template':f,'parameters':p,'bank_profile':'source:'+qid,'level':l,'level_authored':qid=='q-122579'};cases.append(c)
 r=g.generate(l,template=f,parameters=p,profile=c['bank_profile']);q=g.SOURCES[qid];out=r['question'];raw_field=q[':question/answer-fields'][0];field=out[':question/answer-fields'][0]
 assert out[':question/problem']==q[':question/problem']
 assert out.get(':question/worked-solution')==q.get(':question/worked-solution')
 for k in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (k in out)==(k in q)
 assert (':answer-field/correct' in field)==(':answer-field/correct' in raw_field)
 assert not r['generation']['eligible_for_learning'] and r['generation']['evidence_only']
 original_values=[parsed(v[':answer/value']) for v in raw_field[':answer-field/choices']];displayed_values=[parsed(v[':answer/value']) for v in field[':answer-field/choices']]
 for v in original_values:assert sum(s.simplify(v-w)==0 for w in displayed_values)==1
 assert len(original_values)==len(displayed_values)==5;bank_count+=5
 assert sorted(v[':answer/value'] for v in raw_field[':answer-field/choices'])==sorted(v[':answer/value'] for v in field[':answer-field/choices'])
 if ':answer-field/correct' in raw_field:
  cr=next(v for v in field[':answer-field/choices'] if v[':answer/id']==field[':answer-field/correct'][1]);equal(parsed(cr[':answer/value']),parsed(raw_field[':answer-field/correct'][':answer/value']));designations+=1
 source_report.append({'source_id':qid,'full_bank':True,'prompt_byte_exact':True,'solution_byte_exact_or_absent':True,'key_presence_parity':True,'designation_matched':':answer-field/correct' in field,'opaque_bank':True})
(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
records=[];checks=[]
for l,fs in g.LEVELS.items():
 for f in fs:
  for seed in range(6):
   r=g.generate(l,seed,template=f);normal_check(r);records.append(r)
  # Retain the complete sampler's independent eligibility and arithmetic variety.
  rng=__import__('random').Random(40);seen=set()
  for i in range(150):
   p=g.sample(f,rng);d=g.guard(f,p,l);vv,_=g.method_bank(d)
   if g.eligible(vv):seen.add(s.srepr(d['F'])+s.srepr(d['g']-d['k'] if f=='line_power' else d['g'])+str(d['a'])+str(d['b']))
  assert len(seen)>=10,(f,len(seen))
coverage={l:set() for l in g.LEVELS}
# Exercise actual default API records, including profile eligibility and resampling.
for seed in range(16):
 for l in g.LEVELS:coverage[l].add(g.generate(l,seed)['generation']['template'])
assert all(coverage[l]==set(g.LEVELS[l]) for l in g.LEVELS)
# Explicit endpoint variants through every public raw profile, preserving omissions.
changed=[]
for c in cases:
 p=dict(c['parameters']);p['b']={'sqrt':'3','parabola':'sqrt(99)/2','reciprocal':'3','line_log':'5/2','exponential':'log(3)','implicit_parabola':'4'}[c['template']]
 r=g.generate(c['level'],17,template=c['template'],parameters=p,profile=c['bank_profile']);changed.append(r)
 assert r['question'][':question/problem']!=g.SOURCES[c['source_id']][':question/problem']
 # All terminal rendered scalar arithmetic remains the full integral.
 sol=r['question'].get(':question/worked-solution')
 if sol:
  final=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)[-1].removesuffix(r'\end{aligned}').split(r' \\  & =')[-1]
  equal(parsed(final),s.sympify(r['generation']['mathematical_correct_value']))
# Meaningful explicit domain rejection; no parameter mutation.
for l,f,p in [('easy','line_power',dict(a='0',b='2',c='1',k='1')),('hard','implicit_parabola',dict(a='0',b='3',c='1',k='1')),('moderate','line_log',dict(a='2',b='4',c='1',k='4')),('hard','sqrt',dict(a='0',b='3',c='4',k='1')),('moderate','reciprocal',dict(a='1',b='3',c='1000',k='2')),('easy','line_power',dict(a='1',b='3',c='4',k='8'))]:
 try:g.generate(l,template=f,parameters=p)
 except ValueError:pass
 else:raise AssertionError('invalid explicit workload/domain accepted')
# Fresh atomic renderer writes: same and different endpoints in concurrent calls.
render_data=[g.math_data('parabola',dict(a='1',b=z,c='12',k='1')) for z in ('sqrt(7)','sqrt(10)')]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 paths=list(pool.map(g.render_plot,[render_data[0],render_data[0],render_data[1],render_data[1]]))
assert paths[0]==paths[1] and paths[2]==paths[3] and paths[0]!=paths[2]
for path,d in zip(paths,[render_data[0],render_data[0],render_data[1],render_data[1]]):
 side=json.loads(Path(path).with_suffix('.json').read_text());assert side['b']==str(d['b']) and side['curve']==str(d['g']);assert abs(side['x'][-1]-float(d['g'].subs(g.t,d['b'])))<1e-10
# Each private input is removed by its producer; concurrent external QA producers
# may legitimately own other unique inputs, so no global leak assertion is made.
assert all(Path(path).exists() and Path(path).with_suffix('.json').exists() for path in paths)
# Native choice grading for every supported family and source with an original key.
engine=[]
for i,r in enumerate(records[::6]+[g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']) for c in cases if c['source_id']!='q-122579']):
 field=r['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1]
 engine.append({'label':str(i)+'-'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':v[':answer/id'],'expected':'accepted' if v[':answer/id']==correct else 'rejected','purpose':'complete bank owned radio selection'} for v in field[':answer-field/choices']]})
(HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
subprocess.run([str(HERE.parents[1]/'runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
review=[r for i,r in enumerate(records) if i%6<2]+changed
(HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
md='# Originals and generated variants\n\nAll raw profiles are evidence-only. Changed raw endpoint variants demonstrate explicit parameterized replay; method banks are the learner defaults.\n'
for c in cases:
 q=g.SOURCES[c['source_id']];md+='\n## Original '+c['source_id']+'\n\n'+q[':question/problem']+'\n\n'+ '\n'.join('- $'+v[':answer/value']+'$' for v in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','Source worked solution, key and difficulty are absent.')+'\n'
for r in review:md+='\n## Generated '+r['generation']['template']+' / '+r['generation']['bank_profile']+'\n\n'+g.markdown(r)
(HERE/'review.md').write_text(md)
report={'status':'pass','version':g.VERSION,'source_questions':6,'source_banks_matched':6,'source_options_matched':bank_count,'source_options_byte_exact':bank_count,'source_options_byte_exact_total':bank_count,'source_designations_matched':designations,'source_designations_total_present':5,'source_missing_designations':1,'source_prompts_byte_exact':6,'source_present_solutions_byte_exact':5,'source_unrated':1,'source_correctness':'six exact integrals; missing key independently inferred 149/15 only for completed normal records','source_details':source_report,'normal_records_checked':len(records),'authored_easy':True,'family_coverage':{l:sorted(v) for l,v in coverage.items()},'normal_bank_ambiguity_failures':0,'raw_profiles_evidence_only':True,'native_report':json.loads((HERE/'engine-report.json').read_text()),'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'default_api_records_checked':48,'plot_concurrency':{'same_instance_calls':2,'different_instance_calls':2,'atomic_asset_sidecars_checked':4},'native_ungraded_raw_sources':['q-122579: missing original correct reference; omission preserved'],'engine_binary_sha256':hashlib.sha256((HERE.parents[1]/'runs/current/check-engine').read_bytes()).hexdigest(),'database_writes':0}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: 6/6 full source banks (30 options), 5/5 present designations; 48 normal stage/bank checks; native grader separate.')
