#!/usr/bin/env python3
"""Fail on independent math, source fidelity, identity, scope, or native grade."""
import copy, importlib.util, json, math, os, subprocess, sys, hashlib, uuid, re
from pathlib import Path
ROOT=Path(__file__).parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
spec=importlib.util.spec_from_file_location('v',ROOT/'independent.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def write(name,data): (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def failmutation(r,change,label):
 rr=copy.deepcopy(r);change(rr)
 try:v.check_record(rr)
 except (AssertionError,ValueError,KeyError,StopIteration):return {'label':label,'rejected':True}
 raise AssertionError('Mutation escaped '+label)

def family_space(t):
 if g.TEMPLATES[t][0]=='easy':return [{'axis':axis,'a':a} for axis in ['x','y'] for a in range(-6,7)]
 if t=='sum_difference':return [{'m':m,'n':n} for m in range(1,7) for n in range(1,7) if math.gcd(m,n)==1]
 if t=='log_halfplane':return [{'m':m,'b':b} for m in range(-6,7) if m for b in range(7)]
 if t=='log_parabola':return [{'m':m,'b':b} for m in range(1,13) for b in range(7)]
 if t=='atan_circle_line':return [{'r2':r,'c':c} for r in range(1,17) for c in range(-3,4) if c*c<r]
 if t=='rectangle':return [{'a':a,'b':b} for a in range(1,7) for b in range(1,7)]
 if t in ('half_disk','disk_line'):return [{'r2':r,'m':m} for r in range(1,17) for m in range(-4,5) if m]
 return [{'r2':r} for r in range(1,17)]

def main():
 originals=[];cases=[];fidelity=[];checks=[];variants=[];mutations=[]
 for t,(level,sid) in g.TEMPLATES.items():
  if sid:
   case={'source_id':sid,'difficulty':level,'template':t,'parameters':g.ANCHORS[t],'bank_profile':'observed:'+sid};cases.append(case)
   r=g.generate(level,17,t,parameters=case['parameters'],profile=case['bank_profile']);src=g.QUESTIONS[sid];q=r['question'];f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
   assert set(q)==set(src),'question key-presence fidelity'
   assert set(f)==set(sf),'field key-presence fidelity'
   assert all(set(a)==set(sf[':answer-field/choices'][0]) for a in f[':answer-field/choices'])
   assert q[':question/problem']==src[':question/problem']
   assert q[':question/worked-solution']==src[':question/worked-solution']
   assert q[':question/difficulty']==src[':question/difficulty'][':db/ident']
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
   correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct[':answer/value']==sf[':answer-field/correct'][':answer/value']
   assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
   v.check_source_geometry(r)
   fidelity.append({'source_id':sid,'prompt_exact':True,'solution_exact':True,'bank_values':5,'correct_designation_match':True,'attribute_presence_match':True})
   if sid in ['q-122518','q-122671','q-122710','q-122677','q-122554']:case['plotted_domain_evidence']=json.loads((ROOT/'plot-source-domains.json').read_text())['domains'][sid]
   originals.append(r)
  # Two variants PER observed family and each easy authored family, not just levels.
  for seed in [19,41]:
   print('Checking',t,seed,flush=True);r=g.generate(level,seed,t);variants.append(r)
  if sid:
   # Parameterized original source profile at a changed valid object.
   changed=family_space(t)[-1];r=g.generate(level,93,t,parameters=changed,profile='observed:'+sid)
   assert r['question'][':question/problem']!=src[':question/problem'] or t=='closed_disk_puncture' and changed==g.ANCHORS[t]
   assert r['generation']['evidence_only'];v.balanced(r['question'][':question/problem']);v.balanced(r['question'][':question/worked-solution'])
 # Actual default API calls must cover every family, with filtering before sampling.
 default_coverage={}
 import random
 for level in ['easy','moderate','hard']:
  families=[t for t,info in g.TEMPLATES.items() if info[0]==level];seen=set()
  for seed in range(100):
   expected=random.Random(seed).choice(families)
   if expected not in seen:
    print('Default coverage',level,seed,expected,flush=True);rr=g.generate(level,seed);assert rr['generation']['template']==expected;variants.append(rr);seen.add(expected)
   if seen==set(families):break
  assert seen==set(families);default_coverage[level]=sorted(seen)
 for t,(level,sid) in g.TEMPLATES.items():
  if sid:
   print('Normal repaired anchor',t,flush=True);variants.append(g.generate(level,43,t,parameters=g.ANCHORS[t]))
 raw_rectangle=next(r for r in originals if r['generation']['template']=='rectangle');mutated=copy.deepcopy(raw_rectangle);mutated['generation']['geometry'][1]['lower_closed']=False
 try:v.check_source_geometry(mutated)
 except AssertionError:mutations.append({'label':'historical rectangle lower-edge inclusion','rejected':True})
 else:raise AssertionError('historical rectangle lower-edge mutation escaped')
 mutated=copy.deepcopy(raw_rectangle);mutated['generation']['geometry'][3]['cx']=False
 try:v.check_source_geometry(mutated)
 except AssertionError:mutations.append({'label':'historical rectangle vertical-side inclusion','rejected':True})
 else:raise AssertionError('historical rectangle vertical-side mutation escaped')
 for rr in variants:
  content=[rr['question'][':question/problem'],rr['question'][':question/worked-solution']]+[a[':answer/value'] for a in rr['question'][':question/answer-fields'][0][':answer-field/choices']]
  assert not any(re.search(r'(?<!\\)\{\(x,y\)',text) for text in content),'invisible outer set glyph'
 # All normal raw selector spellings, ineligible selector rejection.
 for selector in ['radio',':answer-field.type/radio','answer-field.type/radio']:
  assert g.generate_easy(1,field_type=selector)['question'][':question/answer-fields'][0][':answer-field/type']==':answer-field.type/radio'
 for selector in ['blank',':answer-field.type/blank','math','image']:
  try:g.generate_easy(1,field_type=selector)
  except ValueError:pass
  else:raise AssertionError('unsupported selector accepted')
 # Identity must be independent of seed/order for fixed content.
 a=variants[0];aa=g.generate('easy',seed=91,template=a['generation']['template'],parameters=a['generation']['parameters']);assert a['question'][':question/id']==aa['question'][':question/id']
 assert {z[':answer/id'] for z in a['question'][':question/answer-fields'][0][':answer-field/choices']}=={z[':answer/id'] for z in aa['question'][':question/answer-fields'][0][':answer-field/choices']}
 for t,(l,sid) in g.TEMPLATES.items():
  space=family_space(t)
  for p in space:g.guards(t,p)
  # Domain—not visual radius spelling or option order—defines task variety.
  assert len({tuple(str(c) for c in g.model(t,p)[-1]) for p in space})==len(space)
 for t,p in [('sqrt_axis',{'axis':'x','a':7}),('sum_difference',{'m':2,'n':2}),('log_halfplane',{'m':0,'b':0}),('log_parabola',{'m':0,'b':1}),('atan_circle_line',{'r2':1,'c':1}),('rectangle',{'a':0,'b':1}),('half_disk',{'r2':2,'m':0}),('disk_line',{'r2':17,'m':1})]:
  try:g.generate(g.TEMPLATES[t][0],template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError('explicit out of scope parameters accepted')
 mutations.append(failmutation(a,lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem']+'\x0c'),'C0 formfeed regression'))
 mutations.append(failmutation(a,lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('set it equal to zero and solve:','skip this operation:').replace('solve the following inequality:','skip this operation:')),'operative-stage deletion'))
 mutations.append(failmutation(a,lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/correct',[':answer/id',next(z[':answer/id'] for z in r['question'][':question/answer-fields'][0][':answer-field/choices'] if z[':answer/id']!=r['question'][':question/answer-fields'][0][':answer-field/correct'][1])]),'wrong correct designation'))
 hard=next(r for r in variants if r['generation']['template']=='open_disk_puncture')
 mutations.append(failmutation(hard,lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace(str(r['generation']['parameters']['r2'])+'-',str(r['generation']['parameters']['r2']+1)+'-',1)),'displayed radius mutation'))
 for r in originals+variants:
  f=r['question'][':question/answer-fields'][0];checks.append({'label':(r['generation']['source_id'] or r['generation']['template'])+' '+str(r['generation']['seed'])+' '+r['generation']['profile'],'record':r,'checks':[{'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned choice selection through real learner grader'} for z in f[':answer-field/choices']]})
 # Fresh, concurrent renders: same geometry twice and a different geometry twice.
 from concurrent.futures import ThreadPoolExecutor
 concurrent_root=ROOT/'concurrency'/str(uuid.uuid4());concurrent_root.mkdir(parents=True)
 objects=[{'shape':'disk','r2':13,'closed':False,'puncture':True,'line':3}, {'shape':'disk','r2':15,'closed':True,'side':['gt',-2]}]
 script="import importlib.util,json,sys;from pathlib import Path;s=importlib.util.spec_from_file_location('g',sys.argv[1]);g=importlib.util.module_from_spec(s);s.loader.exec_module(g);g.ROOT=Path(sys.argv[2]);print(g.render_graph(json.loads(sys.argv[3])))"
 def concurrent_render(obj):return subprocess.run([sys.executable,'-c',script,str(ROOT.with_suffix('.py')),str(concurrent_root),json.dumps(obj)],cwd=REPO,text=True,capture_output=True,check=True).stdout.strip()
 with ThreadPoolExecutor(max_workers=4) as pool:paths=list(pool.map(concurrent_render,[objects[0],objects[0],objects[1],objects[1]]))
 assert paths[0]==paths[1] and paths[2]==paths[3] and paths[0]!=paths[2]
 for path in set(paths):
  data=json.loads(Path(path).with_suffix('.json').read_text());v.visual_check(path,data);assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==data['png_sha256']
 assert not list((concurrent_root/'plots').glob('*-*.png')) and not list((concurrent_root/'plots').glob('*-*.json'))
 concurrency={'fresh_render_calls':4,'identical_and_different_objects':True,'atomic_sidecar_hashes':True,'directory':str(concurrent_root)}
 write('engine-input.json',checks)
 engine=REPO/'generate/runs/current/check-engine';subprocess.run([str(engine),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True,cwd=REPO)
 write('source-cases.json',cases);write('review.json',variants)
 lines=['# Domain of a Vector Field: review','All historical records below are evidence-only. Generated variants use complete method-derived banks.']
 for case,r in zip(cases,originals):
  lines.extend(['\n## Original '+case['source_id'],g.markdown(r)])
  for variant in [z for z in variants if z['generation']['template']==case['template']]:lines.extend(['\n### Generated variant (authored bank) '+str(variant['generation']['parameters']),g.markdown(variant)])
 for r in [z for z in variants if z['generation']['authored_level']]:lines.extend(['\n## Authored easy '+r['generation']['template']+' '+str(r['generation']['parameters']),g.markdown(r)])
 (ROOT/'review.md').write_text('\n\n'.join(lines))
 report={'status':'passed','source_fidelity':{'sources':9,'exact_prompts':9,'exact_solutions':9,'complete_banks':9,'displayed_answer_values':45,'correct_designations':9,'raw_key_presence':9,'independently_transcribed_plot_choices':25},'independent_normal_records':len(variants),'authored_easy_records':sum(1 for r in variants if r['generation']['authored_level']),'default_family_coverage':default_coverage,'templates':len(g.TEMPLATES),'finite_task_counts':{t:len(family_space(t)) for t in g.TEMPLATES},'source_anomalies':['q-122474 solution Q numerator y instead of displayed x (domain unchanged)','q-122518 choices0/2 equivalent wrong domain (origin exclusion redundant)','q-122663 solution D2 prose says P instead of Q','q-122554 second region labeled D1 instead of D2','q-122671 closed disk called interior','q-122710 minor missing when in prose'],'mutations':mutations,'concurrency':concurrency,'native_binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'native':json.loads((ROOT/'engine-report.json').read_text()),'runtime':{'python':sys.version.split()[0],'sympy':g.sp.__version__,'matplotlib':__import__('matplotlib').__version__},'remaining_limits':['Historical wrong-recipe intentions are not recovered; all observed profiles are evidence-only.','Original rasters reproduced as exact asset references at anchors; changed plots follow inspected geometric recipes.','Independent predicate equivalence uses exact boundary points plus a finite rational grid; this is bounded-family validation, not a general decision procedure.'],'database_writes':0}
 write('validation.json',report);print('PASS:9 sources45 values;'+str(len(variants))+' generated records;'+str(sum(report['finite_task_counts'].values()))+' finite tasks',flush=True)
if __name__=='__main__':main()
