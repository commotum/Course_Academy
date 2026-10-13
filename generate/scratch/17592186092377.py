#!/usr/bin/env python3
"""Finding parametric arc lengths, math basis 1356; local review only.

All 18 observed prompt/solution structures are compiled into endpoint-parameter
recipes, preserving derivative and speed simplification stages and prose. The
coordinate families stay fixed; uniform positive scales, integral endpoints,
and every evaluation stage are computed. This yields hundreds of distinct assessed intervals within the source
level boundaries. No database writes or engine edits. Explicit observed scalar
banks replay through documented homogeneous expression profiles; their error
intent is unresolved, so defaults use complete authored operation banks.
"""
from __future__ import annotations
import argparse,hashlib,json,math,random,re,subprocess,uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
KP_ID=17592186092377
HERE=Path(__file__).with_suffix('')
VERSION='arc-length-endpoint-v2'
SOURCE=json.loads((HERE/'source.json').read_text())
KP=SOURCE['record'];TITLE=KP[':knowledge-point/title'];KP_UUID=KP[':knowledge-point/id']
T=sp.symbols('t',real=True);PI=sp.pi

def group(text,start):
 assert text[start]=='{'
 depth=1;i=start+1
 while depth:
  if text[i]=='{':depth+=1
  if text[i]=='}':depth-=1
  i+=1
 return text[start+1:i-1],i

def parse_tex(text):
 """Small independent TeX subset parser for source stages and scalar options."""
 text=text.strip().rstrip('.,')
 text=text.replace('⁡','').replace('\\,','').replace('\\!','').replace('\\cdot','*').replace('\\left','').replace('\\right','')
 text=re.sub(r'\\operatorname\{(sin|cos)\}',r'\1',text)
 text=text.replace('{sin}','sin').replace('{cos}','cos').replace('{e}','e')
 text=text.replace('\\sin','sin').replace('\\cos','cos').replace('\\pi','pi')
 for command in ('frac','dfrac','sqrt'):
  while '\\'+command in text:
   start=text.index('\\'+command);pos=start+len(command)+1
   a,end=group(text,pos)
   if command!='sqrt':b,end=group(text,end);value='(('+str(parse_tex(a))+')/('+str(parse_tex(b))+'))'
   else:value='sqrt('+str(parse_tex(a))+')'
   text=text[:start]+value+text[end:]
 # Trig powers in source shorthand: sin^{2}(...) / sin^{2}t.
 text=re.sub(r'(sin|cos)\^\{(\d+)\}t',r'\1(t)^\2',text)
 text=re.sub(r'(sin|cos)t',r'\1(t)',text)
 while True:
  m=re.search(r'(sin|cos)\^\{(\d+)\}\(',text)
  if not m:break
  start=m.end()-1;depth=1;end=start+1
  while depth:
   if text[end]=='(':depth+=1
   if text[end]==')':depth-=1
   end+=1
  text=text[:m.start()]+m.group(1)+'('+text[start+1:end-1]+')^'+m.group(2)+text[end:]
 text=text.replace('{','(').replace('}',')').replace('|','')
 text=re.sub(r'([0-9a-z)])(sin|cos|sqrt)\(',r'\1*\2(',text)
 text=re.sub(r'(sin|cos)0',r'\1(0)',text)
 text=re.sub(r'(sin|cos)pi',r'\1(pi)',text)
 return parse_expr(text,local_dict={'t':T,'pi':PI,'e':sp.E,'sin':sp.sin,'cos':sp.cos,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,convert_xor),evaluate=True)

def tex(value):return sp.latex(sp.simplify(value)).replace('e^{','{e}^{')
def equivalent(a,b):return sp.simplify(sp.trigsimp(a-b))==0

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'kp:'+str(KP_ID)+':'+v))

