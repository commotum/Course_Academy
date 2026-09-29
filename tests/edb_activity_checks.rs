//! Current-schema activity ownership and Python -> native EDB transaction checks.
use super::transact;
use edb_core::{Cardinality, Database, IndexOrder, Keyword, TransactionRequest, Value, View};
use std::{collections::BTreeMap, error::Error, fs, process::Command};

fn attr(db: &Database, ns: &str, name: &str) -> u32 {
    db.entid(&Keyword::new(ns, name)).unwrap() as u32
}
fn find(db: &Database, ns: &str, name: &str, value: Value) -> u64 {
    let a = attr(db, ns, name);
    db.datoms(View::Current, IndexOrder::Eavt).iter()
        .find(|d| d.attribute == a && d.value == value && d.added).unwrap().entity
}
fn json(value: &Value) -> String {
    match value {
        Value::String(v) => format!("{v:?}"),
        Value::Keyword(v) => format!("{:?}", v.qualified_name()),
        Value::Uuid(v) => format!("\"{v:032x}\""),
        Value::Ref(v) => v.to_string(),
        Value::Long(v) | Value::Instant(v) => v.to_string(),
        Value::Double(v) => format!("{v:?}"),
        Value::Bool(v) => v.to_string(),
        other => panic!("unexpected fixture value {other:?}"),
    }
}
// Capture actual native values and cardinalities; no assumed EID allocation and
// no parallel Python-only version of this fixture can hide an unsupported attr.
fn capture(db: &Database) -> String {
    let mut entities: BTreeMap<u64, BTreeMap<String, (bool, Vec<String>)>> = BTreeMap::new();
    for d in db.datoms(View::Current, IndexOrder::Eavt) {
        if !d.added { continue; }
        let attribute = db.schema().attribute(d.attribute).unwrap();
        let name = attribute.ident.qualified_name();
        if (name.starts_with("db/") || name.starts_with("db.")) && name != "db/ident" { continue; }
        let entry = entities.entry(d.entity).or_default().entry(name)
            .or_insert((attribute.cardinality == Cardinality::Many, Vec::new()));
        entry.1.push(json(&d.value));
    }
    let maps: Vec<String> = entities.iter().map(|(eid, record)| {
        let fields: Vec<String> = record.iter().map(|(name, (many, values))| {
            format!("{name:?}:{}", if *many { format!("[{}]", values.join(",")) } else { values[0].clone() })
        }).collect();
        format!("\"{eid}\":{{{}}}", fields.join(","))
    }).collect();
    format!("{{\"basis_t\":{},\"entities\":{{{}}}}}", db.basis_t(), maps.join(","))
}

