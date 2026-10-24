#!/usr/bin/env python3
"""Bounded, complete source-bank exponential sum generator; no EDB writes."""
import argparse,hashlib,json,random,re,uuid,os,sys
from pathlib import Path
try:import sympy as sp
except ModuleNotFoundError:
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).with_suffix('');KP_ID=17592186064177;KP_UUID='980bb2fb-4bb5-5cbb-aea8-87010493c013'
TITLE='Integrating a Sum of Exponential Functions';GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'));VERSION='1.0.0'
SUPPORTED_LEVELS=('easy','moderate');TEMPLATES=json.loads((HERE/'templates.json').read_text());X=sp.Symbol('x',real=True);C=sp.Symbol('C',real=True)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def expression(text):
 text=text.replace('\u2061','').replace(r'\operatorname{ln}',r'\ln').replace('ln',r'\ln')
 text=text.replace('\\\\ln',r'\ln').replace(r'\cdot','*').replace(r'\,','').replace(r'\mid','|')
 text=re.sub(r'\\ln\s*\|x\|','log(Abs(x))',text)
 text=re.sub(r'\\ln\s*(\d+|x)',lambda m:'log('+m[1]+')',text)
 def group(s,pos):
  assert s[pos]=='{',s
  depth=1;i=pos+1
  while depth:
   if s[i]=='{':depth+=1
   if s[i]=='}':depth-=1
   i+=1
  return s[pos+1:i-1],i
 def fractions(s):
  while r'\frac' in s or r'\dfrac' in s:
   m=re.search(r'\\d?frac',s);start=m.start();a,i=group(s,m.end());b,j=group(s,i)
   s=s[:start]+'(('+fractions(a)+')/('+fractions(b)+'))'+s[j:]
  return s
 text=fractions(text).replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(text,local_dict={'x':X,'C':C,'e':sp.E,'log':sp.log,'Abs':sp.Abs},transformations=standard_transformations+(implicit_multiplication_application,))
def integrand(problem):
 if 'f(x)' in problem or 'g(x)' in problem:raise ValueError('Undefined source functions')
 m=re.search(r'\\int\s*(.*?)(?:\\,\\text\{d\}x|\)dx)',problem)
 if not m:raise ValueError('Unparsed integrand')
 s=m[1]
 if problem.endswith('dx$?'):s+=')'
 return expression(s)
def fingerprint_text(problem):return digest(sp.srepr(sp.expand(integrand(problem))))
def generate(difficulty,seed=0,template=None,parameters=None,bank_profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty '+difficulty)
 rng=random.Random(seed);choices=[k for k,t in TEMPLATES.items() if t['difficulty']==difficulty]
 template=template or rng.choice(choices)
 if template not in choices or bank_profile not in (None,template):raise ValueError('Invalid source profile')
 p=parameters or {'base':rng.randint(2,12)}
 if set(p)!={'base'} or type(p['base']) is not int or not 2<=p['base']<=12:raise ValueError('base must be integer 2..12')
 t=TEMPLATES[template];render=lambda s:s.replace('@@B@@',str(p['base']))
 prompt,solution=render(t['prompt']),render(t['solution']);values=[render(s) for s in t['choices']]
 fp=fingerprint_text(prompt);key='v1:'+template+':'+fp
 qid=uid(key);fid=uid(key+':field:'+t['field_key']);answers=[{':answer/id':uid(key+':answer:'+str(i)),':answer/type':':answer.type/math',':answer/value':s} for i,s in enumerate(values)]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':t['field_key'],':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[t['correct_index']][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'source_basis':json.loads((HERE/'source.json').read_text())['basis'],'seed':seed,'template':template,'bank_profile':template,'parameters':p,'parameter_fingerprint':fp,'domain':'x real; for reciprocal term x != 0, interval constants independent','source_references':[template],'recipes':t['choices'],'dependencies':{'sympy':sp.__version__}}}
def batch(difficulty,count=5,seed=0):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty')
 pairs=[(k,b) for k,t in TEMPLATES.items() if t['difficulty']==difficulty for b in range(2,13)];random.Random(seed).shuffle(pairs)
 return [generate(difficulty,seed,k,{'base':b}) for k,b in pairs[:count]]
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--output');a=ap.parse_args();r={'instances':batch(a.difficulty,a.count,a.seed),'supported_levels':SUPPORTED_LEVELS,'generator_id':GENERATOR_UUID};s=json.dumps(r,indent=2)
 if a.output:Path(a.output).write_text(s+'\n')
 else:print(s)
