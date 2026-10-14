#!/usr/bin/env python3
"""Basis2275 draft; registered numeric generator and evidence remain immutable.

Easy: one constant multiple; moderate: two independently weighted sin/cos terms.
Hard authored: distribute two signed grouped sin/cos sums, collect, apply same rules.
Raw profiles preserve source omissions/ambiguous banks and are evidence-only.
"""
import argparse,copy,hashlib,json,random,re,sys,uuid,importlib.util
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
KP_ID=17592186064178
KP_UUID='0cae5c1b-57bd-51f6-a360-db946d25532f'
TITLE='Integrating Sine and Cosine'
VERSION='2.0.0-draft'
HERE=Path(__file__).with_suffix('')
_spec=importlib.util.spec_from_file_location('sine_math_format',HERE.parents[2]/'scripts/question_capture/math_format.py');MF=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(MF)
TEMPLATES=json.loads((HERE/'templates.json').read_text())
SUPPORTED_LEVELS=('easy','moderate','hard')
x,C=sp.symbols('x C',real=True)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def expression(s):
 s=s.replace('⁡','').replace('θ','x').replace(r'\theta','x').replace('y','x')
 s=re.sub(r'\\operatorname\{(sin|cos|tan)\}',r'\1',s)
 s=re.sub(r'\\(sin|cos|tan)',r'\1',s)
 s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',s)
 s=re.sub(r'\{(sin|cos)\}\^\{(\d+)\}',r'\1**\2',s)
 s=re.sub(r'(sin|cos|tan)(?:\*\*(\d+))?\s*(?:\(x\)|\{x\}|x)',lambda m:m[1]+'(x)'+('**'+m[2] if m[2] else ''),s)
 s=s.replace(r'\,','').replace(r'\left','').replace(r'\right','').replace('{','(').replace('}',')').strip().rstrip('.,')
 return parse_expr(s,local_dict={'x':x,'C':C,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan},transformations=standard_transformations+(implicit_multiplication_application,))
def integrand(s):
 z=re.search(r'\\int\s*(.*?)(?:\\text\{d\}|\\textrm\s*d|d[xyθ])',s,re.S)
 if not z:raise ValueError('integral not readable')
 return expression(z[1])
def eq(a,b):return sp.trigsimp(sp.expand(a-b))==0
def family_eq(a,b):return eq(sp.diff(a-b,x),0)
def render(v,p):
 if isinstance(v,str):
  vals=dict(p,ua='' if p.get('a')==1 else str(p.get('a','')),ub='' if p.get('b')==1 else str(p.get('b','')),sum=p.get('a',0)+p.get('b',0))
  return re.sub(r'\{(a|b|ua|ub|sum)\}',lambda m:str(vals[m[1]]),v)
 if isinstance(v,list):return [render(i,p) for i in v]
 if isinstance(v,dict):return {k:render(i,p) for k,i in v.items()}
 return v
def tex(e):
 e=sp.expand(e);out=''
 for f in ['sin','cos']:
  a=e.coeff(getattr(sp,f)(x))
  if not a:continue
  c=sp.latex(abs(a));t=('' if abs(a)==1 else c)+"\\"+f+' x'
  out+=('-' if a<0 else '+' if out else '')+t
 return out or '0' 
