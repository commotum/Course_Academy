#!/usr/bin/env python3
"""Wide ellipses centered at origin. math basis 1356; no EDB writes.
Source banks are parameterized evidence profiles; opaque recipes never defaults.
Run .venv/bin/python generate/scratch/17592186087839/validate.py.
"""
import argparse,hashlib,json,random,re,subprocess,tempfile,uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('');VERSION='wide-ellipse-v1'
SRC=json.loads((HERE/'source.json').read_text());KP=SRC['record'];QS=KP[':knowledge-point/questions']
PROVENANCE={k:SRC[k] for k in ('database','basis','lineage')}
PARAMS={'q-7603':('7/2','2'),'q-7604':('4','2'),'q-279101':('8','6'),'q-279125':('8','9/2'),'q-279126':('11/2','3/2'),'q-279130':('17/2','7/2'),'q-69891':('3','1'),'q-73619':('3','3/2'),'q-115108':('6','3'),'q-277919':('6','2'),'q-279127':('15/2','5/2'),'q-69890':('4','3')}
SPECS={'integer_radio':('easy','radio','integer'),'integer_blank':('easy','blank','integer'),'decimal_x_radio':('moderate','radio','decimal_x'),'decimal_y_radio':('moderate','radio','decimal_y'),'fraction_blank':('moderate','blank','fraction'),'quarter_radio':('hard','radio','fraction'),'quarter_blank':('hard','blank','fraction')}
BANKS={'radii':{'origin':'observed','sources':['q-7604','q-69891']},'double_radii':{'origin':'observed','sources':['q-115108']},'opaque_integer':{'origin':'observed_opaque','sources':['q-69890']},'opaque_decimal':{'origin':'observed_opaque','sources':['q-7603']},'reciprocal':{'origin':'observed','sources':['q-73619']},'method':{'origin':'authored','sources':[]}}
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'wide-ellipse:'+v))
def frac(n,d):return r'\frac{'+str(n)+'}{'+str(d)+'}'
def atom(z):
 z=s.Rational(z);return str(z) if z.q==1 else frac(z.p,z.q)
def term(v,n,d):
 return frac((str(n) if n!=1 else '')+'{'+v+'}^{2}',d)
def equation(cx,cy,equal=True):
 cx,cy=map(s.Rational,(cx,cy));return term('x',cx.p,cx.q)+'+'+term('y',cy.p,cy.q)+('=1' if equal else '')
def rawden(v,d):return frac('{'+v+'}^{2}',d)
def standard(a,b):return rawden('x','{'+atom(a)+'}^{2}')+'+'+rawden('y','{'+atom(b)+'}^{2}')
FORM=r'\frac{{x}^{2}}{{a}^{2}}+\frac{{y}^{2}}{{b}^{2}}'
INTRO='Remember that the equation of an ellipse centered at the origin with a horizontal radius of length $a$ and a vertical radius of length $b$ is given by\n\n$$\n'+FORM+'=1.\n$$\n\n \n\n'
def base_square(z):return '{'+atom(z)+'}^{2}' if z.q==1 else '{('+atom(z)+')}^{2}'
def substitution(a,b):return rawden('x',base_square(a))+'+'+rawden('y',base_square(b))
def squared_den(z):return str(z*z) if z.q==1 else '('+atom(z*z)+')'
def denominator_row(a,b):return rawden('x',squared_den(a))+'+'+rawden('y',squared_den(b))
def decimal(z):return str(float(z)) if z.q!=1 else str(z)
def solution(a,b,style):
 at=atom(a) if style!='decimal_y' else str(a)
 bt=decimal(b) if style=='decimal_y' else atom(b)
 prose=INTRO+'Here, the horizontal radius has length $a='+at+'$ and the vertical radius has length $b='+bt+'.$ Therefore, the equation of the ellipse is\n\n$$\n'
 rows=[FORM]
 if style=='integer':rows += [substitution(a,b),equation(1/a**2,1/b**2)]
 elif style=='fraction':rows += [substitution(a,b),denominator_row(a,b),equation(1/a**2,1/b**2)]
 elif style=='decimal_x':
  rows += [rawden('x','{'+decimal(a)+'}^{2}')+'+'+rawden('y','{'+atom(b)+'}^{2}'),rawden('x',base_square(a))+'+'+rawden('y',str(b*b)),rawden('x','('+frac('{'+str(a.p)+'}^{2}','{'+str(a.q)+'}^{2}')+')')+'+'+rawden('y',str(b*b)),denominator_row(a,b),equation(1/a**2,1/b**2)]
 elif style=='decimal_y':
  rows += [rawden('x','{'+str(a)+'}^{2}')+'+'+rawden('y','{'+decimal(b)+'}^{2}'),substitution(a,b),rawden('x',str(a*a))+'+'+rawden('y','('+frac('{'+str(b.p)+'}^{2}','{'+str(b.q)+'}^{2}')+')'),denominator_row(a,b),equation(1/a**2,1/b**2)]
 # Every row is an LHS only: equation() yields =1, so strip its suffix.
 rows=[r.removesuffix('=1') for r in rows]
 return prose+r'\begin{aligned}'+r' \\ '.join(r+' & =1'+('.' if i==len(rows)-1 else '') for i,r in enumerate(rows))+r'\end{aligned}'+'\n$$'
