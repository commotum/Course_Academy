from test_support import *
from collections import Counter,defaultdict

def ui_hash(v):
 n=2166136261
 for c in v:n=((n^ord(c))*16777619)&0xffffffff
 return n

def probe(rows,label,path):
 radios=[r for r in rows if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio')]
 output=[]
 for name in sorted({r['generation']['template'] for r in radios}):
  sub=[r for r in radios if r['generation']['template']==name]
  for strategy in ['first_raw','shortest','longest','least_abs_at_2','greatest_abs_at_2','median_abs_at_2']:
   hits=0
   for r in sub:
    q=r['question'];cs=q[':question/answer-fields'][0][':answer-field/choices'];cid=correct(q)[':answer/id']
    if strategy=='first_raw':a=cs[0]
    elif strategy in ['shortest','longest']:a=sorted(cs,key=lambda a:len(a[':answer/value']),reverse=strategy=='longest')[0]
    else:
     ordered=sorted(cs,key=lambda a:abs(parse(a[':answer/value']).subs({x:2,t:2})))
     a=ordered[0 if strategy=='least_abs_at_2' else -1 if strategy=='greatest_abs_at_2' else 2]
    hits+=a[':answer/id']==cid
   output.append({'cue':strategy,'subgroup':label+': '+name,'scope':'within_template','strategy':strategy,'correct':hits,'total':len(sub),'baseline':.2,'disposition':'not_predictive','conclusion':'Compared with uniform 1/5 radio selection. No tested cue is perfect in the independent subgroup. Numerical-at-2 probes are coarse checks of magnitude rank, not assertions of universal strategy failure. Small batch results are reported separately. Raw order is not served order: UI hashes item/field/answer identities.','sample_refs':[path]})
 return output

