#!/usr/bin/env python3
"""Private basis2275 draft: direct trig primitives and constant/sum rules only.

Raw profiles are parameterized source masks (including omissions/errors), never
served as learning material. Easy: one integer coefficient. Moderate: observed
integer two-term sums. Hard: authored two noninteger rational coefficients using
identical primitive/decomposition stages; no substitution or extra trig products.
"""
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts/question_capture'))
import math_format as MF
HERE=Path(__file__).with_suffix('');RECIPES=json.loads((HERE/'recipes.json').read_text())
KP_ID=17592186064179;KP_UUID='e617f241-254b-5f70-9937-5883b6f28c4f';TITLE='Integrating Secant-Tangent and Cosecant-Cotangent';VERSION='2.0.0-draft';SOURCE_BASIS=2275
SUPPORTED_LEVELS=('easy','moderate','hard')
# Complete profiles precede parameter selection. Fieldless originals get a
# separately authored five-operation bank; raw field absence stays exact.
BANKS={'easy':('q-113920','q-71656','q-71659','q-71657'),'moderate':('q-113926','q-113928','q-113930','q-113923','q-113925'),'hard':('q-113926','q-113930','q-113923')}
RATIONALS=tuple(str(sp.Rational(n,d)) for d in range(2,6) for n in range(3,19) if sp.Rational(n,d).q==d and 1<sp.Rational(n,d)<9)

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def render(t,p):
 vals={k:sp.latex(sp.Rational(v)) for k,v in p.items()};vals['unit']='' if p.get('a')==1 else vals.get('a','')
 vals['sum']=sp.latex(sum(sp.Rational(v) for v in p.values()))
 return re.sub(r'\{(a|b|sum|unit)\}',lambda m:vals[m[1]],t)
def clean(t):
 # Defensive legacy normalization; frozen decoded source uses real Unicode.
 return t.replace(r'\u2061','⁡').replace('\\\\','\\') if '\\u2061' in t else t

def expression(text):
 """Small independent readback parser for actual rendered source notation."""
 text=text.replace(r'\u2061','').replace('⁡','').replace('θ','theta').replace(r'\theta','theta')
 # Defensive parser accepts legacy slash escaping; frozen source has ordinary single backslashes.
 text=text.replace('\\\\','\\')
 text=re.sub(r'\\operatorname\{(sin|cos|sec|csc|tan|cot)\}',r'\1',text)
 text=re.sub(r'\\(sin|cos|sec|csc|tan|cot)',r'\1',text)
 text=text.replace(r'\,','').replace(r'\displaystyle','').strip().rstrip('.,')
 text=text.replace(r"\left", "").replace(r"\right", "");text=re.sub(r"(sin|cos|sec|csc|tan|cot)\{([^{}]*)\}",r"\1\2",text)
 while r'\frac' in text:
  text=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',text)
 text=re.sub(r'\{(sin|cos|sec|csc|tan|cot)\}\^\{(\d+)\}',r'\1**\2',text)
 text=re.sub(r'(sin|cos|sec|csc|tan|cot)\^\{(\d+)\}',r'\1**\2',text)
 text=re.sub(r'(sin|cos|sec|csc|tan|cot)(?:\*\*(\d+))?\s*(theta|x|y)',lambda m:m[1]+'('+m[3]+')'+('**'+m[2] if m[2] else ''),text)
 loc={n:sp.Symbol(n,real=True) for n in ('x','y','theta','C')};loc.update({n:getattr(sp,n) for n in ('sin','cos','sec','csc','tan','cot')})
 return parse_expr(text,local_dict=loc,transformations=standard_transformations+(implicit_multiplication_application,))

def zero(e):
 args=sorted({f.args[0] for f in e.atoms(sp.Function)},key=str);subs={};pairs=[]
 for j,v in enumerate(args):
  S,T=sp.symbols('_s'+str(j)+' _c'+str(j));pairs.append((S,T));subs.update({sp.sin(v):S,sp.cos(v):T,sp.tan(v):S/T,sp.cot(v):T/S,sp.sec(v):1/T,sp.csc(v):1/S})
 num=sp.fraction(sp.cancel(e.xreplace(subs)))[0]
 for S,T in pairs:
  if num!=0:num=sp.rem(num,S**2+T**2-1,S)
 return sp.expand(num)==0

