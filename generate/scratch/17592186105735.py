#!/usr/bin/env python3
"""Definition of the scalar triple product, math basis 1356.

Source fidelity uses parameterized vector/cross/dot operation masks. Historical
radio banks are opaque numerical evidence profiles, NOT recovered error intent.
Normal radios use complete operation-derived banks, chosen before sampling.
Easy: supplied cross product, signed integers or one matching square-root pair.
Moderate: cross then dot; integers |coordinate|<=4. Hard is authored: all nine
coordinates nonzero, all six cross products and all three dot products active,
and at least one magnitude 5 (ceiling 5). No scalar determinant shortcut,
properties, volumes, or geometry. Explicit calls and sampling share guards.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186105735
KP_UUID='7ba6b6b5-ac1d-5a3a-876a-af51fdf50e0a'
TITLE='Calculating the Scalar Triple Product Using the Definition'
VERSION='definition-triple-v2'
EVIDENCE=Path(__file__).with_suffix('')
SOURCE=json.loads((EVIDENCE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
SPECS={
'q-20063':('easy','dot_int_radio',{'a':['1','0','2'],'d':['-2','1','8']}),
'q-128091':('easy','dot_int_radio',{'a':['-1','1','0'],'d':['6','1','7']}),
'q-275347':('easy','dot_radical_cdot_blank',{'a':['-sqrt(3)','0','-2'],'d':['-sqrt(3)','10','-10']}),
'q-317302':('easy','dot_radical_parens_blank',{'a':['sqrt(7)','-2','5'],'d':['sqrt(7)','3','-1']}),
'q-317303':('easy','dot_radical_thin_blank',{'a':['-sqrt(8)','4','-3'],'d':['sqrt(8)','-1','2']}),
'q-317304':('easy','dot_radical_thin_blank',{'a':['0','5','sqrt(11)'],'d':['7','-2','sqrt(11)']}),
'q-275348':('moderate','cross_blank',{'a':['1','2','3'],'b':['-1','0','-2'],'c':['0','-2','1']}),
'q-73457':('moderate','cross_radio',{'a':['1','-3','2'],'b':['2','-1','-1'],'c':['3','-3','0']}),
'q-73458':('moderate','cross_radio',{'a':['-2','4','3'],'b':['-1','3','2'],'c':['2','-1','4']}),
'q-73459':('moderate','cross_radio',{'a':['-2','0','-1'],'b':['-2','-1','0'],'c':['3','1','4']}),
'q-20065':('moderate','cross_legacy_radio',{'a':['0','-2','3'],'b':['4','-2','1'],'c':['3','-1','2']})}
TEMPLATES={'easy':['dot_int_radio','dot_radical_cdot_blank','dot_radical_parens_blank','dot_radical_thin_blank'], 'moderate':['cross_radio','cross_blank','cross_legacy_radio'], 'hard':['cross_radio','cross_blank']}

def val(x):
 s=str(x)
 if not re.fullmatch(r'-?\d+|-?sqrt\(\d+\)',s): raise ValueError('coordinates must be integers or signed sqrt(n)')
 return sp.sympify(s)
def tex(x):
 s=str(x); m=re.fullmatch(r'(-?)sqrt\((\d+)\)',s)
 return m[1]+r'\sqrt{'+m[2]+'}' if m else sp.latex(sp.sympify(x))
def group(x):
 s=tex(x);return '('+s+')' if sp.sympify(x).could_extract_minus_sign() else s
def vtex(v,thin=False):return '⟨'+(','+r'\,' if thin else ',').join(map(tex,v))+'⟩'
def plus(parts):
 return ''.join(('+' if i and not x.startswith('-') else '')+x for i,x in enumerate(parts))
def dot(a,d):return sp.simplify(sum(val(x)*val(y) for x,y in zip(a,d)))
def cross(b,c):
 b=list(map(val,b));c=list(map(val,c));return [str(sp.simplify(b[1]*c[2]-b[2]*c[1])),str(sp.simplify(b[2]*c[0]-b[0]*c[2])),str(sp.simplify(b[0]*c[1]-b[1]*c[0]))]
def params(p):return {k:[str(x) for x in v] for k,v in p.items()}
def guard(level,template,p):
 expected={'a','d'} if template.startswith('dot_') else {'a','b','c'}
 if set(p)!=expected or any(len(v)!=3 for v in p.values()):raise ValueError('exact three-coordinate vector keys required')
 values=[val(x) for v in p.values() for x in v]
 if level=='easy':
  for k,v in p.items():
   for x in v:
    m=re.fullmatch(r'-?sqrt\((\d+)\)',x)
    if m:
     n=int(m[1]);
     if not 2<=n<=15 or sp.sqrt(n).is_Integer:raise ValueError('nonsquare radicand 2..15')
    elif abs(int(x))>(5 if k=='a' else 10):raise ValueError('easy component ceiling')
  rad=[i for i in range(3) if 'sqrt' in p['a'][i] or 'sqrt' in p['d'][i]]
  if 'radical' in template:
   if len(rad)!=1 or not all('sqrt' in p[k][rad[0]] for k in ['a','d']) or val(p['a'][rad[0]])**2!=val(p['d'][rad[0]])**2:raise ValueError('exactly one paired equal-radicand product')
  elif rad:raise ValueError('integer template')
 else:
  if any(not x.is_Integer for x in values):raise ValueError('cross families use integers')
  ceiling=4 if level=='moderate' else 5
  if any(abs(x)>ceiling for x in values):raise ValueError('level component ceiling')
  if level=='hard':
   d=cross(p['b'],p['c'])
   if any(x==0 for x in values) or not any(abs(x)==5 for x in values) or any(val(x)==0 for x in d):raise ValueError('hard requires nine nonzero inputs, magnitude 5 and three nonzero cross components')
 # Arithmetic ceilings preserve source-style hand computation.
 d=p.get('d') or cross(p['b'],p['c'])
 if abs(dot(p['a'],d))>(100 if level=='easy' else 200 if level=='moderate' else 375):raise ValueError('answer workload ceiling')

def render(template,p,raw=False):
 a=p['a'];thin=template=='dot_radical_thin_blank';av=vtex(a,thin)
 blank=template.endswith('_blank')
 if template.startswith('dot_'):
  d=p['d'];dv=vtex(d,thin)
  prompt=rf'Find $a\cdot (b\times c)$ given that $a={av}$ and $b\times c={dv}.$'
  if 'parens' in template or thin: row='+'.join('('+tex(x)+')('+tex(y)+')' for x,y in zip(a,d))
  else:row='+'.join(group(x)+r'\cdot '+group(y) for x,y in zip(a,d))
  rows=[rf'\begin{{aligned}}a\cdot (b\times c) & ={av}\cdot {dv}',row]
  if 'radical' in template:rows.append(plus([tex(val(x)*val(y)) for x,y in zip(a,d)]))
  rows.append(tex(dot(a,d))+'.')
  solution='Substituting given vectors into the formula for the scalar triple product, we obtain \n\n$$\n'+rows[0]+''.join(r' \\  & ='+r for r in rows[1:])+r'\end{aligned}'+'\n$$'
 else:
  b,c=p['b'],p['c'];d=cross(b,c);bv,cv=vtex(b),vtex(c)
  prompt=rf'Given that $a={av},$ $b={bv},$ and $c={cv},$ find $a\cdot (b\times c)$ using the definition of the scalar triple product.'
  if template=='cross_legacy_radio':
   def spaced(v):return '⟨'+tex(v[0])+','+tex(v[1])+', '+tex(v[2])+'⟩'
   op=r'\cdot' if raw else r'\times'
   prompt=rf'Given that $a = {spaced(a)}$, $b = {spaced(b)}$, and $c = {spaced(c)}$, find $a \cdot (b {op} c)$ using the definition of the scalar triple product.'
  def mat(rows):return r'|\begin{aligned}'+r' \\ '.join(' & '.join(r) for r in rows)+r'\end{aligned}|'
  parts=[mat([[tex(b[i]),tex(b[j])],[tex(c[i]),tex(c[j])]]) for i,j in [(1,2),(0,2),(0,1)]]
  # Cross-product determinant only: definition lesson's two operative phases.
  minor=[group(b[1])+r'\cdot '+group(c[2])+'-'+group(b[2])+r'\cdot '+group(c[1]),group(b[0])+r'\cdot '+group(c[2])+'-'+group(b[2])+r'\cdot '+group(c[0]),group(b[0])+r'\cdot '+group(c[1])+'-'+group(b[1])+r'\cdot '+group(c[0])]
  if blank:minor[1]=group(b[0])+r'\cdot '+group(c[2])+'-'+group(c[0])+r'\cdot '+group(b[2]) # source commuted second product
  basis=plus([('' if val(x)==1 else '-' if val(x)==-1 else tex(x))+v for x,v in zip(d,'ijk')])
  cr=[mat([['i','j','k'],list(map(tex,b)),list(map(tex,c))]),parts[0]+'i-'+parts[1]+'j+'+parts[2]+'k','('+minor[0]+')i-('+minor[1]+')j+('+minor[2]+')k',basis,vtex(d)]
  sol1=r'\begin{aligned}b\times c & ='+cr[0]+''.join(r' \\  & ='+r for r in cr[1:])+r'\end{aligned}'
  dr=[av+r'\cdot '+vtex(d),'+'.join(group(x)+r'\cdot '+group(y) for x,y in zip(a,d))]
  if blank:dr.append(plus([tex(val(x)*val(y)) for x,y in zip(a,d)]))
  dr.append(tex(dot(a,d))+('' if blank else '.'))
  sol2=r'\begin{aligned}a\cdot (b\times c) & ='+dr[0]+''.join(r' \\  & ='+r for r in dr[1:])+r'\end{aligned}'
  solution='First, we find the cross product:\n\n$$\n'+sol1+'\n$$\n\nNow, we can compute the scalar triple product:\n\n$$\n'+sol2+'\n$$'
 if blank:prompt+='\n\n'+r'$a\cdot (b\times c)=$'+'\n{{field-1}}'
 return prompt,solution

def bank(p,profile):
 a=p['a'];d=p.get('d') or cross(p['b'],p['c']);t=dot(a,d)
 if profile.startswith(('source:','completed:')):
  qid=profile.split(':',1)[1];_,_,anchor=SPECS[qid];t0=dot(anchor['a'],anchor.get('d') or cross(anchor['b'],anchor['c']))
  values=[sp.simplify(t+val(c[':answer/value'])-t0) for c in QUESTIONS[qid][':question/answer-fields'][0][':answer-field/choices']]
  return values,['opaque empirical scalar residual']*len(values)
 products=[val(x)*val(y) for x,y in zip(a,d)]
 if profile=='dot_operations':
  return [t,sum(val(x)+val(y) for x,y in zip(a,d)),sum(val(x)**2 for x in a),sum(val(x)**2 for x in d),sum(val(x)*val(y) for x,y in zip(a,reversed(d)))],['correct','add instead of multiply each pair','use a for both dot operands','use supplied cross vector for both dot operands','reverse supplied cross components']
 if profile=='cross_operations':
  b,c=list(map(val,p['b'])),list(map(val,p['c']));wrongj=[val(d[0]),-val(d[1]),val(d[2])];omitsecond=[b[1]*c[2],-b[0]*c[2],b[0]*c[1]]
  return [t,sum(val(x)*y for x,y in zip(a,wrongj)),sum(val(x)*y for x,y in zip(a,omitsecond)),t-products[0],t-products[2]],['correct','omit cofactor minus on j','omit second term of each cross component','omit first dot component','omit third dot component']
 if profile=='blank':return [t],['correct']
 raise ValueError('unsupported complete profile')

def sample(level,template,rng):
 if level=='easy':
  a=[str(rng.randint(-5,5)) for _ in range(3)];d=[str(rng.randint(-10,10)) for _ in range(3)]
  if 'radical' in template:
   i=rng.randrange(3);n=rng.choice([2,3,5,6,7,8,10,11,12,13,14,15]);a[i]=rng.choice(['','-'])+f'sqrt({n})';d[i]=rng.choice(['','-'])+f'sqrt({n})'
  return {'a':a,'d':d}
 return {k:[str(rng.randint(-4,4) if level=='moderate' else rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5])) for _ in range(3)] for k in ['a','b','c']}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in TEMPLATES:raise ValueError('unknown difficulty')
 rng=random.Random(seed)
 if profile and profile.startswith(('source:','completed:')):
  qid=profile.split(':',1)[1]
  if qid not in SPECS:raise ValueError('unknown source')
  if profile.startswith('completed:') and qid!='q-20065':raise ValueError('only the incomplete source has an authored completion profile')
  sl,st,_=SPECS[qid]
  if level!=sl or template not in [None,st]:raise ValueError('source template/level mismatch')
  template=st
 candidates=[t for t in TEMPLATES[level] if t!='cross_legacy_radio' and (not field_type or t.endswith('_'+field_type))]
 template=template or rng.choice(candidates)
 if template not in TEMPLATES[level]:raise ValueError('level/template mismatch')
 ft='blank' if template.endswith('_blank') else 'radio'
 if field_type and field_type!=ft:raise ValueError('field type mismatch')
 profile=profile or ('blank' if ft=='blank' else 'dot_operations' if level=='easy' else 'cross_operations')
 if profile=='blank' and ft!='blank' or profile in ['dot_operations','cross_operations'] and ft!='radio':raise ValueError('profile/field mismatch')
 if profile=='dot_operations' and not template.startswith('dot_') or profile=='cross_operations' and not template.startswith('cross_'):raise ValueError('profile/method mismatch')
 for _ in range(10000):
  p=params(parameters) if parameters is not None else sample(level,template,rng)
  try:
   guard(level,template,p)
   vs,recipes=bank(p,profile)
   if len(set(map(str,map(sp.simplify,vs))))!=len(vs):raise ValueError('ambiguous whole bank')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('no eligible whole instance')
 raw=profile.startswith('source:');qid=profile.split(':',1)[1] if raw else None
 prompt,solution=render(template,p,raw)
 q={':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level}
 if raw:
  original=QUESTIONS[qid]
  for k in [':question/worked-solution',':question/difficulty']:
   if k not in original:q.pop(k)
 # Content identity excludes seed/order/profile spelling; mathematical identity excludes banks.
 canonical={k:[sp.srepr(val(x)) for x in v] for k,v in sorted(p.items())}
 task={'method':'supplied-cross-dot' if template.startswith('dot_') else 'cross-then-dot','vectors':canonical}
 fp=hashlib.sha256(json.dumps(task,sort_keys=True).encode()).hexdigest()
 has_correct=not raw or ':answer-field/correct' in QUESTIONS[qid][':question/answer-fields'][0]
 assigned=tex(dot(p['a'],p.get('d') or cross(p['b'],p['c']))) if has_correct else None
 identity={'version':VERSION,'question':q,'field_type':ft,'bank':sorted(map(tex,vs)),'correct_assignment':{'present':has_correct,'value':assigned}}
 key=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
 uid=lambda s:str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+key+':'+s))
 choices=[{':answer/id':uid('answer:'+tex(v)),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in vs]
 t=dot(p['a'],p.get('d') or cross(p['b'],p['c']));correct=next(c[':answer/id'] for c in choices if val(c[':answer/value'])==t)
 rng.shuffle(choices)
 field={':answer-field/id':uid('field'),':answer-field/key':'field-1' if ft=='blank' else 'selection',':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}
 if raw and ':answer-field/correct' not in QUESTIONS[qid][':question/answer-fields'][0]:field.pop(':answer-field/correct')
 q[':question/id']=uid('question');q[':question/answer-fields']=[field]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'level':level,'template':template,'profile':profile,'parameters':p,'mathematical_fingerprint':fp,'content_fingerprint':key,'recipes':recipes,'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'evidence_only':profile.startswith(('source:','completed:')),'eligible_for_learning':not profile.startswith(('source:','completed:')),'authored_completion':template=='cross_legacy_radio' and not raw,'authored_level':level=='hard','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
# Easy: supplied cross product; each family is an unordered same-method variant.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: cross followed by dot, observed signed integer workload.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: authored dense signed arithmetic, with identical cross-then-dot method.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];s=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):s+='\n'.join(c[':answer/value'] for c in f[':answer-field/choices'])+'\n'
 return s+'\n'+q.get(':question/worked-solution','[raw source has no worked solution]')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ns=ap.parse_args()
 records=[generate(level,ns.seed+i,template=ns.template,profile=ns.profile) for level in (TEMPLATES if ns.difficulty=='all' else [ns.difficulty]) for i in range(ns.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if ns.format=='json' else '\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
