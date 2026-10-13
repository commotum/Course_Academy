"""One-time extraction of complete source math components into reusable masks."""
import json,re,pathlib
D=pathlib.Path(__file__).resolve().parent
p=json.load(open(D.parents[1]/'runs/current/sources/17592186092217.json'))
(D/'source.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n')
qs=p['record'][':knowledge-point/questions']
config={
'q-8513':('legacy_radian_radio','easy','4','1/4','radians'),
'q-8521':('legacy_degree_radio','moderate','8','240','degrees'),
'q-120311':('degree_radio','moderate','4','225','degrees'),
'q-276511':('axis_radian_blank','easy','2','1/2','radians'),
'q-276514':('radian_blank','easy','4','7/6','radians'),
'q-276774':('degree_blank','easy','2','300','degrees'),
'q-8519':('degree_repeated_radio','easy','6','45','degrees')}
recipes={};cases=[]
for q in qs:
 sid=q[':question/math-academy-id'];t,level,r,a,u=config[sid]
 # The tuple is a whole mathematical component, never a scalar search/replace.
 prompt=q[':question/problem'];m=re.search(r'\$\(([^$]+)\)',prompt)
 polar=m.group(0)[1:];prompt=prompt[:m.start()+1]+'{{polar}}'+prompt[m.end():]
 rec={'template':t,'source_id':sid,'level':level,'parameters':{'radius':r,'angle':a,'unit':u},'prompt_mask':prompt,'angle_original':polar.split(',',1)[1].strip(),'fields':[]}
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution']
  blocks=list(re.finditer(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S))
  for bi,block in reversed(list(enumerate(blocks))):
   rows=block.group(1).split('\\\\');masked=[]
   for ri,row in enumerate(rows):
    if ri==0: masked.append(row);continue
    mm=re.search(r'(.*?&\s*=)(.*)',row,re.S);token=('x' if bi==0 else 'y')+'_'+['','sub','mul','final'][ri]
    whitespace=re.match(r'\s*',mm.group(2)).group();trail=re.search(r'\s*$',mm.group(2)).group()
    masked.append(mm.group(1)+whitespace+'{{'+token+'}}'+trail)
   sol=sol[:block.start(1)]+'\\\\'.join(masked)+sol[block.end(1):]
  sol=re.sub(r'(are \$)\([^$]*\)(\.\$)',r'\1{{cartesian}}\2',sol)
  rec['solution_mask']=sol
 for f in q[':question/answer-fields']:
  rec['fields'].append({'key':f.get(':answer-field/key'),'type':f[':answer-field/type'][':db/ident'],'correct_present':':answer-field/correct' in f,'answer_type':f[':answer-field/choices'][0][':answer/type'][':db/ident'],'choice_count':len(f[':answer-field/choices'])})
 rec['difficulty_present']=':question/difficulty' in q
 recipes[t]=rec
 cases.append({'source_id':sid,'template':t,'level':level,'parameters':rec['parameters'],'bank_profile':'raw-'+sid})
(D/'recipes.json').write_text(json.dumps(recipes,indent=2,ensure_ascii=False)+'\n')
(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
