"""Private basis2275 draft. Immutable registered baseline is preserved.
Source profiles replay complete captured mathematical components, never literal anchors.
Default samplers have fixed per-level workloads; source compatibility is explicit.
"""
import argparse, copy, hashlib, importlib.util, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
KP_ID=17592186064281;KP_UUID='73216188-6524-55c3-b945-86d13ef64170';TITLE='Differentiating a Trigonometric Function Using the Chain Rule'
HERE=Path(__file__).with_suffix('');VERSION='2.0.0-draft';GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION));SUPPORTED_LEVELS=('easy','moderate','hard')
_spec=importlib.util.spec_from_file_location('math_format',HERE.parents[2]/'scripts/question_capture/math_format.py');fmt=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(fmt)
SOURCE=json.loads((HERE/'source.json').read_text());SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
x=s.Symbol('x',real=True)
DEFAULTS={'authored-affine-sine':{'A':2,'a':3,'b':-1},'q-1943':{'a':1},'q-1946':{'a':2,'b':2},'q-310179':{'a':3,'b':-5},'q-310180':{'a':3},'q-31153':{'b':5},'q-31163':{'b':11},'q-310182':{'a':1,'b':2},'q-31241':{'b':2,'c':-1},'q-48508':{'a':5},'q-48636':{'a':1},'q-51026':{'A':2}}
LEVELS={'authored-affine-sine':'easy','q-1943':'moderate','q-1946':'easy','q-310179':'moderate','q-310180':'moderate','q-31153':'moderate','q-31163':'moderate','q-310182':'hard','q-31241':'hard','q-48508':'hard','q-48636':'hard','q-51026':'hard'}
DEFAULT_TEMPLATE={'easy':'authored-affine-sine','moderate':'q-310179','hard':'q-310182'}
def tex(e):return s.latex(e).replace(r'\operatorname{sec}',r'\sec').replace(r'\operatorname{csc}',r'\csc').replace(r'\operatorname{cot}',r'\cot')
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def parameters_for(m):
 if m=='authored-affine-sine':return [{'A':A,'a':a,'b':b} for A in range(2,10) for a in range(2,13) for b in range(-12,13) if b]
 if m=='q-1946':return [{'a':a,'b':b} for a in range(2,13) for b in range(1,13)]
 if m=='q-310179':return [{'a':a,'b':b} for a in range(1,25) for b in range(-20,21) if abs(a+b)<=16]
 if m=='q-310182':return [{'a':a,'b':b} for a in range(1,25) for b in range(1,25)]
 if m=='q-31241':return [{'b':b,'c':c} for b in range(1,25) for c in range(-16,0)]
 key=next(iter(DEFAULTS[m]));return [{key:v} for v in range(1,41) if m!='q-31153' or v!=3]
def model(m,p):
 a=p.get('a');b=p.get('b');A=p.get('A');c=p.get('c');at=None
 if m=='authored-affine-sine':u=a*x+b;f=A*s.sin(u)
 elif m=='q-1943':u=a*x**2;f=s.cos(u)
 elif m=='q-1946':u=a*x+b;f=s.tan(u)
 elif m=='q-310179':u=a*x**4+b;f=s.tan(u)
 elif m=='q-310180':u=a*x;f=s.sin(u);at=s.pi/(2*a)
 elif m=='q-31153':u=3*x+b;f=s.sin(u);at=s.Integer(2)
 elif m=='q-31163':u=b-2*x;f=s.cos(u)-6*x**3
 elif m=='q-310182':u=s.pi*(a*x**2+b*x-2);f=s.sin(u);at=s.Integer(1)
 elif m=='q-31241':u=x**2+b*x+c;f=s.sin(u);at=s.Integer(0)
 elif m=='q-48508':u=a*x-2;f=s.cos(u);at=s.Rational(2,a)
 elif m=='q-48636':u=a*x**3;f=s.cos(u);at=s.Integer(0)
 elif m=='q-51026':u=x-1;f=A*s.cos(u);at=1+s.pi
 else:raise ValueError(m)
 derivative=s.diff(f,x);ans=derivative if at is None else s.simplify(derivative.subs(x,at))
 tangent=m in ('q-48508','q-48636','q-51026')
 if tangent:ans=s.expand(ans*(x-at)+f.subs(x,at))
 return f,u,at,derivative,ans,tangent

def mask(t,pairs):
 # Every mask is a complete mathematical component or a formal factor operand.
 pairs=[(a,b) for a,b in pairs if a!=b];pairs=sorted(pairs,key=lambda z:-len(z[0]))
 if not pairs:return t
 mapping=dict(pairs);return re.sub('|'.join(re.escape(a) for a in mapping),lambda m:mapping[m[0]],t)
