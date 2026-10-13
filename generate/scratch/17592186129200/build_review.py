"""Build a human review from preserved originals and validated generated records."""
import json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
source=json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions'];variants=json.loads((HERE/'review.json').read_text());raw=json.loads((HERE/'raw-replay.json').read_text())
def native_images(s):return re.sub(r'!\[\]\((images/[^)]+)\)',lambda m:'![](/media/jake/SSD/EDB/math/'+m[1]+')',s)
def record(q):
 f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'];correct=correct[1] if isinstance(correct,list) else correct[':answer/id']
 bank='\n'.join('- $'+v[':answer/value']+'$'+(' **correct**' if v[':answer/id']==correct else '') for v in f[':answer-field/choices'])
 return native_images(q[':question/problem'])+'\n\n'+bank+'\n\n'+native_images(q[':question/worked-solution'])+'\n\n'
out=['# Source and generated review\n\nAll nine originals, all observed banks and two labeled authored variants per template (18 variants, each level represented). Original source mathematical errors remain visible below and in public observed_raw evidence replay. Normal teaching uses supported corrections.\n\n']
for src in source:
 sid=src[':question/math-academy-id'];out+=['## Original '+sid+'\n\n',record(src)]
 for r in raw:
  if sid in r['generation']['source_ids']:
   out+=['### Public observed_raw replay '+r['generation']['template']+'\n\nParameters: `'+str(r['generation']['parameters'])+'`. Historical mathematical errors are deliberately retained, with balanced normalized TeX.\n\n',record(r['question'])]
 for r in variants:
  if sid in r['generation']['source_ids']:
   out+=['### Authored variant '+r['generation']['template']+' / '+r['question'][':question/difficulty'].rsplit('/',1)[1]+'\n\nParameters: `'+str(r['generation']['parameters'])+'`; complete authored profile; metadata is not learner content.\n\n',record(r['question'])]
(HERE/'review.md').write_text(''.join(out))
