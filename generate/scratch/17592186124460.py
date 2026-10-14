#!/usr/bin/env python3
"""Rate of change in a direction, local step-3–7 generator; no database writes.

Seven source families and full banks are exposed by raw-q-* public profiles.
Raw profiles preserve omissions, original answer notation, and two
mathematically incorrect fastest-decrease solutions; they are evidence only.
Normal defaults use all seven source-shaped families, complete operation banks,
and signed rate -||gradient|| for fastest decrease. Easy is an explicitly
authored assignment of the unrated x^2/y example: two elementary partials,
normalization and one dot product. Moderate and hard retain observed workloads.
Missing unrated solutions and keys are independently authored, never recovered.

Each family renders its own source operation sequence at changed parameters.
Question identity hashes actual content and complete bank (order independent).
Task fingerprint excludes positive common scaling of supplied direction vectors.
Use .venv/bin/python; evidence and validation live in the same-named directory.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as S
KP_ID=17592186124460
KP_UUID='c330648f-69ad-5778-98cb-bd48a0b160dd'
TITLE='Finding the Rate of Change of a Function in a Given Direction'
VERSION='directional-rate-1'
D=Path(__file__).with_suffix('')
CAPTURE=json.loads((D/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
x,y=S.symbols('x y',real=True)
TEMPLATES={'quotient':'easy','ratio_sum':'moderate','sine_quotient':'moderate','tangent':'moderate','exp_bilinear':'hard','sumlog':'hard','sinlog':'hard'}
ANCHORS={
'q-36297':('quotient',dict(c=1,h='2',k='1',v1='-1',v2='3')),
'q-37074':('sinlog',dict(c=1,n=1,j=1)),
'q-130801':('ratio_sum',dict(h='-1',k='1',v1='1',v2='-sqrt(2)')),
'q-36300':('exp_bilinear',dict(a=2,b=3,h=1)),
'q-37083':('sumlog',dict(a=1,b=1,h=2)),
'q-83608':('sine_quotient',dict(a=1,b=1,h='1',k='1',v1='-2',v2='2')),
'q-83613':('tangent',dict(a=2,h='pi/4',k='pi/4',v1='-1',v2='1'))}
FAMILY_SOURCE={t:sid for sid,(t,p) in ANCHORS.items()}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def expr(z):return S.sympify(z,locals={'pi':S.pi,'e':S.E})
def tex(z):return S.latex(expr(z)).replace(r'\log',r'\ln').replace(r'\left', '').replace(r'\right','').replace('- ', '-').replace(r' \sqrt', r'\sqrt')
def group(z):return '('+tex(z)+')' if expr(z)<0 else tex(z)
def vec(a,b,space=False):return '⟨'+a+(','+r'\,' if space else ',')+b+'⟩'
def frac(a,b):return r'\frac{'+str(a)+'}{'+str(b)+'}'
def bracepow(z,n=2):return '('+tex(z)+')^{'+str(n)+'}' if expr(z)<0 else '{'+tex(z)+'}^{'+str(n)+'}'
def mult(c,z):return ('' if c==1 else str(c))+z

def parameters(t,p):
 keys=set(ANCHORS[FAMILY_SOURCE[t]][1])
 if set(p)!=keys:raise ValueError(('parameter keys',t,keys,set(p)))
 q={k:expr(v) for k,v in p.items()}
 if any(v.has(S.Float) or v.free_symbols for v in q.values()):raise ValueError('exact constant parameters required')
 if t in ('quotient','ratio_sum','sine_quotient','tangent'):
  if q['v1']==0 or q['v2']==0:raise ValueError('both supplied direction components must be nonzero')
  v=tuple(q[k] for k in ('v1','v2'))
  if any(not z.is_real for z in v) or S.simplify(sum(z*z for z in v))==0:raise ValueError('real nonzero direction required')
  if t in ('quotient','ratio_sum','sine_quotient'):
   if not all(q[k].is_Integer and 1<=abs(q[k])<=5 for k in ('h','k')):raise ValueError('nonzero integer coordinates bounded by 5')
  if t=='quotient' and not (q['h']>0 and q['k']>0 and q['c'].is_Integer and 1<=q['c']<=4):raise ValueError('easy positive coordinates/coefficient bounds')
  if t=='sine_quotient' and not (q['k']>0 and all(q[k].is_Integer and 1<=q[k]<=4 for k in ('a','b'))):raise ValueError('moderate sine coefficient/domain bounds')
  if t=='tangent' and not(q['h']==q['k'] and abs(q['h'])==S.pi/4 and q['a'].is_Integer and 1<=q['a']<=6):raise ValueError('equal familiar nonzero quarter-pi arguments; coefficient 1..6')
  if any(abs(z.evalf())>6 or not (z.is_Integer or (z/S.sqrt(2)).is_Integer) for z in v):raise ValueError('direction components: signed integers or integer multiples of sqrt(2), absolute bound 6')
 elif t=='exp_bilinear':
  if not all(q[k].is_Integer and lo<=q[k]<=hi for k,lo,hi in [('a',2,6),('b',2,5),('h',1,4)]):raise ValueError('hard exponential coefficient bounds')
  if q['a']*q['b']*q['h']+q['b']>30 or q['a']*q['h']-1>12:raise ValueError('hard exponential evaluated component bounds 30 and 12')
 elif t=='sumlog':
  if not all(q[k].is_Integer and lo<=q[k]<=hi for k,lo,hi in [('a',1,8),('b',1,8),('h',1,4)]):raise ValueError('hard log-product coefficient bounds')
 elif t=='sinlog':
  if not all(q[k].is_Integer and 1<=q[k]<=hi for k,hi in [('c',4),('n',4),('j',4)]):raise ValueError('hard sin-log familiar n*j*pi bounds')
 return q

def data(t,p):
 if t=='quotient':F=p['c']*x*x/y;h,k=p['h'],p['k'];v=(p['v1'],p['v2'])
 elif t=='ratio_sum':F=x/y+y/x;h,k=p['h'],p['k'];v=(p['v1'],p['v2'])
 elif t=='sine_quotient':F=p['a']*S.sin(S.pi*x)/y+p['b']*S.pi*x*y;h,k=p['h'],p['k'];v=(p['v1'],p['v2'])
 elif t=='tangent':F=p['a']*x*S.tan(y)-p['a']*y*S.tan(x);h,k=p['h'],p['k'];v=(p['v1'],p['v2'])
 elif t=='exp_bilinear':F=p['a']*x*y+S.exp(p['b']*x-y);h,k=p['h'],p['b']*p['h'];v=None
 elif t=='sumlog':s=p['a']*x+p['b']*y;F=s*S.log(s);h,k=p['h'],(1-p['a']*p['h'])/p['b'];v=None
 else:F=p['c']*S.sin(y*S.log(x));h,k=S.exp(p['n']),p['j']*S.pi/p['n'];v=None
 grad=tuple(S.diff(F,z) for z in (x,y));ev=tuple(S.simplify(z.subs({x:h,y:k})) for z in grad)
 norm=S.sqrt(sum(z*z for z in ev))
 if v:
  vn=S.sqrt(sum(z*z for z in v));u=tuple(S.simplify(z/vn) for z in v);answer=S.simplify(sum(z*w for z,w in zip(ev,u)))
 else:vn=None;u=None;answer=S.simplify(norm if t=='sinlog' else -norm)
 return dict(F=F,h=h,k=k,v=v,grad=grad,ev=ev,norm=S.simplify(norm),vn=vn,u=u,answer=answer)

def function_tex(t,p):
 if t=='quotient':return frac(mult(p['c'],'x^{2}'),'y')
 if t=='ratio_sum':return r'\frac{x}{y}+\frac{y}{x}'
 if t=='sine_quotient':return frac(mult(p['a'],r'\operatorname{sin}⁡(\pi x)'),'y')+'+'+mult(p['b'],r'\pi xy')
 if t=='tangent':return mult(p['a'],r'x\operatorname{tan}⁡y')+'-'+mult(p['a'],r'y\operatorname{tan}⁡x')
 if t=='exp_bilinear':return str(p['a'])+r'xy+{e}^{'+str(p['b'])+'x-y}'
 if t=='sumlog':s=mult(p['a'],'x')+'+'+mult(p['b'],'y');return '('+s+r')\operatorname{ln}⁡('+s+')'
 return mult(p['c'],r'\sin (y\ln x)')

def point_tex(t,p,d):
 if t=='tangent':return tex(d['h']).replace(r'\pi}',r'\pi }')+','+tex(d['k']).replace(r'\pi}',r'\pi }')
 if t=='sinlog':return ('e' if p['n']==1 else tex(d['h']))+', '+('π' if p['n']==p['j']==1 else tex(d['k']))
 if t=='quotient':return tex(d['h'])+', '+tex(d['k'])
 return tex(d['h'])+','+tex(d['k'])

def prompt(t,p,d):
 sid=FAMILY_SOURCE[t];old=SOURCES[sid][':question/problem'];ap=parameters(t,ANCHORS[sid][1]);ad=data(t,ap)
 # Complete formula/coordinate/vector slots: never global number replacement.
 original_formula=re.search(r'\$[fg]\(x, ?y\)\s*=\s*(.*?)\$',old)[1].rstrip('.')
 original_point=re.search(r'at the point \$\((.*?)\)\$',old)[1]
 slots={original_formula:function_tex(t,p),'('+original_point+')':'('+point_tex(t,p,d)+')'}
 if d['v']:
  original={'quotient':'⟨ - 1, 3⟩','ratio_sum':r'⟨1,-\sqrt{2}⟩','sine_quotient':'⟨-2,2⟩','tangent':'⟨-1,1⟩'}[t]
  slots[original]=('⟨ '+tex(d['v'][0])+', '+tex(d['v'][1])+'⟩') if t=='quotient' else vec(tex(d['v'][0]),tex(d['v'][1]))
  if t=='quotient' and d['v']==(-1,3):slots[original]='⟨ - 1, 3⟩' # source's unary-sign spacing, general rendered data
 return re.sub('|'.join(re.escape(k) for k in sorted(slots,key=len,reverse=True)),lambda m:slots[m[0]],old)

# Each block's row structure is kept intact, including individually evaluated terms.
def tangent_evaluated(p,d):
 a=p['a'];z=tex(abs(2*a*d['h']))
 return (str(a)+'-'+z,z+'-'+str(a)) if d['h']>0 else (z+'-'+str(a),str(a)+'-'+z)

def derivative_rows(t,p,d):
 h,k=d['h'],d['k'];H,K=tex(h),tex(k);a=p.get('a',1);b=p.get('b',1)
 if t=='ratio_sum':
  general=vec(r'\frac{1}{y}-\frac{y}{{x}^{2}}',r'\frac{1}{x}-\frac{x}{{y}^{2}}',True)
  sub=vec(frac('1',group(k))+'-'+frac(group(k),bracepow(h)),frac('1',group(h))+'-'+frac(group(h),bracepow(k)))
  return general,sub,None,vec(*map(tex,d['ev']))
 if t=='sine_quotient':
  general=vec(frac(mult(a,r'\pi \operatorname{cos}⁡(\pi x)'),'y')+'+'+mult(b,r'\pi y'),'-'+frac(mult(a,r'\operatorname{sin}⁡(\pi x)'),'{y}^{2}')+'+'+mult(b,r'\pi x'),True)
  sub=vec(frac(mult(a,r'\pi \operatorname{cos}⁡(\pi \cdot '+H+')'),K)+'+'+mult(b,r'\pi \cdot '+group(k)),'-'+frac(mult(a,r'\operatorname{sin}⁡(\pi \cdot '+H+')'),bracepow(k))+'+'+mult(b,r'\pi \cdot '+group(h)),True)
  # Preserve the source's separately evaluated trig and polynomial components.
  pieces=[a*S.pi*S.Integer(-1)**int(h)/k,b*S.pi*k,0,b*S.pi*h]
  mid=vec(tex(pieces[0])+' '+('+' if pieces[1]>=0 else '')+tex(pieces[1])+' ',tex(pieces[2])+'+'+group(pieces[3])+' ')
  ev=vec(tex(d['ev'][0]),tex(d['ev'][1])+' ')
  return general,sub,mid,ev
 if t=='tangent':
  H=H.replace(r'\pi}',r'\pi }');K=K.replace(r'\pi}',r'\pi }')
  general=vec(str(a)+r'\operatorname{tan}⁡y-'+str(a)+r'y{sec}^{2}⁡x',str(a)+r'x{sec}^{2}⁡y-'+str(a)+r'\operatorname{tan}⁡x',True)
  sub=vec(str(a)+r'\operatorname{tan}⁡('+H+')-'+str(a)+r'\cdot '+group(k)+r'\cdot {sec}^{2}⁡('+H+')',str(a)+r'\cdot '+group(h)+r'\cdot {sec}^{2}⁡('+K+')-'+str(a)+r'\operatorname{tan}⁡('+H+')',True)
  mid=vec(str(a)+r'\cdot '+group(S.tan(k))+'-'+group(a*k)+r'\cdot 2',tex(a*h)+r'\cdot 2-'+str(a)+r'\cdot '+group(S.tan(h)))
  EA,EB=tangent_evaluated(p,d);ev=vec(EA+' ',EB,True)
  return general,sub.replace(r'\pi}',r'\pi }'),mid.replace(r'\pi}',r'\pi }'),ev.replace(r'\pi-',r'\pi -')
 if t=='exp_bilinear':
  exponent=str(b)+'x-y';general='-('+str(a)+'y+'+str(b)+r'{e}^{'+exponent+r'})\text{ }i-('+str(a)+r'x-{e}^{'+exponent+r'})\text{ }j'
  exponent_eval=str(b)+r'\cdot '+group(h)+'-'+group(k)
  sub='-('+str(a)+r'\cdot '+group(k)+'+'+str(b)+r'\cdot {e}^{'+exponent_eval+r'})\text{ }i-('+str(a)+r'\cdot '+group(h)+r'-{e}^{'+exponent_eval+r'})\text{ }j'
  ev=tex(-d['ev'][0])+r'\text{ }i'+('-' if d['ev'][1]>0 else '+')+('' if abs(d['ev'][1])==1 else tex(abs(d['ev'][1])))+r'\text{ }j'
  return general,sub,None,ev
 if t=='sumlog':
  s=mult(a,'x')+'+'+mult(b,'y');L=r'(\operatorname{ln}⁡('+s+')+1)'
  # Raw source has its missing leading negatives. Normal output repairs this row.
  general=mult(a,L)+r'\text{ }i+'+mult(b,L)+r'\text{ }j'
  arg=(group(h) if a==1 else str(a)+r'\cdot '+group(h))+('+' if k>=0 else '-')+(tex(abs(k)) if b==1 else str(b)+r'\cdot '+tex(abs(k)))
  sub='-'+mult(a,r'(\operatorname{ln}⁡('+arg+r')+1)i')+'-'+mult(b,r'(\operatorname{ln}⁡('+arg+r')+1)j')
  ev='-'+('' if a==1 else str(a))+'i-'+('' if b==1 else str(b))+'j'
  return general,sub,None,ev
 # Unrated source solutions missing: these families use explicitly authored stages.
 return None

def replace_slots(text,slots):
 return re.sub('|'.join(re.escape(k) for k in sorted(slots,key=len,reverse=True)),lambda m:slots[m[0]],text)

def source_solution(t,p,d):
 sid=FAMILY_SOURCE[t];old=SOURCES[sid].get(':question/worked-solution')
 if old is None:return None
 ap=parameters(t,ANCHORS[sid][1]);ad=data(t,ap);oldrows=derivative_rows(t,ap,ad);newrows=derivative_rows(t,p,d)
 slots={function_tex(t,ap):function_tex(t,p),point_tex(t,ap,ad):point_tex(t,p,d)}
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',old,re.S)
 derivative_block=blocks[1] if d['v'] else blocks[0]
 actual_rows=[z.split('& =',1)[1].strip() for z in derivative_block.split(chr(92)*2)]
 operative=[actual_rows[1],actual_rows[2],actual_rows[3] if len(actual_rows)==5 else None,actual_rows[-1]]
 for f,g in zip(operative,newrows):
  if f is not None:slots[f]=g
 if d['v']:
  # Normalization slots use the displayed source's actual primitive direction.
  # q83608 cancels common scale 2 before dotting; other source directions primitive.
  v=d['v'];norm=d['vn'];u=d['u'];ov=ad['v'];on=ad['vn'];ou=ad['u']
  oldnorm={'ratio_sum':r'\sqrt{{1}^{2}+(-\sqrt{2})^{2}}=\sqrt{3}', 'sine_quotient':r'\sqrt{(-2)^{2}+{2}^{2}}=2\sqrt{2}','tangent':r'\sqrt{(-1)^{2}+{1}^{2}}=\sqrt{2}'}[t]
  newnorm=r'\sqrt{'+(('('+tex(v[0])+')^{2}') if v[0]<0 else bracepow(v[0]))+'+'+(('('+tex(v[1])+')^{2}') if v[1]<0 else bracepow(v[1]))+'}='+tex(norm)
  slots[oldnorm]=newnorm
  # Represent normalized vector as source style reciprocal norm times primitive vector.
  common=S.gcd(v[0],v[1]) if all(z.is_Integer for z in v) else S.Integer(1);common=abs(common)
  pv=tuple(z/common for z in v);pn=S.simplify(norm/common)
  slots[frac('1',tex(on/(2 if t=='sine_quotient' else 1)))+vec(*map(tex,((-1,1) if t=='sine_quotient' else ov)))]=frac('1',tex(pn))+vec(*map(tex,pv))
  slots[vec(tex(ou[0]),tex(ou[1]))]=vec(tex(u[0]),tex(u[1]))
  if t in ('sine_quotient','tangent'):
   dotblock=blocks[2];dotrows=dotblock.split(chr(92)*2)
   olddotvectors=re.findall('⟨[^⟩]+⟩',dotrows[1])
   slots[olddotvectors[0]]=vec(tex(d['ev'][0]),tex(d['ev'][1])+' ') if t=='sine_quotient' else vec(tangent_evaluated(p,d)[0]+' ',tangent_evaluated(p,d)[1])
   if t=='tangent':slots[olddotvectors[0]]=slots[olddotvectors[0]].replace(r'\pi-',r'\pi -')
   def component(z):return ('-' if z<0 else '')+frac(tex(abs(z)),tex(pn))
   slots[olddotvectors[1]]=vec(component(pv[0]),component(pv[1]))
  if t=='ratio_sum':oldnum=r'\frac{0(1)+0(-\sqrt{2})}{\sqrt{3}}'
  elif t=='sine_quotient':oldnum=r'\frac{0\cdot (-1)+\pi \cdot 1}{\sqrt{2}}'
  else:oldnum=r'\frac{(2-\pi )\cdot (-1)+(\pi -2)\cdot 1}{\sqrt{2}}'
  E=d['ev'];numericnum=(group(E[0])+'('+tex(pv[0])+')+'+group(E[1])+'('+tex(pv[1])+')') if t=='ratio_sum' else '('+tex(E[0])+r')\cdot ('+tex(pv[0])+')+('+tex(E[1])+r')\cdot ('+tex(pv[1])+')'
  if t=='sine_quotient':numericnum=group(E[0])+r'\cdot '+group(pv[0])+'+'+tex(E[1])+r' \cdot '+group(pv[1])
  if t=='tangent':numericnum='('+tangent_evaluated(p,d)[0]+r' )\cdot '+group(pv[0])+'+('+tangent_evaluated(p,d)[1]+r')\cdot '+group(pv[1])
  slots[oldnum]=frac(numericnum.replace(r'\pi-',r'\pi -'),tex(pn))
  if t=='sine_quotient':slots[r'\frac{\pi }{\sqrt{2}}']=frac(tex(S.simplify(E[0]*pv[0]+E[1]*pv[1]))+' ',tex(pn))
  elif t=='tangent':
   slots[r'\frac{2\pi -4}{\sqrt{2}}']=frac(tex(S.expand(E[0]*pv[0]+E[1]*pv[1])).replace(r'-4 + 2 \pi',r'2\pi -4'),tex(pn));slots[r'\sqrt{2}(\pi -2)']=tex(d['answer']).replace(r'\sqrt{2} (-2 + \pi)',r'\sqrt{2}(\pi -2)')
  # Source final 0 row must be a full-row slot; never substitute bare zero.
  elif t=='ratio_sum':slots[' & =0.']= ' & ='+tex(d['answer'])+'.'
 else:
  # Preserve the norm/individual squares/final collected stages of the source.
  oldsquare={'exp_bilinear':r'\sqrt{(-9)^{2}+(-1)^{2}}','sumlog':r'\sqrt{(-1)^{2}+(-1)^{2}}'}[t]
  slots[oldsquare]=r'\sqrt{('+tex(-d['ev'][0])+')^{2}+('+tex(-d['ev'][1])+')^{2}}'
  slots[tex(ad['norm'])+'.']=tex(d['norm'])+'.'
 return replace_slots(old,slots)

def authored_solution(t,p,d):
 P=point_tex(t,p,d);F=function_tex(t,p);h,k=d['h'],d['k'];E=d['ev']
 if t=='quotient':
  C=str(p['c']);formal=vec(frac(r'∂','∂x')+'('+F+')',frac(r'∂','∂y')+'('+F+')',True)
  general=vec(frac(mult(2*p['c'],'x'),'y'),'-'+frac(mult(p['c'],'x^{2}'),'y^{2}'),True)
  sub=vec(frac(C+r'\cdot 2\cdot '+group(h),group(k)),'-'+frac(C+r'\cdot '+bracepow(h),bracepow(k)),True)
  gradient=r'\begin{aligned}∇g(x,y) & ='+formal+r' \\ & ='+general+r' \\ ∇g('+P+r') & ='+sub+r' \\ & ='+vec(*map(tex,E))+r'\end{aligned}'
  norm=r'\begin{aligned}‖v‖ & =\sqrt{'+bracepow(d['v'][0])+'+'+bracepow(d['v'][1])+'}='+tex(d['vn'])+r' \\ u & ='+frac('1',tex(d['vn']))+vec(*map(tex,d['v']))+r'\end{aligned}'
  dot=r'\begin{aligned}{g}_{u}^{′}('+P+r') & =∇g('+P+r')\cdot u \\ & ='+vec(*map(tex,E))+r'\cdot '+vec(*map(tex,d['u']))+r' \\ & ='+frac(group(E[0])+r'\cdot '+group(d['v'][0])+'+'+group(E[1])+r'\cdot '+group(d['v'][1]),tex(d['vn']))+r' \\ & ='+tex(d['answer'])+r'.\end{aligned}'
  return 'The rate of change of $g(x,y)$ at the point $('+P+')$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}('+P+').$\n\nFirst, we find the unit vector $u$ in the direction of $v:$\n\n$$\n'+norm+'\n$$\n\nNow, we find the gradient $∇g(x,y)$ and evaluate it at the point $('+P+'):$\n\n$$\n'+gradient+'\n$$\n\nFinally, the directional derivative ${g}_{u}^{′}('+P+')$ is\n\n$$\n'+dot+'\n$$'
 if t=='sinlog':
  c=p['c'];H,K=tex(h),tex(k)
  formal=vec(frac('∂','∂x')+'('+F+')',frac('∂','∂y')+'('+F+')',True)
  general=vec(mult(c,r'\cos(y\ln x)')+r'\cdot '+frac('y','x'),mult(c,r'\cos(y\ln x)')+r'\cdot \ln x',True)
  sub=vec(mult(c,r'\cos('+K+r'\ln ('+H+')'+')')+r'\cdot '+frac(K,H),mult(c,r'\cos('+K+r'\ln ('+H+')'+')')+r'\cdot \ln ('+H+')',True)
  return 'At a given point, a function $g(x,y)$ increases most rapidly in the direction of its gradient at that point.\n\nIn our case, we compute $∇g(x,y)$ and evaluate it at the point $('+P+'):$\n\n$$\n'+r'\begin{aligned}∇g(x,y) & ='+formal+r' \\ & ='+general+r' \\ ∇g('+P+r') & ='+sub+r' \\ & ='+vec(*map(tex,E))+r'\end{aligned}'+'\n$$\n\nFinally, the rate of change of $g(x,y)$ at the point $('+P+')$ in the direction of $∇g('+P+')$ is given by\n\n$$\n'+r'\begin{aligned}‖∇g('+P+r')‖ & =‖'+vec(*map(tex,E))+r'‖ \\ & =\sqrt{'+bracepow(E[0])+'+'+bracepow(E[1])+'}'+r' \\ & ='+tex(d['answer'])+r'.\end{aligned}'+'\n$$'
 sol=source_solution(t,p,d)
 if t in ('exp_bilinear','sumlog'):
  if t=='sumlog':
   general=derivative_rows(t,p,d)[0];sol=sol.replace(' & ='+general,' & =-'+general.replace(r'\text{ }i+',r'\text{ }i-'))
  # The source norm is positive and useful; change its prose purpose and append signed conclusion.
  start='Finally, the rate of change of $f(x,y)$ at the point $('+P+')$ in the direction of $-∇f('+P+')$ is given by'
  sol=sol.replace(start,'Finally, the norm of $-∇f('+P+')$ is')
  sol+='\n\nTherefore, the signed rate of change of $f(x,y)$ at the point $('+P+')$ in the direction in which the function decreases most rapidly is $'+tex(d['answer'])+'.$'
 return sol

# Complete banks selected before parameter sampling; opaque historical recipes are
# explicit evidence profiles. These formulas reproduce numerical values without
# claiming to recover the unknown original author's cognitive error intentions.
def bank(t,p,d,historical=False):
 E=d['ev'];A,B=E;v=d['v'];correct=d['answer'];norm=d['norm']
 if historical:
  if t=='quotient':
   vals=[d['v'][0]/d['vn'],p['k'],E[0]**2+p['k']**2,correct,p['h']/S.sqrt(p['h']**2+p['k']**2)]
   return vals,[tex(z) for z in vals]
  if t=='sinlog':
   H,K=d['h'],d['k'];vals=[S.sqrt(K+H)/H,S.sqrt((K+H)/H),S.sqrt(K*K+H*H)/H,S.sqrt(K**4+H*H)/K,S.sqrt(K*K+H*H)/K]
   kt=tex(K) if K==S.pi else '('+tex(K)+')';ht=tex(H) if H==S.E else '('+tex(H)+')'
   out=[frac(r'\sqrt{'+tex(K)+' + '+tex(H)+'}',tex(H)),r'\sqrt{'+frac(tex(K)+' + '+tex(H),tex(H))+'}',frac(r'\sqrt{'+kt+'^{2} + '+ht+'^{2}}',tex(H)),frac(r'\sqrt{'+kt+'^{4} + '+ht+'^{2}}',tex(K)),frac(r'\sqrt{'+kt+'^{2} + '+ht+'^{2}}',tex(K))]
   if p['n']==p['j']==1:out=[z.replace(r'\pi','π') for z in out]
   return vals,out
  if t=='ratio_sum':vals=[abs(v[1]),d['vn'],v[1]**2,d['vn']**2,correct];return vals,[tex(z) for z in vals]
  if t=='sine_quotient':
   vals=[2*correct,correct,-2*B,-correct,B/2]
   out=[tex(vals[0]),frac(tex(B)+' ',tex(S.sqrt(2))) if v[0]==-v[1] and A==0 else tex(correct),tex(vals[2])+' ',('-'+frac(tex(B)+' ',tex(S.sqrt(2)))) if v[0]==-v[1] and A==0 else tex(-correct),frac(tex(B)+' ','2')]
   return vals,out
  if t=='tangent':
   a=p['a'];z=2*p['h'];zabs=abs(z);direction=1 if d['answer']>0 else -1
   vals=[correct,S.simplify(A*v[0]+B*v[1]),a*zabs-a/S.sqrt(2),2*a*(zabs+1),S.sqrt(2)*a*(zabs+1)]
   out=[tex(correct),tex(vals[1]),tex(vals[2]),tex(vals[3]),tex(vals[4])]
   # Structural historical expressions retain factorization; source pi/4 values are
   # components of these formulas, not an answer lookup table.
   if p['h']==S.pi/4:
    out=[tex(a/S.sqrt(2))+r'(\pi -2)',tex(a*p['v2'])+r'(\pi -2)',tex(a/2)+r'\pi -'+tex(a/S.sqrt(2)),tex(a)+r'(\pi +2)',tex(a/S.sqrt(2))+r'(\pi +2)'];out[2]=out[2].replace('1'+r'\pi',r'\pi')
   return vals,out
  if t=='exp_bilinear':
   vals=[S.sqrt(A+B),S.sqrt(A-B),S.sqrt(A*A-B*B),A,norm]
   return vals,[r'\sqrt{'+tex(A+B)+'}',r'\sqrt{'+tex(A-B)+'}',r'\sqrt{'+tex(A*A-B*B)+'}',tex(A),r'\sqrt{'+tex(A*A+B*B)+'}']
  if t=='sumlog':
   vals=[2*norm,S.sqrt(sum(E)+1),abs(A),norm,A+B]
   return vals,[tex(vals[0]).replace(' ',''),r'\sqrt{'+tex(sum(E)+1)+'}',tex(vals[2]),tex(norm),tex(vals[4])]
 if t=='quotient':
  dot=lambda aa,bb:S.simplify((aa*v[0]+bb*v[1])/d['vn'])
  vals=[correct,dot(-A,B),dot(A,-B),A*v[0]+B*v[1],dot(A,-p['c']*p['h']/p['k']**2)]
 elif t=='ratio_sum':
  dot=lambda aa,bb:S.simplify((aa*v[0]+bb*v[1])/d['vn'])
  vals=[correct,dot(1/p['k']+p['k']/p['h']**2,B),dot(A,1/p['h']+p['h']/p['k']**2),dot(1/p['k']+p['k']/p['h']**2,1/p['h']+p['h']/p['k']**2),d['vn']]
 elif t=='sine_quotient':
  dot=lambda aa,bb:S.simplify((aa*v[0]+bb*v[1])/d['vn'])
  vals=[correct,A*v[0]+B*v[1],-correct,dot(p['b']*S.pi*p['k'],B),(A*v[0]+B*v[1])/d['vn']**2]
 elif t=='tangent':
  dot=lambda aa,bb:S.simplify((aa*v[0]+bb*v[1])/d['vn']);a=p['a'];h,k=p['h'],p['k']
  vals=[correct,A*v[0]+B*v[1],-correct,dot(a*S.tan(k),-a*S.tan(h)),dot(-2*a*k,2*a*h)]
 elif t=='exp_bilinear':
  a,b,h=p['a'],p['b'],p['h'];k=d['k'];vals=[correct,norm,-S.sqrt((a*k+1)**2+(a*h-1)**2),-S.sqrt(b*b+1),-abs(A)]
 elif t=='sumlog':vals=[correct,norm,S.Integer(0),-abs(A),-(A+B)]
 else:
  c=p['c'];H,K=d['h'],d['k'];n=p['n'];vals=[correct,c*S.sqrt(K*K+n*n),c*S.sqrt((K/H)**2+H*H),abs(A)+abs(B),abs(A)]
 vals=[S.simplify(z) for z in vals]
 return vals,[tex(z) for z in vals]

# Source spelling masks for banks are numerical-operation slots; raw TeX bytes are
# preserved by retaining source formatting at the family anchor and generalizing
# complete scalar/radical components rather than returning the original payload.
def raw_bank(t,p,d):
 vals,strings=bank(t,p,d,True)
 if t=='quotient':
  strings=[tex(z).replace(' ', '') for z in vals]
  # SymPy's rationalized rendering matches all original quotient choices.
 if t=='sine_quotient':
  strings[0]=tex(vals[0]).replace(r'\sqrt{2} \pi',r'\pi \sqrt{2}');strings[2]=strings[2].replace(' ','').replace(r'\pi',r'\pi ')
 # Decoded source inspection confirms single backslashes in all answer values.
 return vals,strings

# Easy: authored placement of unrated elementary quotient, c=1..4, positive 1..5.
def sample(t,r):
 if t=='quotient':return dict(c=r.randint(1,4),h=r.randint(1,5),k=r.randint(1,5),v1=r.choice([-3,-2,-1,1,2,3]),v2=r.choice([-3,-2,-1,1,2,3]))
 # Moderate: distinct quotient/trigonometric partial rules and source dot sequence.
 if t=='ratio_sum':return dict(h=r.choice([-5,-4,-3,-2,-1,1,2,3,4,5]),k=r.choice([-5,-4,-3,-2,-1,1,2,3,4,5]),v1=r.choice([-3,-2,-1,1,2,3]),v2=r.choice([-3,-2,-1,1,2,3]))
 if t=='sine_quotient':return dict(a=r.randint(1,4),b=r.randint(1,4),h=r.randint(1,5),k=r.randint(1,5),v1=r.choice([-3,-2,-1,1,2,3]),v2=r.choice([-3,-2,-1,1,2,3]))
 if t=='tangent':h=r.choice(['pi/4','-pi/4']);return dict(a=r.randint(1,6),h=h,k=h,v1=r.choice([-3,-2,-1,1,2,3]),v2=r.choice([-3,-2,-1,1,2,3]))
 # Hard: source-grounded composite rules; exact familiar evaluations, no new branch.
 if t=='exp_bilinear':
  a,b,h=r.choice([(a,b,h) for a in range(2,7) for b in range(2,6) for h in range(1,5) if a*b*h+b<=30 and a*h-1<=12]);return dict(a=a,b=b,h=h)
 if t=='sumlog':return dict(a=r.randint(1,8),b=r.randint(1,8),h=r.randint(1,4))
 return dict(c=r.randint(1,4),n=r.randint(1,4),j=r.randint(1,4))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only source radio layout supported')
 r=random.Random(seed);choices=[t for t,l in TEMPLATES.items() if l==level]
 profile_family=next((name for name,s in FAMILY_SOURCE.items() if profile in ('raw-'+s,'completed-'+s)),None)
 t=template or profile_family or r.choice(choices)
 if t not in choices:raise ValueError('template level mismatch')
 sid=FAMILY_SOURCE[t];profile=profile or 'authored-operations'
 raw=profile=='raw-'+sid;completed=profile=='completed-'+sid
 if profile not in ('authored-operations','raw-'+sid,'completed-'+sid):raise ValueError('profile belongs to another family')
 for attempt in range(1000):
  candidate=parameters if parameters is not None else sample(t,r)
  if parameters is None and (raw or completed):
   if t=='sinlog':candidate.update(c=1,n=1)
   if t=='tangent':candidate.update(h='pi/4',k='pi/4',v1=-1,v2=1)
  p=globals()['parameters'](t,candidate);d=data(t,p)
  if (raw or completed) and t=='sinlog' and (p['c']!=1 or p['n']!=1):raise ValueError('historical sinlog bank requires unit coefficient and x=e')
  if (raw or completed) and t=='tangent' and (p['h']!=S.pi/4 or p['v1']!=-p['v2'] or p['v2']<=0):raise ValueError('historical tangent profile uses positive quarter-pi and (-s,s) direction')
  if raw or completed:vals,strings=raw_bank(t,p,d)
  else:vals,strings=bank(t,p,d)
  if any(z.has(S.zoo,S.oo,S.nan) or not z.is_real for z in vals):bad=True
  else:bad=any(S.simplify(a-b)==0 for i,a in enumerate(vals) for b in vals[:i])
  # Raw profiles preserve documented errors, never hide missing keys or false rate.
  expected=d['norm'] if (raw or completed) and t in ('exp_bilinear','sumlog') else d['answer']
  matches=[i for i,z in enumerate(vals) if S.simplify(z-expected)==0]
  if len(matches)!=1:bad=True
  if not bad:break
  if parameters is not None:raise ValueError('complete bank invalid/ambiguous at explicit parameters')
 else:raise ValueError('no eligible complete bank')
 problem=prompt(t,p,d);solution=source_solution(t,p,d) if raw else authored_solution(t,p,d)
 if completed:
  # Historical complete bank keeps source errors, and is still ineligible evidence.
  strings=[s.replace('\\\\','\\') for s in strings]
 else:
  if not raw:strings=[s.replace('\\\\','\\') for s in strings]
 original=SOURCES[sid]
 if not raw and t in ('exp_bilinear','sumlog') and completed:
  # Replace the historical wrong positive correct scalar with its negative; this
  # is the separately documented minimal mathematical bank repair.
  ci=matches[0];vals[ci]=d['answer'];strings[ci]=tex(d['answer'])
 if not raw and solution is None:solution=authored_solution(t,p,d)
 q={':question/problem':problem}
 if not raw or ':question/difficulty' in original:q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 content=dict(version=VERSION,level=q.get(':question/difficulty'),problem=problem,solution=solution,bank=sorted(strings),field_type='radio',correct_present=(not raw or ':answer-field/correct' in original[':question/answer-fields'][0]))
 content['correct_value']=strings[matches[0]] if content['correct_present'] else None
 ident=digest(content);fid=uid(ident+'/selection')
 answers=[{':answer/id':uid(ident+'/selection/'+s),':answer/type':':answer.type/math',':answer/value':s} for s in strings]
 correct_id=answers[matches[0]][':answer/id'];r.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if not raw or ':answer-field/correct' in original[':question/answer-fields'][0]:field[':answer-field/correct']=[':answer/id',correct_id]
 q[':question/answer-fields']=[field];q[':question/id']=uid(ident)
 direction=None if d['v'] is None else [S.sstr(S.simplify(z/d['vn'])) for z in d['v']]
 assessed_point=[S.sstr(S.simplify(p['a']*d['h']+p['b']*d['k']))] if t=='sumlog' else [S.sstr(d['h']),S.sstr(d['k'])]
 task={'function':S.sstr(d['F']),'point':assessed_point,'direction':direction,'criterion':'given-vector' if direction else ('maximum-increase' if t=='sinlog' else 'maximum-decrease')}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'bank_profile':profile,'parameters':{k:S.sstr(v) for k,v in p.items()},'source_refs':[sid],'provenance':{k:v for k,v in CAPTURE.items() if k!='record'},'evidence_only':raw or completed,'eligible_for_learning':not(raw or completed),'source_difficulty_origin':'authored unrated assignment' if ':question/difficulty' not in original else 'observed','solution_origin':'authored missing solution' if ':question/worked-solution' not in original else ('raw observed' if raw else 'parameterized observed sequence with documented repairs'),'mathematical_fingerprint':digest(task),'content_identity':ident,'correct_scalar':S.sstr(d['answer']),'runtime':{'python':sys.version.split()[0],'sympy':S.__version__},'domain':'denominators nonzero; log argument positive; familiar trig points; displayed coefficients bounded','bank_interpretation':'opaque historical scalar shapes; evidence only' if raw or completed else 'complete family-specific operation errors'}}

# Easy — authored assignment of the unrated elementary quotient source.
def generate_easy(seed=0,**kw):
 """c*x^2/y: two elementary partials, positive integer point, vector normalization."""
 return generate('easy',seed,**kw)

# Moderate — all three observed families, equal-level alternatives.
def generate_moderate(seed=0,**kw):
 """Reciprocal sums or familiar sine/tangent partials, substitution, normalized dot."""
 return generate('moderate',seed,**kw)

# Hard — observed exponential/product-log plus authored unrated sine-log assignment.
def generate_hard(seed=0,**kw):
 """Composite partials at familiar exact inputs, then maximum/minimum signed rate."""
 return generate('hard',seed,**kw)
def markdown(rec):
 q=rec['question'];s=q[':question/problem']+'\n\n';f=q[':question/answer-fields'][0]
 for i,a in enumerate(f[':answer-field/choices']):s+=f'{chr(65+i)}. $'+a[':answer/value']+'$\n\n'
 return s+q.get(':question/worked-solution','[No observed worked solution.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 selected_template=args.template or next((t for t,s in FAMILY_SOURCE.items() if args.profile in ('raw-'+s,'completed-'+s)),None)
 levels=[TEMPLATES[selected_template]] if args.difficulty=='all' and selected_template else ['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 out=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(out,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in out))
