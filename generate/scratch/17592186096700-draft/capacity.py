"""Exhaust finite support; count actual equations modulo mathematical aliases."""
import importlib.util,itertools,json,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('draft96700_capacity',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
counts={};keysets={};representatives={};rawcounts={};all_reps=[]
for level in ('easy','moderate','hard'):
 keys=set();simple_seen=set();raw=0;reps=[]
 for template in (g.TEMPLATES[:1] if level=='easy' else g.TEMPLATES):
  ds=[(1,0),(0,1),(1,1),(1,-1),(-1,0),(0,-1),(-1,-1),(-1,1)]
  dirs=[(1,2),(2,1),(1,-2),(2,-1),(-1,2),(-2,1),(-1,-2),(-2,-1),(2,3),(3,2),(2,-3),(3,-2),(-2,3),(-3,2),(-2,-3),(-3,-2)]
  ks=['1'] if level=='easy' else ['2'] if level=='moderate' else ['3/2','2/3']
  us=[[2*x for x in d] for d in ds] if level=='easy' else dirs if level=='moderate' else None
  vs=[[2*x for x in d] for d in ds] if level=='easy' else dirs+[(2,5),(5,2),(-3,-5),(3,5),(0,3),(3,0)]
  primaries=[['b','e'],['a','e']] if template==g.TEMPLATES[0] else [['a','c'],['c','a']]
  secondaries=[['c','d'],['d','c']] if template==g.TEMPLATES[0] else [['b','d'],['d','b']]
  for k in ks:
   ul=us if us else [[(2 if k=='3/2' else 3)*x for x in d] for d in dirs[:8]]
   for u,v,s,t,primary,secondary in itertools.product(ul,vs,(-1,1),(-1,1),primaries,secondaries):
    params=dict(u=u,v=v,k=k,s=s,t=t,targets={'primary':primary,'secondary':secondary})
    try:p=g.normalize_parameters(level,template,params)
    except ValueError:continue
    raw+=1
    # Cheap prequotient exactly preserves every relevant sign/ratio/geometry.
    a,b=g.primitive(p['u']),g.primitive(p['v']);orient=[]
    for swap,sx,sy in itertools.product((False,True),(-1,1),(-1,1)):
     def tr(w):
      x,y=w[::-1] if swap else w
      return (sx*x,sy*y)
     orient.append((tr(a),tr(b)))
    effective_s=s if template==g.TEMPLATES[1] or primary==['b','e'] else 1
    simple=(template,k,effective_s,t,min(orient))
    if simple in simple_seen:continue
    simple_seen.add(simple)
    key=g.task_key(template,p)
    if key not in keys:reps.append({'template':template,'parameters':g.serialize_parameters(p),'fingerprint':key})
    keys.add(key)
 counts[level]=len(keys);rawcounts[level]=raw;keysets[level]=sorted(keys);representatives[level]=reps
 print(level,len(keys),'raw',raw,flush=True)
(D/'finite-catalog.json').write_text(json.dumps({'counts':counts,'raw_sampler_support_counts':rawcounts,'equivalence':'Exact queried normalized vector relations; equation inversion, target/label aliases, order, translation, unused arrows, per-family common scale and all8D4 symmetries excluded. Distinct difficulty labels do not create new mathematics.','same_mathematics_across_levels':{a+'-'+b:len(set(keysets[a])&set(keysets[b])) for a,b in itertools.combinations(keysets,2)},'fingerprint_sets':keysets},indent=2)+'\n')
(D/'finite-representatives.json').write_text(json.dumps(representatives,indent=2)+'\n')
