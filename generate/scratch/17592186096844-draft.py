"""Private chain/quotient draft. Frozen MA evidence; complete component masks.
No database operations. Normal profiles derive all ordered source stages.
"""
import argparse,copy,hashlib,importlib.util,json,random,sys,uuid
from pathlib import Path
import sympy as s
KP_ID=17592186096844;KP_UUID='261910cd-a1a4-5c90-8caa-238208558458';TITLE='Calculating a Derivative Using the Chain and Quotient Rules'
HERE=Path(__file__).with_suffix('');VERSION='2.0.0-draft';SUPPORTED_LEVELS=('easy','moderate','hard')
x=s.Symbol('x',real=True);t=s.Symbol('t',real=True)
SOURCE=json.loads((HERE/'source.json').read_text());SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
DEFAULTS={'q-11973':{'c':5},'q-2396':{'b':-2},'q-2400':{},'q-313362':{'c':5},'q-128660':{},'q-132975':{'c':3},'q-11978':{'a':1},'q-2403':{'a':2},'q-313365':{'b':3},'q-313371':{'a':2},'q-343546':{'a':3},'q-343576':{'a':3},'q-344143':{'a':3},'authored-affine-square':{'a':2,'b':1}}
LEVELS={m:q[':question/difficulty'][':db/ident'].split('/')[-1] for m,q in SOURCES.items()};LEVELS['authored-affine-square']='easy'
EXCLUDED={'q-2400':'No captured answer fields; raw evidence only.','q-128660':'Standalone f and preceding parts undefined; raw evidence only.'}
_spec=importlib.util.spec_from_file_location('math_format',HERE.parents[2]/'scripts/question_capture/math_format.py');math_format=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(math_format)
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def tex(e):return s.latex(e).replace(r'\log',r'\ln')
def parameters_for(m):
 if m in EXCLUDED:return [{}]
 if m=='authored-affine-square':return [{'a':a,'b':b} for a in range(2,6) for b in range(1,8)]
 key=next(iter(DEFAULTS[m]));bounds={'q-11973':range(3,10),'q-2396':range(-5,6),'q-313362':range(1,10),'q-132975':range(1,10),'q-11978':range(1,8),'q-2403':range(2,9),'q-313365':range(2,10),'q-313371':range(1,10),'q-343546':(1,3,5,7,9),'q-343576':range(1,10),'q-344143':range(1,10)}
 return [{key:v} for v in bounds[m]]
def validate_parameters(m,p):
 if p not in parameters_for(m) or any(type(v)!=int for v in p.values()):raise ValueError('Outside documented finite parameter domain')
def model(m,p):
 a=p.get('a');b=p.get('b');c=p.get('c');z=x;den=None;factor=s.Integer(1);pt=None
 if m=='q-11973':u=3*x**2;v=(3*x+c)**2
 elif m=='q-2396':u=s.tan(7*x+b);v=4*x
 elif m=='q-313362':u=x**3;v=(3*x+c)**2;den=(3*x+c)**3
 elif m=='q-132975':z=t;u=2*t;v=(2*t**2+c)**2
 elif m=='q-11978':u=(x+a)**2;v=x**2+a**2
 elif m=='q-2403':u=s.sqrt(s.log(x));v=a*x
 elif m=='q-313365':u=(x+1)**2;v=x+b;den=v**2
 elif m=='q-313371':u=s.log(x);v=s.exp(a*x);den=x*v
 elif m=='q-343546':u=s.cos(a*x);v=x;pt=s.pi/2
 elif m=='q-343576':u=s.exp(a*x);v=x+2;pt=1
 elif m=='q-344143':u=s.exp(a*x**2);v=x-2;den=v**2;factor=u
 elif m=='authored-affine-square':u=(a*x+b)**2;v=x;den=x**2
 else:raise ValueError('Raw-only template')
 d=s.factor(s.diff(u/v,z));answer=s.factor(d*den/factor) if den is not None else s.simplify(d.subs(z,pt)) if pt is not None else d
 return z,u,v,d,answer,den,factor,pt

