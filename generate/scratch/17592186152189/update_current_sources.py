"""Extend source replay with the three additions captured at basis 2658."""
import ast,json,re
from pathlib import Path
D=Path(__file__).resolve().parent
# Reuse the established notation extractor without executing its old capture loop.
module=ast.parse((D/'build_specs.py').read_text())
for node in module.body:
 if isinstance(node,ast.FunctionDef):exec(compile(ast.Module(body=[node],type_ignores=[]),'<source-style>','exec'))
src=json.loads((D/'source-current.json').read_text())['record']
catalog={
'q-79288':((7,4,4,-2), [('b','a','h','k','cos','sin'),('b','a','-k','-h','cos','sin'),('a','b','k','h','cos','sin'),('a','b','h','k','cos','sin'),('a**2','b**2','-h','-k','cos','sin')]),
'q-327167':((2,6,-3,4),None),
'q-106396':((3,6,-2,3),[('b**2','a**2','h','k','cos','sin'),('a','b','-h','-k','cos','sin'),('b','a','-h','-k','cos','sin'),('b','a','h','k','cos','sin'),('a','b','h','k','cos','sin')])}
rows=[]
for q in src[':knowledge-point/questions']:
 id=q[':question/math-academy-id']
 if id not in catalog:continue
 (a,b,h,k),bank=catalog[id];p=dict(a=a,b=b,h=h,k=k)
 prob=q[':question/problem'];asset=re.search(r'!\[\]\(([^)]+)',prob)[1];prob=prob.replace(asset,'{PLOT}')
 prob=prob.replace(f'$({h},{k})$', '${CENTER}$').replace(f'$A({h+a},{k})', '$A{START}').replace(f'horizontal radius ${a}$', 'horizontal radius ${A}$').replace(f'vertical radius ${b},$', 'vertical radius ${B},$')
 sol=q[':question/worked-solution'].replace(f'$({h},{k}),$', '${CENTER},$').replace(f'$a={a}$','$a={A}$').replace(f'$b={b}.$','$b={B}.$')
 last=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)[-1];end=last.index(',\\,\\theta');final=pair_styles(last[:end]);sol=sol.replace(last[:end],'{FINAL}')
 fields=[]
 for f in q[':question/answer-fields']:
  choices=f[':answer-field/choices'];recipes=bank or [('a','h','cos') if f[':answer-field/key']=='field-1' else ('b','k','sin')]
  fields.append(dict(key=f[':answer-field/key'],type=f[':answer-field/type'][':db/ident'],has_correct=True,correct_index=next(i for i,v in enumerate(choices) if v[':answer/id']==f[':answer-field/correct'][':answer/id']),recipes=recipes,styles=[pair_styles(v[':answer/value']) for v in choices]))
 rows.append(dict(id=id,db_id=q[':db/id'],level=q[':question/difficulty'][':db/ident'].split('/')[-1],unrated=False,parameters=p,prompt=prob,solution=sol,final_style=final,asset=asset,fields=fields))
(D/'specs-current-additions.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