def integrand(prompt):
 text=re.search(r'\\int\s+(.*?)(?:\\text\{d\}|\\textrm\s*d|d[xyθ])',prompt)[1]
 return expression(text)

def primitive(e,v):
 # Only the six taught primitive patterns; normal prompts use four of them.
 fns=[(sp.sec(v)*sp.tan(v),sp.sec(v)),(sp.csc(v)*sp.cot(v),-sp.csc(v)),(sp.sin(v),-sp.cos(v)),(sp.cos(v),sp.sin(v))]
 out=0
 for term in sp.Add.make_args(sp.expand(e)):
  for f,F in fns:
   c=sp.cancel(term/f)
   if not c.has(v):out+=c*F;break
  else:raise ValueError('outside direct primitive scope: '+str(term))
 return out

def parameters_ok(k,level,p,raw=False):
 keys=set(RECIPES[k]['parameters']);assert set(p)==keys,'parameter keys'
 p={a:sp.Rational(v) for a,v in p.items()}
 if raw:
  if any(not v.is_Integer or not 1<=v<=12 for v in p.values()):raise ValueError('raw positive integer coefficients 1..12')
 elif level=='hard':
  if keys!={'a','b'} or any(str(v) not in RATIONALS for v in p.values()):raise ValueError('hard needs two reduced noninteger rational coefficients in declared domain')
 else:
  if any(not v.is_Integer or not 1<=v<=12 for v in p.values()):raise ValueError('integer coefficient bounds 1..12')
  if k=='q-71659' and p['a']<2:raise ValueError('power bank needs nonunit a')
 return {a:int(v) if v.is_Integer else str(v) for a,v in p.items()}

def authored_bank(k,p,correct):
 v=sp.Symbol(RECIPES[k]['variable'],real=True);e=integrand(render(RECIPES[k]['prompt'],p));terms=sp.Add.make_args(sp.expand(e));parts=[primitive(t,v) for t in terms]
 if len(parts)==1:
  F=parts[0];a=sp.Rational(p['a']);vals=[F,-F,a*sp.sec(v),-a*sp.sec(v),e]
 else:
  A,B=parts;vals=[correct,-A+B,A-B,-correct,e]
 return [sp.latex(f)+r'+C' for f in vals]

