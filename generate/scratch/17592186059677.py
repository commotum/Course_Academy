#!/usr/bin/env python3
"""Second derivatives. Frozen basis 2275; raw MA replay is evidence-only.

All default practice is independently authored from the extracted fixed stages.
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
X=sp.Symbol('x', positive=True)
# Fixed structure and source field contracts; coefficient domains are conservative.
SPECS={
 'quartic':('easy','radio',{'a':(2,3,5),'b':(-7,-4,2),'c':(-8,-7,3)},['q-10573','q-1851']),
 'powers':('easy','radio',{'a':(1,2,3),'b':(1,2,3)},['q-10902']),
 'cubic_evaluation':('easy','radio',{'a':(2,3,4),'b':(2,4,5),'c':(-7,-3,2),'t':(-2,-1,1,2)},['q-10892']),
 'known_first':('easy','blank',{'a':(-3,-2,2),'b':(-6,-4,3),'c':(12,18,24)},['q-128287']),
 'linear_cubic':('easy','blank',{'a':(4,6,8),'b':(1,2,3)},['q-167325','q-167779','q-166072']),
 'sqrt_sum':('moderate','radio',{'a':(4,8,12),'b':(3,5,7),'c':(1,2,3)},['q-10883']),
 'power_sqrt_evaluation':('hard','radio',{'a':(4,8,12),'b':(-3,-2,2),'c':(3,5,7),'t':(1,4,9)},['q-28556']),
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
  return [result,d1.subs(X,t),6*a*t,6*a*t-2*b,6*a*t+2*b*t],['correct','stop after first derivative','omit quadratic contribution','reverse quadratic contribution','retain x in quadratic second derivative']
 if template=='sqrt_sum':
  a,b=p['a'],p['b'];r=-sp.Rational(a,4)*X**sp.Rational(-3,2)
  return [result,-r+2*b,r-2*b,-sp.Rational(a,4)*X**sp.Rational(-5,2)+2*b,r],['correct','reverse radical sign','reverse quadratic sign','decrease radical exponent by two at second step','omit quadratic contribution']
 if template=='power_sqrt_evaluation':
  t=p['t'];a=p['a'];base=sp.sqrt(t)
  return [result,sp.Rational(5,2)*a*base,sp.Rational(15,4)*a*t,sp.Rational(5,4)*a*base,sp.Rational(15,2)*a*base],['correct','omit second exponent multiplier','evaluate x to power one rather than half','use one half instead of three halves at second derivative','double the second exponent multiplier']
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
 record={'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'level':level,'seed':seed,'template':template,'profile':'authored','bank_profile':template+'_procedure_bank' if kind=='radio' else None,'bank_recipes':recipes,'parameters':p,'domain':'x>0' if 'sqrt' in template else 'all real x','source':{k:SOURCE[k] for k in ['database','basis','lineage']},'source_ids':spec[3],'origin':'independently authored inventory','evidence_only':False,'eligible_for_learning':True,'relationship_to_source_templates':'Preserves source function structure, two successive derivative stages, target role, field contract, and optional evaluation; coefficients/points and bank are authored.','mathematical_fingerprint':digest([template,str(f),p.get('t')]),'content_fingerprint':identity}}
 return _fmt.validate_generated_record(record)

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile='authored',source_id=None):
 if type(seed) is not int:raise ValueError('integer seed required')
 if profile=='observed_raw':
  if template is not None or parameters is not None or field_type is not None:raise ValueError('raw replay accepts only original source_id; no unsupported mutations')
  if source_id not in ORIGINALS:raise ValueError('source_id required')
  original=copy.deepcopy(ORIGINALS[source_id]);original_level=original.get(':question/difficulty',{}).get(':db/ident')
  return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':original,'generation':{'template':source_id,'version':VERSION,'seed':seed,'profile':'observed_raw','level':original_level.split('/')[-1] if original_level else None,'source_id':source_id,'parameters':{},'origin':'exact original evidence','evidence_only':True,'eligible_for_learning':False,'source':{k:SOURCE[k] for k in ['database','basis','lineage']}}}
 if profile!='authored' or source_id is not None:raise ValueError('unsupported profile')
 if level not in ['easy','moderate','hard']:raise ValueError('unsupported difficulty')
 rng=random.Random(seed);template=template or rng.choice([k for k,v in SPECS.items() if v[0]==level])
 if template not in SPECS:raise ValueError('unknown template')
 candidates=parameters if parameters is not None else rng.choice(valid_parameters(template))
 return _authored(level,seed,template,field_type,dict(candidates))

from functools import lru_cache
@lru_cache(None)
def valid_parameters(template):
 result=[]
 for p in parameters(template):
  f,display,d1,d2,target=math_instance(template,p)
  if SPECS[template][1]=='radio':
   bank,_=authored_bank(template,p,f,d1,d2,target)
   if any(sp.simplify(bank[i]-bank[j])==0 for i in range(len(bank)) for j in range(i)):continue
  if target in [0,1]:continue
  result.append(p)
 return result

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def inventory(level,seed=0,count=1,template=None,field_type=None):
 if type(count) is not int or count<0:raise ValueError('nonnegative integer count')
 if level not in ['easy','moderate','hard']:raise ValueError('unsupported difficulty')
 if template is not None and (template not in SPECS or SPECS[template][0]!=level):raise ValueError('template/difficulty mismatch')
 entries=[]
 for name,spec in SPECS.items():
  if spec[0]==level and (template is None or name==template) and (field_type is None or field_type in [spec[1],':answer-field.type/'+spec[1]]):
   entries.extend((name,p) for p in valid_parameters(name))
 if count>len(entries):raise ValueError('requested count exceeds mathematical capacity '+str(len(entries)))
 random.Random(seed).shuffle(entries)
 return {'database':SOURCE['database'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'questions':[{'record':generate(level,seed,template=name,parameters=p,field_type=field_type),'role':'independently authored inventory','relationship_to_source_templates':'Same fixed derivative method and source structures; authored coefficients, points, and complete procedure-error banks.'} for name,p in entries[:count]]}

def markdown(record):
 q=record['question'];m=record['generation'];lines=['### '+(m.get('level') or 'unrated')+' — '+m['template']+' — '+m['origin'],q[':question/problem']]
 for field in q.get(':question/answer-fields',[]):
  correct=field.get(':answer-field/correct');correct_id=correct.get(':answer/id') if isinstance(correct,dict) else (correct[1] if correct else None)
  lines.extend('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==correct_id else '') for a in field[':answer-field/choices'])
 lines.append(q.get(':question/worked-solution','Worked solution absent in original.'))
 return '\n\n'.join(lines)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty','--level',dest='difficulty',choices=['easy','moderate','hard'],default='easy');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--template');parser.add_argument('--field-type',choices=['radio','blank']);parser.add_argument('--format',choices=['json','markdown'],default='json');args=parser.parse_args()
 try:data=inventory(args.difficulty,args.seed,args.count,args.template,args.field_type)
 except ValueError as error:parser.error(str(error))
 print(json.dumps(data,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(markdown(x['record']) for x in data['questions']))
if __name__=='__main__':main()
