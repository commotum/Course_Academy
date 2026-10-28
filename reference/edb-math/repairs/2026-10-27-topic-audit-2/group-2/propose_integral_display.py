import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[4]/'scripts'));from question_capture.math_format import MATH
D=json.loads((H/'current.json').read_text());I=json.loads((H.parent/'inventory.json').read_text());topic={q:t for t,k,q in I['links']};out=[]
for q in D['questions']:
 if topic[q[':db/id']]!=17592186050929:continue
 p=q[':question/problem'];ms=list(MATH.finditer(p))
 if len(ms)!=1 or ms[0][0].startswith('$$')or r'\int'not in ms[0][0]:continue
 m=ms[0];after=p[:m.start()].rstrip()+'\n\n$$\n'+m[0][1:-1]+'\n$$'+p[m.end():]
 out.append({'entity':q[':db/id'],'attribute':'question/problem','before':p,'after':after.strip(),'reason':'Display standalone requested integral calculation, following user preference; preserve short inline references elsewhere','evidence':{'basis':9122,'single_math_problem':True,'identity':q.get(':question/math-academy-id')},'confidence':'high'})
(H/'integral-display-proposals.json').write_text(json.dumps(out,indent=2)+'\n');print(len(out))
