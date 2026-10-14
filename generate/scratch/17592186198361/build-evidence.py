import json,re
from pathlib import Path
D=Path(__file__).parent
s=json.load(open(D/'source.json'))['record']
names=['difference','sum_product_evidence','ratio_product','triangular_quadratic','product','exponential','sum_square']
params=[dict(ul=0,uh=3,vl=0,vh=2),dict(ul=1,uh=4,vl=1,vh=10),dict(ul=1,uh=4,vl=1,vh=5),dict(ul=0,uh=5,vl=0,vh=1),dict(ul=-1,uh=1,vl=0,vh=1),dict(ul=0,uh=2,vl=0,vh=4),dict(ul=-1,uh=3,vl=-4,vh=-1)]
out={};cases=[]
for name,p,q in zip(names,params,s[':knowledge-point/questions']):
 def mask(t):
  # Slots are complete bounds of a known inequality/integral, never short global replacements.
  for low,high,var in [('ul','uh','u'),('vl','vh','v')]:
   a,b=p[low],p[high]
   # Integral syntax is exactly the captured source spelling.
   t=t.replace(r'_{'+str(a)+'}^{'+str(b)+'}',r'_{@@'+low+'@@}^{@@'+high+'@@}')
  # Each family has two distinct inequality operands, avoiding coincident bounds.
  operands={'difference':['x + y','y - x'],'sum_product_evidence':['xy','y + x'],'ratio_product':[r'{x}^{2}', 'xy'],'triangular_quadratic':['2x+y','y'],'product':['y-x','x+y'],'exponential':['2x+5y','x+3y'],'sum_square':['x+y','y-x']}[name]
  if name=='ratio_product':
   t=t.replace(r'{x}^{2}\\le y\\le 4{x}^{2}',r'@@ul@@{x}^{2}\\le y\\le @@uh@@{x}^{2}')
   # Source implicit unit coefficient is restored by render special value formatting.
   t=t.replace(r'{x}^{2}\le y\le 4{x}^{2}',r'@@ulcoef@@{x}^{2}\le y\le @@uh@@{x}^{2}')
  for (low,high),expr in zip([('ul','uh'),('vl','vh')],operands):
   a,b=p[low],p[high]
   for space in ['', ' ']:
    t=t.replace(str(a)+space+r'\le '+expr+space+r'\le '+str(b),'@@'+low+'@@'+space+r'\le '+expr+space+r'\le @@'+high+'@@')
   # Final solution rectangle has no spaces before TeX inequality.
   t=t.replace(str(a)+r'\le '+('u' if low=='ul' else 'v')+r'\le '+str(b),'@@'+low+'@@'+r'\le '+('u' if low=='ul' else 'v')+r'\le @@'+high+'@@')
  return t
 tmpl={k:mask(v) for k,v in q.items() if isinstance(v,str) and k in [':question/problem',':question/worked-solution']}
 if name=='ratio_product':
  # The entire operative chain gets a recipe slot, retaining source prose and earlier formal blocks.
  blocks=re.findall(r'\$\$(.*?)\$\$',tmpl[':question/worked-solution'],re.S)
  tmpl[':question/worked-solution']=tmpl[':question/worked-solution'].replace('$$'+blocks[-1]+'$$','$$\n@@chain@@\n$$')
 tmpl['choices']=[mask(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
 if name=='ratio_product':tmpl['choices'][-1]='@@result@@'
 if name=='sum_product_evidence':tmpl['choices']=['@@s0@@','@@s1@@','@@s2@@','@@s3@@','@@s4@@']
 tmpl['source_id']=q[':db/id'];tmpl['source_uuid']=q[':question/id'];tmpl['math_academy_id']=q[':question/math-academy-id'];tmpl['parameters']=p
 f=q[':question/answer-fields'][0]
 tmpl['correct_index']=next((i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')),None)
 tmpl['level']=q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1] or None
 out[name]=tmpl
 cases.append(dict(source_id=q[':db/id'],template=name,parameters=p,bank_profile='observed',level=tmpl['level'] or ('moderate' if name=='sum_product_evidence' else 'easy')))
(D/'templates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
