#!/usr/bin/env python3
"""Independent displayed-math readback, raw fidelity, identity and native grading."""
import importlib.util,itertools,json,re,subprocess,hashlib,sys
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('flux_generator',D.with_suffix('.py'))
p=module('readback',ROOT/'generate/runs/current/divergence-readback.py')
x,y,z=p.variables;math=p.scalar
COUNTS={'normal_records':0,'displayed_components':0,'formal_held_partials':0,'substituted_partial_rows':0,'divergence_rows':0,'complete_integral_choices':0}
def equal(a,b):return s.expand(a-b)==0
def group(text,pos):
 assert text[pos]=='{';depth=1;end=pos+1
 while depth:depth+=(text[end]=='{')-(text[end]=='}');end+=1
 return text[pos+1:end-1],end

def read_integral(text):
 text=text.strip().rstrip('.,');bounds=[];pos=0
 for _ in range(3):
  assert text[pos:].startswith(r'{\int }_');pos+=len(r'{\int }_');lo,pos=group(text,pos);assert text[pos]=='^';hi,pos=group(text,pos+1);bounds.append((math(lo),math(hi)))
 assert text[pos:].startswith(r'\,');pos+=2;cut=text.index(r'\,\text{d}',pos);integrand=math(text[pos:cut]);variables=re.findall(r'\\text\{d\}([xyz])',text[cut:]);assert len(variables)==3
 return integrand,tuple(({'x':x,'y':y,'z':z}[v],*b) for v,b in zip(reversed(variables),bounds))
def eval_integral(obj):
 d,bounds=obj
 for v,a,b in reversed(bounds):d=s.integrate(d,(v,a,b))
 return s.simplify(d)
def setup_equal(a,b):return equal(a[0],b[0]) and all(v==w and equal(l,m) and equal(u,n) for (v,l,u),(w,m,n) in zip(a[1],b[1]))
def formatting(text):
 assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
 assert text.count('$')%2==0
 depth=0
 for match in re.finditer(r'(?<!\\)[{}]',text):
  depth+=1 if match[0]=='{' else -1;assert depth>=0
 assert depth==0

def check(r):
 q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];f=q[':question/answer-fields'][0]
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 for text in [prompt,sol]+[a[':answer/value'] for a in f[':answer-field/choices']]:formatting(text)
 cs=p.field(prompt);assert cs is not None;COUNTS['displayed_components']+=3
 ds=tuple(s.diff(c,v) for c,v in zip(cs,p.variables));div=sum(ds)
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);der=blocks[1];_,inputs=p.derivative_inputs(der);assert len(inputs)==3
 assert [v for v,*_ in inputs]==['x','y','z']
 for c,(_,arg,*_) in zip(cs,inputs):assert equal(math(arg),c);COUNTS['formal_held_partials']+=1
 rows=der.split(' & =')[1:];assert len(rows)==3
 substitute=rows[1].split(r'\\')[0].strip();assert equal(math(substitute),div)
 # Every individual contribution must survive before the collected row.
 terms=re.split(r'(?<![({])\+',substitute) if False else substitute
 # The shared normal printer groups signed summands. Parse the three intended
 # top-level terms independently instead of accepting only their final sum.
 def top_terms(t):
  depth=0;start=0;out=[]
  for i,c in enumerate(t):
   if c in '({':depth+=1
   if c in ')}':depth-=1
   if c=='+' and depth==0:out.append(t[start:i]);start=i+1
  return out+[t[start:]]
 actual=top_terms(substitute);assert len(actual)==3
 for term,d in zip(actual,ds):assert equal(math(term),d);COUNTS['substituted_partial_rows']+=1
 final=rows[2].split(r'\end{aligned}')[0].strip().rstrip('.');assert equal(math(final),div);COUNTS['divergence_rows']+=1
 # Reconstruct planes/surfaces from the displayed prompt, never generation data.
 before=prompt.split('Given that')[0];eqs=re.findall(r'\$([xyz])=(.*?)\$',before)
 assert len(eqs)==6;bounds=[]
 for i in range(0,6,2):
  v=eqs[i][0];assert eqs[i+1][0]==v;bounds.append(({'x':x,'y':y,'z':z}[v],math(eqs[i][1]),math(eqs[i+1][1])))
 expected=(div,tuple(bounds));level=q[':question/difficulty'].split('/')[-1]
 choices=f[':answer-field/choices'];assert len(choices)==5
 if level=='easy':
  objects=[math(a[':answer/value']) for a in choices];valid=[i for i,d in enumerate(objects) if equal(d,div)]
  assert all(not equal(a,b) for a,b in itertools.combinations(objects,2))
 else:
  objects=[read_integral(a[':answer/value']) for a in choices];valid=[i for i,obj in enumerate(objects) if setup_equal(obj,expected)]
  assert len(set(str(eval_integral(obj)) for obj in objects))==5
  COUNTS['complete_integral_choices']+=5
 assert len(valid)==1;assert choices[valid[0]][':answer/id']==f[':answer-field/correct'][1]
 # The final displayed integral must use the exact prompt region and divergence.
 final_integral=re.search(r'(\{\\int \}_.*?)\.\\end\{aligned\}',blocks[-1]).group(1)
 assert setup_equal(read_integral(final_integral),expected)
 assert ':question/math-academy-id' not in q
 assert len(set(a[':answer/id'] for a in choices))==5
 COUNTS['normal_records']+=1
 return cs,ds,expected

