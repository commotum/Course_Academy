"""Reject answer-bank cues within a delivered finite batch, preserving all instances.

Only vector components and recognizable template/axis groups enter predictions;
the correct index is consulted solely to score a prediction. Ties abstain.
"""
from collections import Counter
import math

def _unique(xs,rank):
 value=sorted(xs)[rank];ii=[i for i,x in enumerate(xs) if x==value or (math.isfinite(x) and math.isfinite(value) and math.isclose(x,value,rel_tol=1e-12,abs_tol=1e-12))]
 return ii[0] if len(ii)==1 else None

def predictions(vs):
 result={}
 for c in range(3):
  for absolute in [False,True]:
   xs=[abs(v[c]) if absolute else v[c] for v in vs]
   for rank in range(5):result[f'component:{c}:abs:{absolute}:rank:{rank}']=_unique(xs,rank)
  for label,pred in [('positive',lambda x:x>0),('negative',lambda x:x<0),('zero',lambda x:x==0),('unit',lambda x:abs(x)==1),('fraction',lambda x:math.isfinite(x) and x!=int(x))]:
   ii=[i for i,v in enumerate(vs) if pred(v[c])];result[f'unique:{label}:{c}']=ii[0] if len(ii)==1 else None
 norms=[sum(x*x for x in v) for v in vs]
 for rank in range(5):result[f'norm:{rank}']=_unique(norms,rank)
 slopes=[v[2]/(v[0] if v[0]!=0 else v[1]) if (v[0]!=0 or v[1]!=0) else math.inf for v in vs]
 for absolute in [False,True]:
  xs=[abs(x) if absolute else x for x in slopes]
  for rank in range(5):result[f'slope:abs:{absolute}:rank:{rank}']=_unique(xs,rank)
 for sign in [-1,1]:
  ii=[i for i,x in enumerate(slopes) if math.isfinite(x) and x*sign>0 and any(math.isfinite(y) and math.isclose(x,-y,rel_tol=1e-12,abs_tol=1e-12) for y in slopes)]
  result[f'unique:opposite:slope:{sign}']=ii[0] if len(ii)==1 else None
 modes=[]
 for c in range(3):
  counts=Counter(v[c] for v in vs);n=max(counts.values());modes.append({x for x,k in counts.items() if k==n})
 ii=[i for i,v in enumerate(vs) if all(v[c] in modes[c] for c in range(3))];result['modal-intersection']=ii[0] if len(ii)==1 else None
 for pos in range(5):result[f'position:{pos}']=pos
 return result

def failures(items):
 """Items: vectors(float triples), correct(int), template(str), plane(str)."""
 if len(items)<2:return []
 groups={'batch':list(range(len(items)))}
 for feature in ['template','plane']:
  for value in sorted({t[feature] for t in items}):groups[feature+':'+value]=[i for i,t in enumerate(items) if t[feature]==value]
 for family in ['radical','trig','log','exp']:
  groups['visible:'+family]=[i for i,t in enumerate(items) if family in t['template']]
 guessed=[predictions(t['vectors']) for t in items];out=[]
 for name,indices in groups.items():
  if len(indices)<2:continue
  for cue in guessed[indices[0]]:
   if all(guessed[i][cue]==items[i]['correct'] for i in indices):out.append({'subgroup':name,'cue':cue,'indices':indices})
 return out
