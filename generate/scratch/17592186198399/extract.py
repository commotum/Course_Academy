"""Captured full-component masks; read-only source extraction, private files only."""
import json,re
from pathlib import Path
H=Path(__file__).parent
r=json.load(open(H/'source.json'))['record'];out={};cases=[]
configs=[
 ('linear_yz',dict(a=2,b=1,c=1,d=-2,lu=0,hu=1,lv=-1,hv=1,lw=1,hw=4),r'2y+z'),
 ('reciprocal',dict(a=1,b=1,c=1,d=1,lu=1,hu=2,lv=1,hv=2,lw=1,hw=5),r'\sqrt{y} + x'),
 ('log',dict(a=1,b=1,c=1,d=1,lu='1/2',hu=1,lv=3,hv=10,lw=1,hw=2),r'y+{x}^{2}'),
 ('shear',dict(a=1,b=1,c=1,d=1,lu=0,hu=1,lv=0,hv=1,lw=-1,hw=1),r'x+y'),
 ('linear_xz',dict(a=1,b=1,c=1,d=-1,lu=-5,hu=5,lv=0,hv=10,lw=0,hw=6),r'y'),
 ('sqrt',dict(a=1,b=1,c=1,d=1,lu=-2,hu=2,lv=0,hv=1,lw=1,hw=4),r'{x}^{2}-y-z')]
def parse(t):
 t=t.replace('\\\\','\\').replace('⁡','').replace(r'\operatorname{ln}','log').replace(r'\ln','log')
 t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',t)
 t=re.sub(r'(\d+)log(\d+)',r'\1*log(\2)',t)
 return t
for q,(f,p,expr) in zip(r[':knowledge-point/questions'],configs):
 lo,hi=str(p['lv']),str(p['hv']);slots={'lv':lo+'*h','hv':hi+'*h'}
 def mask(text,prompt=False):
  # Replace COMPLETE components before any scalar slot; no token substitutions.
  if f=='reciprocal':pat=lo+r' \le '+expr+r' \le '+hi;rep='@@lv@@'+r' \le '+expr+r' \le '+'@@hv@@'
  else:pat=lo+r'\le '+expr+r'\le '+hi;rep='@@lv@@'+r'\le '+expr+r'\le '+'@@hv@@'
  assert pat in text,(f,pat);text=text.replace(pat,rep)
  if not prompt:
   components=[(lo+r'\le v\le '+hi,'@@lv@@'+r'\le v\le '+'@@hv@@'),
     (r'{\int }_{'+lo+'}^{'+hi+'}',r'{\int }_{@@lv@@}^{@@hv@@}'),
     ('[v]_{'+lo+'}^{'+hi+'}','[v]_{@@lv@@}^{@@hv@@}'),
     ('[v]_{v='+lo+'}^{v='+hi+'}','[v]_{v=@@lv@@}^{v=@@hv@@}')]
   for a,b in components:text=text.replace(a,b)
   difference='('+hi+'-'+('('+lo+')' if p['lv']<0 else lo)+')'
   assert difference in text,(f,difference);text=text.replace(difference,'(@@hv@@-'+('(@@lv@@)' if p['lv']<0 else '@@lv@@')+')')
   final=text.rsplit(' & =',1)[1].split(r'.\end{aligned}')[0]
   slots['final']= {'linear_yz':'6*h/5','log':'7*h*log(2)','shear':'2*h','linear_xz':'600*h','sqrt':'60*h'}[f]
   text=text.replace(' & ='+final+r'.\end{aligned}',' & =@@final@@'+r'.\end{aligned}')
  return text
 banks=[[parse(a[':answer/value']) for a in fld[':answer-field/choices']] for fld in q[':question/answer-fields']]
 rec=dict(family=f,parameters={k:str(v) for k,v in p.items()},slots=slots,prompt_mask=mask(q[':question/problem'],True),bank_expressions=banks)
 if ':question/worked-solution' in q:rec['solution_mask']=mask(q[':question/worked-solution'])
 out[str(q[':db/id'])]=rec
 cases.append({'source_id':q[':db/id'],'template':f,'parameters':{'h':'1'},'bank_profile':'raw_'+str(q[':db/id']),'level':q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/hard').split('/')[-1],'authored_level_assignment':':question/difficulty' not in q})
(H/'raw-recipes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');(H/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