def run():
 cases=[];raw_records=[];fidelity={'banks':0,'values':0,'designations':0,'prompt_exact':0,'solution_exact':0,'attribute_presence':0,'missing_designations':1,'missing_solutions':1,'unrated':1}
 for t,c in g.CONFIG.items():
  if 'index' not in c:continue
  q0=g.source_q(t);case={'source_id':q0[':question/math-academy-id'],'db_id':q0[':db/id'],'level':c['level'],'template':t,'parameters':{'s':1},'bank_profile':'observed_raw'};cases.append(case)
  r=g.generate(c['level'],template=t,parameters=case['parameters'],profile='observed_raw');q=r['question'];raw_records.append(r);sf=q0[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
  assert q[':question/problem']==q0[':question/problem'];fidelity['prompt_exact']+=1
  for key in (':question/difficulty',':question/worked-solution'):assert (key in q)==(key in q0)
  assert (':answer-field/correct' in sf)==(':answer-field/correct' in nf);fidelity['attribute_presence']+=1
  if ':question/worked-solution' in q:assert q[':question/worked-solution']==q0[':question/worked-solution'];fidelity['solution_exact']+=1
  assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in nf[':answer-field/choices']);fidelity['banks']+=1;fidelity['values']+=5
  if ':answer-field/correct' in sf:
   selected=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert selected==sf[':answer-field/correct'][':answer/value'];fidelity['designations']+=1
  # Independently validate the source's displayed component field and every
  # formal/collected mathematical stage, separately from exact-byte fidelity.
  original_cs=p.field(q0[':question/problem']);original_ds=tuple(s.diff(e,w) for e,w in zip(original_cs,p.variables));original_div=sum(original_ds)
  if ':question/worked-solution' in q0:
   original_blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q0[':question/worked-solution'],re.S);der=original_blocks[1];_,inputs=p.derivative_inputs(der)
   assert len(inputs)==3 and [v for v,*_ in inputs]==['x','y','z']
   for e,(_,arg,*_) in zip(original_cs,inputs):assert equal(math(arg),e)
   rows=der.split(' & =')[1:];assert len(rows)==3
   for row in rows[1:]:assert equal(math(row.split(r'\\')[0].split(r'\end{aligned}')[0].strip().rstrip('.')),original_div)
  if ':answer-field/correct' in sf:
   answer=sf[':answer-field/correct'][':answer/value']
   if c['level']=='easy':assert equal(math(answer),original_div)
   else:assert setup_equal(read_integral(answer),(original_div,(*c['outer'],c['inner'])))
  # Changed scale raw replay is an actual recipe, not a literal source sampler.
  changed=g.generate(c['level'],template=t,parameters={'s':3},profile='observed_raw');assert changed['question'][':question/problem']!=q[':question/problem']
  cs=p.field(changed['question'][':question/problem']);assert all(equal(a,3*b) for a,b in zip(cs,c['components']))
  raw_obj=c['bank']
  for old in sf[':answer-field/choices']:
   if c['level']=='easy':assert any(equal(math(old[':answer/value']),v) for v in raw_obj)
   else:
    ob=read_integral(old[':answer/value']);assert any(setup_equal(ob,(s.sympify(d),(c['outer'][0],c['outer'][1],(c['inner'][0],s.sympify(l),s.sympify(u))))) for d,l,u in raw_obj)
 (D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 reviews=[];native=[];fingerprints={l:set() for l in ('easy','moderate','hard')};family_coverage=set()
 for t,c in g.CONFIG.items():
  for seed in range(24):
   r=g.generate(c['level'],seed,t);check(r);fingerprints[c['level']].add(r['generation']['mathematical_fingerprint'])
   if seed<2:reviews.append(r)
   f=r['question'][':question/answer-fields'][0]
   native.append({'label':t+'-'+str(seed),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual radio grading for complete bank'} for a in f[':answer-field/choices']]})
   # Content identity is independent of seed/option order at explicit parameters.
   again=g.generate(c['level'],seed+999,t,parameters=r['generation']['parameters']);assert again['question'][':question/id']==r['question'][':question/id']
 for l in ('easy','moderate','hard'):
  for seed in range(80):family_coverage.add(g.generate(l,seed)['generation']['template'])
 assert family_coverage==set(g.CONFIG)
 # Reject every invalid explicit domain rather than silently repair inputs.
 for t,c in g.CONFIG.items():
  for bad in ({'a':0},{'b':5},{'h':-1},{'u':3}):
   p0={'a':1,'b':1,'c':1,'h':1,'u':1,'v':1}|bad
   try:g.generate(c['level'],template=t,parameters=p0)
   except ValueError:pass
   else:raise AssertionError('invalid domain accepted')
 # Mutation checks: a formal held-coordinate change and a balanced control byte
 # must fail even if metadata and final correct selection remain unchanged.
 r=reviews[0]
 for old,new in ((r'\frac{∂}{∂x}',r'\frac{∂}{∂y}'),('Computing','Comp\futing')):
  bad=json.loads(json.dumps(r));bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(old,new,1)
  try:check(bad)
  except (AssertionError,ValueError):pass
  else:raise AssertionError('mutation survived')
 # Faithful rated source banks grade by IDs; do not fabricate legacy correct ref.
 for r in raw_records:
  f=r['question'][':question/answer-fields'][0]
  if ':answer-field/correct' in f:native.append({'label':'raw-'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'faithful observed designation'} for a in f[':answer-field/choices']]})
 (D/'native-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n');subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 (D/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n')
 doc='# Source and generated review\n\nRaw original records are evidence-only. Generated records use complete method-derived banks.\n'
 for raw in raw_records:doc+='\n## Original '+raw['generation']['template']+'\n\n'+g.markdown(raw)+'\n'
 for r in reviews:doc+='\n## Generated '+r['generation']['template']+' / '+r['question'][':question/difficulty']+'\n\n'+g.markdown(r)+'\n'
 (D/'review.md').write_text(doc)
 result={'status':'passed','source_fidelity':fidelity,'independent_display_checks':COUNTS,'sampled_unique_mathematical_tasks':{k:len(v) for k,v in fingerprints.items()},'default_family_coverage':sorted(family_coverage),'native':json.loads((D/'native-report.json').read_text()),'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'plot_rating':'none','source_anomalies':['legacy unrated/missing solution/missing correct designation; raw omissions preserved; authored easy completion independently derived','typeIIIbowl raw correct and flat-bound 2xy option both scalar zero on symmetric x domain; raw evidence only; normal avoids whole-bank value collisions','raw typeII/typeI/typeIIIbowl region-set literal braces; retained only in evidence; normal uses escaped visible braces'],'database_writes':0}
 (D/'validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='native'},indent=2))
if __name__=='__main__':run()
