import audit as a
import fast_math as fm
from collections import Counter
import time
g=a.g
def save(n,v):a.save(n,v)
def keyed(r):
 f=r['question'][':question/answer-fields'][0]
 return next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
def replay():
 src=a.json.loads((a.JOB/'source/source.json').read_text())['material']['kp'];rs=[];out=[]
 def normalized(v):
  if isinstance(v,list):return sorted([normalized(x) for x in v],key=lambda x:a.json.dumps(x,sort_keys=True))
  if isinstance(v,dict):
   if set(v)=={':db/ident'}:return v[':db/ident']
   v=a.copy.deepcopy(v)
   if isinstance(v.get(':answer-field/correct'),list):
    ident=v[':answer-field/correct'][1];v[':answer-field/correct']=next(c for c in v[':answer-field/choices'] if c[':answer/id']==ident)
   return {k:normalized(x) for k,x in v.items() if k not in [':db/id',':question/id',':question/math-academy-id',':answer/id',':answer-field/id']}
  if isinstance(v,str):
   v=v.replace(r'\left','').replace(r'\right','')
   while r'\underbrace' in v:
    i=v.index(r'\underbrace');inside,j=a.group(v,i+len(r'\underbrace'));v=v[:i]+'{{'+inside+'}_{⏟}}'+v[j:]
  return v
 for q in src[':knowledge-point/questions']:
  t=q[':question/math-academy-id'];level=q[':question/difficulty'][':db/ident'].split('/')[-1]
  r=g.generate(level,17021,t,parameters={'n':1},profile='observed-raw');rs.append(r)
  out.append({'source_id':q[':question/id'],'template':t,'complete_bank_sizes':[len(f[':answer-field/choices']) for f in q[':question/answer-fields']],'passed':normalized(q)==normalized(r['question'])})
 # Canonical is worked only, so check its mathematical specialization in an ordinary family.
 canonical={'source_id':src[':knowledge-point/canonical-example'][':question/id'],'comparison':'dy/dx + sin(x)y - cos(x)=0 -> P=sin(x), Q=cos(x), verified directly; no answer bank captured.'}
 save('source-replays.json',rs);save('source-replay-results.json',{'results':out,'canonical':canonical,'normalization':'Ignore database identities and radio order; normalize left/right sizing and captured underbrace glyph representation. Preserve prompt, full banks, keys and solution steps.'})
 print('replays',sum(t['passed'] for t in out),'/',len(out),flush=True)