def trigterm(a,f):return ('-' if a==-1 else '' if a==1 else str(a))+'\\'+f+' x'
def sumterms(a,f,b,g):return trigterm(a,f)+('+' if b>0 else '-')+trigterm(abs(b),g)
def repack(q,level,seed,template,profile,p,eligible,author=None):
 q=copy.deepcopy(q);q.pop(':question/math-academy-id',None)
 if eligible:
  for k in [':question/problem',':question/worked-solution']:q[k]=MF.normalize_prose(q[k])
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:a[':answer/value']=MF.normalize_tex(a[':answer/value'])
 # Identity reflects actual grade and all displayed banks, never aliases/seeds.
 keyed=[]
 for f in q.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct');cv=next((a[':answer/value'] for a in f[':answer-field/choices'] if correct and a[':answer/id']==correct[1]),None)
  keyed.append([f[':answer-field/key'],f[':answer-field/type'],sorted((a[':answer/value'],a.get(':answer/feedback')) for a in f[':answer-field/choices']),cv])
 content=digest([VERSION,q[':question/problem'],q.get(':question/worked-solution'),q.get(':question/difficulty'),keyed]);qid=uid('q:'+content);q[':question/id']=qid
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  old=f.get(':answer-field/correct');fid=uid(qid+':f:'+str(i));f[':answer-field/id']=fid
  for a in f[':answer-field/choices']:
   oid=a[':answer/id'];a[':answer/id']=uid(fid+':a:'+a[':answer/value'])
   if old and old[1]==oid:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
  if f[':answer-field/type'].endswith('/radio'):random.Random(seed+i).shuffle(f[':answer-field/choices'])
 try:task=sp.srepr(-p['a']*sp.sin(x)) if 'h(x)'in q[':question/problem'] else sp.srepr(sp.expand(integrand(q[':question/problem'])))
 except Exception:task=sp.srepr(-p['a']*sp.sin(x)) # h prompt is unresolved raw evidence.
 if author=='grouped':task=['grouped-distribute-collect',task,p['a'],p['b']]
 differential=re.search(r'\\text\{d\}\s*(\\theta|[xyθ])',q[':question/problem']) or re.search(r'd([xyθ])',q[':question/problem'])
 variable=differential[1].replace('θ',r'\theta')
 unresolved_h=not eligible and 'h(x)' in q[':question/problem']
 blank=any(f[':answer-field/type'].endswith('/blank') for f in q.get(':question/answer-fields',[]))
 domain={'independent_variable':variable,'status':'unresolved' if unresolved_h else 'established',
         'integrand_domain':'Unresolved: h is not defined in the raw prompt.' if unresolved_h else 'All real values of the independent variable.',
         'correct_primitive_domain':'Unresolved from the raw prompt; worked solution supplies an inferred sine integrand only.' if unresolved_h else 'All real values of the independent variable.',
         'integration_constant':{'symbol':'C','range':'all real numbers','role':'arbitrary integration constant','placement':'supplied outside the requested blank fragment' if blank else 'part of the complete antiderivative family'},
         'response_contract':'nonconstant primitive fragment, with the supplied +C retained' if blank else 'complete antiderivative family modulo an arbitrary additive constant'}
 if template=='q-2034':domain['source_wrong_option_domain']='The tangent distractor excludes theta=pi/2+k*pi for integer k; this does not restrict the sine integrand or its correct cosine primitive.'
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':template,'bank_profile':profile,'parameters':p,'parameter_fingerprint':digest(task),'content_fingerprint':content,'eligible_for_learning':eligible,'evidence_only':not eligible,'authored_extension':author,'source_basis':2275,'source_lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','plot_rating':'none','domain':domain}}
def guard(level,p,keys,raw=False):
 if set(p)!=set(keys) or any(type(v)is not int for v in p.values()):raise ValueError('parameter keys/integer type')
 if raw:
  if any(not 1<=v<=9 for v in p.values()):raise ValueError('raw positive magnitudes1..9')
 else:
  if any(not 2<=abs(v)<=9 for v in p.values()):raise ValueError('signed nonunit coefficient magnitude2..9')
  if level=='moderate' and abs(p['a'])==abs(p['b']):raise ValueError('equal magnitudes cause source-bank collisions')
  if level=='hard' and (p['a']*p['b']>=0 or abs(p['a'])==abs(p['b'])):raise ValueError('hard requires opposing signs and unequal magnitudes')
def bankcheck(q):
 target=integrand(q[':question/problem']);f=q[':question/answer-fields'][0];exprs=[expression(a[':answer/value']) for a in f[':answer-field/choices']]
 cv=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
 assert eq(sp.diff(exprs[cv],x),target)
 for i,e in enumerate(exprs):
  assert (i==cv)==eq(sp.diff(e,x),target)
  for old in exprs[:i]:assert not family_eq(e,old),'ambiguous antiderivative families'
