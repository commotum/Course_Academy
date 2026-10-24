"""Independent exact checks and prompt-blind regression for the tangent repair."""
from collections import Counter
from functools import lru_cache
from pathlib import Path
import importlib.util
import json
import random
import re
import sys
import sympy as S
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'package'))
spec=importlib.util.spec_from_file_location('candidate',HERE/'package/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
OUT=HERE/'evidence';OUT.mkdir(exist_ok=True)
FAMILY=[S.Integer(2)+S.sqrt(3),S.Integer(2)-S.sqrt(3),-S.Integer(2)+S.sqrt(3),-S.Integer(2)-S.sqrt(3)]

def save(name,value):(OUT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
@lru_cache(None)
def tex(text):
 t=text.replace('π',r'\pi').replace('∘',r'\circ')
 for part in [r'\left',r'\right',r'\displaystyle',r'\,',r'\!']:t=t.replace(part,'')
 t=t.replace(r'\dfrac',r'\frac').replace(r'\cdot','*')
 def group(start):
  assert t[start]=='{';depth=1;end=start+1
  while depth:
   if t[end]=='{':depth+=1
   if t[end]=='}':depth-=1
   end+=1
  return t[start+1:end-1],end
 while r'\frac' in t:
  i=t.index(r'\frac');a,j=group(i+5);b,k=group(j);t=t[:i]+'(('+str(tex(a))+')/('+str(tex(b))+'))'+t[k:]
 while r'\sqrt' in t:
  i=t.index(r'\sqrt');a,j=group(i+5);t=t[:i]+'sqrt('+str(tex(a))+')'+t[j:]
 while r'\tan' in t:
  i=t.index(r'\tan');j=i+4
  while t[j].isspace():j+=1
  assert t[j]=='(';k=j+1;depth=1
  while depth:
   if t[k]=='(':depth+=1
   if t[k]==')':depth-=1
   k+=1
  arg=t[j+1:k-1].replace(r'^\circ','*pi/180').replace(r'^{\circ}','*pi/180')
  t=t[:i]+'('+str(S.tan(tex(arg)))+')'+t[k:]
 t=t.replace(r'\pi','pi').replace('{','(').replace('}',')').replace('^','**')
 return S.simplify(parse_expr(t,transformations=standard_transformations+(implicit_multiplication_application,)))

def field(r):return r['question'][':question/answer-fields'][0]
def key(r):
 f=field(r);return next(c for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
def target(r):
 t=re.search(r'\$(.*?)\$',r['question'][':question/problem'])[1]
 a=t.split(r'\tan\left(')[1].split(r'\right)')[0]
 return int(a.split('^')[0]) if r'\circ' in a else int(S.simplify(tex(a)*180/S.pi))
def interval(value):return (value>0,abs(value)<1)
def family_member(v):return any(S.simplify(v-w)==0 for w in FAMILY)
def probe(r):
 f=field(r);a=target(r)%180;bucket=(a<90,a<45 or a>135)
 cs=[(c,tex(c[':answer/value'])) for c in f[':answer-field/choices']]
 bounded=[c for c,v in cs if interval(float(v))==bucket]
 family=[c for c,v in cs if family_member(v)]
 combined=[c for c,v in cs if family_member(v) and interval(float(v))==bucket]
 return {'interval_candidates':len(bounded),'fraction_free_interval_candidates':sum(r'\frac' not in c[':answer/value'] for c in bounded),'family_shape_candidates':len(family),'family_and_bounds_candidates':len(combined),'key':key(r)[':answer/value']}

def math_check(r,full_solution=True):
 expected=S.simplify(S.tan(S.pi*target(r)/180));f=field(r)
 values=[tex(c[':answer/value']) for c in f[':answer-field/choices']]
 assert len(values)==5 and len(set(values))==5
 assert sum(S.simplify(v-expected)==0 for v in values)==1
 assert S.simplify(tex(key(r)[':answer/value'])-expected)==0
 if full_solution:
  q=r['question']
  for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S):
   for row in block.split(r'\\'):
    rhs=row.strip().split('&=')[1];assert S.simplify(tex(rhs)-expected)==0,(target(r),row)
  hint=q[':question/problem'].split('fact that $')[1].split('$')[0];lhs,rhs=hint.split('=')
  if r'\circ' in lhs:lhs=lhs.replace(r'^\circ','');rhs=rhs.replace(r'^\circ','')
  assert S.simplify(tex(lhs)-tex(rhs))==0
 return True

def main():
 negatives={}
 for index in [1,2]:
  rows=json.loads((HERE/'original'/f'review-{index}-batch.json').read_text());probes=[probe(r) for r in rows]
  negatives[str(index)]={'count':len(rows),'unique_interval':sum(p['interval_candidates']==1 for p in probes),'unique_shape':sum(p['family_shape_candidates']==1 for p in probes),'combined':sum(p['family_and_bounds_candidates']==1 for p in probes)}
 assert negatives['1']['unique_interval']>0 and negatives['2']['unique_shape']>0
 batch=g.generate(5,3750266970);fresh=g.generate(8,73)
 catalog=[g.make(*args,rng=random.Random(120083+i)) for i,args in enumerate(g.catalog())]
 save('requested.json',batch);save('fresh.json',fresh);save('catalog.json',catalog)
 cases=[];grader=[]
 for name,rows in [('requested',batch),('fresh',fresh),('catalog',catalog)]:
  for i,r in enumerate(rows):
   math_check(r);p=probe(r)
   assert p['interval_candidates']>=2 and p['fraction_free_interval_candidates']>=2 and p['family_shape_candidates']==2
   cases.append({'set':name,'index':i,**p})
   grader.append({'label':name+'/'+str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==field(r)[':answer-field/correct'][1] else 'rejected'} for c in field(r)[':answer-field/choices']]})
 # Every served bank must support a different exact answer with unchanged options.
 paired=[]
 for i,r in enumerate(catalog):
  choices=[c[':answer/value'] for c in field(r)[':answer-field/choices']]
  old_value=tex(key(r)[':answer/value'])
  alternative=next(tex(c) for c in choices if family_member(tex(c)) and tex(c)!=old_value)
  args=next(args for args in g.catalog() if S.simplify(S.tan(S.pi*(args[0]+(1 if args[2]=='+' else -1)*args[1])/180)-alternative)==0)
  other=g.make(*args,bank_values=choices,rng=random.Random(i))
  assert sorted(c[':answer/value'] for c in field(other)[':answer-field/choices'])==sorted(choices)
  assert tex(key(other)[':answer/value'])!=old_value
  math_check(other)
  paired.append({'original':r,'different_target_same_bank':other})
 save('paired-counterfactuals.json',paired)
 # Broad seed exercise: guards apply by construction, rather than selecting a good seed.
 seed_counts=Counter();tested=0
 for seed in range(250):
  for r in g.generate(5,seed):
   math_check(r,False);p=probe(r);assert p['interval_candidates']>=2 and p['fraction_free_interval_candidates']>=2 and p['family_shape_candidates']==2
   tested+=1;seed_counts[str(p['key'])]+=1
 replays=[];source_probes=[]
 for s in g.SOURCES:
  r=g.make(*s['parameters'],profile=s['ma_id']);math_check(r)
  assert sorted([tex(c[':answer/value']) for c in field(r)[':answer-field/choices']],key=str)==sorted([tex(c) for c in s['bank']],key=str)
  replays.append(r);source_probes.append({'source':s['ma_id'],**probe(r)})
 assert all(p['family_and_bounds_candidates']==1 for p in source_probes)
 save('source-replays.json',replays);save('grader-input.json',grader)
 # Algebraic proof uses exact arithmetic; matching a complete learned answer family
 # then finding the quadrant is inherently sufficient, regardless of the wrong bank.
 obstruction={'exact_family':[str(v) for v in FAMILY],'intervals':[[bool(v>0),bool(abs(v)<1)] for v in FAMILY],'source_bank_probes':source_probes,'classification':'finite-family knowledge; not a fixable option-format leak','limitations':'A learner who knows all four exact values can combine that knowledge with sign and magnitude. The generator cannot force use of the formula from final-answer responses alone.'}
 assert len(set(tuple(x) for x in obstruction['intervals']))==4
 save('finite-family-proof.json',obstruction)
 render=[];covered=set()
 for r in catalog:
  p=r['generation']['parameters'];features={('unit',p['unit']),('operation',p['operation']),('value',key(r)[':answer/value']),('thirds',r['generation']['derivation']['clears_thirds'])}
  if not features<=covered:render.append(r);covered|=features
  if len(render)>=6:break
 save('render-input.json',render)
 result={'passed':True,'negative_regressions':negatives,'full_catalog_records':len(catalog),'explicit_counterfactual_banks':len(paired),'additional_seed_records':tested,'source_replay_banks':len(replays),'cases':cases,'seed_key_counts':dict(seed_counts),'limitations':obstruction['limitations']}
 save('verification.json',result);print(json.dumps({k:v for k,v in result.items() if k!='cases'}))

if __name__=='__main__':main()
