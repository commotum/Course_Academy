"""Read-only extraction from immutable captured sources; private evidence writes."""
import json,re,shutil,pathlib
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[1]/'runs/current'
s=json.load(open(ROOT/'sources/17592186087713.json'))
shutil.copyfile(ROOT/'sources/17592186087713.json',HERE/'source.json')
shutil.copyfile(ROOT/'topics/17592186048896.json',HERE/'topic.json')
shutil.copyfile(ROOT/'lessons/17592186048896.json',HERE/'lesson.json')
old=json.load(open('/home/jake/Developer/MA/DATA/Lessons/861/Source/861.json'))
def walk(x):
 if isinstance(x,dict):
  if x.get('question_id') in ('69514','69515') or x.get('content_id')=='5017':yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
json.dump({'path':'/home/jake/Developer/MA/DATA/Lessons/861/Source/861.json','selected_records':list(walk(old))},open(HERE/'authoritative-layout.json','w'),indent=2,ensure_ascii=False)
cases=[];mapping=[]
for q in s['record'][':knowledge-point/questions']:
 prompt=q[':question/problem'];target=list(map(int,re.search(r'\$(\d+)\s*\\(?:times|cdot)\s*(\d+)\$',prompt).groups()))
 arrays=list(re.finditer(r'([A-Z])\s*=\s*(?:\[)?\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\2\}(?:\])?',prompt,re.S))
 labels=[m[1] for m in arrays];matrices=[[[v.strip() for v in row.split('&')] for row in m[3].split('\\\\')] for m in arrays]
 match=[i for i,a in enumerate(matrices) if [len(a),len(a[0])]==target]
 sid=q[':question/math-academy-id'];template='legacy_bmatrix' if arrays[0][2]=='bmatrix' else 'aligned_multiple' if len(match)==2 else 'aligned_single'
 c={'source_id':sid,'source_db_id':q[':db/id'],'level':'moderate','difficulty_origin':'observed' if ':question/difficulty' in q else 'authored assignment of unrated original at observed peer workload','template':template,'parameters':{'target':target,'labels':labels,'matrices':matrices},'bank_profile':sid,'correct_designation_origin':'observed' if ':answer-field/correct' in q[':question/answer-fields'][0] else 'independently derived from displayed dimensions','worked_solution_origin':'observed' if ':question/worked-solution' in q else 'authored common counting explanation'}
 cases.append(c)
 field=q[':question/answer-fields'][0]
 mapping.append({'source_id':sid,'target':target,'arrays':[{'label':l,'dimensions':[len(a),len(a[0])],'entries':a} for l,a in zip(labels,matrices)],'correct_subset':[labels[i] for i in match],'field_type':field[':answer-field/type'][':db/ident'],'choices':[{'original_value':a[':answer/value'],'subset_positions':[labels.index(l) for l in re.findall(r'\$([A-Z])\$',a[':answer/value'])],'recipe':'select exactly these positional labels; dimensions checked in independently parsed prompt','observed_correct':a[':answer/id']==field.get(':answer-field/correct',{}).get(':answer/id')} for a in field[':answer-field/choices']]})
json.dump(cases,open(HERE/'source-cases.json','w'),indent=2,ensure_ascii=False)
json.dump(mapping,open(HERE/'source-components.json','w'),indent=2,ensure_ascii=False)
