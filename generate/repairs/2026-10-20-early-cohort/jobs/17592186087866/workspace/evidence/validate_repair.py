"""Reproduce the repair checks. Run with the manifest's Python from workspace."""
import copy, importlib.util, json, sys, shutil
from pathlib import Path
from collections import Counter, defaultdict
import math_check as math
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parents[1];E=W/'evidence'
JOB=W.parent;SOURCE=JOB/'source/source.json';INV=JOB/'source/inventory.json'
spec=importlib.util.spec_from_file_location('generator',W/'17592186087866.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,obj): (E/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def key(r):
 f=r['question'][':question/answer-fields'][0]
 return next(v[':answer/value'] for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1])
def presentation(t):
 t=t.replace(r'\left','').replace(r'\right','')
 while r'\underbrace' in t:
  i=t.index(r'\underbrace');v,j=math.group(t,i+len(r'\underbrace'));t=t[:i]+'{{'+v+'}_{⏟}}'+t[j:]
 return t

def source_replay():
 out=[];records=[]
 for q in json.loads(SOURCE.read_text())['material']['kp'][':knowledge-point/questions']:
  t=q[':question/math-academy-id'];level=q[':question/difficulty'][':db/ident'].split('/')[-1]
  r=g.generate(level,9101,t,parameters={'n':1},profile='observed-raw');records.append(r);z=r['question'];fields=[]
  for sf,gf in zip(q[':question/answer-fields'],z[':question/answer-fields']):
   bank=Counter(presentation(v[':answer/value']) for v in sf[':answer-field/choices'])==Counter(v[':answer/value'] for v in gf[':answer-field/choices'])
   sk=sf.get(':answer-field/correct');gk=gf.get(':answer-field/correct')
   keyed=(sk is None and gk is None) or (sk is not None and gk is not None and presentation(sk[':answer/value'])==next(v[':answer/value'] for v in gf[':answer-field/choices'] if v[':answer/id']==gk[1]))
   fields.append({'complete_bank':bank,'correct':bool(keyed),'count':len(gf[':answer-field/choices']),'type':sf[':answer-field/type'][':db/ident']==gf[':answer-field/type']})
  passed=presentation(q[':question/problem'])==z[':question/problem'] and presentation(q[':question/worked-solution'])==z[':question/worked-solution'] and all(f['complete_bank'] and f['correct'] and f['type'] for f in fields) and len(fields)==len(q[':question/answer-fields'])
  out.append({'source_id':q[':question/id'],'template':t,'fields':fields,'passed':passed})
 save('source-replays.json',records);save('source-replay-results.json',out);assert all(v['passed'] for v in out)
 return out

def create_records():
 records=[];pairs=[];boundary=[];render=[]
 for t in g.FAMILIES['easy']:
  for seed in range(6110,6115): records.append(g.generate('easy',seed,t))
  base=copy.deepcopy(g.ORIGINAL[t]);ps=copy.deepcopy(base)
  if t=='q-16400':ps['h']+=1
  elif 'k' in ps:ps['k']+=1
  # Rates are incidental to the coefficient decision; the added linear role
  # supplies a controlled changed P with rate held constant.
  d={'p_sign':1,'q_sign':1,'linear':2 if t=='q-103349' else 1,'forcing':base['c'] if t=='q-16400' else 2 if t=='q-8359' else 1}
  dp=dict(d)
  if t in ('q-103349','q-103354'):dp['linear']+=1
  dq=dict(d,forcing=d['forcing']+1)
  rr=[g.generate('easy',6200,t,parameters=base,decision=d),g.generate('easy',6200,t,parameters=ps,decision=dp),g.generate('easy',6200,t,parameters=base,decision=dq),g.generate('easy',6201,t,parameters=base,decision=d)]
  start=len(records);records.extend(rr);render.extend(rr[:3] if t in ('q-103354','q-79699') else rr[:1])
  ep=[math.equation(key(r)) for r in rr];P=[math.S.expand(e[0]-math.D).coeff(math.y) for e in ep];Q=[e[1] for e in ep]
  checks={'P_change':math.zero(P[0]-P[1])==False,'Q_preserved_for_P_change':math.zero(Q[0]-Q[1]),'Q_change':not math.zero(Q[0]-Q[2]),'P_preserved_for_Q_change':math.zero(P[0]-P[2]),'irrelevant_order_preserves_answer':key(rr[0])==key(rr[3]),'relevant_prompts_changed':rr[0]['question'][':question/problem']!=rr[1]['question'][':question/problem'] and rr[0]['question'][':question/problem']!=rr[2]['question'][':question/problem']}
  pairs.append({'template':t,'record_indices':list(range(start,start+4)),'checks':checks});assert all(checks.values()),pairs[-1]
  # All independent signs, and upper/lower compatible coefficient boundaries.
  for sp,sq in [(-1,-1),(-1,1),(1,-1),(1,1)]:
   p={k:(2 if k=='a' or (t=='q-79699' and k=='k') else 1) for k in base}
   r=g.generate('easy',6300,t,parameters=p,decision={'p_sign':sp,'q_sign':sq,'forcing':1,'linear':1});records.append(r)
   if sp==sq==-1:render.append(r)
  high={k:(5 if t=='q-16400' and k!='h' else 8) for k in base};records.append(g.generate('easy',6301,t,parameters=high,decision={'p_sign':-1,'q_sign':1,'forcing':5 if t=='q-16400' else 8,'linear':8}))
  for bad in ({k:0 for k in base},{k:99 for k in base},{k:1.5 for k in base}):
   try:g.generate('easy',6302,t,parameters=bad);passed=False
   except ValueError:passed=True
   boundary.append({'template':t,'parameters':bad,'rejected':passed});assert passed
 for level in ('moderate','hard'):
  for seed in (6110,6111,6112):records.append(g.generate(level,seed))
  render.append(records[-1])
 for decision in ({'p_sign':0},{'forcing':0},{'linear':9},{'forcing':1.5},{'no_role':1}):
  try:g.generate('easy',6302,'q-8359',parameters={'k':1},decision=decision);passed=False
  except ValueError:passed=True
  boundary.append({'decision':decision,'rejected':passed});assert passed
 save('records.json',records);save('counterfactual-results.json',pairs);save('generation-boundaries.json',boundary);save('render-records.json',render)
 save('easy-records.json',[r for r in records if r['generation']['difficulty']=='easy'])
 return records

def main():
 replay=source_replay();rs=create_records();out=[]
 for i,r in enumerate(rs):
  try:z=math.check(r)
  except Exception as e:z={'index':i,'error':repr(e),'passed':False}
  out.append(z)
 save('math-results.json',out);assert all(v['passed'] for v in out),[v for v in out if not v['passed']][:2]
 # Batch all choices in one native-engine input, deriving expected grades from
 # independently parsed display equations (not from the generator's algebra).
 cases=[]
 for r,z in zip(rs,out):
  cases.append({'label':r['generation']['template']+':'+r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a['choice_id'],'expected':'accepted' if a['standard'] and a['equivalent'] else 'rejected','purpose':'independent displayed standard-form equivalence'} for a in z['choices']]})
 save('grader-input.json',cases)
 print(json.dumps({'replay_banks':sum(len(z['fields']) for z in replay),'source_questions':len(replay),'math_passed':sum(z['passed'] for z in out),'native_cases':sum(len(c['checks']) for c in cases),'render_records':len(json.loads((E/'render-records.json').read_text()))}),flush=True)
if __name__=='__main__':main()
