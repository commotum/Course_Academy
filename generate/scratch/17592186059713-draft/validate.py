#!/usr/bin/env python3
"""Independent QA reads displayed vector definitions, operation, rows and choices.
Run from repository root: .venv/bin/python generate/scratch/17592186059713-draft/validate.py
Writes evidence only in this folder; real native grader uses memory fixtures.
"""
import copy, hashlib, importlib.util, importlib.metadata, json, os, re, subprocess, sys
from pathlib import Path
from collections import Counter
import sympy as sp
D=Path(__file__).resolve().parent;REPO=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,data): (D/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def normalize(text):
 text=re.sub(r'\\overset\{\\to \}\{([uUvVwW])\}',r'\1',text)
 text=re.sub(r'([uvwUVW])\^\(→\)',r'\1',text)
 return text.replace(r'\cdot','*').replace('−','-')
def evaluate(text,env):
 text=normalize(text).strip().replace('&','')
 text=re.sub(r'⟨([^,⟩]+),([^⟩]+)⟩',lambda m:'Matrix(['+m[1]+','+m[2]+'])',text)
 text=re.sub(r'(\d)([uvwUVW])',r'\1*\2',text)
 return sp.sympify(text,locals={'Matrix':sp.Matrix,**env})
def read_prompt(q):
 prompt=q[':question/problem'];fragments=re.findall(r'\$([^$]+)\$',prompt);env={}
 for f in fragments[:-1]:
  left,right=normalize(f).split('=',1)
  assert left.strip() in ('u','v','w','U','V','W'),left
  env[left.strip()]=evaluate(right,{})
 assert fragments[-1].rstrip().endswith('=')
 request=normalize(fragments[-1]).strip()[:-1].strip()
 return env,request,evaluate(request,env)
def check_format(s):
 assert not any(ord(c)<32 and c not in '\n\t' for c in s),'C0 control character'
 assert s.count('$')%2==0,'math delimiter'
 depth=0
 for char in s:
  if char=='{':depth+=1
  if char=='}':depth-=1
  assert depth>=0,'brace'
 assert depth==0,'brace'
 assert not re.search(r'(?<!\\)\\(?!\\|[A-Za-z ])',s),'unexpected single slash'
 assert '--' not in s and '+-' not in s,'bare signed operation'
def rows(q):
 solution=q.get(':question/worked-solution')
 if solution is None:return []
 match=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S);assert match
 return [s.strip() for s in match[1].split('\\\\')]
def independent_bank(r,env,request,z):
 t=r['generation']['template'];profile=r['generation']['profile']; letters=('U','V') if t=='sum_upper' else ('u','v');a=env.get(letters[0],env.get('v'));b=env.get(letters[1],sp.zeros(2,1))
 if t.startswith('sum'):return [z,a-b,b-a,sp.Matrix([a[0]+b[0],a[1]-b[1]]),sp.Matrix([a[0]-b[0],a[1]+b[1]])]
 if t=='subtract' and profile=='raw-q-1323':return [z,sp.Matrix([a[0],b[1]]),sp.Matrix([-z[0],a[1]+b[1]]),sp.Matrix([z[0],-z[1]]),sp.Matrix([b[0],a[0]-b[0]])]
 if t=='subtract':return [z,a+b,b-a,sp.Matrix([a[0]-b[0],a[1]+b[1]]),sp.Matrix([a[0]+b[0],a[1]-b[1]])]
 if t=='scalar':
  a=env['v'];n=int(re.match(r'(-?\d+)v',request)[1]);return [z,-z,a+sp.ones(2,1)*n,sp.Matrix([-z[0],z[1]]),-a-sp.ones(2,1)*n]
 if t=='linear_combination':
  m=re.fullmatch(r'(\d+)u([+-])(\d+)v',request);assert m;n,q,s=int(m[1]),int(m[3]),1 if m[2]=='+' else -1
  return [z,n*a-s*q*b,a+s*q*b,n*a+s*b,sp.Matrix([n*a[0]+s*q*b[0],a[1]+s*b[1]])]
 m=re.fullmatch(r'(\d+)u-\((\d+)v([+-])(\d+)w\)',request);assert m;n,q,s,c=int(m[1]),int(m[2]),1 if m[3]=='+' else -1,int(m[4]);w=env['w']
 return [z,n*a-q*b+s*c*w,n*a+q*b+s*c*w,a-(q*b+s*c*w),n*a-(b+s*w)]
