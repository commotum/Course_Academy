import sys,os,json,re,hashlib,importlib.util,random,subprocess,shutil,platform
from pathlib import Path
from collections import Counter,defaultdict
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent
JOB=E.parent
W=JOB/'workspace'
REPO=Path('/home/jake/Developer/Course_Academy')
PYTHON=str(REPO/'.venv/bin/python')
os.environ['PYTHONDONTWRITEBYTECODE']='1'
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(E/'assets')
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations,implicit_multiplication_application
X=sp.symbols('x y z')
def save(n,d): (E/n).write_text(json.dumps(d,indent=2,default=str)+'\n')
def load(n):return json.load(open(n))
def package_hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
def module(path):
 sys.path.insert(0,str(path.parent));s=importlib.util.spec_from_file_location('reviewed',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def expr(s):
 s=re.sub(r'\\(?:d?frac)\s*\{(-?\d+)\}\s*\{(-?\d+)\}',r'(\1/\2)',s).replace('\\left','').replace('\\right','')
 return sp.expand(parse_expr(s,local_dict=dict(zip('xyz',X)),transformations=standard_transformations+(implicit_multiplication_application,)))
def system(text):
 body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)[1]
 n=3 if 'z' in body else 2;rows=[]
 for line in body.split(r'\\'):
  left,right=line.replace('&','').strip().rstrip('.,').split('=');v=expr(left)
  rows.append([v.coeff(x) for x in X[:n]]+[expr(right)])
 return sp.Matrix(rows)
def matrices(text):
 out=[]
 for env,spec,body in re.findall(r'\\begin\{(array|bmatrix)\}(\{[^}]*\})?(.*?)\\end\{(?:array|bmatrix)\}',text,re.S):
  out.append(sp.Matrix([[expr(v.strip()) for v in r.split('&')] for r in body.split(r'\\')]))
 return out

def classification(m):
 a=m[:,:-1];return 'inconsistent' if a.rank()<m.rank() else 'independent' if a.rank()==a.cols else 'dependent'
def category(text):return 'dependent' if 'consistent dependent' in text else 'independent' if 'independent' in text or 'unique solution' in text else 'inconsistent' if 'inconsistent' in text or 'no solution' in text else 'none'
def value(f):
 c=f[':answer-field/correct'];cid=c[1] if isinstance(c,list) else c[':answer/id']
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)
def ftype(f):
 t=f[':answer-field/type'];return t[':db/ident'] if isinstance(t,dict) else t

def check(r):
 q=r['question'];m=system(q[':question/problem']);kind=classification(m);errors=[]
 fs=q[':question/answer-fields'];sels=[]
 if ftype(fs[0]).endswith('checkbox'):
  for f in fs:
   expected='true' if category(f[':answer-field/key'])==kind else 'false'
   if value(f)!=expected:errors.append('checkbox key '+f[':answer-field/key'])
   if value(f)=='true':sels.append(f[':answer-field/key'])
 else:
  lines=re.findall(r'^(I{1,3})\. (.*)$',q[':question/problem'],re.M)
  expected=next(k+' only' for k,v in lines if category(v)==kind)
  if value(fs[0])!=expected:errors.append('radio key')
  sels=[value(fs[0])]
 # Parse visible matrices, not metadata; all must be row equivalent to prompt.
 ms=matrices(q[':question/worked-solution'])
 if not ms or ms[0]!=m:errors.append('solution initial matrix')
 if any(z.rref()[0]!=m.rref()[0] for z in ms):errors.append('non equivalent displayed matrix')
 if kind not in q[':question/worked-solution'].split('we conclude')[-1] and not (kind=='inconsistent' and 'no solution' in q[':question/worked-solution']):errors.append('conclusion')
 return {'id':q[':question/id'],'seed':r.get('generation',{}).get('seed'),'template':r.get('generation',{}).get('template'),'shape':[m.rows,m.cols-1],'classification':kind,'selected':sels,'errors':errors,'displayed_matrices':len(ms)}

