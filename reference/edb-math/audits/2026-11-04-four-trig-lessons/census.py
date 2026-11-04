"""Inventory all captured content without changing database state."""
import collections,json,re
from pathlib import Path
H=Path(__file__).resolve().parent
kps=json.loads((H/'kps.json').read_text());topics=json.loads((H/'capture.json').read_text())['topics'];owner={k[':db/id']:t[0][':db/id'] for t in topics for k in t[0][':topic/knowledge-points']}
rows=[];summary=[]
for kid,k in kps.items():
    counts=collections.Counter();missing=[];path=H/'kps'/kid/'questions.txt';out=[]
    for role,q in [('canonical',k[':knowledge-point/canonical-example'])]+[('practice',q) for q in k.get(':knowledge-point/questions',[])]:
        origin='imported' if q.get(':question/math-academy-id') else 'generated';band=q.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1];fields=q.get(':question/answer-fields',[]);solution=q.get(':question/worked-solution','');problem=q.get(':question/problem','')
        keys=[f.get(':answer-field/correct',{}).get(':answer/value') for f in fields];types=[f.get(':answer-field/type',{}).get(':db/ident','').split('/')[-1] for f in fields]
        row={'entity':q[':db/id'],'kp':int(kid),'topic':owner[int(kid)],'role':role,'origin':origin,'band':band,'retired':q.get(':question/retired',False),'field_types':types,'key_complete':bool(fields) and all(v is not None for v in keys),'solution_present':bool(solution.strip()),'prompt':problem,'keys':keys,'solution':solution}
        rows.append(row);counts[role+'/'+origin+'/'+band]+=1
        if not row['key_complete'] or not row['solution_present']:missing.append(q[':db/id'])
        out += [f"ID={q[':db/id']} {role} {origin} {band} retired={row['retired']} fields={','.join(types)}",problem.replace('\n',' '), 'KEYS '+json.dumps(keys,ensure_ascii=False),'SOLUTION '+solution.replace('\n',' '),'']
    path.write_text('\n'.join(out)+'\n');summary.append({'kp':int(kid),'title':k[':knowledge-point/title'],'topic':owner[int(kid)],'counts':dict(counts),'incomplete_records':missing})
(H/'question-ledger.json').write_text(json.dumps(rows,indent=2)+'\n');(H/'census.json').write_text(json.dumps({'basis':json.loads((H/'capture.json').read_text())['basis'],'kps':summary,'questions_and_examples':len(rows),'practice_questions':sum(r['role']=='practice' for r in rows),'canonical_examples':sum(r['role']=='canonical' for r in rows),'retired_linked_records':sum(r['retired'] for r in rows)},indent=2)+'\n')
for s in summary:print(s['kp'],s['title'],s['counts'],'incomplete',s['incomplete_records'])
print('all records',len(rows))
