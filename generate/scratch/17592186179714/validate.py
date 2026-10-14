#!/usr/bin/env python3
"""Parse displayed math independently; differentiate prompts; replay complete banks."""
import functools,hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
import sympy as s
from sympy.simplify.fu import fu
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load(D.with_suffix('.py'),'gradient');parser=load(D/'display_parser.py','display')
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,default=str)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def scalar(raw):return parser.scalar(raw)
def vector(raw,n):
 v=tuple(parser.vector(raw));assert n==3 or v[2]==0
 return v[:n]
@functools.lru_cache(maxsize=10000)
def equal(a,b):
 if a==b:return True
 d=s.expand(a-b)
 if d==0:return True
 if d.has(s.tan,s.sec,s.sin,s.cos):
  for point in ({parser.x:0,parser.y:0,parser.z:1},{parser.x:s.pi/3,parser.y:0,parser.z:1},{parser.x:0,parser.y:s.pi,parser.z:0}):
   value=s.simplify(d.subs(point))
   if value.is_zero is False and value.is_finite is True:return False
  return fu(d)==0
 return s.simplify(d)==0
def prompt(q):
 m=re.fullmatch(r'Find the gradient vector field of the function \$f\((.*?)\)\s*=\s*(.*?)\.?\$\.?',q[':question/problem']);assert m,q[':question/problem']
 vs=tuple({'x':parser.x,'y':parser.y,'z':parser.z}[v.strip()] for v in m[1].split(','))
 return scalar(m[2]),vs
def check_record(r):
 q=r['question'];f,vs=prompt(q);answer=tuple(s.diff(f,v) for v in vs);field=q[':question/answer-fields'][0]
 assert len(q[':question/answer-fields'])==1 and field[':answer-field/key']=='selection' and field[':answer-field/type']==':answer-field.type/radio'
 choices=field[':answer-field/choices'];assert len(choices)==5 and all('$' not in a[':answer/value'] for a in choices)
 values=[vector(a[':answer/value'],len(vs)) for a in choices]
 assert all(not all(equal(a,b) for a,b in zip(A,B)) for A,B in itertools.combinations(values,2))
 matches=[a[':answer/id'] for a,V in zip(choices,values) if all(equal(a,b) for a,b in zip(V,answer))];assert matches==[field[':answer-field/correct'][1]]
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==2
 rows=blocks[0].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ');assert len(rows)==2*len(vs)
 for i,v in enumerate(vs):
  m=re.fullmatch(r'f_\{'+str(v)+r'\}\(.*?\)&=\\frac\{\\partial\}\{\\partial '+str(v)+r'\}\\left\((.*?)\\right\)',rows[2*i]);assert m
  assert equal(scalar(m[1]),f) and equal(scalar(rows[2*i+1].removeprefix('&=')),answer[i])
 final=blocks[1].split(r' \\ &= ')[1].removesuffix(r'.\end{aligned}')
 assert all(equal(a,b) for a,b in zip(vector(final,len(vs)),answer))
 # Independently reconstruct task identity from the printed mathematical object.
 assert equal(f,g.model(r['generation']['template'],r['generation']['parameters'])[0])
 replay=g.generate(q[':question/difficulty'].split('/')[-1],r['generation']['seed'],r['generation']['template'],r['generation']['parameters'])
 assert replay==r
 return {'prompt_function':str(f),'gradient':[str(v) for v in answer],'valid_choices':5,'solution_partial_rows':len(vs)}
def fixtures(records):
 return [{'label':r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] else 'rejected','purpose':'independent complete gradient bank'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]} for r in records]
def native(records,p):
 save(p/'input.json',fixtures(records));subprocess.run([str(D/'check-engine'),str(p/'input.json'),str(p/'report.json')],check=True,capture_output=True,text=True,timeout=55)
 return json.loads((p/'report.json').read_text())
