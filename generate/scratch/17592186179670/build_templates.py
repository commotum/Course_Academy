"""Offline extraction; output contains operand masks, never question payload lookup."""
import json,re
from pathlib import Path
P=Path(__file__).parent
source=json.load(open(P/'source.json'))['record']
# Complete scalar operands and vector components. Formula symbols are parameter
# slots, not integration-variable symbols concealed by integer replacements.
def atom(formula,notation):return {'formula':formula,'notation':notation}
D={}
A={
'q-39954':('product',dict(a=1,b=2,dx=1,dy=-1,c=2)),
'q-76565':('odd_linear',dict(a=1,b=0,dx=-2,dy=0,c=2,d=-3)),
'q-123363':('radical',dict(a=2,b=0,dx=0,dy=2,k=2)),
'q-123366':('exponential',dict(a=0,b=0,dx=-1,dy=4,c=3,d=1)),
'q-76564':('product',dict(a=1,b=2,dx=3,dy=5,c=1)),
'q-76605':('secant',dict(a=1,b=1,dx=1,dy=3,n=8)),
'q-76650':('matched_exponential',dict(a=0,b=1,dx=2,dy=2))}
for q in source[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];f,p=A[sid];problem=q[':question/problem'];sol=q.get(':question/worked-solution');slots={}
 def scalar(old,formula,name=None):
  nonlocal_dummy=None
  name=name or 'v'+str(len(slots));slots[name]=atom(formula,old)
  return old,'{{'+name+'}}'
 def vec(old,formula1,formula2,name=None):
  name=name or 'v'+str(len(slots));slots[name]={'components':[formula1,formula2],'notation':old}
  return old,'{{'+name+'}}'
 maps=[]
 # Point slots are complete tuple components; independent commas remain source notation.
 sep=', ' if sid in ['q-39954','q-76565'] else ','
 oldA='('+str(p['a'])+sep+str(p['b'])+')';oldB='('+str(p['a']+p['dx'])+sep+str(p['b']+p['dy'])+')'
 maps.extend([(oldA,'{{A}}'),(oldB,'{{B}}')])
 if sid=='q-39954':maps.append(scalar('2xy','c*x*y','function'))
 if sid=='q-76565':maps.append(scalar('2x - 3y','c*x+d*y','function'))
 if sid=='q-123363':
  maps.extend([
   vec('2\\,i+2\\,j','a+dx','b+dy'),vec('2\\,i','a','b'),
   scalar('2+\\sqrt{2(2t)}','a+sqrt(k*(b+dy*t))'),scalar('2+2\\sqrt{t}','a+sqrt(k*dy)*sqrt(t)'),
   scalar('1+\\sqrt{t}','1+sqrt(k*dy)*sqrt(t)/a'),scalar('t+\\frac{2{t}^{3/2}}{3}','t+2*sqrt(k*dy)*t**(3/2)/(3*a)'),
   scalar('\\frac{20}{3}','dy*(a+2*sqrt(k*dy)/3)'),
   scalar('4(1+\\frac{2}{3})-0','dy*(a+2*sqrt(k*dy)/3)'),
   scalar('\\sqrt{{0}^{2}+{2}^{2}}','sqrt(dx**2+dy**2)'),
   scalar('2t','b+dy*t'),vec('2j','dx','dy'),scalar('x=2','a', 'x_statement')])
  # full contextual operands avoid touching bounds, exponent 2, or radical k.
  maps.extend([('x={{x_coordinate}}','x={{x_coordinate}}'),('x=2','x={{x_coordinate}}')])
  # scalar 2 at explicitly identified derivative and speed positions only.
  maps.extend([('\\text{d}t}(2)i',r'\text{d}t}({{x_coordinate}})i'),(' & =2\\end{aligned}',r' & ={{speed}}\end{aligned}'),('\\cdot 2\\cdot',r'\cdot {{speed}}\cdot'),('=4{\\int',r'={{factor}}{\int'),('=4{[',r'={{factor}}{[')])
  slots['x_coordinate']=atom('a','2');slots['speed']=atom('sqrt(dx**2+dy**2)','2');slots['factor']=atom('a*sqrt(dx**2+dy**2)','4')

  slots['radical_upper']=atom('2*sqrt(k*dy)/(3*a)',r'\frac{2}{3}')
  maps.append(('4(1+\\frac{2}{3})-0','{{factor}}(1+{{radical_upper}})-0'))
  # The fixed integrand x+sqrt(ky) varies k, so its complete occurrence is masked.
  maps.append(scalar('x+\\sqrt{2y}','x+sqrt(k*y)'))
 if sid=='q-123366':
  maps.extend([
   vec('-i+4\\,j','dx','dy'),vec('-t\\,i+4t\\,j','dx*t','dy*t'),
   scalar('{e}^{3x+y}','exp(c*x+d*y)'),scalar('{e}^{3(-t)+4t}','exp(c*(a+dx*t)+d*(b+dy*t))'),scalar('{e}^{t}','exp((c*dx+d*dy)*t)'),
   scalar('\\sqrt{(-1)^{2}+{4}^{2}}','sqrt(dx**2+dy**2)'),scalar('\\sqrt{17}','sqrt(dx**2+dy**2)'),
   scalar('e-1','(exp(c*dx+d*dy)-1)/(c*dx+d*dy)'),scalar('-t','a+dx*t'),scalar('4t','b+dy*t')])
  # Primitive e^t requires slope divisor under changed parameters. Separate
  # expression slot prevents the pulled exponential from becoming primitive.
  slots['primitive']=atom('exp((c*dx+d*dy)*t)/(c*dx+d*dy)','{e}^{t}');maps.insert(0,('[{e}^{t}]','[{{primitive}}]'))
 if sid=='q-76564':
  maps.extend([
   vec('4\\,i+7j','a+dx','b+dy'),vec('4\\,i+7\\,j','a+dx','b+dy'),vec('i+2\\,j','a','b'),vec('3i+5j','dx','dy'),
   scalar('(1+3t)(2+5t)','c*(a+dx*t)*(b+dy*t)'),scalar('15{t}^{2}+11t+2','c*(dx*dy*t**2+(a*dy+b*dx)*t+a*b)'),
   scalar('5{t}^{3}+\\frac{11}{2}{t}^{2}+2t','c*(dx*dy*t**3/3+(a*dy+b*dx)*t**2/2+a*b*t)'),
   scalar('5+\\frac{11}{2}+2','c*(dx*dy/3+(a*dy+b*dx)/2+a*b)'),
   scalar('\\frac{25\\sqrt{34}}{2}','sqrt(dx**2+dy**2)*c*(dx*dy/3+(a*dy+b*dx)/2+a*b)'),
   scalar('\\sqrt{{3}^{2}+{5}^{2}}','sqrt(dx**2+dy**2)'),scalar('\\sqrt{34}','sqrt(dx**2+dy**2)'),scalar('1+3t','a+dx*t'),scalar('2+5t','b+dy*t')])

  slots['epcube']=atom('c*dx*dy/3','5');slots['epquad']=atom('c*(a*dy+b*dx)/2',r'\frac{11}{2}');slots['epconst']=atom('c*a*b','2')
  maps.append(('5+\\frac{11}{2}+2','{{epcube}}+{{epquad}}+{{epconst}}'))
  # family integrand coefficient c has original unit coefficient.
  maps.append(scalar('xy','c*x*y'))
 if sid=='q-76605':
  maps.extend([
   vec('2\\,i+4\\,j','a+dx','b+dy'),vec('i+j','a','b'),vec('1\\,i+3\\,j','dx','dy'),vec('i+3\\,j','dx','dy'),
   scalar('{sec}^{2}⁡(\\frac{\\pi (y-x)}{8})','sec(pi*(y-x)/n)**2'),
   scalar('{sec}^{2}⁡(\\frac{\\pi ((1+3t)-(1+t))}{8})','sec(pi*((b+dy*t)-(a+dx*t))/n)**2'),
   scalar('{sec}^{2}⁡(\\frac{\\pi t}{4})','sec(pi*(dy-dx)*t/n)**2'),
   scalar('\\sqrt{{1}^{2}+{3}^{2}}','sqrt(dx**2+dy**2)'),scalar('\\sqrt{10}','sqrt(dx**2+dy**2)'),
   scalar('\\frac{4\\sqrt{10}}{\\pi }','n*sqrt(dx**2+dy**2)/(pi*(dy-dx))'),
   scalar('\\frac{\\pi t}{4}','pi*(dy-dx)*t/n'),scalar('\\frac{\\pi }{4}','pi*(dy-dx)/n'),scalar('\\pi /4','pi*(dy-dx)/n'),
   scalar('1+3t','b+dy*t'),scalar('1+t','a+dx*t')])

  slots['sec_final']=atom('n*sqrt(dx**2+dy**2)*tan(pi*(dy-dx)/n)/(pi*(dy-dx))',r'\frac{4\sqrt{10}}{\pi }')
  maps.append((r'\frac{4\sqrt{10}}{\pi }\end{aligned}','{{sec_final}}'+r'\end{aligned}'))
  # Tangent endpoint values are formula slots as well; familiar endpoint may -1.
  maps.extend([('(1-0)','({{tan_hi}}-{{tan_lo}})')]);slots['tan_hi']=atom('tan(pi*(dy-dx)/n)','1');slots['tan_lo']=atom('tan(pi*(b-a)/n)','0')
 if sid=='q-76650':
  maps.extend([
   vec('2\\,i+3\\,j','a+dx','b+dy'),vec('2\\,i+2\\,j','dx','dy'),vec('j','a','b','avec'),
   scalar('(4x+2)\\,{e}^{xy}','(2*dy*x+dx*b-dy*a)*exp(x*y)'),
   scalar('(4(2t)+2){e}^{2t(1+2t)}','(2*dy*(a+dx*t)+dx*b-dy*a)*exp((a+dx*t)*(b+dy*t))'),
   scalar('(8t+2)\\,{e}^{2t+4{t}^{2}}','(2*dx*dy*t+dx*b+dy*a)*exp(dx*dy*t**2+(dx*b+dy*a)*t+a*b)'),
   scalar('2t+4{t}^{2}','dx*dy*t**2+(dx*b+dy*a)*t+a*b'),scalar('2+8t','2*dx*dy*t+dx*b+dy*a'),
   scalar('\\sqrt{{2}^{2}+{2}^{2}}','sqrt(dx**2+dy**2)'),scalar('2\\sqrt{2}','sqrt(dx**2+dy**2)'),
   scalar('1+2t','b+dy*t'),scalar('2t','a+dx*t')])
  # Restrict vector j replacement to complete vec slots to protect basis labels.
  maps=[m for m in maps if m[0]!='j']
  maps.extend([('$a=j$',r'$a={{avec}}$'),('=j+t[',r'={{avec}}+t['),('-j]',r'-{{avec}}]'),('=j+t(',r'={{avec}}+t(')])
  # Every endpoint appears separately; no correlated endpoint errors are hidden.
  maps.extend([('{0}^{6}',r'{'+ '{{exp_lo}}' +'}^{'+ '{{exp_hi}}' +'}'),('{|}_{0}^{6}',r'{|}_{'+ '{{exp_lo}}' +'}^{'+ '{{exp_hi}}' +'}'),('{e}^{6}-{e}^{0}',r'{e}^{'+ '{{exp_hi}}' +'}-{e}^{'+ '{{exp_lo}}' +'}'),scalar('{e}^{6}-1','exp((a+dx)*(b+dy))-exp(a*b)','endpoint_difference')])
  slots['exp_lo']=atom('a*b','0');slots['exp_hi']=atom('(a+dx)*(b+dy)','6')
 # longest masks first and do not recursively substitute inserted slot labels.
 maps.sort(key=lambda z:len(z[0]),reverse=True)
 def mask(text):
  if text is None:return None
  # single regex replacement prevents short xy/vector masks from overwriting new slots.
  lookup=dict(maps)
  if not lookup:return text
  return re.sub('|'.join(map(re.escape,lookup)),lambda m:lookup[m.group(0)],text)

 for node in slots.values():
  if node.get('notation') in [r'(1+3t)(2+5t)',r'2+\sqrt{2(2t)}',r'{e}^{3(-t)+4t}',r'{sec}^{2}⁡(\frac{\pi ((1+3t)-(1+t))}{8})',r'(4(2t)+2){e}^{2t(1+2t)}']:
   node['kind']='substitution'
  if node.get('notation')==r'{sec}^{2}⁡(\frac{\pi (y-x)}{8})':node['kind']='secant_function'
  if node.get('notation')==r'{sec}^{2}⁡(\frac{\pi t}{4})':node['kind']='secant_collected'
  if node.get('notation')==r'(8t+2)\,{e}^{2t+4{t}^{2}}':node['kind']='matched_expanded'
 D[sid]={'family':f,'anchor':p,'problem':mask(problem),'solution':mask(sol),'slots':slots,'bank_notation':[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]}
(P/'source-templates.json').write_text(json.dumps(D,indent=2)+'\n')
