"""Source model and replay routines retained from the registered generator."""
from pathlib import Path
import hashlib,json,sys,uuid
import sympy as S
from math_format import normalize_prose, normalize_tex
SOURCE=json.loads(Path(__file__).with_name('source-evidence.json').read_text())
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

