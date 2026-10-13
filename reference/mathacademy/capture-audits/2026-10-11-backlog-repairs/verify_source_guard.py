"""Exercise correction preflight against a native immutable snapshot; no writes."""
from pathlib import Path
import threading
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.evidence import UnsupportedContent
from scripts.database.prepare import Preparation
from scripts.storage import atomic_json

root=Path(__file__).resolve().parent/'native-source-guard'
client=EDBClient(Config(),threading.Event());identity=client.status()
snapshot=client.snapshot({'questions':[{'math_academy_id':mid} for mid in ('q-79044','q-5538')]},root,identity['basis'])
prep=Preparation(snapshot);findings=[]
for mid in ('q-79044','q-5538'):
 question=prep.exact('question/math-academy-id',mid)
 try:prep.check_source_attribution(question);protected=False;reason=None
 except UnsupportedContent as error:protected=True;reason=str(error)
 assert protected==(mid=='q-79044'),(mid,protected,reason)
 findings.append({'id':mid,'protected':protected,'reason':reason})
atomic_json(root/'verification.json',{'identity':identity,'findings':findings,'database_writes':0})
print({'basis':identity['basis'],'findings':findings})