def coefficient(n):return '' if n==1 else str(n)
def transform(t,m,p):
 a=p.get('a');b=p.get('b');A=p.get('A');c=p.get('c')
 if m=='q-1943':pairs=[('x^{2}',coefficient(a)+'x^{2}'),('2x',str(2*a)+'x')]
 elif m=='q-1946':pairs=[('2x + 2',str(a)+'x + '+str(b)),('2\\csc',str(a)+r'\csc'),('2\\cot',str(a)+r'\cot'),('2\\sec',str(a)+r'\sec')]
 elif m=='q-310179':pairs=[('3{x}^{4}-5',str(a)+r'{x}^{4}'+(str(b) if b<0 else '+'+str(b))),('12{x}^{3}',str(4*a)+r'{x}^{3}')]
 elif m=='q-310180':pairs=[(r'\frac{\pi }{6}',r'\frac{\pi }{'+str(2*a)+'}'),('3x',str(a)+'x'),('=3.','='+str(a)+'.'),(r'\cdot 3',r'\cdot '+str(a)),(r'3\operatorname{cos}',str(a)+r'\operatorname{cos}'),('3\\cdot',str(a)+r'\cdot')]
 elif m=='q-31153':pairs=[('3x+5','3x+'+str(b)),('3\\cdot 2+5','3\\cdot 2+'+str(b)),('cos}⁡11','cos}⁡'+str(6+b)),('5\\operatorname',str(b)+r'\operatorname')]
 elif m=='q-31163':pairs=[('11-2x',str(b)+'-2x')]
 elif m=='q-310182':
  q=coefficient(a)+'x^{2} + '+str(b)+'x - 2';compact=coefficient(a)+'x^{2} +'+str(b)+'x - 2';d=str(2*a)+'x + '+str(b);dc=str(2*a)+'x+'+str(b);k=2*a+b;phase=a+b-2;ans=('-' if phase%2 else '')+str(k)+r'\pi'
  pairs=[('x^{2} + 2x - 2',q),('x^{2} +2x - 2',compact),('2x + 2',d),('2x+2',dc),('2\\cdot1+2',str(2*a)+r'\cdot1+'+str(b)),('1^{2} +2\\cdot1 - 2',('' if a==1 else str(a)+r'\cdot')+r'1^{2} +'+str(b)+r'\cdot1 - 2'),('4\\pi \\cos(\\pi)',str(k)+r'\pi \cos('+coefficient(phase)+r'\pi'+')'),('4\\pi \\cdot (-1)',str(k)+r'\pi \cdot ('+str((-1)**phase)+')'),('-4\\pi',ans)]
 elif m=='q-31241':pairs=[('{x}^{2}+2x-1',r'{x}^{2}+'+str(b)+'x'+str(c)),('2x+2','2x+'+str(b)),('2\\cdot 0+2','2\\cdot 0+'+str(b)),('{0}^{2}+2\\cdot 0-1',r'{0}^{2}+'+str(b)+r'\cdot 0'+str(c)),('2\\operatorname{cos}(-1)',str(b)+r'\operatorname{cos}('+str(c)+')'),('2\\operatorname{cos}1',str(b)+r'\operatorname{cos}'+str(abs(c)))]
 elif m=='q-48508':pairs=[('5x-2',str(a)+'x-2'),(r'\dfrac 2 5',r'\dfrac 2 '+str(a) if a<10 else r'\dfrac{2}{'+str(a)+'}'),(r'\dfrac 25',r'\dfrac 2'+str(a) if a<10 else r'\dfrac{2}{'+str(a)+'}'),(r'\dfrac{2}{5}',r'\dfrac{2}{'+str(a)+'}'),('= 5.','= '+str(a)+'.'),('\\cdot 5',r'\cdot '+str(a)),('-5\\sin','-'+str(a)+r'\sin'),('- 5 \\sin','- '+str(a)+r' \sin'),('5\\cdot',str(a)+r'\cdot')]
 elif m=='q-48636':pairs=[('x^3',coefficient(a)+'x^3'),('3x^2',str(3*a)+'x^2'),('3(0)^2',str(3*a)+'(0)^2'),('0^3',('' if a==1 else str(a)+r'\cdot')+'0^3')]
 elif m=='q-51026':pairs=[('y=x-\\pi -3','y=x-\\pi -'+str(A+1)),('y=x+\\pi -2','y=x+\\pi -'+str(A)),('y=-2x+2\\pi ','y=-'+str(A)+'x+'+str(A)+r'\pi '),('y=-2','y=-'+str(A)),('2\\operatorname',str(A)+r'\operatorname'),(',-2',',-'+str(A)),('y-(-2)','y-(-'+str(A)+')'),('y+2','y+'+str(A)),('y & =-2','y & =-'+str(A))]
 else:raise ValueError(m)
 return mask(t,pairs)

