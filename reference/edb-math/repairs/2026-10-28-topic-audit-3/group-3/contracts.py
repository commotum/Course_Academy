import collections,json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());db=connection();ids=[q[':db/id']for q in D['questions']];qf=[];fa=[]
for n in range(0,len(ids),200):qf+=db.query('[:find ?q ?f :in $ [?q ...] :where [?q :question/answer-fields ?f]]',[ids[n:n+200]],H,'membership-qf-'+str(n),9837)
fids=sorted({f for q,f in qf})
for n in range(0,len(fids),200):fa+=db.query('[:find ?f ?a :in $ [?f ...] :where [?f :answer-field/choices ?a]]',[fids[n:n+200]],H,'membership-fa-'+str(n),9837)
expectedqf={(q[':db/id'],f[':db/id'])for q in D['questions']for f in q.get(':question/answer-fields',[])};expectedfa={(f[':db/id'],a[':db/id'])for q in D['questions']for f in q.get(':question/answer-fields',[])for a in f.get(':answer-field/choices',[])};assert set(map(tuple,qf))==expectedqf;assert set(map(tuple,fa))==expectedfa
reports=[];dups=[];bad=[];duplicatevalues=[]
for q in D['questions']:
 by=collections.defaultdict(list)
 for f in q.get(':question/answer-fields',[]):
  by[f[':answer-field/key']].append(f[':db/id']);answerids={a[':db/id']for a in f.get(':answer-field/choices',[])};c=f.get(':answer-field/correct',{}).get(':db/id')
  if c and c not in answerids:bad.append({'question':q[':db/id'],'field':f[':db/id'],'unowned_correct':c})
  valuegroups=collections.defaultdict(list)
  for a in f.get(':answer-field/choices',[]):valuegroups[(a[':answer/type'][':db/id'],a[':answer/value'])].append(a[':db/id'])
  duplicatevalues += [{'question':q[':db/id'],'field':f[':db/id'],'field_type':f[':answer-field/type'][':db/id'],'answer_type':t,'value':v,'ids':a,'canonical':c}for(t,v),a in valuegroups.items()if len(a)>1]
 dups += [{'question':q[':db/id'],'source':q.get(':question/math-academy-id'),'key':k,'fields':v}for k,v in by.items()if len(v)>1]
for n,v in [('duplicate-field-keys',dups),('unowned-canonical-links',bad),('duplicate-value-classes',duplicatevalues)]: (H/(n+'.json')).write_text(json.dumps(v,indent=2))
(H/'membership-coverage.json').write_text(json.dumps({'basis_t':9837,'questions':len(ids),'question_field_memberships':len(qf),'field_answer_memberships':len(fa),'full_explicit_membership_verified':True,'duplicate_field_keys':len(dups),'unowned_canonical_links':len(bad),'duplicate_value_classes':len(duplicatevalues)},indent=2));print('membership',len(qf),len(fa),'dupekeys',len(dups),'unowned',len(bad),'dupevalues',len(duplicatevalues))
