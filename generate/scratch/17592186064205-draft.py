#!/usr/bin/env python3
"""Private bounded draft; no database operations. Fractional affine substitution."""
import argparse,copy,hashlib,importlib.util,json,random,sys,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186064205
KP_UUID='0ae5760b-9277-596c-8546-dca4fd985bd7'
TITLE='Integrating an Algebraic Function With Fractional Exponent'
VERSION='fractional-affine-v2-draft'
PACKAGE=Path(__file__).with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
PROFILES=json.loads((PACKAGE/'templates.json').read_text())
SOURCE=json.loads((PACKAGE/'source.json').read_text())
LEVELS=('easy','moderate','hard')
DOMAIN=tuple(range(-100,101))
_spec=importlib.util.spec_from_file_location('fractional_private_math_format',PACKAGE/'math_format.py')
_formatter=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_formatter)
normalize_prose=_formatter.normalize_prose;normalize_tex=_formatter.normalize_tex

def integer(v,name):
 if type(v) is not int:raise ValueError(name+' must be builtin int, excluding bool')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def base(t,b):
 a=t['a'];v=t['variable'];ax=v if a==1 else '-'+v if a==-1 else str(a)+v
 if a<0:return str(b)+ax
 return ax+('+' if b>=0 else '')+str(b)
def candidates(sid):
 if type(sid) is not str or sid not in PROFILES:raise ValueError('Unknown template')
 return [[b] for b in DOMAIN]
def fingerprint_parameters(t,b):return digest([t['a'],b,t['numerator'],t['denominator']])
def source_record(source_id,raw=False):
 if type(source_id) is not str or type(raw) is not bool:raise ValueError('source_id str and raw bool required')
 for q in SOURCE['record'][':knowledge-point/questions']:
  if source_id in (q.get(':question/math-academy-id'),str(q[':db/id'])):
   q=copy.deepcopy(q)
   if not raw:
    for k in (':question/problem',':question/worked-solution'):
     if k in q:q[k]=normalize_prose(q[k])
    for f in q.get(':question/answer-fields',[]):
     for a in f[':answer-field/choices']:a[':answer/value']=normalize_tex(a[':answer/value'])
   return q
 raise ValueError('Unknown source')
def domain_for(t,b):
 # All served prompts are interpreted on this explicit open real interval.
 # This conservative restriction also keeps the source shifted distractor base-2 positive.
 lower=2 if any(r['offset']==-2 for r in t['bank']) else 0
 boundary=sp.Rational(lower-b,t['a'])
 return {'number_system':'real','branch':'positive radicands, principal real roots','constraint':f"{base(t,b)} > {lower}",'variable':t['variable'],'relation':'>' if t['a']>0 else '<','boundary':str(boundary),'base_lower_exclusive':lower,'reason':'Open positive-base interval makes all fractional powers and every answer choice real; no powers identities are asserted outside this domain.'}

def _source_generate(level,seed,sid,parameters):
 source_id=sid.removeprefix('source:');q=source_record(source_id,raw=True)
 key=q.get(':question/math-academy-id')
 if key in PROFILES:t=PROFILES[key];old=t['base'];original_b=t['b']
 elif source_id=='17592186484773':t=PROFILES['q-49431'];old='-9-9z';original_b=-9
 elif source_id=='17592186484781':t=PROFILES['q-12498'];old='5x-50';original_b=-50
 else:raise ValueError('Unknown source profile')
 p=_parameters(parameters,original_b);b=p['b'];new=old if b==original_b else base(t,b)
 def render(s):return s.replace(old,new).replace('1-5s',base(t,b-2)) if key=='q-49393' and b!=original_b else s.replace(old,new)
 for k in (':question/problem',':question/worked-solution'):
  if k in q:q[k]=normalize_prose(render(q[k]))
 for f in q.get(':question/answer-fields',[]):
  f.pop(':db/id',None);f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f[':answer-field/choices']:
   a.pop(':db/id',None);a[':answer/type']=a[':answer/type'][':db/ident'];a[':answer/value']=normalize_tex(render(a[':answer/value']))
  if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 if ':question/difficulty' in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 q.pop(':db/id',None);q.pop(':question/math-academy-id',None)
 _identities(q,['source',sid,p])
 return _record(q,level,seed,sid,p,t,'independent_inventory_reference' if key is None else 'faithful_source_replay; includes documented source errors/omissions')
def _parameters(parameters,default):
 if parameters is None:return {'b':default}
 if type(parameters) is not dict or set(parameters)!={'b'}:raise ValueError('parameters must be exactly {b: builtin int}')
 integer(parameters['b'],'b')
 if parameters['b'] not in DOMAIN:raise ValueError('b outside -100..100')
 return dict(parameters)
