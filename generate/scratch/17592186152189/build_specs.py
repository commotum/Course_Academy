import json,re,pathlib,shutil
D=pathlib.Path(__file__).resolve().parent;root=D.parents[1]/'runs/current';s=json.load(open(root/'sources/17592186152189.json'));shutil.copyfile(root/'sources/17592186152189.json',D/'source.json')
params=[(4,2,2,1),(2,3,3,-1),(5,3,-2,-3),(7,4,-3,2),(3,8,3,-2),(5,3,2,-1),(3,8,0,5),(4,5,-2,1),(8,6,4,6),(6,4,-2,5),(6,4,-3,2),(5,3,-3,2),(4,6,-4,-4),(3,5,3,2),(1,2,3,1)]
# These complete operation catalogs were read against every displayed source bank.
banks=[
 [('a','b','-h','-k','cos','sin'),('2*a','2*b','h','k','cos','sin'),('a/2','b/2','h','-k','cos','sin'),('a','b','h','k','cos','sin'),('2*a','2*b','-h','-k','cos','sin')],
 [('2*a','2*b','h','k','cos','sin'),('2*a','2*b','h','k','sin','cos'),('1','1','-h','a','cos','sin'),('a','b','h','k','sin','cos'),('a','b','h','k','cos','sin')],
 [('a','b','h','k','cos','sin'),('2*a','2*b','h','k','sin','cos'),('a','b','k','h','cos','sin'),('a','b','h','k','sin','cos'),('a**2','b**2','k','h','cos','sin')],
 [('a','b','k','h','cos','sin'),('b','a','h','k','cos','sin'),('a','b','h','k','cos','sin'),('2*a','2*b','h','k','sin','sin'),('a','b','-h','-k','sin','cos')],
 [('b','a','-h','-k','cos','sin'),('b**2','a**2','h','k','cos','sin'),('b','a','h','k','cos','sin'),('a','b','-h','-k','cos','sin'),('a','b','h','k','cos','sin')],
 None,None,None,
 [('a','b','h','k','cos','sin'),('a','b','k','h','cos','sin'),('b','a','k','h','cos','sin'),('2*a','2*b','h','k','sin','cos'),('a','b','h','k','sin','cos')],
 [('a','b','h','k','cos','sin'),('b','a','k','h','cos','sin'),('2*a','2*b','h','k','sin','cos'),('2*a','2*b','h','k','cos','sin'),('a','b','h','k','sin','cos')],
 [('a**2','b**2','-k','-h','cos','sin'),('a','b','-h','-k','cos','sin'),('2*a','2*b','k','h','cos','sin'),('2*a','2*b','h','k','cos','sin'),('a','b','h','k','cos','sin')],
 [('a','b','h','k','cos','sin'),('a','b','-h','-k','cos','sin'),('2*a','2*b','k','h','cos','sin'),('2*a','2*b','h','k','cos','sin'),('a**2','b**2','-k','-h','cos','sin')],
 [('a','b','h','k','cos','sin'),('b**2','a**2','h','k','cos','sin'),('a','b','-h','-k','cos','sin'),('b','a','-h','-k','cos','sin'),('b','a','h','k','cos','sin')],
 [('a**2','b**2','-k','h','cos','sin'),('a','b','h','k','cos','sin'),('b','a','-h','-k','cos','sin'),('b','a','h','k','cos','sin'),('a','b','k','-h','cos','sin')],
 [('a','b','h','k','cos','sin'),('2*a','2*b','h','k','cos','sin'),('a','b','h','k','sin','cos'),('a','b','k','h','cos','sin'),('2*a','2*b','k','h','sin','cos')]]
def style(v):
 # Whole mathematical components: retain source function spelling and layout.
 m=re.fullmatch(r'(x\s*=\s*)?(\d*)(\\(?:operatorname\{(?:cos|sin)\}⁡?|cos|sin)\s*(?:\\theta|θ))(.*)',v)
 assert m,v
 prefix,c,f,tail=m.groups();tail=re.fullmatch(r'(\s*)([+-])?(\s*)(\d+)?',tail);assert tail,v
 return dict(prefix=prefix or '',function=f.replace('cos','{FUNC}').replace('sin','{FUNC}'),space=tail[1],explicit_one=c=='1',zero_space=tail[1] if not tail[2] else '',has_shift=bool(tail[2]),sign_space=tail[3])
def pair_styles(v):
 if v.startswith('x'):
  m=re.match(r'(.*?)(,\s*(?:\\,)?y\s*=\s*)(.*)',v);assert m,v
  return [style(m[1]),dict(style(m[3]),prefix=m[2])]
 return [style(v)]
specs=[];cases=[]
for i,q in enumerate(s['record'][':knowledge-point/questions']):
 a,b,h,k=params[i];p=dict(a=a,b=b,h=h,k=k);id=q[':question/math-academy-id'];prob=q[':question/problem'];asset=re.search(r'!\[\]\(([^)]+)',prob)[1];prob=prob.replace(asset,'{PLOT}')
 prob=prob.replace(f'$({h},{k})$', '${CENTER}$').replace(f'$A({h+a},{k})', '$A{START}').replace(f'horizontal radius ${a}$', 'horizontal radius ${A}$').replace(f'vertical radius ${b},$', 'vertical radius ${B},$')
 sol=q.get(':question/worked-solution');final=None
 if sol:
  sol=sol.replace(f'$({h},{k}),$', '${CENTER},$').replace(f'$a={a}$','$a={A}$').replace(f'$b={b}.$','$b={B}.$')
  blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);last=blocks[-1];end=last.index(',\\,\\theta');final=pair_styles(last[:end]);sol=sol.replace(last[:end],'{FINAL}')
 fields=[]
 for j,f in enumerate(q[':question/answer-fields']):
  choices=f[':answer-field/choices'];recipes=banks[i]
  if i==1 and j==1:recipes=[banks[i][3],banks[i][2],banks[i][4],banks[i][0],banks[i][1]]
  if recipes is None:
   key=f[':answer-field/key'];recipes=[('a','h','cos') if key=='field-1' else ('b','k','sin')]
  fields.append(dict(key=f[':answer-field/key'],type=f[':answer-field/type'][':db/ident'],has_correct=':answer-field/correct' in f,correct_index=next((n for n,v in enumerate(choices) if v[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')),None),recipes=recipes,styles=[pair_styles(v[':answer/value']) for v in choices]))
 level=q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1] or 'moderate'
 specs.append(dict(id=id,db_id=q[':db/id'],level=level,unrated=':question/difficulty' not in q,parameters=p,prompt=prob,solution=sol,final_style=final,asset=asset,fields=fields))
 cases.append(dict(source_id=id,template=id,parameters=p,bank_profile='observed:'+id,level=level))
(D/'specs.json').write_text(json.dumps(specs,ensure_ascii=False,indent=2)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
