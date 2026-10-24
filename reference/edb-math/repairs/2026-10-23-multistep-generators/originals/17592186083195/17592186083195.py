#!/usr/bin/env python3
"""Improper upper-limit integrals: captured layouts, exact coefficient variants.

Narrow sampling policy: each source layout fixes its exponent, positive lower
endpoint, and variable. The coefficient varies; banks scale as complete observed
profiles. This does not infer unobserved error algorithms. Hard is unsupported.
Run with --difficulty easy|moderate --count N --seed S --format json|markdown.
"""
import argparse,hashlib,json,random,sys,uuid
from pathlib import Path
try:
 import sympy as sp
except ImportError:
 root=Path(__file__).resolve().parents[2]
 sys.path.insert(0,str(root/'.venv/lib/python3.13/site-packages'))
 import sympy as sp
KP_ID=17592186083195
KP_UUID='6ef2ab87-f78b-5cbd-9be4-0c1ac3448d89'
TITLE='Calculating Improper Integrals With an Unbounded Upper Limit'
EVIDENCE=Path(__file__).with_suffix('')
VERSION='1.0.0-coefficient-profiles'
SUPPORTED_LEVELS=('easy','moderate')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
TEMPLATES=json.loads((EVIDENCE/'templates.json').read_text())
BY_ID={t['template']:t for t in TEMPLATES}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),x))
def latex(x):return sp.latex(sp.simplify(x)).replace(' \\sqrt','\\sqrt')
def task_fingerprint(t,C):
 return digest({'coefficient':str(C),'exponent':t['exponent'],'lower':t['lower']})

def generate(difficulty,seed=0,template=None,*,parameters=None,profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed);eligible=[t for t in TEMPLATES if t['level']==difficulty]
 t=BY_ID[template] if template else rng.choice(eligible)
 if t not in eligible:raise ValueError('Template level mismatch')
 if profile is not None and profile!=t['bank_profile']:raise ValueError('Bank profiles cannot be pooled')
 if parameters is not None:
  if set(parameters)!={'coefficient'}:raise ValueError('Only coefficient is variable in this frozen package')
  C=sp.Rational(parameters['coefficient'])
 else:
  C=sp.Rational(1,rng.randint(2,2000)) if t['source_id']=='q-152754' else sp.Integer(rng.randint(1,2000))
 # Signed coefficients would be a new unobserved policy. Bound this package.
 if t['source_id']=='q-152754':
  if C.p!=1 or not 2<=C.q<=2000:raise ValueError('Reciprocal profile requires C=1/D, 2<=D<=2000')
 elif C.q!=1 or not 1<=C<=2000:raise ValueError('Integral coefficient must be an integer from 1 to 2000')
 p=sp.Rational(t['exponent']);L=sp.Integer(t['lower']);K=C/(p-1);V=sp.simplify(K*L**(1-p))
 # Exact derivative and infinite endpoint are also checked by independent validation.
 x=sp.Symbol('x',positive=True);F=-K*x**(1-p)
 assert sp.simplify(sp.diff(F,x)-C*x**(-p))==0 and sp.limit(F,x,sp.oo)==0
 original_C=sp.Rational(t['source_coefficient'])
 integrand=t['integrand']
 if t['source_id']=='q-152754':
  integrand=integrand.replace(r'4\sqrt',str(C.q)+r'\sqrt')
 else:
  prefix=r'\frac{'+latex(original_C)+'}'
  assert integrand.startswith(prefix)
  integrand=r'\frac{'+latex(C)+'}'+integrand[len(prefix):]
 slots={'@INTEGRAND@':integrand,'@C@':latex(C),'@K@':latex(K),'@V@':latex(V)}
 def render(text):
  for key,val in slots.items():text=text.replace(key,val)
  assert '@' not in text
  return text
 problem,solution=render(t['problem']),render(t['solution'])
 bank=[]
 for a in t['bank']:
  value=a['source_value'] if a['ratio'] is None else latex(C*sp.sympify(a['ratio']))
  bank.append({'type':a['type'],'value':value,'correct':a['correct'],'recipe':a['recipe']})
 assert len({(a['type'],a['value']) for a in bank})==len(bank)
 correct=next(a for a in bank if a['correct']);assert correct['value']==latex(V)
 # Content identity includes the full owned bank and fixed layout; task deduplication
 # ignores bank, variable spelling, seed and choice ordering.
 fp=task_fingerprint(t,C)
 content=digest({'problem':problem,'solution':solution,'bank':bank,'level':difficulty,'key':t['field_key'],'type':t['field_type']})
 qid=uid('question:'+content);fid=uid('field:'+qid+':'+t['field_key'])
 answers=[{':answer/id':uid('answer:'+fid+':'+a['type']+':'+a['value']),':answer/type':a['type'],':answer/value':a['value']} for a in bank]
 cid=answers[next(i for i,a in enumerate(bank) if a['correct'])][':answer/id'];rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':t['field_key'],':answer-field/type':t['field_type'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[field]},'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'template':t['template'],'bank_profile':t['bank_profile'],'seed':seed,'parameters':{'coefficient':str(C)},'fixed_parameters':{'exponent':str(p),'lower':int(L),'variable':t['variable']},'domain':'x >= '+str(L)+' > 0','source_references':[t['source_id']],'recipes':[a['recipe'] for a in bank],'parameter_fingerprint':fp,'content_fingerprint':content,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':[],'sampling_policy':'Vary only positive coefficient; preserve each complete source bank profile and fixed exponent/lower endpoint'}}

def batch(difficulty,count,seed=0):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 if count<0:raise ValueError('Nonnegative count required')
 records=[];used=set()
 for attempt in range(40000):
  if len(records)==count:return records
  r=generate(difficulty,seed+attempt);fp=r['generation']['parameter_fingerprint']
  if fp not in used:records.append(r);used.add(fp)
 raise ValueError('Bounded distinct-variant search exhausted; no duplicate padding')

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value']+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template');args=ap.parse_args()
 records=[generate(args.difficulty,args.seed,args.template)] if args.template else batch(args.difficulty,args.count,args.seed)
 print(json.dumps({'instances':records},ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