def check_record(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];env,request,z=read_prompt(q);check_format(q[':question/problem'])
 rs=rows(q)
 if rs:
  check_format(q[':question/worked-solution']);assert q[':question/worked-solution'].startswith(g.OPENING)
  expected_count=6 if r['generation']['template']=='nested_combination' else 4 if r['generation']['template']=='linear_combination' else 3
  assert len(rs)==expected_count,('stage count',rs)
  left=rs[0].split('=',1)[0].replace('&','').strip();assert evaluate(left,env)==z,'solution formal operation'
  for row in rs:
   value=evaluate(row.split('=',1)[1],env);assert value==z,('solution stage',row,value,z)
  assert re.fullmatch(r'\s*&?\s*=\s*⟨\s*-?\d+\s*,\s*-?\d+\s*⟩',rs[-1]),'collected conclusion'
  t=r['generation']['template']
  if t=='scalar': assert rs[1].count(r'\cdot')==2,'two distributed products'
  if t=='linear_combination': assert rs[1].count(r'\cdot')==4 and rs[2].count(r'\cdot')==0,'four distributed products then evaluation'
  if t=='nested_combination':
   assert rs[1].count(r'\cdot')==6,'six distributed products'
   assert len(re.findall('⟨',rs[2]))==3 and len(re.findall('⟨',rs[3]))==2,'individually evaluated vectors before inner reduction'
   assert rs[4].count('⟨')==1 and rs[4].count('-')>=2,'component subtraction before collection'
  # Verify each substituted/evaluated vector independently: correlated errors must fail.
  def vector_nodes(row): return [evaluate(v,{}) for v in re.findall(r'⟨[^⟩]+⟩',row)]
  def component_operands(row,first,second,sign):
   pair=re.search(r'⟨([^,]+),([^⟩]+)⟩',row);assert pair
   for i,part in enumerate(pair.groups()):
    token=re.fullmatch(r'\s*(-?\d+)\s*([+-])\s*(\(?-?\d+\)?)\s*',part);assert token,('component operand structure',part)
    assert int(token[1])==int(first[i]) and int(token[3].strip('()'))==int(second[i]) and token[2]==sign,('individual evaluated operands',part,first,second,sign)
  initial=vector_nodes(rs[0])
  if t.startswith('sum') or t=='subtract':
   a,b=(env['U'],env['V']) if t=='sum_upper' else (env['u'],env['v'])
   assert initial==[a,b],'individual substituted vectors'
   component_operands(rs[1],a,b,'+' if t.startswith('sum') else '-')
  elif t=='scalar':
   assert initial==[env['v']],'individual substituted scalar vector'
  elif t=='linear_combination':
   m=re.fullmatch(r'(\d+)u([+-])(\d+)v',request)
   assert initial==[env['u'],env['v']],'individual substituted linear vectors'
   component_operands(rs[2],int(m[1])*env['u'],int(m[3])*env['v'],m[2])
  else:
   m=re.fullmatch(r'(\d+)u-\((\d+)v([+-])(\d+)w\)',request)
   p,qq,c=int(m[1]),int(m[2]),int(m[4]);sgn=1 if m[3]=='+' else -1
   assert initial==[env['u'],env['v'],env['w']],'individual substituted nested vectors'
   assert vector_nodes(rs[2])==[p*env['u'],qq*env['v'],c*env['w']],'individual evaluated vector terms'
   inner=qq*env['v']+sgn*c*env['w']
   assert vector_nodes(rs[3])==[p*env['u'],inner],'individual inner reduction'
   component_operands(rs[4],p*env['u'],inner,'-')

  # Individually distributed/evaluated terms are read and checked, not only final vectors.
  # At product rows compare complete component token trees to prompt-derived product values.
  if t in ('scalar','linear_combination','nested_combination'):
   productrow=rs[1]
   observed=[(int(a) if t=='scalar' else abs(int(a)))*int(b) for a,b in re.findall(r'(\(?-?\d+\)?)\\cdot\s*(\(?-?\d+\)?)',productrow) for a,b in [(a.strip('()'),b.strip('()'))]]
   if t=='scalar':n=int(re.match(r'(-?\d+)v',request)[1]);expected=[n*int(x) for x in env['v']]
   elif t=='linear_combination':
    m=re.fullmatch(r'(\d+)u([+-])(\d+)v',request);expected=[int(m[1])*int(env['u'][0]),int(m[3])*int(env['v'][0]),int(m[1])*int(env['u'][1]),int(m[3])*int(env['v'][1])]
   else:
    m=re.fullmatch(r'(\d+)u-\((\d+)v([+-])(\d+)w\)',request);expected=[int(m[k])*int(env[v][i]) for i in range(2) for k,v in [(1,'u'),(2,'v'),(4,'w')]]
   assert observed==expected,('individual component products',observed,expected)
 fields=q.get(':question/answer-fields',[])
 for f in fields:
  assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
  values=[evaluate(a[':answer/value'],{}) for a in f[':answer-field/choices']]
  assert len(values)==5 and len({tuple(v) for v in values})==5,'bank collisions'
  assert Counter(tuple(v) for v in values)==Counter(tuple(v) for v in independent_bank(r,env,request,z)),'complete displayed operation bank'
  assert sum(v==z for v in values)==1,'unique correct value'
  if ':answer-field/correct' in f:
   correct=f[':answer-field/correct'];assert correct[0]==':answer/id'
   a=next(x for x in f[':answer-field/choices'] if x[':answer/id']==correct[1]);assert evaluate(a[':answer/value'],{})==z
  assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
  for a in f[':answer-field/choices']:check_format(a[':answer/value'])
 return len(rs)