# EASY: constant speed, nonnegative linear speed, and an elementary power rule.
# MODERATE: cubic trig factoring, exponential product derivatives, and radical
# power integration. HARD: trig differences and half-angle speed simplification.
# Entries are source IDs, x(t), y(t), source lower/upper, positive speed, family.
SPECS={
'q-10255':(T-sp.sin(T),1-sp.cos(T),0,PI,2*sp.sin(T/2),'cycloid'),
'q-10260':(1+3*T,2*T**sp.Rational(3,2),0,1,3*sp.sqrt(1+T),'power'),
'q-10256':(sp.sin(T)**3,sp.cos(T)**3,0,PI/2,3*sp.sin(T)*sp.cos(T),'astroid'),
'q-10257':(2*sp.cos(T)**3,2*sp.sin(T)**3,0,PI/2,6*sp.sin(T)*sp.cos(T),'astroid'),
'q-10258':(2*(sp.sin(T)-T*sp.cos(T)),2*(sp.cos(T)+T*sp.sin(T)),0,PI,2*T,'involute'),
'q-10261':(2*sp.cos(T)-sp.cos(2*T),2*sp.sin(T)-sp.sin(2*T),0,PI,4*sp.sin(T/2),'epicycle'),
'q-20907':(4*sp.sin(T)+5,4*(sp.cos(T)+1),0,PI/2,sp.Integer(4),'circle'),
'q-348086':(sp.sin(T)-T*sp.cos(T),-sp.cos(T)-T*sp.sin(T),0,PI,T,'involute'),
'q-348088':(sp.cos(T)+T*sp.sin(T),sp.sin(T)-T*sp.cos(T),0,2*PI,T,'involute'),
'q-351427':(3*sp.sin(T)+2,3*sp.cos(T)-4,0,PI/3,sp.Integer(3),'circle'),
'q-351428':(5*sp.sin(T)-3,5*sp.cos(T)+1,PI/5,PI/2,sp.Integer(5),'circle'),
'q-351429':(T**2/2,(2*T+1)**sp.Rational(3,2)/3,0,2,T+1,'linear'),
'q-351438':(sp.exp(2*T)*sp.cos(T),sp.exp(2*T)*sp.sin(T),0,PI/2,sp.sqrt(5)*sp.exp(2*T),'spiral'),
'q-351439':(4*sp.cos(T)**3,4*sp.sin(T)**3,0,PI/4,12*sp.sin(T)*sp.cos(T),'astroid'),
'q-351471':(3*sp.cos(T)-sp.cos(3*T),3*sp.sin(T)-sp.sin(3*T),0,PI,6*sp.sin(T),'epicycle3'),
'q-351474':((6*T+1)**sp.Rational(3,2)/9,3*T**2/2,0,1,3*T+1,'linear'),
'q-351505':(T-T**3/3,T**2,0,3,1+T**2,'polynomial'),
'q-351508':(2+4*T,8*T**sp.Rational(3,2)/3,0,2,4*sp.sqrt(1+T),'power'),
}
TEMPLATES={}
for q in KP[':knowledge-point/questions']:
 key=q[':question/math-academy-id'];x,y,a,b,s,family=SPECS[key];x,y,a,b,s=map(sp.sympify,(x,y,a,b,s))
 TEMPLATES[key]={'source':q,'level':q[':question/difficulty'][':db/ident'].split('/')[-1],'kind':q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1], 'x':x,'y':y,'a':a,'b':b,'speed':s,'family':family,'primitive':sp.integrate(s,T),'squared_primitive':sp.integrate(sp.expand_trig(s**2),T)}

def data(key,u,scale=1):
 d=TEMPLATES[key];scale=sp.sympify(scale);d={**d,**{k:scale*d[k] for k in ('x','y','speed','primitive')},'squared_primitive':scale**2*d['squared_primitive']};a=d['a'];F=d['primitive'];L=sp.simplify(F.subs(T,u)-F.subs(T,a))
 return {**d,'u':u,'scale':scale,'length':L,'dx':sp.diff(d['x'],T),'dy':sp.diff(d['y'],T),'squared_speed':sp.expand(sp.diff(d['x'],T)**2+sp.diff(d['y'],T)**2)}

