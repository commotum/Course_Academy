#!/usr/bin/env python3
"""Complete the square, negative even linear terms. Local review generator, no DB writes.

Frozen math basis 1356. Source profiles are parameterized evidence replay, preserving
raw omissions. Two historical expression banks expose opaque residual parameters;
they are never promoted to learning. Default five-choice banks use the real
half-coefficient, sign, omitted correction and unsquared correction operations.

Easy: direct/fragment completion, positive constant. Moderate: identify p,q with
nonnegative constant (including absent zero). Hard: authored p,q with negative
constant: subtract a square and combine two negative constants. All use exactly
the source's four-stage method, with integer half-coefficients 1..12; odd linear
terms, nonmonic quadratics and solving equations belong to successor topics.
Explicit bounds equal sampling bounds. No within-level progression.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186068876
KP_UUID='08c6d8d6-3d86-5074-bf99-0cb744c9412a'
TITLE='Completing the Square on a Quadratic Expression with a Negative Linear Term'
VERSION='negative-completion-1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
# Complete captured profiles; opaque components are explicit evidence parameters,
# never a fitted polynomial or default distractor claim.
CASES={
 'q-235904':dict(level='easy',template='fragment',v='y',h=9,c=64),
 'q-25253':dict(level='moderate',template='pq_plus',v='y',h=4,c=12),
 'q-141615':dict(level='easy',template='direct',v='x',h=6,c=28),
 'q-141611':dict(level='easy',template='direct',v='x',h=5,c=19,opaque=[-12,9,3,-5]),
 'q-141612':dict(level='easy',template='direct',v='y',h=2,c=10,opaque=[1,-4,3,5]),
 'q-250465':dict(level='easy',template='fragment',v='y',h=12,c=44),
 'q-250466':dict(level='easy',template='fragment',v='y',h=5,c=53),
 'q-250517':dict(level='moderate',template='pq_minus',v='x',h=5,c=0),
 'q-3662':dict(level='moderate',template='pq_plus',v='x',h=1,c=0),
 'q-141622':dict(level='moderate',template='pq_plus',v='y',h=5,c=30),
}
TEMPLATES={'easy':('direct','fragment'),'moderate':('pq_plus','pq_minus'),'hard':('pq_plus','pq_minus')}


def dump(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def uid(tag,obj):return str(uuid.uuid5(uuid.UUID(KP_UUID),tag+dump(obj)))
def signed(n):return ('+' if n>=0 else '-')+str(abs(n))
def polynomial(v,h,c,show_zero=False):return '{'+v+'}^{2}-'+str(2*h)+v+(signed(c) if c or show_zero else '')
def square(v,h,grouped=True):return '('+v+'-'+str(h)+('{)}' if grouped else ')')+'^{2}'


def worked(p,template,style='constant',grouped=True):
 """Ordered unevaluated factor/add-subtract/factor/collect masks, source prose."""
 v,h,c=p['v'],p['h'],p['c'];r=c-h*h
 omit=style=='omit_zero';tail='' if omit else signed(c)
 # Positive source constants include +0; signed authored constants never use +-. 
 first='{'+v+'}^{2}-2\\cdot '+str(h)+v+tail
 second='{{'+v+'}^{2}-2\\cdot '+str(h)+v+'+{'+str(h)+'}^{2}}_{⏟}-\\,{'+str(h)+'}^{2}'+tail
 sq=square(v,h,grouped)
 third=sq+'-{'+str(h)+'}^{2}'+tail
 final=sq+signed(r)
 intro='First, we rewrite the coefficient of the linear term as a product with $2$ as a factor:'
 trick="Now, here's the trick. We *add* and *then subtract* ${"+str(h)+'}^{2}'+(':$ ' if omit else ',$ writing the constant term $'+str(c)+'$ last:')
 factor='The first three terms form a perfect square, which we factor as follows:'
 finish='Finally, evaluating the last '+('term' if omit else 'two terms')+', we get'
 # q-250517 does not put a period in its final math row.
 period='' if style=='written_zero' else '.'
 text=intro+'\n\n$$\n'+first+'\n$$\n\n'+trick+'\n\n$$\n'+second+'\n$$\n\n'+factor+'\n\n$$\n'+third+'\n$$\n\n'+finish+'\n\n$$\n'+final+period+'\n$$'
 if template.startswith('pq'):
  pv=h if template=='pq_minus' else -h
  text+='\n\nTherefore, $p='+str(pv)+'$ and $q='+str(r)+'.$'
 return text


def raw_prompt(sid,p):
 """Complete mathematical component masks, retaining original punctuation/layout."""
 v,h,c=p['v'],p['h'],p['c'];poly=polynomial(v,h,c)
 if sid=='q-235904':
  pretty=v+'^{2} - '+str(2*h)+v+' + '+str(c)
  return 'Complete the square on the quadratic expression $'+pretty+'$.$'+pretty+' = ($ {{field-1}} $)^{2} -$\n{{field-2}}'
 if sid=='q-25253':
  return 'If the expression $'+v+'^{2} - '+str(2*h)+v+' + '+str(c)+'$ is written as $('+v+' + p)^{2} + q$, then what are the values of $p$ and $q$?'
 if sid in ('q-141615','q-141611','q-141612'):
  return 'Complete the square on the quadratic expression $'+poly+'.$'
 if sid in ('q-250465','q-250466'):
  return 'Complete the square on the quadratic expression $'+poly+'.$\n\n$'+poly+'=(${{field-1}}${)}^{2}\\,'+('-' if c<h*h else '+')+'$\n{{field-2}}'
 op='-' if sid=='q-250517' else '+'
 suffix=',' if sid=='q-141622' else ''
 text='If the expression $'+poly+'$ is written as $('+v+op+'p{)}^{2}+q'+suffix+('$ then' if suffix else '$, then')+' what are the values of $p$ and $q?$'
 if sid=='q-250517':text+='\n\n$p=$\n{{field-1}},\n$\\,q=$\n{{field-2}}'
 return text


def raw_values(sid,p):
 v,h,c=p['v'],p['h'],p['c'];r=c-h*h
 if sid=='q-235904':return {}
 if sid=='q-25253':
  pairs=[(-h,-r),(-h,r),(h,-r),(h,r),(-h,-h*h)]
  return {'selection':['p ='+(' ' if a>0 else '')+str(a)+', q ='+(' ' if b>0 else '')+str(b) for a,b in pairs]}
 if sid in ('q-141611','q-141612'):
  if 'opaque' not in p or len(p['opaque'])!=4:raise ValueError('opaque historical bank requires four explicit scalar components')
  o=p['opaque'];components=([(h,o[0]),(h,o[1]),(h,r),(h,o[2]),(2*h,o[3])] if sid=='q-141611' else [(2*h,o[0]),(h,o[1]),(h,o[2]),(h,r),(2*h,o[3])])
  return {'selection':[square(v,a)+signed(b) for a,b in components]}
 if sid in ('q-250465','q-250466'):return {'field-1':[v+'-'+str(h)],'field-2':[str(abs(r))]}
 if sid=='q-250517':return {'field-1':[str(h)],'field-2':[str(r)]}
 pairs=([(-h,r),(-h,-2*h),( -2*h,r),(-2*h,-r),(-h,2*h)] if sid=='q-3662' else [(-h,2*r),(h,r),(-2*h,r),(-h,r),(h,-r)])
 return {'selection':['p='+str(a)+r',\text{ }q='+str(b) for a,b in pairs]}


def enum(x,prefix):
 if isinstance(x,dict):x=x[':db/ident']
 return x if x.startswith(':') else ':'+prefix+'/'+x


def identity_payload(q):
 """Presence of correct/choices/difficulty is material; order and UUIDs are not."""
 x={k:q[k] for k in (':question/problem',':question/worked-solution',':question/difficulty') if k in q}
 if ':question/answer-fields' in q:
  x['fields']=[]
  for f in sorted(q[':question/answer-fields'],key=lambda z:z[':answer-field/key']):
   y={'key':f[':answer-field/key'],'type':f[':answer-field/type']}
   choices=f.get(':answer-field/choices',[])
   if ':answer-field/choices' in f:y['choices']=sorted([(a[':answer/type'],a[':answer/value']) for a in choices])
   if ':answer-field/correct' in f:
    ref=f[':answer-field/correct'][1];matches=[a for a in choices if a[':answer/id']==ref]
    if len(matches)!=1:raise ValueError('correct answer must be owned')
    y['correct']=(matches[0][':answer/type'],matches[0][':answer/value'])
   x['fields'].append(y)
 return {'version':VERSION,'content':x}


def finalize(q,p,template,level,seed,profile,raw=False):
 ident=identity_payload(q);qid=uid('question',ident)
 for f in q.get(':question/answer-fields',[]):
  key=f[':answer-field/key'];old=f.get(':answer-field/correct');mapping={}
  fid=uid('field',[ident,key]);f[':answer-field/id']=fid
  for a in f.get(':answer-field/choices',[]):
   aid=uid('answer',[ident,key,a[':answer/type'],a[':answer/value']]);mapping[a[':answer/id']]=aid;a[':answer/id']=aid
  if old:f[':answer-field/correct']=[':answer/id',mapping[old[1]]]
  if f[':answer-field/type']==':answer-field.type/radio':random.Random(str(seed)+key).shuffle(f.get(':answer-field/choices',[]))
 q[':question/id']=qid
 # Canonical polynomial task, response demand; excludes spelling, profile/bank and seed.
 task={'linear':-2*p['h'],'constant':p['c'],'response':'pq' if template.startswith('pq') else 'completed_square'}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
  'generation':{'version':VERSION,'difficulty':level,'seed':seed,'template':template,'profile':profile,'parameters':copy.deepcopy(p),
   'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'origin':'raw_observed_evidence' if raw else ('authored_missing_level' if level=='hard' else 'source_method_authored_bank'),
   'evidence_only':raw,'eligible_for_learning':not raw,'mathematical_fingerprint':hashlib.sha256(dump(task).encode()).hexdigest(),
   'content_fingerprint':hashlib.sha256(dump(ident).encode()).hexdigest(),'python':sys.version.split()[0],'sympy':sp.__version__}}


def guard(p,level,template,raw=False):
 if set(p)-{'v','h','c','opaque'}:raise ValueError('unknown parameters')
 if p.get('v') not in ('x','y','z'):raise ValueError('variable x/y/z required')
 if type(p.get('h')) is not int or not 1<=p['h']<=12:raise ValueError('half-coefficient integer 1..12')
 if type(p.get('c')) is not int or not -60<=p['c']<=144:raise ValueError('constant integer -60..144')
 if 'opaque' in p and (not raw or len(p['opaque'])!=4 or any(type(n) is not int or abs(n)>300 for n in p['opaque'])):raise ValueError('opaque components are four evidence-only integers of magnitude at most 300')
 if raw:return
 if level=='easy' and (template not in TEMPLATES[level] or not 1<=p['c']<=144):raise ValueError('easy positive constant and direct/fragment')
 if level=='moderate' and (template not in TEMPLATES[level] or not 0<=p['c']<=144):raise ValueError('moderate nonnegative constant and p/q')
 if level=='hard' and (template not in TEMPLATES[level] or not -60<=p['c']<=-1 or p['h']<3):raise ValueError('hard negative constant -60..-1 and half-coefficient 3..12 and p/q')
 if p['c']==p['h']**2:raise ValueError('nonzero residual required')


def raw_question(sid,p):
 src=QUESTIONS[sid];q={':question/problem':raw_prompt(sid,p)}
 if ':question/difficulty' in src:q[':question/difficulty']=enum(src[':question/difficulty'],'question.difficulty')
 if ':question/worked-solution' in src:
  style='omit_zero' if sid=='q-3662' else ('written_zero' if sid=='q-250517' else 'constant')
  q[':question/worked-solution']=worked(p,CASES[sid]['template'],style,grouped=sid!='q-141615')
 if ':question/answer-fields' in src:
  q[':question/answer-fields']=[];values=raw_values(sid,p)
  for sf in src[':question/answer-fields']:
   key=sf[':answer-field/key'];f={':answer-field/key':key,':answer-field/type':enum(sf[':answer-field/type'],'answer-field.type')}
   if ':answer-field/choices' in sf:
    f[':answer-field/choices']=[{':answer/id':str(i),':answer/type':enum(a[':answer/type'],'answer.type'),':answer/value':values[key][i]} for i,a in enumerate(sf[':answer-field/choices'])]
   if ':answer-field/correct' in sf:
    idx=next(i for i,a in enumerate(sf[':answer-field/choices']) if a[':answer/id']==sf[':answer-field/correct'][':answer/id'])
    f[':answer-field/correct']=[':answer/id',str(idx)]
   q[':question/answer-fields'].append(f)
 for f in q.get(':question/answer-fields',[]):
  vals=[a[':answer/value'] for a in f.get(':answer-field/choices',[])]
  if len(set(vals))!=len(vals):raise ValueError('whole raw bank collision')
 return q


def normal_question(p,level,template,kind):
 v,h,c=p['v'],p['h'],p['c'];r=c-h*h;poly=polynomial(v,h,c)
 q={':question/difficulty':':question.difficulty/'+level,':question/worked-solution':worked(p,template,('written_zero' if template=='pq_minus' else 'omit_zero') if c==0 else 'constant'),':question/answer-fields':[]}
 if template in ('direct','fragment'):
  prompt='Complete the square on the quadratic expression $'+poly+'.$'
  if kind=='blank':prompt+=' Use a binomial whose coefficient of $'+v+'$ is positive.\n\n$'+poly+'=(${{field-1}}${)}^{2}\\,'+('+' if r>0 else '-')+'$\n{{field-2}}'
 else:
  op='-' if template=='pq_minus' else '+'
  prompt='If the expression $'+poly+'$ is written as $('+v+op+'p{)}^{2}+q$, then what are the values of $p$ and $q?$'
  if kind=='blank':prompt+='\n\n$p=$\n{{field-1}},\n$\\,q=$\n{{field-2}}'
 q[':question/problem']=prompt
 if kind=='blank':
  vals=([v+'-'+str(h),str(abs(r))] if template in ('direct','fragment') else [str(h if template=='pq_minus' else -h),str(r)])
  banks=[('field-'+str(i+1),[value],0) for i,value in enumerate(vals)]
 else:
  # Complete method-derived bank: correct, wrong binomial sign, omit square
  # subtraction, subtract h instead of h², fail to halve the linear coefficient.
  objs=[(h,r),(-h,r),(h,c),(h,c-h),(2*h,c-4*h*h)]
  if template in ('direct','fragment'):
   vals=[('('+v+('+' if a<0 else '-')+str(abs(a))+'{)}^{2}'+signed(b)) for a,b in objs]
  else:
   vals=['p='+str(a if template=='pq_minus' else -a)+r',\text{ }q='+str(b) for a,b in objs]
  # Equality of full polynomials/tuples; never pick a replacement distractor.
  if len(set(objs))!=5:raise ValueError('whole bank collision')
  banks=[('selection',vals,0)]
 for key,vals,correct in banks:
  q[':question/answer-fields'].append({':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,
   ':answer-field/choices':[{':answer/id':str(i),':answer/type':':answer.type/math',':answer/value':val} for i,val in enumerate(vals)],
   ':answer-field/correct':[':answer/id',str(correct)]})
 return q


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in TEMPLATES:raise ValueError('difficulty easy/moderate/hard required')
 kind=(field_type or '').removeprefix(':answer-field.type/')
 if kind and kind not in ('radio','blank'):raise ValueError('field selector radio/blank')
 if profile and profile.startswith('source:'):
  sid=profile.split(':',1)[1]
  if sid not in CASES:raise ValueError('unknown source profile')
  case=CASES[sid]
  if level!=case['level'] or template not in (None,case['template']):raise ValueError('source profile level/template mismatch')
  template=case['template'];p=copy.deepcopy(parameters) if parameters is not None else {k:v for k,v in case.items() if k not in ('level','template')}
  guard(p,level,template,raw=True)
  if sid in ('q-235904','q-25253') and p['c']<1:raise ValueError('spaced historical positive-constant mask')
  if sid=='q-235904' and p['c']>=p['h']**2:raise ValueError('historical blank supplies a negative residual sign')
  if sid=='q-3662' and p['c']!=0:raise ValueError('omitted constant profile requires c=0')
  q=raw_question(sid,p)
  observed={f[':answer-field/type'].split('/')[-1] for f in q.get(':question/answer-fields',[])}
  if kind and (not observed or observed!={kind}):raise ValueError('source field selector mismatch or fieldless evidence')
  return finalize(q,p,template,level,seed,profile,raw=True)
 if profile not in (None,'authored_method'):raise ValueError('unknown profile')
 rng=random.Random(seed)
 if template is None:
  eligible=list(TEMPLATES[level]);template=rng.choice(eligible)
 if template not in TEMPLATES[level]:raise ValueError('unsupported level/template')
 kind=kind or ('blank' if template in ('fragment','pq_minus') else 'radio')
 if parameters is not None:
  p=copy.deepcopy(parameters);guard(p,level,template);q=normal_question(p,level,template,kind)
 else:
  for _ in range(1000):
   p={'v':rng.choice(('x','y','z')),'h':rng.randint(3 if level=='hard' else 1,12),'c':rng.randint(-60,-1) if level=='hard' else rng.randint(0 if level=='moderate' else 1,144)}
   try:guard(p,level,template);q=normal_question(p,level,template,kind);break
   except ValueError:continue
  else:raise RuntimeError('no eligible complete bank')
 return finalize(q,p,template,level,seed,'authored_method')

# Easy: observed direct completion and binomial/constant fragment shapes.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: observed p/q recognition with nonnegative/absent constant.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: authored signed-constant bookkeeping, same four operation stages.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)


def markdown(record):
 q=record['question'];parts=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  parts.append('\n'+f[':answer-field/key']+' ('+f[':answer-field/type']+')')
  for a in f.get(':answer-field/choices',[]):parts.append('- $'+a[':answer/value']+'$')
 if ':question/worked-solution' in q:parts+=['\nWorked solution',q[':question/worked-solution']]
 return '\n'.join(parts)

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--field-type');args=ap.parse_args()
 if args.count<1:ap.error('count must be positive')
 records=[generate(level,args.seed+i,args.template,args.field_type,profile=args.profile) for level in (TEMPLATES if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