def fidelity(r,source):
 q=r['question'];assert set(q)==set(source),'raw question key-presence parity'
 for key in (':question/problem',':question/worked-solution'):
  assert q.get(key)==source.get(key),(key,q.get(key),source.get(key))
 assert q.get(':question/difficulty')==(source.get(':question/difficulty') or {}).get(':db/ident')
 assert len(q.get(':question/answer-fields',[]))==len(source.get(':question/answer-fields',[]))
 for f,sf in zip(q.get(':question/answer-fields',[]),source.get(':question/answer-fields',[])):
  assert set(f)==set(sf),'raw field presence parity'
  assert f[':answer-field/key']==sf[':answer-field/key']
  assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
  vals=sorted(a[':answer/value'] for a in f[':answer-field/choices']);sv=sorted(a[':answer/value'] for a in sf[':answer-field/choices']);assert vals==sv
  if ':answer-field/correct' in sf:
   selected=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
   assert evaluate(selected[':answer/value'],{})==evaluate(sf[':answer-field/correct'][':answer/value'],{}),'correct designation value match'
  for a in f[':answer-field/choices']:
   sa=next(sa for sa in sf[':answer-field/choices'] if a[':answer/value']==sa[':answer/value']);assert set(a)==set(sa),'raw answer presence parity'
   assert a[':answer/type']==sa[':answer/type'][':db/ident']


def native_engine():
 # Existing generic harness; memory-only fixtures, no recompilation or shared edits.
 return REPO/'generate/runs/current/check-engine'

