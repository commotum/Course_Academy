"""Verify skipped topics have no new pool members outside completed audits."""
import collections,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;inv=json.loads((H/'inventory.json').read_text());links=inv['links'];ledger=json.loads((H/'skip-ledger.json').read_text());cache={};rows=[];drift=[]
for t in ledger:
 prior=max(t['prior_completed_audits'],key=lambda a:a['verified_basis_t']);path=Path(prior['directory']);name=path.name
 if name not in cache:
  if name=='2026-10-29-q17592186604616':
   ss=[json.loads((path/'lesson.json').read_text()),json.loads((path/'expanded-scope/current.json').read_text())];pls=[]
   for s in ss:
    ts=[s['topic']]if'topic'in s else s['topics']
    pls.extend([q[':db/id'],k[':db/id'],t[':db/id']]for t in ts for k in t[':topic/knowledge-points']for key in[':knowledge-point/questions',':knowledge-point/canonical-example']for q in(k.get(key,[])if isinstance(k.get(key,[]),list)else[k[key]]))
   cache[name]={(tid,k,q)for q,k,tid in pls}
  else:cache[name]={tuple(l)for l in json.loads((path/'inventory.json').read_text())['links']}
 before={l for l in cache[name]if l[0]==t['topic']};now={tuple(l)for l in links if l[0]==t['topic']};extra=now-before;missing=before-now
 r={'topic':t['topic'],'title':t['title'],'prior_audit':str(path),'prior_verified_basis':prior['verified_basis_t'],'current_basis':inv['basis_t'],'question_example_links':len(now),'unreviewed_added_links':sorted(extra),'removed_links':sorted(missing),'unchanged_pool':before==now};rows.append(r)
 if extra or missing:drift.append(r)
report={'passed':not drift,'skipped_topics':len(rows),'checks':rows,'requires_review':drift,'database_writes':0};(H/'skip-coverage-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('Skipped pools verified:',len(rows),'changed since completed audit:',len(drift));print([(r['topic'],len(r['unreviewed_added_links']),len(r['removed_links']))for r in drift])
