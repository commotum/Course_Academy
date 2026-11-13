"""Read-only E3 scope/progress capture; no learner or assignment mutation."""
import collections,json,re,sys,uuid
from pathlib import Path
ROOT=Path('/home/jake/Developer/Course_Academy');OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import connection

def save(name,value):
 (OUT/name).write_text(json.dumps(value,default=str,ensure_ascii=False,indent=2)+'\n')
def main():
 graph=json.loads((OUT/'graph-api.json').read_text());expanded=json.loads((OUT/'expanded-api.json').read_text());guide=json.loads((OUT/'guide-api.json').read_text());basis=graph['basis']
 assert expanded['basis']==basis==guide['basis']
 nodes={n['id']:n for n in graph['nodes']};by_uuid={n['uuid']:n for n in graph['nodes']}
 ids=[]
 for step in expanded['steps'][1:]:
  u=re.search(r'topic\?topic=([0-9a-f-]+)',step['markdown'])[1];ids.append(by_uuid[u]['id'])
 assert len(set(ids))==len(ids)==119
 db=connection()
 assignments=db.query('''[:find (pull ?a [:db/id :activity/id :activity/title :activity/due
 {[:activity/steps :limit nil] [:db/id {:step/content [:db/id :assigned-problem/id
 {[:assigned-problem/topic-coverage :limit nil] [:db/id :topic/title]}]}]}])
 :in $ [?a ...] :where [?a :activity/id _]]''',[[17592186761967,17592186762132]],OUT,'assignment-coverage',basis)
 save('assignment-coverage.json',list(assignments))
 guide_record=next(r[0]for r in assignments if r[0][':db/id']==17592186761967)
 coverage={s[':step/content'][':db/id']:[t[':db/id']for t in s[':step/content'].get(':assigned-problem/topic-coverage',[])]for s in guide_record[':activity/steps']}
 roots=set(t for ts in coverage.values()for t in ts)
 learner=db.query('[:find ?e :in $ ?id :where [?e :learner/id ?id]]',[graph['learner']['id']],OUT,'learner-id',basis)[0][0]
 progress=db.query('''[:find ?t (pull ?p [:db/id :progress/learned :progress/repetitions
 :progress/practice-accuracy :progress/practice-mass :progress/assessment-accuracy
 :progress/assessment-mass :progress/last-direct-at :progress/memory :progress/memory-at])
 :in $ [?t ...] :where [?p :progress/topic ?t]]''',[ids],OUT,'progress',basis)
 profile=db.query('[:find (pull ?l [{[:learner/knowledge-profile :limit nil] [:db/id]}]) :in $ ?l :where [?l :learner/id _]]',[learner],OUT,'profile-ownership',basis)[0][0]
 owned={p[':db/id']for p in profile.get(':learner/knowledge-profile',[])}
 progress=[(t,p)for t,p in progress if p[':db/id']in owned]
 save('progress.json',list(progress));P=dict(progress)
 incoming=collections.defaultdict(list)
 for e in graph['links']:incoming[e['target']].append(e['source'])
 layers={}
 def layer(i):
  if i not in layers:layers[i]=1+max((layer(p)for p in incoming[i]),default=0)
  return layers[i]
 rows=[]
 for i in ids:
  n=nodes[i];p=P.get(i,{})
  rows.append({'id':i,'uuid':n['uuid'],'title':n['name'],'layer':layer(i),'guide_root':i in roots,'learned':graph['learned'].get(str(i),False),'repetitions':graph['repetitions'].get(str(i),0),'progress':p,'prerequisites':[{'id':t,'title':nodes[t]['name'],'learned':graph['learned'].get(str(t),False),'in_expansion':t in ids}for t in incoming[i]]})
 linked=db.query('[:find ?u ?e :in $ [?u ...] :where [?e :activity/id ?u]]',[[uuid.UUID('d58af8ee-31ff-5364-87d1-9474dd41865f'),uuid.UUID('4771eb83-434d-5edb-a38a-03676de85913')]],OUT,'linked-homework-ids',basis)
 save('linked-homework-ids.json',list(linked))
 summary={'basis':basis,'guide_id':17592186761967,'expanded_id':17592186762132,'total_targets':len(rows),'guide_roots':len(roots),'studied':sum(r['learned']for r in rows),'unstudied':sum(not r['learned']for r in rows),'problem_roots':coverage,'linked_homework':list(linked),'rows':rows}
 save('scope.json',summary)
 text=['# MTH 341 E3 candidate scope',f'Basis {basis}; {len(rows)} targets; {summary["unstudied"]} unstudied.','']
 for r in rows:
  text.append(f'{"STUDIED"if r["learned"]else"UNSTUDIED"} L{r["layer"]} {r["id"]} {r["title"]}'+(' [guide coverage]'if r['guide_root']else''))
  text.append('  Prerequisites: '+', '.join(f'{p["id"]} {p["title"]} ({"studied"if p["learned"]else"unstudied"}{";outside expansion"if not p["in_expansion"]else""})'for p in r['prerequisites']))
 (OUT/'scope-readable.txt').write_text('\n'.join(text)+'\n')
 print(json.dumps({k:summary[k]for k in ('basis','total_targets','guide_roots','studied','unstudied','linked_homework')},default=str))
 print('\n'.join(f'{r["id"]} {r["title"]}'+(' [DIRECT]'if r['guide_root']else'')for r in rows if not r['learned']))
if __name__=='__main__':main()
