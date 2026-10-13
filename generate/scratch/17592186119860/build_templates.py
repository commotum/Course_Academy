import json,re,shutil
from pathlib import Path
D=Path(__file__).parent
raw=json.load(open('generate/runs/current/sources/17592186119860.json'));(D/'source.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n')
config={
'q-33759':('log_square','moderate',1,'E',['log(t)','2*t','t**2'],'1/t+2*t'),
'q-33779':('product_trig','moderate',1,3,['cos(t)+t*sin(t)','sin(t)-t*cos(t)','sqrt(3)*t**2/2'],'2*t'),
'q-127635':('poly_negative','easy',-1,0,['2*t','t**3/3','t**2'],'t**2+2'),
'q-76906':('quadratic_two','easy',0,2,['t**2','4','t**2'],'2*sqrt(2)*t'),
'q-76908':('poly_ordered','easy',0,3,['t','t**2','2*t**3/3'],'1+2*t**2'),
'q-76914':('chain_product','hard',0,2,['2*t*cos(2*t)-sin(2*t)','3*t**2/2','2*t*sin(2*t)+cos(2*t)'],'5*t'),
'q-77064':('poly_constant','easy',0,3,['10','t**3/3-t','t**2'],'t**2+1'),
'q-127633':('helix','easy',0,1,['t','sin(t)','cos(t)'],'sqrt(2)'),
'q-76909':('quadratic_three','easy',0,4,['2-t**2','t**2+4','t**2/2'],'3*t'),
'q-76910':('poly_radical','easy',0,5,['(4-sqrt(3)*t**2)/sqrt(2)','t**3','t+5'],'1+3*t**2'),
}
rows={}
for q in raw['record'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];name,level,a,b,curve,speed=config[sid];problem=q[':question/problem'];worked=q.get(':question/worked-solution','')
 # Slot only full endpoint components. Preserve curve, prose and every row.
 problem=re.sub(r'(from\s+\$t\s*=\s*)([^$]+)(\$ to \$t\s*=\s*)([^$]+)\$',lambda m:m[1]+'@a@'+m[3]+'@b@'+('.' if m[4].endswith('.') else '')+'$',problem)
 worked=re.sub(r'(?<=_{)'+str(a)+r'(?=}\^{)', '@a@',worked)
 worked=worked.replace('_{@a@}^{'+str(b)+'}', '_{@a@}^{@b@}')
 worked=worked.replace(f'[{a},{b}]','[@a@,@b@]')
 # Endpoint arithmetic is an explicit structural slot: preserve row count.
 if worked:
  start=worked.rfind('\\begin{aligned}L');prefix=worked[:start];block=worked[start:];r=block.split(' \\\\  & =')
  # All rows after the antiderivative bound row are numeric endpoint stages.
  numeric=next(i+1 for i,x in enumerate(r) if '|}_{@a@}' in x or '|_{@a@}' in x)
  for i in range(numeric,len(r)):r[i]='@endpoint'+str(i-numeric)+'@'+('\\end{aligned}\n$$' if i==len(r)-1 else '')
  worked=prefix+' \\\\  & ='.join(r)
 else: numeric=0
 choices=[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]
 rows[name]={'source_id':sid,'level':level,'a':a,'b':b,'curve':curve,'speed':speed,'problem':problem,'solution':worked,'numeric_rows':len(r)-numeric if worked else 0,'choice_shapes':choices}
 for image in re.findall(r'!\[\]\((.*?)\)',q[':question/problem']):
  target=D/image;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(Path('/media/jake/SSD/EDB/math')/image,target)
(D/'templates.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print([(k,x['numeric_rows']) for k,x in rows.items()])