def evaluation_rows(key,d):
 u=d['u'];L=d['length'];a=d['a'];ut=tex(u);lt=tex(L)
 # Every endpoint substitution and simplified final value is recomputed.
 if key in ('q-10255','q-10261','q-351471'):
  c=4 if key=='q-10255' else 8 if key=='q-10261' else 6;arg=u if key=='q-351471' else u/2
  return [rf'-{c}(\operatorname{{cos}}⁡({tex(arg)})-\operatorname{{cos}}⁡0)',rf'-{c}({tex(sp.cos(arg))}-1)',lt]
 if key in ('q-10256','q-10257'):
  c=sp.Rational(3,4) if key=='q-10256' else sp.Rational(3,2)
  return [rf'-{tex(c)}(\operatorname{{cos}}⁡({tex(2*u)})-\operatorname{{cos}}⁡0)',rf'-{tex(c)}({tex(sp.cos(2*u))}-1)',lt]
 if key=='q-10260':return [rf'2\sqrt{{{tex((1+u)**3)}}}-2',lt]
 if key=='q-10258':return [rf'2(\frac{{({ut})^{{2}}}}{{2}}-0)',lt]
 if key in ('q-348086','q-348088'):return [rf'\frac{{({ut})^{{2}}}}{{2}}-0',lt]
 if key in ('q-20907','q-351427'):return [rf'{tex(d["speed"])}({ut}-0)',lt]
 if key=='q-351428':return [rf'5({ut}-{tex(a)})',rf'5({tex(u-a)})',lt]
 if key=='q-351429':return [rf'(\frac{{{tex(u**2)}}}{{2}}+{ut})-0',lt]
 if key=='q-351474':return [rf'(\frac{{{tex(3*u**2)}}}{{2}}+{ut})-0',lt]
 if key=='q-351505':return [rf'({ut}+\frac{{{tex(u**3)}}}{{3}})-0',lt]
 if key=='q-351438':return [rf'\frac{{\sqrt{{5}}}}{{2}}({{e}}^{{{tex(2*u)}}}-1)']
 if key=='q-351439':return [rf'-3\operatorname{{cos}}⁡({tex(2*u)})+3\operatorname{{cos}}⁡0',lt]
 if key=='q-351508':return [rf'\frac{{8}}{{3}}(({tex(1+u)})^{{3/2}}-1^{{3/2}})',rf'\frac{{8}}{{3}}({tex((1+u)**sp.Rational(3,2))}-1)',lt]
 raise ValueError(key)

def render_solution(key,d):
 """Compile all original stages; substitute endpoint and evaluation slots."""
 raw=d['source'][':question/worked-solution']
 # Only a source punctuation typo is repaired, with raw evidence retained.
 if key=='q-20907':raw=raw.replace(r'4\operatorname{sin}⁡t+5))',r'4\operatorname{sin}⁡t+5)')
 blocks=list(re.finditer(r'\$\$\n(.*?)\n\$\$',raw,re.S));last=blocks[-1];block=last.group(1)
 marker=r' \\  & =';parts=block.split(marker)
 # Rows after the antiderivative's evaluation bar are the endpoint slots.
 idx=next(i for i,row in enumerate(parts) if '{|}' in row or '|}' in row)
 rows=evaluation_rows(key,d)
 assert len(parts)-idx-1==len(rows),(key,len(parts)-idx-1,len(rows))
 parts=parts[:idx+1]+rows
 block=marker.join(parts)+r'.\end{aligned}'
 raw=raw[:last.start(1)]+block+raw[last.end(1):]
 a,b=d['a'],d['b']
 # Captured integral notation uses pi /n rather than nested fractions.
 olda='0' if a==0 else r'\pi /5';oldb={'pi':r'\pi ','pi/2':r'\pi /2','pi/3':r'\pi /3','pi/4':r'\pi /4','2*pi':r'2\pi '}.get(str(b),str(b))
 old='_{'+olda+'}^{'+oldb+'}'
 raw=raw.replace(old,'_{'+tex(a)+'}^{'+tex(d['u'])+'}')
 return raw

