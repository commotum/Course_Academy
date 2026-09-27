//! Schema and ownership-lifecycle checks; draft domain rules remain controller contracts.
use super::transact;
use edb_core::{Database, IndexOrder, Keyword, Value, View};
use std::{error::Error, fs};

fn attribute(db: &Database, ns: &str, name: &str) -> u32 {
    db.entid(&Keyword::new(ns, name)).unwrap() as u32
}
fn find(db: &Database, ns: &str, name: &str, value: Value) -> u64 {
    let a = attribute(db, ns, name);
    db.datoms(View::Current, IndexOrder::Eavt)
        .iter()
        .find(|d| d.attribute == a && d.value == value && d.added)
        .unwrap()
        .entity
}

pub fn check(base: &Database) -> Result<(), Box<dyn Error>> {
    let example = fs::read_to_string("schema-v2/proposed/examples/quiz-4-retake.edn")?;
    let mut db = transact(base, &example, 4000)?.db_after;
    let activity = find(&db, "activity", "math-academy-id", Value::Long(13682227));
    let definition = match db.values(activity, attribute(&db, "activity", "content"))[0] {
        Value::Ref(id) => *id,
        _ => panic!(),
    };
    assert_eq!(
        db.values(definition, attribute(&db, "assessment", "id"))
            .len(),
        1
    );
    // An assessment identity preserves the category without inventing its scope.
    assert!(db
        .values(definition, attribute(&db, "assessment", "topics"))
        .is_empty());
    let tasks_attr = attribute(&db, "activity", "tasks");
    assert_eq!(db.values(activity, tasks_attr).len(), 8);
    assert_eq!(
        db.values(activity, attribute(&db, "activity", "xp-earned")),
        vec![&Value::Long(18)]
    );
    assert_eq!(
        db.values(activity, attribute(&db, "activity", "xp-base")),
        vec![&Value::Long(15)]
    );
    assert!(db
        .values(activity, attribute(&db, "activity", "elapsed-seconds"))
        .is_empty());
    assert!(db
        .values(activity, attribute(&db, "activity", "completed-at"))
        .is_empty());
    let question = find(&db, "question", "math-academy-id", Value::Long(37713));
    let first = db
        .values(activity, tasks_attr)
        .into_iter()
        .find_map(|v| match v {
            Value::Ref(id)
                if db.values(*id, attribute(&db, "task", "index")) == vec![&Value::Long(1)] =>
            {
                Some(*id)
            }
            _ => None,
        })
        .unwrap();
    assert_eq!(
        db.values(first, attribute(&db, "task", "content")),
        vec![&Value::Ref(question)]
    );
    assert_eq!(
        db.values(first, attribute(&db, "task", "elapsed-seconds")),
        vec![&Value::Double(103.0)]
    );
    assert!(db
        .values(first, attribute(&db, "task", "completed-at"))
        .is_empty());
    let associated = match db.values(first, attribute(&db, "task", "example"))[0] {
        Value::Ref(e) => *e,
        _ => panic!(),
    };
    assert_eq!(
        db.values(associated, attribute(&db, "example", "math-academy-id")),
        vec![&Value::Long(4962)]
    );
    let deleted = transact(&db, &format!("[[:db.fn/retractEntity {activity}]]"), 4100)?.db_after;
    assert!(deleted
        .values(first, attribute(&db, "task", "id"))
        .is_empty());
    assert!(!deleted
        .values(question, attribute(&db, "question", "id"))
        .is_empty());

    // A referenced identity-only definition identifies each category without
    // inventing its unrecovered content, durations or outcomes.
    for (i, kind) in [
        "lesson",
        "review",
        "assessment",
        "multistep",
        "diagnostic",
        "supplemental-diagnostic",
    ]
    .iter()
    .enumerate()
    {
        let optional = if *kind == "lesson" {
            ":activity/xp-earned -1 :activity/xp-base 14"
        } else {
            ":activity/xp-earned 0"
        };
        let text = format!(
            r#"[{{:db/id "history" :learner/id "schema-activity-history-{i}" :learner/activity ["attempt"]}}
          {{:db/id "definition" :{kind}/id #uuid "00000000-0000-4000-9000-00000000000{i}"}}
          {{:db/id "attempt" :activity/id #uuid "00000000-0000-4000-8000-00000000000{i}"
          :activity/content "definition" :activity/title "Synthetic summary" :activity/status :activity.status/completed
          {optional} :db/ensure :activity/validate}}]"#
        );
        db = transact(&db, &text, 4200 + i as i64)?.db_after;
        let attempt = find(
            &db,
            "activity",
            "id",
            Value::Uuid(0x00000000000040008000000000000000 + i as u128),
        );
        let definition = match db.values(attempt, attribute(&db, "activity", "content"))[0] {
            Value::Ref(id) => *id,
            _ => panic!(),
        };
        assert_eq!(db.values(definition, attribute(&db, kind, "id")).len(), 1);
    }
    // When even the content identity is unknown, the summary is still valid,
    // but the ready spec must reject the missing reference.
    db = transact(&db, r#"[{:activity/id #uuid "00000000-0000-4000-8000-000000000099" :activity/title "Unknown content" :activity/status :activity.status/completed :db/ensure :activity/validate}]"#,4300)?.db_after;
    assert!(transact(&db, r#"[{:activity/id #uuid "00000000-0000-4000-8000-000000000099" :db/ensure :activity/ready-validate}]"#,4301).is_err());
    assert!(transact(
        &db,
        &format!("[{{:db/id {first} :task/elapsed-seconds \"1:43\"}}]"),
        4300
    )
    .is_err());

    // Stable selected-answer IDs and repeated submissions are independent of
    // canonical answer keys and repeated question presentations.
    let synthetic = r#"[
     {:db/id "q" :question/id #uuid "00000000-0000-4000-8000-000000000020"
      :question/type :question.type/multiple-choice :question/problem "Select 2."
      :question/answer-fields ["field"] :db/ensure :question/validate}
     {:db/id "field" :answer-field/id #uuid "00000000-0000-4000-8000-000000000021"
      :answer-field/key "selection" :answer-field/answer-choices ["right" "wrong"] :answer-field/correct-answer "right" :db/ensure :answer-field/validate}
     {:db/id "right" :answer/id #uuid "00000000-0000-4000-8000-000000000022" :answer/type :answer.type/math :answer/value "2" :db/ensure :answer/validate}
     {:db/id "wrong" :answer/id #uuid "00000000-0000-4000-8000-000000000023" :answer/type :answer.type/math :answer/value "3" :db/ensure :answer/validate}
     {:db/id "learner" :learner/id "synthetic-responses" :learner/activity ["activity"]}
     {:db/id "review" :review/id #uuid "00000000-0000-4000-8000-000000000031"}
     {:db/id "activity" :activity/id #uuid "00000000-0000-4000-8000-000000000024"
      :activity/content "review" :activity/title "Synthetic retry example" :activity/status :activity.status/completed
      :activity/tasks ["one" "two"] :db/ensure :activity/validate}
     {:db/id "one" :task/id #uuid "00000000-0000-4000-8000-000000000025"
      :task/index 1 :task/type :task.type/question :task/content "q"
      :task/result :task.result/correct :task/response-state :task.response/recorded
      :task/submissions ["s1" "s2"] :db/ensure :task/ready-validate}
     {:db/id "two" :task/id #uuid "00000000-0000-4000-8000-000000000026"
      :task/index 2 :task/type :task.type/question :task/content "q"
      :task/result :task.result/incorrect :task/response-state :task.response/no-answer :db/ensure :task/ready-validate}
     {:db/id "s1" :submission/id #uuid "00000000-0000-4000-8000-000000000027" :submission/index 1
      :submission/result :task.result/incorrect :submission/fields ["a1"] :db/ensure :submission/validate}
     {:db/id "s2" :submission/id #uuid "00000000-0000-4000-8000-000000000028" :submission/index 2
      :submission/result :task.result/correct :submission/fields ["a2"] :db/ensure :submission/validate}
     {:db/id "a1" :submitted-answer/id #uuid "00000000-0000-4000-8000-000000000029"
      :submitted-answer/field "field" :submitted-answer/selected-answer "wrong" :db/ensure :submitted-answer/validate}
     {:db/id "a2" :submitted-answer/id #uuid "00000000-0000-4000-8000-000000000030"
      :submitted-answer/field "field" :submitted-answer/selected-answer "right" :db/ensure :submitted-answer/validate}
    ]"#;
    db = transact(&db, synthetic, 4400)?.db_after;
    let content = find(
        &db,
        "question",
        "id",
        Value::Uuid(0x00000000000040008000000000000020),
    );
    let attempt = find(
        &db,
        "activity",
        "id",
        Value::Uuid(0x00000000000040008000000000000024),
    );
    let submitted = find(
        &db,
        "submitted-answer",
        "id",
        Value::Uuid(0x00000000000040008000000000000029),
    );
    let after = transact(&db, &format!("[[:db.fn/retractEntity {attempt}]]"), 4500)?.db_after;
    assert!(after
        .values(submitted, attribute(&db, "submitted-answer", "id"))
        .is_empty());
    assert!(!after
        .values(content, attribute(&db, "question", "id"))
        .is_empty());

    // Queue entries belong to the learner; their content definitions remain shared.
    // The queue records why and how content was selected independently of history.
    let queued = r#"[
     {:db/id "learner" :learner/id "synthetic-queue" :learner/queue ["recommended" "selected"] :db/ensure :learner/validate}
     {:db/id "definition" :review/id #uuid "00000000-0000-4000-8000-000000000050"}
     {:db/id "recommended" :queue/id #uuid "00000000-0000-4000-8000-000000000051"
      :queue/content "definition" :queue/index 1 :queue/selection :queue.selection/recommended
      :queue/reason "Review is due." :db/ensure :queue/validate}
     {:db/id "selected" :queue/id #uuid "00000000-0000-4000-8000-000000000052"
      :queue/content "definition" :queue/index 2 :queue/selection :queue.selection/self-selected
      :queue/reason "Practice for this week's assignment." :db/ensure :queue/validate}
    ]"#;
    db = transact(&db, queued, 4600)?.db_after;
    let owner = find(
        &db,
        "learner",
        "id",
        Value::String("synthetic-queue".into()),
    );
    let queue_attr = attribute(&db, "learner", "queue");
    let shared = find(
        &db,
        "review",
        "id",
        Value::Uuid(0x00000000000040008000000000000050),
    );
    let entries: Vec<u64> = db
        .values(owner, queue_attr)
        .into_iter()
        .map(|v| match v {
            Value::Ref(id) => *id,
            _ => panic!(),
        })
        .collect();
    assert_eq!(entries.len(), 2);
    for entry in &entries {
        assert_eq!(
            db.values(*entry, attribute(&db, "queue", "content")),
            vec![&Value::Ref(shared)]
        );
        let owners = db.datoms_with_prefix(&edb_core::IndexPrefix::Vaet {
            value: Value::Ref(*entry),
            attribute: Some(queue_attr),
            entity: None,
        })?;
        assert_eq!(owners.len(), 1);
        assert_eq!(owners[0].entity, owner);
    }
    assert!(transact(
        &db,
        r#"[{:queue/id #uuid "00000000-0000-4000-8000-000000000053"
         :queue/index 3 :queue/selection :queue.selection/recommended
         :queue/reason "Missing content." :db/ensure :queue/validate}]"#,
        4700
    )
    .is_err());
    let removed = transact(&db, &format!("[[:db.fn/retractEntity {owner}]]"), 4800)?.db_after;
    for entry in entries {
        assert!(removed
            .values(entry, attribute(&db, "queue", "id"))
            .is_empty());
    }
    assert!(!removed
        .values(shared, attribute(&db, "review", "id"))
        .is_empty());
    println!("PASS activity drafts: six categories identifiable through content refs, summaries with unknown content, signed/above-base XP, unknown durations, eight real quiz tasks, example ID mapping, repeated questions/submissions and component deletion preserving canonical content. Learner-owned queue entries support both selection reasons, resolve reverse ownership, require content and cascade on learner deletion while preserving shared definitions. Proposed enum/range/ownership-controller rules are not claimed to be enforced by required-attribute specs.");
    Ok(())
}
