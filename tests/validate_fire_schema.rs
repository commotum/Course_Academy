// Run from the repository root; requires the local EDB edb_core build.
use edb_core::{Database, Keyword, Value};
use std::{error::Error, fs};
fn main() -> Result<(), Box<dyn Error>> {
 let root=std::env::current_dir()?;
 let mut db=Database::bootstrap()?;
 let mut clock=1000i64;
 for dir in ["schema-v2/data", "schema-v2/content", "schema-v2/fire"] {
  let mut paths=fs::read_dir(root.join(dir))?.filter_map(Result::ok).map(|e|e.path()).filter(|p|p.extension().is_some_and(|e|e=="edn")).collect::<Vec<_>>();
  paths.sort();
  for path in paths {
   db=db.with_edn(&fs::read_to_string(&path)?,clock).map_err(|e|format!("{}: {e}",path.display()))?.db_after;
   clock+=1;
  }
 }
 let fixture=r#"[
 {:db/id "advanced" :topic/id #uuid "b3d88ca6-d319-409b-bdb1-000000000001" :topic/title "Illustrative advanced topic" :topic/encompasses ["edge"]}
 {:db/id "component" :topic/id #uuid "b3d88ca6-d319-409b-bdb1-000000000002" :topic/title "Illustrative component topic"}
 {:db/id "learner" :fire-learner/id "schema-check-learner"
  :fire-learner/assessment-accuracy 0.8 :fire-learner/practice-accuracy 0.9
  :fire-learner/assessment-mass 0.0 :fire-learner/practice-mass 4.0
  :db/ensure [:fire-learner/validate :fire-learner/ability-validate]}
 {:db/id "policy" :fire-policy/id "schema-check-policy" :fire-policy/algorithm :fire.algorithm/schema-test
  :fire-policy/parameters-edn "{:base-days 1.0 :growth 2.0}" :db/ensure :fire-policy/validate}
 {:db/id "edge" :encompassing/topic "component" :encompassing/weight 0.0
  :encompassing/rationale "Illustrative explicit zero coverage for schema validation." :db/ensure :encompassing/validate}
 {:db/id "difficulty" :fire-difficulty/topic "advanced" :fire-difficulty/prior-accuracy 0.8
  :fire-difficulty/assessment-correct 3.0 :fire-difficulty/assessment-total 4.0
  :fire-difficulty/method :fire.calibration/assessment-cohort :fire-difficulty/cohort "Illustrative schema fixture"
  :db/ensure :fire-difficulty/validate}
 {:db/id "calibration" :fire-calibration/id "schema-check-calibration" :fire-calibration/entries ["difficulty"] :db/ensure :fire-calibration/validate}
 {:db/id "event" :fire-event/id "schema-check-event" :fire-event/learner "learner" :fire-event/at #inst "2026-09-26T00:00:00.000Z"
  :fire-event/topic "advanced" :fire-event/kind "review" :fire-event/passed true :fire-event/assessment false :fire-event/quality 1.5
  :fire-event/learned false :fire-event/question-results-edn "[true true true true]" :fire-event/source "direct" :db/ensure :fire-event/validate}
 {:db/id "state" :fire-state/id "schema-check-state" :fire-state/learner "learner" :fire-state/topic "advanced"
  :fire-state/repetitions 1.5 :fire-state/memory 1.0 :fire-state/memory-at #inst "2026-09-26T00:00:00.000Z"
  :fire-state/interval-days 2.8284271247461903 :fire-state/assessment-accuracy 0.8 :fire-state/practice-accuracy 0.8
  :fire-state/assessment-mass 0.0 :fire-state/practice-mass 4.0
  :fire-state/learned true :fire-state/policy "policy" :db/ensure :fire-state/validate}
 {:fire-state/id "schema-check-unlearned" :fire-state/learner "learner" :fire-state/topic "component"
  :fire-state/repetitions 0.0 :fire-state/memory 0.0 :fire-state/memory-at #inst "2026-09-26T00:00:00.000Z"
  :fire-state/interval-days 1.0 :fire-state/assessment-accuracy 0.4 :fire-state/practice-accuracy 0.6
  :fire-state/assessment-mass 2.0 :fire-state/practice-mass 3.0
  :fire-state/learned false :fire-state/policy "policy" :db/ensure :fire-state/validate}
 {:db/id "update" :fire-update/topic "advanced" :fire-update/trace-edn "{:direct true :raw_delta 1.0 :before {:repetitions 0.5} :after {:repetitions 1.5}}" :db/ensure :fire-update/validate}
 {:fire-application/id "schema-check-application" :fire-application/event "event" :fire-application/event-hash "schema-test-payload" :fire-application/policy "policy"
  :fire-application/calibration "calibration" :fire-application/input-state-edn "{}"
  :fire-application/applied-at #inst "2026-09-26T00:00:01.000Z" :fire-application/updates ["update"] :db/ensure :fire-application/validate}
 ]"#;
 db=db.with_edn(fixture,2000)?.db_after;
 let idattr=db.entid(&Keyword::new("fire-state","id")).unwrap() as u32;
 let keyattr=db.entid(&Keyword::new("fire-state","key")).unwrap() as u32;
 let state=db.datoms(edb_core::View::Current,edb_core::IndexOrder::Eavt).iter().find(|d|d.attribute==idattr&&d.value==Value::String("schema-check-state".into())&&d.added).unwrap().entity;
 assert_eq!(db.values(state,keyattr).len(),1);
 let find_string = |database: &Database, ns: &str, name: &str, value: &str| {
  let attr=database.entid(&Keyword::new(ns,name)).unwrap() as u32;
  database.datoms(edb_core::View::Current,edb_core::IndexOrder::Eavt).iter()
   .find(|d|d.attribute==attr&&d.value==Value::String(value.into())&&d.added).unwrap().entity
 };
 let learner=find_string(&db,"fire-learner","id","schema-check-learner");
 let topicattr=db.entid(&Keyword::new("fire-state","topic")).unwrap() as u32;
 let topic=match db.values(state,topicattr).first().unwrap() { Value::Ref(id)=>*id, other=>panic!("Unexpected ref {other:?}") };
 let event=find_string(&db,"fire-event","id","schema-check-event");
 let eventkeyattr=db.entid(&Keyword::new("fire-event","key")).unwrap() as u32;
 assert_eq!(db.values(event,eventkeyattr).len(),1);
 let state_count=db.datoms(edb_core::View::Current,edb_core::IndexOrder::Eavt).iter().filter(|d|d.attribute==idattr&&d.added).count();
 let update=format!(r#"[{{:db/id [:fire-state/key [{learner} {topic}]] :fire-state/memory 0.75 :db/ensure :fire-state/validate}}
  {{:db/id [:fire-event/key [{learner} "schema-check-event"]] :fire-event/quality 1.5 :db/ensure :fire-event/validate}}]"#);
 db=db.with_edn(&update,2500)?.db_after;
 assert_eq!(state_count,db.datoms(edb_core::View::Current,edb_core::IndexOrder::Eavt).iter().filter(|d|d.attribute==idattr&&d.added).count());
 assert_eq!(event,find_string(&db,"fire-event","id","schema-check-event"));
 let second_learner=r#"[
  {:db/id "other" :fire-learner/id "schema-check-other" :db/ensure :fire-learner/validate}
  {:fire-event/id "schema-check-event" :fire-event/learner "other" :fire-event/at #inst "2026-09-26T00:00:00.000Z"
   :fire-event/topic [:topic/id #uuid "b3d88ca6-d319-409b-bdb1-000000000001"] :fire-event/kind "review"
   :fire-event/passed false :fire-event/assessment true :fire-event/quality 1.5 :fire-event/learned false
   :fire-event/question-results-edn "[false true]" :fire-event/source "direct" :db/ensure :fire-event/validate}]"#;
 db=db.with_edn(second_learner,2600)?.db_after;
 let duplicate_event=format!(r#"[{{:fire-event/id "schema-check-event" :fire-event/learner {learner}}}]"#);
 assert!(db.with_edn(&duplicate_event,3000).is_err());
 let wrong_type=format!(r#"[{{:db/id {event} :fire-event/passed "true"}}]"#);
 assert!(db.with_edn(&wrong_type,3000).is_err());
 let wrong_cardinality=format!(r#"[{{:db/id {state} :fire-state/repetitions [1.0 2.0]}}]"#);
 assert!(db.with_edn(&wrong_cardinality,3000).is_err());
 let missing=r#"[{:fire-state/id "incomplete" :db/ensure :fire-state/validate}]"#;
 assert_eq!(db.with_edn(missing,3000).unwrap_err().code,"transaction/entity-spec");
 let duplicate=r#"[{:fire-state/id "duplicate" :fire-state/learner [:fire-learner/id "schema-check-learner"] :fire-state/topic [:topic/id #uuid "b3d88ca6-d319-409b-bdb1-000000000001"]}]"#;
 assert!(db.with_edn(duplicate,3000).is_err());
 println!("PASS all current content and FIRe schemas install; required-attribute specs accept topic-owned encompassing/calibration/global ability/event/application/state fixtures, explicit zero coverage, optional rationale, quality 1.5 and unlearned ability.");
 println!("PASS state/event composites derive and resolve updates without new rows; event IDs are learner-scoped; missing state fields, duplicate state/event pairs, wrong scalar type and scalar-cardinality vector are rejected.");
 println!("Scope: schema shape/EDB semantics only; no engine equations, enum/range checks, or embedded EDN payload validation claimed.");
 Ok(())
}
