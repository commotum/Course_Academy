import json,sys
from pathlib import Path
b=Path(__file__).parent.parent
orig={}
for folder in ['prose','compound']:
 for r in map(json.loads,(b/folder/'reviews.jsonl').read_text().splitlines()):orig[r['id']]=r
decisions=json.loads(sys.argv[1]);out=[]
for q,d in decisions.items():
 r=orig[q];directory=r['directory'];s=json.loads(Path(directory,'state.json').read_text())['questions'][q];json.loads(Path(directory,'content.json').read_text());sf='history' if s.get('history',{}).get('worked_solution') else 'after';sol=s[sf]['worked_solution'];loc=dict(file=str(Path(directory,'state.json')),json_pointer=f'/questions/{q}/{sf}/worked_solution')
 evidence=dict(prompt=s['before']['problem'],original_fields=[dict(key=f['key'],choices=[{k:ch[k] for k in ['type','value']} for ch in f.get('choices',[])]) for f in s['before']['fields']],worked_solution=sol,source_location=loc,independent_check=d['check'])
 row=dict(id=q,confirmed_hold=d['confirmed'],reason=d['reason'],explanation=d['explanation'],source_evidence=evidence)
 if 'indices' in d:
  fields=[]
  assert len(d['indices'])==len(s['before']['fields'])
  for f,i in zip(s['before']['fields'],d['indices']):
   ch=f['choices'][i];fields.append(dict(key=f['key'],choice_index=i,answer={k:ch[k] for k in ['type','value']},binding=s['before']['problem'],source_quote=sol,source_location=loc,method=d['method']))
  row['resolve_record']=dict(id=q,ready=True,directory=directory,fields=fields,situation_types=d.get('types',[]),disagreements=d.get('disagreements',[]),revision_reason=d['explanation'])
 out.append(row)
with (b/'math'/'hold-peer-review.jsonl').open('a') as f:
 for row in out:f.write(json.dumps(row,ensure_ascii=False)+'\n')
print('Peer checkpoint',len(out))
