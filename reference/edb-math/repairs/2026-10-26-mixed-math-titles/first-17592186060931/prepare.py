import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path[:0]=[str(R/'scripts'),str(H.parent)]
from bs4 import BeautifulSoup
from migrate_learner_history import connection,kw,dumps
from question_capture.math_format import MATH
from reconstruct import reconstruct
assert not(H/'commit-intent.json').exists()
db=connection();basis=db.basis();before=db.query('[:find ?v :in $ ?e :where [?e :tutorial/content ?v]]',[17592186060931],H,'before',basis)[0][0]
source=Path('/home/jake/Developer/MA/DATA/Lessons/152/Source/152.html');step=BeautifulSoup(source.read_text(),'html.parser').find(id='step-16233');titles=[svg.find('title')for svg in step.select('svg')];math=list(MATH.finditer(before));edits=[]
for index in [1,3,4]:
 title=titles[index];tex=reconstruct(title);old=math[index];assert ('a & b'in old[0])if index in [1,3]else('2 & 1'in old[0]);edits.append({'span':[old.start(),old.end()],'before':old[0],'after':'$$\n\\displaystyle '+tex+'\n$$','source_title':str(title),'recovered_tex':tex})
after=before
for e in reversed(edits):s,z=e['span'];after=after[:s]+e['after']+after[z:]
field={'entity':17592186060931,'attribute':'tutorial/content','before':before,'after':after,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest()}
(H/'fields.json').write_text(json.dumps([field],indent=2)+'\n');(H/'edits.json').write_text(json.dumps(edits,indent=2)+'\n');payload=dumps([[kw('db/cas'),field['entity'],kw(field['attribute']),before,after]])+'\n';(H/'transaction.edn').write_text(payload);(H/'preparation.json').write_text(json.dumps({'basis':basis,'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sha256':hashlib.sha256(payload.encode()).hexdigest(),'entity':17592186060931,'restored_formulas':3},indent=2)+'\n');print(after[:1100])
