import json,sys,pathlib,importlib.util,re,collections,subprocess
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent;P=R.parent/'workspace';repo=pathlib.Path('/home/jake/Developer/Course_Academy')
spec=importlib.util.spec_from_file_location('g',P/'17592186100988.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(p,x):(R/p).write_text(json.dumps(x,indent=2))
def parse(r):
 q=r['question'];p=q[':question/problem'];m=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',p,re.S);a=[[int(v.strip()) for v in row.split('&')] for row in m[1].split(r'\\')];ix=re.search(r'_\{(\d)(\d)\}',p);i,j=map(int,ix.groups());return a,i,j,str(a[i-1][j-1]) if i<=len(a) and j<=len(a[0]) else 'No such entry'
def cases(rows):
 d={}
 for r in rows:
  f=r['question'][':question/answer-fields'][0]
  if not any(a[':answer/value']=='No such entry' for a in f[':answer-field/choices']):continue
  p=r['question'][':question/problem'];style='inline' if '$$' not in p else 'display';v=parse(r)[3];z=d.setdefault(style,{'valid':0,'absent':0});z['absent' if v=='No such entry' else 'valid']+=1
 return d
boundary=[]
for i in range(1,4):
 for j in range(1,3):
  r=g.generate('easy',seed=7783,profile='four_locations',parameters={'matrix':[[-3,-2],[-1,0],[1,2]],'i':i,'j':j,'letter':'C'});a,ri,rj,v=parse(r);f=r['question'][':question/answer-fields'][0];assert len(set(x[':answer/value'] for x in f[':answer-field/choices']))==5;assert next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id']==f[':answer-field/correct'][1])==v;boundary.append(r)
save('numeric-3x2-records.json',boundary)
# New batch algorithm: exact previous seed plus independent seeds/counts; actual delivery for combined controls.
batches=[]
for seed,count in [(4036014606,5),(8921,2),(8922,3),(8923,4),(8924,5),(8925,6)]:
 rows=g.generate_batch('easy',seed,count);assert rows==g.generate_batch('easy',seed,count)
 d=cases(rows);assert all(z['valid'] and z['absent'] for z in d.values()),(seed,d)
 batches.append({'seed':seed,'count':count,'cases':d,'records':rows})
save('batch-rule-tests.json',batches)
rows=boundary+[r for b in batches for r in b['records']];save('changed-rule-records.json',rows)
cmd=[sys.executable,str(repo/'generate/pipeline/check_delivery.py'),'--input',str(R/'changed-rule-records.json'),'--source',str(R.parent/'source/source.json'),'--inventory',str(R.parent/'source/inventory.json'),'--difficulty','easy','--output',str(R/'delivery-changed'),'--asset-root',str(R),'--math-root','/media/jake/SSD/EDB/math']
p=subprocess.run(cmd,capture_output=True,text=True);assert p.returncode==0,p.stderr
after=json.load(open(R/'delivery-changed/accepted.json'))
for b in batches:
 delivered=[r for r in after if r['generation'].get('batch',{}).get('seed')==b['seed']];b['after_cases']=cases(delivered);b['delivered']=len(delivered);assert b['after_cases']==b['cases'];assert len(delivered)==b['count']
save('batch-rule-tests.json',batches)
# Native checks on added numeric-only boundaries, retaining original bank test.
grading=[]
for r in boundary:
 v=parse(r)[3];f=r['question'][':question/answer-fields'][0];grading.append({'record':r,'label':'3x2-'+str(parse(r)[1:3]),'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==v else 'rejected'} for a in f[':answer-field/choices']]})
save('changed-grader-input.json',grading)
save('changed-rule-results.json',{'numeric_3x2_targets':6,'batch_cases':[{'seed':b['seed'],'count':b['count'],'before':b['cases'],'after':b['after_cases']} for b in batches],'delivery_command':cmd,'passed':True})
print('Six 3x2 numeric-only targets and six deterministic batch constructions passed actual delivery.')
