from review import *
import importlib.util,collections,math
s=importlib.util.spec_from_file_location('gen',PK/(KP+'.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
rs=[]
for name,level,scale in [('q-96476','moderate',.5),('q-119372','moderate',-1),('q-98229','hard',-1),('q-98231','hard',1.5)]:rs.append(g.generate(level,seed=7146,profile=name,parameters={'scale':scale}))
p={'a':-2,'b':-2,'c':0,'px':1,'py':1,'orientation':'x','single':'exp'}
for t in ['impossible_x','impossible_y']:rs.append(g.generate('hard',seed=69247,template=t,parameters=p))
dump('boundary-records.json',rs)
checks=[];grader=[]
for i,r in enumerate(rs):
 f=r['question'][':question/answer-fields'][0];out=[]
 for a in f[':answer-field/choices']:
  d=json.loads(pathlib.Path(a[':answer/value']).with_suffix('.json').read_text());rows=collections.defaultdict(list);cols=collections.defaultdict(list)
  for x,y,m in d['points']:rows[y].append(m);cols[x].append(m)
  varies_x=any(max(ms)-min(ms)>1e-7 for ms in rows.values());varies_y=any(max(ms)-min(ms)>1e-7 for ms in cols.values());qualifies=(varies_x and varies_y)==r['generation']['template'].startswith('possible');iskey=a[':answer/id']==f[':answer-field/correct'][1]
  out.append({'choice_id':a[':answer/id'],'varies_x':varies_x,'varies_y':varies_y,'key_matches':qualifies==iskey})
 checks.append({'question_id':r['question'][':question/id'],'profile':r['generation']['bank_profile'],'parameters':r['generation']['parameters'],'images':out})
 grader.append({'label':'boundary '+str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independent grid invariance/outlier classification'} for a in f[':answer-field/choices']]})
dump('boundary-results.json',checks);dump('boundary-grader-input.json',grader)
print('boundary records',len(rs),'key mismatches',sum(not x['key_matches'] for c in checks for x in c['images']))