def bank(m,p):
 f,u,at,D,ans,tangent=model(m,p);a=p.get('a');b=p.get('b');A=p.get('A')
 if m=='authored-affine-sine':vals=[ans,A*s.cos(u),-ans,A*a*s.sin(u),A*a*s.cos(a*x-b)];ci=0
 elif m=='q-1943':vals=[x*s.sin(2*a*x),-x*s.sin(u),ans,a*x**2*s.sin(2*a*x),a*x**2*s.cos(u)];ci=2
 elif m=='q-310179':vals=[4*a*x**3*s.sec(u)**2];ci=0
 elif m=='q-1946':vals=[a*s.csc(u)**2,a*s.cot(u),a*s.sec(u)**2,a*s.sec(u),s.sec(u)**2];ci=2
 elif m=='q-31153':vals=[ans,-ans,b*s.cos(2),b*s.cos(6+b),-b*s.cos(6+b)];ci=0
 elif m=='q-31163':vals=[-2*s.sin(u)-9*x**2,-s.cos(u)-9*x**2,s.sin(u)-18*x**2,2*s.cos(u)-18*x**2,ans];ci=4
 elif m=='q-51026':vals=[x-s.pi-(A+1),x+s.pi-A,ans,-A*x+A*s.pi,s.Integer(0)];ci=2
 else:vals=[ans];ci=0
 # Selected full bank; exact trig expansion plus numeric witnesses avoids costly identities.
 for i,v in enumerate(vals):
  for w in vals[:i]:
   delta=v-w
   if all(s.simplify(delta.subs(x,z))==0 for z in (0,1,2)) and s.simplify(s.expand_trig(delta))==0:raise ValueError('Complete bank collision')
 return vals,ci

def authored_solution(m,p):
 f,u,at,D,ans,tangent=model(m,p)
 if m=='authored-affine-sine':outer=p['A']*s.sin(s.Symbol('u'));name='f'
 else:outer=s.cos(s.Symbol('u')) if m=='q-1943' else s.tan(s.Symbol('u'));name='f'
 od=s.sec(s.Symbol('u'))**2 if m=='q-1946' else s.diff(outer,s.Symbol('u'));innerd=s.diff(u,x);chained=od*innerd;substituted=chained.subs(s.Symbol('u'),u)
 return ('First, we express $f(x)$ as a composite function\n\n$$\n'+f'f={tex(outer)}, \\qquad u={tex(u)}.'+'\n$$\n\nDifferentiating gives\n\n$$\n'+r'\frac{\mathrm{d}f}{\mathrm{d}u}='+tex(od)+r',\qquad \frac{\mathrm{d}u}{\mathrm{d}x}='+tex(innerd)+'.\n$$\n\nWe now apply the chain rule, and get\n\n$$\n'+r'\begin{aligned}\frac{\mathrm{d}f}{\mathrm{d}x}&=\frac{\mathrm{d}f}{\mathrm{d}u}\cdot\frac{\mathrm{d}u}{\mathrm{d}x}\\&=('+tex(od)+r')\cdot('+tex(innerd)+r')\\&='+tex(chained)+r'\\&='+tex(substituted)+r'.\end{aligned}'+'\n$$')

def normalized_prose(t):
 t=re.sub(r'\\\\\[[0-9]+pt\]',lambda _:r'\\',t)
 t=re.sub(r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}',lambda m:'\n$$\n'+r'\begin{aligned}'+m[1]+r'\end{aligned}'+'\n$$\n',t,flags=re.S)
 t=t.replace(r'\style{font-family:inherit;}{\text{and}}',r'\text{and}')
 t=re.sub(r'\\begin\{eqnarray\}(.*?)\\end\{eqnarray\}',lambda m:'\n$$\n'+m[1]+'\n$$\n',t,flags=re.S)
 return fmt.normalize_prose(t)

