import json, threading, tempfile
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from scripts.config import Config
from scripts.database.client import EDBClient
root=Path('/home/jake/Developer/Course_Academy')
manifest=json.loads((root/'reference/mathacademy/capture-audits/2026-10-11-backlog-repairs/paused-backlog-drain.json').read_text())
mids=set(); package_counts={}
for row in manifest['captures']:
    data=json.loads((Path(row['directory'])/'content.json').read_text())
    own={q['math_academy_id'] for q in data.get('questions',[])+data.get('canonical_examples',[]) if q.get('math_academy_id')}
    mids.update(own); package_counts[Path(row['directory']).name]=len(own)
client=EDBClient(Config(account='foundations',capture_only=True),threading.Event())
status=client.status(); basis=status['basis']; directory=Path(tempfile.mkdtemp(prefix='finite37-duplicates-'))
query='''[:find ?mid ?f ?key ?type ?value ?a :in $ [?mid ...] :where [?q :question/math-academy-id ?mid] [?q :question/answer-fields ?f] [?f :answer-field/key ?key] [?f :answer-field/choices ?a] [?a :answer/type ?type] [?a :answer/value ?value]]'''
found_query='[:find ?mid :in $ [?mid ...] :where [?q :question/math-academy-id ?mid]]'
ordered=sorted(mids); batches=[ordered[i:i+100] for i in range(0,len(ordered),100)]
def read(item):
    i,group=item
    rows=client.query(query,[group],directory,'choices-'+str(i),basis)
    found=client.query(found_query,[group],directory,'found-'+str(i),basis)
    return rows,found
with ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(read,enumerate(batches)))
groups=defaultdict(set); found=set()
for rows,found_rows in results:
    for row in rows:
        mid,field,key,typ,value,answer=row
        groups[(mid,field,key,typ,value)].add(answer)
    found.update(row[0] for row in found_rows)
duplicates=[{'mid':key[0],'field':key[1],'key':key[2],'type':key[3],'value':key[4],'answers':sorted(values)} for key,values in groups.items() if len(values)>1]
ids=sorted({a for group in duplicates for a in group['answers']})
owners=client.query('[:find ?a ?owner :in $ [?a ...] :where [?owner :task-item/responses ?a]]',[ids],directory,'duplicate-owners',basis) if ids else []
owned_ids={row[0] for row in owners}
for group in duplicates: group['owned_answers']=[eid for eid in group['answers'] if eid in owned_ids]
report={'status':status,'manifest_count':len(manifest['captures']),'question_ids':len(mids),'found_question_ids':len(found),'missing_question_ids':sorted(mids-found),'choice_groups':len(groups),'duplicate_groups':duplicates,'response_owned_duplicate_groups':sum(bool(d['owned_answers']) for d in duplicates),'artifact_directory':str(directory),'package_counts':package_counts}
(directory/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
