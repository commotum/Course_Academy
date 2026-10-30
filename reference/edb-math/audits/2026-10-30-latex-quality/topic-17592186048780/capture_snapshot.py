import sys,json
from pathlib import Path
sys.path.insert(0,'/home/jake/Developer/Course_Academy')
from scripts.generator_publish import Publisher
D=Path('/home/jake/Developer/Course_Academy/reference/edb-math/audits/2026-10-30-latex-quality/topic-17592186048780')
p=Publisher.from_environment(source=':agent/codex'); c=p.client
s=c.status();assert s['lineage']=='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';s['read_basis']=11863
(D/'database-identity.json').write_text(json.dumps(s,indent=2))
def q(n,s,inputs):
 r=c.query(s,inputs,D,n,basis=11863);(D/(n+'.json')).write_text(json.dumps(r,indent=2,default=str));print(n,len(r),flush=True);return r
q('topic','[:find (pull ?e [*]) :in $ ?e :where [?e :topic/id _]]',[17592186048780])
q('activities','[:find (pull ?a [* {:activity/type [:db/id :db/ident]} {:activity/steps [* {:step/content [*]}]}]) :in $ ?t :where [?a :activity/scope ?t]]',[17592186048780])
for kp in [17592186096652,17592186096653,17592186096701,17592186235285]:
 r=p.read_kp(kp,D/str(kp),11863);(D/(str(kp)+'.json')).write_text(json.dumps(r,indent=2,default=str));print(kp,len(r.get(':knowledge-point/questions',[])),flush=True)
q('relevant-schema','[:find ?ident :where [?a :db/ident ?ident]]',[])