def scale_solution(raw,scale):
 """Uniform coordinate dilation; preserve every original equation stage.

At scale one this wrapper has no effect. Derivative RHS stages are multiplied
by scale; substituted integral radicands by scale squared; antiderivatives and
endpoint evaluations by scale. The universal formula and trig identities stay
unchanged. No wrong-choice feedback is added.
 """
 if scale==1:return raw
 blocks=list(re.finditer(r'\$\$\n(.*?)\n\$\$',raw,re.S));edits=[]
 for index,m in enumerate(blocks):
  block=m.group(1)
  if index==0:continue
  if index in (1,2):
   # Scale the coordinate inside the printed differential, then every
   # evaluated derivative stage. Original product/chain-rule steps remain.
   op=r'\frac{\text{d}}{\text{d}t}('
   pos=block.index(op)+len(op);depth=1;end=pos
   while depth:
    if block[end]=='(':depth+=1
    if block[end]==')':depth-=1
    end+=1
   block=block[:pos]+tex(scale)+r'\left('+block[pos:end-1]+r'\right)'+block[end-1:]
   chunks=block.split('=')
   for i in range(2,len(chunks)):
    chunk=chunks[i];cut=chunk.find(r'\\')
    if cut<0:cut=chunk.find(r'\end{aligned}')
    value=chunk[:cut].strip();punct=''
    if value[-1:] in ',.':punct=value[-1];value=value[:-1]
    chunks[i]=''+tex(scale)+r'\left('+value+r'\right)'+punct+' '+chunk[cut:]
   block='='.join(chunks)
  elif r'\int' in block:
   chunks=block.split('=')
   for i,chunk in enumerate(chunks):
    if r'\frac{\text{d}' in chunk:continue
    if r'{\int }_' in chunk:
     # Rows whose radicals contain the source derivative sums are scaled
     # inside the radical. Reduced scalar-root rows can be scaled outside.
     if r'\sqrt{' in chunk:
      pos=chunk.index(r'\sqrt{')+5;rad,end=group(chunk,pos)
      chunk=chunk[:pos]+'{'+tex(scale**2)+r'\left('+rad+r'\right)}'+chunk[end:]
     else:
      pos=chunk.index(r'{\int }_');prefix=chunk[:pos];chunk=prefix+(r'\cdot ' if prefix.strip() else '')+tex(scale)+r'\cdot '+chunk[pos:]
    elif i>0:
     # Antiderivative and numeric evaluation rows have no integral.
     cut=chunk.find(r'\\')
     if cut<0:cut=chunk.find(r'\end{aligned}')
     value=chunk[:cut].strip();punct=''
     if value[-1:] in ',.':punct=value[-1];value=value[:-1]
     # Keep the evaluation bar outside the scale wrapper.
     marker='{|}' if '{|}' in value else '|}' if '|}' in value else None
     if marker:
      before,after=value.split(marker,1)
      if marker=='|}' and before.count('{')>before.count('}'):before+='}'*(before.count('{')-before.count('}'))
      value=tex(scale)+r'\left('+before+r'\right){|}'+after
     else:value=tex(scale)+r'\left('+value+r'\right)'
     chunk=value+punct+' '+chunk[cut:]
    chunks[i]=chunk
   block='='.join(chunks)
  edits.append((m.start(1),m.end(1),block))
 for start,end,value in reversed(edits):raw=raw[:start]+value+raw[end:]
 return raw

def sample_endpoint(key,rng):
 d=TEMPLATES[key];family=d['family'];a=d['a']
 # Closed finite menus keep exact radicals/trig endpoints and no new branches.
 if family=='astroid':pool=[PI*q for q in map(sp.Rational,('1/12','1/8','1/6','1/4','1/3','3/8','5/12','1/2'))]
 elif family in ('cycloid','epicycle'):pool=[PI*q for q in map(sp.Rational,('1/3','1/2','2/3','1'))]
 elif family=='epicycle3':pool=[PI*q for q in map(sp.Rational,('1/6','1/4','1/3','1/2','2/3','3/4','5/6','1'))]
 elif family=='circle':pool=[a+PI*sp.Rational(n,24) for n in range(1,25)]
 elif family=='spiral':pool=[PI*sp.Rational(n,12) for n in range(1,7)]
 elif family=='involute':pool=[PI*sp.Rational(n,12) for n in range(1,25)]
 else:pool=[sp.Integer(n) for n in range(1,5)]
 return rng.choice(pool)

def check_endpoint(d):
 u=d['u'];a=d['a'];family=d['family']
 if not u.is_real or u<=a:raise ValueError('Require real upper endpoint greater than lower endpoint')
 limit=PI/2 if family=='astroid' else PI if family in ('epicycle3','cycloid','epicycle') else 2*PI if family in ('circle','involute') else PI/2 if family=='spiral' else 4
 if u>limit:raise ValueError('Endpoint exceeds the source family sign/scope domain')


