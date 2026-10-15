#!/usr/bin/env python3
"""Basis-2275 normal-intercept draft. Local replay and bounded same-method variants.
All three levels use derivative, negative reciprocal, point-slope, intercept.
Hard is a conservative sparse-source extension from canonical e-149, no new rule.
Raw replay preserves captures including missing attributes; normal APIs fail closed
for no-field originals. No EDB, registrations, commits, or plot creation.
"""
import sys
sys.dont_write_bytecode=True
import argparse,copy,hashlib,importlib.util,json,random,re,uuid
from pathlib import Path
try:import sympy as s
except ImportError:
 import os
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python';os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
HERE=Path(__file__).with_suffix(''); ROOT=Path(__file__).resolve().parents[2]
SOURCE=json.loads((HERE/'source.json').read_text());KP=SOURCE['record'];KP_ID=17592186092385
VERSION='normal-intercept-draft-2275-2';X=s.Symbol('x',real=True)
fs=importlib.util.spec_from_file_location('math_format',ROOT/'scripts/question_capture/math_format.py');fmt=importlib.util.module_from_spec(fs);fs.loader.exec_module(fmt)
ROWS={q.get(':question/math-academy-id','nonMA-'+str(q[':db/id'])):q for q in KP[':knowledge-point/questions']}
SPECS={
'q-10871':(2*X**2+X,1,'x','easy','poly'),
'q-10878':(X**2,3,'x','easy','poly'),
'q-71542':(3*X**2-4*X+1,2,'y','easy','poly'),
'q-342200':(4-X**2,1,'x','easy','poly'),
'q-342201':(3*X**2-6*X+5,0,'x','easy','poly'),
'q-11124':(2*s.sqrt(X),1,'y','moderate','sqrt'),
'q-104073':(3*X**s.Rational(2,3),8,'y','moderate','cubert'),
'q-104075':(2*X**s.Rational(3,2),1,'x','moderate','sqrtcube'),
'q-342222':(2*X**s.Rational(1,4),1,'x','moderate','fourth'),
'q-308823':(2/X+1,1,'x','moderate','reciprocal'),
'hard-canonical':(2*s.sqrt(X)-4*X,1,'x','hard','sqrtlinear')}
NORMAL_TEMPLATES={'easy':('q-10871','q-342200','q-342201'),'moderate':('q-11124','q-104073','q-104075','q-342222','q-308823'),'hard':('hard-canonical',)}
SUPPORTED_LEVELS=('easy','moderate','hard')
def tex(e):return s.latex(e).replace(r'\left','').replace(r'\right','')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),v))
def content_hash(q):
 fields=[]
 for f in q[':question/answer-fields']:
  ref=f[':answer-field/correct'];cid=ref[':answer/id'] if isinstance(ref,dict) else ref[1];correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)
  fields.append([f[':answer-field/key'],f[':answer-field/type'],[(a[':answer/value'],a.get(':answer/feedback')) for a in f[':answer-field/choices']],correct])
 return digest([VERSION,q[':question/problem'],q[':question/worked-solution'],q[':question/difficulty'],fields])
def domain(t):return 'x>0' if SPECS[t][4] in ('sqrt','cubert','sqrtcube','fourth','sqrtlinear') else 'x!=0' if t=='q-308823' else 'real x'
def data(t,p):
 f0,_,axis0,level,kind=SPECS[t];scale=p.get('scale',1);point=p.get('point',SPECS[t][1]);axis=p.get('axis',axis0)
 if type(scale)!=int or scale not in range(1,9) or type(point)!=int or axis not in ('x','y'):raise ValueError('Invalid bounded parameters')
 allowed=points(t)
 if point not in allowed:raise ValueError('Outside declared point slot')
 f=s.expand(scale*f0);yp=s.simplify(f.subs(X,point));d=s.diff(f,X);m=s.simplify(d.subs(X,point))
 if m==0 or not m.is_finite or not yp.is_real:raise ValueError('Undefined normal or nonreal point')
 n=-1/m;b=s.simplify(yp-n*point);a=s.simplify(-b/n) if axis=='x' else b
 return f,s.Integer(point),yp,d,m,n,b,a,axis

def points(t):
 if t in ('q-11124','q-104075','hard-canonical'):return (1,4,9)
 if t=='q-104073':return (1,8,27)
 if t=='q-342222':return (1,16,81)
 if t=='q-308823':return (1,2,4)
 if t=='q-342201':return (0,2,3)
 if t=='q-10878':return (1,2,3)
 return (1,2,3)
