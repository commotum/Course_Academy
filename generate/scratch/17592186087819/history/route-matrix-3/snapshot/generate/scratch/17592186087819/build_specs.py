import json,re,pathlib,shutil
HERE=pathlib.Path(__file__).parent
s=json.load(open(HERE/'source.json'))['record']
data=[('q-138940','easy',[[0,1,1],[0,1,2],[1,0,0]],[[0,1],[1,1],[1,2]]),('q-139685','easy',[[0,1,1],[0,0,1],[1,1,0]],[[0,0],[1,0],[2,1]]),('q-139689','moderate',[[1,1,0],[0,1,2],[0,1,0]],[[0,1],[1,1],[2,0]]),('q-139719','easy',[[0,1,0,2],[0,0,1,0],[0,0,0,1],[0,0,1,0]],[[0,3],[1,2],[2,2]]),('q-319346','easy',[[0,2,0],[1,0,3],[2,0,0]],[[0,1],[1,0],[1,2]]),('q-319412','easy',[[0,1,2,0],[2,0,1,0],[1,0,0,2],[0,1,1,0]],[[0,2],[1,0],[2,2]]),('q-319429','easy',[[1,1,3],[1,2,2],[0,1,1]],[[0,2],[1,1],[2,1]])]
specs={};cases=[]
for id,level,m,holes in data:
 q=next(q for q in s[':knowledge-point/questions'] if q[':question/math-academy-id']==id)
 name=('sum_' if len(q[':question/answer-fields'])==1 else 'blanks_')+id[2:]
 asset=re.search(r'!\[\]\((.*?)\)',q[':question/problem']).group(1)
 out=HERE/asset;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(pathlib.Path('/media/jake/SSD/EDB/math')/asset,out)
 specs[name]={'source':id,'level':level,'matrix':m,'holes':holes,'asset':asset,'row_order':list(range(len(m))),'col_order':list(range(len(m)))}
 profile='observed_'+id[2:] if name.startswith('sum') else 'observed'
 cases.append({'source_id':id,'template':name,'level':level,'parameters':{'matrix':m,'holes':holes,'row_order':list(range(len(m))),'col_order':list(range(len(m)))},'bank_profile':profile})
(HERE/'specs.json').write_text(json.dumps(specs,indent=2)+'\n');(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
