#!/usr/bin/env python3
"""Second derivatives. Frozen basis 2275; raw MA replay is evidence-only.

Default practice includes faithful complete source profiles and separately
documented authored variants of the extracted fixed stages.
The bounded domain is the same for explicit calls, samplers, and CLI inventory.
Derivative order is fixed at two: higher orders belong to a separate KP.
"""
import argparse, copy, hashlib, importlib.util, itertools, json, random, sys, uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
KP_ID=17592186059677
ROOT=Path(__file__).with_suffix('')
VERSION='second-derivative-b2275-v1'
_spec=importlib.util.spec_from_file_location('second_derivative_math_format',ROOT/'math_format.py')
_fmt=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_fmt)
SOURCE=json.loads((ROOT/'source.json').read_text()); KP=SOURCE['record']
ORIGINALS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
SOURCE_PARAMETERS={
 'q-10573':{'function':'3x^4-7x^2-8','target':'f second derivative at x'},
 'q-1851':{'function':'5x^4-4x^2-7x','target':'f second derivative at x'},
 'q-10907':{'a':4,'b':-3,'powers':[5,4],'t':-1,'function_name':'f'},
 'q-1852':{'cubic_coefficient':12,'sin_coefficient':-5,'cos_coefficient':4,'function_name':'f'},
 'q-128287':{'a':-3,'b':-6,'c':24,'supplied_object':'first derivative','function_name':'f'},
 'q-167325':{'linear_coefficient':8,'cubic_coefficient':'-2/3','function_name':'g'},
 'q-167779':{'linear_coefficient':8,'cubic_coefficient':'-2/3','function_name':'g'},
 'q-166072':{'linear_coefficient':8,'cubic_coefficient':'-2/3','function_name':'g'},
 'q-10883':{'a':4,'b':5,'c':1,'function_name':'f'},
 'q-10892':{'a':2,'b':4,'c':-7,'t':-2,'function_name':'f'},
 'q-10902':{'a':1,'b':1,'powers':[6,5],'function_name':'f'},
 'q-28556':{'a':4,'b':-2,'c':7,'t':4,'function_name':'g'},
 'q-342851':{'a':-1,'b':4,'t':1,'function_name':'g'}}
X=sp.Symbol('x', positive=True)
# Fixed structure and source field contracts; coefficient domains are conservative.
SPECS={
 'quartic':('easy','radio',{'a':(2,3,5),'b':(-7,-4,2),'c':(-8,-7,3)},['q-10573','q-1851']),
 'powers':('easy','radio',{'a':(1,2,3),'b':(1,2,3)},['q-10902']),
 'cubic_evaluation':('easy','radio',{'a':(2,3,4),'b':(2,4,5),'c':(-7,-3,2),'t':(-2,-1,1,2)},['q-10892']),
 'known_first':('easy','blank',{'a':(-3,-2,2),'b':(-6,-4,3),'c':(12,18,24)},['q-128287']),
 'linear_cubic':('easy','blank',{'a':(4,6,8),'b':(1,2,3)},['q-167325','q-167779','q-166072']),
 'sqrt_sum':('moderate','radio',{'a':(4,8,12),'b':(3,5,7),'c':(1,2,3)},['q-10883']),
 'power_sqrt_evaluation':('hard','radio',{'a':(4,8,12),'b':(-3,-2,2),'c':(3,5,7),'t':(4,9)},['q-28556']),
 'mixed_sqrt_evaluation':('hard','blank',{'a':(-3,-2,-1),'b':(4,8,12),'t':(1,4,9)},['q-342851'])}

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(value):return str(uuid.uuid5(uuid.NAMESPACE_URL,value))
def tex(expr):return _fmt.normalize_tex(sp.latex(sp.expand(expr)))
def signed_terms(terms):
 result=''
 for coefficient,body in terms:
  if not coefficient:continue
  c=abs(coefficient);piece=(tex(c) if c!=1 or not body else '')+body
  result+=('-' if coefficient<0 else '+' if result else '')+piece
 return result or '0'

def math_instance(template,p):
 a,b=p['a'],p['b'];c=p.get('c',0)
 if template=='quartic': f=a*X**4+b*X**2+c; display=tex(f)
 elif template=='powers': f=a*X**6+b*X**5; display=tex(f)
 elif template=='cubic_evaluation':f=a*X**3+b*X**2+c;display=tex(f)
 elif template=='known_first':f=a*X**2+b*X+c;display=tex(f)
 elif template=='linear_cubic':f=a*X-sp.Rational(b,3)*X**3;display=tex(f)
 elif template=='sqrt_sum':
  f=a*sp.sqrt(X)+b*X**2+c*X;display=signed_terms([(a,r'\sqrt{x}'),(b,'x^{2}'),(c,'x')])
 elif template=='power_sqrt_evaluation':
  f=a*X**sp.Rational(5,2)+b*X+c;display=signed_terms([(a,r'x^{2}\sqrt{x}'),(b,'x'),(c,'')])
 else:
  f=a*X**3+b*X**sp.Rational(3,2);display=signed_terms([(a,'x^{3}'),(b,r'x\sqrt{x}')])
 d1=f if template=='known_first' else sp.diff(f,X)
 d2=sp.diff(d1,X); target=sp.simplify(d2.subs(X,p['t'])) if 't' in p else d2
 return f,display,d1,d2,target