def recipes(a,b,profile):
 c=(1/a**2,1/b**2)
 if profile=='double_radii':return [(1/b,1/a),(1/a**2,1/b**2),(1/a,1/b),(1/b**2,1/a**2),(1/(2*a),1/(2*b))]
 if profile=='radii':return [(1/a,1/b),c,(1/b,1/a),(1/b**2,1/a**2),(1/(2*a),1/b)]
 if profile=='opaque_integer':return [(1/a,1/b),(1/b**2,1/a**2),(1/(2*a),1/(b-1)),c,(1/b,1/a)]
 if profile=='opaque_decimal':
  f=s.floor(a);return [(1/a,1/b),(1/b**2,1/f**2),(s.Rational(9)/(12*b),1/b),c,(1/f**2,1/b**2)]
 if profile=='reciprocal':return [(1/a**2,b**2),c,(s.Rational(1,4),1/b**2),(1/a**2,1/a**2),(s.Rational(1,4),b**2)]
 if profile=='method':return [c,(1/b**2,1/a**2),(1/a,1/b),(1/(4*a**2),1/(4*b**2)),(1/a**2,1/b)]
 raise ValueError('Unknown complete bank')
def bank_values(a,b,profile,kind):
 if kind=='blank':return [equation(1/a**2,1/b**2,False)]
 values=[equation(*v) for v in recipes(a,b,profile)]
 # Preserve source denominator syntax for opaque compound option without a value lookup.
 if profile=='opaque_decimal': values[2]=term('x',9,12*b)+'+'+term('y',1,b)+'=1'
 return values

def source_spec(q):
 qid=q[':question/math-academy-id'];kind=q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]
 if qid=='q-7603':return 'decimal_x_radio','opaque_decimal'
 if qid=='q-73619':return 'decimal_y_radio','reciprocal'
 if kind=='blank':return ('integer_blank' if q[':question/difficulty'][':db/ident'].endswith('/easy') else 'fraction_blank'),None
 return 'integer_radio',('opaque_integer' if qid=='q-69890' else 'double_radii' if qid=='q-115108' else 'radii')

def domain(level,template):
 if level=='easy':vals=[s.Rational(i) for i in range(1,10)]
 elif level=='moderate':vals=[s.Rational(i,2) for i in range(2,20)]
 else:vals=[s.Rational(i,4) for i in range(3,24,2)]
 return [(a,b) for a in vals for b in vals if a>b and a/b<=6 and (level!='moderate' or (a.q==2 or b.q==2)) and (template!='decimal_x_radio' or a.q==2 and b.q==1) and (template!='decimal_y_radio' or a.q==1 and b.q==2)]

