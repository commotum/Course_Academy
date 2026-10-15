#!/usr/bin/env python3
"""Second derivative component-mask profiles; draft only, bounded and read-only.

--difficulty easy|moderate|hard|all --count N --seed N --format json|markdown
Count is per level; JSON is always a flat array. See extraction and calibration.
"""
import argparse,copy,hashlib,importlib.util,itertools,json,random,sys,uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 import os
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
if sp.__version__!='1.14.0':raise RuntimeError('Frozen generator requires SymPy 1.14.0')
HERE=Path(__file__).with_suffix('');ROOT=HERE.parents[2]
def local(name):
 spec=importlib.util.spec_from_file_location('kp59678_'+name,HERE/(name+'.py'));mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
fmt=local('math_format');parser=local('display_parser')
SOURCE=json.loads((HERE/'source.json').read_text());MASKS=json.loads((HERE/'component-masks.json').read_text())
KP_ID=17592186059678;KP_UUID=SOURCE['record'][':knowledge-point/id'];TITLE=SOURCE['record'][':knowledge-point/title'];VERSION='2.0.0-draft';SUPPORTED_LEVELS=('easy','moderate','hard')
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id'in q}
PROFILES={sid:q[':question/difficulty'][':db/ident'].split('/')[-1] for sid,q in SOURCES.items() if sid in MASKS}
PROFILES['authored-hard-radical']='hard'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def sid_for(profile):return 'q-342868' if profile=='authored-hard-radical' else profile
def params(values):return {'multipliers':list(values)}
def candidates(profile):
 if profile not in PROFILES:raise ValueError('Unknown profile')
 sid=sid_for(profile);n=3 if sid in ('q-10884','q-342868','q-342877','q-342970')else 2
 values=[str(sp.Rational(n,2)) for n in range(1,20,2)]if PROFILES[profile]=='hard'else [str(n) for n in range(1,7 if PROFILES[profile]=='easy'else 11)]
 return [params(v) for v in itertools.product(*[(['1']if sid in ('q-342868','q-342877')and i==1 else values)for i in range(n)])]
def check_int(value,label):
 if type(value)is not int:raise ValueError(label+' must be an integer')
def check_parameters(profile,p):
 if not isinstance(p,dict)or set(p)!= {'multipliers'}or type(p['multipliers'])is not list or any(type(v)is not str for v in p['multipliers'])or p not in candidates(profile):raise ValueError('Parameters outside declared exact finite multiplier domain')
def typography(t):
 t=t.replace('\u2061','')
 import re
 t=re.sub(r'(?<![A-Za-z\\])(sin|cos|ln)(?=x)',lambda m:'\\'+m[1]+' ',t)
 return t

def scale_term(t,k):
 if k==1:return t
 sign=''
 if t.startswith(('+','-')):sign=t[0];t=t[1:]
 return sign+sp.latex(k)+r'\left('+t+r'\right)'
def render(profile,part,p):
 sid=sid_for(profile);mask=MASKS[sid][part];text=mask['raw']
 for c in reversed(mask['components']):text=text[:c['start']]+scale_term(c['raw'],sp.Rational(p['multipliers'][c['slot']]))+text[c['end']:]
 return typography(text)
def observed_raw(source_id,parameters=None):
 if source_id not in SOURCES:raise ValueError('Unknown observed MA source')
 q=SOURCES[source_id];p=params(['1']*(3 if source_id in ('q-10894','q-1873','q-10884','q-342868','q-342877','q-342970')else 2))
 if parameters is not None and parameters!=p:raise ValueError('Raw replay only supports exact observed parameters')
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':copy.deepcopy(q),'generation':{'template':source_id,'profile':source_id,'parameters':p,'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'evidence_only':True,'eligible':False,'source_question':q[':question/id']}}
def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty')
 check_int(seed,'seed');rng=random.Random(seed)
 if template is not None and profile is not None and template!=profile:raise ValueError('Conflicting template/profile')
 selected=profile if profile is not None else template
 if selected is None:selected=rng.choice([s for s,l in PROFILES.items()if l==level])
 if selected not in PROFILES or PROFILES[selected]!=level:raise ValueError('Ineligible profile')
 p=copy.deepcopy(parameters)if parameters is not None else rng.choice(candidates(selected));check_parameters(selected,p)
 sid=sid_for(selected);old=SOURCES[sid];qid=uid(VERSION+digest([selected,p]));fields=[]
 for fi,of in enumerate(old[':question/answer-fields']):
  fid=uid(qid+':'+of[':answer-field/key']);bank=[]
  for ai,oa in enumerate(of[':answer-field/choices']):
   val=fmt.normalize_tex(render(selected,f'answer-{fi}-{ai}',p));bank.append({':answer/id':uid(fid+':'+str(ai)+':'+val),':answer/type':oa[':answer/type'][':db/ident'],':answer/value':val})
  ci=next(i for i,a in enumerate(of[':answer-field/choices'])if a[':answer/id']==of[':answer-field/correct'][':answer/id'])
  fields.append({':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':bank,':answer-field/correct':[':answer/id',bank[ci][':answer/id']]})
 q={':question/id':qid,':question/problem':fmt.normalize_prose(render(selected,'problem',p)),':question/worked-solution':fmt.normalize_prose(render(selected,'solution',p)),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields}
 r={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':selected,'profile':selected,'parameters':p,'source_question':old[':question/id'],'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'relationship_to_source_templates':'Observed complete profile with independent constant-multiple coefficient slots'if level!='hard'else 'Independently authored hard calibration of moderate three-term power/radical profile; no hard source evidence','domain':'x>0'if sid in ('q-104191','q-104192','q-342868','q-342966')else 'x!=0'if sid in ('q-342877','q-342970')else 'real x','dependencies':{'sympy':sp.__version__,'formatter':'private frozen math_format.py','parser':'private frozen display_parser.py'},'sampling_policy':'Exact finite coefficient multipliers; derivative order 2, operand structure, complete bank profile and every ordered source solution stage fixed'}}
 fmt.validate_generated_record(r);return r

def mathematical_fingerprint(r):
 x=parser.x;return digest([str(sp.expand(parser.function(r['question']))),r['question'][':question/problem'].split(' for ')[0],r['generation']['profile']=='q-342970'])
def catalog(level):return [(s,p)for s,l in PROFILES.items()if l==level for p in candidates(s)]
def batch(level,count=1,seed=0):
 if level not in (*SUPPORTED_LEVELS,'all'):raise ValueError('Unsupported difficulty')
 check_int(count,'count');check_int(seed,'seed')
 if count<1:raise ValueError('Positive count required')
 if level=='all':return [r for l in SUPPORTED_LEVELS for r in batch(l,count,seed)]
 options=catalog(level)
 if count>len(options):raise ValueError('finite-limit: '+str(len(options)))
 random.Random(seed).shuffle(options)
 return [generate(level,seed,template=s,parameters=p)for s,p in options[:count]]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value']for f in q[':question/answer-fields']for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',required=True,choices=(*SUPPORTED_LEVELS,'all'));ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');a=ap.parse_args();rs=batch(a.difficulty,a.count,a.seed);print(json.dumps(rs,indent=2,ensure_ascii=False)if a.format=='json'else'\n\n'.join(map(markdown,rs)))
