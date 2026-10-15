"""Read rendered systems independently; exercise every bounded variant and grade every option."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x,y=sp.symbols('x y')
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def parse(s):
 s=s.strip().rstrip('.,').replace(' ','').replace(r'\,','')
 s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 s=re.sub(r'(\d|\))(?=[xy])',r'\1*',s)
 return sp.sympify(s,locals={'x':x,'y':y})
def mats(text):return [sp.Matrix([[parse(e) for e in row.split('&')] for row in b.split(r'\\')]) for b in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def prompt_matrix(text):
 body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)[1];rows=[]
 for row in body.split(r'\\'):
  lhs,rhs=row.replace('&','').split('=');z=parse(lhs);rows.append([z.coeff(x),z.coeff(y),parse(rhs)])
 return sp.Matrix(rows)
def answer(v):
 if v=='No solution':return ('none',)
 m=mats(v);assert len(m)==2 and m[0]==sp.Matrix([x,y])
 return ('family',tuple(m[1]))
def checks(rec):
 f=rec['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete-bank native grading'} for a in f[':answer-field/choices']]
def fingerprint(q):return g.fingerprint(q)
def independent(rec):
 q=rec['question'];m=rec['generation'];level=q[':question/difficulty'].split('/')[-1]
 assert rec==g.generate(level,m['seed'],m['template'],m['parameters'])
 a=prompt_matrix(q[':question/problem']);assert a.shape==(2,3) and a[:,:2].rank()==1
 aug=[z for z in mats(q[':question/worked-solution']) if z.shape==(2,3)];assert aug[0]==a
 prev=a
 for z in aug[1:]:
  normalized=prev.copy();normalized[0,:]=prev[0,:]/prev[0,0]
  eliminated=prev.copy();eliminated[1,:]=prev[1,:]-prev[1,0]/prev[0,0]*prev[0,:]
  assert z==prev or z==normalized or z==eliminated,('Invalid reduction step',m['template'],z,prev)
  prev=z
 assert prev[0,0]==1 and prev[1,0]==prev[1,1]==0
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 assert len(f[':answer-field/choices'])==5
 keys=[answer(a[':answer/value']) for a in f[':answer-field/choices']];assert len(set(keys))==5
 valid=[]
 for opt,key in zip(f[':answer-field/choices'],keys):
  ok=(a.rank()>a[:,:2].rank()) if key[0]=='none' else key[1][1]==y and all(sp.expand(a[i,0]*key[1][0]+a[i,1]*key[1][1]-a[i,2])==0 for i in range(2))
  if ok:valid.append(opt[':answer/id'])
 assert valid==[f[':answer-field/correct'][1]],m['template']
 sol=q[':question/worked-solution'];reduced=sp.Matrix([[1,a[0,1]/a[0,0],a[0,2]/a[0,0]],[0,0,prev[1,2]]])
 # Read every reduced/scalar equation; compare constants as well as consistency.
 equations=[]
 for mt in re.finditer(r'(?<![A-Za-z0-9])((?:0x\+0y|x[+\-0-9y ]*|0))\s*&?=([+\-0-9y ]+)',sol):
  lhs,rhs=parse(mt[1]),parse(mt[2]);expr=sp.expand(lhs-rhs)
  if expr.has(x):assert sp.expand(sp.solve(expr,x)[0]-(reduced[0,2]-reduced[0,1]*y))==0,('Stale x',mt[0])
  else:assert lhs==0 and rhs==prev[1,2],('Stale contradiction',mt[0],prev)
  equations.append(mt[0])
 assert len(equations)>=3
 if a.rank()==1:
  for z in mats(sol):
   if z.shape==(2,1) and z[0]!=x:assert a*sp.Matrix([z[0],z[1],-1])==sp.zeros(2,1)
 else:assert 'no solution' in sol and 'false statement' in sol
 assert m['mathematical_fingerprint']==fingerprint(q)
 return rec
check=independent

def main():
 inputs=[];replays=[];reviews=[];coverage={}
 for sid,old in g.CASES.items():
  level=old[':question/difficulty'][':db/ident'].split('/')[-1];r=independent(g.generate(level,template=sid,parameters={'rhs_scale':1}));q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem']
  assert q[':question/worked-solution']==g.corrected_solution(sid)
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  replays.append({'source':sid,'complete_bank_match':True,'matched_choices':5,'matched_distractors':4,'prompt_exact':True,'solution_exact':sid not in ('q-42159','q-130924'),'supported_correction':'initial second RHS -24 must be +24' if sid=='q-42159' else 'initial coefficient 10 must be 12' if sid=='q-130924' else None,'missing':[],'extra':[]})
  for t in [-4,-3,-2,-1,1,2,3,4]:
   r=independent(g.generate(level,template=sid,parameters={'rhs_scale':t}));assert r['question']==g.generate(level,999,sid,{'rhs_scale':t})['question'];inputs.append({'label':sid+' t='+str(t),'record':r,'checks':checks(r)})
  coverage[sid]={'rhs_scale':[-4,-3,-2,-1,1,2,3,4],'fixed_roles':'x basic, y free; two equations, dependent coefficient rows','missing_slots':[]}
  reviews.append({'source':old,'variants':[g.generate(level,template=sid,parameters={'rhs_scale':t}) for t in [-2,3]]})
 for level in g.SUPPORTED_LEVELS:
  cli=subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty',level,'--count','5','--seed','105746','--format','json'],capture_output=True,text=True,check=True);records=json.loads(cli.stdout);assert len(records)==5
  for r in records:independent(r)
 for level in ['hard','unclassified']:
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('Unsupported accepted')
 save('source-replay.json',{'passed':True,'banks_matched':len(replays),'banks_total':len(replays),'distractors_matched':len(replays)*4,'distractors_total':len(replays)*4,'profiles':replays})
 save('slot-coverage.json',coverage);save('review.json',reviews);save('native-input.json',inputs)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('validation.json',{'status':'pass','passed':True,'exhaustive_instances':len(inputs),'source_banks':len(replays),'source_distractors':len(replays)*4,'correctness':'Independently parsed rendered systems, exact elementary row operations, scalar equations, full answer objects and solution families','grading':'actual application grade_field; all five options for all 128 bounded instances','fidelity':'all source prompts and complete banks replay; two documented source initial-matrix corrections','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'replenish.py',HERE/'capabilities.json',ROOT/'generate/runs/current/check-engine']}})
if __name__=='__main__':main()
