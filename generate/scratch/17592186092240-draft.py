"""Equation of a normal line. Frozen registered baseline; basis-2275 draft only.

Source interpolation retains every observed bank and complete solution sequence.
Easy/moderate/hard authored defaults use the same derivative, evaluation,
negative-reciprocal and point-slope/rearrangement stages. No vertical tangents.
"""
import argparse, copy, hashlib, importlib.util, itertools, json, random, re, uuid
from pathlib import Path
import sympy as s
H=Path(__file__).with_suffix(''); SOURCE=json.loads((H/'source.json').read_text()); K=SOURCE['record']; T=json.loads((H/'templates.json').read_text())
_f=importlib.util.spec_from_file_location('normal_private_math_format',H/'math_format.py');F=importlib.util.module_from_spec(_f);_f.loader.exec_module(F)
x=s.Symbol('x',positive=True); NS=uuid.UUID(K[':knowledge-point/id']); VERSION='2.0.0-draft'; GENERATOR_ID=str(uuid.uuid5(NS,'normal-line-all-levels-basis2275'))
def tex(v):return s.latex(s.expand(v))
def fmt(v):return '('+tex(v)+')'
def interp(text,values):
 for k,v in values.items():text=text.replace('@@'+k+'@@',v)
 if '@@' in text:raise ValueError('Unfilled source slot')
 return text
