"""Prompt-blind modal-component attack on the revised quotient banks.
No prompt, generation parameters, stored key or worked solution is read by choose().
Run after delivery: PYTHONDONTWRITEBYTECODE=1 <context python> bank_shortcut.py
The script exits 1 if the new structural bypass is demonstrated.
"""
import json,pathlib,sys,re,collections
R=pathlib.Path(__file__).resolve().parent
D=r'\frac{\text{d}y}{\text{d}x}'
def choose(choices):
 # Only visible answer strings: repeated y powers and repeated right sides.
 texts=[c[':answer/value'].replace(D,'D') for c in choices]
 powers=collections.Counter()
 for text in texts:
  for match in re.finditer(r'\{y\}\^\{([1-4])\}|(?<![A-Za-z])y(?![A-Za-z])',text):powers[int(match[1]) if match[1] else 1]+=1
 if not powers:return None
 n=powers.most_common(1)[0][0];rhs=collections.Counter(t.split('=')[1] for t in texts).most_common(1)[0][0]
 yn='y' if n==1 else '{y}^{'+str(n)+'}'
 wanted=yn+r'\cdot D='+rhs
 found=[i for i,t in enumerate(texts) if t==wanted]
 return found[0] if len(found)==1 else None

def probe(r):
 f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];idx=choose(cs);key=f[':answer-field/correct'];key=key[':answer/id'] if isinstance(key,dict) else key[1]
 return {'question_id':r['question'][':question/id'],'template':r.get('generation',{}).get('template'),'bank_profile':r.get('generation',{}).get('bank_profile'),'chosen_index':idx,'chosen_value':cs[idx][':answer/value'] if idx is not None else None,'correct':idx is not None and cs[idx][':answer/id']==key}

def power_sign_shortest(cs):
 # Independent simpler attack specific to the recognizable no-reciprocal bank.
 rows=[c[':answer/value'].replace(D,'D') for c in cs];left=collections.Counter(t.split('=')[0] for t in rows);mode,count=left.most_common(1)[0]
 if count!=3:return None
 cand=[i for i,t in enumerate(rows) if t.split('=')[0]==mode];best=min(len(rows[i]) for i in cand);w=[i for i in cand if len(rows[i])==best]
 return w[0] if len(w)==1 else None

if __name__=='__main__':
 pools={n:json.load(open(R/p)) for n,p in [('focused','revision-records.json'),('batch','batch.json'),('accepted_batch','delivery-batch/accepted.json'),('accepted_control','delivery-control/accepted.json')]}
 results={};summary={};simple=[]
 for name,rs in pools.items():
  sub=[r for r in rs if r.get('generation',{}).get('template') in ['simple_quotient','exp_quotient']];results[name]=[probe(r) for r in sub];summary[name]={}
  for t in ['simple_quotient','exp_quotient']:
   for profile in ['quotient-reciprocal','quotient-power-sign']:
    z=[p for p in results[name] if p['template']==t and p['bank_profile']==profile]
    if z:summary[name][t+'/'+profile]={'correct':sum(p['correct'] for p in z),'total':len(z)}
  for r in sub:
   if r['generation']['bank_profile']=='quotient-power-sign':
    f=r['question'][':question/answer-fields'][0];idx=power_sign_shortest(f[':answer-field/choices']);simple.append({'pool':name,'question_id':r['question'][':question/id'],'chosen_index':idx,'correct':idx is not None and f[':answer-field/choices'][idx][':answer/id']==f[':answer-field/correct'][1]})
 out={'strategy':'Hide ODE; count visible y powers (outside dy/dx); take most common exponent and most common RHS; select row whose bare y-power coefficient and RHS match those modes. No equation is factored or checked against the ODE.','baseline':0.2,'pools':results,'summary':summary,'simpler_power_sign_attack':{'strategy':'Choose shortest among the three rows with identical derivative-side coefficient.','cases':simple}}
 (R/'bank-shortcut-results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
 minimal=next(r for r in pools['focused'] if r['generation']['template']=='simple_quotient' and r['generation']['parameters']=={'n':1} and r['generation']['bank_profile']=='quotient-power-sign' and r['generation']['seed']==17)
 (R/'minimal-failing-record.json').write_text(json.dumps([minimal],indent=2,ensure_ascii=False))
 print(json.dumps(summary));print('simpler power/sign:',sum(p['correct'] for p in simple),'/',len(simple))
 if any(z['correct'] for z in results['focused']):raise SystemExit('FAIL: revised quotient construction exposes a prompt-blind modal-component key')
