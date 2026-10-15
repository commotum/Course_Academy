#!/usr/bin/env python3
"""Frozen2275 MA replay and conservative no-solution parameter variants; no database writes."""
import argparse, copy, hashlib, importlib.util, json, random, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186204092
KP_UUID='d63847ef-6360-50b5-b585-9084140b2d67'
TITLE='Solving For an Unknown Parameter - Variables and Constants on Both Sides'
VERSION='2.0.0-draft'
SUPPORTED_LEVELS=('easy','moderate','hard')
SOURCE_BASIS=2275
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
HERE=Path(__file__).with_suffix('')
def _private(name):
 spec=importlib.util.spec_from_file_location('kp04092_'+name,HERE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
fmt=_private('math_format')
parser=_private('display_parser')
SOURCE=json.loads((HERE/'source.json').read_text())
CATALOG=json.loads((HERE/'catalog.json').read_text())
DOMAIN={'kind':'explicit finite parameter catalog','path':'catalog.json','capacity_per_level':80,'constraints':'nonzero a,c; unequal b,d; easy b=0,a>0,c>0,d>0, complete five-option observed-profile bank distinct; moderate/hard nonzero b, signed integer coefficients and constants','hard_evidence':'No observed hard practice. Authored same-method blank variants, no added operations or reasoning stages; calibration unverified.'}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def fingerprint(p):return digest([str(sp.Rational(p['c'],p['a']))])
def term(n,s=''):
 if not s:return str(n)
 return ('-' if n==-1 else '' if n==1 else str(n))+s
def add(n,s=''):return ('+' if n>0 else '-')+term(abs(n),s) if n else ''
def bank(p):
 a,c=p['a'],p['c']
 # Observed numerical patterns; misconception interpretation is unresolved.
 return [sp.Rational(c,a),sp.Rational(a,c),sp.Rational(c-1,a),sp.Rational(c,c-1),sp.Integer(c-1)]
def render(p,template):
 x,k,a,b,c,d=(p[z] for z in ('variable','parameter','a','b','c','d'))
 ak=term(a,k); ax=ak+x; cx=term(c,x); left=ax+add(b); eq=left+'='+cx+add(d)
 coef=ak+add(-c); collected=ax+add(-c,x); rhs=d-b; root=sp.Rational(c,a); val=sp.latex(root)
 prompt=f'Consider the equation in the variable ${x},$ given by\n\n$$\n{eq}\n$$\n\nwhere ${k}$ is a constant. Given that this equation has no solution, what is the value of ${k}?$'
 if b:prompt+=f'\n\n${k}=$\n{{{{field-1}}}}'
 solution='Suppose we have an equation of the form\n\n$$\nax=b\n$$\n\nwhere $a$ and $b$ are constants, and $b\\ne 0.$ If $a=0,$ then the equation has no solution.\n\n'
 solution+=f'First, we rewrite the equation in the form $a{x}=b.$ \n\n'
 action=('subtracting' if c>0 else 'adding')+' $'+term(abs(c),x)+'$'
 solution+=f'We start by {action} from both sides of the equation:\n\n$$\n'
 # Sources use "adding ... to", not "from".
 if c<0:solution=solution.rsplit(' from both',1)[0]+' to both sides of the equation:\n\n$$\n'
 lines=[left+' & ='+cx+add(d),collected+add(b)+' & ='+cx+add(d)+add(-c,x),collected+add(b)+' & ='+str(d)]
 solution+=r'\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}'+'\n$$\n\n'
 if b:
  solution+=f"Then, we {'subtract' if b>0 else 'add'} ${abs(b)}$ {'from' if b>0 else 'to'} both sides:\n\n$$\n"
  lines=[collected+add(b)+' & ='+str(d),collected+add(b)+add(-b)+' & ='+str(d)+add(-b),collected+' & ='+str(rhs)]
  solution+=r'\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}'+'\n$$\n\n'
 solution+=f'Next, we factor ${x}$ on the left-hand side. This gives\n\n$$\n({coef}){x}={rhs}.\n$$\n\n'
 form='x' if template=='both-constants-ax-layout' else x
 solution+=f'Notice that this equation is now in the form $a{form}=b:$\n\n$$\n'
 solution+='{{('+coef+')}_{⏟}}_{a}'+x+'={{'+str(rhs)+'}_{⏟}}_{b}\n$$\n\nTherefore, the equation has no solution if\n\n$$\n'+coef+'=0.\n$$\n\n'
 solution+=f'Solving this for ${k},$ we get\n\n$$\n'
 lines=[coef+' & =0',coef+add(c)+' & =0'+add(c),ak+' & ='+str(c),r'\frac{'+ak+'}{'+str(a)+'} & ='+r'\frac{'+str(c)+'}{'+str(a)+'}',k+' & ='+val+'.']
 solution+=r'\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}'+'\n$$'
 return prompt,solution

def parameters(level,p):
 if level not in SUPPORTED_LEVELS:raise ValueError('unsupported level')
 if type(p) is not dict or set(p)!={'variable','parameter','a','b','c','d'}:raise ValueError('parameter keys')
 if type(p['variable']) is not str or p['variable'] not in ('x','y','z','u','v','w') or type(p['parameter']) is not str or p['parameter'] not in ('p','q','r','k','m','n'):raise ValueError('names')
 if any(type(p[k]) is not int for k in 'abcd'):raise ValueError('integer parameters required')
 if p not in CATALOG[level] and not any(p==parser.prompt_parameters(q[':question/problem']) and q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/'+level for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q):raise ValueError('outside finite catalog or observed parameters')
 if not p['a'] or not p['c'] or p['b']==p['d']:raise ValueError('no-solution constraints')
 if level=='easy' and (p['b'] or p['a']<=0 or p['c']<=0 or p['d']<=0 or len(set(bank(p)))!=5):raise ValueError('easy profile')
 if level!='easy' and not p['b']:raise ValueError('both constants required')
 return dict(p)
def _seed(seed):
 if type(seed) is not int:raise ValueError('integer seed required')
def _defaults(level):return ('right-constant','observed-ratio-bank') if level=='easy' else ('both-constants','blank-rational')
def _check_profile(level,template,profile):
 default,bank_profile=_defaults(level)
 if template not in ((default,) if level=='easy' else (default,'both-constants-ax-layout')):raise ValueError('template')
 if profile!=bank_profile:raise ValueError('bank profile')
def _record(level,seed,template,p,profile,raw=False):
 root=sp.Rational(p['c'],p['a']);values=bank(p) if level=='easy' else [root]
 prompt,solution=render(p,template)
 if not raw:
  # Unicode underbrace capture wrappers are retained only in raw replay.
  solution=re_underbraces(solution)
  prompt=fmt.normalize_prose(prompt);solution=fmt.normalize_prose(solution)
 content=digest([level,prompt,solution,sorted(map(str,values)),profile])
 qid=uid('question:'+content);key='selection' if level=='easy' else 'field-1';fid=uid(qid+':field:'+key)
 answers=[{':answer/id':uid(fid+':answer:'+str(v)),':answer/type':':answer.type/math',':answer/value':fmt.normalize_tex(sp.latex(v))} for v in values]
 f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('radio' if level=='easy' else 'blank'),':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[0][':answer/id']]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[f]},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'parameter_fingerprint':fingerprint(p),'content_fingerprint':content,'domain':DOMAIN,'plot_rating':'none','evidence_role':'authored conservative same-method extension' if level=='hard' else 'observed backbone with authored parameters','source_analysis':{'basis':SOURCE_BASIS,'lineage':LINEAGE,'reference':str(HERE/'source-cases.json')}}}
def re_underbraces(text):
 import re
 return re.sub(r'{{(.*?)}_{⏟}}_{([ab])}',lambda m:r'\underbrace{'+m[1]+'}_{'+m[2]+'}',text)
@fmt.checked_math_content
def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty')
 _seed(seed);default,bp=_defaults(level);template=default if template is None else template;profile=bp if profile is None else profile;_check_profile(level,template,profile)
 p=globals()['parameters'](level,parameters if parameters is not None else random.Random(seed).choice(CATALOG[level]))
 rec=_record(level,seed,template,p,profile);parser.validate_record(rec);return rec
def observed_raw(source_id,parameters=None):
 if type(source_id) is not str:raise ValueError('MA source identifier required')
 matches=[q for q in SOURCE['record'][':knowledge-point/questions'] if q.get(':question/math-academy-id')==source_id]
 if len(matches)!=1:raise ValueError('unknown MA practice source')
 q=matches[0];original=parser.prompt_parameters(q[':question/problem'])
 if parameters is not None and (type(parameters) is not dict or parameters!=original or any(type(parameters.get(k)) is not type(v) for k,v in original.items())):raise ValueError('raw replay requires original parameters')
 complete=':question/difficulty' in q and ':question/worked-solution' in q and all(':answer-field/correct' in f for f in q[':question/answer-fields'])
 if not complete:
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':copy.deepcopy(q),'generation':{'version':VERSION,'template':'incomplete-raw-evidence','source_id':source_id,'parameters':original,'basis':SOURCE_BASIS,'lineage':LINEAGE,'evidence_only':True,'eligible':False,'role':'ineligible source evidence; missing rating/key/solution; preserved without repair'}}
 level=q[':question/difficulty'][':db/ident'].split('/')[-1];template='right-constant' if level=='easy' else 'both-constants-ax-layout' if source_id=='q-288678' else 'both-constants'
 p=globals()['parameters'](level,original);prompt,solution=render(p,template)
 # Reconstruct text from the observed template. Preserve field banks, feedback and all extra source attributes independently.
 rebuilt={k:copy.deepcopy(v) for k,v in q.items() if k not in (':question/problem',':question/worked-solution',':question/answer-fields')}
 rebuilt[':question/problem']=prompt;rebuilt[':question/worked-solution']=solution
 rebuilt[':question/answer-fields']=[{k:copy.deepcopy(v) for k,v in f.items()} for f in q[':question/answer-fields']]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':rebuilt,'generation':{'version':VERSION,'template':template,'source_id':source_id,'parameters':p,'basis':SOURCE_BASIS,'lineage':LINEAGE,'evidence_only':True,'eligible':False,'role':'whole original raw MA replay'}}
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def batch(level,count=5,seed=0):
 if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty')
 _seed(seed)
 if type(count) is not int or count<0 or count>len(CATALOG[level]):raise ValueError('count outside finite capacity')
 domain=list(CATALOG[level]);random.Random(seed).shuffle(domain)
 return [generate(level,seed,parameters=p) for p in domain[:count]]
def markdown(rec):
 parser.validate_record(rec)
 q=rec['question'];lines=[q[':question/problem']]
 for f in q[':question/answer-fields']:
  lines.append('Field `'+f[':answer-field/key']+'` ('+f[':answer-field/type']+')')
  for a in f[':answer-field/choices']:lines.append(('* ' if a[':answer/id']==f[':answer-field/correct'][1] else '- ')+'$'+a[':answer/value']+'$')
 lines.extend(['Worked solution',q[':question/worked-solution']]);return '\n\n'.join(lines)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=SUPPORTED_LEVELS+('all',),required=True);ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--output',type=Path);args=ap.parse_args()
 rows=([r for level in SUPPORTED_LEVELS for r in batch(level,args.count,args.seed)] if args.difficulty=='all' else batch(args.difficulty,args.count,args.seed));text=(json.dumps(rows,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))+'\n'
 if args.output:args.output.write_text(text)
 else:print(text,end='')
if __name__=='__main__':main()
