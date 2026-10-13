#!/usr/bin/env python3
"""Spatial arc length, basis 1356. Ten interval-parameterized observed families.

Derivative stage masks preserve each source's complete sequence. Every interval
is integrated exactly; no literal question replay or answer lookup. Observed
scalar banks are evidence-only amplitude profiles (intent underdetermined),
except the logarithmic bank's explicit endpoint-expression shapes. Normal banks
use a complete authored speed/integration-operation profile. Intervals vary on
half-integer grids, with source arithmetic complexity preserved. No DB access.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,uuid,subprocess,os,tempfile
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().with_suffix('')
TEMPLATES=json.loads((HERE/'templates.json').read_text())
T=sp.Symbol('t',real=True)
VERSION='spatial-arc-1'
KP=17592186119860
TITLE='Computing the Arc Length of a Three-Dimensional Spatial Curve'

def expr(s):return sp.sympify(s,locals={'t':T,'E':sp.E})
def tex(x):
 x=sp.simplify(x)
 # Simplification must not introduce an unassessed hyperbolic-function branch.
 if x.has(sp.sinh,sp.cosh,sp.tanh,sp.coth,sp.sech,sp.csch):x=sp.expand(x.rewrite(sp.exp))
 return sp.latex(x).replace(' \\sqrt','\\sqrt').replace(r'\log',r'\ln')
def parse_tex(s):
 """Exact scalar/polynomial/trig parser used for displayed values, not metadata."""
 s=s.replace('⁡','').replace('\\,','').replace('\\:','').replace('\\left','').replace('\\right','').replace('\\operatorname{sin}','sin').replace('\\operatorname{cos}','cos').replace('\\sin','sin').replace('\\cos','cos').replace('\\ln','log').replace('\\log','log')
 s=s.replace('{sin}','sin').replace('{cos}','cos').replace('\\pi','pi').replace('\\text{ }','')
 def group(i):
  assert s[i]=='{';depth=1;j=i+1
  while depth:
   if s[j]=='{':depth+=1
   elif s[j]=='}':depth-=1
   j+=1
  return s[i+1:j-1],j
 while '\\frac' in s or '\\sqrt' in s:
  m=re.search(r'\\(frac|sqrt)',s);body,end=group(m.end())
  if m[1]=='frac':den,end=group(end);v='(('+parse_tex_string(body)+')/('+parse_tex_string(den)+'))'
  else:v='sqrt('+parse_tex_string(body)+')'
  s=s[:m.start()]+v+s[end:]
 s=parse_tex_string(s)
 s=re.sub(r'(?<=[0-9t)])(?=(?:sin|cos|log|sqrt)\()', '*', s)
 return parse_expr(s,local_dict={'t':T,'e':sp.E,'pi':sp.pi,'sqrt':sp.sqrt,'sin':sp.sin,'cos':sp.cos,'log':sp.log},transformations=standard_transformations+(implicit_multiplication_application,))
def parse_tex_string(s):
 # Recursive conversion happens through parse_tex for fraction/radical bodies.
 if '\\frac' in s or '\\sqrt' in s:return str(parse_tex(s))
 s=s.replace('{','(').replace('}',')').replace('^','**')
 s=re.sub(r'(sin|cos)\*\*\(2\)\s*(2?t)',r'\1(\2)**2',s)
 s=re.sub(r'(sin|cos|log)\s*(2?t)',r'\1(\2)',s)
 return s

def math_data(template,a,b):
 c=TEMPLATES[template];curve=[expr(x) for x in c['curve']];speed=expr(c['speed']);anti=sp.integrate(speed,T);L=sp.simplify(anti.subs(T,b)-anti.subs(T,a));return curve,speed,anti,L

def endpoint_rows(name,a,b,L):
 # Ordered arithmetic components retain endpoint substitution and evaluation.
 def par(x):return '('+tex(x)+')' if x<0 else tex(x)
 def evaluated(parts):return '+'.join(tex(x) for x in parts)
 if name=='product_trig':return [tex(b*b)+'-'+tex(a*a),tex(L)+'.']
 if name=='poly_negative':
  row=r'(\frac{'+par(b)+r'^{3}}{3}+2('+tex(b)+r'))-(\frac{'+par(a)+r'^{3}}{3}+2('+tex(a)+'))'
  upper=sp.Rational(1,3)*b**3+2*b;lower=sp.Rational(1,3)*a**3+2*a
  mid=tex(-a**3/3)+'+'+tex(-2*a) if b==0 and a<0 else tex(upper)+'-('+tex(lower)+')'
  return [row,mid,tex(L)]
 if name=='helix':return [r'\sqrt{2}('+tex(b)+'-'+tex(a)+')',tex(L)+'.']
 if name in ('poly_ordered','poly_constant','poly_radical'):
  anti=math_data(name,a,b)[2];terms=sp.Add.make_args(anti)
  # Source order: linear first except poly_constant.
  terms=sorted(terms,key=lambda x:sp.degree(x,T),reverse=name=='poly_constant')
  upper=evaluated([x.subs(T,b) for x in terms]);lower=sp.simplify(anti.subs(T,a));row=upper+'-'+('0' if lower==0 else '('+tex(lower)+')')
  return [row,tex(L)+'.']
 return [tex(L)+'.']

def solution(name,a,b,L):
 c=TEMPLATES[name];v={'a':tex(a),'b':tex(b)}
 if c['solution']:
  out=c['solution']
  for i,row in enumerate(endpoint_rows(name,a,b,L)):v['endpoint'+str(i)]=row
  for key,value in v.items():out=out.replace('@'+key+'@',value)
  if name=='product_trig' and a==0:out=out.replace('Notice that $t>0',r'Notice that $t\ge 0')
  # Three small source presentation repairs, retained separately in evidence.
  out=out.replace(r'(\operatorname{cos}⁡t))⟩',r'(\operatorname{cos}⁡t)⟩').replace(r'({t}^{2}))⟩',r'({t}^{2})⟩')
  out=out.replace(r'({t}^{2})\,\frac',r'({t}^{2}),\,\frac')
  return out
 return r"First, we find ${r}^{′}(t)$ and $‖{r}^{′}(t)‖:$"+'\n\n$$\n'+r'\begin{aligned}r^{\prime}(t)&=\langle 1/t,2,2t\rangle \\ \|r^{\prime}(t)\|&=\sqrt{1/t^2+4+4t^2} \\ &=\sqrt{(1/t+2t)^2} \\ &=1/t+2t\end{aligned}'+'\n$$\n\nNotice that $t>0$ for $t\\in ['+tex(a)+','+tex(b)+'].$\n\nTherefore, the arc length of the curve is\n\n$$\n'+r'\begin{aligned}L&=\int_{'+tex(a)+'}^{'+tex(b)+r'}\|r^{\prime}(t)\|\,\mathrm dt \\ &=\int_{'+tex(a)+'}^{'+tex(b)+r'}(1/t+2t)\,\mathrm dt \\ &=(\ln t+t^2)\big|_{'+tex(a)+'}^{'+tex(b)+r'} \\ &=\ln('+tex(b)+'/'+tex(a)+')+'+tex(b*b)+'-'+tex(a*a)+r' \\ &='+tex(L)+r'.\end{aligned}'+'\n$$'

def bank(name,a,b,speed,L,profile):
 c=TEMPLATES[name]
 if profile=='authored_operations':return [L,L/2,2*L,sp.integrate(speed**2,(T,a,b)),speed.subs(T,b)]
 if profile!='observed_'+c['source_id']:raise ValueError('Unknown or ineligible bank profile')
 if name=='log_square':return [1/b+b*b-2*a*a,b*b-a*a,b*b+a*a,1/(b*b)+b*b-2*a*a,L]
 # Explicit replay-only amplitude shapes. No recovered error intent is claimed.
 base=math_data(name,expr(str(c['a'])),expr(str(c['b'])))[3]
 return [sp.simplify(parse_tex(x)/base*L) for x in c['choice_shapes']]

def check_parameters(name,p):
 if set(p)!={'a','b'}:raise ValueError('Exactly a and b required')
 a,b=expr(str(p['a'])),expr(str(p['b']));c=TEMPLATES[name]
 if not (a.is_real and b.is_real and 0<float(b-a)<=5 and -3<=float(a)<float(b)<=5):raise ValueError('Bounds must increase, span <=5, within [-3,5]')
 if name=='log_square':
  if a<=0 or not all(x in (sp.Rational(1,2),sp.Integer(1),sp.Integer(2),sp.E) for x in (a,b)):raise ValueError('Log bounds limited to 1/2, 1, 2, e')
 elif name in ('quadratic_two','quadratic_three','product_trig','chain_product') and a<0:raise ValueError('This family requires t>=0')
 elif any(not x.is_Rational or x.q>2 for x in (a,b)):raise ValueError('Half-integer bounds required')
 return a,b

def render_plots(name,a,b,output_dir=HERE):
 if name!='log_square':return {}
 key=hashlib.sha256((str(a)+':'+str(b)).encode()).hexdigest()[:20];path=Path(output_dir)/('curve-'+key+'.png')
 if not path.exists():
  data={'a':float(a),'b':float(b),'a_label':tex(a),'b_label':tex(b),'coordinate_labels':[[tex(sp.log(x)),tex(2*x),tex(x*x)] for x in (a,b)],'output':str(path)}
  with tempfile.NamedTemporaryFile(mode='w',suffix='.json',dir=HERE,delete=False) as f:json.dump(data,f);input_path=f.name
  try:subprocess.run([os.sys.executable,str(HERE/'render_plot.py'),input_path],check=True,capture_output=True)
  finally:Path(input_path).unlink()
 return {'prompt':str(path)}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Invalid level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio observed')
 rng=random.Random(seed);eligible=[k for k,c in TEMPLATES.items() if c['level']==level]
 if template is None and profile is not None and profile.startswith('observed_'):
  eligible=[k for k in eligible if profile=='observed_'+TEMPLATES[k]['source_id']]
  if not eligible:raise ValueError('Profile level mismatch')
 name=template or rng.choice(eligible)
 if name not in eligible:raise ValueError('Template level mismatch')
 c=TEMPLATES[name];profile=profile or 'authored_operations'
 for attempt in range(200):
  if parameters is None:
   vals=[sp.Rational(n,2) for n in range(-6,11)] if name in ('poly_negative','poly_ordered','poly_constant','poly_radical','helix') else [sp.Rational(n,2) for n in range(11)]
   if name=='log_square':vals=[sp.Rational(1,2),sp.Integer(1),sp.Integer(2),sp.E]
   a,b=sorted(rng.sample(vals,2));p={'a':str(a),'b':str(b)}
   try:a,b=check_parameters(name,p)
   except ValueError:continue
  else:a,b=check_parameters(name,parameters);p={'a':str(a),'b':str(b)}
  curve,speed,anti,L=math_data(name,a,b);values=[sp.simplify(x) for x in bank(name,a,b,speed,L,profile)]
  valid=all(x.is_real and x>0 for x in values) and all(sp.simplify(x-y)!=0 for i,x in enumerate(values) for y in values[i+1:]) and sum(sp.simplify(x-L)==0 for x in values)==1
  if valid:break
  if parameters is not None:raise ValueError('Complete bank invalid/colliding; explicit parameters not resampled')
 else:raise ValueError('No eligible instance')
 problem=c['problem'].replace('@a@',tex(a)).replace('@b@',tex(b))
 plot=render_plots(name,a,b)
 if plot:problem=re.sub(r'!\[\]\(.*?\)','![]('+plot['prompt']+')',problem)
 worked=solution(name,a,b,L)
 task=hashlib.sha256(json.dumps({'speed':sp.srepr(sp.simplify(speed)),'a':str(a),'b':str(b)},sort_keys=True).encode()).hexdigest()
 display=[tex(v) for v in values];fingerprint=hashlib.sha256(json.dumps([VERSION,problem,worked,sorted(display)],ensure_ascii=False).encode()).hexdigest()
 uid=lambda suffix:str(uuid.uuid5(uuid.NAMESPACE_URL,f'{KP}:{fingerprint}:{suffix}'))
 answers=[{':answer/id':uid('selection:'+sp.srepr(v)),':answer/type':':answer.type/math',':answer/value':text} for v,text in zip(values,display)];correct=answers[values.index(L)][':answer/id'];rng.shuffle(answers)
 field={':answer-field/id':uid('selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 return {'knowledge_point':{'db_id':KP,'id':'1889ba1a-09d4-5021-9ed2-3e531f8d5ef0','title':TITLE},'question':{':question/id':uid('question'),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':worked,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'source_id':c['source_id'],'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'mathematical_fingerprint':task,'content_fingerprint':fingerprint,'domain':'Half-integer bounded intervals; nonnegative t for speed proportional to t; positive t for logarithms','curve':[str(x) for x in curve],'speed':str(speed),'antiderivative':str(anti),'correct_value':str(L),'plots':plot,'authored_level':name=='log_square','dependencies':{'sympy':sp.__version__}}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=2);p.add_argument('--format',choices=['markdown','json'],default='markdown');p.add_argument('--template');p.add_argument('--profile');args=p.parse_args()
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 if args.format=='json':print(json.dumps(records,ensure_ascii=False,indent=2))
 else:
  for r in records:
   q=r['question'];print(q[':question/problem']);print('\n'.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']));print(q[':question/worked-solution']+'\n')
