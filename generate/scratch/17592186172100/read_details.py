from context import *
import re
from PIL import Image,ImageOps,ImageDraw
src=json.loads((HERE/'source.json').read_text());kp=src['record'];basis=src['basis']
query='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
(or-join [?q ?l] (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
(and [?l :learner/activity ?t] [?t :learner-task/status ?status]
(or [?status :db/ident :learner-task.status/unlocked] [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
[?t :learner-task/activity ?a] [?a :activity/steps ?s] [?s :step/content ?q]))]'''
(HERE/'reference/usage-query.edn').write_text(query)
used=DB.query(query,[KP,LEARNER],HERE/'reference/read-before','usage',basis)
history=DB.query(query,[KP,LEARNER],HERE/'reference/read-before','historical-usage',basis,history=True)
print('Unavailable',used,history)
assets=[];sheet=Image.new('RGB',(1500,900),'white');d=ImageDraw.Draw(sheet)
for i,q in enumerate(kp[':knowledge-point/questions']):
 refs=re.findall(r'!\[.*?\]\((.*?)\)',q[':question/worked-solution'])
 print(q[':question/math-academy-id'],'CORRECT',q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'])
 for ref in refs:
  path=Path(ENV['EDB_MATH_ROOT'])/ref
  im=Image.open(path).convert('RGB');im.thumbnail((285,400));x=(i%5)*300;y=(i//5)*450
  sheet.paste(im,(x,y+35));d.text((x+5,y+5),q[':question/math-academy-id'],fill='black');assets.append({'source':q[':question/math-academy-id'],'path':ref,'dimensions':Image.open(path).size})
sheet.save(HERE/'reference/source-diagrams.png');save(HERE/'reference/assets.json',assets)
