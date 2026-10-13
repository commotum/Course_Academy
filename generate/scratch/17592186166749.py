#!/usr/bin/env python3
"""Two intermediate / two independent variable partial chain rule.

Basis 1356 source: five moderate and five hard source-shaped families. Every
source arithmetic stage is an expression slot; translated independent inputs
h,k=-2..2 retain held-coordinate derivatives and original teaching chains.
Observed complete banks are explicit evidence-only profiles, never defaults.
Normal defaults choose an entire method bank and a family before parameters.
Easy is an authored two-affine-map reduction of this exact curriculum branch.
No transactions, registration, engine edits or parameter-dependent graphics.
"""
import argparse,hashlib,json,random,re,sys,uuid
from importlib.metadata import version as package_version
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).with_suffix('');VERSION='two-independent-chain-rule-1'
CAPTURE=json.loads((ROOT/'source.json').read_text());SOURCE=CAPTURE['record']
KP_ID=17592186166749;KP_UUID=SOURCE[':knowledge-point/id'];TITLE=SOURCE[':knowledge-point/title']
x,y,s,t=sp.symbols('x y s t',real=True)
SOURCES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
FAMILIES={'zero_exponential':'q-37205','quadratic_linear':'q-94448','trig_sum_product':'q-170672','exponential_product':'q-170673','expanded_polynomial':'q-37138','reciprocal_exponential':'q-94747','trig_product':'q-94749','log_norm':'q-94751','quadratic_trig':'q-37201','cubic_product':'q-94748'}
TEMPLATES={k:SOURCES[v][':question/difficulty'][':db/ident'].split('/')[-1] for k,v in FAMILIES.items()};TEMPLATES['affine_two_maps']='easy'
PROFILES={**{'observed:'+v:{'template':k,'eligible':False,'origin':'observed value-pattern; intention unresolved'} for k,v in FAMILIES.items()},**{'operations:'+k:{'template':k,'eligible':True,'origin':'authored complete method bank'} for k in TEMPLATES}}
class SampleRejected(ValueError):pass
def tex(v):return sp.latex(v).replace(r'\log',r'\ln')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+str(v)))
def equal(a,b):
 d=sp.expand(a-b)
 if d==0:return True
 d=sp.cancel(d)
 if d==0:return True
 for p in ((1,2),(2,3),(3,1)):
  z=d.subs({s:p[0],t:p[1]})
  if z.is_zero is False:return False
 return sp.simplify(d)==0

def base(name):
 return {'zero_exponential':(2*x+x*y,s*sp.exp(s),t*sp.exp(s),t),'quadratic_linear':(x**2-4*y,2*s*t,s**2*t,s),'trig_sum_product':(x*y,sp.cos(t)+sp.sin(s),sp.sin(t),t),'exponential_product':(y*sp.exp(x),t+s,t*s,s),'expanded_polynomial':(x*y**2-2*y,s*t**2,s**3-t,s),'reciprocal_exponential':(1/x+1/y,sp.exp(s*t),sp.exp(-s*t),s),'trig_product':(x*y,sp.sin(s*t),sp.cos(s*t),t),'log_norm':(sp.log(x*x+y*y),t*sp.exp(s),t*sp.exp(-s),t),'quadratic_trig':(x*x-2*y*y,s*sp.sin(t),t*sp.sin(s),s),'cubic_product':(y*x*x,t*s,s-t,t)}[name]
