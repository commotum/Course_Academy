"""Reviewed finite subsets; preserve continuous-set and whole-graph radios."""
from pathlib import Path
import copy,json,re,hashlib
H=Path(__file__).resolve().parent
Q={q[':db/id']:q for q in json.loads((H/'questions.json').read_text())}
KEYS={17592186064800:([0,1,3,6],[1,3],'Horizontal minimum at 1 and sharp corner at 3; 0 is regular and 6 is a regular intercept.'),17592186064802:([-1,3,5,7],[3],'Horizontal tangent at 3; 5 is a discontinuity and the intercepts -1/7 have nonzero slopes.'),17592186329838:([1,2,3,4,5,6],[2,4],'Horizontal tangent at 2 and corner at 4; other offered coordinates are regular.'),17592186341964:([-1,3,7],[3,7],'Horizontal maximum at 3 and defined discontinuity at 7; -1 is a regular intercept.'),17592186341965:([0,2,6],[0],'Horizontal stationary inflection at 0; corner at 2 and nonhorizontal crossing at 6.'),17592186600826:([-1,2,5,8],[2,8],'Corner at 2 and defined discontinuity at 8; -1 and 5 are regular intercepts.')}
STATEMENTS={17592186238008:[True,False,False],17592186600837:[True,True,False]}
INTERVALS={17592186238003,17592186238004,17592186329839,17592186403633,17592186403640}
GRAPHS={17592186064801,17592186620883}
ROMAN=('I','II','III')
ledger=[]
for eid,q in Q.items():
 row={'question_eid':eid,'math_academy_id':q.get(':question/math-academy-id'),'kp_ids':[k[':db/id'] for k in q.get(':knowledge-point/_questions',[])],'canonical_memberships':q.get(':knowledge-point/_canonical-example',[]),'old_fields':q.get(':question/answer-fields',[]),'difficulty':q.get(':question/difficulty'),'problem_before':q[':question/problem'],'worked_solution_before':q.get(':question/worked-solution'),'learner_uses':q.get(':task-item/_content',[]),'commit_status':'not_submitted'}
 fs=q.get(':question/answer-fields',[])
 if eid in KEYS:
  values,key,proof=KEYS[eid];objects=[{'source_label':'x='+str(x),'content':'$x='+str(x)+'$','selected':x in key} for x in values]
  mapping=[{'old_answer':a[':db/id'],'old_value':a[':answer/value'],'selected':['x='+str(int(n)) for n in re.findall(r'x\s*=\s*(-?\d+)',a[':answer/value'])]} for a in fs[0][':answer-field/choices']]
  row.update(decision='convert',objects=objects,choice_mapping=mapping,proof=proof,problem_after=q[':question/problem']+'\n\nSelect all that apply.')
 elif eid in STATEMENTS:
  head,_,tail=q[':question/problem'].partition('\n\nWhich of the following statements')
  texts=[]
  for line in tail.splitlines():
   line=line.strip()
   if line.startswith('- '):texts.append(line[2:])
   elif re.match(r'^(?:I|II|III)[.] ',line):texts.append(line.split('. ',1)[1])
  assert len(texts)==3
  objects=[{'source_label':label,'content':text,'selected':truth} for label,text,truth in zip(ROMAN,texts,STATEMENTS[eid])]
  mapping=[{'old_answer':a[':db/id'],'old_value':a[':answer/value'],'selected':re.findall(r'\b(?:III|II|I)\b',a[':answer/value'])} for a in fs[0][':answer-field/choices']]
  sol=q[':question/worked-solution']
  for label,text in reversed(list(zip(ROMAN,texts))):sol=sol.replace('Statement '+label+' is', 'The statement “'+text+'” is')
  if eid==17592186238008:sol=sol.replace('Therefore, statement I is true, while statements II and III are false.','Therefore, select only “'+texts[0]+'.”')
  else:sol=sol.replace('Therefore, only statements I and II are true.','Therefore, select “'+texts[0]+'” and “'+texts[1]+'.”')
  row.update(decision='convert',objects=objects,choice_mapping=mapping,proof='Graph inspection agrees with the stored key; the complete statements become checkbox captions.',problem_after=head+'\n\nWhich of the following statements are true with respect to the function $y=f(x)$ plotted above?\n\nSelect all that apply.',solution_after=sol)
  if eid==17592186238008:row['existing_solution_note']='The derivative index in the original second bullet is -1 despite discussing x=1. This separate source typo is preserved rather than silently repaired during response conversion.'
 elif eid==17592186620891:
  image=re.search(r'!\[.*?\]\((.*?)\)',q[':question/problem'])[1]
  objects=[{'source_label':label,'content':'Point $'+label+'$','selected':label=='A','shared_image':{'image':image,'evidence':'questions.json; graph visually inspected in graphs-4.png','reason':'The point is identified by its label and location on the shared curve; coordinates for B/C are not specified.'}} for label in 'ABCD']
  mapping=[{'old_answer':a[':db/id'],'old_value':a[':answer/value'],'selected':re.findall(r'\$([A-D])\$',a[':answer/value'])} for a in fs[0][':answer-field/choices']]
  row.update(decision='convert',objects=objects,choice_mapping=mapping,proof='A is the lowest point on the full closed-domain graph; C is a higher local minimum, B is a local maximum, D the global maximum.',problem_after=q[':question/problem']+'\n\nSelect all that apply.')
 elif eid==17592186238006:
  none=next(f for f in fs if f[':answer-field/key']=='None of the above')
  assert none[':answer-field/correct'][':answer/value']=='false'
  row.update(decision='remove_redundant_none',reason='None is represented by an empty subset, not a separate checkbox.',removed_field=none,objects=[{'source_label':str(i+1),'content':f[':answer-field/key'],'field_id':f[':answer-field/id'],'selected':f[':answer-field/correct'][':answer/value']=='true'} for i,f in enumerate(fs) if f is not none],problem_after=q[':question/problem'])
 elif eid in INTERVALS:row.update(decision='retain_radio',reason='Whole intervals or interval unions are mutually exclusive descriptions of the requested set. Inventing a partition into selectable atoms would redesign the response rather than convert an existing finite list.')
 elif eid in GRAPHS:row.update(decision='retain_radio',reason='Single whole-graph alternatives, not combination options or a requested finite subset; retain the existing single-graph response contract.')
 elif any(f[':answer-field/type'][':db/ident'].endswith('/checkbox') for f in fs):row.update(decision='retain_checkbox',reason='Already represented as independently selectable objects.')
 elif fs:row.update(decision='retain_entry',reason='Existing numerical entry structure is not a finite-subset radio task.')
 else:row.update(decision='retain_canonical',reason='Canonical worked example has no answer fields to convert.')
 if row['decision']=='convert':
  f=fs[0];row['database_key']=f.get(':answer-field/correct');row['correct_labels']=[o['source_label'] for o in row['objects'] if o['selected']]
  if row['database_key']:
   choice=next(c for c in row['choice_mapping'] if c['old_answer']==row['database_key'][':db/id']);assert set(choice['selected'])==set(row['correct_labels'])
   row['key_evidence']='Existing database key, stored worked solution and independently inspected graph.'
  else:
   row['key_evidence']='Missing original key independently established from the graph; a matching original radio alternative exists. Old detached field remains unchanged.'
   row['missing_key_resolved']=True
  assert all(set(c['selected'])<={o['source_label'] for o in row['objects']} for c in row['choice_mapping'])
 ledger.append(row)
(H/'case-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
from collections import Counter
counts=dict(Counter(r['decision'] for r in ledger));(H/'resolutions.json').write_text(json.dumps({'scope':29,'decisions':counts,'missing_keys_resolved':[r['question_eid'] for r in ledger if r.get('missing_key_resolved')],'database_writes':0},indent=2)+'\n');print(counts)