def authored(level,seed,family,p,field_type):
 a=p['a'];b=p.get('b',0);basis='cos' if family=='cos' else 'sin';target=a*getattr(sp,basis)(x) if level=='easy' else a*sp.cos(x)+b*sp.sin(x)
 if level=='hard':target=sp.expand(a*(sp.cos(x)-sp.sin(x))+b*(sp.cos(x)+sp.sin(x)))
 correct=sp.integrate(target,x);A=sp.expand(target).coeff(sp.cos(x));B=sp.expand(target).coeff(sp.sin(x))
 if level=='easy':
  base=sp.sin(x) if basis=='cos' else -sp.cos(x)
  bank=[correct,-correct,(-sp.Rational(1,a))*base,a*getattr(sp,basis)(x),-a*getattr(sp,basis)(x)]
 else:bank=[correct,A*sp.sin(x)+B*sp.cos(x),A*sp.cos(x)-B*sp.sin(x),B*sp.cos(x)-A*sp.sin(x),B*sp.sin(x)-A*sp.cos(x)]
 if level=='hard':bank=[correct,(a-b)*sp.sin(x)-(a+b)*sp.cos(x),a*sp.sin(x)-b*sp.cos(x),(a+b)*sp.cos(x)-(b-a)*sp.sin(x),-(a+b)*sp.sin(x)+(b-a)*sp.cos(x)]
 body=trigterm(a,basis) if level=='easy' else '('+sumterms(a,'cos',b,'sin')+')'
 if level=='hard':body='('+str(a)+r'(\cos x-\sin x)'+('+'if b>0 else '-')+str(abs(b))+r'(\cos x+\sin x))'
 prompt='$'+r'\int '+body+r'\,\text{d}x=$'
 recall=r'\int \sin x\,\text{d}x=-\cos x+C,\qquad \int \cos x\,\text{d}x=\sin x+C.'
 rows=[]
 if level=='hard':
  distributed=''
  for c,f in [(a,'cos'),(-a,'sin'),(b,'cos'),(b,'sin')]:distributed+=('+' if distributed and c>0 else '')+trigterm(c,f)
  rows.extend([r'\int ('+distributed+r')\,\text{d}x',r'\int ('+sumterms(A,'cos',B,'sin')+r')\,\text{d}x'])
 if level=='easy':rows=[str(a)+r'\int '+'\\'+basis+r' x\,\text{d}x',str(a)+'('+('-' if basis=='sin' else '')+'\\'+('cos' if basis=='sin' else 'sin')+' x)+C']
 else:rows += [str(A)+r'\int \cos x\,\text{d}x+('+str(B)+r')\int \sin x\,\text{d}x',str(A)+r'\sin x+('+str(B)+r')(-\cos x)+C']
 rows.append(tex(correct)+'+C.')
 solution='Recall that\n\n$$\n'+recall+'\n$$\n\nTherefore, we have\n\n$$\n'+r'\begin{aligned}\int '+body+r'\,\text{d}x & ='+((r' \\'+'\n & =').join(rows))+r'\end{aligned}'+'\n$$'
 ft=field_type or 'radio';values=[tex(e)+(r'+C' if ft=='radio' else '') for e in bank] if ft=='radio' else [tex(correct)]
 if ft=='blank':prompt='$'+r'\int '+body+r'\,\text{d}x=$ {{field-1}} $+C$, where $C$ is an arbitrary constant. Give the displayed fragment without an added constant.'
 ans=[{':answer/id':str(i),':answer/type':':answer.type/math',':answer/value':v}for i,v in enumerate(values)]
 q={':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/key':'selection'if ft=='radio'else'field-1',':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':ans,':answer-field/correct':[':answer/id','0']}]}
 bankcheck(q)
 return repack(q,level,seed,family,'authored_'+family,p,True,'grouped' if level=='hard' else 'source-shaped-method-bank')
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('unsupported level')
 rng=random.Random(seed)
 if template is None and profile and profile.startswith(('observed_','authored_')):template=profile.split('_',1)[1]
 if template is None and profile is None and field_type is None:
  template=rng.choice({'easy':['cos','sin','q-113907','q-113908','repaired_h','completed_q-71653'],'moderate':['sum','q-113909','q-2161','completed_q-71654'],'hard':['grouped']}[level])
 if template in ['repaired_h','completed_q-71653','completed_q-71654']:
  sid='q-166078' if template=='repaired_h' else template[len('completed_'):]
  t=TEMPLATES[sid]
  if level!=t['level'] or profile not in (None,'authored_'+template) or field_type not in (None,'blank'):raise ValueError('completed contract')
  p=parameters if parameters is not None else {'a':rng.randint(2,9)};guard(level,p,['a'],True)
  printed_prompt=render(t['record'][':question/problem'],p);target=-p['a']*sp.sin(x) if template=='repaired_h' else integrand(printed_prompt);canonical=sp.integrate(target,x)
  q=render(t['record'],p)
  if template=='repaired_h':q[':question/problem']='Given $h(x)=-'+str(p['a'])+r'\sin x$, '+q[':question/problem']
  else:
   v=tex(canonical).replace(' x',' y') if sid=='q-71653' else tex(canonical);q[':question/problem']=q[':question/problem']+' {{field-1}} $+C$, where $C$ is an arbitrary constant.'
   q[':question/answer-fields']=[{':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':'0',':answer/type':':answer.type/math',':answer/value':v}],':answer-field/correct':[':answer/id','0']}]
  q[':question/problem']+=' Give the displayed fragment without an added constant.'
  f=q[':question/answer-fields'][0];assert eq(expression(f[':answer-field/choices'][0][':answer/value']),canonical)
  return repack(q,level,seed,template,'authored_'+template,p,True,'source-format completion')
 if profile and profile.startswith('raw_'):
  template=template or profile[4:];t=TEMPLATES[template]
  if profile!='raw_'+template or level!=t['level'] or field_type:raise ValueError('raw contract mismatch')
  p=parameters if parameters is not None else t['parameters'];guard(level,p,t['parameters'],True)
  if template=='q-113909' and p['a']==p['b']:raise ValueError('raw changed source coefficient collision')
  if template in ['q-113907','q-113908','q-2033'] and p['a']<2:raise ValueError('nonunit source bank coefficient required')
  prompt=render(t['record'][':question/problem'],p)
  target=-p['a']*sp.sin(x) if 'h(x)'in prompt else integrand(prompt)
  canonical=sp.integrate(target,x)
  return repack(render(t['record'],p),level,seed,template,profile,p,False)
 if template in TEMPLATES:
  if profile not in (None,'observed_'+template) or field_type not in (None,'radio'):raise ValueError('profile/field mismatch')
  t=TEMPLATES[template]
  if not t['eligible'] or level!=t['level']:raise ValueError('source evidence profile requires explicit raw replay')
  p=parameters if parameters is not None else {k:rng.randint(2,9) for k in t['parameters']}
  if parameters is None and template=='q-113909':
   while p['a']==p['b']:p['b']=rng.randint(2,9)
  guard(level,p,t['parameters'],True)
  canonical=sp.integrate(integrand(render(t['record'][':question/problem'],p)),x)
  q=render(t['record'],p);bankcheck(q)
  f=q[':question/answer-fields'][0];v=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);assert family_eq(expression(v),canonical)
  return repack(q,level,seed,template,'observed_'+template,p,True)
 family=template or rng.choice(['cos','sin'] if level=='easy' else ['sum'] if level=='moderate' else ['grouped'])
 if family not in ({'easy':['cos','sin'],'moderate':['sum'],'hard':['grouped']}[level]):raise ValueError('template level mismatch')
 if field_type not in (None,'radio','blank'):raise ValueError('field type')
 if profile not in (None,'authored_'+family):raise ValueError('unknown profile')
 keys=['a'] if level=='easy' else ['a','b']
 if parameters is not None:
  guard(level,parameters,keys);return authored(level,seed,family,parameters,field_type)
 for _ in range(1000):
  p={k:rng.choice([-1,1])*rng.randint(2,9) for k in keys}
  try:guard(level,p,keys);return authored(level,seed,family,p,field_type)
  except (ValueError,AssertionError):continue
 raise ValueError('complete bank exhaustion')
# Easy: one multiplier, reverse derivative, preserve sign; coefficient abs2..9.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: two nonzero unequal-magnitude coefficients; separate and substitute.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard authored: opposing grouped multipliers; distribute/collect then same method.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'for f in q.get(':question/answer-fields',[])for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=[*SUPPORTED_LEVELS,'all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 rows=[generate(l,args.seed+i,template=args.template,profile=args.profile)for l in SUPPORTED_LEVELS if args.difficulty in ('all',l)for i in range(args.count)]
 print(json.dumps(rows,indent=2,ensure_ascii=False)if args.format=='json'else'\n\n---\n\n'.join(map(markdown,rows)))
if __name__=='__main__':main()
