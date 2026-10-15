"""Parameterized source chains, keeping each original family’s operative stages."""
def family_solution(g,t,u,v,target,scale):
 s,X=g.s,g.X;tex,frac,gp=g.tex,g.frac,g.gp;a=s.Integer(scale);sin,cos=s.sin(X),s.cos(X);ex=s.exp(X);ln=s.log(X);den=tex(v**2)
 rule=g.RULE;formal=g.formal(u,v);sub=g.substitution(u,v);blocks=[]
 if t in ['q-17921','q-47999']:return g.generic_solution(u,v,target)
 if t=='q-340318':
  last=frac(tex(a-3*a*X),tex(s.exp(3*X)))
  rows=[rule,formal,sub,frac(tex(s.exp(3*X)*(a-3*a*X)),den),last]
 elif t=='q-9908':
  rows=[rule,formal,sub,frac(tex(-a*sin-a*sin**2-a*cos**2),den),frac('-'+tex(a)+r'\sin x-'+tex(a)+r'(\sin^2 x+\cos^2 x)',den)]
  blocks.append(rows)
  last=frac(tex(-a),r'1+\sin x')
  rows=[frac(tex(-a*sin-a),den),frac('-'+tex(a)+r'(1+\sin x)',den),last]
 elif t in ['q-167328','q-167782','q-166075']:
  rows=[rule,formal,frac(gp(s.diff(u,X))+r'\cdot '+gp(v)+'-'+gp(u)+r'\cdot '+gp(s.diff(v,X)),r'16\sin^2 x'),frac(tex(2*a)+r'e^x(\cos x-\sin x)',r'16\sin^2 x'),frac(tex(a)+r'e^x(\cos x-\sin x)',r'8\sin^2 x')]
 elif t=='q-2385':
  rows=[rule,sub,frac(tex(-10*a*X**2*sin-20*a*X*cos),r'100x^4'),frac(r'\cancel{10x}('+tex(-a*X*sin-2*a*cos)+')',r'\cancel{10x}\cdot 10x^3'),frac(tex(-a*X*sin-2*a*cos),r'10x^3')]
 elif t=='q-340308':rows=[rule,formal,frac(tex(a)+r'\sec^2 x\cdot x-'+tex(a)+r'\tan x\cdot 1',r'x^2'),frac(tex(a)+r'x\sec^2 x-'+tex(a)+r'\tan x',r'x^2')]
 elif t=='q-340309':rows=[rule,formal,sub,frac(tex(a*sin-a*X*cos),r'\sin^2 x')]
 elif t=='q-340316':
  last=frac(tex(a)+r'\cdot 2^x[(x^2-1)\ln 2-2x]',r'(x^2-1)^2')
  rows=[rule,formal,sub,last]
 elif t=='q-47943':rows=[rule,formal,frac(tex(a*ex*cos+a*ex*sin),r'\cos^2 x'),frac(tex(a)+r'e^x(\cos x+\sin x)',r'\cos^2 x')]
 elif t=='q-47998':rows=[rule,formal,frac(tex(a*X**2*cos-2*a*X*sin),r'x^4'),frac(tex(a)+r'x(x\cos x-2\sin x)',r'x^4'),frac(tex(a*X*cos-2*a*sin),r'x^3')]
 elif t=='q-48504':
  last=frac(tex(a)+r'x(2\ln x-1)',r'\ln^2 x')
  rows=[rule,formal,sub,frac(tex(2*a*X*ln-a*X),r'\ln^2 x'),last]
 elif t=='q-48507':
  last=frac(tex(a*X*cos-a*sin),r'2x^2')
  rows=[rule,formal,sub,frac(tex(2*a)+r'(x\cos x-\sin x)',r'4x^2'),last]
 else:raise ValueError(t)
 blocks.append(rows)
 if t in ['q-167328','q-167782','q-166075']:
  text='Recall that $f(x)='+tex(u)+'$ and $h(x)='+tex(v)+'.$\n\nWe apply the quotient rule, as follows:\n\n'
 else:text='In this case, the expression for $'+('y' if target is not None else 'f(x)')+'$ is a quotient $\\frac{u(x)}{v(x)}$ with $u(x)='+tex(u)+'$ and $v(x)='+tex(v)+'.$\n\nTherefore, we apply the quotient rule as follows:\n\n'
 for i,rows in enumerate(blocks):
  if i:text+='\n\nSince $\\sin^2 x+\\cos^2 x=1$, we have\n\n'
  text+='$$\n'+r'\begin{aligned}f^{\prime}(x)&='+r'\\ &='.join(rows)+r'\end{aligned}'+'\n$$'
 if target is not None:
  import re
  ans=s.simplify(s.diff(u/v,X).subs(X,target));ts=tex(target)
  substituted=re.sub(r'(?<![A-Za-z])x(?![A-Za-z])',lambda m:'('+ts+')',last)
  if t=='q-340318':intermediate=frac(tex(a*(1-3*target)),tex(s.exp(3*target)))
  elif t=='q-9908':intermediate=frac(tex(-a),tex(1+s.sin(target)))
  elif t=='q-340316':intermediate=frac(tex(a*2**target*((target**2-1)*s.log(2)-2*target)),tex((target**2-1)**2))
  elif t=='q-48504':intermediate=frac(tex(a*target*(2*s.log(target)-1)),tex(s.log(target)**2))
  elif t=='q-48507':intermediate=frac(tex(a*target*s.cos(target)-a*s.sin(target)),tex(2*target**2))
  targetrows=[substituted,intermediate]
  if t=='q-48507':targetrows.append(frac(tex(-a*target) if s.cos(target)==-1 else tex(a*target),tex(2*target**2)))
  targetrows.append(tex(ans))
  text+='\n\nTo find the slope of the tangent line, we now substitute $x='+ts+'$ into the formula and get\n\n$$\n'+r'\begin{aligned}f^{\prime}('+ts+')&='+r'\\ &='.join(targetrows)+r'\end{aligned}'+'\n$$\n\nTherefore, the slope of the tangent line'+(' at $x='+ts+'$' if t in ['q-340318','q-340316'] else '')+' is $'+tex(ans)+'.$'
 return text