def assemble(level,k,p,raw,seed):
 t=RECIPES[k];prompt=render(t['prompt'],p);q={':question/problem':prompt};fields=[]
 if 'solution' in t:q[':question/worked-solution']=render(t['solution'],p)
 if 'difficulty' in t:q[':question/difficulty']=t['difficulty']
 if t.get('has_fields'):q[':question/answer-fields']=fields
 v=sp.Symbol(t['variable'],real=True);e=integrand(prompt);F=primitive(e,v) # correct first, then bank/stages
 for f in t['fields']:
  af={':answer-field/key':f['key'],':answer-field/type':f['type'],':answer-field/choices':[]}
  for a in f['choices']:
   av={':answer/type':a['type'],':answer/value':render(a['value'],p)}
   if 'feedback' in a:av[':answer/feedback']=render(a['feedback'],p)
   af[':answer-field/choices'].append(av)
  if 'correct' in f:af['_correct_index']=f['correct']
  fields.append(af)
 if not raw:
  q[':question/difficulty']=':question.difficulty/'+level
  # Repair exactly the stray cos in fieldless q113925's distributed sum.
  if k=='q-113920':
   fields[0][':answer-field/choices'][0][':answer/value']=render(r'{a}csc⁡xcot⁡x+C',p)
  if k=='q-113925':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\operatorname{cos}\operatorname{csc}',r'\operatorname{csc}')
  if not fields:
   values=authored_bank(k,p,F)
   fields.append({':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':s} for s in values],'_correct_index':0})
  q[':question/answer-fields']=fields
  for key in (':question/problem',':question/worked-solution'):q[key]=MF.normalize_prose(clean(q[key]))
  for f in fields:
   for a in f[':answer-field/choices']:a[':answer/value']=MF.normalize_tex(clean(a[':answer/value']))
  # In normal source-shaped output every complete antiderivative option is
  # checked modulo arbitrary constants, including wrong/wrong equivalence.
  for f in fields:
   vals=[expression(a[':answer/value']) for a in f[':answer-field/choices']]
   ci=f['_correct_index']
   if not zero(sp.diff(vals[ci],v)-e):raise ValueError('incorrect bank key')
   for i,a in enumerate(vals):
    if any(zero(sp.diff(a-b,v)) for b in vals[:i]):raise ValueError('equivalent antiderivative options')
   if sum(zero(sp.diff(a,v)-e) for a in vals)!=1:raise ValueError('ambiguous bank')
 # Identity derives from actual rendered content, no source/profile alias or
 # unused parameter data. Bank order is incidental; level is material.
 content=digest({'version':VERSION,'q':{k:v for k,v in q.items() if k!=':question/answer-fields'},'fields':[{k:v for k,v in f.items() if k not in (':answer-field/choices','_correct_index')}|{'bank':sorted(f[':answer-field/choices'],key=lambda a:json.dumps(a,sort_keys=True)),'correct':f[':answer-field/choices'][f['_correct_index']][':answer/value'] if '_correct_index' in f else None} for f in fields]})
 qid=uid('question:'+content);q[':question/id']=qid
 for j,f in enumerate(fields):
  fid=uid(qid+':field:'+str(j));f[':answer-field/id']=fid
  for a in f[':answer-field/choices']:a[':answer/id']=uid(fid+':answer:'+digest(a))
  if '_correct_index' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][f.pop('_correct_index')][':answer/id']]
  random.Random(str(seed)+fid).shuffle(f[':answer-field/choices'])
 fp=digest(sp.srepr(sp.expand(e.subs(v,sp.Symbol('x',real=True)))))
 out={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':k,'bank_profile':('raw_' if raw else 'method_')+k,'parameters':p,'parameter_fingerprint':fp,'content_fingerprint':content,'source_basis':SOURCE_BASIS,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','source_ids':[k],'domain':'Real intervals excluding sin/cos poles of the complete displayed bank; arbitrary C.','plot_rating':'none','evidence_only':raw,'eligible_for_learning':not raw,'difficulty_origin':'authored rational-coefficient extension; no observed hard label' if level=='hard' else 'original observed label' if 'difficulty' in t else 'authored; original unrated','math_format':MF.FORMAT_VERSION}}
 if not raw:MF.validate_generated_record(out)
 return out

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('field type')
 raw=bool(profile and profile.startswith('raw_'));k=(profile.removeprefix('raw_').removeprefix('method_') if profile else template)
 if template and k and template!=k:raise ValueError('template/profile mismatch')
 rng=random.Random(seed);k=k or rng.choice(BANKS[level])
 if k not in RECIPES or (not raw and k not in BANKS[level]):raise ValueError('ineligible bank')
 if raw and RECIPES[k]['level']!=level:raise ValueError('raw replay level')
 if parameters is not None:p=parameters_ok(k,level,parameters,raw)
 else:
  p=parameters_ok(k,level,{a:rng.choice(RATIONALS) if level=='hard' and not raw else rng.randint(2 if k=='q-71659' else 1,12) for a in RECIPES[k]['parameters']},raw)
 return assemble(level,k,p,raw,seed)

# Easy: one constant multiple, observed primitive recognition/sign bookkeeping.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: two direct primitive terms, integer coefficients and source stages.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard (authored): same two-term method, two noninteger reduced coefficients.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 levels=SUPPORTED_LEVELS if a.difficulty=='all' else (a.difficulty,);rs=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
 if a.format=='json':print(json.dumps(rs,indent=2,ensure_ascii=False))
 else:
  for r in rs:
   q=r['question'];print(q[':question/problem']);print('\n'.join(x[':answer/value'] for f in q.get(':question/answer-fields',[]) for x in f[':answer-field/choices']));print(q.get(':question/worked-solution','[Original solution absent]'))
if __name__=='__main__':main()