def curve(t,scale):
 k=SPECS[t][4]
 return {'sqrt':str(2*scale)+r'\sqrt{x}','cubert':str(3*scale)+r'\sqrt[3]{x^{2}}','sqrtcube':str(2*scale)+r'\sqrt{x^{3}}','fourth':str(2*scale)+r'\sqrt[4]{x}','reciprocal':r'\frac{'+str(2*scale)+r'}{x}+'+str(scale),'sqrtlinear':str(2*scale)+r'\sqrt{x}-'+str(4*scale)+'x'}.get(k,tex(s.expand(scale*SPECS[t][0])))
def add(a,b):return a+('+' if not str(b).startswith('-') else '')+str(b)
def blocks(t,p):
 f,px,yp,d,m,n,b,a,axis=data(t,p);L=tex;c=curve(t,p['scale']);kind=SPECS[t][4]
 operator=lambda e:r'\frac{\mathrm{d}}{\mathrm{d}x}('+e+')'
 if kind=='poly':first="f'(x)="+operator(c)+'='+L(d)+'.'
 elif kind=='fourth':first="f'(x)="+operator(c)+'='+str(2*p['scale'])+r'\cdot'+operator(r'x^{1/4}')+'='+str(2*p['scale'])+r'\cdot\frac{1}{4}x^{-3/4}='+L(d)+'.'
 else:
  power=s.latex(f,root_notation=False)
  derivative_power=s.latex(d,root_notation=False)
  first="f'(x)="+operator(c)+'='+operator(power)+'='+derivative_power+'='+L(d)+'.'
 first=r'\begin{aligned}'+first+r'\end{aligned}'
 # Keep actual substitution as a displayed operand instead of collapsed slope.
 subst=L(d).replace('x','('+L(px)+')')
 slope="m=f'("+L(px)+')='+subst+'='+L(m)+','
 normal=r"m'=-\frac{1}{m}=-\frac{1}{("+L(m)+')}='+L(n)+'.'
 line1='y-('+L(yp)+')&='+L(n)+'(x-('+L(px)+'))'
 distributed=add(add('y&='+L(n)+'x',L(-n*px)),L(yp))
 simplified=add('y&='+L(n)+'x',L(b))
 rows=[line1,distributed,simplified]
 if t=='q-342201' and px==0:rows=[line1,simplified]
 line=r'\begin{aligned}'+r'\\'.join(rows)+r'.\end{aligned}'
 if axis=='x':
  rows=[add(L(n)+'x',L(b))+'&=0',L(n)+'x&='+L(-b),'x&='+L(a)]
  if t in ('q-10871','q-104075','q-308823'):rows=[rows[0],rows[-1]]
 else:rows=['y&='+add(L(n)+r'\cdot0',L(b)),'y&='+L(a)]
 intercept=r'\begin{aligned}'+r'\\'.join(rows)+r'.\end{aligned}'
 return [first,slope,normal,line,intercept]
def normal_solution(t,p):
 bs=blocks(t,p);axis=p['axis'];a=data(t,p)[7];point='('+tex(a)+',0)' if axis=='x' else '(0,'+tex(a)+')'
 words=['Taking the derivative, we have','So the slope of the tangent line is','and therefore the slope of the normal line is','Finally, the equation of the normal line is','Lastly, we find the point of intersection with the $'+axis+'$-axis by setting $'+('y' if axis=='x' else 'x')+'=0$ and solving the resulting equation. We get']
 return '\n\n'.join(w+'\n\n$$\n'+b+'\n$$' for w,b in zip(words,bs))+'\n\nTherefore, the normal line intersects the $'+axis+'$-axis at $'+point+'.$'
def source_bank(t,d):
 f,p,yp,der,m,n,b,a,axis=d
 if t=='q-10871':return [-p,p,m,a,a/m]
 if t=='q-11124':return [1/m,yp,yp+1/(2*m),1/(2*m),a]
 if t=='q-104073':return [-a,a,-p,yp-p,-(yp-p)]
 if t=='q-104075':return [m,1/a,1/m,p,a]
 return [a]
def authored_bank(d):
 """One complete inferred error profile, derived from lines at the actual point."""
 f,p,y0,der,m,n,b,a,axis=d
 lines=[(n,y0-n*p),(m,y0-m*p),(1/m,y0-p/m),(n,y0),(n,-n*p)]
 return [s.simplify(-intercept/slope) if axis=='x' else s.simplify(intercept) for slope,intercept in lines]
