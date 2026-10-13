"""Finding ranges of transformed sinusoids; local draft, basis 1356.

Normal defaults select a complete family and bank before sampling. Public raw
profiles preserve missing attributes and source errors and are evidence-only.
All arithmetic is exact. No assets or database writes are used.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186129124
KP_UUID='5696c2d5-4e35-5ed3-a4a2-6fe9b158e461'
TITLE='Finding the Range of a Transformed Sinusoidal Function'
VERSION='1.0.0'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
LEVELS=('easy','moderate','hard')
# Complete components, never unconstrained substring replacements.
RAW={
'q-10249':dict(A=3,B=2,C=1,D=-4,trig='sin',out='y',unit='linear',level='easy',arg='2x + 1',prompt=r'y = 3\sin (2x + 1) - 4'),
'q-40977':dict(A=-1,B=1,C='pi/4',D=3,trig='cos',out='f(x)',unit='radian',level='moderate',arg=r'x + \frac{π}{4}',prompt=r'f(x) =-\cos (x + \frac{π}{4}) + 3'),
'q-25512':dict(A=-2,B=3,C=0,D=1,trig='sin',out='f(x)',unit='linear',level='moderate',arg='3x',prompt=r'f(x)=-2\operatorname{sin}(3x)+1.'),
'q-40908':dict(A=4,B=1,C=30,D=-2,trig='sin',out='f(x)',unit='degree',level='easy',arg='x+{30}^{∘}',prompt=r'f(x)=4\operatorname{sin}(x+{30}^{∘})-2?'),
'q-10379':dict(A=2,B=4,C=0,D=-2,trig='cos',out='y',unit='linear',level='easy',arg='4x',prompt='y=2\\operatorname{cos}⁡(4x)-2.'),
'q-40903':dict(A=3,B=1,C='pi/6',D=2,trig='sin',out='f(x)',unit='radian',level='easy',arg=r'x+\frac{\pi }{6}',prompt='f(x)=3\\operatorname{sin}⁡(x+\\frac{\\pi }{6})+2?'),
'q-41840':dict(A=-2,B=1,C=30,D=4,trig='sin',out='y',unit='degree',level='easy',arg='x+{30}^{∘}',prompt='y=-2\\operatorname{sin}⁡(x+{30}^{∘})+4?'),
'q-41964':dict(A=-4,B=1,C=-30,D=1,trig='cos',out='y',unit='degree',level='moderate',arg='x-{30}^{∘}',prompt='y=-4\\operatorname{cos}⁡(x-{30}^{∘})+1?'),
'q-65928':dict(A=-1,B=3,C='pi',D=-4,trig='cos',out='f(x)',unit='radian',level='moderate',arg=r'3x+\pi ',prompt='f(x)=-\\operatorname{cos}⁡(3x+\\pi )-4?'),
}
TEMPLATES={f'{response}_{trig}_{unit}':dict(response=response,trig=trig,unit=unit,out='f(x)' if response=='minimum' else 'y')
 for response in ('range','minimum') for trig in ('sin','cos') for unit in ('linear','degree','radian')}
BANK_PROFILES={
'endpoints':dict(response='range',origin='observed-method-derived',recipes=['closed range','open both','open lower','open upper','unbounded']),
'outer_transform':dict(response='range',origin='authored-method-derived',recipes=['D +/- abs(A)','omit D','negate D','omit A','use abs(A*B)']),
'extrema':dict(response='minimum',origin='observed-method-derived',recipes=['D-abs(A)','D+abs(A)','D','abs(A)','-abs(A)']),
}
for sid in RAW:
 BANK_PROFILES['raw_'+sid]=dict(origin='raw-evidence',source_id=sid)

class SampleRejected(ValueError): pass

def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,f'{KP_ID}/{s}'))
def tex(n): return sp.latex(sp.sympify(n))
def rat(n):
 v=sp.sympify(n)
 if not v.is_Rational: raise ValueError('A, B and D must be exact rational values')
 return v

def source_parameters(sid): return {k:str(RAW[sid][k]) for k in ('A','B','C','D')}
def normalize(p):
 if set(p)!=set(('A','B','C','D')): raise ValueError('Parameters are exactly A, B, C, D')
 v={k:rat(p[k]) for k in ('A','B','D')};v['C']=sp.sympify(p['C'])
 if v['A']==0 or v['B']==0: raise ValueError('A and B must be nonzero')
 return v

def guard(level,spec,p,raw=False):
 a,b,c,d=(p[k] for k in ('A','B','C','D'))
 if not 0<abs(a)<=6 or not 1<=b<=5 or not b.is_Integer or not 0<abs(d)<=8: raise ValueError('Coefficient workload bounds exceeded')
 if spec['unit']=='degree':
  if b!=1 or not c.is_Integer or c not in (-90,-60,-45,-30,-15,15,30,45,60,90): raise ValueError('Degree shifts require B=1 and a familiar nonzero angle')
 elif spec['unit']=='linear':
  if not c.is_Integer or abs(c)>3: raise ValueError('Linear shift must be an integer -3..3')
 elif c not in (0,sp.pi,-sp.pi,sp.pi/2,-sp.pi/2,sp.pi/3,-sp.pi/3,sp.pi/4,-sp.pi/4,sp.pi/6,-sp.pi/6): raise ValueError('Radian shift must be a familiar multiple of pi')
 if raw:
  if not a.is_Integer or not d.is_Integer:raise ValueError('Raw source masks retain integer coefficient number forms')
  return
 if level=='easy' and (a<=0 or not a.is_Integer or not d.is_Integer): raise ValueError('Authored easy uses positive integer A and integer D')
 if level=='moderate' and (a>=0 or not a.is_Integer or not d.is_Integer): raise ValueError('Authored moderate uses negative integer A and integer D')
 if level=='hard' and (a>=0 or a.is_Integer or d.is_Integer or a.q not in (2,3,4) or d.q not in (2,3,4) or abs(a.p)>12 or abs(d.p)>16): raise ValueError('Authored hard requires reduced noninteger A,D with small denominators and negative A')

def signed(v): return ('+' if v>=0 else '-')+tex(abs(v))
def coefficient(a): return '' if a==1 else '-' if a==-1 else tex(a)
def argument(spec,p):
 b,c=p['B'],p['C'];s=coefficient(b)+'x'
 if c:
  z=tex(abs(c))+r'^{\circ}' if spec['unit']=='degree' else tex(abs(c))
  s+=('+' if c>0 else '-')+z
 return s

def math_components(spec,p):
 a,d=p['A'],p['D'];arg=argument(spec,p);trig='\\'+spec['trig']
 t=trig+'('+arg+')';scaled=coefficient(a)+t;fun=scaled+signed(d)
 return dict(base=trig+' x',trig=t,scaled=scaled,fun=fun,lo=d-abs(a),hi=d+abs(a))

def normal_solution(spec,p):
 a,d=p['A'],p['D'];m=math_components(spec,p);op=r'\ge' if a<0 else r'\le'
 rows=[r'-1\le '+m['trig']+r'\le 1',tex(-a)+op+' '+m['scaled']+op+' '+tex(a),tex(d-a)+op+' '+m['fun']+op+' '+tex(d+a),tex(m['lo'])+r'\le '+spec['out']+r'\le '+tex(m['hi'])+'.']
 solution='The range of $'+m['base']+'$ is\n\n$$\n-1\\le '+m['base']+'\\le 1.\n$$\n\nHorizontal shifts and stretches have no effect on the range. Therefore,\n\n$$\n-1\\le '+m['trig']+'\\le 1.\n$$\n\n'
 solution+='Multiplying the above inequality by $'+tex(a)+'$ and then '+('adding' if d>0 else 'subtracting')+' $'+tex(abs(d))+'$, we get\n\n$$\n\\begin{aligned} & '+' \\\\  & '.join(rows)+r'\end{aligned}'+'\n$$\n\n'
 if spec['response']=='range': solution+='Therefore, the range is $'+spec['out']+r'\in ['+tex(m['lo'])+','+tex(m['hi'])+'].$'
 else: solution+='Therefore, the minimum value is $'+tex(m['lo'])+'.$'
 return solution

# Raw extraction uses complete inline/display components and four ordered rows.
# Source masks retain byte-for-byte prose, notation and errors at original values.
def raw_solution(sid,p):
 q=ORIGINALS[sid];spec=RAW[sid]
 if ':question/worked-solution' not in q: return None
 old=source_parameters(sid);a0,d0=sp.Rational(old['A']),sp.Rational(old['D']);a,d=p['A'],p['D']
 spans=list(re.finditer(r'\$\$.*?\$\$|\$[^$]*\$',q[':question/worked-solution'],re.S))
 assert len(spans)==7
 arg=raw_argument(sid,p)
 trigbase=spans[0].group()[1:-1]
 oldarg=spec['arg']; t0=trigbase[:-1]+'('+oldarg+')';t=trigbase[:-1]+'('+arg+')'
 origrows=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',spans[5].group(),re.S).group(1).split(' \\\\ ')
 vals=[(-1,1),(-a,a),(d-a,d+a),(d-abs(a),d+abs(a))]
 newrows=[]
 for i,row in enumerate(origrows):
  # Build endpoint positions independently; preserve source alignment glyphs.
  pieces=re.split(r'(\\le |\\ge |\\le|\\ge)',row)
  assert len(pieces)==5
  l,op1,mid,op2,r=pieces
  nl,nr=vals[i]
  l=re.sub(r'-?\d+',lambda _:tex(nl),l,count=1)
  r=re.sub(r'-?\d+',lambda _:tex(nr),r,count=1)
  if i==0: mid=mid.replace(t0,t)
  elif i in (1,2):
   # q-25512's captured wrong 2x remains in evidence, scaled with B.
   oldt=t0.replace('3x','2x') if sid=='q-25512' else t0
   newt=t.replace(arg,coefficient(p['B']-1)+'x') if sid=='q-25512' else t
   mid=mid.replace(coefficient(a0)+oldt,coefficient(a)+newt)
   if i==2: mid=mid.replace(signed(d0),signed(d))
  newrows.append(l+op1+mid+op2+r)
 block=spans[5].group().replace(' \\\\ '.join(origrows),' \\\\ '.join(newrows))
 lo,hi=d-abs(a),d+abs(a)
 ending='$'+(tex(lo)+'.' if sid=='q-65928' else spec['out']+r'\in ['+tex(lo)+','+tex(hi)+'].' )+'$'
 shiftspan='$'+tex(abs(d))+(',' if ',' in spans[4].group() else '')+'$'
 new=[spans[0].group(),spans[1].group(),spans[2].group().replace(oldarg,arg),'$'+tex(a)+'$',shiftspan,block,ending]
 result=q[':question/worked-solution'];out=[];last=0
 for span,value in zip(spans,new,strict=True): out.extend((result[last:span.start()],value));last=span.end()
 out.append(result[last:]);result=''.join(out)
 return result.replace('then adding' if d0>0 else 'then subtracting','then adding' if d>0 else 'then subtracting')

def raw_argument(sid,p):
 spec=RAW[sid];orig=spec['arg'];base=source_parameters(sid)
 # Retain source whitespace, Unicode degree/pi spelling and complete argument.
 if spec['unit']=='degree': return 'x'+('+' if p['C']>0 else '-')+'{'+str(abs(p['C']))+'}^{∘}'
 if str(p['B'])==base['B'] and str(p['C'])==base['C']: return orig
 return argument(spec,p)

def raw_prompt(sid,p):
 spec=RAW[sid];old=spec['prompt'];arg=raw_argument(sid,p)
 # Preserve the extracted equation mask; substitute each complete component.
 a0,d0=sp.Rational(spec['A']),sp.Rational(spec['D']);a,d=p['A'],p['D']
 expr=old.replace(spec['arg'],arg)
 # Original A and D formatting is preserved at their values.
 if a!=a0:
  trigpos=expr.index('\\');start=expr.index('=')+1
  leading=expr[start:trigpos];space=leading[:len(leading)-len(leading.lstrip())]
  expr=expr[:start]+space+coefficient(a)+expr[trigpos:]
 if d!=d0:
  suffix=re.search(r'([+-]\s*\d+)([.?]?)$',expr)
  assert suffix
  expr=expr[:suffix.start()]+signed(d)+suffix.group(2)
 return ORIGINALS[sid][':question/problem'].replace(old,expr)

def raw_values(sid,p):
 """Opaque profiles use a documented affine endpoint envelope, never defaults.

 These coefficients recover only the observed complete values; they are not
 claimed to recover the historical misconception. Endpoint closure profile and
 minimum profile q-65928 have explicit method recipes instead.
 """
 a,d=p['A'],p['D'];r=abs(a);r0=abs(sp.Rational(RAW[sid]['A']));d0=sp.Rational(RAW[sid]['D'])
 original=ORIGINALS[sid].get(':question/answer-fields',[])
 if not original:return []
 options=original[0][':answer-field/choices'];result=[]
 for i,opt in enumerate(options):
  text=opt[':answer/value']
  nums=list(re.finditer(r'-\s*\d+|\d+',text))
  if sid=='q-10379':
   if i==4:result.append(text);continue
   values=[d-r,d+r]
  elif sid=='q-65928':values=[d,r,d-r,d+r,-r][i:i+1]
  elif sid=='q-10249':values=[(d-r,d+r),(-r,r),(-1,1),(d-r,1),(-abs(d),abs(d))][i]
  else:values=[d+(sp.Rational(m.group().replace(' ',''))-d0)/r0*r for m in nums]
  out=[];last=0
  for m,v in zip(nums,values,strict=True):
   value=tex(v)
   if v<0 and m.group().startswith('- '):value='- '+tex(abs(v))
   out.extend((text[last:m.start()],value));last=m.end()
  out.append(text[last:]);result.append(''.join(out))
 return result

def bank(spec,p,profile):
 m=math_components(spec,p);r=abs(p['A']);d=p['D'];lo,hi=m['lo'],m['hi']
 if profile=='endpoints': values=[(lo,hi,'[]'),(lo,hi,'()'),(lo,hi,'(]'),(lo,hi,'[)'),(-sp.oo,sp.oo,'()')]
 elif profile=='outer_transform':values=[(lo,hi,'[]'),(-r,r,'[]'),(-d-r,-d+r,'[]'),(d-1,d+1,'[]'),(d-r*p['B'],d+r*p['B'],'[]')]
 elif profile=='extrema':values=[lo,hi,d,r,-r]
 else:raise ValueError('Unknown normal profile')
 signatures=[str(x) for x in values]
 if len(set(signatures))!=5:raise SampleRejected('Reject complete bank: equivalent choices')
 if spec['response']=='minimum':return [tex(v) for v in values]
 return [spec['out']+r'\in '+br[0]+tex(l)+','+tex(h)+br[1] for l,h,br in values]

def assemble(level,seed,name,profile,p,prompt,solution,values,raw_sid=None):
 spec=RAW[raw_sid] if raw_sid else TEMPLATES[name]
 original=ORIGINALS[raw_sid] if raw_sid else None
 raw=raw_sid is not None
 # Mathematical identity excludes horizontal parameters/trig aliases: they have
 # no effect on this assessed transformation. Signed A captures reversal demand.
 task=dict(A=str(p['A']),D=str(p['D']),response='minimum' if name.startswith('minimum') or raw_sid in ('q-40977','q-65928') else 'range')
 mathkey=digest(task)
 presence={k:k in original for k in (':question/difficulty',':question/answer-fields',':question/worked-solution')} if raw else {}
 content=dict(version=VERSION,level=None if raw and not presence[':question/difficulty'] else level,prompt=prompt,solution=solution,values=sorted(values),raw=raw,presence=presence)
 key=digest(content);qid=uid(key);q={':question/id':qid,':question/problem':prompt}
 if not raw or presence[':question/difficulty']:q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 if not raw or presence[':question/answer-fields']:
  fid=uid(key+'/field/selection');answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
  f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
  if not raw:f[':answer-field/correct']=[':answer/id',answers[0][':answer/id']]
  elif ':answer-field/correct' in original[':question/answer-fields'][0]:
   oldf=original[':question/answer-fields'][0];oldid=oldf[':answer-field/correct'][':answer/id'];idx=next(i for i,a in enumerate(oldf[':answer-field/choices']) if a[':answer/id']==oldid)
   f[':answer-field/correct']=[':answer/id',answers[idx][':answer/id']]
  random.Random(seed).shuffle(answers);q[':question/answer-fields']=[f]
 return dict(knowledge_point=dict(db_id=KP_ID,id=KP_UUID,title=TITLE),question=q,generation=dict(version=VERSION,python_version=sys.version.split()[0],sympy_version=sp.__version__,seed=seed,template=name,bank_profile=profile,parameters={k:str(v) for k,v in p.items()},parameter_fingerprint=mathkey,mathematical_task=task,content_fingerprint=key,source_analysis={k:SOURCE[k] for k in ('database','basis','lineage')},source_ids=[raw_sid] if raw else list(RAW),authored_extension=not raw,origin='raw-evidence' if raw else BANK_PROFILES[profile]['origin'],evidence_only=raw,eligible_for_learning=not raw,raw_attribute_presence_preserved=raw,plot_rating='none',plot_assets={},domain='all real x',recipes=['documented raw complete bank envelope'] if raw else BANK_PROFILES[profile]['recipes'],inferred_correct=str(p['D']-abs(p['A'])) if spec.get('response')=='minimum' or raw_sid in ('q-40977','q-65928') else [str(p['D']-abs(p['A'])),str(p['D']+abs(p['A']))]))

def sample(level,spec,rng):
 if level=='easy':a=rng.randint(1,6);d=rng.choice([i for i in range(-8,9) if i])
 elif level=='moderate':a=-rng.randint(1,6);d=rng.choice([i for i in range(-8,9) if i])
 else:
  amplitudes=sorted({sp.Rational(-n,m) for n in range(1,13) for m in (2,3,4) if n%m and sp.Rational(n,m)<=6})
  shifts=sorted({sp.Rational(n,m) for n in range(-16,17) for m in (2,3,4) if n and n%m and abs(sp.Rational(n,m))<=8})
  a=rng.choice(amplitudes);d=rng.choice(shifts)
 b=1 if spec['unit']=='degree' else rng.randint(1,5)
 c=rng.choice((-90,-60,-45,-30,-15,15,30,45,60,90)) if spec['unit']=='degree' else rng.randint(-3,3) if spec['unit']=='linear' else rng.choice((0,sp.pi,-sp.pi,sp.pi/2,-sp.pi/2,sp.pi/3,-sp.pi/3,sp.pi/4,-sp.pi/4,sp.pi/6,-sp.pi/6))
 return dict(A=a,B=b,C=c,D=d)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unknown difficulty')
 if profile is not None and profile not in BANK_PROFILES:raise ValueError('Unknown bank profile')
 if field_type not in (None,'radio'):raise ValueError('Only observed radio response layout is supported')
 if profile and profile.startswith('raw_'):
  sid=profile[4:]
  if sid not in RAW:raise ValueError('Unknown raw profile')
  name='source_'+sid
  if template not in (None,name):raise ValueError('Raw profile and template mismatch')
  if level!=RAW[sid]['level']:raise ValueError('Use the documented observed/authored evidence level')
  p=normalize(source_parameters(sid) if parameters is None else parameters);guard(level,RAW[sid],p,raw=True)
  if sp.sign(p['A'])!=sp.sign(RAW[sid]['A']):raise ValueError('Raw source mask preserves the coefficient sign')
  values=raw_values(sid,p)
  if len({re.sub(r'\s+','',v).replace('∈',r'\in') for v in values})!=len(values):raise SampleRejected('Reject complete raw evidence bank: equivalent options')
  return assemble(level,seed,name,profile,p,raw_prompt(sid,p),raw_solution(sid,p),values,sid)
 rng=random.Random(seed)
 eligible=[t for t,s in TEMPLATES.items() if profile is None or profile in BANK_PROFILES and BANK_PROFILES[profile].get('response')==s['response'] and not (profile=='outer_transform' and s['unit']=='degree')]
 if template and template not in eligible:raise ValueError('Unknown or profile-incompatible template')
 name=template or rng.choice(eligible);spec=TEMPLATES[name]
 profiles=(['endpoints'] if spec['unit']=='degree' else ['endpoints','outer_transform']) if spec['response']=='range' else ['extrema']
 if profile and profile not in profiles:raise ValueError('Bank is incompatible with family')
 # For explicit parameters, bank selection is stable across option-shuffle seeds.
 chooser=random.Random(digest(dict(template=name,parameters=parameters))) if parameters is not None else rng
 profile=profile or chooser.choice(profiles)
 for _ in range(512):
  p=normalize(parameters) if parameters is not None else normalize(sample(level,spec,rng))
  guard(level,spec,p)
  try:values=bank(spec,p,profile)
  except SampleRejected:
   if parameters is not None:raise
   continue
  m=math_components(spec,p)
  prompt=('What is the range of the function $' if spec['response']=='range' else 'What is the minimum value of $')+spec['out']+'='+m['fun']+'$?'
  return assemble(level,seed,name,profile,p,prompt,normal_solution(spec,p),values)
 raise SampleRejected('Bounded full-instance rejection exhausted')

# EASY: positive integer multiplication and integer translation of [-1,1].
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: negative integer multiplication reverses both inequalities, then shift.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored absent level): negative noninteger rational A and rational D;
# same four inequalities, with exact small-denominator endpoint arithmetic.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q,g=record['question'],record['generation'];lines=['## '+g['template']+' — '+q.get(':question/difficulty','unrated raw'),'',q[':question/problem'],'']
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:lines.append('- $'+a[':answer/value']+'$'+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''))
  if ':answer-field/correct' not in f:lines+=['','*Original correct designation absent; evidence only.*']
 if ':question/answer-fields' not in q:lines+=['*Original fields absent; evidence only.*']
 lines+=['',q.get(':question/worked-solution','*Original worked solution absent.*'),'']
 return '\n'.join(lines)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=('markdown','json'),default='markdown');args=ap.parse_args()
 if args.count<1:ap.error('Positive count required')
 if args.difficulty=='all' and (args.template or args.profile):ap.error('Choose one level for an explicit template/profile')
 try:records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in LEVELS if args.difficulty in (l,'all') for i in range(args.count)]
 except ValueError as e:ap.error(str(e))
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n---\n'.join(map(markdown,records)))
if __name__=='__main__':main()