def plot(a,b,source_id=None):
 if source_id:
  q=next(q for q in QS if q[':question/math-academy-id']==source_id)
  if (a,b)==tuple(map(s.Rational,PARAMS[source_id])):
   return re.search(r'!\[\]\((.*?)\)',q[':question/problem']).group(1),{'reused_source':True}
 data={'a':str(a),'b':str(b),'version':VERSION,'renderer':'matplotlib','axes':'equal','ticks':'four-intercepts'}
 key=sha(data);directory=HERE/'plots';directory.mkdir(exist_ok=True);path=directory/(key+'.png');side=path.with_suffix('.json')
 if not path.exists() or not side.exists():
  fd=tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='render-',dir=directory,delete=False);inputpath=Path(fd.name)
  json.dump({'data':data,'output':str(path)},fd);fd.close()
  try:subprocess.run([str(Path('.venv/bin/python').resolve()),str(HERE/'render.py'),str(inputpath)],check=True,capture_output=True)
  finally:inputpath.unlink(missing_ok=True)
 return str(path.resolve()),data

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 replay_source=None
 if profile and profile.startswith('source:'):
  replay_source=profile.split(':',1)[1];q=next((q for q in QS if q[':question/math-academy-id']==replay_source),None)
  if q is None:raise ValueError('Unknown source profile')
  t,bank=source_spec(q)
  if template is not None and template!=t:raise ValueError('Source template mismatch')
  template=t;profile=bank
 eligible=[t for t,(l,k,_) in SPECS.items() if l==level and (field_type is None or k==field_type)]
 rng=random.Random(seed)
 template=template or rng.choice(eligible)
 if template not in eligible:raise ValueError('Template/field/difficulty mismatch')
 _,kind,style=SPECS[template]
 profile=profile or ('method' if kind=='radio' else None)
 if kind=='blank' and profile is not None:raise ValueError('Blank has no choice bank')
 if kind=='radio' and profile not in BANKS:raise ValueError('Unknown profile')
 allowed={'integer_radio':('method','radii','double_radii','opaque_integer'),'decimal_x_radio':('method','opaque_decimal'),'decimal_y_radio':('method','reciprocal'),'quarter_radio':('method',)}
 if kind=='radio' and profile not in allowed[template]:raise ValueError('Profile does not belong to template')
 if parameters is not None:
  if set(parameters)!= {'a','b'}:raise ValueError('Exact a,b parameters required')
  a,b=map(s.Rational,(parameters['a'],parameters['b']))
  if (a,b) not in domain(level,template):raise ValueError('Parameters exceed authored workload bounds')
  choices=[(a,b)]
 else:choices=domain(level,template);rng.shuffle(choices)
 # Whole complete bank chosen BEFORE parameters; reject entire invalid instance.
 for a,b in choices:
  coefficients=recipes(a,b,profile) if kind=='radio' else [(1/a**2,1/b**2)]
  if len(set(coefficients))!=len(coefficients) or any(x.is_finite is not True or y.is_finite is not True or x.is_real is not True or y.is_real is not True or x<=0 or y<=0 for x,y in coefficients):
   if parameters is not None:raise ValueError('Whole bank collision or invalid coefficient')
   continue
  values=bank_values(a,b,profile,kind);correct=equation(1/a**2,1/b**2,kind=='radio')
  if values.count(correct)!=1:raise ValueError('Missing unique correct value')
  ref,pdata=plot(a,b,replay_source);prompt='![]('+ref+')\n\nWhat is the equation of the ellipse given above?'+ ('\n\n{{field-1}}$=1$' if kind=='blank' else '')
  worked=solution(a,b,style);finger=sha({'a':str(a),'b':str(b),'read':'explicit intercepts'})
  content=sha({'version':VERSION,'prompt':prompt,'solution':worked,'kind':kind,'bank':sorted(values)})
  qid=uid(content);key='field-1' if kind=='blank' else 'selection';fid=uid(qid+key)
  answers=[{':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in values];rng.shuffle(answers)
  question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid(fid+correct)]}]}
  return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'bank_origin':BANKS[profile]['origin'] if profile else ('authored' if level=='hard' else 'observed_blank'),'parameters':{'a':str(a),'b':str(b)},'parameter_fingerprint':finger,'content_fingerprint':content,'source_profile':replay_source,'source_analysis':PROVENANCE,'authored_extension':level=='hard' or profile=='method','evidence_only':bool(replay_source) or profile in ('opaque_integer','opaque_decimal','reciprocal'),'eligible_for_learning':not (bool(replay_source) or profile in ('opaque_integer','opaque_decimal','reciprocal')),'plot_assets':{'prompt':ref},'plot_data':pdata,'plot_rating':'heavy'}}
 raise ValueError('No valid instance in bounded domain')

# EASY: integers 1..9, a>b, ratio<=6; squares are integer denominators.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: halves 1..9.5, at least one odd half; preserves decimal conversion stages.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD authored: two odd quarter radii .75..5.75. Same skill, two denominator-16 squares.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='markdown');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
 if a.count<1:p.error('Positive count required')
 rs=[generate(l,a.seed+i,a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
if __name__=='__main__':main()