def independent_inventory():
 rows=[]
 for sid,(t,p) in g.INVENTORY_CASES.items():
  family='two-component sum' if t.startswith('sum') else 'two-component scalar multiplication'
  rows.append({'record':g.QS[sid],'role':'independently authored inventory','relationship_to_source_templates':f'Matches the {family} arrow-notation mask with changed signed integer coordinates; adds a complete authored five-choice radio bank and correct reference. It is current inventory, not an original MA template or original difficulty evidence.','source_id':sid,'template':t,'parameters':p,'bank_profile':'raw-'+sid})
 inventory={**{k:g.SOURCE[k] for k in ('database','basis','lineage')},'questions':rows}
 write('independent-inventory.json',inventory)
 captured=[q for q in g.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
 assert sorted((r['record'] for r in rows),key=lambda r:r[':db/id'])==sorted(captured,key=lambda r:r[':db/id']),'exact independent inventory coverage'
 return inventory

def capacity():
 # Independent integer-pair enumeration for the small easy domains.
 vals=range(-9,10);counts=Counter();sumtasks=set();subtasks=set();scalartasks=set()
 for ax in vals:
  for ay in vals:
   for bx in vals:
    for by in vals:
     bank=[(ax+bx,ay+by),(ax-bx,ay-by),(bx-ax,by-ay),(ax+bx,ay-by),(ax-bx,ay+by)]
     if len(set(bank))==5:
      counts['sum_valid_parameter_sets']+=1;sumtasks.add(tuple(sorted(((ax,ay),(bx,by)))))
     bank=[(ax-bx,ay-by),(ax+bx,ay+by),(bx-ax,by-ay),(ax-bx,ay+by),(ax+bx,ay-by)]
     if len(set(bank))==5:
      counts['subtraction_valid_parameter_sets']+=1;subtasks.add((ax,ay,bx,by))
   for n in (-6,-5,-4,-3,-2,2,3,4,5,6):
    bank=[(n*ax,n*ay),(-n*ax,-n*ay),(ax+n,ay+n),(-n*ax,n*ay),(-ax-n,-ay-n)]
    if len(set(bank))==5:counts['scalar_valid_parameter_sets']+=1;scalartasks.add((n*ax,n*ay))
 counts.update(sum_unique_mathematical_tasks=len(sumtasks),subtraction_unique_mathematical_tasks=len(subtasks),scalar_unique_mathematical_tasks=len(scalartasks))
 witnesses={};coverage={}
 for level,t in [('moderate','linear_combination'),('hard','nested_combination')]:
  tasks={};signs=Counter();domains={}
  for seed in range(1600):
   r=g.generate(level,seed,template=t);p=r['generation']['parameters'];tasks.setdefault(r['generation']['mathematical_fingerprint'],p);signs[p['s']]+=1
   for k,v in p.items():domains.setdefault(k,set()).update(v if isinstance(v,list) else [v])
  assert len(tasks)>=1500,'same-method capacity witnesses'
  witnesses[level]={'template':t,'distinct_valid_mathematical_task_count':len(tasks),'witness_parameters':list(tasks.values())}
  coverage[level]={'sampled_signs':dict(signs),'slot_values':{k:sorted(v) for k,v in domains.items()}}
  assert set(signs)=={-1,1}
  assert domains['p']==set(range(2,7 if level=='moderate' else 5))
  for k in ('a','b')+ (('c',) if level=='hard' else ()):
   assert domains[k]==set(range(-6,0))|set(range(1,7))
 write('capacity-witnesses.json',witnesses)
 return {'easy_exact_finite_enumeration':dict(counts),'moderate_valid_task_lower_bound':witnesses['moderate']['distinct_valid_mathematical_task_count'],'hard_valid_task_lower_bound':witnesses['hard']['distinct_valid_mathematical_task_count'],'unfiltered_parameter_domain_sizes':{'sum_or_subtraction':19**4,'scalar':19**2*10,'moderate':12**4*25*2,'hard':12**6*27*2},'authored_slot_coverage':coverage,'note':'Exact easy counts and explicitly witnessed moderate/hard lower bounds; unfiltered domains are not claimed valid-bank counts. Name/profile/order aliases do not count.'}

def main():
 assert g.SOURCE['basis']==2275 and len(g.QS)==9
 raw_ma={sid:q for sid,q in g.QS.items() if ':question/math-academy-id' in q}
 assert set(raw_ma)=={'q-1300','q-1324','q-1323','q-1386'}
 cases=[{'source_id':sid,'template':g.SOURCE_TEMPLATE[sid],'parameters':g.SOURCE_PARAMS[sid],'bank_profile':'raw-'+sid,'level':'easy','level_assignment':'observed MA easy' if ':question/difficulty' in g.QS[sid] else 'authored one-operation easy; raw difficulty omitted'} for sid in raw_ma]
 write('source-cases.json',cases)
 inventory=independent_inventory()
 raws=[];completed=[];inventory_replays=[]
 for case in cases:
  r=g.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check_record(r);fidelity(r,g.QS[case['source_id']]);raws.append(r)
  n=g.generate('easy',template=case['template'],parameters=case['parameters']);check_record(n);completed.append(n)
 for sid,(t,p) in g.INVENTORY_CASES.items():
  r=g.generate('easy',template=t,parameters=p,profile='raw-'+sid);check_record(r);fidelity(r,g.QS[sid]);inventory_replays.append(r)
 write('raw-replay.json',raws);write('independent-replay.json',inventory_replays)
 records=[];counts=Counter();stages=0;tasks={l:set() for l in g.SUPPORTED_LEVELS}
 for t,level in g.TEMPLATES.items():
  for seed in range(200):
   r=g.generate(level,seed,template=t);stages+=check_record(r);counts[t]+=1;tasks[level].add(r['generation']['mathematical_fingerprint']);records.append(r)
   assert r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
   other=g.generate(level,seed+1,template=t,parameters=r['generation']['parameters'],profile=r['generation']['profile'])
   assert other['question'][':question/id']==r['question'][':question/id'],'seed/order changes identity'
   assert other['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
 for level in g.SUPPORTED_LEVELS:
  expected={t for t,l in g.TEMPLATES.items() if l==level}
  assert {g.generate(level,s)['generation']['template'] for s in range(400)}==expected,'default family coverage'
 invalid=[('moderate','linear_combination',{'a':[1,1],'b':[1,2],'p':1,'q':2,'s':1}),('moderate','linear_combination',{'a':[0,1],'b':[1,2],'p':2,'q':2,'s':1}),('hard','nested_combination',{'a':[1,1],'b':[1,2],'c':[2,3],'p':5,'q':2,'r':2,'s':1}),('easy','sum_lower',{'a':[0,0],'b':[0,0]}),('easy','scalar',{'a':[1,0],'p':3}),('easy','subtract',{'a':[10,1],'b':[1,1]}),('easy','scalar',{'a':[1,2],'p':1}),('hard','nested_combination',{'a':[1,1],'b':[1,2],'c':[2,0],'p':2,'q':2,'r':2,'s':1}),('moderate','linear_combination',{'a':[1,1],'b':[1,2],'p':2,'q':-3,'s':1})]
 for l,t,p in invalid:
  try:g.generate(l,template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('explicit invalid input accepted',l,t,p))
 boundaries=[('easy','scalar',{'a':[-9,8],'p':-6}),('moderate','linear_combination',{'a':[6,-5],'b':[-4,6],'p':6,'q':5,'s':-1}),('hard','nested_combination',{'a':[6,-5],'b':[-4,6],'c':[5,-6],'p':4,'q':3,'r':4,'s':1})]
 for l,t,p in boundaries:check_record(g.generate(l,template=t,parameters=p))
 for sid in g.QS:
  for seed in range(50):
   r=g.generate('easy',seed,template=g.SOURCE_TEMPLATE[sid],profile='raw-'+sid);check_record(r)
   assert set(r['question'])==set(g.QS[sid])
   assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
   for f,sf in zip(r['question'].get(':question/answer-fields',[]),g.QS[sid].get(':question/answer-fields',[])):
    assert set(f)==set(sf) and all(set(a)==set(sf[':answer-field/choices'][0]) for a in f[':answer-field/choices'])
 # Name/order/factor alias checks and changed-coordinate identity.
 pa={'a':[-3,1],'b':[4,6]}
 lo=g.generate_easy(template='sum_lower',parameters=pa);up=g.generate_easy(template='sum_upper',parameters=pa)
 check_record(lo);check_record(up)
 assert lo['question'][':question/id']==up['question'][':question/id'],'cosmetic case affects content identity'
 assert lo['generation']['mathematical_fingerprint']==up['generation']['mathematical_fingerprint']
 swapped=g.generate_easy(template='sum_lower',parameters={'a':pa['b'],'b':pa['a']});check_record(swapped)
 assert swapped['generation']['mathematical_fingerprint']==lo['generation']['mathematical_fingerprint']
 sa=g.generate_easy(template='scalar',parameters={'a':[2,-4],'p':6});sb=g.generate_easy(template='scalar',parameters={'a':[4,-8],'p':3})
 check_record(sa);check_record(sb);assert sa['generation']['mathematical_fingerprint']==sb['generation']['mathematical_fingerprint']
 changed=g.generate_easy(template='sum_lower',parameters={'a':[-2,1],'b':[4,6]});check_record(changed)
 assert changed['question'][':question/id']!=lo['question'][':question/id']
 hard=g.generate_hard(parameters={'a':[2,-3],'b':[4,5],'c':[-2,3],'p':2,'q':3,'r':4,'s':-1})
 mutations=[]
 bad=copy.deepcopy(lo);bad['question'][':question/problem']=bad['question'][':question/problem'].replace('⟨-3,1⟩','⟨-2,1⟩');mutations.append(bad)
 bad=copy.deepcopy(lo);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('⟨-3+4,1+6⟩','⟨-2+3,1+6⟩');mutations.append(bad)
 bad=copy.deepcopy(lo);f=bad['question'][':question/answer-fields'][0];f[':answer-field/choices'][0][':answer/value']=f[':answer-field/choices'][1][':answer/value'];mutations.append(bad)
 bad=copy.deepcopy(lo);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('⟨1,7⟩','⟨2,7⟩');mutations.append(bad)
 bad=copy.deepcopy(hard);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('3\\cdot 4-4\\cdot (-2)','3\\cdot 4+4\\cdot (-2)');mutations.append(bad)
 bad=copy.deepcopy(hard);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('⟨4,-6⟩-(⟨12,15⟩','⟨5,-6⟩-(⟨13,15⟩');mutations.append(bad)
 bad=copy.deepcopy(sa);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(r'6\cdot 2',r'6\cdot 3');mutations.append(bad)
 bad=copy.deepcopy(lo);bad['question'][':question/worked-solution']='\x0c'+bad['question'][':question/worked-solution'];mutations.append(bad)
 for bad in mutations:
  try:check_record(bad)
  except AssertionError:pass
  else:raise AssertionError('mutation survived displayed-math checks')
 capacity_report=capacity();write('capacity.json',capacity_report)
 fixtures=[]
 for i,r in enumerate(completed+inventory_replays+records):
  f=r['question'][':question/answer-fields'][0]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independently verified complete displayed vector choice'} for a in f[':answer-field/choices']]
  fixtures.append({'label':str(i),'record':r,'checks':checks})
 write('native-input.json',fixtures);engine=native_engine()
 subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 native=json.loads((D/'native-report.json').read_text());assert native['accepted_checks']==len(fixtures) and native['rejected_checks']==4*len(fixtures) and native['documented_unresolved_checks']==0
 reviews=[g.generate(l,seed,template=t) for t,l in g.TEMPLATES.items() for seed in (27,83)]
 for sid in ('q-1323','q-1386'):reviews.append(g.generate_easy(91,template=g.SOURCE_TEMPLATE[sid],profile='raw-'+sid))
 write('review.json',reviews)
 review=['# Basis-2275 original evidence, inventory and draft variants','', 'Raw originals retain omissions. Completed versions infer missing fields/refs/solutions. Moderate and hard are explicitly authored levels; independent inventory is not MA-source evidence.']
 for case,r,n in zip(cases,raws,completed):review.extend(['\n## Original MA '+case['source_id']+' — exact raw replay',g.markdown(r),'\n### Completed learning version — authored repairs where missing',g.markdown(n)])
 for sid,r in zip(g.INVENTORY_CASES,inventory_replays):review.extend(['\n## Independent inventory '+sid+' — exact public replay',g.markdown(r)])
 for r in reviews:review.extend(['\n## Generated '+r['generation']['level']+' / '+r['generation']['template']+' / '+r['generation']['profile'],g.markdown(r)])
 (D/'review.md').write_text('\n'.join(review)+'\n')
 before=json.loads((D/'baseline-hashes.json').read_text())
 assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in before.items()),'registered baseline or its evidence changed'
 result={'status':'pass','source_provenance':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':importlib.metadata.version('matplotlib')},'original_MA_fidelity':{'sources':4,'prompts_exact':4,'question_attribute_presence_exact':4,'complete_banks_matched':2,'complete_banks_total':2,'displayed_values_matched':10,'displayed_values_total':10,'distractors_matched':8,'distractors_total':8,'worked_solutions_exact':2,'worked_solutions_available':2,'correct_designations_matched':0,'correct_designations_available':0,'missing_correct_designations':2,'fieldless_sources':2,'raw_gradeable_records':0,'completed_learning_versions':4},'independent_inventory':{'exact_captured_records':5,'prompts_exact':5,'worked_solutions_exact':5,'complete_banks_matched':5,'values_matched':25,'correct_designations_matched':5,'not_MA_evidence':True},'generated_records':len(records),'per_template':dict(counts),'independent_displayed_solution_stages':stages,'sampled_unique_mathematical_tasks':{k:len(v) for k,v in tasks.items()},'task_capacity':capacity_report,'valid_explicit_boundaries':len(boundaries),'invalid_explicit_rejections':len(invalid),'mutation_rejections':len(mutations),'raw_changed_parameter_checks':450,'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((D/'source.json').read_bytes()).hexdigest(),'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'native_harness_source_sha256':hashlib.sha256((engine.parent/'check-engine.rs').read_bytes()).hexdigest(),'registered_baseline_unchanged':True,'supported_levels':list(g.SUPPORTED_LEVELS),'evidence_limits':['No observed MA moderate/hard labels; both are authored bounded same-method backbones requested for missing levels.','Original radio questions lack captured correct refs/solutions, and original easy sums are fieldless. Raw replay preserves those omissions.','Opaque q-1323 selector bank is publicly parameterized but evidence-only; normal subtraction uses a separate authored complete operation bank.','The five independent inventory records are exact current inventory and not recovered MA templates or observed difficulty evidence.','The canonical raster is inspected context; all practice questions supply coordinates directly, with plot rating none.']}
 write('validation.json',result);print(json.dumps({k:v for k,v in result.items() if k!='task_capacity'},indent=2))

if __name__=='__main__':main()