def make(level,seed,template,profile,params,prompt,solution,field_specs,key,domain,raw=False):
 if not raw:
  prompt=F.normalize_prose(prompt);solution=F.normalize_prose(solution);field_specs=[(k,t,[F.normalize_tex(v) for v in vs],F.normalize_tex(c)) for k,t,vs,c in field_specs]
 content={'version':VERSION,'level':level,'prompt':prompt,'solution':solution,'fields':field_specs,'profile':profile,'domain':domain}
 qid=str(uuid.uuid5(NS,json.dumps(content,sort_keys=True)));fields=[]
 for fieldkey,kind,values,correct in field_specs:
  fid=str(uuid.uuid5(uuid.UUID(qid),fieldkey));choices=[]
  for val in values:
   aid=str(uuid.uuid5(uuid.UUID(fid),val));choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':val})
  if len(set(c[':answer/id'] for c in choices))!=len(choices):raise ValueError('Duplicate bank')
  cid=str(uuid.uuid5(uuid.UUID(fid),correct))
  if cid not in [c[':answer/id'] for c in choices]:raise ValueError('Correct absent from bank')
  if kind=='radio':random.Random(seed).shuffle(choices)
  fields.append({':answer-field/id':fid,':answer-field/key':fieldkey,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',cid]})
 record={'knowledge_point':{'db_id':K[':db/id'],'id':str(NS),'title':K[':knowledge-point/title']},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields},'generation':{'generator_id':GENERATOR_ID,'version':VERSION,'template':template,'profile':profile,'seed':seed,'parameters':params,'mathematical_key':key,'domain':domain,'source_references':[profile] if profile in T else ['e-6080'],'authored':profile not in T,'raw_context':raw,'dependencies':{'sympy':s.__version__},'plots':[]}}
 return record if raw else F.validate_generated_record(record)
def concise_solution(expr,point,y,m,L=1,response='blank'):
 n=-1/m; B=L*(point+m*y)
 sol=(rf'Let $f(x)={tex(expr)}.$ First, we compute the derivative:'+'\n\n$$\n'+rf"f'(x)=\frac{{\text{{d}}}}{{\text{{d}}x}}\left({tex(expr)}\right)={tex(s.diff(expr,x))}"+'\n$$\n\n'+rf'Then, we compute the slope of the tangent at the point $({tex(point)},{tex(y)}):$'+'\n\n$$\n'+rf"m=f'({tex(point)})={tex(s.diff(expr,x).subs(x,point))}"+'\n$$\n\nTherefore, the slope of the normal line is\n\n$$\n'+rf"m'=-\frac{{1}}{{m}}={tex(n)}."+'\n$$\n\nFinally, the equation of the normal line is\n\n$$\n'+rf'\begin{{aligned}}y-{fmt(y)}&={tex(n)}(x-{fmt(point)}) \\ {tex(L*x+L*m*s.Symbol("y"))}&={tex(B)}.\end{{aligned}}'+'\n$$')
 if response!='blank':
  p=m;q=point+m*y;a=n;b=y-n*point; val={'p+q':p+q,'p-q':p-q,'q-p':q-p,'a+b':a+b}[response]
  sol+='\n\nTherefore, $'+response+'='+tex(val)+'.$'
 return sol
# EASY: quadratic plus constant; small signed coefficients, ordinary points.
# MODERATE: cubic, linear and constant; comparable source power-rule evaluation.
# HARD: sextic and cubic with source rational coefficients, ordinary points.
def authored_parameters(level):
 if level=='easy':return [{'a':a,'c':c,'point':p} for a,c,p in itertools.product([-3,-2,-1,1,2,3],range(-3,4),[1,2])]
 if level=='moderate':return [{'a':a,'b':b,'c':c,'point':p} for a,b,c,p in itertools.product([-2,-1,1,2],[-2,-1,1,2],range(-2,3),[-1,1,2]) if 3*a*p*p+b!=0]
 if level=='hard':return [{'a':a,'b':b,'c':c,'point':p} for a,b,c,p in itertools.product(range(1,5),range(1,9),range(-2,3),[1,2]) if s.Rational(3*a,4)*p**5-s.Rational(3*b,4)*p**2!=0]
 raise ValueError('Unknown difficulty')
def _authored(level,seed,parameters):
 allowed=authored_parameters(level);p=parameters if parameters is not None else random.Random(seed).choice(allowed)
 if not isinstance(p,dict) or any(type(v) is not int for v in p.values()) or p not in allowed or set(p)!=set(allowed[0]):raise ValueError('Parameters outside documented level bounds')
 a=s.Integer(p['a']);c=s.Integer(p['c']);point=s.Integer(p['point'])
 expr=a*x*x+c if level=='easy' else a*x**3+s.Integer(p['b'])*x+c if level=='moderate' else a*x**6/8-s.Integer(p['b'])*x**3/4+c
 y=expr.subs(x,point);m=s.diff(expr,x).subs(x,point);A=abs(m);B=point+m*y;sign='+' if m>0 else '-'
 prompt=rf'Find the equation of the normal line to the curve $y={tex(expr)}$ at the point $({tex(point)},{tex(y)}).$'+'\n\n$x\\,'+sign+'$\n{{field-1}}$\\cdot \\,y\\,=$\n{{field-2}}'
 specs=[('field-1','blank',[tex(A)],tex(A)),('field-2','blank',[tex(B)],tex(B))]
 return make(level,seed,'authored-'+level,'authored',p,prompt,concise_solution(expr,point,y,m),specs,'normal:'+str(s.expand(expr))+':at:'+str(point),'real x; tangent slope nonzero')
def source_parameters(profile):return [{'shift':i} for i in ([0] if T[profile].get('context') or profile=='q-47406' else [0,1,2] if profile=='q-103546' else range(-2,3))]
def _source(level,seed,profile,parameters,raw=False):
 if profile not in T or level!='moderate':raise ValueError('Observed replay profiles belong to moderate; unrated q-47406 assigned moderate')
 p=parameters if parameters is not None else random.Random(seed).choice(source_parameters(profile))
 if not isinstance(p,dict) or any(type(v) is not int for v in p.values()) or p not in source_parameters(profile) or set(p)!={'shift'}:raise ValueError('Unsupported source parameter')
 c=T[profile];shift=s.Integer(p['shift'])
 if c.get('context'):
  # Raw fragments omit prior-part bindings. Normal public replay supplies them.
  prompt=c['prompt_template'];solution=c['solution_template'];val=-(x-s.pi)/(2*s.exp(s.pi));values=[a[':answer/value'] for a in c['fields'][0][':answer-field/choices']];correct=c['fields'][0][':answer-field/correct'][':answer/value']
  if not raw:prompt='Use $f(x)=\\frac{1}{2}e^x$ and $h(x)=-4\\sin x$, with $y(\\pi)=0$ and tangent slope $m=2e^{\\pi}$.\n\n'+prompt
  return make(level,seed,'context-normal',profile,p,prompt,solution,[('field-1','blank',values,correct)],'normal:product-exp-sin:at:pi','real x; prior-part value and slope supplied',raw)
 base=s.sympify(c['expr'],locals={'x':x});point=s.Rational(c['point']);y=s.Rational(c['ordinate'])+shift;m=s.diff(base,x).subs(x,point);L=s.Integer(c['L']);B=L*(point+m*y);normal=-1/m
 response=c['response'];q=point+m*y;v={'blank':None,'p+q':m+q,'p-q':m-q,'q-p':q-m,'a+b':normal+y-normal*point}[response]
 # Every variable slot is a complete mathematical component, never a global number replacement.
 originals=c['slot_originals'];slots=dict(originals)
 if shift:
  slots['curve']=c['curve']+('+' if shift>0 else '')+str(shift)
  slots['pair']='('+tex(point)+','+tex(y)+')';slots['left']='y-'+fmt(y)
  # These rows multiply point-slope by the source's actual signed coefficient.
  coeff=16 if profile=='q-342190' else -3 if profile=='q-342168' else abs(m)
  slots['expanded']=tex(coeff*s.Symbol('y')-coeff*y);slots['grouped']=tex(coeff)+'(y-'+fmt(y)+')';slots['rhs']='='+tex(B)+'.'
  slots['line']=tex(normal*x+y-normal*point)
  if response=='a+b':slots['target']=tex(normal)+'+'+fmt(y-normal*point)+'='+tex(v)
  elif response in ('q-p','p-q','p+q'):
   operands={'q-p':(q,m,'-'),'p-q':(m,q,'-'),'p+q':(m,q,'+')}[response];slots['target']=tex(operands[0])+operands[2]+fmt(operands[1])+'='+tex(v)
 prompt=interp(c['prompt_template'],slots);solution=interp(c['solution_template'],slots) if c['solution_template'] else concise_solution(base+shift,point,y,m,response=response)
 if response=='blank':bykey={'field-1':abs(L*m),'field-2':B};specs=[(f[':answer-field/key'],'blank',[tex(bykey[f[':answer-field/key']])],tex(bykey[f[':answer-field/key']])) for f in c['fields']]
 elif not c['fields']:specs=[('selection','blank',[tex(v)],tex(v))];prompt+='\n\n{{selection}}'
 else:
  # Complete observed bank profiles. Unresolved error intent is documented;
  # these are explicit evidence profiles, never the authored default bank.
  vals={
   'q-47406':[77,74,66,56,58],
   'q-47408':[y+1/(2*m),v,y+2/m,y+4/m,y+1/m],
   'q-103546':[-m*y,v,-point,-y,y-point],
   'q-47409':[m+q,v,-m-q,point,-2*m+y],
   'q-47410':[q,q-m,-m-q,m+q,-q]}[profile]
  if len({s.simplify(t) for t in vals})!=len(vals):raise ValueError('Observed profile collision: whole instance rejected')
  specs=[('selection','radio',[tex(t) for t in vals],tex(v))]
 return make(level,seed,'source-'+response,profile,p,prompt,solution,specs,'normal:'+str(s.expand(base+shift))+':at:'+str(point),'real x; positive x for radical/reciprocal; tangent slope nonzero',raw)
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if profile=='observed_raw':
  if template not in T or not isinstance(parameters,dict) or parameters!={'shift':0} or type(parameters.get('shift')) is not int or field_type is not None:raise ValueError('Raw evidence accepts one original template and its original parameters only')
  question=next(q for q in K[':knowledge-point/questions'] if q[':question/math-academy-id']==template)
  return {'knowledge_point':{'db_id':K[':db/id'],'id':str(NS),'title':K[':knowledge-point/title']},'question':copy.deepcopy(question),'generation':{'version':VERSION,'template':template,'profile':'observed_raw','parameters':{'shift':0},'seed':seed,'evidence_only':True,'eligible_for_learning':False,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'plots':[]}}
 if profile is not None and profile!='authored':
  if template is not None and template not in ('source-'+T.get(profile,{}).get('response',''), 'context-normal'):raise ValueError('Template/profile mismatch')
  r=_source(level,seed,profile,parameters)
 else:
  if template not in (None,'authored-'+level):raise ValueError('Unsupported template')
  r=_authored(level,seed,parameters)
 if field_type is not None and any(f[':answer-field/type']!=':answer-field.type/'+field_type for f in r['question'][':question/answer-fields']):raise ValueError('Field type mismatch')
 return r
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def candidates(level,profile=None,template=None):
 if profile=='observed_raw':
  if template not in T:raise ValueError('Raw evidence requires an original MA template ID')
  return [('observed_raw',{'shift':0})]
 if profile and profile!='authored':return [(profile,p) for p in source_parameters(profile)]
 return [('authored',p) for p in authored_parameters(level)]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--profile');ap.add_argument('--template');a=ap.parse_args();out=[]
 if a.count<1:raise ValueError('Positive count required')
 for level in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]):
  cs=candidates(level,a.profile,a.template);random.Random(a.seed).shuffle(cs);seen=set();batch=[]
  for profile,p in cs:
   try:r=generate(level,a.seed,template=a.template,profile=profile,parameters=p)
   except ValueError:continue
   key=r['generation'].get('mathematical_key',r['question'].get(':question/math-academy-id'))
   if key in seen:continue
   seen.add(key);batch.append(r)
   if len(batch)==a.count:break
  if len(batch)<a.count:raise ValueError('Finite capacity exceeded')
  out+=batch
 print(json.dumps(out,indent=2) if a.format=='json' else '\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in out))
if __name__=='__main__':main()
