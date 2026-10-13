"""Retain a complete, independently verified choice-to-recipe source mapping."""
import json
import validate as v
result=[]
for name,(level,parameters) in v.g.CASES.items():
 original=v.g.SOURCES[name];f=original[':question/answer-fields'][0]
 z,u,w,d,ans,bank,*_=v.g.objects(name,parameters)
 choices=[]
 for a in f[':answer-field/choices']:
  indices=[i for i,b in enumerate(bank) if v.equal(v.scalar(a[':answer/value']),b)]
  assert len(indices)==1
  choices.append({'source_answer_id':a[':answer/id'],'field_id':f[':answer-field/id'],'exact_rendered_value':a[':answer/value'],'complete_mathematical_value':str(v.scalar(a[':answer/value'])),'correct':a[':answer/id']==f[':answer-field/correct'][':answer/id'],'matched_recipe_index':indices[0]})
 result.append({'source_id':name,'difficulty':level,'original_problem':original[':question/problem'],'original_solution':original[':question/worked-solution'],'original_parameters':parameters,'variable':str(z),'numerator':str(u),'denominator':str(w),'mathematical_derivative':str(d),'response_fragment':str(ans),'field_key':f[':answer-field/key'],'field_type':f[':answer-field/type'][':db/ident'],'profile':name if len(bank)>1 else None,'source_choices':choices})
(v.H/'source-components.json').write_text(json.dumps(result,indent=2)+'\n')
print('Mapped',sum(len(r['source_choices']) for r in result),'source options across',len(result),'complete banks.')
