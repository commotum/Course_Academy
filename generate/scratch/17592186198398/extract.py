"""Read-only source extraction. Writes only this KP's recipe evidence."""
import json,re
from pathlib import Path
here=Path(__file__).parent
source=json.loads((here/'source.json').read_text())['record'][':knowledge-point/questions']
families=['power','vcosu','ucosv','sum','exp','zcosu','sinsin']
integrands=[r'(3x - 2y)^{2}(y + 2z)',r'(x + z)\cos (x^{2} + y)',r'({x}^{2}+2y)\operatorname{cos}⁡(x-z)',r'(\frac{2x-y}{2}+\frac{z}{3})',r'(y+z){e}^{x+{y}^{2}}',r'{z}^{2}\operatorname{cos}⁡(2x+3y)',r'\operatorname{sin}⁡(x-2z)\operatorname{sin}⁡({x}^{2}+2y)']
raw={};cases=[]
for q,f,integrand in zip(source,families,integrands):
 sid=str(q[':db/id']);field=q[':question/answer-fields'][0]
 assert integrand in q[':question/problem']
 recipe=dict(source_id=sid,ma_id=q[':question/math-academy-id'],family=f,question_keys=sorted(k for k in q if k not in (':db/id',':question/id',':question/math-academy-id')),field_keys=sorted(k for k in field if k not in (':db/id',':answer-field/id')),integrand=integrand,prompt_mask=q[':question/problem'].replace(integrand,'{{integrand}}'),choice_atoms=[a[':answer/value'] for a in field[':answer-field/choices']],defects=[])
 if ':answer-field/correct' in field:recipe['correct_index']=next(i for i,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][':answer/id'])
 if ':question/difficulty' in q:recipe['difficulty']=q[':question/difficulty'][':db/ident'].split('/')[-1]
 else:recipe['defects'].append('Unrated, no correct designation, no worked solution; raw omission retained.')
 if ':question/worked-solution' in q:
  solution=q[':question/worked-solution']; prefix,arithmetic=solution.split('**Step 4**: Perform the change of variables:\n\n')
  recipe['solution_prefix']=prefix.split('**Step 1**:')[0]
  recipe['change']=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/problem'],re.S)[0]
  head,body=arithmetic.split(' & =',1);body,tail=body.rsplit('\\end{aligned}',1)
  nodes=body.split(' \\\\  & =');recipe['arithmetic_nodes']=nodes
  masked=prefix+'**Step 4**: Perform the change of variables:\n\n'+head.replace(integrand,'{{integrand}}')+' & ='+' \\\\  & ='.join('{{stage_'+str(i)+'}}' for i in range(len(nodes)))+'\\end{aligned}'+tail
  recipe['solution_mask']=masked
  assert masked.replace('{{integrand}}',integrand).replace('{{stage_0}}',nodes[0]) # subsequent replay validated below
  reproduced=masked.replace('{{integrand}}',integrand)
  for i,node in enumerate(nodes):reproduced=reproduced.replace('{{stage_'+str(i)+'}}',node)
  assert reproduced==solution
 if sid=='17592186374090':recipe['defects'].append('Last endpoint row lacks closing parenthesis: (1-(-1). Raw retained; authored normal expands balanced endpoints.')
 raw[sid]=recipe
 cases.append(dict(source_id=sid,template=f,level='moderate',parameters={'scale':1},bank_profile='raw-'+sid,observed_level=recipe.get('difficulty'),authored_routing_level=(':question/difficulty' not in q)))
(here/'raw-recipes.json').write_text(json.dumps(raw,indent=2,ensure_ascii=False)+'\n')
(here/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
