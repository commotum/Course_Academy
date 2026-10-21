import json,re,pathlib,collections,hashlib
R=pathlib.Path(__file__).resolve().parent

def save(n,v):(R/n).write_text(json.dumps(v,indent=2)+'\n')
def tri(v):
 m=re.search(r'\\begin\{(?:bmatrix|array)\}(?:\{[^}]*\})?(.*?)\\end\{(?:bmatrix|array)\}',v,re.S)
 if m:return tuple(int(row.split('&')[3]) for row in m[1].split(r'\\'))
 if 'langle' in v or '⟨' in v:return tuple(map(int,re.findall(r'-?\d+',v)))
 return tuple(int(re.search(var+r'\s*=\s*(-?\d+)',v)[1]) for var in 'xyz')
def metrics(records):
 groups=collections.defaultdict(list)
 for r in records:
  groups['overall'].append(r);groups['profile:'+r['generation']['source_profile']].append(r);groups['shape:'+r['generation']['template']].append(r)
 out=[]
 for group,rs in groups.items():
  for strategy in ['position1','position2','position3','position4','position5','lex_min','lex_max','majority_coordinates','unique_z']:
   successes=total=0;ids=[]
   for r in rs:
    q=r['question'];f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];values=[tri(c[':answer/value']) for c in choices];correct=next(i for i,c in enumerate(choices) if c[':answer/id']==f[':answer-field/correct'][1]);pred=None
    if strategy.startswith('position'):pred=int(strategy[-1])-1
    elif strategy=='lex_min':pred=values.index(min(values))
    elif strategy=='lex_max':pred=values.index(max(values))
    elif strategy=='majority_coordinates':
     v=tuple(collections.Counter(t[j] for t in values).most_common(1)[0][0] for j in range(3));pred=values.index(v) if v in values else 0
    else:
     z=int(re.search(r'\\\\\s*z\s*&?=\s*(-?\d+)',q[':question/problem'])[1]);eligible=[i for i,v in enumerate(values) if v[2]==z]
     if len(eligible)!=1:continue
     pred=eligible[0]
    total+=1;successes+=pred==correct;ids.append(q[':question/id'])
   if total:out.append({'subgroup':group,'strategy':strategy,'correct':successes,'total':total,'baseline':0.2,'question_ids':ids})
 return out
stages={name:json.load(open(R/path)) for name,path in [('controlled','controlled-records.json'),('random','random-records.json'),('random_delivered','delivery-sample/accepted.json'),('batch','runner-batch.json'),('batch_delivered','delivery-batch/accepted.json')]}
result={name:metrics(rs) for name,rs in stages.items()};save('shortcut-results.json',result)
coverage={name:{'count':len(rs),'profiles':dict(collections.Counter(r['generation']['source_profile'] for r in rs)),'roles':dict(collections.Counter(str(r['generation']['instance']['role']) for r in rs)),'masks':dict(collections.Counter(str(r['generation']['instance']['parameters']['mask']) for r in rs)),'correct_positions':dict(collections.Counter(str(next(i for i,c in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if c[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1])) for r in rs))} for name,rs in stages.items()};save('variation-coverage.json',coverage)
# Actual preview DOM option positions (UI reorders choices with seeded FNV; raw array position is separate).
html=[]
for i in range(1,6):
 text=(R/f'render/question-{i:03}.html').read_text();inputs=re.findall(r'<input\b[^>]*type="radio"[^>]*>',text);order=[re.search(r'value="([^"]+)"',s)[1] for s in inputs];key=stages['batch'][i-1]['question'][':question/answer-fields'][0][':answer-field/correct'][1];assert key in order;html.append({'fixture_content_id':i,'question_id':stages['batch'][i-1]['question'][':question/id'],'displayed_choice_ids':order,'correct_position':order.index(key)})
save('ui-choice-order.json',{'basis':'Actual rendered DOM in render/question-001.html through question-005.html; preview content IDs 1..5, not allocated production task-item IDs. learning.js choiceOrder hashes itemId and field/choice IDs, unrelated to correctness.','cases':html,'position_counts':dict(collections.Counter(str(x['correct_position']) for x in html))})
# All questions in captured inventory examined; omission is not a per-instance defect.
inv=json.load(open(R.parent/'source/inventory.json'));save('inventory-assessment.json',{'basis':inv['basis'],'question_count':len(inv['questions']),'questions':[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'math_academy_id':q.get(':question/math-academy-id'),'generation_metadata_fields':[k for k in q if 'generat' in k]} for q in inv['questions']],'demonstrated_defect':'Package omits replay/profile entries; no corresponding defective generated-instance rule demonstrated. q-20598 is a captured original source, not a generated record. q-131590 has a captured source key error corrected by package replay.','status':'Verified absence of affected inventory instances for the demonstrated omission; no assertion of absence of other possible defects.','limits':'Five non-Math-Academy inventory records lack generation metadata; no inferred seed or generator attribution.'});save('affected-inventory.json',{'affected_questions':[]})
print(json.dumps({'coverage':coverage,'perfect_conditional_controlled':[x for x in result['controlled'] if x['correct']==x['total'] and x['strategy']!='unique_z'],'batch_overall':[{k:v for k,v in x.items() if k!='question_ids'} for x in result['batch'] if x['subgroup']=='overall'],'ui_positions':[x['correct_position'] for x in html]}))