def transform(text,m,p):
 """Simultaneous source-specific whole-component masks, never anchor bypass."""
 a=p.get('a');b=p.get('b');c=p.get('c');pairs=[]
 if m in ('q-11973','q-313362'):
  pairs=[('3x+5',f'3x+{c}'),('(5)',f'({c})'),('30x',f'{6*c}x'),('5x}',f'{c}x}}'),('x+5',f'x+{c}')]
 elif m=='q-2396':pairs=[('7x-2',f'7x{b:+d}')]
 elif m=='q-132975':pairs=[('2{t}^{2}+3',f'2{{t}}^{{2}}+{c}'),('4{t}^{2}+6',f'4{{t}}^{{2}}+{2*c}'),('6-12{t}^{2}',f'{2*c}-12{{t}}^{{2}}')]
 elif m=='q-11978':
  pairs=[('x+1',f'x+{a}'),('{x}^{2}+1',f'{{x}}^{{2}}+{a*a}'),('1-x',f'{a}-x'),('2(1-{x}^{2})',f'{2*a}({a*a}-{{x}}^{{2}})'),('2(x+1)(1-x)',f'{2*a}(x+{a})({a}-x)'),('2(x+1)({x}^{2}+1-{x}^{2}-x)',f'2(x+{a})({{x}}^{{2}}+{a*a}-{{x}}^{{2}}-{str(a) if a!=1 else ""}x)'),('2(1-x)',f'2({a}-x)'),('(1-2{x}^{2})',f'({a}-2{{x}}^{{2}})')]
 elif m=='q-2403':
  L=r'\operatorname{ln}⁡x';R=r'\sqrt{'+L+'}'
  pairs=[('2x.$',f'{a}x.$'),('2{x}^{2}',f'{a}{{x}}^{{2}}'),('2x}',f'{a}x}}'),('(2x)',f'({a}x)'),(')(2)',f')({a})'),('=2.',f'={a}.'),('4{x}^{2}',f'{a*a}{{x}}^{{2}}'),('2'+R,f'{a}'+R),(r'\frac{1}{'+R+'}-2'+R,r'\frac{'+tex(s.Rational(a,2))+'}{'+R+'}-'+str(a)+R),('1-2'+L,tex(s.Rational(a,2))+'-'+str(a)+L),('1+2'+R,'1+'+str(a)+R),(L+'-2',L+'-'+str(a))]
 elif m=='q-313365':pairs=[('x+3',f'x+{b}'),('2x+6-x-1',f'2x+{2*b}-x-1'),('x+5',f'x+{2*b-1}')]
 elif m=='q-313371':pairs=[('2x',f'{a}x'),('2{e}',f'{a}{{e}}')]
 elif m=='q-343546':
  sn=int(s.sin(a*s.pi/2));ans=rf'\frac{{{-2*a*sn}}}{{\pi }}'
  pairs=[('3x',f'{a}x'),('-3',f'-{a}'),(r'\frac{3\pi }{2}',rf'\frac{{{a}\pi }}{{2}}'),('(-1)',f'({sn})'),(r'\frac{6}{\pi }',ans)]
 elif m=='q-343576':pairs=[('3x',f'{a}x'),('3{e}',f'{a}{{e}}'),('3x+6-1',f'{a}x+{2*a}-1'),('3x+5',f'{a}x+{2*a-1}'),('3(1)+5',f'{a}(1)+{2*a-1}'),('3(1)',f'{a}(1)'),('8{e}^{3}',f'{3*a-1}{{e}}^{{{a}}}')]
 elif m=='q-344143':pairs=[('3{x}^{2}',f'{a}{{x}}^{{2}}'),('6x',f'{2*a}x'),('6{x}^{2}-12x-1',f'{2*a}{{x}}^{{2}}-{4*a}x-1')]
 elif m not in EXCLUDED:raise ValueError(m)
 # Longest component wins before shorter nested components. New values cannot cascade.
 pairs=sorted(pairs,key=lambda p:len(p[0]),reverse=True)
 for i,(old,new) in enumerate(pairs):text=text.replace(old,f'@@MASK{i}@@')
 for i,(old,new) in enumerate(pairs):text=text.replace(f'@@MASK{i}@@',new)
 return text