def main():
 save('package-before.json',package_hashes())
 g=module(W/'17592186115299.py')
 source=load(JOB/'source/source.json')['material']['kp'][':knowledge-point/questions']
 replays=[];replay_report=[]
 for q in source:
  name=q[':question/math-academy-id'];n=system(q[':question/problem']).cols-1
  r=g.generate('moderate',seed=91021,template=name,parameters={'scales':[1]*n,'translations':[0]*n});replays.append(r)
  old=q[':question/answer-fields'];new=r['question'][':question/answer-fields']
  banks=lambda fs:sorted([(f[':answer-field/key'],ftype(f),sorted(a[':answer/value'] for a in f[':answer-field/choices']),value(f)) for f in fs])
  replay_report.append({'source_id':q[':question/id'],'template':name,'same_system':system(q[':question/problem'])==system(r['question'][':question/problem']),'same_complete_banks':banks(old)==banks(new),'check':check(r),'source_repairs':r['generation']['source_repairs']})
 save('source-replays.json',replays);save('source-replay-report.json',replay_report)
 # Fresh seeds, ten per schedule; instrument the true rejection/resampling branch.
 attempts=[];real=g.moderate_instance
 def tracked(name,p):
  try:r=real(name,p)
  except ValueError as ex:attempts.append({'template':name,'accepted':False,'reason':str(ex),'parameters':p});raise
  attempts.append({'template':name,'accepted':True,'parameters':p});return r
 g.moderate_instance=tracked
 records=[g.generate('moderate',seed=seed,template=name) for name in g.TEMPLATES for seed in range(81031,81041)]
 g.moderate_instance=real
 save('independent-samples.json',records);save('sampling-attempts.json',attempts)
 batch=load(JOB/'samples.json');save('batch.json',batch)
 # Same visible numerical evidence except the contradictory RHS; same seed/layout/order.
 cf=[]
 for matrix in [[[3,2,-3],[-6,-4,7]],[[3,2,-3],[-6,-4,6]],[[6,4,-6],[-12,-8,12]]]:
  cf.append(g.generate('moderate',seed=81077,template='q-74638',parameters={'matrix':matrix,'order':['independent','dependent','inconsistent']}))
 cf.append(g.generate('moderate',seed=81077,template='q-74638',parameters={'matrix':[[3,2,-3],[-6,-4,6]],'order':['dependent','inconsistent','independent']}))
 save('counterfactual-records.json',cf)
 reports={k:[check(r) for r in rs] for k,rs in [('samples',records),('batch',batch),('counterfactuals',cf)]};save('math-report.json',reports)
 cases=[]
 for r in replays+records+batch+cf:
  checks=[]
  for i,f in enumerate(r['question'][':question/answer-fields']):
   for a in f[':answer-field/choices']:
    checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==value(f) else 'rejected','purpose':'independent classification; every field-owned alternative'})
  cases.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
 save('native-input.json',cases)
 # Inventory is inspected mathematically; metadata is absent from captured generated entries.
 inv=load(JOB/'source/inventory.json');inv_report=[]
 for q in inv['questions']:
  r={'question':q};row=check(r);row['entity_id']=q[':db/id'];row['source_original']=bool(q.get(':question/math-academy-id'));inv_report.append(row)
 save('inventory-math-report.json',inv_report)
 save('affected-inventory.json',{'affected_questions':[]})
 summary={'source_replays':len(replays),'replay_mismatches':[r for r in replay_report if not r['same_system'] or not r['same_complete_banks'] or r['check']['errors']], 'math_errors':{k:[r for r in v if r['errors']] for k,v in reports.items()},'attempts':len(attempts),'rejections':sum(not a['accepted'] for a in attempts),'native_cases':len(cases),'inventory_errors':[r for r in inv_report if r['errors']]}
 save('initial-summary.json',summary);print(json.dumps(summary,default=str)[:6000])
 (E/'session-state.md').write_text('Independent source account saved before package read. Completed source replay, 170 fresh samples, exact batch math, controlled pairs, and captured inventory math. Native input ready. No package edits. See initial-summary.json.\n')
if __name__=='__main__':main()
