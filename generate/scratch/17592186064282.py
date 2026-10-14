#!/usr/bin/env python3
"""Reciprocal trig chain rule, frozen basis 2275, local unregistered generator.
Easy: direct composite derivative. Moderate: derivative of an observed sum, or
slope evaluation. Hard: tangent equation after the same chain rule and evaluation.
Raw profiles are parameterized captured evidence including omissions and errors.
"""
import argparse,copy,hashlib,importlib.util,json,random,re,sys,uuid
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R))
from scripts.question_capture.math_format import normalize_prose,normalize_tex,validate_generated_record
D=Path(__file__).with_suffix('');SOURCE=json.loads((D/'source.json').read_text());REC=SOURCE['record']
KP_ID=17592186064282;KP_UUID=REC[':knowledge-point/id'];TITLE=REC[':knowledge-point/title'];VERSION='1.0.0'
SUPPORTED_LEVELS=('easy','moderate','hard');QUESTIONS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
LEVELS={q[':question/math-academy-id']:q.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1] for q in QUESTIONS.values()}
DEFAULTS={'easy':('q-31333','q-310222','q-31320'),'moderate':('q-31341','q-342405','q-31338','q-31340','q-342402'),'hard':('q-342412','q-48510','q-48512')}
# Each observed source has one complete bank profile; no pooled first-valid options.
TEMPLATES={k:{'difficulty':LEVELS[k],'plot_rating':'none'} for k in QUESTIONS};SUPPORTED_PROFILES=tuple(TEMPLATES)
spc=importlib.util.spec_from_file_location('captured_tex_reader',D/'tex-parser.py');reader=importlib.util.module_from_spec(spc);spc.loader.exec_module(reader)
x,u=reader.x,reader.u
for fn in ('sec','csc','cot','tan'):reader.functions[fn]=lambda arg,fn=fn:getattr(s,fn)(arg,evaluate=False)

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def scalar(t):return reader.scalar(t.replace(r'\dfrac',r'\frac').replace('[','(').replace(']',')').strip('$'))
def tex(e):return s.latex(e).replace(r'\left', '').replace(r'\right','')
def eq(a,b):
 if a==b:return True
 delta=a-b
 if not delta.has(s.sec,s.csc,s.cot,s.tan,s.sin,s.cos):return s.simplify(delta)==0
 subs={};circles=[]
 for i,arg in enumerate(sorted({f.args[0] for f in delta.atoms(s.sec,s.csc,s.cot,s.tan,s.sin,s.cos)},key=str)):
  si,co=s.symbols('_s'+str(i)+' _c'+str(i));circles.append((si,co))
  subs.update({s.sin(arg):si,s.cos(arg):co,s.sec(arg):1/co,s.csc(arg):1/si,s.tan(arg):si/co,s.cot(arg):co/si})
 num=s.cancel(delta.xreplace(subs)).as_numer_denom()[0]
 for si,co in circles:
  try:num=s.rem(num,si**2+co**2-1,si)
  except s.PolynomialError:return False
 return s.expand(num)==0

def clean(v):
 if isinstance(v,list):return [clean(z) for z in v]
 if isinstance(v,dict):
  if ':db/ident' in v:return v[':db/ident']
  return {k:(v[':answer-field/correct'][':answer/value'] if k==':answer-field/correct' else clean(z)) for k,z in v.items() if k not in (':db/id',':question/id',':question/math-academy-id',':answer-field/id',':answer/id')}
 return v

