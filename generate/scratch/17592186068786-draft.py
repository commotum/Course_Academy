#!/usr/bin/env python3
"""Bounded fractional substitution integral draft; registered baseline stays frozen."""
import argparse,copy,hashlib,importlib.util,json,random,sys,uuid,functools
from pathlib import Path
try:
 import sympy as sp
except ImportError:
 import os
 py=Path(__file__).resolve().parents[2]/'.venv/bin/python';os.execv(str(py),[str(py),__file__,*sys.argv[1:]])
sys.dont_write_bytecode=True
H=Path(__file__).with_suffix('');KP_ID=17592186068786;KP_UUID='03e934c8-da65-5615-9717-a50eee3577fd';TITLE='Integrating Other Fractional Expressions'
VERSION='fractional-shift-draft-v2';GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'));LEVELS=SUPPORTED_LEVELS=('easy','moderate','hard')
def private(name):
 spec=importlib.util.spec_from_file_location('fractional68786_'+name,H/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
FORMAT=private('math_format');PARSER=private('parser');PROFILES=json.loads((H/'contract.json').read_text())['profiles'];SOURCE=json.loads((H/'source.json').read_text());SOURCES={q.get(':question/math-academy-id',str(q[':db/id'])):q for q in SOURCE['record'][':knowledge-point/questions']}
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(obj):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(obj)))
def integer(v,name):
 if type(v)is not int:raise TypeError(name+' must be a built-in int')
 return v
def integrand(t,b):
 x=PARSER.SYMBOLS[t['variable']];return t['k']*x**(t['n']-1)/(b+t['sign']*x**t['n'])**sp.Rational(t['power'])
def render(sid,b):
 t=PROFILES[sid];subst=lambda s:s.replace('@@B@@',str(b))
 return FORMAT.normalize_prose(subst(t['prompt'])),FORMAT.normalize_prose(subst(t['solution'])),[FORMAT.normalize_tex(subst(s)) for s in t['bank']]
def eligible(level):return [s for s,t in PROFILES.items()if t['level']==level]
def parameters_checked(p):
 if type(p)is not dict or set(p)!={'b'}:raise ValueError('parameters must be a complete mapping {b: int}')
 integer(p['b'],'b')
 if not 1<=p['b']<=12:raise ValueError('b must be in 1..12')
 return dict(p)
def task_fingerprint(problem,level):
 c,f,z=PARSER.prompt(problem)
 return digest([level,'supplied-substitution'if level=='easy'else'choose-substitution',sp.srepr(sp.cancel((c*f).subs(z,PARSER.SYMBOLS['x'])))])
@functools.lru_cache(maxsize=256)
def bank_valid(sid,b,values):
 t=PROFILES[sid];z=PARSER.SYMBOLS[t['variable']];ds=[sp.diff(PARSER.scalar(s),z)for s in values];f=integrand(t,b)
 if [i for i,d in enumerate(ds)if sp.simplify(d-f)==0]!=[0]:raise ValueError('bank correct designation mismatch')
 if any(sp.simplify(a-b)==0 for i,a in enumerate(ds)for b in ds[i+1:]):raise ValueError('duplicate derivative families modulo constants')
 return True
