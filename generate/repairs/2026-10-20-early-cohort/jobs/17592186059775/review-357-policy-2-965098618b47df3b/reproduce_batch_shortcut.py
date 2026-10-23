"""Strict regression: reject the demonstrated shortcut, never repair package files."""
import argparse,sys,json,pathlib,importlib.util,re
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;W=E.parent/'workspace'
sys.path.insert(0,str(W))
s=importlib.util.spec_from_file_location('generator',W/'17592186059775.py')
g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
p=argparse.ArgumentParser();p.add_argument('--input');a=p.parse_args()
rs=json.load(open(a.input)) if a.input else g.batch('easy',5,4258185931)
def matrices(t):
 return g.matrices(t)
hits=0;sub=[]
for r in rs:
 q=r['question'];f=q[':question/answer-fields'][0]
 ordered=sorted(f[':answer-field/choices'],key=lambda a:matrices(a[':answer/value'])[0][1,2])
 # A superficial unit-pivot/template cue. It does not inspect either input RHS.
 pivot=matrices(q[':question/problem'])[0][0,0]
 selected=ordered[3 if pivot==1 else 0]
 hit=selected[':answer/id']==f[':answer-field/correct'][1]
 hits+=hit
 if r['generation']['template']=='q-73439':sub.append(hit)
print(json.dumps({'input':a.input or 'current batch(easy,5,4258185931)','strategy':'if input a11==1 choose second-largest candidate y, else choose smallest','correct':hits,'total':len(rs),'random_baseline':0.2,'q73439_correct':sum(sub),'q73439_total':len(sub)}))
assert hits<len(rs),'Incidental pivot-cue strategy answers every delivered member; revise batch selection.'
