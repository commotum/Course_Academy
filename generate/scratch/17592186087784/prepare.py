"""One-time explicit extraction; generator uses the extracted templates, not sources."""
import json,re
from pathlib import Path
H=Path(__file__).resolve().parent
S=json.loads((H/'source.json').read_text())['record']
parameters={'q-78681':(7,0,0,'0','1'),'q-79205':(4,0,0,'1','3/2'),'q-106294':(3,0,0,'0','1'),'q-275161':(3,0,0,'1','2'),'q-321947':(4,0,0,'0','7/6'),'q-321948':(4,0,0,'0','1/2'),'q-321976':(1,-1,1,'1/2','2'),'q-79165':(2,0,0,'0','1/4'),'q-79166':(3,0,0,'0','3/2'),'q-79168':(2,0,0,'0','5/4'),'q-79210':(3,5,-4,'0','1/2'),'q-79270':(6,0,0,'0','1'),'q-79271':(3,0,0,'0','1/2'),'q-79272':(1,0,0,'0','1/2'),'q-106293':(2,0,0,'1/2','1')}
tnames={'q-78681':'easy_semi_radio','q-79205':'moderate_compact_radio','q-106294':'easy_semi_radio','q-275161':'moderate_arc_blank','q-321947':'easy_arc_blank','q-321948':'easy_quarter_blank','q-321976':'hard_threequarter_blank','q-79165':'easy_arc_radio','q-79166':'easy_threequarter_radio','q-79168':'easy_arc_radio','q-79210':'hard_quarter_radio','q-79270':'easy_semi_radio','q-79271':'easy_quarter_radio','q-79272':'easy_quarter_radio','q-106293':'moderate_quarter_radio'}
# Angle expressions stored as exact rational multiples of pi; copied values are evidence only.
def rat(v):
 import fractions
 v=v.strip().replace('π',r'\pi').replace('θ',r'\theta').replace('∈',r'\in').replace(' ','')
 if v=='0':return '0'
 m=re.fullmatch(r'(-?)\\frac\{(\d*)\\pi\}\{(\d+)\}',v)
 if m:return str(fractions.Fraction(int((m[2] or '1'))*(-1 if m[1] else 1),int(m[3])))
 m=re.fullmatch(r'(-?\d*)\\pi',v)
 if m:return str(int(m[1] or '1') if m[1]!='-' else -1)
 raise ValueError(v)
def interval(v):
 v=v.split('[')[1];l,r=v[:-1].split(',');return [rat(l),rat(r),v[-1]]
contract={'templates':{},'profiles':{}};cases=[];mapping=[]
for q in S[':knowledge-point/questions']:
 id=q[':question/math-academy-id'];r,h,k,a,b=parameters[id];name=tnames[id];level=q.get(':question/difficulty',{}).get(':db/ident','/moderate').split('/')[-1];p={'r':r,'h':h,'k':k,'start':a,'end':b};f=q[':question/answer-fields'];kind=f[0][':answer-field/type'][':db/ident'].split('/')[-1]
 eq=re.search(r'x\s*=.*?sin.*?(?:\\theta|θ)(?:\s*[+-]\d+)?',q[':question/problem']).group()
 problem=q[':question/problem'].replace(eq,'{equations}')
 problem=re.sub(r'!\[.*?\]\(.*?\)','{prompt_plot}',problem)
 solution=q.get(':question/worked-solution','')
 # Replace complete displayed x/y equation pair, not isolated numerical digits.
 if solution:
  solution=solution.replace(eq,'{equations}')
  solution=re.sub(r'!\[.*?\]\(.*?\)','{solution_plot}',solution)
  solution=solution.replace('$r='+str(r)+'.$','$r={r}.$')
  if h or k:solution=solution.replace('radius $'+str(r)+'$','radius ${r}$').replace('('+str(h)+','+str(k)+')','({h},{k})')
  last=re.findall(r'\$\[(.*?)\]\$',solution)
  if not last:raise ValueError(id)
  old='['+last[-1]+']';solution=solution.replace(old,'{interval}')
  # Not all input source equation pairs have identical trailing whitespace.
  solution=re.sub(r'x=(?:\d+)?\\operatorname\{cos\}⁡\\theta (?:[+-]\d+)?,\\,y=(?:\d+)?\\operatorname\{sin\}⁡\\theta (?:[+-]\d+)?',lambda m:'{equations}',solution)
 else:
  solution='The parametric equations of a circle  of radius $r$  centered at  the origin are\n\n$$\nx=r\\operatorname{cos}⁡\\theta ,\\,y=r\\operatorname{sin}⁡\\theta ,\\,\\theta \\in [0,2\\pi ).\n$$\n\nIn our case, the radius $r={r}.$ So, the parametric equations of the *full* circle are \n\n$$\n{equations},\\,\\theta \\in [0,2\\pi ).\n$$\n\nTo restrict the parameterization to a quarter-circle, we associate the parameter $\\theta $ with the central angle formed by a point $(x,y)$ on the circle and the $x$-axis. \n\n{solution_plot}\n\nWe can see that if we restrict $\\theta $ to ${interval}$, we get the required quarter-circle.\n\nTherefore, the parametric equations of the quarter-circle are \n\n$$\n{equations},\\,\\theta \\in {interval}.\n$$'
 if name not in contract['templates']:
  contract['templates'][name]={'level':level,'kind':kind,'problem':problem,'solution':solution,'field_keys':[x[':answer-field/key'] for x in f],'centered':bool(h or k),'start_mode':'zero' if a=='0' else 'nonzero','default_end':b,'sources':[],'eq_style':'compact' if id=='q-79205' else 'operator','cue':id in ('q-79165','q-79168','q-321947')}
 contract['templates'][name]['sources'].append(id)
 profile=None
 if kind=='radio':
  profile='observed-'+id;opts=[interval(x[':answer/value']) for x in f[0][':answer-field/choices']]
  contract['profiles'][profile]={'origin':'observed','template':name,'source':id,'required_interval':[a,b],'options':opts,'prefix':'unicode' if id=='q-79205' else ('none' if id in ('q-79210','q-106293') else 'theta'),'source_values':[x[':answer/value'] for x in f[0][':answer-field/choices']]}
 cases.append({'source_id':id,'template':name,'level':level,'parameters':p,'bank_profile':profile,'repair':id=='q-79205'})
 mapping.append({'source_id':id,'template':name,'parameters':p,'fields':[{'key':x[':answer-field/key'],'values':[a[':answer/value'] for a in x[':answer-field/choices']],'correct':x.get(':answer-field/correct',{}).get(':answer/value')} for x in f]})
(H/'contract.json').write_text(json.dumps(contract,indent=2,ensure_ascii=False)+'\n');(H/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(H/'choice-mapping.json').write_text(json.dumps(mapping,indent=2,ensure_ascii=False)+'\n')