def owned_fields(q,identity):
 for f in q.get(':question/answer-fields',[]):
  ft=f[':answer-field/type'];f[':answer-field/type']=ft[':db/ident'] if isinstance(ft,dict) else ft
  f[':answer-field/id']=uid(identity+':field:'+f[':answer-field/key']);mapping={}
  for a in f.get(':answer-field/choices',[]):
   old=a[':answer/id'];a[':answer/id']=uid(f[':answer-field/id']+':answer:'+a[':answer/value']);mapping[old]=a[':answer/id'];a.pop(':db/id',None)
   at=a[':answer/type'];a[':answer/type']=at[':db/ident'] if isinstance(at,dict) else at
  if ':answer-field/correct' in f:
   old=f[':answer-field/correct'];oid=old[':answer/id'] if isinstance(old,dict) else old[1];f[':answer-field/correct']=[':answer/id',mapping[oid]]
  f.pop(':db/id',None)
def clean_capture(raw):
 q=copy.deepcopy(raw);q.pop(':db/id',None);q.pop(':question/math-academy-id',None)
 if ':question/difficulty' in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 return q

def source_replay(source_id,profile='observed_raw'):
 if source_id not in ROWS:raise ValueError('Unknown captured source')
 raw=ROWS[source_id]
 if profile=='observed_raw':return {'question':copy.deepcopy(raw),'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'generation':{'version':VERSION,'template':source_id,'profile':profile,'parameters':{},'seed':0,'source_basis':2275,'lineage':SOURCE['lineage'],'evidence_only':True,'eligible_for_learning':False,'learner_normalization_applied':False}}
 if profile!='observed_served':raise ValueError('Unknown replay profile')
 if source_id in ('q-10878','q-71542'):raise ValueError('Raw-only source: answer-field contract absent')
 q=clean_capture(raw)
 if source_id=='q-342222':
  for f in q[':question/answer-fields']:
   value='2' if f[':answer-field/key']=='field-1' else '0';aid=uid('repair:'+value);f[':answer-field/choices']=[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value}];f[':answer-field/correct']=[':answer/id',aid]
 return finish(q,source_id,{},0,profile,False)
