import sys,json,pathlib,collections,hashlib,re
sys.dont_write_bytecode=True
from independent_math import *
E=pathlib.Path(__file__).resolve().parent

def dump(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def decision(r):
 M=system(r['question'][':question/problem']);R,piv=M.rref();n=M.cols-1;fc=next(j for j in range(n) if j not in piv)
 key=next(vec(c[':answer/value']) for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r))
 if n==2:return 'rank_one'
 if fc==1:return 'free_y'
 if key[0]==key[1]:return 'equal_coordinates'
 if any(not key[j].has(v[fc]) for j in piv):return 'constant_coordinate'
 if any(key[j].subs(v[fc],0)==0 for j in piv):return 'zero_intercept'
 return 'general'

def features(r):
 cs=field(r)[':answer-field/choices'];vv=[vec(c[':answer/value']) for c in cs];n=len(vv[0]);M=system(r['question'][':question/problem']);piv=M.rref()[1];fc=next(j for j in range(n) if j not in piv);t=v[fc]
 strings=[[a.strip() for a in re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',rawfix(c[':answer/value']),re.S)[1].split(r'\\')] for c in cs]
 counts=[collections.Counter(x[j] for x in strings) for j in range(n)]
 return {'first_position':list(range(5)),'component_singletons':[sum(counts[j][x[j]]==1 for j in range(n)) for x in strings],'component_repetitions':[sum(counts[j][x[j]] for j in range(n)) for x in strings],'negative_slopes':[sum(bool(sp.diff(e,t)<0) for e in x) for x in vv],'first_intercept':[x[0].subs(t,0) for x in vv],'first_slope':[sp.diff(x[0],t) for x in vv],'term_count':[sum(len(sp.Add.make_args(e)) for e in x) for x in vv]}

def summary(rr):
 groups={'overall':rr}
 for template in sorted(set(r['generation']['template'] for r in rr)):groups['template:'+template]=[r for r in rr if r['generation']['template']==template]
 out={}
 for name,rs in groups.items():
  probes={};pos=collections.Counter();role=collections.Counter()
  for r in rs:
   cs=field(r)[':answer-field/choices'];ki=next(i for i,c in enumerate(cs) if c[':answer/id']==correct(r));pos[str(ki+1)]+=1;role[str(r['generation'].get('bank_role'))]+=1
   for feature,scores in features(r).items():
    for direction,extreme in [('min',min(scores)),('max',max(scores))]:
     candidates=[i for i,s in enumerate(scores) if s==extreme]
     if len(candidates)==1:
      p=probes.setdefault(feature+'_'+direction,{'correct':0,'total':0});p['total']+=1;p['correct']+=candidates[0]==ki
   old=shortcut(r)
   if old.get('unique_modes'):
    p=probes.setdefault('old_unique_component_modes',{'correct':0,'total':0});p['total']+=1;p['correct']+=old['correct']
   frac=[i for i,c in enumerate(cs) if '\\frac' in c[':answer/value']]
   if len(frac)==1:
    p=probes.setdefault('unique_fraction',{'correct':0,'total':0});p['total']+=1;p['correct']+=frac[0]==ki
  out[name]={'count':len(rs),'decision_cases':dict(collections.Counter(decision(r) for r in rs)),'key_positions':dict(pos),'bank_roles':dict(role),'probes':probes}
 return out
if __name__=='__main__':
 paths=['batch.json','delivery-batch/accepted.json','fresh.json','delivery-fresh/accepted.json','source-shortcut-records.json','delivery-source-shortcut/accepted.json','cue-control-records.json','delivery-controls/accepted.json']
 measures={p:summary(json.loads((E/p).read_text())) for p in paths};dump('delivery-shortcuts.json',measures)
 print(json.dumps({p:measures[p]['overall'] for p in paths},indent=2))
