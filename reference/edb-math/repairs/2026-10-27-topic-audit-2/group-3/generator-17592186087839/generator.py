#!/usr/bin/env python3
"""Seeded wide-ellipse questions with exact source replay and portable plots.
Source banks are evidence profiles; normal radio banks vary graph assignments.
Run validate.py with the declared Python environment for local evidence.
"""
import argparse,hashlib,json,random,re,uuid,os,sys
sys.dont_write_bytecode=True
from math_format import checked_math_content, normalize_prose, normalize_tex
from plotter import render_plot
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;VERSION='wide-ellipse-v3'
SRC=json.loads((HERE/'source-data.json').read_text());KP=SRC['record'];QS=KP[':knowledge-point/questions']
PROVENANCE={k:SRC[k] for k in ('database','basis','lineage')}
PARAMS={'q-7603':('7/2','2'),'q-7604':('4','2'),'q-279101':('8','6'),'q-279125':('8','9/2'),'q-279126':('11/2','3/2'),'q-279130':('17/2','7/2'),'q-69891':('3','1'),'q-73619':('3','3/2'),'q-115108':('6','3'),'q-277919':('6','2'),'q-279127':('15/2','5/2'),'q-69890':('4','3'),'q-16457':('5/2','3/2'),'q-115107':('2','1'),'q-277920':('11/2','2')}
SPECS={'integer_radio':('easy','radio','integer'),'integer_blank':('easy','blank','integer'),'decimal_x_radio':('moderate','radio','decimal_x'),'decimal_y_radio':('moderate','radio','decimal_y'),'fraction_blank':('moderate','blank','fraction'),'decimal_both_radio':('moderate','radio','decimal_both')}
BANKS={'radii':{'origin':'observed','sources':['q-7604','q-69891']},'double_radii':{'origin':'observed','sources':['q-115108']},'opaque_integer':{'origin':'observed_opaque','sources':['q-69890']},'opaque_decimal':{'origin':'observed_opaque','sources':['q-7603']},'reciprocal':{'origin':'observed','sources':['q-73619']},'method':{'origin':'authored_legacy_evidence','sources':[]},'radius_candidates':{'origin':'authored','sources':[]},'both_decimal':{'origin':'observed_opaque','sources':['q-16457']},'rhs_four':{'origin':'observed','sources':['q-115107']}}
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
 elif style=='decimal_both':
  rows += [rawden('x','{'+decimal(a)+'}^{2}')+'+'+rawden('y','{'+decimal(b)+'}^{2}'),substitution(a,b),rawden('x','('+frac('{'+str(a.p)+'}^{2}','{'+str(a.q)+'}^{2}')+')')+'+'+rawden('y','('+frac('{'+str(b.p)+'}^{2}','{'+str(b.q)+'}^{2}')+')'),denominator_row(a,b),equation(1/a**2,1/b**2)]
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
 if profile=='both_decimal':return [(1/(2*a)**2,1/b**2),(s.Rational(1,4),1/(2*b)**2),(1/a**2,1/(2*b)**2),c,(1/(2*a)**2,1/(2*b)**2)]
 if profile=='rhs_four':return [(1/(4*b),1/(4*a)),(1/(4*a*a),1/(4*a)),(1/a,1/b),(1/b**2,1/a**2),c]
 if profile=='method':return [c,(1/b**2,1/a**2),(1/a,1/b),(1/(4*a**2),1/(4*b**2)),(1/a**2,1/b)]
 raise ValueError('Unknown complete bank')
def bank_values(a,b,profile,kind):
 if kind=='blank':return [equation(1/a**2,1/b**2,False)]
 values=[equation(*v) for v in recipes(a,b,profile)]
 # Preserve source denominator syntax for opaque compound option without a value lookup.
 if profile=='rhs_four':
  values[0]=equation(1/b,1/a).removesuffix('=1')+'=4'
  values[1]=equation(1/a**2,1/a).removesuffix('=1')+'=4'
 if profile=='opaque_decimal': values[2]=term('x',9,12*b)+'+'+term('y',1,b)+'=1'
 return values

def source_spec(q):
 qid=q[':question/math-academy-id'];kind=q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]
 if qid=='q-7603':return 'decimal_x_radio','opaque_decimal'
 if qid=='q-16457':return 'decimal_both_radio','both_decimal'
 if qid=='q-115107':return 'integer_radio','rhs_four'
 if qid=='q-73619':return 'decimal_y_radio','reciprocal'
 if kind=='blank':return ('integer_blank' if q[':question/difficulty'][':db/ident'].endswith('/easy') else 'fraction_blank'),None
 return 'integer_radio',('opaque_integer' if qid=='q-69890' else 'double_radii' if qid=='q-115108' else 'radii')

def domain(level,template):
 if level=='easy':vals=[s.Rational(i) for i in range(1,10)]
 elif level=='moderate':vals=[s.Rational(i,2) for i in range(2,20)]
 else:raise ValueError('Unsupported difficulty: '+level)
 return [(a,b) for a in vals for b in vals if a>b and a/b<=6 and (level!='moderate' or (a.q==2 or b.q==2)) and (template!='decimal_x_radio' or a.q==2 and b.q==1) and (template!='decimal_y_radio' or a.q==1 and b.q==2) and (template!='decimal_both_radio' or a.q==2 and b.q==2)]

