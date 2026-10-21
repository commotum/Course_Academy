"""Affected source-description check and small numeric/response invariance sample."""
import copy,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import validate_repair as c

def main():
 records=[];witness=[]
 # This reruns all 17 inexpensive source comparisons and refreshes the replay report.
 replays=c.source_replays();records.append(replays[-1])
 for name,n in [('q-74637',2),('q-131720',3),('q-74638',2)]:
  r=c.g.generate('moderate',template=name,parameters={'scales':[-2]+[1]*(n-1),'translations':[1]*n});c.mathematical(r);records.append(r)
 samples=json.loads((c.E/'test-records.json').read_text());seen=set()
 for a in samples:
  if not a['question'][':question/difficulty'].endswith('/moderate'):continue
  m,kind,_=c.mathematical(a);group=(m.rows,m.cols,a['generation']['response_layout'])
  if group in seen:continue
  seen.add(group);p=copy.deepcopy(a['generation']['parameters'])
  # Translate x by one: b' = b - A[:,0], preserving every consistency/rank decision.
  changed=m.copy();changed[:,-1]=m[:,-1]-m[:,0];p['matrix']=[[str(x) for x in row] for row in changed.tolist()]
  b=c.g.generate('moderate',a['generation']['seed'],template=a['generation']['template'],parameters=p);_,after,_=c.mathematical(b);assert after==kind
  def truth(r):
   q=r['question'];return sorted((f[':answer-field/key'],next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id']==f[':answer-field/correct'][1])) for f in q[':question/answer-fields'])
  assert truth(a)==truth(b);assert a['question'][':question/problem']!=b['question'][':question/problem'];records.extend([a,b]);witness.append({'template':a['generation']['template'],'group':group,'classification':kind,'same_visible_response':True})
 fixtures=[{'label':str(i),'record':r,'checks':c.mathematical(r)[2]} for i,r in enumerate(records)];c.dump('final-focus-native-input.json',fixtures)
 subprocess.run([str(c.REPO/'generate/runs/current/check-engine'),str(c.E/'final-focus-native-input.json'),str(c.E/'final-focus-native-report.json')],check=True)
 c.dump('source-correction-render.json',[replays[-1]])
 c.dump('final-focus.json',{'passed':True,'source_replays':17,'native_records':len(records),'irrelevant_numeric_changes':witness,'source_correction':'q-74638 leading pivot is 3 and row has a nonzero second entry; echelon stage is not reduced echelon. Prompt, complete radio bank and mathematics unchanged.','command':'python checks/final_focus.py'})
 print(json.dumps({'passed':True,'source_replays':17,'native_records':len(records),'invariance_groups':len(witness)}))
if __name__=='__main__':main()