def power_form(expr):
 return signed_terms([(term.as_coeff_exponent(X)[0],('' if term.as_coeff_exponent(X)[1]==0 else ('x' if term.as_coeff_exponent(X)[1]==1 else 'x^{'+str(term.as_coeff_exponent(X)[1])+'}'))) for term in sp.expand(expr).as_ordered_terms()])

def differentiated_terms(expr):
 terms=[]
 for term in sp.expand(expr).as_ordered_terms():
  coefficient,exponent=term.as_coeff_exponent(X)
  if exponent==0:terms.append('0');continue
  terms.append('('+tex(coefficient)+r')\cdot('+tex(exponent)+r')\cdot x^{'+str(exponent-1)+'}')
 return '+'.join(terms)

def stage(label,input_display,rewrite,intermediate,output):
 rows=[label+r' &= \left('+input_display+r'\right)^{\prime}']
 if rewrite is not None:rows.append(r'&= \left('+rewrite+r'\right)^{\prime}')
 rows.extend([r'&= '+intermediate,r'&= '+tex(output)+'.'])
 return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'

# Complete procedure-error bank is fixed before computing options. No pooled recipes.
def authored_bank(template,p,f,d1,d2,result):
 if template in ['quartic','powers']:
  terms=sp.expand(f).as_ordered_terms();first_term=next(t for t in terms if t.has(X)); last_variable=[t for t in terms if t.has(X)][-1]
  high=sp.diff(first_term,X,2);low=sp.diff(last_variable,X,2)
  return [result,d1,high,high-low,X*d2],['correct','stop after first derivative','omit lower-power term','reverse lower-term sign','fail to lower exponents at second differentiation']
 if template=='cubic_evaluation':
  t=p['t'];a=p['a'];b=p['b']
  return [result,d1.subs(X,t),6*a*t,6*a*t-2*b,6*t+2*b],['correct','stop after first derivative','omit quadratic contribution','reverse quadratic contribution','omit original constant multiplier on cubic term']
 if template=='sqrt_sum':
  a,b=p['a'],p['b'];r=-sp.Rational(a,4)*X**sp.Rational(-3,2)
  return [result,-r+2*b,r-2*b,-sp.Rational(a,4)*X**sp.Rational(-5,2)+2*b,r],['correct','reverse radical sign','reverse quadratic sign','decrease radical exponent by two at second step','omit quadratic contribution']
 if template=='power_sqrt_evaluation':
  t=p['t'];a=p['a'];base=sp.sqrt(t)
  return [result,sp.Rational(5,2)*a*base,sp.Rational(15,4)*a*t**sp.Rational(3,2),sp.Rational(5,4)*a*base,sp.Rational(15,2)*a*base],['correct','omit second exponent multiplier','retain exponent three halves after second differentiation','use one half instead of three halves at second derivative','double the second exponent multiplier']
 raise ValueError('blank has no bank')

def parameters(template):
 names=list(SPECS[template][2]);return [dict(zip(names,v)) for v in itertools.product(*(SPECS[template][2][k] for k in names))]