def transform(k,t,a):
 """Complete component substitutions, using a sentinel to prevent cascades.
 Mathematical numeric powers and formal derivative arguments are never generic
 numeric substitution targets. At original a, every raw byte is reproduced.
 """
 
 c=str(a);pre='' if a==1 else c
 if k=='q-31338' and t==r'\frac{\pi }{2}':
  z=s.Rational(2*a+1,2*a+4);return r'\frac{'+('' if z.p==1 else str(z.p))+r'\pi }{'+str(z.q)+'}'
 if k=='q-31338' and t in ('3','-3'):return str((a+2)*(1 if t=='3' else -1))
 if k=='q-31340' and t in ('5','-5'):return str((2*a+3)*(1 if t=='5' else -1))
 mappings=[]
 if k=='q-31330':mappings=[('3\\cot',str(3*a)+r'\cot'),('3\\csc',str(3*a)+r'\csc')]
 elif k=='q-48640':mappings=[('24x',str(24*a)+'x'),('8x',str(8*a)+'x')]
 elif k=='q-31333':mappings=[('80',str(80*a)),('8\\csc',str(8*a)+r'\csc')]
 elif k=='q-310222':mappings=[('2{x}^{3}',str(2*a)+'{x}^{3}'),('6{x}^{2}',str(6*a)+'{x}^{2}')]
 elif k=='q-31320':mappings=[('2x',str(2*a)+'x'),('=2.',f'={2*a}.'),('=2\\operatorname',f'={2*a}'+r'\operatorname'),('=2\\',f'={2*a}'+'\\'),(' 2 ',f' {2*a} '),('-2\\operatorname',f'-{2*a}'+r'\operatorname'),('2\\operatorname',f'{2*a}'+r'\operatorname')]
 elif k=='q-31341':
  d=4+a;mappings=[('\\dfrac{4}{5}',r'\dfrac{'+str(d-1)+'}{'+str(d)+'}'),('\\dfrac 4 5',r'\dfrac '+str(d-1)+' '+str(d)),('\\dfrac{1}{5}',r'\dfrac{1}{'+str(d)+'}'),('\\dfrac 1 5',r'\dfrac 1 '+str(d)),('\\dfrac x 5',r'\dfrac x '+str(d)),('\\dfrac{x}{5}',r'\dfrac{x}{'+str(d)+'}')]
 elif k=='q-342405':mappings=[(r'\sec',pre+r'\sec'),(r'\pi\sqrt{2}',pre+r'\pi\sqrt{2}'),(r'\pi \cdot \sqrt{2}',pre+r'\pi \cdot \sqrt{2}')]
 elif k=='q-342412':
  mappings=[(r'\pi\sqrt{3}+2',pre+r'\pi\sqrt{3}+'+str(2*a)),(r'\pi\sqrt{3} + 2',pre+r'\pi\sqrt{3} + '+str(2*a)),(r'\pi\sqrt{3}',pre+r'\pi\sqrt{3}'),(r'\csc',pre+r'\csc'),('(1,2)',f'(1,{2*a})'),(r'1,2\right',f'1,{2*a}'+r'\right'),('y-2',f'y-{2*a}'),(r'\cdot 2 \cdot',r'\cdot '+str(2*a)+r' \cdot')]
 elif k=='q-48510':mappings=[('-2x',f'-{a+1}x'),('-2 ',f'-{a+1} '),('-2.',f'-{a+1}.'),('-2\n',f'-{a+1}\n'),('- 2',f'- {a+1}'),('-2\\',f'-{a+1}'+'\\')]
 elif k=='q-31338':
  n=2+a;mappings=[('2\\pi',str(n-1)+r'\pi'),('-3x',f'-{n}x'),('=-3.',f'=-{n}.'),('(-3)',f'(-{n})'),('3{csc}',str(n)+'{csc}'),('3\\cdot',str(n)+r'\cdot'),('3\\pi',str(n)+r'\pi'),('=3.',f'={n}.'),('$3.',f'${n}.'),('-3',f'-{n}'),('3',str(n))]
  # Keep phase pi/2 by changing evaluation point and replacing all its occurrences.
  mappings=[('x='+r'\frac{\pi }{2}','x='+r'\frac{'+('' if s.Rational(2*n-3,2*n).p==1 else str(s.Rational(2*n-3,2*n).p))+r'\pi }{'+str(s.Rational(2*n-3,2*n).q)+'}'),('}('+r'\frac{\pi }{2}'+')','}('+r'\frac{'+('' if s.Rational(2*n-3,2*n).p==1 else str(s.Rational(2*n-3,2*n).p))+r'\pi }{'+str(s.Rational(2*n-3,2*n).q)+'})'),(r'2\pi -\frac{3\pi }{2}',str(n-1)+r'\pi -\frac{'+str(2*n-3)+r'\pi }{2}'),('2\\pi',str(n-1)+r'\pi'),('-3x',f'-{n}x'),('=-3.',f'=-{n}.'),('(-3)',f'(-{n})'),('3{csc}',str(n)+'{csc}'),('3\\cdot',str(n)+r'\cdot'),('=3.',f'={n}.'),('$3.',f'${n}.'),('-3',f'-{n}')]
 elif k=='q-31340':
  n=2*a+3;mappings=[('5x',str(n)+'x'),('=5.',f'={n}.'),('(5)',f'({n})'),('-5\\',f'-{n}'+'\\'),('5\\cdot',str(n)+r'\cdot'),('5\\pi',str(n)+r'\pi'),('-5',f'-{n}')]
  # n stays odd: original evaluated csc(-5pi/2)=-1 changes sign for n=7,9.
  sign=(-1)**((n+1)//2);mappings += [('(-1)',f'({sign})')]
 elif k=='q-342402':mappings=[(r'\frac{1}{4}',r'\frac{'+str(a)+'}{4}'),('-{x}^{3}','-'+pre+'{x}^{3}')]
 elif k=='q-48512':
  # vary outer amplitude; phase, point x0, and zero ordinate remain fixed.
  mappings=[(r'\operatorname{cot}',pre+r'\operatorname{cot}'),('-{csc}','-'+pre+'{csc}'),(r'3x-\frac{3\pi }{2}',str(3*a)+r'x-\frac{'+str(3*a)+r'\pi }{2}'),('3x-',str(3*a)+'x-'),('3{csc}',str(3*a)+'{csc}'),('3\\cdot',str(3*a)+r'\cdot'),('=3.',f'={3*a}.'),('=3(',f'={3*a}('),('3(x-',f'{3*a}(x-')]
 # longest complete fragment wins, with no recursive parameter replacement.
 mappings=sorted(mappings,key=lambda z:len(z[0]),reverse=True)
 if not mappings:return t
 pattern='|'.join(re.escape(old) for old,new in mappings)
 table=dict(mappings);return re.sub(pattern,lambda m:table[m[0]],t)

def raw_record(k,a):
 q=clean(QUESTIONS[k])
 def walk(v):
  if isinstance(v,str):return transform(k,v,a)
  if isinstance(v,list):return [walk(z) for z in v]
  if isinstance(v,dict):return {key:walk(z) for key,z in v.items()}
  return v
 return walk(q)

def function(k,a):
 # One exact instance drives formal operators, component derivatives and keys.
 if k=='q-31330':return 3*a*s.cot(x+1),None
 if k=='q-48640':return s.sec(8*a*x**3+1),None
 if k=='q-31333':return 8*a*s.csc(10*x),None
 if k=='q-310222':return s.cot(2*a*x**3),None
 if k=='q-31320':return s.sec(2*a*x-1),None
 if k=='q-31341':return s.cot(1-x/(a+4)),s.Integer(1)
 if k=='q-342405':return a*s.sec(s.pi*x**2),s.Rational(1,2)
 if k=='q-342412':return a*s.csc(s.pi*x**3/6),s.Integer(1)
 if k=='q-48510':return s.sec(3*x)-(a+1)*x,s.Integer(0)
 if k=='q-31338':n=a+2;return s.cot((n-1)*s.pi-n*x,evaluate=False),s.Rational(2*n-3,2*n)*s.pi
 if k=='q-31340':return s.csc((2*a+3)*x),-s.pi/2
 if k=='q-342402':return s.sec(2*x)/2-a*x**4/4,None
 if k=='q-48512':return a*s.cot(2*s.pi-3*x,evaluate=False),s.pi/2
 raise ValueError(k)

def derivative(F):
 term=next(t for t in s.Add.make_args(F) if t.has(s.sec,s.csc,s.cot));trig=next(iter(term.atoms(s.sec,s.csc,s.cot)));arg=trig.args[0];coef=term/trig
 se=s.sec(arg,evaluate=False);ta=s.tan(arg,evaluate=False);cs=s.csc(arg,evaluate=False);co=s.cot(arg,evaluate=False)
 outer={s.sec:se*ta,s.csc:-cs*co,s.cot:-cs**2}[trig.func]
 return coef*outer*s.diff(arg,x)+s.diff(F-term,x)

def normal_solution(k,a):
 text=raw_record(k,a).get(':question/worked-solution')
 if text is None:raise ValueError('raw source has no solution; no invented normal branch')
 if k=='q-31341':text=text.replace("f'(x) & =", "f'(1) & =")
 if k=='q-342412':
  # Captured two rows put cot inside the csc braces; move that boundary.
  text=text.replace(r'\right)\cot{',r'\right)}\cot{').replace(r'\right)}}',r'\right)}')
 # Presentation conversion preserves the complete ordered source rows.
 text=normalize_prose(text).replace(r'\style{font-family:inherit;}{\text{and}}',r'\text{and}')
 text=re.sub(r'\\begin\{eqnarray\}\s*\\eqalign\{(.*?)\}\s*\\end\{eqnarray\}',lambda m:'\n$$\n'+r'\begin{aligned}'+m[1]+r'\end{aligned}'+'\n$$',text,flags=re.S)
 text=re.sub(r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}',lambda m:'\n$$\n'+r'\begin{aligned}'+m[1]+r'\end{aligned}'+'\n$$',text,flags=re.S)
 return normalize_prose(text)

def validate_parameters(k,p,raw=False):
 if set(p)!={'a'} or type(p['a']) is not int or not 1<=p['a']<=9:raise ValueError('integer a in 1..9 required')
 if k=='q-310222' and p['a']==9 and not raw:raise ValueError('learner-eligible cot cubic inner scale bound is a<=8; a9 is raw diagnostics only')
 return dict(p)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 raw=bool(profile and (profile.startswith('raw:') or profile=='observed_raw'));name=(template if profile=='observed_raw' else profile[4:]) if raw else (template or profile or random.Random(seed).choice(DEFAULTS[level]))
 if name not in QUESTIONS or (template and template!=name):raise ValueError('unknown template/profile')
 if level!=LEVELS[name] or (not raw and name not in DEFAULTS.get(level,())):raise ValueError('level/profile mismatch; unrated originals evidence-only')
 if profile and not raw and profile!=name:raise ValueError('unknown profile')
 a=validate_parameters(name,parameters if parameters is not None else {'a':random.Random(seed).randint(1,8 if name=='q-310222' and not raw else 9)},raw)['a'];q=raw_record(name,a);F,x0=function(name,a)
 if not raw:
  q[':question/worked-solution']=normal_solution(name,a)
  if name=='q-342412':
   # Repair the original malformed nested-csc scope only in normal solution.
   pass
  if not q.get(':question/answer-fields'):
   Dvalue=derivative(F);answer=Dvalue if x0 is None else Dvalue.subs(x,x0)
   if level=='hard':answer=s.simplify(answer*x+F.subs(x,x0)-answer*x0)
   q[':question/answer-fields']=[{':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':tex(s.simplify(answer))}],':answer-field/correct':tex(s.simplify(answer))}]
   q[':question/problem']+='\n\n'+('$y =$' if level=='hard' else '$m =$' if x0 is not None else r"$\frac{\mathrm{d}y}{\mathrm{d}x} =$" )+'\n{{field-1}}'
  for key in (':question/problem',':question/worked-solution'):q[key]=normalize_prose(q[key])
  q[':question/difficulty']=':question.difficulty/'+level
  # Correct values are recomputed, not read back from the source answer key.
  ans=derivative(F) if x0 is None else s.simplify(derivative(F).subs(x,x0))
  expected=[ans]
  if level=='hard':
   intercept=s.simplify(F.subs(x,x0)-ans*x0);expected=[ans,intercept] if len(q[':question/answer-fields'])==2 else [ans*x+intercept]
  for f,val in zip(q[':question/answer-fields'],expected):
   for z in f[':answer-field/choices']:z[':answer/type']=':answer.type/math';z[':answer/value']=normalize_tex(z[':answer/value'].strip('$'))
   if f[':answer-field/type'].endswith('/blank') and not QUESTIONS[name].get(':question/answer-fields'):f[':answer-field/choices']=[{':answer/type':':answer.type/math',':answer/value':tex(val)}]
   matches=[z[':answer/value'] for z in f[':answer-field/choices'] if eq(scalar(z[':answer/value'].split('=')[-1]),val)]
   if len(matches)!=1:raise ValueError('complete selected profile has invalid correct/duplicate options')
   f[':answer-field/correct']=matches[0]
   vals=[scalar(z[':answer/value'].split('=')[-1]) for z in f[':answer-field/choices']]
   if any(eq(v,w) for i,v in enumerate(vals) for w in vals[:i]):raise ValueError('complete profile equivalence collision')
  validate_generated_record({'question':q})
 if field_type and any(f[':answer-field/type'].split('/')[-1]!=field_type.split('/')[-1] for f in q.get(':question/answer-fields',[])):raise ValueError('field contract mismatch')
 bare=copy.deepcopy(q)
 for f in bare.get(':question/answer-fields',[]):f[':answer-field/choices']=sorted(f[':answer-field/choices'],key=lambda z:json.dumps(z,sort_keys=True))
 content=digest(bare);qid=uid('question:'+content);q[':question/id']=qid
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  fid=uid(qid+':field:'+str(i));f[':answer-field/id']=fid;cv=f.get(':answer-field/correct')
  for z in f[':answer-field/choices']:z[':answer/id']=uid(fid+':answer:'+digest(z))
  if cv is not None:
   match=[z for z in f[':answer-field/choices'] if z[':answer/value']==cv]
   if len(match)!=1:raise ValueError('correct value ownership')
   f[':answer-field/correct']=[':answer/id',match[0][':answer/id']]
 trig=next(iter(F.atoms(s.sec,s.csc,s.cot)));pole='cos('+str(trig.args[0])+') != 0' if trig.func==s.sec else 'sin('+str(trig.args[0])+') != 0'
 fingerprint=digest([s.srepr(F),s.srepr(x0) if x0 is not None else None,'tangent' if level=='hard' else 'slope' if x0 is not None else 'derivative'])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'seed':seed,'template':name,'bank_profile':profile or name,'parameters':{'a':a},'parameter_fingerprint':fingerprint,'content_fingerprint':content,'domain':'Real x with '+pole+'; point evaluation must be defined.','evidence_only':raw,'eligible_for_learning':not raw,'source_references':[name],'math_format':'course-academy-tex-v1','plot_rating':'none','authored':not raw and not QUESTIONS[name].get(':question/answer-fields'),'solution_provenance':'complete parameterized source prose/steps; two explicit mathematical repairs and canonical presentation only'}}
# Easy: source direct chain rule, no tangent/evaluation added.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: observed evaluation or trig-plus-polynomial sum, same methods.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard: observed tangent slope and intercept after chain rule.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+z[':answer/value']+'$' for f in q.get(':question/answer-fields',[]) for z in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Absent]')
def batch(level,count=1,seed=0,template=None,profile=None):
 if count<1:raise ValueError('positive count required')
 records=[];seen=set()
 for offset in range(1000):
  r=generate(level,seed+offset,template=template,profile=profile);fp=r['generation']['parameter_fingerprint']
  if fp not in seen:records.append(r);seen.add(fp)
  if len(records)==count:return records
 raise ValueError('requested count exceeds bounded distinct mathematical tasks')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'unrated','all'),required=True);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=('json','markdown'),default='json');a=ap.parse_args();rs=[r for l in (SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty]) for r in batch(l,a.count,a.seed,a.template,a.profile)];print(json.dumps(rs,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n'.join(map(markdown,rs)))
if __name__=='__main__':main()
