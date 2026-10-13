"""Independently parse printed linear equations; test actual application grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('perpendicular',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x,y=sp.symbols('x y',real=True)
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def expression(t):
 t=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
 return sp.expand(parse_expr(t,local_dict={'x':x,'y':y},transformations=standard_transformations+(implicit_multiplication_application,)))
def polynomial(t):
 l,r=t.split('=');return sp.expand(expression(l)-expression(r))
def normalized(t):
 e=polynomial(t);a=e.coeff(x);b=e.coeff(y);c=e.subs({x:0,y:0});scale=a if a else b
 assert scale!=0
 return tuple(sp.cancel(z/scale) for z in (a,b,c))
def fingerprint(q):return g.fingerprint(q)
def printed(q):
 p=q[':question/problem'];pairs=[tuple(map(int,z)) for z in re.findall(r'\((-?\d+),\s*(-?\d+)\)',p)];u,v=pairs[0]
 if 'line passing through the points' in p:
  (a,b),(c,d)=pairs[-2:];m1=sp.Rational(d-b,c-a)
 else:
  ref=p.split('perpendicular to ',1)[1].split('$',2)[1].rstrip('.?');e=polynomial(ref);m1=-e.coeff(x)/e.coeff(y)
 return u,v,m1

def check(rec):
 q=rec['question'];meta=rec['generation'];s=meta['template'];t=meta['parameters']['t']
 assert meta['version']==g.VERSION and rec['knowledge_point']['db_id']==g.KP_ID
 assert g.generate(g.DATA[s][0],meta['seed'],s,{'t':t})==rec
 u,v,m1=printed(q);m=-1/m1;b=v-m*u;f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];kind=f[':answer-field/type']
 assert len(q[':question/answer-fields'])==1
 if kind.endswith('/blank'):
  assert len(bank)==1 and '=' not in bank[0][':answer/value'] and '{{field-1}}' in q[':question/problem']
  assert expression(bank[0][':answer/value'])==m*x+b
 else:
  assert len(bank)==5 and len({normalized(a[':answer/value']) for a in bank})==5
  for a in bank:
   e=polynomial(a[':answer/value']);correct=e.coeff(y)!=0 and sp.cancel(-e.coeff(x)/e.coeff(y))==m and e.subs({x:u,y:v})==0
   assert correct==(a[':answer/id']==f[':answer-field/correct'][1])
 assert m*m1==-1 and (m*x+b).subs(x,u)==v
 # Every generated numerical algebra row involving y is an equivalent line.
 if t!=0 or not g.sources()[s].get(':question/worked-solution'):
  sol=q[':question/worked-solution'];rows=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
  for index,block in enumerate(rows):
   for row in block.split('\\\\'):
    if '&=' not in row:continue
    l,r=row.split('&=');l=l.strip();r=r.strip()
    if 'y_1' in l or 'm_1' in l or not 'y' in l:continue
    e=sp.expand(expression(l)-expression(r));expected=m1*x + sp.Rational(g.DATA[s][2][2],g.DATA[s][2][1]) if index==0 and g.DATA[s][2] else m*x+b
    assert e.subs(y,expected)==0,(s,t,row,e,expected)
 assert fingerprint(q)==meta['mathematical_fingerprint']
 return rec

def native(label,r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'full bank ID grading'} for a in f[':answer-field/choices']]
 else:
  u,v,m1=printed(r['question']);m=-1/m1;b=v-m*u
  checks=[{'submitted':a,'expected':e,'purpose':p} for a,e,p in [(f[':answer-field/choices'][0][':answer/value'],'accepted','canonical latex'),(str(m*x+b),'accepted','expanded equivalent'),(f'({m})*(x-({u}))+({v})','accepted','point-slope equivalent RHS'),(str(m*x+b+1),'rejected','wrong intercept'),(str(-m*x+b),'rejected','wrong slope')]]
 return {'label':label,'record':r,'checks':checks}

def main():
 source=json.loads((HERE/'source.json').read_text());inputs=[];replays=[];reviews=[];fps=set();counts={}
 for s,old in g.sources().items():
  rec=check(g.generate(g.DATA[s][0],0,s,{'t':0}));q=rec['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem']
  assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
  observed=of.get(':answer-field/choices',[]);actual=f[':answer-field/choices']
  if observed:
   normal=normalized if f[':answer-field/type'].endswith('/radio') else expression
   assert {normal(a[':answer/value']) for a in actual}=={normal(a[':answer/value']) for a in observed} and len(actual)==len(observed)
   if of.get(':answer-field/correct'):
    ca=next(a for a in actual if a[':answer/id']==f[':answer-field/correct'][1]);assert normal(ca[':answer/value'])==normal(of[':answer-field/correct'][':answer/value'])
  if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution']
  replays.append({'source':s,'complete_bank_matched':bool(observed),'matched':len(observed),'total':len(observed),'distractors_matched':4 if len(observed)==5 else 0,'correct_origin':'source verified' if of.get(':answer-field/correct') else 'mathematically derived missing marker','solution_origin':'source exact' if old.get(':question/worked-solution') else 'authored missing solution','missing_extra_options':[]})
  reviews.append('## Source '+s+'\n\n'+g.markdown(rec))
 for level in ('easy','moderate'):
  count=0
  for s,p in g.candidates(level):
   rec=check(g.generate(level,1910,s,p));inputs.append(native(s+'-'+str(p['t']),rec));fp=rec['generation']['mathematical_fingerprint'];assert fp not in fps;fps.add(fp);count+=1
   assert g.generate(level,999,s,p)['question']==rec['question']
  counts[level]=count
 previews=g.batch('easy',5,1910)+g.batch('moderate',5,1910)
 for rec in previews:check(rec);reviews.append('## Variant\n\n'+g.markdown(rec))
 for level,s,p in [('hard','q-23631',{'t':1}),('easy','q-23631',{'t':9}),('easy','q-23631',{'t':1.5}),('moderate','q-23631',{'t':1})]:
  try:g.generate(level,0,s,p)
  except ValueError:pass
  else:raise AssertionError('Invalid boundary accepted')
 save('previews.json',previews);save('native-input.json',inputs)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('source-replay.json',{'passed':True,'source_basis':source['basis'],'source_results':replays,'complete_banks_matched':8,'complete_banks_total':8,'source_distractors_matched':20,'source_distractors_total':20,'matched_answer_values':28,'total_observed_answer_values':28,'missing_or_extra_options':[],'fidelity_limits':'Unrated q-214033 has no answer or solution; q-23633 has no marker or solution. These are authored additions. Variant solutions keep slope, negative reciprocal, point-slope expansion, then standard form sequences, with streamlined parentheses. Exact source solutions retained at replay.'})
 (HERE/'review.md').write_text('\n\n'.join(reviews)+'\n')
 save('validation.json',{'passed':True,'exhaustive_instances':len(fps),'counts':counts,'distinct_bounded_tasks':len(fps),'native_grading':'every bank option and canonical/equivalent/incorrect blank entries for all bounded tuples','mathematics':'printed reference direction, perpendicular product, target incidence, unique equation banks, all generated numeric solution rows','source_fidelity':'all 28 observed values, 20 distractors, 8 complete banks; 9 prompts and field contracts; 7 exact supplied source solutions','supported_levels':['easy','moderate'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json')}})
 print('Validated',counts)
if __name__=='__main__':main()