def bank(m,p,answer):
 a=p.get('a');b=p.get('b');c=p.get('c')
 if m=='q-11973':return [6*x/(3*x+c)**3,x/(3*x+c)**4,answer,2*x/(3*x+c)**4,c*x/(3*x+c)**4]
 if m=='q-2396':T=s.tan(7*x+b);S=s.sec(7*x+b)**2;return [answer,(7*S-T)/(16*x**2),(x*S+T)/(4*x**2),(7*x*S-T)/(16*x**2),(S-T)/(4*x**2)]
 if m=='q-11978':D=(x*x+a*a)**2;return [(a-x)**2/D,2*(x+a)/D,answer,2*(a-x)/D,(a-2*x*x)/D]
 if m=='q-2403':L=s.log(x);return [(x-a*s.sqrt(L))/(a*a*x*x*L),(s.Rational(a,2)-a*L)/s.sqrt(L),(1+a*s.sqrt(L))/(a*x*x*s.sqrt(L)),answer,(L-a)/s.sqrt(L)]
 return [answer]

def domain(m,p):
 if m=='q-2396':return {'restriction':f'x != 0; cos(7*x{p["b"]:+d}) != 0','denominator_zeroes':['0'],'chain_inner':f'7*x{p["b"]:+d}'}
 if m=='q-2403':return {'restriction':'x>1','denominator_zeroes':['0'],'chain_inner':'ln(x)>0'}
 if m=='q-132975':return {'restriction':'t>0','denominator_zeroes':[],'chain_inner':f'2*t^2+{p["c"]}>0'}
 if m=='q-313371':return {'restriction':'x>0','denominator_zeroes':[],'chain_inner':f'{p["a"]}*x'}
 if m=='q-11978':return {'restriction':'all real x','denominator_zeroes':[],'chain_inner':f'x+{p["a"]}'}
 z,u,v,d,ans,den,factor,pt=model(m,p);zeros=s.solve(v,z)
 return {'restriction':'real '+str(z)+'; denominator nonzero','denominator_zeroes':[tex(v) for v in zeros if v.is_real is not False],'evaluation_point':tex(s.sympify(pt)) if pt is not None else None}
def task_fingerprint(m,p):
 z,u,v,d,ans,den,factor,pt=model(m,p)
 return digest([s.srepr(u/v),str(z),s.srepr(pt),s.srepr(ans),'fragment' if den is not None else 'full'])
def authored(p):
 a=p['a'];b=p['b'];I=f'{a}x+{b}';A=f'{a*a}{{x}}^{{2}}-{b*b}'
 prompt=rf'Given that $y=\frac{{({I})^{{2}}}}{{x}},$ find $\frac{{\text{{d}}y}}{{\text{{d}}x}}.$'+'\n\n| $'+r'\frac{\text{d}y}{\text{d}x}'+'$ | $=$ | {{field-1}} |\n| --- | --- | --- |\n|  |  | $x^2$ |'
 sol=rf'We use the quotient rule with the numerator $u(x)=({I})^{{2}}$ and the denominator $v(x)=x.$ '+'\n\nDifferentiating $u(x)$ and $v(x),$ we have\n\n$$\n'+rf"{{u}}^{{′}}(x)={2*a}({I}),\,{{v}}^{{′}}(x)=1."+'\n$$\n\nNote that we used the chain rule to differentiate $u.$\n\nNow, applying the quotient rule and simplifying, we have\n\n$$\n'+r'\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{u}^{′}(x)\cdot v(x)-u(x)\cdot {v}^{′}(x)}{[v(x)]^{2}} \\ & ='+rf'\frac{{{2*a}({I})x-({I})^{{2}}}}{{x^{{2}}}} \\ & =\frac{{({I})({a}x-{b})}}{{x^{{2}}}} \\ & =\frac{{{A}}}{{x^{{2}}}}.\end{{aligned}}'+'\n$$'
 return prompt,sol