pub fn check(base: &Database) -> Result<(), Box<dyn Error>> {
    let fixture = r#"[
     {:db/id "q" :question/id #uuid "00000000-0000-4000-8000-000000000020"
      :question/type :question.type/multiple-choice :question/problem "Select 2."
      :question/answer-fields ["field"] :db/ensure :question/validate}
     {:db/id "field" :answer-field/id #uuid "00000000-0000-4000-8000-000000000021"
      :answer-field/key "selection" :answer-field/answer-choices ["right" "wrong"]
      :answer-field/correct-answer "right" :db/ensure :answer-field/validate}
     {:db/id "right" :answer/id #uuid "00000000-0000-4000-8000-000000000022"
      :answer/type :answer.type/math :answer/value "2" :db/ensure :answer/validate}
     {:db/id "wrong" :answer/id #uuid "00000000-0000-4000-8000-000000000023"
      :answer/type :answer.type/math :answer/value "3" :db/ensure :answer/validate}
     {:db/id "example" :example/id #uuid "00000000-0000-4000-8000-000000000030"
      :example/problem "Recognize 2." :example/explanation "Two is written 2." :db/ensure :example/validate}
     {:db/id "kp" :knowledge-point/id #uuid "00000000-0000-4000-8000-000000000031"
      :knowledge-point/title "Recognize two" :knowledge-point/example "example"
      :knowledge-point/questions ["q"] :db/ensure :knowledge-point/validate}
     {:db/id [:topic/id #uuid "b3d88ca6-d319-409b-bdb1-000000000001"]
      :topic/knowledge-points ["kp"] :db/ensure :topic/validate}
     {:db/id "review" :assessment/id #uuid "00000000-0000-4000-8000-000000000024"
      :assessment/title "Native one-question assessment"
      :assessment/questions ["q"] :db/ensure :assessment/validate}
     {:db/id "task" :learner-task/id #uuid "00000000-0000-4000-8000-000000000025"
      :learner-task/activity "review" :learner-task/status :learner-task.status/in-progress
      :learner-task/items ["item"] :db/ensure :learner-task/validate}
     {:db/id "item" :task-item/id #uuid "00000000-0000-4000-8000-000000000026"
      :task-item/index 1 :task-item/content "q" :db/ensure :task-item/validate}
     {:db/id [:learner/id "schema-check-learner"] :learner/activity ["task"] :db/ensure :learner/validate}
    ]"#;
    let db = transact(base, fixture, 4000)?.db_after;
    let learner = find(&db, "learner", "id", Value::String("schema-check-learner".into()));
    let policy = find(&db, "policy", "id", Value::Uuid(0xb3d88ca6d319409bbdb1000000000003));
    let item = find(&db, "task-item", "id", Value::Uuid(0x00000000000040008000000000000026));
    let task = find(&db, "learner-task", "id", Value::Uuid(0x00000000000040008000000000000025));
    let answer = find(&db, "answer", "id", Value::Uuid(0x00000000000040008000000000000022));
    let dir = std::env::temp_dir().join(format!("course-academy-native-{}", std::process::id()));
    fs::create_dir_all(&dir)?;
    let input = dir.join("capture.json");
    fs::write(&input, capture(&db))?;
    let code = r#"
import json,sys
from datetime import datetime,timezone
from engine.runtime import complete_item
from engine.schema import EntitySnapshot,load_runtime
capture=json.load(open(sys.argv[1]))
snapshot=EntitySnapshot({int(k):v for k,v in capture['entities'].items()},capture['basis_t'])
learner,policy,item,answer=map(int,sys.argv[2:])
loaded=load_runtime(snapshot,learner,policy)
at=datetime(2026,9,28,tzinfo=timezone.utc)
completion=complete_item(loaded,item,completed_at=at,result=True,response_refs=(answer,),elapsed_seconds=2)
assert completion.delivery.complete
plan=completion.transaction
print(plan.request_key)
print(plan.compare_basis_t)
print(plan.edn)
"#;
    let output = Command::new("python3").args(["-c", code]).arg(&input)
        .args([learner.to_string(), policy.to_string(), item.to_string(), answer.to_string()]).output()?;
    assert!(output.status.success(), "Python adapter failed: {}", String::from_utf8_lossy(&output.stderr));
    let text = String::from_utf8(output.stdout)?;
    let mut lines = text.lines();
    let key = lines.next().unwrap();
    let basis: u64 = lines.next().unwrap().parse()?;
    let edn = lines.next().unwrap();
    let request = TransactionRequest::from_edn(key, edn)?.comparing_basis(basis);
    assert_eq!(request.compare_basis_t, Some(db.basis_t()));
    assert!(request.request_key.starts_with("complete-item-"));
    // with_forms checks transaction/CAS semantics; it is not the durable writer.
    let after = transact(&db, edn, 5000)?.db_after;
    assert_eq!(after.values(item, attr(&after,"task-item","elapsed-seconds")), vec![&Value::Double(2.0)]);
    assert_eq!(after.values(item, attr(&after,"task-item","responses")), vec![&Value::Ref(answer)]);
    assert_eq!(after.values(item, attr(&after,"task-item","completed-at")).len(),1);
    assert!(transact(&after, edn, 5100).is_err(), "the item CAS must reject a second fresh application");
    let state = find(&after,"progress","id",Value::String("schema-check-state".into()));
    assert_eq!(after.values(state,attr(&after,"progress","practice-mass")),vec![&Value::Double(4.0)]);
    assert_eq!(after.values(state,attr(&after,"progress","assessment-mass")),vec![&Value::Double(1.0)]);
    assert_eq!(after.values(state,attr(&after,"progress","last-direct-at")).len(),1);
    let performance = match after.values(learner,attr(&after,"learner","performance"))[0] {
        Value::Ref(eid) => *eid, _ => panic!("performance ref required"),
    };
    assert_eq!(after.values(performance,attr(&after,"performance","assessment-mass")),vec![&Value::Double(1.0)]);
    assert_eq!(after.values(performance,attr(&after,"performance","practice-mass")),vec![&Value::Double(4.0)]);
    assert_eq!(after.values(task,attr(&after,"learner-task","status")),vec![&Value::Ref(after.entid(&Keyword::new("learner-task.status","completed")).unwrap())]);
    let deleted = transact(&after,&format!("[[:db.fn/retractEntity {task}]]"),5200)?.db_after;
    assert!(deleted.values(item,attr(&deleted,"task-item","id")).is_empty());
    assert_eq!(deleted.values(answer,attr(&deleted,"answer","id")).len(),1);
    fs::remove_dir_all(dir)?;
    println!("PASS actual EDB capture -> Python automatic assessment completion -> native request EDN, exact basis field, item CAS, progress/global update, stable answer refs and component lifecycle.");
    Ok(())
}
