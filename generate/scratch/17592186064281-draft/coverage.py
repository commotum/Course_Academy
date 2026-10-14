"""Per-slot controlled parameter changes, read rendered math independently."""
import importlib.util,json
from pathlib import Path
D=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('v',D/'validate.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v);g=v.g
cases=[]
for key in ('A','a','b'):
 m='authored-affine-sine'
 for value in sorted({p[key] for p in g.parameters_for(m)}):
  p=dict(g.DEFAULTS[m]);p[key]=value;cases.append((m,key,p))
for key in ('a','b'):
 m='q-310179'
 for value in sorted({p[key] for p in g.parameters_for(m)}):
  p={'a':value,'b':-8} if key=='a' else {'a':4 if value<=12 else 1,'b':value};cases.append((m,key,p))
for key in ('a','b'):
 m='q-310182'
 for value in range(1,25):
  p=dict(g.DEFAULTS[m]);p[key]=value;cases.append((m,key,p))
results=[]
for m,key,p in cases:
 r=g.generate(g.LEVELS[m],template=m,parameters=p);read=v.rendered_check(r);read['controlled_slot']=key;results.append(read)
rejected=[]
for m,p in [('q-310179',{'a':24,'b':20}),('q-31241',{'b':2,'c':-20}),('authored-affine-sine',{'A':2,'a':3,'b':0}),('q-31153',{'b':3})]:
 try:g.generate(g.LEVELS[m],template=m,parameters=p)
 except ValueError:rejected.append({'template':m,'parameters':p,'reason':'Outside eligible normal parameter bounds or entire bank collision'})
 else:raise AssertionError('Invalid bounds served')
report={'records':results,'per_slot_coverage':{},'invalid_parameter_negative_controls':rejected,'meaningful_counts':{l:len(g.parameters_for(m)) for l,m in g.DEFAULT_TEMPLATE.items()},'native_excluded_moderate_b_values':[16,17,18,19,20]}
for m,key,p in cases:
 report['per_slot_coverage'].setdefault(m,{}).setdefault(key,[]).append(p[key])
for slots in report['per_slot_coverage'].values():
 for key,vals in slots.items():slots[key]=sorted(set(vals))
(D/'coverage.json').write_text(json.dumps(report,indent=2)+'\n');print('Controlled rendered cases',len(results),'rejected invalid parameters',len(rejected))