def plot(a,b,source_id=None):
 if source_id:
  q=next(q for q in QS if q[':question/math-academy-id']==source_id)
  if (a,b)==tuple(map(s.Rational,PARAMS[source_id])):
   return re.search(r'!\[\]\((.*?)\)',q[':question/problem']).group(1),{'reused_source':True}
 output=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
 if not output:raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required for generated assets')
 directory=Path(output).resolve()
 if directory==HERE or HERE in directory.parents:raise ValueError('Asset output must be outside the runtime package directory')
 directory.mkdir(parents=True,exist_ok=True)
 data={'a':str(a),'b':str(b),'version':VERSION,'renderer':'matplotlib','axes':'equal','ticks':'four-intercepts'}
 path=directory/(sha(data)+'.png')
 render_plot(data,path)
 return str(path),data

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,bank_pairs=None,correct_role=None):
 if level not in ('easy','moderate'):raise ValueError('Unknown difficulty')
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
 profile=profile or ('radius_candidates' if kind=='radio' else None)
 if kind=='blank' and profile is not None:raise ValueError('Blank has no choice bank')
 if kind=='radio' and profile not in BANKS:raise ValueError('Unknown profile')
 allowed={'integer_radio':('radius_candidates','method','radii','double_radii','opaque_integer','rhs_four'),'decimal_x_radio':('radius_candidates','method','opaque_decimal'),'decimal_y_radio':('radius_candidates','method','reciprocal'),'decimal_both_radio':('radius_candidates','method','both_decimal')}
 if kind=='radio' and profile not in allowed[template]:raise ValueError('Profile does not belong to template')
 role=correct_role if correct_role is not None else rng.randrange(5)
 if role not in range(5):raise ValueError('Correct role must be 0..4')
 candidate_pairs=None
 if profile=='radius_candidates':
  if bank_pairs is not None:
   candidate_pairs=sorted(tuple(map(s.Rational,p)) for p in bank_pairs)
   if len(candidate_pairs)!=5 or len(set(candidate_pairs))!=5 or any(p not in domain(level,template) for p in candidate_pairs):raise ValueError('Five distinct in-domain radius pairs required')
  elif parameters is None:
   candidate_pairs=sorted(rng.sample(domain(level,template),5))
  else:
   target=tuple(map(s.Rational,(parameters['a'],parameters['b'])))
   if target not in domain(level,template):raise ValueError('Out of domain')
   others=rng.sample([p for p in domain(level,template) if p!=target],4)
   candidate_pairs=sorted([target,*others]);role=candidate_pairs.index(target)
  choices=[candidate_pairs[role]]
 elif parameters is not None:
  if set(parameters)!= {'a','b'}:raise ValueError('Exact a,b parameters required')
  a,b=map(s.Rational,(parameters['a'],parameters['b']))
  if (a,b) not in domain(level,template):raise ValueError('Parameters exceed authored workload bounds')
  choices=[(a,b)]
 else:choices=domain(level,template);rng.shuffle(choices)
 # Whole complete bank chosen BEFORE parameters; reject entire invalid instance.
 for a,b in choices:
  coefficients=[(1/u**2,1/v**2) for u,v in candidate_pairs] if candidate_pairs else recipes(a,b,profile) if kind=='radio' else [(1/a**2,1/b**2)]
  if len(set(coefficients))!=len(coefficients) or any(x.is_finite is not True or y.is_finite is not True or x.is_real is not True or y.is_real is not True or x<=0 or y<=0 for x,y in coefficients):
   if parameters is not None:raise ValueError('Whole bank collision or invalid coefficient')
   continue
  values=[equation(*v) for v in coefficients] if candidate_pairs else bank_values(a,b,profile,kind);values=list(map(normalize_tex,values));correct=equation(1/a**2,1/b**2,kind=='radio')
  if values.count(correct)!=1:raise ValueError('Missing unique correct value')
  ref,pdata=plot(a,b,replay_source);prompt='![]('+ref+')\n\nWhat is the equation of the ellipse given above?'+ ('\n\n{{field-1}}$=1$' if kind=='blank' else '')
  prompt=normalize_prose(prompt);worked=normalize_prose(solution(a,b,style));finger=sha({'a':str(a),'b':str(b),'read':'explicit intercepts'})
  identity_prompt=prompt if replay_source else prompt.replace(ref,'asset-sha256:'+hashlib.sha256(Path(ref).read_bytes()).hexdigest())
  content=sha({'version':VERSION,'prompt':identity_prompt,'solution':worked,'kind':kind,'bank':sorted(values)})
  qid=uid(content);key='field-1' if kind=='blank' else 'selection';fid=uid(qid+key)
  answers=[{':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in values];rng.shuffle(answers)
  question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid(fid+correct)]}]}
  return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'bank_origin':BANKS[profile]['origin'] if profile else ('authored' if level=='hard' else 'observed_blank'),'parameters':{'a':str(a),'b':str(b)},'parameter_fingerprint':finger,'content_fingerprint':content,'source_profile':replay_source,'source_analysis':PROVENANCE,'authored_extension':profile in ('method','radius_candidates'),'evidence_only':bool(replay_source) or (kind=='radio' and profile!='radius_candidates'),'eligible_for_learning':not bool(replay_source) and (kind=='blank' or profile=='radius_candidates'),'correct_role':role if candidate_pairs else None,'candidate_pairs':[[str(u),str(v)] for u,v in candidate_pairs] if candidate_pairs else None,'generator_rejections':0,'plot_assets':{'prompt':ref},'plot_data':pdata,'plot_rating':'heavy'}}
 raise ValueError('No valid instance in bounded domain')

# EASY: integers 1..9, a>b, ratio<=6; squares are integer denominators.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: halves 1..9.5, at least one odd half; preserves decimal conversion stages.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard has no supporting source difficulty evidence.
def generate_hard(*args,**kwargs):raise ValueError('Hard unsupported: no source difficulty evidence')
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='markdown');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
 if a.count<1:p.error('Positive count required')
 rs=[generate(l,a.seed+i,a.template,profile=a.profile) for l in (['easy','moderate'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
if __name__=='__main__':main()
