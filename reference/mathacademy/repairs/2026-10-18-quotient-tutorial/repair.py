"""Repair the quotient-rule tutorial's two equation chains, preserving prose."""
import hashlib,json,re,threading
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient
from capture.scripts.database.edn import dumps,loads,kw
HERE=Path(__file__).resolve().parent
ENTITY=17592186065337
SOURCE=':agent/codex'
FIRST=r'''$$
\begin{aligned}
\dfrac{a^5}{a^2} &= a^{5-2} \\
&= a^3.
\end{aligned}
$$'''
SECOND=r'''$$
\begin{aligned}
\dfrac{a^5}{a^2} &= \dfrac{a \cdot a \cdot a \cdot a \cdot a}{a \cdot a} \\
&= \dfrac{\cancel{a} \cdot \cancel{a} \cdot a \cdot a \cdot a}{\cancel{a} \cdot \cancel{a}} \\
&= a \cdot a \cdot a \\
&= a^3.
\end{aligned}
$$'''
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def prepare():
 old=json.loads((HERE/'before.json').read_text())[0][0][':tutorial/content']
 blocks=list(re.finditer(r'\$\$.*?\$\$',old,re.S));assert len(blocks)==3
 new=old[:blocks[2].start()]+SECOND+old[blocks[2].end():]
 new=new[:blocks[1].start()]+FIRST+new[blocks[1].end():]
 assert re.sub(r'\$\$.*?\$\$','',old,flags=re.S)==re.sub(r'\$\$.*?\$\$','',new,flags=re.S)
 assert r'\require' not in new and r'\eqalign' not in new
 assert new.count(r'\cancel{a}')==4
 (HERE/'after.md').write_text(new+'\n');save('change.json',{'entity':ENTITY,'attribute':':tutorial/content','before':old,'after':new})
 q={':question/problem':new,':question/worked-solution':'',':question/answer-fields':[{':answer-field/key':'preview',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/id':'0',':answer/type':':answer.type/math',':answer/value':'0'}],':answer-field/correct':[':answer/id','0']}]}
 save('render-input.json',[{'question':q}])
 forms=[[kw(':db/cas'),ENTITY,kw(':tutorial/content'),old,new],[kw(':db/ensure'),ENTITY,kw(':tutorial/validate')]]
 (HERE/'transaction.edn').write_text(dumps(forms)+'\n')
 print('Prepared two corrected equation blocks; prose and cancellation steps preserved.')
def commit():
 db=EDBClient(Config(),threading.Event());change=json.loads((HERE/'change.json').read_text());tx=HERE/'transaction.edn'
 assert json.loads((HERE/'ui/rendering.json').read_text())['passed']
 attrs={str(i):e for e,i in loads((HERE.parent/'2026-10-18-big-parentheses/evidence/idents.edn').read_text())}
 def check(report):
  datoms=report[':edb/tx-data'];assert len(datoms)==3 and not report[':edb/tempids']
  content=[(e,v,added) for e,a,v,t,s,added in datoms if a==attrs[':tutorial/content']]
  assert set(content)=={(ENTITY,change['before'],False),(ENTITY,change['after'],True)}
  assert all(s==attrs[SOURCE] for e,a,v,t,s,added in datoms)
 intent=HERE/'request.json'
 if intent.exists():request=json.loads(intent.read_text())
 else:
  preview=db.command('with','--file',tx,'--source',SOURCE,timeout=150);(HERE/'preview.edn').write_text(preview)
  report=loads(preview);assert report[':edb/committed'] is False;check(report)
  assert db.status()['lineage']==json.loads((HERE/'identity.json').read_text())['lineage']
  digest=hashlib.sha256(tx.read_bytes()).hexdigest();basis=report[':edb/db-before-t']
  request={'source':SOURCE,'basis':basis,'sha256':digest,'request_key':'quotient-tutorial-v1-b'+str(basis)+'-'+digest};save('request.json',request)
 assert hashlib.sha256(tx.read_bytes()).hexdigest()==request['sha256']
 if not (HERE/'receipt.edn').exists():
  result=db.command('transact','--file',tx,'--source',request['source'],'--basis',request['basis'],'--endpoint',db.config.endpoint,'--request-key',request['request_key'],'--timeout-ms','120000',timeout=150);(HERE/'receipt.edn').write_text(result)
 report=loads((HERE/'receipt.edn').read_text());assert report[':edb/committed'] is True;check(report)
 rows=db.query('[:find (pull ?e [*]) :in $ ?e :where [?e :tutorial/id _]]',[ENTITY],HERE/'committed','tutorial',report[':edb/basis-t'])
 expected=json.loads((HERE/'before.json').read_text())[0][0];expected[':tutorial/content']=change['after']
 assert json.loads(json.dumps(rows[0][0],default=str))==expected
 result={'passed':True,'committed':True,'entity':ENTITY,'basis_before':report[':edb/db-before-t'],'basis_after':report[':edb/basis-t'],'changed_attributes':[':tutorial/content'],'prose_unchanged':True,'cancellation_preserved':True,'render_verified':True,'exact_readback':True};save('verification.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':
 import sys
 commit() if '--commit' in sys.argv else prepare()
