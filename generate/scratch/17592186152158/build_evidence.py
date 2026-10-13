"""Extract fixed prose and whole-component slots; only writes this KP directory."""
import json
from pathlib import Path
D=Path(__file__).parent
s=json.loads((D/'source.json').read_text())['record']
names=['exponential','line_product','circle','line_sum','line_polynomial','line_constant','parabola','reciprocal']
params=[{'n':3},{'b':1},{'b':2},{'b':3},{'b':1},{'b':2},{'n':5},{'n':2}]
levels=['hard','moderate','hard','moderate','moderate','moderate','hard','hard']
masks={};cases=[]
for q,name,p,level in zip(s[':knowledge-point/questions'],names,params,levels):
 prompt=q[':question/problem'];sol=q.get(':question/worked-solution')
 repairs=[]
 if sol:
  if '{r}^{′}(u)' in sol: sol=sol.replace('{r}^{′}(u)','{r}^{′}(t)');repairs.append('derivative argument u -> t')
  if name=='line_constant': sol=sol.replace(r'\frac{1}{t-(t-4))}',r'\frac{1}{t-(t-4)}');repairs.append('remove extra denominator parenthesis')
  if name=='reciprocal': sol=sol.replace(r'3{x}^{5}{y}^{2}',r'\frac{4{y}^{2}}{{x}^{3}}');repairs.append('replace unrelated original integral integrand with given integrand')
 # Slots are full endpoint expressions or complete bound components.
 repl={
 'exponential':[(r'\operatorname{ln}⁡3','@upper@'),('{10}^{3/2}','@powerupper@'),('10\\sqrt{10}-2\\sqrt{2}','@expanded@'),(r'\frac{4}{3}(5\sqrt{10}-\sqrt{2})','@answer@'),('{2}^{10}','{2}^{@uupper@}')],
 'circle':[('\\le 2','\\le @upper@'),('_{0}^{2}','_{0}^{@upper@}'),('{|}_{0}^{2}','{|}_{0}^{@upper@}'),('2({2}^{2}-{0}^{2})','@endpoint@'),('=8.','= @answer@.')],
 'line_sum':[('\\le 3','\\le @upper@'),('_{0}^{3}','_{0}^{@upper@}'),('{|}_{0}^{3}','{|}_{0}^{@upper@}'),(r'\sqrt{2}({3}^{2}-{0}^{2})','@endpoint@'),('=9\\sqrt{2}.','=@answer@.')],
 'line_polynomial':[('\\le 1','\\le @upper@'),('_{0}^{1}','_{0}^{@upper@}'),('{|}_{0}^{1}','{|}_{0}^{@upper@}'),(r'\sqrt{10}(\frac{1}{3}+\frac{3}{2}+2)','@endpoint@'),(r'\frac{23\sqrt{10}}{6}','@answer@')],
 'line_constant':[('\\le 2','\\le @upper@'),('_{0}^{2}','_{0}^{@upper@}'),('{|}_{0}^{2}','{|}_{0}^{@upper@}'),(r'\frac{\sqrt{2}}{4}(2-0)','@endpoint@'),(r'\frac{\sqrt{2}}{2}.','@answer@.')],
 'parabola':[(r'4\sqrt{6}','@upper@'),('{1}^{25}','{1}^{@uupper@}'),('{25}^{3/2}','@powerupper@'),('125-1','@expanded@'),(r'\frac{124}{3}','@answer@')],
 'reciprocal':[(r'\sqrt[4]{2}','@upper@'),('^{3/2}','^{@uupper@}'),(r'\sqrt{{(\frac{3}{2})}^{3}}','@powerupper@'),(r'\frac{3\sqrt{6}}{4}-2\sqrt{2}','@expanded@'),(r'\frac{1}{6}(8\sqrt{2}-3\sqrt{6})','@answer@')],
 }.get(name,[])
 # reciprocal ^{3/2} replacement must only target transformed bound, not exponent.
 if name=='reciprocal': repl[1]=(r'_{2}^{3/2}',r'_{2}^{@uupper@}')
 for old,new in repl:
  prompt=prompt.replace(old,new)
  if sol: sol=sol.replace(old,new)
 masks[name]={'problem':prompt,'solution':sol,'repairs':repairs,'source_id':q[':question/math-academy-id'],'level':level}
 cases.append({'source_id':q[':question/math-academy-id'],'template':name,'level':level,'parameters':p,'bank_profile':'observed_'+name,'original':q,'authored_level':name=='line_product','missing_correct_reference':name=='line_product'})
(D/'templates.json').write_text(json.dumps(masks,indent=2,ensure_ascii=False))
(D/'source-cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False))