def main():
 libraries=[ROOT/'target/release/deps/libcourse_academy_engine-db2f80585ab00950.rlib',ROOT/'target/release/deps/libserde_json-37082c8a95e79bab.rlib']
 for name in ('check-engine','check-pool'):
  subprocess.run(['rustc','--edition=2024','-O',str(D/(name+'.rs')),'--extern','course_academy_engine='+str(libraries[0]),'--extern','serde_json='+str(libraries[1]),'-L','dependency='+str(libraries[0].parent),'-o',str(D/name)],check=True,capture_output=True,text=True,timeout=55)
 save(D/'reference/native/build.json',{'libraries':{str(p):sha(p) for p in libraries},'binaries':{n:sha(D/n) for n in ('check-engine','check-pool')},'sources':{n:sha(ROOT/n) for n in ['engine/rust/learning.rs','engine/rust/assessment_sampling.rs']}})
 replays=[];samples=[];coverage={};banks=[]
 for name,(level,mid,params) in g.TEMPLATES.items():
  print('Checking '+name,flush=True)
  r=g.replay(name);check_record(r);o=g.SOURCES[mid];n=len(prompt(o)[1]);old=o[':question/answer-fields'][0]
  ov=[vector(a[':answer/value'],n) for a in old[':answer-field/choices']];nv=[vector(a[':answer/value'],n) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  mapping=[]
  for a,v in zip(old[':answer-field/choices'],ov):
   matches=[j for j,w in enumerate(nv) if all(equal(x,y) for x,y in zip(v,w))];assert len(matches)==1,(name,a,matches)
   mapping.append({'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'recipe_index':matches[0],'formula_at_source':list(map(str,nv[matches[0]]))})
  assert len({m['recipe_index'] for m in mapping})==5
  f,_=prompt(o);assert equal(f,prompt(r['question'])[0])
  key=old[':answer-field/correct'][':answer/id'];assert all(equal(a,b) for a,b in zip(ov[next(i for i,a in enumerate(old[':answer-field/choices']) if a[':answer/id']==key)],nv[next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1])]))
  banks.append({'template':name,'profile':'observed','source_id':mid,'source_parameters':params,'matched_options':5,'matched_distractors':4,'correct_designation_preserved':True,'mapping':mapping})
  replays.append(r);coverage[name]={k:set() for k in params}
  # Each declared slot's complete discrete domain, with all other slots fixed.
  cases=[params]
  for k,values in g.BOUNDS[name].items():
   for value in values:
    p=dict(params);p[k]=value
    try:g.guard(name,p)
    except ValueError:
     other='c' if name=='separate_roots' else 'b' if name in ('linear_log','linear_tan') else None
     if other is None:continue
     other=other if k=='a' else 'a'
     p[other]=next(v for v in g.BOUNDS[name][other] if v!=(-p[k] if name=='linear_tan' else p[k]))
     g.guard(name,p)
    cases.append(p)
  for i,p in enumerate(cases):
   r=g.generate(level,seed=i,template=name,parameters=p);check_record(r);samples.append(r)
   for k,value in p.items():coverage[name][k].add(value)
  for i in range(4):
   r=g.generate(level,seed=1700+i,template=name);check_record(r);samples.append(r)
   for k,value in r['generation']['parameters'].items():coverage[name][k].add(value)
 # Independent audit of existing practice, including missing/erroneous records.
 source_audit=[]
 for o in g.KP[':knowledge-point/questions']:
  errors=[]
  if ':question/difficulty' not in o:errors.append('unrated')
  if ':question/worked-solution' not in o:errors.append('missing worked solution')
  if ':answer-field/correct' not in o[':question/answer-fields'][0]:errors.append('missing correct answer reference')
  if o[':question/math-academy-id']=='q-122601':errors.append('worked-solution final j component uses zz instead of xz; partial rows and correct bank are right')
  source_audit.append({'source_id':o[':question/math-academy-id'],'valid_for_inventory':not errors,'errors':errors})
 save(D/'source-bank-replay.json',banks);save(D/'source-audit.json',source_audit);save(D/'reference/replay.json',replays);save(D/'reference/sampled.json',samples)
 grade=native(replays+samples,D/'reference/native/grading')
 coverage={t:{k:sorted(v) for k,v in slots.items()} for t,slots in coverage.items()}
 assert all(set(values)==set(g.BOUNDS[t][k]) for t,slots in coverage.items() for k,values in slots.items()),coverage
 one=g.generate('easy',template='linear_log',parameters={'a':2,'b':4})
 two=g.generate('easy',template='linear_log',parameters={'a':3,'b':6})
 assert one['generation']['mathematical_fingerprint']==two['generation']['mathematical_fingerprint']
 assert one['question'][':question/id']!=two['question'][':question/id'],'different complete banks need distinct stable identities'
 # Fixed targets remain x,y[,z]. Coefficient perturbation cannot leave stale keys.
 save(D/'slot-coverage.json',coverage)
 (D/'reference/side-by-side.md').write_text('\n\n---\n\n'.join('### '+n+'\n\nOriginal:\n\n'+g.SOURCES[mid][':question/problem']+'\n\nVariant:\n\n'+g.generate(l,1701,template=n)['question'][':question/problem']+'\n\n'+g.generate(l,1701,template=n)['question'][':question/worked-solution'] for n,(l,mid,_) in g.TEMPLATES.items()))
 try:g.generate('hard')
 except ValueError:pass
 else:raise AssertionError('Unsupported band accepted')
 report={'passed':True,'basis':g.RAW['basis'],'lineage':g.RAW['lineage'],'supported_levels':['easy','moderate'],'unsupported_levels':['hard'],'source_fidelity':{'complete_banks':'8/8','distractors':'32/32','options':'40/40','correct_refs':'8/8','layout':'same prompt contract, one five-choice radio, partial derivative rows then vector assembly','source_error':'arctan final zz corrected to xz in generated solution only'},'source_exclusions':2,'validated_variants':len(samples),'all_slots_covered':coverage,'mathematics':'independently parsed prompts, every partial derivative row, complete bank, final vector and deterministic replay','grading':{'entry_point':grade['entry_point'],'accepted':grade['accepted_checks'],'rejected':grade['rejected_checks']},'file_hashes':{str(p.relative_to(ROOT)):sha(p) for p in [D.with_suffix('.py'),D/'source.json',D/'display_parser.py',D/'validate.py']}}
 save(D/'validation.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ['file_hashes','all_slots_covered']},indent=2))
if __name__=='__main__':main()
