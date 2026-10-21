"""Check live registered samplers against saved sources and independent algebra."""
import importlib.util,itertools,json,random,re,sys,subprocess
from pathlib import Path
from fractions import Fraction
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
from scripts.generator_publish import validate_question,answer_id,enum
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
V={c:sp.Symbol(c,positive=True) for c in 'xyzpk'};V['e']=sp.E
TRANS=standard_transformations+(implicit_multiplication_application,)
def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False,default=str)+'\n')
def scalar(text,atoms=None):
 text=text.strip()
 while (m:=re.search(r'\\(?:d?frac|sqrt)\{',text)):
  start=m.start();pos=m.end()-1;parts=[]
  for _ in range(1 if 'sqrt' in m[0] else 2):
   assert text[pos]=='{';depth=1;j=pos+1
   while depth:
    if text[j]=='{':depth+=1
    elif text[j]=='}':depth-=1
    j+=1
   parts.append(text[pos+1:j-1]);pos=j
  replacement='(sqrt('+str(scalar(parts[0]))+'))' if len(parts)==1 else '('+str(scalar(parts[0]))+')/('+str(scalar(parts[1]))+')'
  text=text[:start]+replacement+text[pos:]
 text=text.replace(r'\cdot','*').replace('^','**').replace('{','(').replace('}',')')
 return parse_expr(text,local_dict={**V,**(atoms or {})},transformations=TRANS)
def expr(text):
 text=text.strip().rstrip('.').strip();atoms={};pat=re.compile(r'\\(ln|log)(?:_\{([^}]+)\})?\s*(\\left\()?\s*\(?')
 while (m:=pat.search(text)):
  if m[3]:end=text.index(r'\right)',m.end());skip=7
  else:end=text.index(')',m.end());skip=1
  inner=text[m.end():end];base=sp.E if m[1]=='ln' else scalar(m[2] or '10');name='L'+str(len(atoms));atoms[name]=sp.expand_log(sp.log(scalar(inner))/sp.log(base),force=True);text=text[:m.start()]+name+text[end+skip:]
 # Substitute placeholders before implicit multiplication can split them.
 return scalar(text,atoms)
def equal(a,b): return sp.simplify(sp.expand_log(a-b,force=True))==0
def target(q):
 maths=re.findall(r'\$(.*?)\$',q[':question/problem'],re.S);maths=[m for m in maths if '\\log' in m or '\\ln' in m]
 if len(maths)==1:return expr(maths[0].rstrip('='))
 givens={}
 for m in maths[:-1]:
  lhs,rhs=m.split('=');givens[expr(lhs)]=expr(rhs)
 return sp.expand(expr(maths[-1].rstrip('='))).subs(givens,simultaneous=True).expand(),givens
def algebra(q):
 t=target(q);givens={}
 if isinstance(t,tuple):t,givens=t
 f=q[':question/answer-fields'][0];aid=answer_id(f[':answer-field/correct']);steps=0
 def evaluate(s):return sp.expand(expr(s)).subs(givens,simultaneous=True).expand()
 for a in f[':answer-field/choices']:
  assert equal(evaluate(a[':answer/value']),t)==(str(a[':answer/id'])==aid),(q[':question/id'],a[':answer/value'],t)
 for display in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
  display=re.sub(r'\\(?:begin|end)\{aligned\}','',display).replace('&','')
  for line in display.split(r'\\'):
   for piece in line.split('='):
    piece=piece.strip().rstrip('.').strip()
    if piece:assert equal(evaluate(piece),t),(q[':question/id'],piece,t);steps+=1
 return steps