def _identities(q,content):
 qid=ident([VERSION,content,q[':question/problem'],q.get(':question/worked-solution'),[[a[':answer/value'] for a in f[':answer-field/choices']] for f in q[':question/answer-fields']]]);q[':question/id']=qid
 for i,f in enumerate(q[':question/answer-fields']):
  correct=f.get(':answer-field/correct',[None,None])[1];fid=ident([qid,'field',i,f[':answer-field/key']]);f[':answer-field/id']=fid
  for a in f[':answer-field/choices']:
   old=a[':answer/id'];a[':answer/id']=ident([fid,a[':answer/value']])
   if old==correct:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
def _record(q,level,seed,sid,p,t,role):
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':sid,'profile':sid,'bank_profile':sid,'parameters':p,'difficulty':level,'source_ids':(['q-12498','e-448'] if sid=='easy-square-root' else [sid]),'domain':domain_for(t,p['b']),'mathematical_fingerprint':fingerprint_parameters(t,p['b']),'parameter_fingerprint':fingerprint_parameters(t,p['b']),'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'evidence_role':role,'dependencies':{'sympy':sp.__version__,'python':sys.version.split()[0]},'sampling_policy':'Only affine constant b varies in -100..100. Slope, exponent, complete bank and ordered solution stages stay fixed.','plot_rating':'none'}}
def generate(difficulty='moderate',seed=0,template=None,parameters=None,profile=None):
 integer(seed,'seed')
 if type(difficulty) is not str or difficulty not in LEVELS:raise ValueError('Unsupported difficulty')
 if any(v is not None and type(v) is not str for v in (template,profile)):raise ValueError('template/profile must be strings')
 if any(v=='' for v in (template,profile) if v is not None):raise ValueError('Unknown empty profile')
 if template and profile and template!=profile:raise ValueError('template/profile mismatch')
 rng=random.Random(seed);sid=profile or template or rng.choice([s for s,t in PROFILES.items() if t['difficulty']==difficulty])
 if sid.startswith('source:'):return _source_generate(difficulty,seed,sid,parameters)
 if sid not in PROFILES or PROFILES[sid]['difficulty']!=difficulty:raise ValueError('Unknown/ineligible template')
 t=PROFILES[sid];p=_parameters(parameters,rng.choice(DOMAIN));b=p['b']
 def render(s):return s.replace('@@BASE@@',base(t,b)).replace('@@ALTERED@@',base(t,b-2))
 values=[normalize_tex(render(z['value'])) for z in t['bank']]
 solution=render(t['solution'])
 if sid=='q-17019':solution=solution.replace('^{3/2}','^{2/3}')
 solution=solution.replace('final answer in terms of $u$ at the very end','final answer in terms of $'+t['variable']+'$ at the very end')
 f={':answer-field/id':'pending',':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/id':str(i),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(values)],':answer-field/correct':[':answer/id',str(next(i for i,r in enumerate(t['bank']) if r['correct']))]}
 q={':question/problem':normalize_prose(render(t['prompt'])),':question/worked-solution':normalize_prose(solution),':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[f]}
 _identities(q,[difficulty,sid,p])
 # Dedicated option RNG cannot perturb parameter selection or stable IDs.
 random.Random(digest(['options',sid,p])).shuffle(f[':answer-field/choices'])
 return _formatter.validate_generated_record(_record(q,difficulty,seed,sid,p,t,t['evidence_role']))
def capacity(difficulty):
 if type(difficulty) is not str or difficulty not in LEVELS:raise ValueError('Unsupported difficulty')
 return len({fingerprint_parameters(t,b) for t in PROFILES.values() if t['difficulty']==difficulty for b in DOMAIN})
def batch(difficulty,count=1,seed=0):
 integer(seed,'seed');integer(count,'count')
 if type(difficulty) is not str or difficulty not in LEVELS or count<0:raise ValueError('Unsupported difficulty/count')
 if count>capacity(difficulty):raise ValueError('Requested count exceeds finite mathematical capacity')
 pairs=[(s,b) for s,t in PROFILES.items() if t['difficulty']==difficulty for b in DOMAIN];random.Random(seed).shuffle(pairs);out=[];seen=set()
 for s,b in pairs:
  if len(out)==count:break
  fp=fingerprint_parameters(PROFILES[s],b)
  if fp in seen:continue
  r=generate(difficulty,seed,s,{'b':b});seen.add(fp);out.append(r)
 return out
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+z[':answer/value']+'$' for f in q[':question/answer-fields'] for z in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rows=[r for level in LEVELS for r in batch(level,a.count,a.seed)] if a.difficulty=='all' else batch(a.difficulty,a.count,a.seed);print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
