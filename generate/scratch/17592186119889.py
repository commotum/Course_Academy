#!/usr/bin/env python3
"""Surface-area integrand templates. Read-only generation; publication is separate.

Each source has one complete observed bank. Coefficient variations below are
conservative authored extensions of those banks, with opaque errors explicitly
retained as expression patterns, not diagnoses of a learner's reasoning.
"""
from pathlib import Path
import argparse, hashlib, json, os, random, sys, uuid
try:
 import sympy as S
except ModuleNotFoundError:
 interpreter=Path(__file__).resolve().parents[2]/".venv/bin/python"
 if Path(sys.executable).resolve()!=interpreter.resolve():os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])
 raise
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import checked_math_content, normalize_prose, normalize_tex
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP_ID=17592186119889
KP_UUID=SOURCE['record'][':knowledge-point/id']
TITLE=SOURCE['record'][':knowledge-point/title']
VERSION='surface-integrand-v1'
U,V=S.symbols('u v',nonnegative=True)
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
TEMPLATES={
 'q-105613':{'level':'hard','base':{'a':2},'domain':[{'a':a} for a in range(2,6)],'bounds':(1,S.pi)},
 'q-109941':{'level':'moderate','base':{'a':1},'domain':[{'a':a} for a in range(1,6)],'bounds':(2,2)},
 'q-109948':{'level':'hard','base':{'a':1},'domain':[{'a':a} for a in range(1,6)],'bounds':(4,S.pi)},
 'q-110019':{'level':'hard','base':{'a':2},'domain':[{'a':a} for a in range(2,6)],'bounds':(1,S.pi)},
 'q-109943':{'level':'moderate','base':{'a':4,'b':5},'domain':[{'a':a,'b':b} for a in range(2,9) for b in range(a+1,a+4) if (a,b)!=(2,3)],'bounds':(1,2)},
 'q-109947':{'level':'hard','base':{'a':3},'domain':[{'a':a} for a in range(3,8)],'bounds':(1,1)},
 'q-109951':{'level':'hard','base':{'a':1},'domain':[{'a':a} for a in range(1,6)],'bounds':(2,4)},
}
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(value):return str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+':'+value))
def tex(x):return S.latex(S.sympify(x))
def vec(v):return r'\langle '+r',\,'.join(map(tex,v))+r'\rangle'
def det(rows):return r'\begin{vmatrix}'+r' \\ '.join(' & '.join(map(str,r)) for r in rows)+r'\end{vmatrix}'
def aligned(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def root(x):return r'\sqrt{'+x+'}'
def model(template,p):
 a=S.Integer(p['a']);u,v=U,V;sin,cos,exp,sqrt=S.sin,S.cos,S.exp,S.sqrt
 if template=='q-105613':
  b=a+1;r=S.Matrix([a*u*sin(v),b*u*cos(v),u])
  correct=u*sqrt((b*b-a*a)*sin(v)**2+a*a*(1+b*b))
  bank=[correct,sqrt(u*u+a*a*b*b),a*b*sqrt(u*u*sin(v)**2+u*u+1),a*b*sqrt(u*u+1),sqrt(b*u*u*cos(v)**2+a*a*u*u+a*a*b*b)]
 elif template=='q-109941':
  r=S.Matrix([a*u*u,u-v*v,v*v]);correct=2*v*sqrt(1+8*a*a*u*u)
  bank=[correct,u*sqrt(1+4*a*a*v),sqrt(v*v-a*a*u*u),sqrt(a*a*u*u+v*v),v*v*sqrt(1+4*a*a*u*u)]
 elif template=='q-109948':
  r=S.Matrix([a*u,exp(u)*sin(v),exp(u)*cos(v)]);correct=exp(u)*sqrt(exp(2*u)+a*a)
  bank=[exp(u)*sqrt(u+a*a),exp(2*u)*sqrt(cos(v)+sin(v)),correct,exp(u)*cos(v)*sin(v),sqrt(exp(u)*cos(v)*sin(v))]
 elif template=='q-110019':
  r=S.Matrix([u*u,a*u*sin(v),u*cos(v)]);correct=u*sqrt(a*a+4*u*u+4*(a*a-1)*u*u*cos(v)**2)
  bank=[u*sqrt(u*u+cos(v)**2),sqrt(1+a*u*u),a*u*sqrt(1+u*u*cos(v)**2),cos(v)*sqrt(1+u*u),correct]
 elif template=='q-109943':
  b=S.Integer(p['b']);r=S.Matrix([u+v,3-v,1+a*u+b*v]);correct=sqrt(a*a+(a-b)**2+1)
  bank=[sqrt(a+b+1),sqrt(b-a+2),u*sqrt(v*v+1),2*sqrt(u+v),correct]
 elif template=='q-109947':
  r=S.Matrix([u+v,a*u*u,u-v]);correct=2*sqrt(2*a*a*u*u+1)
  bank=[sqrt(u*u+4),2*u*sqrt(a*a*u*u+1),2*sqrt(u*u+1),correct,u*sqrt(u*u+4)]
 elif template=='q-109951':
  r=S.Matrix([a*u*u,v*v,u*v]);correct=2*sqrt(a*a*u**4+v**4+4*a*a*u*u*v*v)
  bank=[sqrt(u*u+v*v),correct,2*u*u*v,u*sqrt(u*u+1),2*u*sqrt(v*v+u*v)]
 else:raise ValueError(template)
 return r,correct,bank

def norm_stages(template,p,cross,answer):
 """Retain the source's sum-of-squares, collection and factor stages."""
 a=S.Integer(p['a']);u,v=U,V
 square_terms=[S.expand(x*x) for x in cross]
 square=S.trigsimp(sum(square_terms));expanded='+'.join(map(tex,square_terms))
 stages=[r'\left\|'+vec(cross)+r'\right\|',root('+'.join(r'\left('+tex(x)+r'\right)^2' for x in cross)),root(expanded)]
 if template=='q-109943':
  stages += [root(tex(square)),tex(answer)]
 elif template=='q-105613':
  b=a+1;d=b*b-a*a;c=a*a*(1+b*b)
  stages += [root(tex(d*u*u*S.sin(v)**2)+r'+'+tex(a*a*u*u)+r'\left(\sin^2 v+\cos^2 v\right)+'+tex(a*a*b*b*u*u)),root(tex(d*u*u*S.sin(v)**2+a*a*u*u+a*a*b*b*u*u)),root(tex(u*u*(d*S.sin(v)**2+c))),root(tex(u*u))+root(tex(d*S.sin(v)**2+c)),tex(answer)]
 elif template=='q-109948':
  stages += [root(tex(S.exp(4*u))+'+'+tex(a*a*S.exp(2*u))+r'\left(\sin^2 v+\cos^2 v\right)'),root(tex(square)),root(tex(S.exp(2*u)))+root(tex(S.exp(2*u)+a*a)),tex(answer)]
 elif template=='q-110019':
  stages += [root(tex(a*a*u*u)+'+'+tex(4*u**4)+r'\left(\sin^2 v+\cos^2 v\right)+'+tex(4*(a*a-1)*u**4*S.cos(v)**2)),root(tex(a*a*u*u+4*u**4+4*(a*a-1)*u**4*S.cos(v)**2)),root(tex(u*u))+root(tex(a*a+4*u*u+4*(a*a-1)*u*u*S.cos(v)**2)),tex(answer)]
 elif template=='q-109941':
  stages += [root(tex(square)),root(tex(4*v*v*(1+8*a*a*u*u))),root(tex(4*v*v))+root(tex(1+8*a*a*u*u)),tex(answer)]
 elif template=='q-109947':
  stages += [root(tex(square)),root('4'+r'\left('+tex(2*a*a*u*u+1)+r'\right)'),tex(answer)]
 elif template=='q-109951':
  stages += [root('4'+r'\left('+tex(a*a*u**4+v**4+4*a*a*u*u*v*v)+r'\right)'),tex(answer)]
 return stages

def solution(template,p,r,answer):
 ru=r.diff(U);rv=r.diff(V);raw=ru.cross(rv);cross=raw.applyfunc(S.trigsimp)
 norm=r'\left\|\mathbf r_u\times\mathbf r_v\right\|'
 formula='$'+r'\iint_S\mathrm{d}S=\iint_D'+norm+r'\,\mathrm{d}A'+'$'
 # Retain the source sentences and ordered mathematical stages, replacing
 # captured Unicode operators and nested aligned determinant tables with TeX.
 sol='For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\\in D,$ the surface area of $S$ is given by\n\n$$\n'+formula[1:-1]+'.\n$$\n\nWe first compute the tangent vectors to the grid curves:\n\n'
 rows=[]
 for variable,deriv in [(U,ru),(V,rv)]:
  rows += [r'\mathbf r_'+str(variable)+r' &='+r'\langle '+r',\,'.join(r'\frac{\partial '+x+r'}{\partial '+str(variable)+'}' for x in 'xyz')+r'\rangle',r' &='+r'\langle '+r',\,'.join(r'\frac{\partial}{\partial '+str(variable)+r'}\left('+tex(x)+r'\right)' for x in r)+r'\rangle',r' &='+vec(deriv)]
 sol+=aligned(rows)+'\n\nNow, the fundamental vector product is\n\n'
 d=det([['i','j','k'],list(map(tex,ru)),list(map(tex,rv))])
 minors=[det([[tex(ru[i]),tex(ru[j])],[tex(rv[i]),tex(rv[j])]]) for i,j in [(1,2),(0,2),(0,1)]]
 rows=[r'\mathbf r_u\times\mathbf r_v &='+d,r' &='+r'\langle '+minors[0]+r',\,-'+minors[1]+r',\,'+minors[2]+r'\rangle',r' &='+vec(raw)]
 if raw!=cross:rows.append(r' &='+vec(cross))
 sol+=aligned(rows)+'\n\nand\n\n'
 stages=norm_stages(template,p,cross,answer)
 sol+=aligned([norm+r' &='+stages[0]]+[r' &='+s for s in stages[1:]])
 if template in ['q-105613','q-110019']:sol+='\n\nNotice that $\\sqrt{u^2}=u$ since $u\\ge 0$ on $D.$'
 if template=='q-109941':sol+='\n\nNotice that $\\sqrt{v^2}=v$ since $v\\ge 0$ on $D.$'
 sol+='\n\nTherefore, the surface area is\n\n'+aligned([r'\iint_S\mathrm{d}S &=\iint_D'+norm+r'\,\mathrm{d}A',r' &=\iint_D '+tex(answer)+r'\,\mathrm{d}A'])
 return normalize_prose(sol)

@checked_math_content
def generate(difficulty='moderate',seed=0,template=None,parameters=None,profile=None):
 rng=random.Random(seed)
 templates=[k for k,t in TEMPLATES.items() if t['level']==difficulty]
 if not templates:raise ValueError('Unsupported difficulty: '+difficulty)
 template=template or rng.choice(templates);t=TEMPLATES[template]
 if template not in templates:raise ValueError('Template/difficulty mismatch')
 p=parameters or rng.choice(t['domain'])
 if p not in t['domain']:raise ValueError('Outside validated parameter domain')
 bank_profile='observed-expression-pattern:'+template
 if profile is not None and profile!=bank_profile:raise ValueError('Unknown complete bank profile')
 r,answer,bank=model(template,p);umax,vmax=t['bounds']
 bounds=r'0\le u\le '+tex(umax)+r',\,0\le v\le '+tex(vmax)
 prompt='$$\n'+r'\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):'+bounds+r'\}'+'\n$$\n\nThe integral above gives the surface area of the parametric surface $r(u,v)='+vec(r)+'$ for $'+bounds+'.$ What is the missing expression?'
 prompt=normalize_prose(prompt);sol=solution(template,p,r,answer)
 values=[normalize_tex(tex(x)) for x in bank]
 # All bank entries are mathematical functions, including deliberately invalid
 # real-valued candidates retained from the source; exactly one works on D.
 correct_index=next(i for i,x in enumerate(bank) if S.simplify(x-answer)==0)
 fingerprint=digest({'task':'surface-integrand','template':template,'integrand_squared':S.srepr(S.trigsimp(answer**2)),'bounds':[str(umax),str(vmax)]})
 content=digest({'task':fingerprint,'prompt':prompt,'solution':sol,'bank':sorted(values),'correct':values[correct_index]})
 qid=uid('question:'+content);fid=uid('field:'+qid+':selection')
 choices=[{':answer/id':uid(fid+':'+value),':answer/type':':answer.type/math',':answer/value':value} for value in values]
 cid=choices[correct_index][':answer/id'];rng.shuffle(choices)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',cid]}]},'generation':{'version':VERSION,'template':template,'bank_profile':bank_profile,'seed':seed,'parameters':p,'bounds':{'u':[0,str(umax)],'v':[0,str(vmax)]},'source_question':QS[template][':db/id'],'source_basis':SOURCE['basis'],'mathematical_task_fingerprint':fingerprint,'content_fingerprint':content,'dependencies':{'python':sys.version.split()[0],'sympy':S.__version__},'plot_rating':'none','correct_expression':str(answer)}}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',default='moderate');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--template');parser.add_argument('--parameters',type=json.loads);parser.add_argument('--output',type=Path);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='json')
 args=parser.parse_args()
 if args.count<1:parser.error('--count must be positive')
 templates=[args.template] if args.template else [k for k,t in TEMPLATES.items() if t['level']==args.difficulty]
 if not templates:parser.error('Unsupported difficulty; see capabilities.json')
 tasks=[(t,p) for t in templates for p in TEMPLATES[t]['domain'] if args.parameters is None or p==args.parameters]
 rng=random.Random(args.seed);rng.shuffle(tasks);rows=[];seen=set()
 for i,(t,p) in enumerate(tasks):
  r=generate(args.difficulty,args.seed+i,t,p);key=r['generation']['mathematical_task_fingerprint']
  if key in seen:continue
  seen.add(key);rows.append(r)
  if len(rows)==args.count:break
 if len(rows)<args.count:parser.error('Finite capability: requested '+str(args.count)+' but only '+str(len(rows))+' distinct tasks in this domain')
 out=(json.dumps(rows,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in rows))+'\n'
 if args.output:args.output.write_text(out)
 else:print(out,end='')
