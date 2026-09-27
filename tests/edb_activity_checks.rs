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
    let task = find(&db, "learner-task", "math-academy-id", Value::Long(13682227));
    let definition = match db.values(task, attribute(&db, "learner-task", "activity"))[0] {
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
    let items_attr = attribute(&db, "learner-task", "items");
    assert_eq!(db.values(task, items_attr).len(), 8);
    assert_eq!(
        db.values(task, attribute(&db, "learner-task", "xp-earned")),
        vec![&Value::Long(18)]
    );
    assert_eq!(
        db.values(task, attribute(&db, "learner-task", "xp-base")),
        vec![&Value::Long(15)]
    );
    assert!(db
        .values(task, attribute(&db, "learner-task", "elapsed-seconds"))
        .is_empty());
    assert!(db
        .values(task, attribute(&db, "learner-task", "completed-at"))
        .is_empty());
    let question = find(&db, "question", "math-academy-id", Value::Long(37713));
    let first = db
        .values(task, items_attr)
        .into_iter()
        .find_map(|v| match v {
            Value::Ref(id)
                if db.values(*id, attribute(&db, "task-item", "index"))
                    == vec![&Value::Long(1)] =>
            {
                Some(*id)
            }
            _ => None,
        })
        .unwrap();
    assert_eq!(
        db.values(first, attribute(&db, "task-item", "content")),
        vec![&Value::Ref(question)]
    );
    assert_eq!(
        db.values(first, attribute(&db, "task-item", "elapsed-seconds")),
        vec![&Value::Double(103.0)]
    );
    assert!(db
        .values(first, attribute(&db, "task-item", "completed-at"))
        .is_empty());
    let deleted = transact(&db, &format!("[[:db.fn/retractEntity {task}]]"), 4100)?.db_after;
    assert!(deleted
        .values(first, attribute(&db, "task-item", "id"))
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
            ":learner-task/xp-earned -1 :learner-task/xp-base 14"
        } else {
            ":learner-task/xp-earned 0"
        };
        let text = format!(
            r#"[{{:db/id "history" :learner/id "schema-activity-history-{i}" :learner/activity ["attempt"]}}
          {{:db/id "definition" :{kind}/id #uuid "00000000-0000-4000-9000-00000000000{i}"}}
          {{:db/id "attempt" :learner-task/id #uuid "00000000-0000-4000-8000-00000000000{i}"
          :learner-task/activity "definition" :learner-task/title "Synthetic summary" :learner-task/status :learner-task.status/completed
          {optional} :db/ensure :learner-task/validate}}]"#
        );
        db = transact(&db, &text, 4200 + i as i64)?.db_after;
        let attempt = find(
            &db,
            "learner-task",
            "id",
            Value::Uuid(0x00000000000040008000000000000000 + i as u128),
        );
        let definition = match db.values(attempt, attribute(&db, "learner-task", "activity"))[0] {
            Value::Ref(id) => *id,
            _ => panic!(),
        };
        assert_eq!(db.values(definition, attribute(&db, kind, "id")).len(), 1);
    }
    // When even the content identity is unknown, the summary is still valid,
    // but the ready spec must reject the missing reference.
    db = transact(&db, r#"[{:learner-task/id #uuid "00000000-0000-4000-8000-000000000099" :learner-task/title "Unknown content" :learner-task/status :learner-task.status/completed :db/ensure :learner-task/validate}]"#,4300)?.db_after;
    assert!(transact(&db, r#"[{:learner-task/id #uuid "00000000-0000-4000-8000-000000000099" :db/ensure :learner-task/ready-validate}]"#,4301).is_err());
    assert!(transact(
        &db,
        &format!("[{{:db/id {first} :task-item/elapsed-seconds \"1:43\"}}]"),
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
     {:db/id "activity" :learner-task/id #uuid "00000000-0000-4000-8000-000000000024"
      :learner-task/activity "review" :learner-task/title "Synthetic retry example" :learner-task/status :learner-task.status/completed
      :learner-task/items ["one" "two"] :db/ensure :learner-task/validate}
     {:db/id "one" :task-item/id #uuid "00000000-0000-4000-8000-000000000025"
      :task-item/index 1 :task-item/content "q"
      :task-item/result :task-item.result/correct :task-item/response-state :task-item.response/recorded
      :task-item/submissions ["s1" "s2"] :db/ensure :task-item/ready-validate}
     {:db/id "two" :task-item/id #uuid "00000000-0000-4000-8000-000000000026"
      :task-item/index 2 :task-item/content "q"
      :task-item/result :task-item.result/incorrect :task-item/response-state :task-item.response/no-answer :db/ensure :task-item/ready-validate}
     {:db/id "s1" :submission/id #uuid "00000000-0000-4000-8000-000000000027" :submission/index 1
      :submission/result :task-item.result/incorrect :submission/fields ["a1"] :db/ensure :submission/validate}
     {:db/id "s2" :submission/id #uuid "00000000-0000-4000-8000-000000000028" :submission/index 2
      :submission/result :task-item.result/correct :submission/fields ["a2"] :db/ensure :submission/validate}
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
        "learner-task",
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

    // Queue entries belong to the learner; their activity definitions remain shared.
    // The queue records why and how content was selected independently of history.
    let queued = r#"[
     {:db/id "learner" :learner/id "synthetic-queue" :learner/queue ["required" "recommended" "selected"] :db/ensure :learner/validate}
     {:db/id "definition" :review/id #uuid "00000000-0000-4000-8000-000000000050"}
     {:db/id "required" :queue/id #uuid "00000000-0000-4000-8000-000000000054"
      :queue/activity "definition" :queue/index 1 :queue/selection :queue.selection/required
      :queue/reason "Required review after repeated failures." :db/ensure :queue/validate}
     {:db/id "recommended" :queue/id #uuid "00000000-0000-4000-8000-000000000051"
      :queue/activity "definition" :queue/index 2 :queue/selection :queue.selection/recommended
      :queue/reason "Review is due." :db/ensure :queue/validate}
     {:db/id "selected" :queue/id #uuid "00000000-0000-4000-8000-000000000052"
      :queue/activity "definition" :queue/index 3 :queue/selection :queue.selection/self-selected
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
    assert_eq!(entries.len(), 3);
    for entry in &entries {
        assert_eq!(
            db.values(*entry, attribute(&db, "queue", "activity")),
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
         :queue/index 4 :queue/selection :queue.selection/recommended
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
    check_task_item_ownership(&db)?;
    println!("PASS task and activity drafts: six categories identifiable through activity refs, summaries with unknown activity, signed/above-base XP, unknown durations, eight real quiz items, repeated questions/submissions and component deletion preserving canonical content. Authored lesson steps support tutorials and knowledge points, and authored multistep steps reference questions; two attempts keep separate task items and responses while sharing lesson and question content. Deleting one attempt preserves the other attempt, authored steps and shared content. Learner-owned queue entries represent required, recommended and self-selected work, resolve reverse ownership, require activity and cascade on learner deletion while preserving shared definitions. Scheduling obligations and proposed enum/range/ownership-controller rules are not claimed to be enforced by required-attribute specs.");
    Ok(())
}

fn check_task_item_ownership(base: &Database) -> Result<(), Box<dyn Error>> {
    // Attempts at a shared lesson own separate example and question occurrences.
    // Authored placements retain their source MA step IDs independently of
    // those learner records.
    let fixture = r#"[
     {:db/id "topic" :topic/id #uuid "00000000-0000-4000-8000-000000000100"
      :topic/knowledge-points ["kp"]}
     {:db/id "example" :example/id #uuid "00000000-0000-4000-8000-000000000101"
      :example/problem "Select the number 2." :example/explanation "The numeral 2 denotes two."
      :db/ensure :example/validate}
     {:db/id "kp" :knowledge-point/id #uuid "00000000-0000-4000-8000-000000000102"
      :knowledge-point/title "Recognizing two" :knowledge-point/example "example"
      :knowledge-point/questions [[:question/id #uuid "00000000-0000-4000-8000-000000000020"]]
      :db/ensure :knowledge-point/validate}
     {:db/id "lesson" :lesson/id #uuid "00000000-0000-4000-8000-000000000103"
      :lesson/topic "topic" :lesson/steps ["intro-placement" "kp-placement"] :db/ensure :lesson/validate}
     {:db/id "kp-placement" :lesson-step/id #uuid "00000000-0000-4000-8000-000000000104"
      :lesson-step/math-academy-id 900000104 :lesson-step/index 2 :lesson-step/content "kp"
      :db/ensure :lesson-step/validate}
     {:db/id "learner" :learner/id "synthetic-shared-lesson" :learner/activity ["first" "second"]}
     {:db/id "first" :learner-task/id #uuid "00000000-0000-4000-8000-000000000105"
      :learner-task/activity "lesson" :learner-task/title "First attempt" :learner-task/status :learner-task.status/completed
      :learner-task/groups ["first-group"] :learner-task/items ["first-example" "first-question"] :db/ensure :learner-task/ready-validate}
     {:db/id "second" :learner-task/id #uuid "00000000-0000-4000-8000-000000000106"
      :learner-task/activity "lesson" :learner-task/title "Second attempt" :learner-task/status :learner-task.status/completed
      :learner-task/groups ["second-group"] :learner-task/items ["second-example" "second-question"] :db/ensure :learner-task/ready-validate}
     {:db/id "first-example" :task-item/id #uuid "00000000-0000-4000-8000-000000000107"
      :task-item/index 1 :task-item/content "example" :db/ensure :task-item/ready-validate}
     {:db/id "first-question" :task-item/id #uuid "00000000-0000-4000-8000-000000000108"
      :task-item/index 2 :task-item/content [:question/id #uuid "00000000-0000-4000-8000-000000000020"]
      :task-item/result :task-item.result/incorrect :task-item/response-state :task-item.response/recorded
      :task-item/submissions ["first-submission"] :db/ensure :task-item/ready-validate}
     {:db/id "second-example" :task-item/id #uuid "00000000-0000-4000-8000-000000000109"
      :task-item/index 1 :task-item/content "example" :db/ensure :task-item/ready-validate}
     {:db/id "second-question" :task-item/id #uuid "00000000-0000-4000-8000-00000000010a"
      :task-item/index 2 :task-item/content [:question/id #uuid "00000000-0000-4000-8000-000000000020"]
      :task-item/result :task-item.result/correct :task-item/response-state :task-item.response/recorded
      :task-item/submissions ["second-submission"] :db/ensure :task-item/ready-validate}
     {:db/id "first-submission" :submission/id #uuid "00000000-0000-4000-8000-00000000010b"
      :submission/index 1 :submission/fields ["first-response"] :submission/result :task-item.result/incorrect
      :db/ensure :submission/validate}
     {:db/id "second-submission" :submission/id #uuid "00000000-0000-4000-8000-00000000010c"
      :submission/index 1 :submission/fields ["second-response"] :submission/result :task-item.result/correct
      :db/ensure :submission/validate}
     {:db/id "first-group" :task-group/id #uuid "00000000-0000-4000-8000-00000000010d"
      :task-group/index 1 :task-group/lesson-step "kp-placement" :task-group/knowledge-point "kp"
      :db/ensure :task-group/validate}
     {:db/id "second-group" :task-group/id #uuid "00000000-0000-4000-8000-00000000010e"
      :task-group/index 1 :task-group/lesson-step "kp-placement" :task-group/knowledge-point "kp"
      :db/ensure :task-group/validate}
     {:db/id "first-response" :submitted-answer/id #uuid "00000000-0000-4000-8000-00000000010f"
      :submitted-answer/field [:answer-field/id #uuid "00000000-0000-4000-8000-000000000021"]
      :submitted-answer/selected-answer [:answer/id #uuid "00000000-0000-4000-8000-000000000023"]
      :db/ensure :submitted-answer/validate}
     {:db/id "intro" :tutorial/id #uuid "00000000-0000-4000-8000-000000000110"
      :tutorial/title "Introduction" :tutorial/content "Recognize a numeral before selecting it."
      :db/ensure :tutorial/validate}
     {:db/id "intro-placement" :lesson-step/id #uuid "00000000-0000-4000-8000-000000000111"
      :lesson-step/math-academy-id 900000111 :lesson-step/index 1 :lesson-step/content "intro"
      :db/ensure :lesson-step/validate}
     {:db/id "second-response" :submitted-answer/id #uuid "00000000-0000-4000-8000-000000000112"
      :submitted-answer/field [:answer-field/id #uuid "00000000-0000-4000-8000-000000000021"]
      :submitted-answer/selected-answer [:answer/id #uuid "00000000-0000-4000-8000-000000000022"]
      :db/ensure :submitted-answer/validate}
     {:db/id "scenario" :multistep/id #uuid "00000000-0000-4000-8000-000000000120"
      :multistep/title "Recognize a number" :multistep/topics ["topic"] :multistep/steps ["scenario-placement"]
      :db/ensure :multistep/validate}
     {:db/id "scenario-placement" :multistep-step/id #uuid "00000000-0000-4000-8000-000000000121"
      :multistep-step/index 1 :multistep-step/question [:question/id #uuid "00000000-0000-4000-8000-000000000020"]
      :db/ensure :multistep-step/validate}
    ]"#;
    let db = transact(base, fixture, 4900)?.db_after;
    let entity = |ns, suffix: u128| {
        find(
            &db,
            ns,
            "id",
            Value::Uuid(0x00000000000040008000000000000000 + suffix),
        )
    };
    let authored = entity("lesson-step", 0x104);
    let kp = entity("knowledge-point", 0x102);
    assert_eq!(
        db.values(authored, attribute(&db, "lesson-step", "content")),
        vec![&Value::Ref(kp)]
    );
    assert_eq!(
        db.values(authored, attribute(&db, "lesson-step", "math-academy-id")),
        vec![&Value::Long(900000104)]
    );
    for suffix in [0x107, 0x108, 0x109, 0x10a] {
        let performed = entity("task-item", suffix);
        assert_ne!(performed, authored);
        assert!(db
            .values(performed, attribute(&db, "lesson-step", "math-academy-id"))
            .is_empty());
    }
    assert!(db
        .values(authored, attribute(&db, "task-item", "result"))
        .is_empty());
    assert!(db
        .values(authored, attribute(&db, "task-item", "submissions"))
        .is_empty());

    let first = entity("learner-task", 0x105);
    let after = transact(&db, &format!("[[:db.fn/retractEntity {first}]]"), 5000)?.db_after;
    for (ns, suffix) in [
        ("learner-task", 0x105),
        ("task-item", 0x107),
        ("task-item", 0x108),
        ("submission", 0x10b),
        ("task-group", 0x10d),
        ("submitted-answer", 0x10f),
    ] {
        assert!(
            after
                .values(entity(ns, suffix), attribute(&after, ns, "id"))
                .is_empty(),
            "{ns} {suffix:x} must cascade"
        );
    }
    for (ns, suffix) in [
        ("learner-task", 0x106),
        ("task-item", 0x109),
        ("task-item", 0x10a),
        ("submission", 0x10c),
        ("task-group", 0x10e),
        ("submitted-answer", 0x112),
        ("lesson", 0x103),
        ("lesson-step", 0x104),
        ("lesson-step", 0x111),
        ("knowledge-point", 0x102),
        ("example", 0x101),
        ("tutorial", 0x110),
        ("question", 0x020),
        ("answer-field", 0x021),
        ("answer", 0x022),
    ] {
        assert_eq!(
            after
                .values(entity(ns, suffix), attribute(&after, ns, "id"))
                .len(),
            1,
            "{ns} {suffix:x} must survive"
        );
    }
    let scenario = entity("multistep", 0x120);
    let after = transact(
        &after,
        &format!("[[:db.fn/retractEntity {scenario}]]"),
        5100,
    )?
    .db_after;
    assert!(after
        .values(
            entity("multistep-step", 0x121),
            attribute(&after, "multistep-step", "id")
        )
        .is_empty());
    assert_eq!(
        after
            .values(
                entity("question", 0x020),
                attribute(&after, "question", "id")
            )
            .len(),
        1
    );
    Ok(())
}
