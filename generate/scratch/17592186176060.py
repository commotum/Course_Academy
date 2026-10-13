#!/usr/bin/env python3
"""Cosecant oddness generators, math basis 1356; stop after steps 3–7.

Easy: one oddness substitution. Moderate (authored missing-level claim): remove
one nonzero whole-period shift then apply oddness, as in the canonical example.
Hard: the same two substitutions plus nonunit multiplication and nonzero offset,
following both labeled hard solutions. Bounds/complete banks apply to explicit
calls as well as samplers. No graph reconstruction or arbitrary-angle evaluation.

Public raw_<source-id> profiles are parameterized EVIDENCE ONLY: they preserve
missing attribute presence and historical complete banks. The two hard opaque
banks use explicitly uninterpreted proportional evidence masks, never defaults.
Raw replay does not return stored source question payloads. Normal presentation
uses each family's original shared prose and ordered symbolic/arithmetic stages.
Question IDs depend on actual displayed content and level; task fingerprints
exclude notation aliases, seed, banks, variable letters and whole-period aliases.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186176060
KP_UUID='48a710f9-fed1-5fdb-b4c0-fd3ae2d4d8a4'
TITLE='Utilizing the Oddness Property of the Cosecant Function'
VERSION='cosecant-oddness-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
GRAPH='images/a8/a8e7894ea970c539ca59a73713fa15450f4361b3fc8bc22183e3fe84946411bd.png'
C=r'\operatorname{csc}⁡'
EASY_PREFIX=QUESTIONS['q-136554'][':question/worked-solution'].split('Therefore,')[0]
HARD_PREFIX=QUESTIONS['q-158069'][':question/worked-solution'].split('$$\n\\begin{aligned}')[0]
TEMPLATES={'easy_integer':'easy','easy_rational':'easy','easy_radical':'easy',
 'moderate_periodic':'moderate','hard_integer':'hard','hard_rational':'hard',
 'legacy_simple':'easy','legacy_shift':'moderate'}
CASES=[
 ('q-136605','legacy_shift',{'v':'-6','n':5,'a':1,'b':0,'variable':'x'}),
 ('q-136614','legacy_simple',{'v':'7','n':0,'a':1,'b':0,'variable':'x'}),
 ('q-136554','easy_integer',{'v':'-3','n':0,'a':1,'b':0,'variable':'a'}),
 ('q-158065','easy_rational',{'v':'11/4','n':0,'a':1,'b':0,'variable':'a'}),
 ('q-158066','easy_radical',{'v':'sqrt(5)','n':0,'a':1,'b':0,'variable':'a'}),
 ('q-158069','hard_integer',{'v':'-4','n':-9,'a':3,'b':-7,'variable':'x'}),
 ('q-158071','hard_rational',{'v':'7/6','n':3,'a':4,'b':1,'variable':'x'})]
RAW={f'raw_{sid}':(sid,t,p) for sid,t,p in CASES}
PROFILES={'sign_reciprocal','radical_square','period_output','outer_operations',*RAW}

def tex(v): return sp.latex(sp.simplify(v)).replace("- ", "-")
def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(value): return str(uuid.uuid5(uuid.UUID(KP_UUID),value))
def scalar(s):
 v=sp.sympify(s,locals={'sqrt':sp.sqrt})
 if v.free_symbols or v.is_real is not True or v.is_finite is not True: raise ValueError('v must be a finite real exact scalar')
 return sp.simplify(v)
def normalized(p):
 if set(p)-{'v','n','a','b','variable'}: raise ValueError('unknown parameters')
 return {'v':scalar(p['v']),'n':sp.sympify(p.get('n',0)),'a':sp.sympify(p.get('a',1)),
         'b':sp.sympify(p.get('b',0)),'variable':p.get('variable','a')}
def number_form(v):
 if v.is_Integer: return 'integer'
 if v.is_Rational: return 'rational'
 if (v*v).is_Integer and not v.is_Rational: return 'radical'
 raise ValueError('supported forms are integers, proper nonintegral rationals, and signed square roots')
def guard(level,t,p,raw=False):
 v,n,a,b=p['v'],p['n'],p['a'],p['b']; form=number_form(v)
 if abs(v)<=1 or abs(v)>17: raise ValueError('1 < |csc value| <= 17 required')
 if p['variable'] not in ('a','x','t','theta'): raise ValueError('unsupported angle variable')
 if not n.is_Integer or abs(n)>12: raise ValueError('integer period multiplier with |n| <= 12 required')
 if not a.is_Integer or not b.is_Integer: raise ValueError('integer outer coefficients required')
 if form=='rational' and (abs(v.p)>17 or v.q>6): raise ValueError('reduced rational bounds |numerator|<=17, denominator<=6')
 if form=='radical' and v*v not in (2,3,5,6,7,10,11,13): raise ValueError('squarefree radicand 2..13')
 if level=='easy' and (n!=0 or a!=1 or b!=0): raise ValueError('easy requires only oddness')
 if level=='moderate' and (n==0 or a!=1 or b!=0): raise ValueError('moderate requires a nonzero whole-period shift only')
 if level=='hard' and (n==0 or not 2<=abs(a)<=6 or not 1<=abs(b)<=9 or form=='radical'): raise ValueError('hard requires nonunit multiplier, nonzero offset and integer/rational value')
 if t.endswith('_integer') and form!='integer': raise ValueError('integer family required')
 if t.endswith('_rational') and form!='rational': raise ValueError('rational family required')
 if t.endswith('_radical') and form!='radical': raise ValueError('radical family required')

def profile_for(t):
 return 'radical_square' if t=='easy_radical' else ('outer_operations' if TEMPLATES[t]=='hard' else ('period_output' if TEMPLATES[t]=='moderate' else 'sign_reciprocal'))
def bank(profile,p):
 v,n,a,b=p['v'],p['n'],p['a'],p['b']; correct=-a*v+b
 if profile=='sign_reciprocal': vals=[v,0,-v,1/v,-1/v]; recipes=['unchanged','zero','oddness','reciprocal','negative reciprocal']
 elif profile=='radical_square': vals=[-v,v,1,-v*v,v*v]; recipes=['oddness','unchanged','unit','negative square','square']
 elif profile=='period_output': vals=[-v+2*n*sp.pi,v+2*n*sp.pi,v,0,-v];recipes=['shift output after oddness','shift output unchanged','unchanged','zero','periodicity and oddness']
 elif profile=='outer_operations': vals=[correct,a*v+b,-a*v-b,-v+b,-a/v+b];recipes=['correct','omit oddness','reverse offset','omit multiplier','confuse reciprocal']
 elif profile in RAW:
  sid=RAW[profile][0]
  if sid in ('q-136614','q-136554'): vals=[v,0,-v,1/v,-1/v];recipes=['unchanged','zero','oddness','reciprocal','negative reciprocal']
  elif sid=='q-136605': return bank('period_output',p)
  elif sid=='q-158066': return bank('radical_square',p)
  elif sid=='q-158065': vals=[v-1,1/v,1-v,-v,v];recipes=['observed subtract unit (intent unresolved)','reciprocal','observed reverse subtract-unit','oddness','unchanged']
  else:
   # Transparent, uninterpreted evidence parametrization. These ratios only
   # preserve the complete historical numeric bank; no error intent is claimed.
   ratios={'q-158069':[sp.Rational(9,5),-3,sp.Rational(2,5),1,sp.Rational(-19,5)],
           'q-158071':[1,sp.Rational(-1,22),sp.Rational(-17,11),sp.Rational(15,22),sp.Rational(5,22)]}[sid]
   vals=[r*correct for r in ratios]; recipes=['opaque proportional evidence mask '+str(r) for r in ratios]
 else: raise ValueError('unknown bank')
 vals=[sp.simplify(x) for x in vals]
 if any(x.is_real is not True or x.is_finite is not True for x in vals): raise ValueError('invalid whole bank')
 if any(sp.simplify(x-y)==0 for i,x in enumerate(vals) for y in vals[i+1:]): raise ValueError('ambiguous whole bank')
 if sum(sp.simplify(x-correct)==0 for x in vals)!=1: raise ValueError('bank lacks unique correct value')
 return vals,recipes

def display_variable(p):
 return r'\theta' if p['variable']=='theta' else p['variable']

def angle(p,expanded=False):
 v=display_variable(p);n=int(p['n'])
 if not n:return '-'+v
 return '-'+v+('+' if n>0 else '-')+(r'2\pi \cdot '+str(abs(n)) if expanded else str(2*abs(n))+r'\pi ')
def aff(term,a,b):
 coefficient='' if a==1 else ('-' if a==-1 else tex(a))
 return coefficient+term+('+'+tex(b) if b>0 else tex(b) if b<0 else '')
def align(rows): return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def odd_rows(p,var):
 v=p['v']; rows=[C+'(-'+var+') & =-'+C+var]
 if v<0: rows+=[' & =-('+tex(v)+')',' & ='+tex(-v)+'.']
 else: rows+=[' & ='+tex(-v)+'.']
 return rows

def prompt(t,p):
 v=tex(p['v']);var=display_variable(p)
 if t=='legacy_simple': return 'If $\\csc '+var+' = '+v+'$, then $\\csc (-'+var+') =$'
 if t=='legacy_shift':
  n=int(p['n']);return 'If $\\csc '+var+' ='+v+'$, then $\\csc (-'+var+' '+('+' if n>0 else '-')+' '+str(2*abs(n))+'π) =$'
 term=C+'('+angle(p)+')'
 return 'If $'+C+var+'='+v+',$ then $'+aff(term,p['a'],p['b'])+'=$'

def solution(level,p):
 var=display_variable(p);v=p['v'];a=p['a'];b=p['b'];n=p['n']
 if level=='easy': return EASY_PREFIX+'Therefore,\n\n'+align(odd_rows(p,var))
 sol=HARD_PREFIX+align([C+'('+angle(p)+') & ='+C+'('+angle(p,True)+')',' & ='+C+'(-'+var+').'])
 sol+='\n\n- Secondly, using the oddness of $'+C+'x,$ we have\n\n'+align(odd_rows(p,var))
 if level=='moderate':return sol+'\n\nTherefore, $'+C+'('+angle(p)+') = '+tex(-v)+'.$'
 term=aff(C+'('+angle(p)+')',a,b)
 sol+='\n\nTherefore, \n\n'+align([term+' & ='+aff('('+tex(-v)+')',a,b),' & ='+aff(tex(-a*v),1,b),' & ='+tex(-a*v+b)+'.'])
 return sol

def sample(rng,level,t):
 form=t.split('_')[-1]
 if form not in ('integer','rational','radical'):form=rng.choice(['integer','rational','radical'] if level!='hard' else ['integer','rational'])
 if form=='integer': v=sp.Integer(rng.randint(2,12))
 elif form=='rational':
  den=rng.randint(2,6);v=sp.Rational(rng.randint(den+1,17),den)
  if v.is_Integer:return sample(rng,level,t)
 else:v=sp.sqrt(rng.choice([2,3,5,6,7,10,11,13]))
 v*=rng.choice([-1,1]);return {'v':str(v),'n':0 if level=='easy' else rng.choice([*range(-12,0),*range(1,13)]),
  'a':rng.randint(2,6) if level=='hard' else 1,'b':rng.choice([*range(-9,0),*range(1,10)]) if level=='hard' else 0,'variable':'a' if level=='easy' else 'x'}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio field supported')
 rng=random.Random(seed);raw=profile in RAW
 if raw:
  sid,rt,rp=RAW[profile];template=template or rt
  if template!=rt:raise ValueError('raw source/template mismatch')
 if template is None:template=rng.choice([t for t,l in TEMPLATES.items() if l==level and not t.startswith('legacy')])
 if TEMPLATES.get(template)!=level:raise ValueError('template difficulty mismatch')
 profile=profile or profile_for(template)
 if profile not in PROFILES:raise ValueError('unknown profile')
 if not raw and profile!=profile_for(template):raise ValueError('profile not eligible for family')
 # Complete family/profile is fixed before parameter sampling. No pooled repairs.
 for attempt in range(1000):
  p=normalized(parameters if parameters is not None else sample(rng,level,template))
  try: guard(level,template,p,raw);vals,recipes=bank(profile,p);break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('no valid complete-bank instance')
 problem=prompt(template,p);sol=solution(level,p);source=QUESTIONS[sid] if raw else None
 q={':question/problem':problem}
 if not raw or ':question/difficulty' in source:q[':question/difficulty']=':question.difficulty/'+level
 if not raw or ':question/worked-solution' in source:q[':question/worked-solution']=sol
 shown=[tex(x).replace(r' \pi','π') if raw and sid=='q-136605' else tex(x) for x in vals]
 content={'version':VERSION,'question':dict(q),'bank':sorted(shown),'field':'radio','correct_ref_present':not raw or ':answer-field/correct' in source[':question/answer-fields'][0]}
 content_hash=digest(content)
 ident=uid(content_hash);fid=uid(ident+'/selection')
 choices=[{':answer/id':uid(fid+'/'+sp.srepr(x)),':answer/type':':answer.type/math',':answer/value':shown[i]} for i,x in enumerate(vals)]
 rng.shuffle(choices)
 f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 correct=-p['a']*p['v']+p['b'];cid=uid(fid+'/'+sp.srepr(sp.simplify(correct)))
 if not raw or ':answer-field/correct' in source[':question/answer-fields'][0]:f[':answer-field/correct']=[':answer/id',cid]
 q[':question/answer-fields']=[f];q[':question/id']=ident
 # A whole-period shift aliases the same assessed scalar operation. Its sign and
 # value affect presentation, not mathematical tasks; moderate still has an
 # assessed removal stage absent at easy, and hard has its outer arithmetic.
 task={'level':level,'v':str(p['v']),'a':str(p['a']),'b':str(p['b']),'period_removal':level!='easy'}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
  'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,
  'parameters':{k:str(x) for k,x in p.items()},'source':{k:SOURCE[k] for k in ('database','basis','lineage')},
  'source_ids':[sid] if raw else [x for x,t,_ in CASES if t==template],
  'evidence_only':raw,'eligible_for_learning':not raw,'authorship':'observed evidence recipe' if raw else ('authored missing-level scope' if level=='moderate' else 'source-shaped method bank'),
  'recipes':recipes,'mathematical_fingerprint':digest(task),'content_fingerprint':content_hash,
  'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'domain':'real angle in cosecant domain; |csc(angle)|>1; n integer'}}

# Easy: direct oddness only; integer, rational and square-root forms preserve the
# same one-substitution workload. Reciprocal bank rejects the |v|=1 degeneracy.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: explicit authored gap between observed easy and hard; all samples
# require the additional whole-period removal but no outer arithmetic.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: source multiplication, component evaluation, offset arithmetic and final
# collected result remain separate rows; bounds prohibit a collapsed easy task.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
 q=r['question'];out=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  out+='\n'.join('- $'+a[':answer/value']+'$' for a in f.get(':answer-field/choices',[]))+'\n\n'
 return out+q.get(':question/worked-solution','[Raw capture has no worked solution.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
