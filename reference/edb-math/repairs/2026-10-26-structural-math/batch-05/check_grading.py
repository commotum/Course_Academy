"""Actual native grading, every affected bank and every selectable choice."""
import copy,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];changes={f['entity']:f['after']for f in json.loads((H/'fields.json').read_text())if f['attribute']=='answer/value'};out=[]
for original in json.loads((H/'answer-fields.json').read_text()):
 for side in ['before','after']:
  f=copy.deepcopy(original);cid=f.get(':answer-field/correct',{}).get(':answer/id')
  if cid:f[':answer-field/correct']=[':answer/id',cid]
  for a in f[':answer-field/choices']:
   if side=='after'and a[':db/id']in changes:a[':answer/value']=changes[a[':db/id']]
  assert f[':answer-field/type'][':db/ident']in (':answer-field.type/radio',':answer-field.type/select')
  f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
  q={':question/problem':'Preserved choice-bank fixture',':question/answer-fields':[f]}
  checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'unresolved'if cid is None else'accepted'if a[':answer/id']==cid else'rejected','purpose':'Preserve exact selection identity '+side+' matrix formatting'}for a in f[':answer-field/choices']]
  out.append({'label':str(original[':db/id'])+':'+side,'record':{'question':q,'knowledge_point':{'title':'Matrix layout fidelity'},'generation':{'template':'existing-selection-identities'}},'checks':checks})
(H/'native-grading-input.json').write_text(json.dumps(out,indent=2)+'\n');subprocess.run([str(R/'.local/edb/html-table-repair/check-engine'),str(H/'native-grading-input.json'),str(H/'native-grading.json')],check=True);print('Verified',len(out)//2,'existing banks before and after;',sum(len(x['checks'])for x in out),'native grading checks.')
