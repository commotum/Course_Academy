"""Read visible math independently; no database/service access or runtime writes.
Run from any directory with the job Python, -B checks/validate_repair.py.
"""
import collections,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from witness import vec,system,field,correct,mathcheck,shortcut,sp,v
spec=importlib.util.spec_from_file_location('repair_generator',ROOT/'17592186115241.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
E=ROOT/'evidence';E.mkdir(exist_ok=True)
def dump(name,data):(E/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def check(r):
 result=mathcheck(r)
 assert result['pass'],result
 # The last displayed vector equals the independently solved parametrization.
 M=system(r['question'][':question/problem']);R,piv=M.rref();free=next(j for j in range(M.cols-1) if j not in piv)
 values=list(v[:M.cols-1])
 for i,j in enumerate(piv):values[j]=sp.expand(R[i,-1]-R[i,free]*v[free])
 sol=r['question'][':question/worked-solution'];vectors=[]
 import re
 for m in re.finditer(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',sol,re.S):
  if '&' not in m[0]:
   try:vectors.append(vec(m[0]))
   except Exception:pass
 assert tuple(values) in vectors,(r['question'][':question/id'],'missing final vector',values,vectors)
 return result

def summarize(records):
 by=collections.defaultdict(list)
 for r in records:by[r['generation']['template']].append(r)
 out={}
 for name,rs in by.items():
  pos=collections.Counter();roles=collections.Counter();cue=collections.defaultdict(lambda:[0,0]);freecols=collections.Counter()
  for r in rs:
   cs=field(r)[':answer-field/choices'];key=correct(r);vectors=[vec(c[':answer/value']) for c in cs];M=system(r['question'][':question/problem']);piv=M.rref()[1];fc=next(j for j in range(M.cols-1) if j not in piv)
   freecols[str(fc)]+=1;ki=next(i for i,c in enumerate(cs) if c[':answer/id']==key);pos[str(ki+1)]+=1
   roles[str(r['generation'].get('bank_role'))]+=1
   assert not (shortcut(r).get('unique_modes') and shortcut(r).get('correct')),('modal shortcut',name)
   counts=[collections.Counter(str(x[j]) for x in vectors) for j in range(len(vectors[0]))]
   signatures=[tuple(counts[j][str(x[j])] for j in range(len(x))) for x in vectors]
   # Finite cue rules do not inspect equations or metadata when choosing.
   features={
    'first_position':list(range(5)),
    'component_singletons':[sum(c==1 for c in sig) for sig in signatures],
    'repeated_components':[sum(c>1 for c in sig) for sig in signatures],
    'terms':[sum(len(sp.Add.make_args(a)) for a in x) for x in vectors],
    'negative_slopes':[sum(bool(sp.diff(a,v[fc])<0) for a in x) for x in vectors],
    'first_intercept':[x[0].subs(v[fc],0) for x in vectors],
    'first_slope':[sp.diff(x[0],v[fc]) for x in vectors]}
   for feature,scores in features.items():
    for direction,extreme in [('min',min(scores)),('max',max(scores))]:
     indices=[i for i,s in enumerate(scores) if s==extreme]
     if len(indices)==1:
      tally=cue[feature+'_'+direction];tally[0]+=1;tally[1]+=indices[0]==ki
  out[name]={'count':len(rs),'key_positions':dict(pos),'answer_roles':dict(roles),'free_columns':dict(freecols),'probes':dict(cue)}
 return out

def main():
 source=json.load(open(E/'source-outline.json'))['material']['kp'];replay=[];reports=[];variants=[]
 for q in source[':knowledge-point/questions']:
  profile=q[':question/math-academy-id'];M=system(q[':question/problem']);n=M.cols-1
  r=g.generate_easy(seed=90217,profile=profile,parameters={'scale':1,'offsets':[0]*n});replay.append(r)
  bank=lambda choices:collections.Counter(str(vec(c[':answer/value'])) for c in choices)
  assert bank(field(r)[':answer-field/choices'])==bank(q[':question/answer-fields'][0][':answer-field/choices']),profile
  assert system(r['question'][':question/problem'])==M
  src_key=q[':question/answer-fields'][0].get(':answer-field/correct')
  if src_key:
   original=next(c for c in q[':question/answer-fields'][0][':answer-field/choices'] if c[':answer/id']==(src_key[':answer/id'] if isinstance(src_key,dict) else src_key[-1]))
   generated=next(c for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r))
   assert vec(original[':answer/value'])==vec(generated[':answer/value']),profile
  reports.append({'profile':profile,'source_id':q[':question/id'],'complete_bank':5,'math':check(r)})
  # Changed parameters check the same source compiler, including newer bmatrices.
  changed=g.generate_easy(seed=90218,profile=profile,parameters={'scale':-1,'offsets':[1]*n});check(changed);variants.append(changed)
  ordinary=g.generate_easy(seed=90219,profile=profile);check(ordinary);variants.append(ordinary)
 dump('source-replay-records.json',replay);dump('source-replay.json',reports)
 # The exact canonical source is reached by the alternate free-column path.
 canonical=g.generate_easy(seed=90217,parameters={'free_coefficients':[5,0],'constants':[-1,3],'mix':[1,1],'free_column':1})
 assert system(canonical['question'][':question/problem'])==system(source[':knowledge-point/canonical-example'][':question/problem'])
 check(canonical)
 p={'free_coefficients':[2,-3],'constants':[1,4],'mix':[1,1]}
 special=[g.generate_easy(seed=90217,parameters=pp) for pp in [p,{**p,'free_coefficients':[0,-3]},{**p,'free_coefficients':[2,2],'constants':[1,1]},{**p,'constants':[0,4]},{**p,'free_coefficients':['1/2',-5],'constants':['1/2',-6],'mix':[-2,2]}]]
 for r in special:check(r)
 assert not(shortcut(special[0]).get('unique_modes') and shortcut(special[0]).get('correct'))
 # Independently read math supports exactly the reported boundary cases.
 assert vec(next(c[':answer/value'] for c in field(special[1])[':answer-field/choices'] if c[':answer/id']==correct(special[1])))==(sp.Integer(1),4+3*v[2],v[2])
 assert vec(next(c[':answer/value'] for c in field(special[2])[':answer-field/choices'] if c[':answer/id']==correct(special[2])))==(1-2*v[2],1-2*v[2],v[2])
 zero_constant=g.generate_easy(seed=90217,parameters={**p,'free_coefficients':[0,-3],'constants':[0,4]})
 check(zero_constant)
 assert all(vec(c[':answer/value'])[0]==0 for c in field(zero_constant)[':answer-field/choices'])
 special.append(zero_constant)
 fresh=[g.generate_easy(seed=seed) for seed in range(100,160)]
 for r in fresh:check(r)
 assert {r['generation']['decision_case'] for r in fresh}==set(g.EASY_CASES)
 # Decision-case witnesses from visible equations, rather than trusting metadata.
 cases=set()
 for r in fresh:
  M=system(r['question'][':question/problem']);R,piv=M.rref();n=M.cols-1;fc=next(j for j in range(n) if j not in piv)
  if n==2:cases.add('rank_one');continue
  vv=next(vec(c[':answer/value']) for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r))
  if fc==1:cases.add('free_y')
  elif vv[0]==vv[1]:cases.add('equal_coordinates')
  elif any(not vv[j].has(v[fc]) for j in piv):cases.add('constant_coordinate')
  elif any(vv[j].subs(v[fc],0)==0 for j in piv):cases.add('zero_intercept')
  else:cases.add('general')
 assert cases==set(g.EASY_CASES),cases
 cf=[g.generate_easy(seed=90217,parameters=pp) for pp in [p,{**p,'free_coefficients':[-2,-3]},{**p,'mix':[-1,1]},{**p,'free_coefficients':[2,0],'free_column':1},{**p,'free_coefficients':[2,0]}]]
 for r in cf:check(r)
 keyed=lambda r:next(vec(c[':answer/value']) for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r))
 assert keyed(cf[0])!=keyed(cf[1]) and keyed(cf[0])==keyed(cf[2])
 assert keyed(cf[3])!=keyed(cf[4])
 for r in cf[1:]:
  assert r['question'][':question/problem']!=cf[0]['question'][':question/problem']
  assert r['question'][':question/worked-solution']!=cf[0]['question'][':question/worked-solution']
 # Smoke-check retained moderate/hard banks with the exact historical parameter sets.
 old=json.load(open(E/'generated-records.json'));retained=[]
 for r in old:
  gg=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
  rr=g.generate(level,seed=gg['seed'],parameters=gg['parameters']);check(rr);retained.append(rr)
  assert not(shortcut(rr).get('unique_modes') and shortcut(rr).get('correct'))
 allrecords=replay+variants+[canonical]+special+fresh+cf+retained
 dump('math-results.json',{'count':len(allrecords),'failures':[],'decision_cases_from_visible_math':sorted(cases),'command':'python -B checks/validate_repair.py'})
 dump('fresh.json',fresh);dump('counterfactual-records.json',cf);dump('counterfactual-results.json',{'relevant_changes_answer':keyed(cf[0])!=keyed(cf[1]),'row_mixing_preserves_answer':keyed(cf[0])==keyed(cf[2]),'changed_free_column_changes_answer':keyed(cf[3])!=keyed(cf[4])})
 dump('pedagogical-variation.json',summarize(fresh))
 for name,group in summarize(fresh).items():
  assert len(group['answer_roles'])>1,(name,'fixed answer role')
  assert len(group['key_positions'])>1,(name,'fixed key position')
  for cue,(attempts,hits) in group['probes'].items():
   assert not(attempts>=4 and attempts==hits),(name,cue,'perfect predictor')
 grade=[]
 for i,r in enumerate(allrecords):
  grade.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==correct(r) else 'rejected','purpose':'independent complete-line and key verification'} for c in field(r)[':answer-field/choices']]})
 for i in [1,2]:
  # Relevant changes reject the old vector choice; irrelevant changes preserve
  # selection of the same visible vector using its current field-owned UUID.
  import copy
  r=copy.deepcopy(cf[i]);c=copy.deepcopy(next(c for c in field(cf[0])[':answer-field/choices'] if c[':answer/id']==correct(cf[0])))
  if i==2:c=next(cc for cc in field(r)[':answer-field/choices'] if vec(cc[':answer/value'])==vec(c[':answer/value']))
  else:field(r)[':answer-field/choices'].append(c)
  grade.append({'label':'stale-response-'+str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if i==2 else 'rejected','purpose':'controlled relevant/irrelevant change'}]})
 dump('grader-input.json',grade)
 dump('render-records.json',[next(r for r in fresh if r['generation']['decision_case']==case) for case in g.EASY_CASES]+[replay[-1],canonical,special[-1]])
 dump('samples.json',[g.generate_easy(seed=90217+i) for i in range(5)])
 print(json.dumps({'source_banks':len(reports),'math_records':len(allrecords),'fresh':len(fresh),'decision_cases':sorted(cases),'grader_checks':sum(len(c['checks']) for c in grade)}))
if __name__=='__main__':main()