def derivative(v,w):return r'\frac{∂'+v+'}{∂'+w+'}'
def block(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def mul(a,b):return '('+tex(a)+r')\cdot ('+tex(b)+')'

def translate(text,p):
 """Lex mathematical letters only; protect TeX commands and operator names.

 All replacement slots are complete grouped independent-coordinate inputs.
 Derivative labels and prose are handled by callers, never blind substitutions.
 """
 tokens=re.split(r'(\\[A-Za-z]+(?:\{(?:sin|cos|ln)\})?|\{(?:sin|cos)\})',text)
 for i in range(0,len(tokens),2):
  tokens[i]=re.sub('[st]',lambda m:m[0] if p['h' if m[0]=='s' else 'k']==0 else r'\left('+m[0]+('+' if p['h' if m[0]=='s' else 'k']>0 else '-')+str(abs(p['h' if m[0]=='s' else 'k']))+r'\right)',tokens[i])
 return ''.join(tokens)

def source_solution(name,p):
 sol=SOURCES[FAMILIES[name]][':question/worked-solution']
 def math(m):
  z=m[1];protected={}
  def protect(n):
   key='@'+str(len(protected))+'@';protected[key]=n[0];return key
  z=re.sub(r'\\frac\{∂[fxy]\}\{∂[xyst]\}',protect,z)
  z=translate(z,p)
  for key,val in protected.items():z=z.replace(key,val)
  return '$$'+z+'$$'
 return re.sub(r'\$\$(.*?)\$\$',math,sol,flags=re.S)

def validate_parameters(name,p):
 if name in FAMILIES:
  if set(p)!={'h','k'} or any(type(v)is not int or abs(v)>2 for v in p.values()):raise ValueError('Observed-family inputs require integer h,k in -2..2')
 else:
  if set(p)!={'a','b','c','d','e','g','variable'} or p['variable'] not in ('s','t') or any(type(p[v])is not int or not 1<=abs(p[v])<=3 for v in ('a','b','c','d','e','g')):raise ValueError('Easy requires signed nonzero integer coefficients |a,b,c,d,e,g|<=3 and variable s|t')
 return p

def render(name,p):
 if name in FAMILIES:
  f,X,Y,v=base(name);subs={s:s+p['h'],t:t+p['k']};X=X.subs(subs,simultaneous=True);Y=Y.subs(subs,simultaneous=True)
  prompt=SOURCES[FAMILIES[name]][':question/problem']
  prompt=re.sub(r'(where \$x=)(.*?)(\$ and \$y=)(.*?)(\.\$)',lambda m:m[1]+translate(m[2],p)+m[3]+translate(m[4],p)+m[5],prompt)
  return f,X,Y,v,prompt,source_solution(name,p)
 a,b,c,d,e,g=(p[z] for z in ('a','b','c','d','e','g'));v=s if p['variable']=='s' else t
 f=a*x+b*y;X=c*s+d*t;Y=e*s+g*t
 D=derivative('f',str(v));FX=derivative('f','x');FY=derivative('f','y');XD=derivative('x',str(v));YD=derivative('y',str(v));A=sp.diff(f,x);B=sp.diff(f,y);C=sp.diff(X,v);E=sp.diff(Y,v)
 formal=D+'='+FX+r'\cdot '+XD+'+'+FY+r'\cdot '+YD
 prompt='Let $f(x,y)='+tex(f)+',$ where $x='+tex(X)+'$ and $y='+tex(Y)+'.$ Calculate $'+D+'.$'
 asset='images/'+('21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png' if v==s else '11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png')
 sol='\n\n'.join(['![]('+asset+')','The chain rule for a multivariable function $f(x,y)$ with two independent variables $s$ and $t,$ where $x=x(s,t)$ and $y=y(s,t),$ can be expressed as follows:','$$\n'+formal+'\n$$','First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ ',block([FX+'='+tex(A)+r',\,'+FY+'='+tex(B)]),'Writing the above results in terms of $s$ and $t,$ we get',block([FX+' & ='+tex(A)+',',FY+' & ='+tex(B)+'.']),'Next, we take the derivatives of $x$ and $y$ with respect to $'+str(v)+',$ and we get',block([XD+' & ='+tex(C)+',',YD+' & ='+tex(E)+'.']),'Finally, substituting all of our derivatives into the multivariable chain rule, we get',block([D+' & ='+formal.split('=',1)[1],' & ='+mul(A,C)+'+'+mul(B,E),' & =('+tex(A*C)+')+('+tex(B*E)+')',' & ='+tex(A*C+B*E)+'.'])])
 return f,X,Y,v,prompt,sol

def operation_bank(name,f,X,Y,v):
 A=sp.diff(f,x).subs({x:X,y:Y},simultaneous=True);B=sp.diff(f,y).subs({x:X,y:Y},simultaneous=True);C=sp.diff(X,v);E=sp.diff(Y,v);U=A*C;V=B*E
 if name=='zero_exponential':
  w=s if v==t else t
  vals=[U+V,sp.diff(f.subs({x:X,y:Y},simultaneous=True),w),B,B*sp.diff(Y,w),Y*E]
  recipes=['correct','differentiate_other_coordinate','omit_y_coordinate_factor','use_other_coordinate_factor','substitute_y_for_x_partial']
 elif name=='affine_two_maps':
  w=s if v==t else t
  vals=[U+V,sp.diff(f.subs({x:X,y:Y},simultaneous=True),w),U-V,U,V]
  recipes=['correct','differentiate_other_coordinate','reverse_y_chain_sign','omit_y_chain','omit_x_chain']
 else:
  vals=[U+V,U,V,U-V,A+B]
  recipes=['correct','omit_y_chain','omit_x_chain','reverse_y_chain_sign','omit_both_coordinate_factors']
 for i,z in enumerate(vals):
  if any(equal(z,w) for w in vals[:i]):raise SampleRejected('Complete operation bank collision')
 return [tex(z) for z in vals],recipes

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio fields supported')
 rng=random.Random(seed)
 if profile:
  if profile not in PROFILES:raise ValueError('Unknown bank profile')
  pt=PROFILES[profile]['template']
  if template and pt!=template:raise ValueError('Template/profile mismatch')
  template=pt
 name=template or rng.choice([n for n,l in TEMPLATES.items() if l==level])
 if name not in TEMPLATES or TEMPLATES[name]!=level:raise ValueError('Template/level mismatch')
 profile=profile or 'operations:'+name;raw=not PROFILES[profile]['eligible']
 # Whole family/profile selected before parameter sampling.
 for attempt in range(100):
  p=dict(parameters) if parameters is not None else ({'h':rng.randint(-2,2),'k':rng.randint(-2,2)} if name in FAMILIES else {**{z:rng.choice((-3,-2,-1,1,2,3)) for z in ('a','b','c','d','e','g')},'variable':rng.choice(('s','t'))})
  validate_parameters(name,p);f,X,Y,v,prompt,sol=render(name,p)
  try:
   if raw:
    sq=SOURCES[FAMILIES[name]];sf=sq[':question/answer-fields'][0];values=[translate(a[':answer/value'],p) for a in sf[':answer-field/choices']];ci=next(i for i,a in enumerate(sf[':answer-field/choices']) if a[':answer/id']==sf[':answer-field/correct'][':answer/id']);recipes=['observed pattern; error intent unresolved']*5
   else:values,recipes=operation_bank(name,f,X,Y,v);ci=0
   break
  except SampleRejected:
   if parameters is not None:raise
 else:raise SampleRejected('Bounded whole-bank sampling exhausted')
 correct=sp.diff(f.subs({x:X,y:Y},simultaneous=True),v)
 mathematical=digest({'family':name,'assessed_derivative':sp.srepr(sp.cancel(sp.expand(correct))),'level':level,**({'composed_affine_function':sp.srepr(sp.expand(f.subs({x:X,y:Y},simultaneous=True))),'held_coordinate_partial':str(v)} if name=='affine_two_maps' else {})})
 content=digest({'version':VERSION,'level':level,'prompt':prompt,'solution':sol,'bank':sorted((z,i==ci) for i,z in enumerate(values))})
 qid=uid(content);fid=uid(content+'selection');answers=[{':answer/id':uid(fid+z),':answer/type':':answer.type/math',':answer/value':z} for z in values];correct_id=answers[ci][':answer/id'];rng.shuffle(answers)
 question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':PROFILES[profile]['origin'],'evidence_only':raw,'eligible_for_learning':not raw,'authored_extension':level=='easy' or not raw,'mathematical_fingerprint':mathematical,'parameter_fingerprint':mathematical,'content_fingerprint':content,'recipes':recipes,'source_analysis':{'database':'math','basis':1356,'lineage':CAPTURE['lineage'],'question_ids':[FAMILIES[name]] if name in FAMILIES else [],'topic_db_id':17592186050031},'domain':'s,t real; t != '+str(-p['k']) if name=='log_norm' else 's,t real','plot_rating':'none','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':package_version('matplotlib')}}}

# EASY — authored missing level: linear f, two affine coordinate maps, both terms.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Signed coefficients of magnitude 1..3; no nested functions/expansion.

 Two independent variables enter both maps; differentiate one holding the other
 fixed, compute both outer partials, both map partials and sum two products.
 """
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — five observed masks, shifts -2..2 preserving the exact source stages.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Five unordered observed polynomial/exponential/trig families and banks.

 Input translations change complete nested products and powers without adding
 operations: coordinate derivatives of shifts are 1. Zero terms stay printed.
 """
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — five observed product/expansion/logarithmic masks at equal source workload.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Retain each source's substitution, expansion, collection/cancellation rows.

 Same shift bounds as moderate; hard workload is its observed function/map
 structure, never an ordered progression or a third intermediate variable.
 """
 return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return '\n\n'.join([q[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']),q[':question/worked-solution']])
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 if a.count<1 or a.difficulty=='all' and (a.template or a.profile):ap.error('Positive count and specific level required with template/profile')
 levels=('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)
 rs=[generate(l,a.seed+i,a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(rs,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rs))
if __name__=='__main__':main()