def _generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unknown difficulty')
 rng=random.Random(seed);m=template or DEFAULT_TEMPLATE[level]
 if profile and profile.startswith('raw-'):m=profile[4:];profile='observed_raw'
 raw=profile=='observed_raw'
 if m not in LEVELS or LEVELS[m]!=level:raise ValueError('Template/difficulty mismatch')
 if profile not in (None,'default','source-bank','authored-bank','observed_raw'):raise ValueError('Unknown bank profile')
 if raw and m not in SOURCES:raise ValueError('Authored template has no raw source')
 p=copy.deepcopy(parameters) if parameters is not None else rng.choice(parameters_for(m))
 if p not in parameters_for(m) or any(type(v)!=int for v in p.values()):raise ValueError('Invalid parameter bounds')
 f,u,at,D,ans,tangent=model(m,p);vals,ci=bank(m,p)
 if m in SOURCES:
  src=SOURCES[m];prompt=transform(src[':question/problem'],m,p);worked=transform(src.get(':question/worked-solution',''),m,p)
  sf=src.get(':question/answer-fields',[None])[0]
 else:src={};sf=None;prompt=rf'Calculate $f^{{\prime}}(x)$ if $f(x)={tex(f)}.$';worked=authored_solution(m,p)
 if raw:
  q={':question/problem':prompt}
  if ':question/worked-solution' in src:q[':question/worked-solution']=worked
  if ':question/difficulty' in src:q[':question/difficulty']=src[':question/difficulty'][':db/ident']
  fields=[]
  if sf:
   values=[transform(a[':answer/value'],m,p) for a in sf[':answer-field/choices']];key=sf[':answer-field/key'];ft=sf[':answer-field/type'][':db/ident'];correct=next((i for i,a in enumerate(sf[':answer-field/choices']) if a[':answer/id']==sf.get(':answer-field/correct',{}).get(':answer/id')),None)
   types=[a[':answer/type'][':db/ident'] for a in sf[':answer-field/choices']]
  else:values=[];key='field-1';ft=':answer-field.type/blank';correct=None;types=[]
 else:
  q={':question/problem':normalized_prose(prompt),':question/worked-solution':normalized_prose(worked or authored_solution(m,p)),':question/difficulty':':question.difficulty/'+level}
  key=sf[':answer-field/key'] if sf else 'selection' if m=='authored-affine-sine' else 'field-1';ft=sf[':answer-field/type'][':db/ident'] if sf else ':answer-field.type/radio' if m=='authored-affine-sine' else ':answer-field.type/blank'
  values=[('y=' if tangent and sf else '')+tex(v) for v in vals];values=[fmt.normalize_tex(v) for v in values];correct=ci;types=[':answer.type/math']*len(values)
  q[':question/problem']=q[':question/problem'].replace('{sec}',r'\sec');q[':question/worked-solution']=q[':question/worked-solution'].replace('{sec}',r'\sec')
  if sf is None and ft.endswith('/blank') and '{{'+key+'}}' not in q[':question/problem']:q[':question/problem']+=('\n\n$y=$\n' if tangent else '\n\n')+'{{'+key+'}}'
 if field_type is not None and field_type not in (ft,ft.split('/')[-1]):raise ValueError('Field contract cannot change')
 # Content identity excludes seed and option order, includes response contract and complete selected bank.
 fp=digest({'function':s.srepr(f),'at':s.srepr(at),'response':'tangent' if tangent else 'slope' if at is not None else 'derivative','key':key,'field':ft,'bank':sorted(zip(types,values)),'has_field':bool(sf) or not raw,'raw':raw,'actual_prompt':q[':question/problem'],'actual_solution':q.get(':question/worked-solution'),'correct_value':values[correct] if correct is not None else None})
 qid=str(uuid.uuid5(uuid.UUID(KP_UUID),fp));q[':question/id']=qid
 if (not raw) or sf:
  fid=str(uuid.uuid5(uuid.UUID(qid),key));choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':typ,':answer/value':v} for v,typ in zip(values,types)]
  field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':ft,':answer-field/choices':choices}
  if correct is not None:field[':answer-field/correct']=[':answer/id',choices[correct][':answer/id']]
  q[':question/answer-fields']=[field]
 domain='real x' if m not in ('q-1946','q-310179') else 'real x with cos('+tex(u)+') != 0'
 result={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'source_lineage':SOURCE['lineage'],'seed':seed,'template':m,'profile':'observed_raw' if raw else 'authored-bank' if m=='authored-affine-sine' else 'source-bank','parameters':p,'parameter_fingerprint':fp,'source_ids':[m] if m in SOURCES else [],'source_basis':2275,'domain':domain,'sympy_version':s.__version__,'default_sampler':m==DEFAULT_TEMPLATE[level],'evidence_only':raw,'eligible_for_learning':not raw,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}
 return result

_checked_generate=fmt.checked_math_content(_generate)
def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
 evidence_only=profile=='observed_raw' or bool(profile and profile.startswith('raw-'))
 return (_generate if evidence_only else _checked_generate)(level,seed,template,parameters,profile,field_type)

def batch(level,count,seed):
 records=[]
 for l in (SUPPORTED_LEVELS if level=='all' else (level,)):
  m=DEFAULT_TEMPLATE[l];params=parameters_for(m);random.Random(seed).shuffle(params)
  if count>len(params):raise ValueError('Count exceeds meaningful default task pool')
  records.extend(generate(l,seed+i,parameters=p) for i,p in enumerate(params[:count]))
 return records
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');a=ap.parse_args();rs=batch(a.difficulty,a.count,a.seed)
 print(json.dumps(rs,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'].get(':question/worked-solution','') for r in rs))
