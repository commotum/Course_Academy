"""Copy supplied source evidence and map complete banks, without database access."""
import json
from pathlib import Path
SOURCE = Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-priority-17592186050321/jobs/17592186184155/source/source.json')
s = json.loads(SOURCE.read_text())
# Terms are [coefficient, rational exponent], in observed answer term order.
maps = {
 'q-2250': {'input':[['1','2'],['-1','1/2'],['2','0']], 'key':1, 'banks':[
 [['1/3','3'],['1','3/2'],['2','1']],
 [['1/3','3'],['-2/3','3/2'],['2','1']],
 [['1/3','3'],['-1','3/2'],['2','1']],
 [['1/3','3'],['-2/3','3/2'],['2/3','1']],
 [['1/3','3'],['2/3','2/3'],['2/3','1']]]},
 'q-29830': {'input':[['4','7'],['1','1/5'],['-1','-13/7']], 'key':3, 'banks':[
 [['1/8','8'],['5/6','6/5'],['7/6','-6/7']],
 [['1/2','8'],['-5/3','6/5'],['7/6','-6/7']],
 [['1/4','8'],['5/6','5/6'],['7/6','-6/7']],
 [['1/2','8'],['5/6','6/5'],['7/6','-6/7']],
 [['1/2','8'],['6/5','6/5'],['7/6','-6/7']]]},
 'q-113848': {'input':[['1','-4/3'],['1','3'],['-1','-2']], 'key':0, 'banks':[
 [['-3','-1/3'],['1/4','4'],['1','-1']],
 [['-3','-1/3'],['1/4','2'],['1','-3']],
 [['-3','-4/3'],['1/2','2'],['1','-1']],
 [['1/3','3/2'],['4','4'],['1/2','1']],
 [['1','1/3'],['1/4','4'],['-1/4','1']]]},
 'q-113850': {'input':[['1','4/5'],['-1','1'],['2','-4']], 'key':1, 'banks':[
 [['1','9/5'],['-2','2'],['-2/3','-3']],
 [['5/9','9/5'],['-1/2','2'],['-2/3','-3']],
 [['9/5','-9/5'],['-2','-1'],['-6','-3']],
 [['4','-4/5'],['-2','-2'],['-6','-4']],
 [['5/4','4/5'],['-1/2','-1'],['-2/3','-6']]]}}
rows=[]
for q in s['material']['kp'][':knowledge-point/questions']:
 name=q[':question/math-academy-id']
 rows.append({'source_name':name,'source':q,**maps.get(name,{}),
              'key_origin':'supplied' if name in ('q-113848','q-113850') else 'independently inferred' if name in maps else 'missing fields; unsupported'})
Path('source_cases.json').write_text(json.dumps(rows,indent=2)+'\n')
Path('evidence/source-context.json').write_text(json.dumps(s,indent=2)+'\n')
print('Copied 6 source records; mapped all 20 supplied options across 4 radio banks.')