@FORMAT.checked_math_content
def _normal_generate(difficulty='moderate',seed=0,template=None,parameters=None,profile=None,option_seed=None):
 integer(seed,'seed')
 if option_seed is not None:integer(option_seed,'option_seed')
 if type(difficulty)is not str or difficulty not in LEVELS:raise ValueError('unsupported difficulty')
 if template is not None and type(template)is not str:raise TypeError('template must be str')
 if profile=='reference':raise ValueError('raw original references are in source-cases.json; they are not served questions')
 if profile not in (None,'source','authored-easy'):raise ValueError('unknown profile')
 rng=random.Random(seed);sid=template if template is not None else rng.choice(eligible(difficulty))
 if sid not in eligible(difficulty):raise ValueError('template difficulty mismatch')
 if profile=='source'and sid=='authored-easy' or profile=='authored-easy'and sid!='authored-easy':raise ValueError('profile/template mismatch')
 t=PROFILES[sid];p=parameters_checked(parameters)if parameters is not None else {'b':rng.randint(1,12)};b=p['b']
 problem,solution,values=render(sid,b)
 for s in [problem,solution,*values]:
  if any(ord(c)<32 and c not in '\n\t'for c in s):raise ValueError('control character in displayed content')
 bank_valid(sid,b,tuple(values));fp=task_fingerprint(problem,difficulty)
 qid=ident(['question',VERSION,difficulty,sid,fp,values]);fid=ident([qid,'selection'])
 choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v}for v in values];correct=choices[0][':answer/id']
 if option_seed is not None:random.Random(option_seed).shuffle(choices)
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
 z=t['variable'];extra='; x > 0 so the original sqrt(x) distractor is also real'if sid=='q-2389'else'';base=f"{b} {'+'if t['sign']==1 else '-'} {z}^{t['n']}";relation='> 0'if t['power']=='1/2'else'!= 0'
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_version':VERSION,'seed':seed,'option_seed':option_seed,'template':sid,'profile':'authored-easy'if sid=='authored-easy'else'source','bank_profile':sid,'parameters':p,'domain':f'{z} real; {base} {relation}{extra}; each connected interval; square root is the principal positive real root; antiderivatives identified modulo additive constants','source_basis':2275,'source_lineage':SOURCE['lineage'],'source_ids':[]if sid=='authored-easy'else[sid],'authored_extension':sid=='authored-easy','mathematical_fingerprint':fp,'sympy_version':sp.__version__,'python_version':sys.version.split()[0],'plots':'none'}}
def generate(difficulty='moderate',seed=0,template=None,parameters=None,profile=None,option_seed=None):
 integer(seed,'seed')
 if option_seed is not None:integer(option_seed,'option_seed')
 if profile=='reference':
  if template!='q-49636' or parameters not in (None,{}):raise ValueError('only incomplete q-49636 has a reference-only API; no slots')
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':copy.deepcopy(SOURCES[template]),'generation':{'generator_version':VERSION,'seed':seed,'option_seed':option_seed,'template':template,'profile':'reference','parameters':{},'source_basis':2275,'source_lineage':SOURCE['lineage'],'reference_only':True,'normal_eligible':False}}
 return _normal_generate(difficulty,seed,template,parameters,profile,option_seed)
def batch(difficulty,count,seed=0,template=None,profile=None,option_seed=None):
 integer(count,'count');integer(seed,'seed')
 if option_seed is not None:integer(option_seed,'option_seed')
 if difficulty not in LEVELS:raise ValueError('unsupported difficulty')
 if count<0:raise ValueError('count must be nonnegative')
 candidates=[(s,b)for s in ([template]if template is not None else eligible(difficulty))for b in range(1,13)]
 if template is not None and template not in eligible(difficulty):raise ValueError('template difficulty mismatch')
 random.Random(seed).shuffle(candidates);out=[];seen=set()
 for sid,b in candidates:
  r=generate(difficulty,seed,sid,{'b':b},profile,option_seed);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:seen.add(fp);out.append(r)
  if len(out)==count:return out
 if count==0:return []
 raise ValueError('count exceeds finite distinct task capacity '+str(len(out)))
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');p.add_argument('--count',type=int,default=3);p.add_argument('--seed',type=int,default=0);p.add_argument('--template');p.add_argument('--profile');p.add_argument('--option-seed',type=int);p.add_argument('--format',choices=('json','markdown','md'),default='json');a=p.parse_args()
 try:
  rs=[r for l in (LEVELS if a.difficulty=='all'else[a.difficulty])for r in batch(l,a.count,a.seed,a.template,a.profile,a.option_seed)]
  print(json.dumps(rs,indent=2)if a.format=='json'else'\n\n---\n\n'.join(map(markdown,rs)))
 except (ValueError,TypeError)as e:p.exit(2,str(e)+'\n')