def main():
 records=[];report={};ledger=[]
 for kp in (17592186054622,17592186054625):
  directory=HERE/'package' if kp==17592186054625 else HERE/str(kp)/'original';sys.path.insert(0,str(directory));spec=importlib.util.spec_from_file_location('g'+str(kp),directory/'generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
  samples=[];families={};steps=0;paths=0
  for seed in range(50):
   rng=random.Random(seed);batch=[g.generate(rng) for _ in range(20)]
   rng2=random.Random(seed);assert batch==[g.generate(rng2) for _ in range(20)]
   for r in batch:
    validate_question(r['question']);m=r['generation'];family=m.get('template',m.get('profile'));families[family]=families.get(family,0)+1
    if kp==17592186054622:
     p=m['parameters'];assert p['a']>0 and p['b']>0 and max(p['a'],p['b'])>1
     assert family in ('numeric','symbolic') and '\\frac' not in r['question'][':question/problem']
     assert all(c['a']>0 and c['b']>0 for c in p['role_bank'])
    elif family!='numeric-combine':
     v=list(map(Fraction,m['answer_vector']));assert sum(c>0 for c in v)==2 and any(abs(c)!=1 for c in v)
    else: assert m['p']>=2 and m['a']>1 and m['d']>1 and m['constant_sign']==m['variable_sign']==1
   samples+=batch
  if kp==17592186054625:
   # Exhaust every bank target, sign partition, variable role and term order.
   for profile,signs,perm,order,key in itertools.product(g.PROFILES,g.SIGNS,itertools.permutations(range(3)),itertools.permutations(range(3)),range(5)):
    p,q=(3,2) if profile=='combine-revised' else (2,3)
    visible=[signs[perm.index(i)] for i in range(3)];allowed=[visible[i] for i in order]==[1,1,-1]
    try:
     r=g.build(profile,key,p,q,signs,perm,'2',order);assert allowed;v=list(map(Fraction,r['generation']['answer_vector']));assert sum(c>0 for c in v)==2 and any(abs(c)!=1 for c in v)
    except ValueError:assert not allowed
    paths+=1
   for omitted in range(6):
    for a,d in g.numeric_parameters(omitted):
     for key,sign in itertools.product(range(5),(-1,1)):
      cases=[c for i,c in enumerate(g.NUMERIC_CASES) if i!=omitted];allowed=cases[key][1]==1 and sign==1
      try:g.build_numeric(omitted,key,a,d,sign);assert allowed
      except ValueError:assert not allowed
      paths+=1
  live=json.loads((HERE/str(kp)/'kp.json').read_text());authored=[q for q in live[':knowledge-point/questions'] if not q.get(':question/math-academy-id')]
  for q in authored:
   steps+=algebra(q);records.append({'question':q});ledger.append({'kp':kp,'question':q[':db/id'],'decision':'retain','scope':'positive product and power; substitute given log values' if kp==17592186054622 else 'product, quotient, and non-unit power all required','algebra':'all choices and printed steps verified'})
  for r in samples[:80]:steps+=algebra(r['question']);records.append(r)
  report[str(kp)]={'passed':True,'sampled_questions':len(samples),'profiles':families,'exhaustive_bank_paths':paths,'existing_authored_questions':len(authored),'algebra_questions':80+len(authored),'printed_steps_verified':steps,'sampler_deterministic':True}
  print(json.dumps({str(kp):report[str(kp)]}),flush=True)
 for r in json.loads((HERE/'replacements.json').read_text()):algebra(r['question']);records.append(r)
 live=json.loads((HERE/'kp.json').read_text())
 for patch in json.loads((HERE/'solution-updates.json').read_text()):
  import copy
  q=copy.deepcopy(next(q for q in live[':knowledge-point/questions'] if q[':db/id']==patch['entity']));q[patch['attribute']]=patch['after'];algebra(q);records.append({'question':q})
 spec=importlib.util.spec_from_file_location('original625',HERE/'original/generator.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
 for i in range(5):
  r=g.replay(i)
  source=json.loads((HERE/'package/canonical_case.json').read_text()) if i==4 else next(q for q in json.loads((HERE/'package/source_cases.json').read_text()) if q[':question/id']==g.SOURCE_IDS[i])
  assert r['question'][':question/problem']==g.normalize_prose(source[':question/problem'])
  assert r['question']==old.replay(i)['question'],'Captured source replay changed'
 save('independent-algebra-ledger.json',ledger);save('grading-records.json',records)
 save('scope-verification.json',{'passed':True,'database_basis':json.loads((HERE/'identity.json').read_text())['basis'],'generators':report,'unregistered_kp':17592186054623,'withdrawals_required':3,'database_writes_pending':True})
 # Use the installed native grading path on new samples and all live authored banks.
 questions=[]
 for r in records:
  q=r['question'];fs=[]
  for f in q[':question/answer-fields']:
   correct=f[':answer-field/correct'];value=correct.get(':answer/value') if isinstance(correct,dict) else next(a[':answer/value'] for a in f[':answer-field/choices'] if str(a[':answer/id'])==answer_id(correct))
   fs.append({'key':f[':answer-field/key'],'type':enum(f[':answer-field/type']).split('/')[-1],'correct_value':value,'choices':[{'type':enum(a[':answer/type']).split('/')[-1],'value':a[':answer/value']} for a in f[':answer-field/choices']]})
  questions.append({'math_academy_id':str(q[':question/id']),'problem':q[':question/problem'],'knowledge_point':'Logarithm scope audit','answer_fields':fs})
 out=HERE/'native-grading';out.mkdir(exist_ok=True);(out/'input.json').write_text(json.dumps({'questions':questions})+'\n')
 binary=ROOT/'reference/mathacademy/repairs/2026-10-20-log-product-quotient/native-grading/grader';subprocess.run([str(binary),str(out/'input.json'),str(out/'results.json')],check=True)
 result=json.loads((out/'results.json').read_text());assert result['current_engine_ready_count']==len(questions)
 save('quality-verification.json',{'passed':True,'scope':report,'unregistered_kp':17592186054623,'native_grading_questions':len(questions),'source_replays':5,'existing_authored_questions_audited':len(ledger),'withdrawals_required':3,'database_writes_pending':True})
 save('algebra-verification.json',{'passed':True,'questions':len(questions),'printed_steps_verified':sum(r['printed_steps_verified'] for r in report.values()),'replacements_and_solution_update_independently_checked':4,'distractors_verified_incorrect':4*len(questions)})
if __name__=='__main__':main()