def finish(q,t,p,seed,profile,eligible=True):
 q=copy.deepcopy(q)
 q[':question/problem']=fmt.normalize_prose(q[':question/problem']);q[':question/worked-solution']=fmt.normalize_prose(q[':question/worked-solution'])
 for f in q.get(':question/answer-fields',[]):
  if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f.get(':answer-field/choices',[]):
   a[':answer/value']=fmt.normalize_tex(a[':answer/value'])
   if isinstance(a[':answer/type'],dict):a[':answer/type']=a[':answer/type'][':db/ident']
 content=content_hash(q)
 q[':question/id']=uid('question:'+content);owned_fields(q,content)
 meta={'version':VERSION,'template':t,'profile':profile,'parameters':copy.deepcopy(p),'seed':seed,'content_hash':content,'source_basis':2275,'lineage':SOURCE['lineage'],'evidence_only':not eligible,'eligible_for_learning':eligible,'learner_normalization_applied':True,'sympy':s.__version__,'source_references':[t if t in ROWS else 'e-149'],'extension_policy':'conservative same derivative/negative-reciprocal/point-slope/intercept method; unordered variants'}
 if p:
  f,px,yp,d,m,n,b,a,axis=data(t,p);meta.update(domain=domain(t),mathematical_fingerprint=digest([s.srepr(f),str(px),axis]),bank_profile=profile)
 out={'question':q,'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'generation':meta};fmt.validate_generated_record(out);return out

def generate(level,seed=0,template=None,parameters=None,profile='authored',field_type='radio'):
 if type(seed) is not int:raise ValueError('Seed must be an integer')
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported level')
 if profile in ('observed_raw','observed_served'):
  if not template or template not in ROWS:raise ValueError('Explicit source required')
  captured=ROWS[template][':question/difficulty'][':db/ident'].split('/')[-1]
  if level!=captured or parameters not in (None,{}):raise ValueError('Captured replay is fixed')
  return source_replay(template,profile)
 if profile not in ('authored','source_bank') or field_type not in ('radio','blank'):raise ValueError('Unsupported profile/field')
 rng=random.Random(seed);t=template or rng.choice(NORMAL_TEMPLATES[level])
 if parameters is None:
  if t not in NORMAL_TEMPLATES[level]:raise ValueError('Unsupported normal template for this level')
  ts=(t,) if template else NORMAL_TEMPLATES[level]
  candidates=[(tt,{'scale':scale,'point':point,'axis':axis}) for tt in ts for scale in range(1,9) for point in (points(tt) if profile=='authored' else (SPECS[tt][1],)) for axis in (('x','y') if profile=='authored' else (SPECS[tt][2],))];rng.shuffle(candidates)
  for tt,pp in candidates:
   try:return generate(level,seed,tt,pp,profile,field_type)
   except ValueError:continue
  raise ValueError('No valid complete bank in declared domain')
 if t not in NORMAL_TEMPLATES[level]:raise ValueError('Unsupported normal template for this level')
 p=parameters or {'scale':rng.randint(1,8),'point':rng.choice(points(t)),'axis':rng.choice(('x','y'))}
 if set(p)!={'scale','point','axis'}:raise ValueError('Complete explicit slot values required')
 d=data(t,p);f,px,yp,der,m,n,b,a,axis=d
 if profile=='source_bank' and (t not in ('q-10871','q-11124','q-104073','q-104075') or axis!=SPECS[t][2] or px!=SPECS[t][1] or field_type!='radio'):raise ValueError('Observed bank fixed-target conditions')
 problem='Find where the normal line to the curve $f(x)='+curve(t,p['scale'])+'$ at the point $('+tex(px)+','+tex(yp)+')$ intersects the $'+axis+'$-axis.'
 q={':question/problem':problem,':question/worked-solution':normal_solution(t,p),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[]}
 point=lambda v:'('+tex(v)+',0)' if axis=='x' else '(0,'+tex(v)+')'
 if field_type=='radio':
  vals=source_bank(t,d) if profile=='source_bank' else authored_bank(d)
  vals=list(map(s.simplify,vals))
  if len(set(vals))!=5 or vals.count(a)!=1:raise ValueError('Ambiguous complete bank')
  cs=[{':answer/id':uid('temporary:'+str(i)),':answer/type':':answer.type/math',':answer/value':point(v)} for i,v in enumerate(vals)]
  q[':question/answer-fields']=[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':cs,':answer-field/correct':[':answer/id',cs[vals.index(a)][':answer/id']]}]
 else:
  q[':question/problem']+='\n\nThe normal line intersects the $'+axis+'$-axis at $(${{field-1}}$,${{field-2}}$).$'
  for key,v in [('field-1',a if axis=='x' else 0),('field-2',0 if axis=='x' else a)]:
   aid=uid('temporary:'+key);q[':question/answer-fields'].append({':answer-field/key':key,':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':tex(v)}],':answer-field/correct':[':answer/id',aid]})
 return finish(q,t,p,seed,profile)
def catalog(level,field_type='radio'):
 if field_type not in ('radio','blank'):raise ValueError('Unsupported field type')
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported level')
 out=[]
 for t in NORMAL_TEMPLATES[level]:
  for scale in range(1,9):
   for point in points(t):
    for axis in ('x','y'):
     p={'scale':scale,'point':point,'axis':axis}
     try:r=generate(level,template=t,parameters=p,field_type=field_type)
     except ValueError:continue
     out.append(r)
 return out
def batch(level,count,seed=0,field_type='radio'):
 if type(count) is not int or count<0:raise ValueError('Count must be a nonnegative integer')
 if type(seed) is not int:raise ValueError('Seed must be an integer')
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported level')
 if field_type not in ('radio','blank'):raise ValueError('Unsupported field type')
 if count==0:return []
 rows=catalog(level,field_type);random.Random(seed).shuffle(rows);seen=set();out=[]
 for r in rows:
  fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:seen.add(fp);r['generation']['seed']=seed;out.append(r)
 if count>len(out):raise ValueError('Requested count exceeds distinct eligible catalog capacity: '+str(len(out)))
 return out[:count]
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\n'+'\n'.join(f[ ':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f.get(':answer-field/choices',[])) for f in q.get(':question/answer-fields',[]))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=5);ap.add_argument('--field-type',choices=['radio','blank'],default='radio');ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args()
 if args.count<0:ap.error('Nonnegative count required')
 levels=SUPPORTED_LEVELS if args.difficulty=='all' else (args.difficulty,)
 try:rs=[r for level in levels for r in batch(level,args.count,args.seed,field_type=args.field_type)]
 except ValueError as exc:ap.error(str(exc))
 print(json.dumps(rs,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,rs)))
