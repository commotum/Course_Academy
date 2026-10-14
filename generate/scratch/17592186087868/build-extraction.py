import json,re
from pathlib import Path
P=Path('generate/scratch/17592186087868')
source=json.load(open('generate/runs/current/sources/17592186087868.json'))
(P/'source.json').write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n')
D='{y}^{′}'
def mono(a,n):
 if not a:return '0'
 base='' if n==0 else ('x' if n==1 else '{x}^{'+str(n)+'}')
 return ('-' if a<0 else '')+('' if abs(a)==1 and base else str(abs(a)))+base
def rhs(r):
 b,c,m=r
 return mono(b,0).replace('1','',1)+'y' if b else mono(c,m)
def sy(b):return ('-' if b<0 else '')+('' if abs(b)==1 else str(abs(b)))+'y'
def lhs(a,n):return D+('+' if a>0 else '')+mono(a,n)+'y'
def eq(a,n,r):return lhs(a,n)+'='+sy(r[0]) if r[0] else lhs(a,n)+'='+mono(r[1],r[2])
def final(a,n,b):
 if n==0:
  v=a-b;return D+('+' if v>0 else '')+(sy(v) if v else '')
 if a>0:return D+'+('+mono(a,n)+('+' if -b>0 else '')+mono(-b,0)+')y'
 return D+'-('+mono(-a,n)+('+' if b>0 else '')+mono(b,0)+')y'
params={
'q-331601':(2,1,[(0,0,0),(0,4,0),(-1,0,0)]),
'q-331744':(-1,1,[(0,0,0),(1,0,0),(0,1,3)]),
'q-331605':(1,2,[(0,3,1),(0,0,0),(1,0,0)]),
'q-331724':(2,3,[(0,1,2),(-3,0,0),(0,0,0)]),
'q-331725':(-1,1,[(-1,0,0),(0,0,0),(-5,0,0)]),
'q-331727':(1,2,[(-3,0,0),(0,1,1),(0,0,0)]),
'q-331728':(-4,1,[(1,0,0),(0,0,0),(0,9,0)]),
'q-331729':(7,1,[(0,5,0),(0,0,0),(-2,0,0)]),
'q-331738':(4,1,[(0,2,0),(0,0,0),(1,0,0)]),
'q-331739':(-1,2,[(0,1,3),(1,0,0),(0,0,0)]),
'q-331742':(2,0,[(1,0,0),(0,1,1),(0,0,0)]),
'q-331743':(1,2,[(0,-2,0),(1,0,0),(0,0,0)]),
}
recipes={};cases=[]
for q in source['record'][':knowledge-point/questions']:
 id=q[':question/math-academy-id'];a,n,rs=params[id];p={'a':a,'n':n,'rhs':[list(r) for r in rs]}; masks={}
 for i,r in enumerate(rs):
  e=eq(a,n,r);masks[e]='{{eq'+str(i)+'}}'; masks[e.replace('=',' & =')]='{{aligned_eq'+str(i)+'}}'
  if r[0]:
   stage=lhs(a,n)+('+' if -r[0]>0 else '')+sy(-r[0])+' & =0'; masks[stage]='{{move'+str(i)+'}}';masks[final(a,n,r[0])+' & =0']='{{collect'+str(i)+'}}'
  if r[1]:
   force=mono(r[1],r[2]); masks['$Q(x)='+force+'$']='$Q(x)={{force'+str(i)+'}}$'; masks['$'+force+'$']='$'+'{{force'+str(i)+'}}'+'$'
 rx=re.compile('|'.join(re.escape(s) for s in sorted(masks,key=len,reverse=True)))
 render=lambda s:rx.sub(lambda m:masks[m[0]],s)
 pm=render(q[':question/problem']);sm=render(q[':question/worked-solution'])
 f=q[':question/answer-fields'][0];vals=[v[':answer/value'] for v in f[':answer-field/choices']]
 recipes[id]={'level':q[':question/difficulty'][':db/ident'].split('/')[-1], 'parameters':p,'problem_mask':pm,'solution_mask':sm,'bank':vals,'correct':f[':answer-field/correct'][':answer/value'],'keys':list(q),'field_keys':list(f),'source_id':id}
 cases.append({'source_id':id,'template':id,'level':recipes[id]['level'],'parameters':p,'bank_profile':'raw_'+id})
(P/'recipes.json').write_text(json.dumps(recipes,ensure_ascii=False,indent=2)+'\n')
(P/'source-cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