def bank(key,d,profile):
 L=d['length'];q=d['source'];correct=q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
 if d['kind']=='blank' and profile not in ('blank','observed'):raise ValueError('Unknown blank profile')
 if d['kind']=='blank':return [('correct',sp.exp(2*d['u'])-1 if key=='q-351438' else L)]
 if profile=='observed':
  # Underdetermined scalar patterns: explicit replay only. Normalize complete
  # source expression shapes by the independently computed original length.
  L0=data(key,d['b'])['length'];result=[]
  for choice in q[':question/answer-fields'][0][':answer-field/choices']:
   value=parse_tex(choice[':answer/value']);is_correct=equivalent(value,parse_tex(correct))
   result.append(('correct' if is_correct else 'observed_expression_homogeneous_scale',sp.simplify(value*L/L0)))
  return result
 if profile!='authored_operations':raise ValueError('Unknown profile')
 # Complete bank chosen before parameters; source choice count is always five.
 family=d['family'];u=d['u'];a=d['a'];F=d['primitive'];delta=u-a
 F2=d['squared_primitive'];squared=sp.simplify(F2.subs(T,u)-F2.subs(T,a))
 if family=='circle':
  r=d['speed'];wrong=[('drop_square_root',r*r*delta),('omit_one_squared_component_factor',L/sp.sqrt(2)),('double_arc_length',2*L),('halve_arc_length',L/2)]
 elif family=='involute':
  c=sp.simplify(d['speed']/T);wrong=[('omit_power_rule_division',c*(u*u-a*a)),('omit_square_root',squared),('replace_integral_with_speed_change',c*(u-a)),('omit_scale_and_division',u*u-a*a)]
  # The source scale c=2 makes the last expression equal correct. A complete
  # alternate bank is declared for c=2 rather than patching one failed option.
  if c==2:wrong=[('omit_power_rule_division',c*(u*u-a*a)),('omit_square_root',squared),('replace_integral_with_speed_change',c*(u-a)),('drop_one_derivative_scale',L/2)]
 else:
  wrong=[('halve_arc_length',L/2),('double_arc_length',2*L),('omit_square_root',squared),('forget_upper_endpoint_integration',d['speed'].subs(T,u)*delta)]
 return [('correct',L)]+wrong

