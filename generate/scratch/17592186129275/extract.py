"""One-time extraction of complete radius slots; source snapshot remains untouched."""
import json,re,pathlib,copy
B=pathlib.Path(__file__).parent
P=json.loads((B/'source.json').read_text())['record']
configs=[
('difference','moderate','x',1,'full','3',4),('xsqrt','hard','x',1,'upper','1',4),
('linear','moderate','y',1,'full','1',3),('x2y','moderate','x',1,'full','2',2),
('expdiff','hard','x',1,'lower','4',0),('sqrt','hard','y',1,'right','2',2),
('xy2','hard','x',-1,'lower','1/2',4),('radial2','hard','y',1,'left','1/2',0),('log','hard','x',1,'lower','1',2)]
# Complete mathematical operation tuples: angular endpoints (multiples of pi), lower r, upper r, density.
ops=[
[('-1/2','1/2','0','2*a*cos(t)','r**2*cos(2*t)'),('-1/2','1/2','0','a','r**3'),('0','2','0','2*a*cos(t)','r**3'),('0','2','0','a','r**3*cos(2*t)'),('-1/2','1/2','0','2*a*cos(t)','r**3*cos(2*t)')],
[('0','1','0','2*a*cos(t)','r**3*cos(t)'),('0','1','0','2*a*cos(t)','r**2*cos(t)'),('0','1/2','0','a','r**2*cos(t)'),('0','1/2','0','a','r*cos(t)'),('0','1/2','0','2*a*cos(t)','r**3*cos(t)')],
[('0','2','0','2*a*cos(t)','r*sin(t)'),('0','2','0','2*a*sin(t)','r**2*sin(t)'),('0','1','0','2*a*sin(t)','r*cos(t)'),('0','1','0','2*a*sin(t)','r**2*cos(t)'),('0','1','0','2*a*cos(t)','r**2*cos(t)')],
[('0','2','0','a','r**4*cos(t)**2*sin(t)'),('-1/2','1/2','0','a','r**3*cos(t)**2*sin(t)'),('-1/2','1/2','0','2*a*cos(t)','r**4*cos(t)**2*sin(t)'),('0','2','0','2*a*cos(t)','r**4*cos(t)**2*sin(t)'),('-1/2','1/2','0','2*a*cos(t)','r**3*cos(t)**2*sin(t)')],
[('3/2','2','0','2*a*cos(t)','r*exp(r**2*cos(2*t))'),('3/2','2','0','a','r*exp(r**2*cos(2*t))'),('3/2','2','0','2*a*cos(t)','exp(r**2)'),('0','2','0','2*a*cos(t)','exp(r**2*cos(2*t))'),('0','2','0','a','r*exp(r**2)')],
[('0','1/2','0','2*a*sin(t)','r'),('0','1','0','2*a*sin(t)','r**2'),('0','1/2','0','2*a*sin(t)','r**2'),('0','1/2','0','a*sin(t)','r**2'),('0','1','0','a*sin(t)','r**3')],
[('0','1/2','2*a','4*a*sin(t)','r**4*cos(t)*sin(t)**2'),('0','1','2*a/cos(t)','4*a*sin(t)','r**3*cos(t)*sin(t)**2'),('0','1','0','2*a*sin(t)','r**4*cos(t)*sin(t)'),('0','1/2','2*a','-2*a*cos(t)','r**2*cos(t)*sin(t)'),('1','3/2','0','-2*a*cos(t)','r**4*cos(t)*sin(t)**2')],
[('1/2','1','0','2*a*sin(t)','r**3'),('0','1','0','2*a*sin(t)','r**2'),('-1/2','1','0','2*a*sin(t)','r**3'),('1/2','3/2','0','2*a*sin(t)','r'),('1','2','0','2*a*sin(t)','r**2')],
[('-1','0','0','2*a*cos(t)','2*r*log(r+1)'),('0','1','0','a*cos(t)','r**2*log(r+1)'),('-1/2','0','0','2*a*cos(t)','r*log(r**2+1)'),('0','1/2','0','a*cos(t)','log(r**2+1)'),('-1/2','1/2','0','2*a*cos(t)','r*log(r**2)')]
]
T={}; cases=[]
for q,c,op in zip(P[':knowledge-point/questions'],configs,ops):
 name,level,axis,sign,part,a,correct=c
 from fractions import Fraction
 v=Fraction(a); av=str(v.numerator) if v.denominator==1 else r'\frac{'+str(v.numerator)+'}{'+str(v.denominator)+'}'
 b=2*v; bv='' if b==1 else str(b.numerator) if b.denominator==1 else r'\frac{'+str(b.numerator)+'}{'+str(b.denominator)+'}'
 sq=v*v; sv=str(sq.numerator) if sq.denominator==1 else r'\frac{'+str(sq.numerator)+'}{'+str(sq.denominator)+'}'
 def bankslot(s):
  # Replace entire radial bounds only, never powers, angles or function arguments.
  s=s.replace('\\int_{0}^{'+bv+'\\cos', '\\int_{0}^{@@B@@\\cos').replace('\\int_{0}^{'+av+'}', '\\int_{0}^{@@A@@}')
  for tr in ('cos','sin'):
   s=s.replace('{0}^{'+bv+'\\operatorname{'+tr+'}', '{0}^{@@B@@\\operatorname{'+tr+'}')
  s=s.replace('{0}^{'+av+'}', '{0}^{@@A@@}')
  if name=='sqrt':s=s.replace('{0}^{2\\operatorname{sin}', '{0}^{@@A@@\\operatorname{sin}')
  if name in ('xy2','radial2'):
   s=s.replace('{0}^{-\\operatorname{cos}', '{0}^{-@@B@@\\operatorname{cos}').replace('{1}^{-\\operatorname{cos}', '{@@Bfull@@}^{-@@B@@\\operatorname{cos}')
   s=s.replace('{0}^{\\operatorname{sin}', '{0}^{@@B@@\\operatorname{sin}')
   s=s.replace('{1}^{2\\operatorname{sin}', '{@@Bfull@@}^{@@FourA@@\\operatorname{sin}').replace('{\\operatorname{sec}⁡\\theta }^{2\\operatorname{sin}', '{@@B@@\\operatorname{sec}⁡\\theta }^{@@FourA@@\\operatorname{sin}')
  if name=='log':s=s.replace('{0}^{\\operatorname{cos}', '{0}^{@@Acoef@@\\operatorname{cos}')
  return s
 bank=[]
 for ch,operation in zip(q[':question/answer-fields'][0][':answer-field/choices'],op):
  raw=ch[':answer/value']; repaired=raw.replace('\\\\','\\') if name in ('difference','xsqrt') else raw
  bank.append({'raw':raw,'mask':bankslot(repaired),'operation':operation})
 s=q.get(':question/worked-solution')
 if s:
  # Restrict numeric geometry slotting to the geometry section; final integrands are fixed.
  head,tail=s.split('Therefore, using the change of variables formula, we obtain ',1)
  head=head.replace('radius $'+av+'$', 'radius $@@A@@$')
  for coord in ['(0,'+av+')','('+av+',0)','(-'+av+',0)']:
   head=head.replace(coord,coord.replace(av,'@@A@@'))
  # All shift components have full coordinate/function prefixes.
  for var in ('x','y',r'r\operatorname{cos}⁡\theta ',r'r\operatorname{sin}⁡\theta '):
   for sg in ('-','+'):
    prefix='(' if var.startswith('r') else ''
    head=head.replace(prefix+var+sg+av,prefix+var+sg+'@@A@@')
  head=head.replace(' & ='+sv,' & =@@A2@@').replace('}='+sv,'}=@@A2@@').replace('='+sv+'$', '=@@A2@@$')
  head=head.replace('+'+sv+'+', '+@@A2@@+').replace('+'+sv+' &', '+@@A2@@ &')
  # Full r-factor terms; these do not include coordinate squares or angle endpoints.
  for tr in ('cos','sin'):
   for sg in ('-', '+'):
    head=head.replace(sg+bv+'r\\operatorname{'+tr+'}', sg+'@@B@@r\\operatorname{'+tr+'}')
   if bv:
    head=head.replace(bv+'\\operatorname{'+tr+'}', '@@B@@\\operatorname{'+tr+'}')
   else:
    head=head.replace('r(r-\\operatorname{'+tr+'}', 'r(r-@@B@@\\operatorname{'+tr+'}').replace('r(r+\\operatorname{'+tr+'}', 'r(r+@@B@@\\operatorname{'+tr+'}')
    head=head.replace('r=-\\operatorname{'+tr+'}', 'r=-@@B@@\\operatorname{'+tr+'}').replace('r=\\operatorname{'+tr+'}', 'r=@@B@@\\operatorname{'+tr+'}').replace('r\\le -\\operatorname{'+tr+'}', 'r\\le -@@B@@\\operatorname{'+tr+'}').replace('r\\le \\operatorname{'+tr+'}', 'r\\le @@B@@\\operatorname{'+tr+'}')
   tail=tail.replace('{0}^{'+bv+'\\operatorname{'+tr+'}', '{0}^{@@B@@\\operatorname{'+tr+'}').replace('{0}^{-'+bv+'\\operatorname{'+tr+'}', '{0}^{-@@B@@\\operatorname{'+tr+'}')
  s=head+'Therefore, using the change of variables formula, we obtain '+tail
 T[name]={'level':level,'axis':axis,'sign':sign,'part':part,'original_a':a,'correct':correct,'source_id':q[':db/id'],'question_id':q[':question/id'],'raw_prompt':q[':question/problem'],'solution_mask':s,'bank':bank}
 cases.append({'source_id':q[':db/id'],'template':name,'level':level,'parameters':{'a':a},'bank_profile':'observed','observed_difficulty':q.get(':question/difficulty'),'correct_designation_observed':':answer-field/correct' in q[':question/answer-fields'][0]})
(B/'templates.json').write_text(json.dumps(T,ensure_ascii=False,indent=2))
(B/'source-cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2))
