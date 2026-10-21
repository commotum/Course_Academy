"""Independent changed-rule and retained-counterexample audit. All output stays here."""
import sys
sys.dont_write_bytecode=True
import json,pathlib,random,collections,itertools,importlib.util
from fractions import Fraction as F
from audit_math import *
R=pathlib.Path(__file__).resolve().parent;J=R.parent
sys.path.insert(0,str(J/'workspace'));import generator as G
save=lambda n,v:(R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
load=lambda n:json.loads((R/n).read_text())
def visible(r):
 integ,v=extract(r);x=V[v];rows=[]
 for a in field(r)[':answer-field/choices']:
  val=S.expand(tex(a[':answer/value'])-V['C']);c=val.coeff(x);rest=S.simplify(val-c*x)
  rows.append({'id':a[':answer/id'],'linear':F(str(c)),'power':F(str(rest.subs(x,1))),'length':len(a[':answer/value'])})
 return rows,F(str(S.expand(integ).coeff(x,0)))
def strategies(r):
 rows,k=visible(r);cs=collections.Counter(z['linear'] for z in rows);ps=collections.Counter(z['power'] for z in rows)
 matched=[z for z in rows if z['linear']==k]
 d={'range6':[z for z in rows if abs(z['linear'])<=6],
 'eliminate_singleton':[z for z in rows if cs[z['linear']]>1],
 'choose_singleton':[z for z in rows if cs[z['linear']]==1],
 'min_constant':[z for z in rows if abs(z['linear'])==min(abs(t['linear']) for t in rows)],
 'max_constant':[z for z in rows if abs(z['linear'])==max(abs(t['linear']) for t in rows)],
 'shortest':[z for z in rows if z['length']==min(t['length'] for t in rows)],
 'longest':[z for z in rows if z['length']==max(t['length'] for t in rows)],
 'constant_then_max':[z for z in matched if abs(z['power'])==max(abs(t['power']) for t in matched)],
 'constant_then_min':[z for z in matched if abs(z['power'])==min(abs(t['power']) for t in matched)],
 'constant_then_most':[z for z in matched if ps[z['power']]==max(ps[t['power']] for t in matched)],
 'typography':[z for z in matched if abs(z['power']).numerator==1 and abs(z['power']).denominator<10]}
 d.update({'position'+str(j):[rows[j]] for j in range(5)})
 key=answer(r)[':answer/id'];rng=random.Random('independent-ties-'+r['question'][':question/id'])
 # Empty filters fall back to the full constant-matched row.
 return {cue:{'selected':(z:=rng.choice(pool or matched))['id'],'success':z['id']==key,
             'expected_success':float(F(any(a['id']==key for a in (pool or matched)),len(pool or matched))),
             'baseline':1/len(matched) if cue.startswith('constant_') or cue=='typography' else .2}
         for cue,pool in d.items()}
def probe(records):
 trials=[]
 for j,r in enumerate(records):
  if field(r)[':answer-field/type'].endswith('/blank'):continue
  integ,v=extract(r);exponents=[p for (p,) in []] # grouping derives from visible integrand below
  p=next(t.as_powers_dict().get(V[v],S.Integer(0)) for t in S.Add.make_args(integ) if t.has(V[v]))
  profile='R' if p<0 else 'P'
  trials.append({'index':j,'id':r['question'][':question/id'],'profile':profile,'exponent':str(p),'strategies':strategies(r)})
 summary=[]
 for group in ['radio','P','R']+sorted({t['profile']+':'+t['exponent'] for t in trials}):
  ts=[t for t in trials if group=='radio' or group==t['profile'] or group==t['profile']+':'+t['exponent']]
  for cue in ts[0]['strategies'] if ts else []:
   summary.append({'subgroup':group,'cue':cue,'correct':sum(t['strategies'][cue]['success'] for t in ts),'total':len(ts),
     'tie_averaged_rate':sum(t['strategies'][cue]['expected_success'] for t in ts)/len(ts),
     'baseline':sum(t['strategies'][cue]['baseline'] for t in ts)/len(ts)})
 return {'trials':trials,'summary':summary}