def _authored(level,seed,template,field_type,p):
 spec=SPECS[template]
 if spec[0]!=level:raise ValueError('template/difficulty mismatch')
 if field_type not in [None,spec[1],':answer-field.type/'+spec[1]]:raise ValueError('unsupported field contract')
 if set(p)!=set(spec[2]) or any(type(p[k]) is not int or p[k] not in spec[2][k] for k in p):raise ValueError('parameters outside complete bounded domain')
 f,display,d1,d2,result=math_instance(template,p)
 name='g' if template in ['linear_cubic','power_sqrt_evaluation','mixed_sqrt_evaluation'] else 'f'
 target=name+r'^{\prime\prime}('+str(p['t'])+')' if 't' in p else name+r'^{\prime\prime}(x)'
 d1label=name+r'^{\prime}(x)';d2label=name+r'^{\prime\prime}(x)'
 if template=='known_first':
  prompt='Given $'+d1label+'='+display+'$, calculate $'+target+'.$'
  solution='We already know that\n\n$$\n'+d1label+'='+display+'.\n$$\n\n'
 else:
  prompt='Find $'+target+'$ '+('if' if 't' in p else 'for')+' $'+name+'(x)='+display+'.$'
  solution='Computing the first derivative, we have\n\n'+stage(d1label,display,power_form(f) if 'sqrt' in template else None,differentiated_terms(f),d1)+'\n\n'
 solution+='Computing the second derivative, we have\n\n'+stage(d2label,tex(d1),None,differentiated_terms(d1),d2)
 if 't' in p:
  substitution=tex(d2).replace('x','('+str(p['t'])+')')
  solution+='\n\nFinally, evaluating the second derivative at $x='+str(p['t'])+'$, we obtain\n\n$$\n'+r'\begin{aligned}'+target+' &= '+substitution+r' \\ &= '+tex(result)+'.'+r'\end{aligned}'+'\n$$'
 kind=spec[1]
 if kind=='blank':prompt+='\n\n$'+target+'=$ {{field-1}}';bank=[result];recipes=[]
 else:
  bank,recipes=authored_bank(template,p,f,d1,d2,result)
  if any(sp.simplify(bank[i]-bank[j])==0 for i in range(len(bank)) for j in range(i)):raise ValueError('complete selected bank invalid')
  prompt+='\n\n{{selection}}'
 prompt=_fmt.normalize_prose(prompt);solution=_fmt.normalize_prose(solution);values=[tex(v) for v in bank]
 identity=digest([VERSION,prompt,solution,sorted(values),tex(result)])
 field_id=uid(identity+'/field');key='field-1' if kind=='blank' else 'selection'
 choices=[{':answer/id':uid(field_id+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 field={':answer-field/id':field_id,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[0][':answer/id']]}
 q={':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]}
 record={'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'level':level,'seed':seed,'template':template,'profile':'authored','bank_profile':template+'_procedure_bank' if kind=='radio' else None,'bank_recipes':recipes,'parameters':p,'domain':'x>0' if 'sqrt' in template else 'all real x','source':{k:SOURCE[k] for k in ['database','basis','lineage']},'source_ids':spec[3],'origin':'independently authored inventory','evidence_only':False,'eligible_for_learning':True,'relationship_to_source_templates':'Preserves source function structure, two successive derivative stages, target role, field contract, and optional evaluation; coefficients/points and bank are authored.','mathematical_fingerprint':digest(['given_first' if template=='known_first' else 'function',str(f),p.get('t')]),'content_fingerprint':identity}}
 return _fmt.validate_generated_record(record)

_fs=importlib.util.spec_from_file_location('second_derivative_faithful',ROOT/'faithful.py')
_faithful=importlib.util.module_from_spec(_fs);_fs.loader.exec_module(_faithful)
FAITHFUL_SPECS={name:(ORIGINALS[sid][':question/difficulty'][':db/ident'].split('/')[-1],ORIGINALS[sid][':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]) for name,sid in _faithful.SOURCES.items()}

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile='auto',source_id=None):
 if type(seed) is not int:raise ValueError('integer seed required')
 if profile=='observed_raw':
  if template is not None or parameters is not None or field_type is not None:raise ValueError('raw replay accepts only original source_id; no unsupported mutations')
  if source_id not in ORIGINALS:raise ValueError('source_id required')
  original=copy.deepcopy(ORIGINALS[source_id]);original_level=original.get(':question/difficulty',{}).get(':db/ident')
  return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':original,'generation':{'template':source_id,'version':VERSION,'seed':seed,'profile':'observed_raw','level':original_level.split('/')[-1] if original_level else None,'source_id':source_id,'parameters':copy.deepcopy(SOURCE_PARAMETERS[source_id]),'origin':'exact original evidence','evidence_only':True,'eligible_for_learning':False,'source':{k:SOURCE[k] for k in ['database','basis','lineage']}}}
 if profile=='source_faithful' and source_id is not None:
  if template is not None:raise ValueError('select source_id or template, not both')
  template=next((name for name,sid in _faithful.SOURCES.items() if sid==source_id),None)
  if template is None:raise ValueError('source has no complete served profile')
  source_id=None
 if profile not in ['auto','authored','source_faithful'] or source_id is not None:raise ValueError('unsupported profile')
 if template in FAITHFUL_SPECS or profile=='source_faithful':
  if profile=='authored':raise ValueError('faithful template requires source_faithful or auto profile')
  if template not in FAITHFUL_SPECS:raise ValueError('faithful template required')
  return _faithful.render(_module_proxy(),template,level,seed,parameters if parameters is not None else {'scale':random.Random(seed).choice(_faithful.SCALES)},field_type)
 if level not in ['easy','moderate','hard']:raise ValueError('unsupported difficulty')
 if field_type not in [None,'radio','blank',':answer-field.type/radio',':answer-field.type/blank']:raise ValueError('unsupported field contract')
 candidates=[k for k,v in {**SPECS,**FAITHFUL_SPECS}.items() if v[0]==level and (field_type is None or field_type in [v[1],':answer-field.type/'+v[1]])]
 if profile=='authored':candidates=[k for k in candidates if k in SPECS]
 if not candidates:raise ValueError('no supported template for field contract')
 rng=random.Random(seed);template=template or rng.choice(candidates)
 if template in FAITHFUL_SPECS:return _faithful.render(_module_proxy(),template,level,seed,parameters if parameters is not None else {'scale':rng.choice(_faithful.SCALES)},field_type)
 if template not in SPECS:raise ValueError('unknown template')
 candidates=parameters if parameters is not None else rng.choice(valid_parameters(template))
 return _authored(level,seed,template,field_type,dict(candidates))

def _module_proxy():
 from types import SimpleNamespace
 return SimpleNamespace(**globals())

from functools import lru_cache
@lru_cache(None)
def valid_parameters(template):
 result=[]
 for p in parameters(template):
  f,display,d1,d2,target=math_instance(template,p)
  if SPECS[template][1]=='radio':
   bank,_=authored_bank(template,p,f,d1,d2,target)
   if any(sp.simplify(bank[i]-bank[j])==0 for i in range(len(bank)) for j in range(i)):continue
  result.append(p)
 return result

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def inventory_entries(level,template=None,field_type=None):
 if level not in ['easy','moderate','hard']:raise ValueError('unsupported difficulty')
 specs={**FAITHFUL_SPECS,**SPECS}
 if template is not None and (template not in specs or specs[template][0]!=level):raise ValueError('template/difficulty mismatch')
 if field_type not in [None,'radio','blank',':answer-field.type/radio',':answer-field.type/blank']:raise ValueError('unsupported field contract')
 entries=[];seen=set()
 for name,spec in specs.items():
  if spec[0]!=level or (template is not None and name!=template) or (field_type is not None and field_type not in [spec[1],':answer-field.type/'+spec[1]]):continue
  for p in ([{'scale':s} for s in _faithful.SCALES] if name in FAITHFUL_SPECS else valid_parameters(name)):
   if name in FAITHFUL_SPECS:fp=generate(level,template=name,parameters=p)['generation']['mathematical_fingerprint']
   else:
    f,*_=math_instance(name,p);fp=digest(['given_first' if name=='known_first' else 'function',str(f),p.get('t')])
   if fp in seen:continue
   seen.add(fp);entries.append((name,p))
 return entries

def inventory(level,seed=0,count=1,template=None,field_type=None):
 if type(count) is not int or count<0:raise ValueError('nonnegative integer count')
 if type(seed) is not int:raise ValueError('integer seed required')
 entries=inventory_entries(level,template,field_type)
 if count>len(entries):raise ValueError('requested count exceeds mathematical capacity '+str(len(entries)))
 random.Random(seed).shuffle(entries)
 return {'database':SOURCE['database'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'questions':[{'record':generate(level,seed,template=name,parameters=p,field_type=field_type),'role':'independently authored inventory','relationship_to_source_templates':('Faithful served whole-source scalar template, preserving complete original bank and ordered shared prose.' if name in FAITHFUL_SPECS else 'Same fixed derivative method and source structures; authored coefficients, points, and complete procedure-error banks.')} for name,p in entries[:count]]}

def markdown(record):
 q=record['question'];m=record['generation'];lines=['### '+(m.get('level') or 'unrated')+' — '+m['template']+' — '+m['origin'],q[':question/problem']]
 for field in q.get(':question/answer-fields',[]):
  correct=field.get(':answer-field/correct');correct_id=correct.get(':answer/id') if isinstance(correct,dict) else (correct[1] if correct else None)
  lines.extend('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==correct_id else '') for a in field[':answer-field/choices'])
 lines.append(q.get(':question/worked-solution','Worked solution absent in original.'))
 return '\n\n'.join(lines)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty','--level',dest='difficulty',choices=['easy','moderate','hard','all'],default='easy');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--template');parser.add_argument('--field-type',choices=['radio','blank']);parser.add_argument('--format',choices=['json','markdown'],default='json');args=parser.parse_args()
 try:
  levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
  records=[x['record'] for level in levels for x in inventory(level,args.seed,args.count,args.template,args.field_type)['questions']]
 except ValueError as error:parser.error(str(error))
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(markdown(x) for x in records))
if __name__=='__main__':main()