def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unknown difficulty')
 rng=random.Random(seed);raw=profile in ('observed_raw','raw') or bool(profile and profile.startswith('raw-'))
 if profile and profile.startswith('raw-'):template=template or profile[4:]
 eligible=[m for m,l in LEVELS.items() if l==level and (raw or m not in EXCLUDED)]
 m=template or rng.choice(eligible)
 if m not in eligible:raise ValueError('Template/level unavailable')
 if profile not in (None,'default','source-component-bank','authored-blank','observed_raw','raw','raw-'+m):raise ValueError('Unknown profile')
 p=copy.deepcopy(parameters) if parameters is not None else copy.deepcopy(DEFAULTS[m]) if raw else rng.choice(parameters_for(m));validate_parameters(m,p)
 if raw:
  if m not in SOURCES or p!=DEFAULTS[m]:raise ValueError('Exact frozen raw profile requires source parameters')
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':copy.deepcopy(SOURCES[m]),'generation':{'version':VERSION,'template':m,'level':level,'seed':seed,'parameters':p,'profile':'observed_raw','evidence_only':True,'eligible_for_learning':False,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'plots':'none'}}
 z,u,v,d,answer,den,factor,pt=model(m,p);values=bank(m,p,answer)
 # All recipes chosen as one complete bank; explicit collisions reject entirely.
 for i,one in enumerate(values):
  for two in values[i+1:]:
   if one==two or (not any(s.simplify((one-two).subs(z,n))!=0 for n in (2,3)) and s.simplify(one-two)==0):raise ValueError('Complete bank collision')
 if m=='authored-affine-square':prompt,sol=authored(p);key='field-1';ft=':answer-field.type/blank';ci=0;rendered=[tex(answer)]
 else:
  src=SOURCES[m];sf=src[':question/answer-fields'][0];ft=sf[':answer-field/type'][':db/ident'];key=sf[':answer-field/key'];ci=next(i for i,a in enumerate(sf[':answer-field/choices']) if a[':answer/id']==sf[':answer-field/correct'][':answer/id'])
  prompt=transform(src[':question/problem'],m,p);sol=transform(src[':question/worked-solution'],m,p)
  rendered=[transform(a[':answer/value'],m,p) for a in sf[':answer-field/choices']]
  if m=='q-132975':
   prompt=rf'Given that $x(t)=\frac{{2t}}{{(2{{t}}^{{2}}+{p["c"]})^{{2}}}},\,t>0,$ find ${{x}}^{{′}}(t).$'+'\n\n'+r'${x}^{′}(t)=\,$'+'\n{{field-1}}'
   sol=sol.replace('and from part 1, we have','and differentiating $h(t)$ using the chain rule, we have')
 if field_type not in (None,ft,ft.split('/')[-1]):raise ValueError('Answer-field contract is fixed')
 prompt=math_format.normalize_prose(prompt);sol=math_format.normalize_prose(sol);rendered=[math_format.normalize_tex(v) for v in rendered]
 fp=task_fingerprint(m,p);body=[prompt,sol,level,ft,key,rendered,ci,domain(m,p),VERSION];cid=digest(body);uid=lambda q:str(uuid.uuid5(uuid.UUID(KP_UUID),q));qid=uid(cid);fid=uid(qid+key)
 choices=[{':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in rendered];correct=choices[ci][':answer/id']
 if ft.endswith('/radio'):rng.shuffle(choices)
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':ft,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
 out={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'generator_id':uid(VERSION),'level':level,'seed':seed,'template':m,'profile':'authored-blank' if m=='authored-affine-square' else 'source-component-bank','bank_profile':m if ft.endswith('/radio') else None,'parameters':p,'parameter_fingerprint':fp,'mathematical_fingerprint':fp,'content_identity':cid,'domain':domain(m,p),'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'source_refs':[] if m=='authored-affine-square' else [m],'evidence_only':False,'eligible_for_learning':True,'difficulty_provenance':'authored conservative simple affine-square quotient' if m=='authored-affine-square' else 'observed MA level','dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'plots':'none'}}
 return math_format.validate_generated_record(out)
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def batch(level,count,seed=0,template=None,profile=None):
 rng=random.Random(seed);out=[];seen=set()
 for i in range(max(100,count*100)):
  if len(out)==count:return out
  try:r=generate(level,rng.getrandbits(32),template=template,profile=profile)
  except ValueError:continue
  fp=r['generation'].get('parameter_fingerprint',digest(r['question']))
  if fp not in seen:out.append(r);seen.add(fp)
 raise ValueError('Requested count exceeds finite distinct tasks')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+q.get(':question/worked-solution','')+'\n\nAnswers: '+', '.join(a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[]))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=SUPPORTED_LEVELS+('all',),default='all');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=('json','markdown'),default='json');args=ap.parse_args();levels=SUPPORTED_LEVELS if args.difficulty=='all' else [args.difficulty];out=[r for l in levels for r in batch(l,args.count,args.seed,args.template,args.profile)];print(json.dumps(out,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,out)))
if __name__=='__main__':main()