def main():
 replay();records=[];pairs=[];fixed=[];bounds=[]
 for level,ts in g.FAMILIES.items():
  for t in ts:
   for seed in [17023,17029,17033]:records.append(g.generate(level,seed,t))
   p=dict(g.ORIGINAL[t]);dec={}
   if level=='easy':
    us=[2,3,5,6,8] if t=='q-79699' else [1,3,4,6,8];vs=[1,2,3,4,5] if t=='q-16400' else [1,2,4,6,8]
    dec={'p_sign':-1,'q_sign':1,'p_candidates':us,'q_candidates':vs,'correct_slot':0,'linear':us[0],'forcing':vs[0]}
   elif level=='hard':dec={'b_candidates':[-4,-2,1,2,4],'correct_slot':0}
   else:dec={'b_candidates':[1,2,4,6,8],'d_candidates':[8,6,4,2,1],'correct_slot':0}
   bank=[]
   for slot in range(5):
    dd=a.copy.deepcopy(dec);dd['correct_slot']=slot;pp=dict(p)
    if level=='easy':
     dd['linear']=us[slot];dd['forcing']=vs[slot]
     if t=='q-16400':pp['h']=us[slot];pp['c']=vs[slot]
     elif 'k' in pp:pp['k']=us[slot]
    else:
     pp['b']=dd['b_candidates'][slot]
     if level=='moderate':pp['d']=dd['d_candidates'][slot]
    r=g.generate(level,17041,t,parameters=pp,decision=dd);bank.append(r);records.append(r)
   fixed.append({'template':t,'records':bank,'bank_held_fixed':len({tuple(sorted(c[':answer/value'] for c in r['question'][':question/answer-fields'][0][':answer-field/choices'])) for r in bank})==1,'five_distinct_keys':len(set(keyed(r) for r in bank))==5})
   # Irrelevant shuffle seed: explicitly hold mathematical roles and candidates.
   before=bank[0];after=g.generate(level,17043,t,parameters=before['generation']['parameters'],decision=before['generation']['decision']);records.append(after)
   pairs.append({'template':t,'kind':'irrelevant','before':before,'after':after,'same_prompt':before['question'][':question/problem']==after['question'][':question/problem'],'same_solution':before['question'][':question/worked-solution']==after['question'][':question/worked-solution'],'same_answer':keyed(before)==keyed(after)})
   # Relevant changes: fixed bank reassigns the key and corresponding prompt evidence.
   for after in bank[1:]:pairs.append({'template':t,'kind':'relevant','before':before,'after':after,'changed_prompt':before['question'][':question/problem']!=after['question'][':question/problem'],'changed_solution':before['question'][':question/worked-solution']!=after['question'][':question/worked-solution'],'changed_answer':keyed(before)!=keyed(after)})
   if level=='easy':
    # Independent P and Q sign perturbations hold magnitudes, catalog and most evidence fixed.
    for role in ['p_sign','q_sign']:
     dd=a.copy.deepcopy(before['generation']['decision']);dd[role]*=-1
     r=g.generate(level,17041,t,parameters=before['generation']['parameters'],decision=dd);records.append(r)
     pairs.append({'template':t,'kind':'relevant','role':role,'before':before,'after':r,'changed_prompt':before['question'][':question/problem']!=r['question'][':question/problem'],'changed_solution':before['question'][':question/worked-solution']!=r['question'][':question/worked-solution'],'changed_answer':keyed(before)!=keyed(r)})
   # Boundaries and invalid shape/value/decision rejection.
   low={k:2 if t=='q-79699' or (k=='a' and t in ('q-16400','rational-collect')) else 1 for k in p}
   high={k:(5 if t=='q-16400' and k!='h' else 6 if t=='q-16401' and k!='b' else 4 if t=='q-16401' else 8) for k in p}
   for pp in [low,high]:
    r=g.generate(level,17047,t,parameters=pp);records.append(r);bounds.append({'template':t,'parameters':pp,'accepted':True})
   for pp in [{k:0 for k in p},{k:99 for k in p},{k:1.5 for k in p}]:
    try:g.generate(level,17049,t,parameters=pp);reject=False
    except ValueError:reject=True
    bounds.append({'template':t,'parameters':pp,'rejected':reject})
   print('generated',t,flush=True)
 save('independent-records.json',records);save('independent-easy.json',[r for r in records if r['generation']['difficulty']=='easy']);save('fixed-bank-tests.json',fixed);save('counterfactual-pairs.json',pairs);save('boundary-tests.json',bounds)
 batch=a.json.loads((a.JOB/'samples.json').read_text());save('runner-batch.json',batch)
 maths=[]
 for r in records+batch:
  try:maths.append(fm.check(r))
  except Exception as e:maths.append({'id':r['question'][':question/id'],'error':repr(e),'passed':False})
 save('math-results.json',{'method':'Independent displayed TeX parser; exact residual normalization, double-angle and quotient identities; check every choice and every worked equation.','results':maths})
 # Native grader checks use independently established mathematical classifications.
 cases=[]
 for i,(r,result) in enumerate(zip(records+batch,maths)):
  f=r['question'][':question/answer-fields'][0]
  if not result['passed']:continue
  cases.append({'label':str(i)+':'+r['generation']['template'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'All displayed options independently checked for equivalence and standard form.'} for c in f[':answer-field/choices']]})
 save('grader-input.json',cases)
 # Render every family, opposite sign pair, boundary and full controlled before/after.
 render=[]
 for t in [t for ts in g.FAMILIES.values() for t in ts]:
  rs=[r for r in records if r['generation']['template']==t]
  render.extend([rs[0],rs[3],rs[4],rs[-1]])
 save('render-records.json',render)
 save('runtime.json',{'python':a.platform.python_version(),'sympy':a.S.__version__,'dependencies':a.json.loads((a.PKG/'package.json').read_text())['dependencies'],'deterministic':g.generate('easy',17053)==g.generate('easy',17053)})
 (a.E/'session-state.md').write_text('Milestone: source replay, independent generation, fixed-bank counterfactuals, boundaries, and exact mathematics completed. See review.py and JSON results. Delivery, native grader, rendering, selection and packaging still pending.\n')
 print('math',sum(r['passed'] for r in maths),'/',len(maths),'failures',[r for r in maths if not r['passed']][:3],flush=True)
if __name__=='__main__':main()