def render_plots(d,content_id):
 """Plot from the exact instance, preserving endpoint and direction cues."""
 if '![](' not in d['source'][':question/problem']:return None
 if d['u']==d['b'] and d['scale']==1:
  return re.search(r'!\[\]\((.*?)\)',d['source'][':question/problem']).group(1)
 out=HERE/'plots'/f'{content_id}.png';out.parent.mkdir(exist_ok=True)
 if out.exists():return str(out)
 a=float(d['a']);u=float(d['u']);b=max(float(d['b']),u)
 if d['family'] in ('spiral','involute','power','linear','polynomial'):b=u+max(.12*(u-a),.12)
 ts=[a+(u-a)*i/400 for i in range(401)];ct=[max(0,a-.2)+(b+.2-max(0,a-.2))*i/600 for i in range(601)]
 fx=sp.lambdify(T,d['x'],'math');fy=sp.lambdify(T,d['y'],'math')
 obj={'x':[fx(t) for t in ts],'y':[fy(t) for t in ts],'context_x':[fx(t) for t in ct],'context_y':[fy(t) for t in ct],'start_label':'$t='+tex(d['a'])+'$','end_label':'$t='+tex(d['u'])+'$','path':str(out)}
 input_path=HERE/'plot-input'/f'{content_id}.json';input_path.parent.mkdir(exist_ok=True);input_path.write_text(json.dumps([obj]))
 subprocess.run([str(Path('.venv/bin/python').resolve()),str(HERE/'render.py'),str(input_path)],check=True,stdout=subprocess.DEVNULL)
 return str(out)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 rng=random.Random(seed)
 choices=[key for key,d in TEMPLATES.items() if d['level']==level and (field_type is None or d['kind']==field_type)]
 if template is None:template=rng.choice(choices)
 if template not in choices:raise ValueError('Template not compatible with level/field type')
 if profile is None:profile='authored_operations' if TEMPLATES[template]['kind']=='radio' else 'blank'
 if profile=='observed' and parameters is None:raise ValueError('Observed scalar banks require explicit endpoint parameters')
 for attempt in range(100):
  if parameters is not None:
   if set(parameters) not in ({'upper'},{'upper','scale'}):raise ValueError('Explicit upper and optional scale are supported')
   u=sp.sympify(parameters['upper'],locals={'pi':PI});scale=sp.sympify(parameters.get('scale',1))
   if not scale.is_Integer or not 1<=scale<=6:raise ValueError('Uniform coordinate scale must be an integer from 1 to 6')
  else:u=sample_endpoint(template,rng);scale=rng.randint(1,6)
  d=data(template,u,scale);check_endpoint(d);values=bank(template,d,profile)
  invalid=any(not value.is_real or value<=0 for _,value in values) or any(equivalent(x[1],y[1]) for i,x in enumerate(values) for y in values[i+1:])
  if not invalid:break
  if parameters is not None:raise ValueError('Complete bank collision or invalid length option')
 else:raise ValueError('No eligible complete bank')
 solution=scale_solution(render_solution(template,data(template,u)),scale)
 q=d['source'];prompt=q[':question/problem']
 if profile!='observed':prompt=prompt.replace('Do not round the answer.','Give an exact answer.')
 if template=='q-351438':
  prompt=prompt.replace(r'$L=\frac{\sqrt{5}}{2}(', '$L='+tex(scale*sp.sqrt(5)/2)+'(')
 if scale!=1:
  prompt=re.sub(r'x=(.*?),\\,y=(.*?),\\,t',lambda m:'x='+tex(scale)+r'\left('+m.group(1)+r'\right),\,y='+tex(scale)+r'\left('+m.group(2)+r'\right),\,t',prompt,flags=re.S)
 prompt=re.sub(r't\\in \[[^\]]+\]',lambda m:'t\\in ['+tex(d['a'])+','+tex(u)+']',prompt)
 canonical=[sp.srepr(sp.simplify(v)) for v in (d['x'],d['y'],d['a'],u)]
 fingerprint=digest({'math':canonical,'response':'exponential-factor-fragment' if template=='q-351438' else 'full-length','field':d['kind']})
 # Content identity covers all displayed math and bank; plot semantic endpoint
 # descriptor is stable and does not depend on output filename or option order.
 content_id=digest({'version':VERSION,'prompt':re.sub(r'!\[\]\(.*?\)',f'![parametric plot]({fingerprint})',prompt),'solution':solution,'bank':sorted(tex(v) for _,v in values),'field':d['kind']})
 asset=render_plots(d,content_id)
 if asset is not None:prompt=re.sub(r'!\[\]\(.*?\)',lambda m:'![]('+asset+')',prompt)
 qid=uid(content_id);fid=uid(qid+':field');answers=[];correct=None
 for recipe,value in values:
  aid=uid(fid+':'+sp.srepr(sp.simplify(value)));answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':tex(value)})
  if recipe=='correct':correct=aid
 rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':q[':question/answer-fields'][0][':answer-field/key'],':answer-field/type':':answer-field.type/'+d['kind'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'template':template,'seed':seed,'parameters':{'upper':str(u),'scale':str(scale)},'domain':{'lower':str(d['a']),'upper':str(u),'orientation':'increasing parameter; nonnegative speed'},'bank_profile':profile,'presentation_profile':'original_observed' if profile=='observed' else 'exact_answer_compatibility', 'bank_origin':'observed scalar expression profile; intent unresolved' if profile=='observed' and d['kind']=='radio' else 'authored complete operation bank' if d['kind']=='radio' else 'observed blank shape','parameter_fingerprint':fingerprint,'displayed_identity':content_id,'recipes':[{'recipe':recipe,'value':str(value)} for recipe,value in values],'math':{k:str(d[k]) for k in ('x','y','dx','dy','speed','primitive','squared_speed','length')},'plot':asset,'dependencies':{'sympy':sp.__version__}}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+ '\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='markdown');p.add_argument('--template');p.add_argument('--profile');p.add_argument('--parameters',help='Explicit JSON object with upper and optional scale');args=p.parse_args()
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile,parameters=json.loads(args.parameters) if args.parameters else None) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
