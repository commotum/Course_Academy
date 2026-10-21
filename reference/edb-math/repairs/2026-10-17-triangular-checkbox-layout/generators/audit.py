"""Read-only live generator, pool, and conversion provenance audit."""
import json,re,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'Cargo.toml').exists())
sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher
from scripts.generator_packages import resolve_registered_script
from capture.scripts.database.edn import loads,dumps,kw
SOURCE=':agent/gpt-6.1-sol-high';KPS=[17592186119772,17592186119784];TARGETS=[17592186120421,17592186262617,17592186571448]
Q='[* {:question/difficulty [:db/id :db/ident]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [*]} {[:answer-field/choices :limit nil] [*]}]}]'
KP='[* {:knowledge-point/question-generator [*]} {[:topic/_knowledge-points :limit nil] [:db/id :topic/title]} {:knowledge-point/canonical-example '+Q+'} {[:knowledge-point/questions :limit nil] '+Q+'}]'
def main():
 pub=Publisher.from_environment(source=SOURCE);db=pub.client;identity=db.status();basis=identity['basis'];out=HERE/f'capture-{basis}';out.mkdir(exist_ok=True)
 rows=db.query('[:find (pull ?kp '+KP+') :in $ [?kp ...] :where [?kp :knowledge-point/id _]]',[KPS],out,'kps',basis)
 records=[r for [r] in rows];ids=TARGETS[:]
 for kp in records:
  for q in kp[':knowledge-point/questions']:
   if q[':db/id'] in TARGETS:ids.extend(f[':db/id'] for f in q[':question/answer-fields'])
 q='[:find ?e ?a ?v ?tx ?s ?op :in $ [?e ...] :where [?e ?a ?v ?tx ?s ?op]]'
 (out/'history-query.edn').write_text(q);(out/'history-inputs.edn').write_text(dumps([ids]))
 raw=db.command('query','--file',out/'history-query.edn','--inputs',out/'history-inputs.edn','--as-of',basis,'--history',timeout=180)
 (out/'history.edn').write_text(raw);history=loads(raw)
 attrs=dict(db.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],out,'idents',basis))
 hist=[{'entity':e,'attribute':str(attrs.get(a,a)),'value':v,'tx':tx,'basis':tx-13194139533312,'source':str(attrs.get(s,s)),'added':op} for e,a,v,tx,s,op in history]
 snapshot={**identity,'kps':records,'history':hist};(out/'snapshot.json').write_text(json.dumps(snapshot,indent=2,default=str)+'\n')
 summary=[]
 for kp in records:
  questions=kp[':knowledge-point/questions'];generator=kp.get(':knowledge-point/question-generator')
  script=generator.get(':question-generator/script') if generator else None
  resolved=str(resolve_registered_script(script,ROOT,pub.config.math_root)) if script else None
  bare=[];radios=[];checkboxes=[]
  for q in questions:
   fs=q[':question/answer-fields'];types={f[':answer-field/type'][':db/ident'] for f in fs}
   if ':answer-field.type/checkbox' in types:
    checkboxes.append(q[':db/id'])
    if any(re.fullmatch(r'\$?(?:[A-E]|I{1,3}|IV|V)\$?',f.get(':answer-field/key','')) for f in fs):bare.append({'id':q[':db/id'],'ma_id':q.get(':question/math-academy-id'),'keys':[f.get(':answer-field/key') for f in fs]})
   if ':answer-field.type/radio' in types:radios.append({'id':q[':db/id'],'ma_id':q.get(':question/math-academy-id'),'level':q.get(':question/difficulty',{}).get(':db/ident')})
  summary.append({'kp':kp[':db/id'],'title':kp[':knowledge-point/title'],'pool_count':len(questions),'bare_label_checkbox_questions':bare,'checkbox_count':len(checkboxes),'radio_questions':radios,'generator':generator,'resolved_entrypoint':resolved})
 result={**identity,'kps':summary,'target_history':hist,'capture':str(out.relative_to(ROOT))}
 (HERE/'audit.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
 print(json.dumps({**identity,'kps':summary},indent=2,default=str))
if __name__=='__main__':main()
