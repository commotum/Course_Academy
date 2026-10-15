"""Independent rendered-system checks and actual application radio grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('singular_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
y=sp.Symbol('y');x=sp.Symbol('x')
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def parse(s):
 s=s.strip().replace(' ','').replace(r'\,','')
 s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 s=re.sub(r'(\d|\))(?=y)',r'\1*',s)
 return sp.sympify(s,locals={'y':y,'x':x})
def mats(s):return [sp.Matrix([[parse(e) for e in row.split('&')] for row in body.split(r'\\')]) for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)]
def answer(s):
 ms=mats(s)
 if len(ms)==1 and ms[0].shape==(2,3):return ('ref',tuple(ms[0].rref()[0]))
 if len(ms)==2:return ('family',tuple(ms[1]))
 angle=re.search('⟨([^⟩]+)⟩',s);assert angle
 vals=tuple(parse(v) for v in angle[1].replace(r'\,','').split(','))
 return ('family' if y in set().union(*(v.free_symbols for v in vals)) else 'point', vals)
def checks(rec):
 f=rec['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all complete-bank choices, actual grade_field'} for a in f[':answer-field/choices']]
def fingerprint(q):return g.fingerprint(q)
def independent(rec):
 m=rec['generation'];q=rec['question'];level=q[':question/difficulty'].split('/')[-1]
 assert rec==g.generate(level,m['seed'],m['template'],m['parameters'])
 a=mats(q[':question/problem'])[0];assert a.shape==(2,3) and a.rank()==a[:,:2].rank()==1
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection'
 assert len(f[':answer-field/choices'])==5
 keys=[answer(z[':answer/value']) for z in f[':answer-field/choices']]
 assert len(set(keys))==5, 'Equivalent answer objects '+m['template']
 matches=[]
 for opt,key in zip(f[':answer-field/choices'],keys):
  if key[0]=='ref':correct=key[1]==tuple(a.rref()[0])
  elif key[0]=='family':
   vx,vy=key[1];correct=all(sp.expand(a[i,0]*vx+a[i,1]*vy-a[i,2])==0 for i in range(2)) and vy==y
  else:correct=False # a single point is not the general solution
  if correct:matches.append(opt[':answer/id'])
 assert matches==[f[':answer-field/correct'][1]],m['template']
 sol=q[':question/worked-solution'];ms=mats(sol);aug=[z for z in ms if z.shape==(2,3)]
 for z in aug:assert z.rref()[0]==a.rref()[0], 'Wrong row-reduction stage'
 if 'reduce' in q[':question/problem']:
  assert aug[0]==a and aug[-1][0,0]==1 and aug[-1][1,:]==sp.zeros(1,3)
 else:assert a[1,:]==sp.zeros(1,3)
 # Independently read every scalar equation in the prose and aligned system.
 equations=[]
 for match in re.finditer(r'(?<![0-9A-Za-z])(x[+\-0-9y ]*)\s*&?=([+\-0-9y ]+)',sol):
  lhs,rhs=parse(match[1]),parse(match[2]);expr=sp.expand(lhs-rhs)
  if expr.has(x):
   normalized=sp.solve(expr,x)[0];expected=sp.solve(a[0,0]*x+a[0,1]*y-a[0,2],x)[0]
   assert sp.expand(normalized-expected)==0,('Stale scalar equation',match[0]);equations.append(match[0])
 if 'general solution' in q[':question/problem']:
  assert len(equations)>=3
  families=[z for z in ms if z.shape==(2,1) and z[0]!=x]
  for z in families:assert a*sp.Matrix([z[0],z[1],-1])==sp.zeros(2,1)
  for body in re.findall('⟨([^⟩]+)⟩',sol):
   z=[parse(v) for v in body.replace(r'\,','').split(',')];assert a*sp.Matrix(z+[-1])==sp.zeros(2,1)
 assert m['mathematical_fingerprint']==fingerprint(q)
 return rec
check=independent
def main():
 inputs=[];replays=[];review=[];coverage={};total=0
 for sid,old in g.CASES.items():
  level=old[':question/difficulty'][':db/ident'].split('/')[-1];r=independent(g.generate(level,template=sid,parameters={'rhs_scale':1}));q=r['question'];f=q[':question/answer-fields'][0];original=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in original[':answer-field/choices'])
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==original[':answer-field/correct'][':answer/value']
  replays.append({'source':sid,'complete_bank_match':True,'matched_choices':5,'matched_distractors':4,'prompt_exact':True,'solution_exact':True,'missing':[],'extra':[]})
  for t in [-4,-3,-2,-1,1,2,3,4]:
   rec=independent(g.generate(level,template=sid,parameters={'rhs_scale':t}));assert rec['question']==g.generate(level,999,sid,{'rhs_scale':t})['question'];total+=1
   inputs.append({'label':sid+' scale '+str(t),'record':rec,'checks':checks(rec)})
  coverage[sid]={'rhs_scale':[-4,-3,-2,-1,1,2,3,4],'targets':'fixed x basic, y free; rank-one 2x2 backbone','missing_slots':[]}
  variants=[g.generate(level,template=sid,parameters={'rhs_scale':t}) for t in [1,-2,3]]
  review.append({'source':sid,'variants':variants})
 for level in g.SUPPORTED_LEVELS:
  cli=subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty',level,'--count','5','--seed','105745','--format','json'],capture_output=True,text=True,check=True)
  records=json.loads(cli.stdout);assert isinstance(records,list) and len(records)==5
  for rec in records:independent(rec)
 for l in ['hard','unclassified']:
  try:g.generate(l)
  except ValueError:pass
  else:raise AssertionError('Unsupported level accepted')
 save('source-replay.json',{'passed':True,'banks_matched':len(replays),'banks_total':len(replays),'distractors_matched':len(replays)*4,'distractors_total':len(replays)*4,'profiles':replays,'excluded_sources':['q-42156','q-73524']})
 save('slot-coverage.json',coverage);save('review.json',review);save('native-input.json',inputs)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('validation.json',{'status':'pass','passed':True,'exhaustive_instances':total,'source_banks':len(replays),'source_distractors':4*len(replays),'correctness':'Rendered matrices, rowspace of every reduction stage, every scalar equation, solution vectors, complete answer banks; rank-one family not isolated points','grading':'actual application grade_field for all five options on every bounded instance','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'replenish.py',HERE/'capabilities.json',ROOT/'generate/runs/current/check-engine']}})
if __name__=='__main__':main()
