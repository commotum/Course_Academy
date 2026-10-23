use super::*;
use edb_core::{Database, EntityRef};

fn fixture() -> Result<DatabaseValue> {
    let source = EntityRef::Ident(Keyword::new("db.source", "system"));
    let mut db = Database::bootstrap()?;
    for schema in [
        include_str!("../../schema/data/5-1-topic.edn"),
        include_str!("../../schema/data/6-knowledge-point.edn"),
        include_str!("../../schema/data/7-question-generator.edn"),
        include_str!("../../schema/content/0-activity.edn"),
        include_str!("../../schema/content/1-step.edn"),
        include_str!("../../schema/content/4-question.edn"),
        include_str!("../../schema/content/5-answer-field.edn"),
        include_str!("../../schema/content/6-answer.edn"),
        include_str!("../../schema/content/8-assigned-problem.edn"),
        include_str!("../../schema/learner/1-1-learner.edn"),
        include_str!("../../schema/learner/2-1-learner-task.edn"),
        include_str!("../../schema/learner/2-2-learner-task-item.edn"),
        include_str!("../../schema/learner/1-3-learner-progress.edn"),
        include_str!("../../schema/engine/1-fire-policy.edn"),
    ] {
        db = db.with_edn(schema, 0, source.clone())?.db_after;
    }
    let mut forms = vec![];
    for (n, name) in [
        "Queue",
        "Target",
        "Unlocked",
        "Due",
        "Refreshed",
        "Assigned review",
        "Assessment",
        "Retake",
        "Locked lesson",
        "Completed review",
    ]
    .iter()
    .enumerate()
    {
        forms.push(format!(r#"{{:db/id "t{n}" :topic/id #uuid "00000000-0000-4000-8000-{n:012}" :topic/title "{name}" :topic/knowledge-points ["kp{n}"]}}"#));
        forms.push(format!(r#"{{:db/id "kp{n}" :knowledge-point/id #uuid "00000000-0000-4000-8001-{n:012}" :knowledge-point/title "KP {name}"}}"#));
    }
    forms.push(r#"
      {:db/id "generator" :db/ident :fixture/generator}
      {:db/id "kp1" :knowledge-point/question-generator "generator"}
      {:db/id "kp6" :knowledge-point/questions ["assessment-q"]}
      {:db/id "kp7" :knowledge-point/questions ["original-q"]}
      {:db/id "assessment-q" :question/id #uuid "00000000-0000-4000-8002-000000000001"}
      {:db/id "original-q" :question/id #uuid "00000000-0000-4000-8002-000000000002"}
      {:db/id "learner" :learner/id "test" :learner/queue ["t0"] :learner/targets ["t1"]
       :learner/activity ["unlocked-task" "locked-task" "review-task" "assessment-task" "retake-task" "completed-task"]
       :learner/knowledge-profile ["due-state" "refreshed-state"]}
      {:db/id "unlocked-task" :learner-task/activity "lesson" :learner-task/status :learner-task.status/unlocked}
      {:db/id "lesson" :activity/type :activity.type/lesson :activity/scope "t2"}
      {:db/id "locked-task" :learner-task/activity "locked-lesson" :learner-task/status :learner-task.status/locked}
      {:db/id "locked-lesson" :activity/type :activity.type/lesson :activity/scope "t8"}
      {:db/id "review-task" :learner-task/activity "review" :learner-task/status :learner-task.status/locked}
      {:db/id "review" :activity/type :activity.type/review :activity/scope "t5"}
      {:db/id "assessment-task" :learner-task/activity "assessment" :learner-task/status :learner-task.status/unlocked}
      {:db/id "assessment" :activity/type :activity.type/assessment :activity/steps ["assessment-step"]}
      {:db/id "assessment-step" :step/content "assessment-q"}
      {:db/id "retake-task" :learner-task/activity "retake" :learner-task/status :learner-task.status/locked
       :learner-task/retake-of "original-task"}
      {:db/id "retake" :activity/type :activity.type/assessment}
      {:db/id "original-task" :learner-task/items ["original-item"]}
      {:db/id "original-item" :task-item/content "original-q"}
      {:db/id "completed-task" :learner-task/activity "completed-review" :learner-task/status :learner-task.status/completed}
      {:db/id "completed-review" :activity/type :activity.type/review :activity/scope "t9"}
      {:db/id "policy" :policy/id #uuid "00000000-0000-4000-8003-000000000001" :policy/review-threshold 0.5}
      {:db/id "due-state" :progress/topic "t3" :progress/learned true :progress/memory 1.0
       :progress/interval-days 1.0 :progress/memory-at #inst "2026-10-10T00:00:00Z" :progress/policy "policy"}
      {:db/id "refreshed-state" :progress/topic "t4" :progress/learned true :progress/memory 1.0
       :progress/interval-days 1.0 :progress/memory-at #inst "2026-10-10T12:00:00Z" :progress/policy "policy"}
    "#.into());
    Ok(db
        .with_edn(&format!("[{}]", forms.join("\n")), 0, source)?
        .db_after
        .database_value())
}
fn identity(db: &DatabaseValue, attr: &str, value: &str) -> Result<u64> {
    let q = format!("[:find ?e :in $ ?v :where [?e :{attr} ?v]]");
    eid(&query(db, &q, vec![EdnValue::String(value.into())])?[0][0])
}
fn titles(result: &Json) -> BTreeSet<String> {
    result
        .as_array()
        .unwrap()
        .iter()
        .map(|v| v["topic/title"].as_str().unwrap().into())
        .collect()
}
fn at(s: &str) -> i64 {
    DateTime::parse_from_rfc3339(s).unwrap().timestamp_millis()
}

#[test]
fn eligibility_includes_selected_studied_and_actual_pending_work() -> Result<()> {
    let db = fixture()?;
    let learner = identity(&db, "learner/id", "test")?;
    let result = candidates(
        &db,
        learner,
        at("2026-10-11T00:00:00Z"),
        None,
        &BTreeSet::new(),
        "assessment",
        false,
    )?;
    assert_eq!(
        titles(&result),
        [
            "Queue",
            "Target",
            "Due",
            "Refreshed",
            "Unlocked",
            "Assigned review",
            "Assessment",
            "Retake"
        ]
        .into_iter()
        .map(String::from)
        .collect()
    );
    let target = result
        .as_array()
        .unwrap()
        .iter()
        .find(|v| v["topic/title"] == "Target")
        .unwrap();
    // A placeholder generator ref is not a registered script.
    assert_eq!(target["knowledge_points"][0]["has_generator"], false);
    assert!(!target["knowledge_points"][0]["generator_entity"].is_null());
    assert_eq!(target["urgency_value"], 4);
    let queue = result
        .as_array()
        .unwrap()
        .iter()
        .find(|v| v["topic/title"] == "Queue")
        .unwrap();
    assert_eq!(queue["knowledge_points"][0]["has_generator"], false);
    assert!(queue["knowledge_points"][0]["generator_entity"].is_null());
    Ok(())
}

#[test]
fn standard_discovery_expands_self_directed_scope_in_one_capture_only() -> Result<()> {
    let db = fixture()?;
    let learner = identity(&db,"learner/id","test")?;
    let request = json!({"selected_only":true,"respect_study_scope":true});
    assert_eq!(discovery_selection(&db,learner,&request)?,(false,true));
    let db = db.with_edn(&format!("[[:db/add {learner} :learner/self-directed true]]"),0,
        EntityRef::Ident(Keyword::new("db.source","system")))?.db_after;
    assert_eq!(discovery_selection(&db,learner,&request)?,(true,false));
    assert_eq!(discovery_selection(&db,learner,&json!({"selected_only":true}))?,(true,true));
    assert_eq!(discovery_selection(&db,learner,&json!({"selected_only":true,"respect_study_scope":false}))?,(true,true));
    assert!(discovery_selection(&db,learner,&json!({"respect_study_scope":"yes"})).is_err());
    Ok(())
}

#[test]
fn self_directed_generation_uses_bounded_graph_scope_and_preserves_explicit_work() -> Result<()> {
    let db = fixture()?;
    let learner = identity(&db,"learner/id","test")?;
    let target = identity(&db,"topic/title","Target")?;
    let target_kp = identity(&db,"knowledge-point/title","KP Target")?;
    let mut forms = vec![format!("[:db/add {learner} :learner/self-directed true]")];
    for n in 0..29 {
        let next = if n == 28 {"outside".to_owned()} else {format!("foundation-{}",n+1)};
        forms.push(format!(r#"{{:db/id "foundation-{n}" :topic/id #uuid "10000000-0000-4000-8000-{n:012}" :topic/next ["{next}"]}}"#));
    }
    forms.push(format!(r#"
        {{:db/id "outside" :topic/id #uuid "10000000-0000-4000-8001-000000000001" :topic/title "Outside preparation" :topic/next ["entry"]}}
        {{:db/id "entry" :topic/id #uuid "10000000-0000-4000-8001-000000000002" :topic/title "Entry lesson" :topic/next ["middle"] :topic/knowledge-points ["entry-kp"]}}
        {{:db/id "entry-kp" :knowledge-point/id #uuid "10000000-0000-4000-8002-000000000002" :knowledge-point/title "Empty entry bank"}}
        {{:db/id "middle" :topic/id #uuid "10000000-0000-4000-8001-000000000003" :topic/title "Known intermediate" :topic/next [{target}]}}
        {{:db/id "middle-progress" :progress/topic "middle" :progress/learned true}}
        [:db/add {learner} :learner/knowledge-profile "middle-progress"]
        [:db/add {target_kp} :knowledge-point/key-prerequisites "outside"]
    "#));
    let db=db.with_edn(&format!("[{}]",forms.join("\n")),0,
        EntityRef::Ident(Keyword::new("db.source","system")))?.db_after;
    let now=at("2026-10-11T00:00:00Z");
    let (self_directed,selected_only)=discovery_selection(&db,learner,
        &json!({"selected_only":true,"respect_study_scope":true}))?;
    assert!(self_directed);
    let mut result=candidates_scoped(&db,learner,now,None,&BTreeSet::new(),"lesson",false,selected_only)?;
    find_candidates_ranking::annotate(&db,learner,now,&mut result)?;
    assert!(titles(&result).contains("Entry lesson"),"learned intermediate does not close scope traversal");
    assert!(!titles(&result).contains("Outside preparation"),"depth-three and KP-only preparation cannot widen scope");
    let row = |title:&str| result.as_array().unwrap().iter().find(|r|r["topic/title"]==title).unwrap();
    assert!(row("Entry lesson")["activity_demands"].as_array().unwrap().iter().any(|d|d["activity_type"]=="lesson"));
    for title in ["Entry lesson","Target"] {
        assert_eq!(row(title)["new_scoped_lesson"],true);
        assert_eq!(row(title)["relevance_tier"],1);
        assert_eq!(row(title)["activity_demands"],json!([{"activity_type":"lesson","relevance_tier":1}]));
    }
    for title in ["Known intermediate","Unlocked","Queue"] {
        assert_eq!(row(title)["new_scoped_lesson"],false);
        assert!(row(title)["activity_demands"].as_array().unwrap().iter().all(|d|d["activity_type"]!="lesson"),
            "{title} must not establish ordinary lesson demand");
    }
    let outside=identity(&db,"topic/title","Outside preparation")?;
    let mut manual=candidates(&db,learner,now,None,&BTreeSet::from([outside]),"lesson",false)?;
    find_candidates_ranking::annotate(&db,learner,now,&mut manual)?;
    let row=manual.as_array().unwrap().iter().find(|r|r["topic/title"]=="Outside preparation").unwrap();
    assert!(row["activity_demands"].as_array().unwrap().iter().any(|d|d["activity_type"]=="lesson" && d["relevance_tier"]==0),
        "explicit generation requests retain their independent authority");
    // Already-started work outside the new lesson scope also retains its
    // immediate supply demand rather than competing as ordinary preparation.
    let active_topic=identity(&db,"topic/title","Unlocked")?;
    let task=eid(&query(&db,
        "[:find ?task :in $ ?topic :where [?activity :activity/scope ?topic] [?task :learner-task/activity ?activity]]",
        vec![input_eid(active_topic)?])?[0][0])?;
    let db=db.with_edn(&format!("[[:db/add {task} :learner-task/status :learner-task.status/started]]"),0,
        EntityRef::Ident(Keyword::new("db.source","system")))?.db_after;
    let result=ranked_fixture(&db,learner)?;
    let active=result.as_array().unwrap().iter().find(|r|r["db/id"]==active_topic).unwrap();
    assert_eq!(active["new_scoped_lesson"],false);
    assert_eq!(active["activity_demands"],json!([{"activity_type":"lesson","relevance_tier":0}]));
    Ok(())
}

#[test]
fn scoped_generation_uses_graph_bands_instead_of_false_flags_or_fractional_history() -> Result<()> {
    let db=fixture()?;
    let learner=identity(&db,"learner/id","test")?;
    let target=identity(&db,"topic/title","Target")?;
    let mut forms=vec![format!("[:db/add {learner} :learner/self-directed true]")];
    for n in 0..29 {
        let next=if n==28 {"band-one\" \"fractional".to_owned()} else {format!("band-foundation-{}",n+1)};
        forms.push(format!(r#"{{:db/id "band-foundation-{n}" :topic/id #uuid "20000000-0000-4000-8000-{n:012}" :topic/next ["{next}"]}}"#));
    }
    forms.push(format!(r#"
        {{:db/id "band-one" :topic/id #uuid "20000000-0000-4000-8001-000000000001" :topic/title "Band one prerequisite" :topic/next [{target}] :topic/knowledge-points ["band-one-kp"]}}
        {{:db/id "band-one-kp" :knowledge-point/id #uuid "20000000-0000-4000-8002-000000000001" :knowledge-point/title "Band one bank"}}
        {{:db/id "fractional" :topic/id #uuid "20000000-0000-4000-8001-000000000002" :topic/title "Fractional prerequisite" :topic/next [{target}] :topic/knowledge-points ["fractional-kp"]}}
        {{:db/id "fractional-kp" :knowledge-point/id #uuid "20000000-0000-4000-8002-000000000002" :knowledge-point/title "Fractional bank"}}
        {{:db/id "band-one-progress" :progress/topic "band-one" :progress/repetitions 1.0 :progress/learned false}}
        {{:db/id "fractional-progress" :progress/topic "fractional" :progress/repetitions 0.5}}
        [:db/add {learner} :learner/knowledge-profile "band-one-progress"]
        [:db/add {learner} :learner/knowledge-profile "fractional-progress"]
    "#));
    let db=db.with_edn(&format!("[{}]",forms.join("\n")),0,
        EntityRef::Ident(Keyword::new("db.source","system")))?.db_after;
    let now=at("2026-10-11T00:00:00Z");
    let band_one=identity(&db,"topic/title","Band one prerequisite")?;
    let fractional=identity(&db,"topic/title","Fractional prerequisite")?;
    let groups=urgency_groups(&db,learner,now)?;
    assert!(!groups.get(&band_one).is_some_and(|groups|groups.iter().any(|(_,name)|name=="selected-prerequisite")));
    assert!(groups[&fractional].iter().any(|(_,name)|name=="selected-prerequisite"));
    assert!(groups[&fractional].iter().any(|(_,name)|name=="studied"),"broad maintenance evidence stays intact");
    // Explicit selection still cannot relabel a band-one topic as ordinary new work.
    let db=db.with_edn(&format!("[[:db/add {learner} :learner/queue {band_one}]]"),0,
        EntityRef::Ident(Keyword::new("db.source","system")))?.db_after;
    let mut result=candidates(&db,learner,now,None,&BTreeSet::new(),"lesson",false)?;
    find_candidates_ranking::annotate(&db,learner,now,&mut result)?;
    let row=|title:&str|result.as_array().unwrap().iter().find(|r|r["topic/title"]==title).unwrap();
    assert_eq!(row("Band one prerequisite")["new_scoped_lesson"],false);
    assert_eq!(row("Fractional prerequisite")["new_scoped_lesson"],true);
    assert_eq!(row("Fractional prerequisite")["relevance_tier"],1);
    assert!(row("Band one prerequisite")["activity_demands"].as_array().unwrap().iter().all(|d|d["activity_type"]!="lesson"));
    assert!(row("Fractional prerequisite")["activity_demands"].as_array().unwrap().iter().any(|d|d["activity_type"]=="lesson"));
    assert_eq!(row("Fractional prerequisite")["next_activity"],"lesson");
    Ok(())
}

#[test]
fn cursor_keeps_full_population_and_scheduler_selection_establishes_demand() -> Result<()> {
    let db = fixture()?;
    let learner = identity(&db, "learner/id", "test")?;
    let topic = identity(&db, "topic/title", "Locked lesson")?;
    let result = candidates(
        &db,
        learner,
        at("2026-10-11T12:00:00Z"),
        Some(&Changes::default()),
        &BTreeSet::from([topic]),
        "assessment",
        false,
    )?;
    assert_eq!(
        titles(&result),
        [
            "Due",
            "Refreshed",
            "Queue",
            "Target",
            "Unlocked",
            "Assigned review",
            "Assessment",
            "Retake",
            "Locked lesson"
        ]
        .into_iter()
        .map(String::from)
        .collect()
    );
    Ok(())
}

#[test]
fn registered_packages_can_be_replenished_outside_build_eligibility() -> Result<()> {
    let db = fixture()?;
    let learner = identity(&db, "learner/id", "test")?;
    let reviewed_kp = identity(&db, "knowledge-point/title", "KP Completed review")?;
    let due_kp = identity(&db, "knowledge-point/title", "KP Due")?;
    let legacy_kp = identity(&db, "knowledge-point/title", "KP Locked lesson")?;
    let db = db
        .with_edn(
            &format!(
                r#"[
      {{:db/id "package" :question-generator/script "generators/aa/{}/generator.py"}}
      {{:db/id "legacy" :question-generator/script "generate/scratch/legacy.py"}}
      {{:db/id "orphan" :question-generator/script "generators/bb/{}/generator.py"}}
      [:db/add {reviewed_kp} :knowledge-point/question-generator "package"]
      [:db/add {due_kp} :knowledge-point/question-generator "package"]
      [:db/add {legacy_kp} :knowledge-point/question-generator "legacy"]
    ]"#,
                "a".repeat(64),
                "b".repeat(64)
            ),
            0,
            EntityRef::Ident(Keyword::new("db.source", "system")),
        )?
        .db_after;
    let now = at("2026-10-11T00:00:00Z");
    let ordinary = candidates(
        &db,
        learner,
        now,
        None,
        &BTreeSet::new(),
        "assessment",
        false,
    )?;
    assert_eq!(
        titles(&ordinary),
        [
            "Queue",
            "Target",
            "Due",
            "Refreshed",
            "Unlocked",
            "Assigned review",
            "Assessment",
            "Retake"
        ]
        .into_iter()
        .map(String::from)
        .collect()
    );
    let mut extended = candidates(
        &db,
        learner,
        now,
        None,
        &BTreeSet::new(),
        "assessment",
        true,
    )?;
    find_candidates_ranking::annotate(&db, learner, now, &mut extended)?;
    assert_eq!(
        titles(&extended),
        [
            "Queue",
            "Target",
            "Due",
            "Refreshed",
            "Unlocked",
            "Assigned review",
            "Assessment",
            "Retake",
            "Completed review"
        ]
        .into_iter()
        .map(String::from)
        .collect()
    );
    let rows = extended.as_array().unwrap();
    let outside = rows
        .iter()
        .find(|r| r["topic/title"] == "Completed review")
        .unwrap();
    assert_eq!(outside["urgency_groups"], json!([]));
    assert_eq!(outside["urgency_value"], 0);
    assert_eq!(outside["studied"], false);
    // Review history is retained independently of selection/eligibility.
    assert_eq!(outside["reviewed"], true);
    assert_eq!(outside["knowledge_points"][0]["has_generator"], true);
    assert_eq!(
        outside["knowledge_points"][0]["inventory"]["available"],
        json!({"easy":0,"moderate":0,"hard":0})
    );
    let due = rows.iter().find(|r| r["topic/title"] == "Due").unwrap();
    assert_eq!(due["urgency_groups"], json!(["current-need", "studied"]));
    assert_eq!(due["urgency_value"], 6);
    assert_eq!(due["studied"], true);
    Ok(())
}

#[test]
fn log_filter_ignores_withdrawals_and_unrelated_learners() {
    let mut changes = Changes::default();
    let pending_states = [2, 3, 4, 5];
    changes.observe(
        1,
        1,
        "learner/queue",
        &Value::Ref(5),
        false,
        &pending_states,
    );
    changes.observe(
        1,
        9,
        "learner/targets",
        &Value::Ref(6),
        true,
        &pending_states,
    );
    changes.observe(
        1,
        7,
        "learner-task/status",
        &Value::Ref(8),
        true,
        &pending_states,
    );
    assert!(changes.selections.is_empty());
    assert!(changes.tasks.is_empty());
    changes.observe(1, 1, "learner/queue", &Value::Ref(5), true, &pending_states);
    changes.observe(
        1,
        7,
        "learner-task/status",
        &Value::Ref(2),
        true,
        &pending_states,
    );
    assert!(changes.selections.contains(&(5, "learner/queue".into())));
    assert!(changes.tasks.contains(&7));
}

#[test]
fn ongoing_lesson_establishes_immediate_demand_outside_selections() -> Result<()> {
    for state in ["started", "paused"] {
        let db = fixture()?;
        let learner = identity(&db, "learner/id", "test")?;
        let task = eid(&query(
            &db,
            "[:find ?task :where [?a :activity/scope ?t] [?t :topic/title \"Locked lesson\"] [?task :learner-task/activity ?a]]",
            vec![],
        )?[0][0])?;
        let state_id = db
            .entid(&Keyword::new("learner-task.status", state))
            .unwrap();
        let db = db
            .with_edn(
                &format!("[[:db/add {task} :learner-task/status :learner-task.status/{state}]]"),
                0,
                EntityRef::Ident(Keyword::new("db.source", "system")),
            )?
            .db_after;
        let now = at("2026-10-11T00:00:00Z");
        let result = candidates(
            &db,
            learner,
            now,
            None,
            &BTreeSet::new(),
            "assessment",
            false,
        )?;
        assert!(titles(&result).contains("Locked lesson"));
        let topic = identity(&db, "topic/title", "Locked lesson")?;
        let db = db
            .with_edn(
                &format!("[[:db/add {learner} :learner/targets {topic}]]"),
                0,
                EntityRef::Ident(Keyword::new("db.source", "system")),
            )?
            .db_after;
        let mut changes = Changes::default();
        changes.observe(
            learner,
            task,
            "learner-task/status",
            &Value::Ref(state_id),
            true,
            &[state_id],
        );
        for changed in [None, Some(&changes)] {
            let mut result = candidates(
                &db,
                learner,
                now,
                changed,
                &BTreeSet::new(),
                "assessment",
                false,
            )?;
            find_candidates_ranking::annotate(&db, learner, now, &mut result)?;
            let row = result
                .as_array()
                .unwrap()
                .iter()
                .find(|r| r["topic/title"] == "Locked lesson")
                .unwrap();
            assert_eq!(row["activity_state"], "needed-now");
            assert_eq!(row["next_activity"], "lesson");
            assert!(row["engine_priority"].as_f64().unwrap() >= 10000.0);
            assert!(
                row["triggers"]
                    .as_array()
                    .unwrap()
                    .iter()
                    .any(|t| t["reason"] == state)
            );
            assert!(!titles(&result).contains("Completed review"));
        }
    }
    Ok(())
}

#[test]
fn refreshed_memory_postpones_review_and_invalid_state_fails() -> Result<()> {
    let now = at("2026-10-11T00:00:00Z");
    assert!(review_due(1.0, now - 86_400_000, 1.0, 0.5, now)?);
    assert!(!review_due(1.0, now - 43_200_000, 1.0, 0.5, now)?);
    assert!(!review_due(1.0, now + 1, 1.0, 0.5, now)?);
    assert!(review_due(1.0, now, 0.0, 0.5, now).is_err());
    Ok(())
}

#[test]
fn ranking_propagates_assignment_deadline_to_prerequisites_without_bank_filtering() -> Result<()> {
    let db = fixture()?;
    let source = EntityRef::Ident(Keyword::new("db.source", "system"));
    let learner = identity(&db, "learner/id", "test")?;
    let queued = identity(&db, "topic/title", "Queue")?;
    let target = identity(&db, "topic/title", "Target")?;
    let foundations = (0..29).map(|n| {
        let next = if n == 28 {queued.to_string()} else {format!("\"deadline-foundation-{}\"",n+1)};
        format!(r#"{{:db/id "deadline-foundation-{n}" :topic/id #uuid "20000000-0000-4000-8000-{n:012}" :topic/next [{next}]}}"#)
    }).collect::<Vec<_>>().join("\n");
    let text = format!(
        r#"[
      {foundations}
      [:db/add {learner} :learner/self-directed true]
      [:db/add {queued} :topic/next {target}]
      {{:db/id "school" :activity/type :activity.type/assignment
        :activity/due #inst "2026-10-15T00:00:00Z" :activity/steps ["school-step"]}}
      {{:db/id "school-step" :step/content "assigned"}}
      {{:db/id "assigned" :assigned-problem/id #uuid "00000000-0000-4000-8004-000000000001" :assigned-problem/topic-coverage [{target}] :assigned-problem/content [:question/id #uuid "00000000-0000-4000-8002-000000000001"]}}
      [:db/add {learner} :learner/assignments "school"]
    ]"#
    );
    let db = db.with_edn(&text, 0, source)?.db_after;
    let now = at("2026-10-11T00:00:00Z");
    let mut result = candidates(
        &db,
        learner,
        now,
        None,
        &BTreeSet::new(),
        "assessment",
        false,
    )?;
    find_candidates_ranking::annotate(&db, learner, now, &mut result)?;
    let rows = result.as_array().unwrap();
    for title in ["Queue", "Target"] {
        let row = rows.iter().find(|r| r["topic/title"] == title).unwrap();
        assert_eq!(row["assignment_due"], "2026-10-15T00:00:00+00:00");
        assert!(row["engine_priority"].as_f64().unwrap() > 500.0);
        assert_eq!(
            row["knowledge_points"][0]["inventory"]["available"]["hard"],
            0
        );
    }
    assert_eq!(
        rows.iter().find(|r| r["topic/title"] == "Queue").unwrap()["activity_state"],
        "queued"
    );
    Ok(())
}

#[test]
fn ranking_inventory_excludes_seen_reserved_and_canonical_questions() -> Result<()> {
    let db = fixture()?;
    let learner = identity(&db, "learner/id", "test")?;
    let kp = query(
        &db,
        "[:find ?k :where [?t :topic/title \"Queue\"] [?t :topic/knowledge-points ?k]]",
        vec![],
    )?[0][0]
        .clone();
    let task=query(&db,"[:find ?task :where [?a :activity/scope ?t] [?t :topic/title \"Unlocked\"] [?task :learner-task/activity ?a]]",vec![])?[0][0].clone();
    let lesson = query(
        &db,
        "[:find ?a :where [?a :activity/scope ?t] [?t :topic/title \"Unlocked\"]]",
        vec![],
    )?[0][0]
        .clone();
    let mut forms = vec![];
    for (n, band) in ["easy", "moderate", "hard", "easy", "easy"]
        .iter()
        .enumerate()
    {
        forms.push(format!(r#"{{:db/id "rq{n}" :question/id #uuid "00000000-0000-4000-8010-{n:012}"
          :question/problem "Choose yes." :question/difficulty :question.difficulty/{band} :question/answer-fields ["rf{n}"]}}
          {{:db/id "rf{n}" :answer-field/id #uuid "00000000-0000-4000-8011-{n:012}"
          :answer-field/key "selection" :answer-field/type :answer-field.type/radio :answer-field/choices ["ra{n}" "rb{n}"] :answer-field/correct "ra{n}"}}
          {{:db/id "ra{n}" :answer/id #uuid "00000000-0000-4000-8012-{n:012}" :answer/type :answer.type/text :answer/value "yes"}}
          {{:db/id "rb{n}" :answer/id #uuid "00000000-0000-4000-8013-{n:012}" :answer/type :answer.type/text :answer/value "no"}}"#));
    }
    forms.push(format!(r#"{{:db/id {kp} :knowledge-point/questions ["rq0" "rq1" "rq2" "rq3" "rq4"] :knowledge-point/canonical-example "rq3"}}
      [:db/add {task} :learner-task/status :learner-task.status/paused]
      [:db/add {task} :learner-task/items "seen-item"]
      {{:db/id "seen-item" :task-item/content "rq2"}}
      {{:db/id {lesson} :activity/steps ["reserved-step"]}}
      {{:db/id "reserved-step" :step/content "rq1"}}"#));
    let db = db
        .with_edn(
            &format!("[{}]", forms.join("\n")),
            0,
            EntityRef::Ident(Keyword::new("db.source", "system")),
        )?
        .db_after;
    let unrated = eid(&query(
        &db,
        "[:find ?q :where [?q :question/id #uuid \"00000000-0000-4000-8010-000000000004\"]]",
        vec![],
    )?[0][0])?;
    let db = db
        .with_edn(
            &format!("[[:db/retract {unrated} :question/difficulty :question.difficulty/easy]]"),
            0,
            EntityRef::Ident(Keyword::new("db.source", "system")),
        )?
        .db_after;
    let now = at("2026-10-11T00:00:00Z");
    let mut result = candidates(
        &db,
        learner,
        now,
        None,
        &BTreeSet::new(),
        "assessment",
        false,
    )?;
    find_candidates_ranking::annotate(&db, learner, now, &mut result)?;
    let queue = result
        .as_array()
        .unwrap()
        .iter()
        .find(|r| r["topic/title"] == "Queue")
        .unwrap();
    assert_eq!(
        queue["knowledge_points"][0]["inventory"]["available"],
        json!({"easy":1,"moderate":0,"hard":0})
    );
    assert_eq!(
        queue["knowledge_points"][0]["inventory"]["available_total"],
        2
    );
    assert_eq!(queue["topic_inventory"]["rated_total"], 1);
    assert_eq!(queue["topic_inventory"]["unrated_total"], 1);
    Ok(())
}

#[test]
fn eligibility_uses_transitive_selected_prerequisites_and_one_hop_speculation() -> Result<()> {
    let db = fixture()?;
    let topic = |title| identity(&db, "topic/title", title);
    let target = topic("Target")?;
    let queue = topic("Queue")?;
    let prerequisite = topic("Unlocked")?;
    let ancestor = topic("Locked lesson")?;
    let descendant = topic("Assessment")?;
    let grandson = topic("Retake")?;
    let key_prerequisite = topic("Assigned review")?;
    let kp_target = identity(&db, "knowledge-point/title", "KP Target")?;
    let kp_descendant = identity(&db, "knowledge-point/title", "KP Completed review")?;
    let db = db
        .with_edn(
            &format!(
                r#"[
        [:db/add {prerequisite} :topic/next {target}]
        [:db/add {ancestor} :topic/next {prerequisite}]
        [:db/add {queue} :topic/next {descendant}]
        [:db/add {descendant} :topic/next {grandson}]
        [:db/add {kp_target} :knowledge-point/key-prerequisites {key_prerequisite}]
        [:db/add {kp_descendant} :knowledge-point/key-prerequisites {queue}]
        [:db/add {queue} :topic/next {target}]
    ]"#
            ),
            0,
            EntityRef::Ident(Keyword::new("db.source", "system")),
        )?
        .db_after;
    let learner = identity(&db, "learner/id", "test")?;
    let result = candidates(
        &db,
        learner,
        at("2026-10-11T00:00:00Z"),
        None,
        &BTreeSet::new(),
        "assessment",
        false,
    )?;
    assert_eq!(
        titles(&result),
        [
            "Queue",
            "Target",
            "Due",
            "Refreshed",
            "Unlocked",
            "Assigned review",
            "Assessment",
            "Retake",
            "Locked lesson",
            "Completed review"
        ]
        .into_iter()
        .map(String::from)
        .collect()
    );
    let rows = result.as_array().unwrap();
    let queue = rows.iter().find(|r| r["topic/title"] == "Queue").unwrap();
    assert_eq!(queue["urgency_groups"], json!(["queued"]));
    assert_eq!(queue["urgency_value"], 3);
    let target = rows.iter().find(|r| r["topic/title"] == "Target").unwrap();
    assert_eq!(target["urgency_value"], 4);
    assert_eq!(
        target["urgency_groups"],
        json!(["target", "studied-or-queued-descendant"])
    );
    Ok(())
}

#[test]
fn lifecycle_uses_completed_history_legacy_progress_and_original_first_study_time() -> Result<()> {
    let db = fixture()?;
    let learner = identity(&db, "learner/id", "test")?;
    let refreshed = identity(&db, "topic/title", "Refreshed")?;
    let imported = identity(&db, "topic/title", "Unlocked")?;
    let unstudied = identity(&db, "topic/title", "Locked lesson")?;
    let generator = db.entid(&Keyword::new("fixture", "generator")).unwrap();
    let refreshed_progress = eid(&query(
        &db,
        "[:find ?progress :in $ ?topic :where [?progress :progress/topic ?topic]]",
        vec![input_eid(refreshed)?],
    )?[0][0])?;
    let db = db.with_edn(&format!(r#"[
      [:db/add {learner} :learner/activity "old-lesson"]
      [:db/add {learner} :learner/activity "new-lesson"]
      [:db/add {learner} :learner/activity "finished-review"]
      {{:db/id "old-lesson" :learner-task/activity "study" :learner-task/status :learner-task.status/completed :learner-task/finished-at #inst "2020-01-01T00:00:00Z"}}
      {{:db/id "new-lesson" :learner-task/activity "study" :learner-task/status :learner-task.status/completed :learner-task/finished-at #inst "2022-01-01T00:00:00Z"}}
      {{:db/id "study" :activity/type :activity.type/lesson :activity/scope {refreshed}}}
      {{:db/id "finished-review" :learner-task/activity "reviewed" :learner-task/status :learner-task.status/completed}}
      {{:db/id "reviewed" :activity/type :activity.type/review :activity/scope {refreshed}}}
      [:db/add {learner} :learner/knowledge-profile "legacy-progress"]
      {{:db/id "legacy-progress" :progress/topic {imported} :progress/repetitions 2.0}}
      [:db/add {learner} :learner/knowledge-profile "not-learned"]
      {{:db/id "not-learned" :progress/topic {unstudied} :progress/repetitions 2.0 :progress/learned false}}
      [:db/add {generator} :question-generator/script "generators/aa/hash/generator.py"]
      [:db/add {refreshed_progress} :progress/learned false]
    ]"#), 0, EntityRef::Ident(Keyword::new("db.source", "system")))?.db_after;
    let now = at("2026-10-10T12:00:00Z");
    let mut result = candidates(
        &db,
        learner,
        now,
        None,
        &BTreeSet::new(),
        "assessment",
        false,
    )?;
    find_candidates_ranking::annotate(&db, learner, now, &mut result)?;
    let rows = result.as_array().unwrap();
    let refreshed = rows
        .iter()
        .find(|r| r["topic/title"] == "Refreshed")
        .unwrap();
    // Current unlearned state reopens lesson demand without erasing history.
    assert_eq!(refreshed["next_activity"], "lesson");
    assert_eq!(refreshed["studied"], true);
    assert_eq!(refreshed["reviewed"], true);
    assert_eq!(refreshed["first_studied_at"], "2020-01-01T00:00:00+00:00");
    let imported = rows
        .iter()
        .find(|r| r["topic/title"] == "Unlocked")
        .unwrap();
    assert_eq!(imported["studied"], true);
    // Its explicitly unlocked lesson wins over the lifecycle review fallback.
    assert_eq!(imported["next_activity"], "lesson");
    assert_eq!(imported["first_studied_at"], Json::Null);
    assert!(!titles(&result).contains("Locked lesson"));
    let target = rows.iter().find(|r| r["topic/title"] == "Target").unwrap();
    assert_eq!(target["knowledge_points"][0]["has_generator"], true);
    assert_eq!(
        target["knowledge_points"][0]["generator_script"],
        "generators/aa/hash/generator.py"
    );
    Ok(())
}

#[test]
fn completed_lesson_lookup_does_not_cross_owned_tasks_with_unrelated_lessons() -> Result<()> {
    let db = fixture()?;
    let topic = identity(&db, "topic/title", "Locked lesson")?;
    let mut forms = vec![format!(
        "{{:db/id \"owned-lesson\" :activity/type :activity.type/lesson :activity/scope {topic}}}"
    )];
    // Each input task refers to one lesson. The unrelated catalog must never
    // become a Cartesian product with the bound task collection: 200 x 600
    // would exceed the production query's unchanged 100,000-row allowance.
    for n in 0..200 {
        forms.push(format!(
            "{{:db/ident :completed-lookup/task-{n} :learner-task/status :learner-task.status/completed :learner-task/activity \"owned-lesson\"}}"
        ));
    }
    for n in 0..600 {
        forms.push(format!(
            "{{:db/id \"unrelated-lesson-{n}\" :activity/type :activity.type/lesson :activity/scope {topic}}}"
        ));
    }
    let db = db
        .with_edn(
            &format!("[{}]", forms.join("\n")),
            0,
            EntityRef::Ident(Keyword::new("db.source", "system")),
        )?
        .db_after;
    let tasks: BTreeSet<_> = (0..200)
        .map(|n| {
            db.entid(&Keyword::new("completed-lookup", format!("task-{n}")))
                .unwrap()
        })
        .collect();
    assert_eq!(
        query(&db, COMPLETED_LESSONS, vec![ids(&tasks)?])?,
        vec![vec![json!(topic)]]
    );
    Ok(())
}

#[test]
fn selected_prerequisites_use_current_retention_and_preserve_review_vs_lesson_demand() -> Result<()>
{
    let db = fixture()?;
    let learner = identity(&db, "learner/id", "test")?;
    let target = identity(&db, "topic/title", "Target")?;
    let due = identity(&db, "topic/title", "Due")?;
    let ready = identity(&db, "topic/title", "Refreshed")?;
    let forgotten = identity(&db, "topic/title", "Locked lesson")?;
    let behind_ready = identity(&db, "topic/title", "Completed review")?;
    let policy = eid(&query(
        &db,
        "[:find ?p :where [?p :policy/review-threshold _]]",
        vec![],
    )?[0][0])?;
    let mut forms = vec![format!(
        r#"
      [:db/add {due} :topic/next {target}]
      [:db/add {ready} :topic/next {target}]
      [:db/add {forgotten} :topic/next {target}]
      [:db/add {behind_ready} :topic/next {ready}]
      [:db/add {learner} :learner/activity "past-forgotten"]
      {{:db/id "past-forgotten" :learner-task/activity "old-forgotten-lesson" :learner-task/status :learner-task.status/completed}}
      {{:db/id "old-forgotten-lesson" :activity/type :activity.type/lesson :activity/scope {forgotten}}}
      [:db/add {learner} :learner/knowledge-profile "forgotten-state"]
      {{:db/id "forgotten-state" :progress/topic {forgotten} :progress/learned false
        :progress/memory 0.0 :progress/interval-days 1.0 :progress/memory-at #inst "2026-10-10T00:00:00Z"
        :progress/policy {policy} :progress/repetitions 2.0 :progress/assessment-accuracy 1.0
        :progress/practice-accuracy 1.0 :progress/assessment-mass 1.0 :progress/practice-mass 1.0}}
    "#
    )];
    for topic in [due, ready] {
        let progress = eid(&query(
            &db,
            "[:find ?p :in $ ?t :where [?p :progress/topic ?t]]",
            vec![input_eid(topic)?],
        )?[0][0])?;
        forms.push(format!(r#"{{:db/id {progress} :progress/repetitions 2.0 :progress/assessment-accuracy 1.0
          :progress/practice-accuracy 1.0 :progress/assessment-mass 1.0 :progress/practice-mass 1.0}}"#));
    }
    let db = db
        .with_edn(
            &format!("[{}]", forms.join("\n")),
            0,
            EntityRef::Ident(Keyword::new("db.source", "system")),
        )?
        .db_after;
    let result = ranked_fixture(&db, learner)?;
    let rows = result.as_array().unwrap();
    let row = rows.iter().find(|t| t["db/id"] == due).unwrap();
    assert_eq!(row["relevance_tier"], 2);
    assert_eq!(
        row["activity_demands"],
        json!([{"activity_type":"review","relevance_tier":2}])
    );
    let row = rows.iter().find(|t| t["db/id"] == forgotten).unwrap();
    assert_eq!(row["studied"], true);
    assert_eq!(row["completed_local_lesson"], true);
    assert_eq!(row["relevance_tier"], 2);
    assert_eq!(
        row["activity_demands"],
        json!([{"activity_type":"lesson","relevance_tier":2}])
    );
    let row = rows.iter().find(|t| t["db/id"] == ready).unwrap();
    assert_eq!(row["relevance_tier"], 4);
    assert!(!rows.iter().any(|t| t["db/id"] == behind_ready));
    Ok(())
}

#[test]
fn direct_selection_precedes_foundation_relevance_regardless_of_layer() -> Result<()> {
    let db = fixture()?;
    let learner = identity(&db, "learner/id", "test")?;
    let foundation = identity(&db, "topic/title", "Locked lesson")?;
    let queue = identity(&db, "topic/title", "Queue")?;
    let target = identity(&db, "topic/title", "Target")?;
    let mut forms = vec![format!("[:db/add {foundation} :topic/next {queue}]")];
    for layer in 2..38 {
        forms.push(format!(r#"{{:db/id "layer-{layer}" :topic/id #uuid "00000000-0000-4000-8020-{layer:012}" :topic/title "Layer {layer}"}}"#));
        if layer == 2 {
            forms.push(format!(r#"[:db/add {queue} :topic/next "layer-{layer}"]"#));
        } else {
            forms.push(format!(
                r#"[:db/add "layer-{}" :topic/next "layer-{layer}"]"#,
                layer - 1
            ));
        }
    }
    forms.push(format!(r#"[:db/add "layer-37" :topic/next {target}]"#));
    let db = db
        .with_edn(
            &format!("[{}]", forms.join("\n")),
            0,
            EntityRef::Ident(Keyword::new("db.source", "system")),
        )?
        .db_after;
    let mut result = candidates(
        &db,
        learner,
        at("2026-10-11T00:00:00Z"),
        None,
        &BTreeSet::new(),
        "assessment",
        false,
    )?;
    // Both memberships may be present in captured metadata. Direct selection
    // wins even for the queue topic that is also an ancestor of this target.
    result
        .as_array_mut()
        .unwrap()
        .iter_mut()
        .find(|t| t["db/id"] == queue)
        .unwrap()["urgency_groups"]
        .as_array_mut()
        .unwrap()
        .push(json!("selected-prerequisite"));
    find_candidates_ranking::annotate(&db, learner, at("2026-10-11T00:00:00Z"), &mut result)?;
    let rows = result.as_array().unwrap();
    for (topic, layer, tier) in [(foundation, 0, 2), (queue, 1, 1), (target, 38, 1)] {
        let row = rows.iter().find(|t| t["db/id"] == topic).unwrap();
        assert_eq!(row["topic_layer"], layer);
        assert_eq!(row["relevance_tier"], tier);
        assert_eq!(
            row["activity_demands"],
            json!([{"activity_type":"lesson","relevance_tier":tier}])
        );
    }
    Ok(())
}

#[test]
fn selected_only_discovery_keeps_all_direct_kps_without_expanding_other_work() -> Result<()> {
    let db = fixture()?;
    let learner = identity(&db, "learner/id", "test")?;
    let queue = identity(&db, "topic/title", "Queue")?;
    let target = identity(&db, "topic/title", "Target")?;
    let prerequisite = identity(&db, "topic/title", "Locked lesson")?;
    let downstream = identity(&db, "topic/title", "Refreshed")?;
    let registered_kp = identity(&db, "knowledge-point/title", "KP Completed review")?;
    let generator = db.entid(&Keyword::new("fixture", "generator")).unwrap();
    let script = format!("generators/aa/{}/generator.py", "a".repeat(64));
    let source = EntityRef::Ident(Keyword::new("db.source", "system"));
    let db = db.with_edn(&format!(r#"[
      [:db/add {prerequisite} :topic/next {queue}]
      [:db/add {queue} :topic/next {downstream}]
      [:db/add {registered_kp} :knowledge-point/question-generator {generator}]
      [:db/add {generator} :question-generator/script "{script}"]
      [:db/add {learner} :learner/knowledge-profile "queued-import"]
      {{:db/id "queued-import" :progress/topic {queue} :progress/learned true :progress/repetitions 2.0}}
    ]"#), 0, source.clone())?.db_after;
    let now = at("2026-10-11T00:00:00Z");
    let mut selected = candidates_scoped(
        &db,
        learner,
        now,
        None,
        &BTreeSet::from([prerequisite]),
        "lesson",
        false,
        true,
    )?;
    assert_eq!(
        titles(&selected),
        ["Queue", "Target"].into_iter().map(String::from).collect()
    );
    find_candidates_ranking::annotate(&db, learner, now, &mut selected)?;
    let rows = selected.as_array().unwrap();
    let queued = rows.iter().find(|t| t["db/id"] == queue).unwrap();
    assert_eq!(queued["knowledge_points"].as_array().unwrap().len(), 1);
    assert_eq!(queued["knowledge_points"][0]["has_generator"], false);
    assert_eq!(
        queued["knowledge_points"][0]["inventory"]["available_total"],
        0
    );
    assert_eq!(queued["studied"], true);
    assert_eq!(
        queued["activity_demands"],
        json!([
            {"activity_type":"lesson","relevance_tier":1},
            {"activity_type":"review","relevance_tier":1}
        ])
    );
    let targeted = rows.iter().find(|t| t["db/id"] == target).unwrap();
    assert_eq!(targeted["knowledge_points"].as_array().unwrap().len(), 1);
    assert_eq!(targeted["knowledge_points"][0]["has_generator"], true);
    assert_eq!(targeted["knowledge_points"][0]["generator_script"], script);
    assert_eq!(
        targeted["knowledge_points"][0]["inventory"]["available_total"],
        0
    );
    let mut full = candidates_scoped(
        &db,
        learner,
        now,
        None,
        &BTreeSet::new(),
        "assessment",
        true,
        false,
    )?;
    find_candidates_ranking::annotate(&db, learner, now, &mut full)?;
    for title in [
        "Locked lesson",
        "Refreshed",
        "Due",
        "Completed review",
        "Unlocked",
        "Assigned review",
        "Assessment",
        "Retake",
    ] {
        assert!(titles(&full).contains(title), "full mode omitted {title}");
    }
    for direct in rows {
        let full = full
            .as_array()
            .unwrap()
            .iter()
            .find(|t| t["db/id"] == direct["db/id"])
            .unwrap();
        for field in [
            "studied",
            "relevance_tier",
            "topic_layer",
            "selected_support_count",
            "activity_demands",
            "completed_local_lesson",
            "topic_inventory",
        ] {
            assert_eq!(
                direct[field], full[field],
                "selected metadata differs for {field}"
            );
        }
    }
    let db = db
        .with_edn(
            &format!(
                r#"[
      [:db/retract {learner} :learner/queue {queue}]
      [:db/retract {learner} :learner/targets {target}]
    ]"#
            ),
            0,
            source,
        )?
        .db_after;
    assert_eq!(
        candidates_scoped(
            &db,
            learner,
            now,
            None,
            &BTreeSet::new(),
            "assessment",
            false,
            true
        )?,
        json!([])
    );
    Ok(())
}

#[test]
fn selected_only_refill_maintenance_includes_only_registered_outside_kps() -> Result<()> {
    let db = fixture()?;
    let learner = identity(&db, "learner/id", "test")?;
    let queue = identity(&db, "topic/title", "Queue")?;
    let target = identity(&db, "topic/title", "Target")?;
    let outside = identity(&db, "topic/title", "Completed review")?;
    let registered_kp = identity(&db, "knowledge-point/title", "KP Completed review")?;
    let generator = db.entid(&Keyword::new("fixture", "generator")).unwrap();
    let source = EntityRef::Ident(Keyword::new("db.source", "system"));
    let script = format!("generators/aa/{}/generator.py", "a".repeat(64));
    let db = db.with_edn(&format!(r#"[
      [:db/add {registered_kp} :knowledge-point/question-generator {generator}]
      [:db/add {generator} :question-generator/script "{script}"]
      [:db/add {outside} :topic/knowledge-points "unregistered-sibling"]
      [:db/add {outside} :topic/knowledge-points "legacy-sibling"]
      {{:db/id "unregistered-sibling" :knowledge-point/id #uuid "00000000-0000-4000-8030-000000000001" :knowledge-point/title "Unregistered sibling"}}
      {{:db/id "legacy-sibling" :knowledge-point/id #uuid "00000000-0000-4000-8030-000000000002" :knowledge-point/title "Legacy sibling" :knowledge-point/question-generator "legacy-generator"}}
      {{:db/id "legacy-generator" :question-generator/script "legacy/generator.py"}}
    ]"#), 0, source.clone())?.db_after;
    let now = at("2026-10-11T00:00:00Z");
    let mut result = candidates_scoped(
        &db,
        learner,
        now,
        None,
        &BTreeSet::new(),
        "assessment",
        true,
        true,
    )?;
    assert_eq!(
        titles(&result),
        ["Queue", "Target", "Completed review"]
            .into_iter()
            .map(String::from)
            .collect()
    );
    find_candidates_ranking::annotate(&db, learner, now, &mut result)?;
    let outside_record = result
        .as_array()
        .unwrap()
        .iter()
        .find(|t| t["db/id"] == outside)
        .unwrap();
    let kps = outside_record["knowledge_points"].as_array().unwrap();
    assert_eq!(kps.len(), 1);
    assert_eq!(kps[0]["db/id"], registered_kp);
    assert_eq!(kps[0]["generator_script"], script);
    assert_eq!(kps[0]["inventory"]["available_total"], 0);
    // This is maintenance metadata, not a new selected-topic obligation.
    assert_eq!(outside_record["urgency_groups"], json!([]));

    let db = db
        .with_edn(
            &format!(
                r#"[
      [:db/retract {learner} :learner/queue {queue}]
      [:db/retract {learner} :learner/targets {target}]
    ]"#
            ),
            0,
            source,
        )?
        .db_after;
    let result = candidates_scoped(
        &db,
        learner,
        now,
        None,
        &BTreeSet::new(),
        "assessment",
        true,
        true,
    )?;
    assert_eq!(
        titles(&result),
        ["Target", "Completed review"]
            .into_iter()
            .map(String::from)
            .collect()
    );
    assert!(
        result
            .as_array()
            .unwrap()
            .iter()
            .all(|topic| topic["knowledge_points"].as_array().unwrap().len() == 1)
    );
    assert_eq!(
        candidates_scoped(
            &db,
            learner,
            now,
            None,
            &BTreeSet::new(),
            "assessment",
            false,
            true,
        )?,
        json!([])
    );
    Ok(())
}

fn ranked_fixture(db: &DatabaseValue, learner: u64) -> Result<Json> {
    let now = at("2026-10-11T00:00:00Z");
    let mut result = candidates(
        db,
        learner,
        now,
        None,
        &BTreeSet::new(),
        "assessment",
        false,
    )?;
    find_candidates_ranking::annotate(db, learner, now, &mut result)?;
    Ok(result)
}

#[test]
fn imported_mastery_does_not_hide_selected_fresh_lesson_but_local_completion_does() -> Result<()> {
    let db = fixture()?;
    let learner = identity(&db, "learner/id", "test")?;
    let target = identity(&db, "topic/title", "Target")?;
    let source = EntityRef::Ident(Keyword::new("db.source", "system"));
    let db = db.with_edn(&format!(r#"[
      [:db/add {learner} :learner/knowledge-profile "imported-target"]
      {{:db/id "imported-target" :progress/topic {target} :progress/learned true :progress/repetitions 2.0}}
    ]"#), 0, source.clone())?.db_after;
    let result = ranked_fixture(&db, learner)?;
    let row = result
        .as_array()
        .unwrap()
        .iter()
        .find(|t| t["db/id"] == target)
        .unwrap();
    assert_eq!(row["studied"], true);
    assert_eq!(row["completed_local_lesson"], false);
    assert_eq!(row["next_activity"], "review");
    assert_eq!(
        row["activity_demands"],
        json!([
            {"activity_type":"lesson","relevance_tier":1},
            {"activity_type":"review","relevance_tier":1}
        ])
    );
    let rows = result.as_array().unwrap();
    let refreshed = rows
        .iter()
        .find(|t| t["topic/title"] == "Refreshed")
        .unwrap();
    assert_eq!(refreshed["relevance_tier"], 4);
    assert_eq!(refreshed["review_due_at"], "2026-10-11T12:00:00+00:00");
    let due = rows.iter().find(|t| t["topic/title"] == "Due").unwrap();
    assert_eq!(due["relevance_tier"], 3);
    assert_eq!(due["review_due_at"], "2026-10-11T00:00:00+00:00");

    let db = db.with_edn(&format!(r#"[
      [:db/add {learner} :learner/activity "finished-target"]
      {{:db/id "finished-target" :learner-task/activity "target-lesson" :learner-task/status :learner-task.status/completed}}
      {{:db/id "target-lesson" :activity/type :activity.type/lesson :activity/scope {target}}}
    ]"#), 0, source.clone())?.db_after;
    let result = ranked_fixture(&db, learner)?;
    let row = result
        .as_array()
        .unwrap()
        .iter()
        .find(|t| t["db/id"] == target)
        .unwrap();
    assert_eq!(row["completed_local_lesson"], true);
    assert_eq!(
        row["activity_demands"],
        json!([{"activity_type":"review","relevance_tier":1}])
    );
    let db = db.with_edn(&format!(r#"[
      [:db/add {learner} :learner/activity "finished-target-review"]
      {{:db/id "finished-target-review" :learner-task/activity "target-review" :learner-task/status :learner-task.status/completed}}
      {{:db/id "target-review" :activity/type :activity.type/review :activity/scope {target}}}
    ]"#), 0, source.clone())?.db_after;
    let result = ranked_fixture(&db, learner)?;
    let row = result
        .as_array()
        .unwrap()
        .iter()
        .find(|t| t["db/id"] == target)
        .unwrap();
    assert_eq!(row["next_activity"], "assessment");
    assert_eq!(
        row["activity_demands"],
        json!([{"activity_type":"assessment","relevance_tier":4}])
    );
    let db = db
        .with_edn(
            &format!("[[:db/add {learner} :learner/queue {target}]]"),
            0,
            source,
        )?
        .db_after;
    let result = ranked_fixture(&db, learner)?;
    let row = result
        .as_array()
        .unwrap()
        .iter()
        .find(|t| t["db/id"] == target)
        .unwrap();
    assert!(
        row["activity_demands"]
            .as_array()
            .unwrap()
            .contains(&json!({"activity_type":"lesson","relevance_tier":1}))
    );
    Ok(())
}

#[test]
fn selected_support_deduplicates_membership_and_diamond_paths_and_uses_global_layers() -> Result<()>
{
    let db = fixture()?;
    let learner = identity(&db, "learner/id", "test")?;
    let root = identity(&db, "topic/title", "Locked lesson")?;
    let left = identity(&db, "topic/title", "Unlocked")?;
    let right = identity(&db, "topic/title", "Assigned review")?;
    let queue = identity(&db, "topic/title", "Queue")?;
    let target = identity(&db, "topic/title", "Target")?;
    let db = db
        .with_edn(
            &format!(
                r#"[
      [:db/add {learner} :learner/queue {target}]
      [:db/add {root} :topic/next {left}]
      [:db/add {root} :topic/next {right}]
      [:db/add {root} :topic/next {queue}]
      [:db/add {left} :topic/next {target}]
      [:db/add {right} :topic/next {target}]
    ]"#
            ),
            0,
            EntityRef::Ident(Keyword::new("db.source", "system")),
        )?
        .db_after;
    let result = ranked_fixture(&db, learner)?;
    let rows = result.as_array().unwrap();
    for (id, layer, support) in [
        (root, 0, 2),
        (left, 1, 1),
        (right, 1, 1),
        (queue, 1, 1),
        (target, 2, 1),
    ] {
        let row = rows.iter().find(|t| t["db/id"] == id).unwrap();
        assert_eq!(
            row["relevance_tier"],
            if id == queue || id == target { 1 } else { 2 }
        );
        assert_eq!(row["topic_layer"], layer);
        assert_eq!(row["selected_support_count"], support);
    }
    let root = rows.iter().find(|t| t["db/id"] == root).unwrap();
    assert!(
        root["urgency_groups"]
            .as_array()
            .unwrap()
            .contains(&json!("selected-prerequisite"))
    );
    Ok(())
}

#[test]
fn required_review_upgrades_only_review_and_locked_remediation_lessons_are_eligible() -> Result<()>
{
    let db = fixture()?;
    let learner = identity(&db, "learner/id", "test")?;
    let queue = identity(&db, "topic/title", "Queue")?;
    let locked = identity(&db, "topic/title", "Locked lesson")?;
    let locked_task = eid(&query(
        &db,
        "[:find ?task :in $ ?topic :where [?a :activity/scope ?topic] [?task :learner-task/activity ?a]]",
        vec![input_eid(locked)?],
    )?[0][0])?;
    assert!(!titles(&ranked_fixture(&db, learner)?).contains("Locked lesson"));
    let db = db
        .with_edn(
            &format!(
                r#"[
      [:db/add {learner} :learner/activity "required-review"]
      {{:db/id "required-review" :learner-task/status :learner-task.status/locked
        :learner-task/activity "repair-review" :learner-task/remediation-for {locked_task}}}
      {{:db/id "repair-review" :activity/type :activity.type/review :activity/scope {queue}}}
      [:db/add {locked_task} :learner-task/remediation-for "required-review"]
    ]"#
            ),
            0,
            EntityRef::Ident(Keyword::new("db.source", "system")),
        )?
        .db_after;
    let result = ranked_fixture(&db, learner)?;
    let row = result
        .as_array()
        .unwrap()
        .iter()
        .find(|t| t["db/id"] == queue)
        .unwrap();
    assert_eq!(row["relevance_tier"], 1);
    assert_eq!(
        row["activity_demands"],
        json!([
            {"activity_type":"lesson","relevance_tier":1},
            {"activity_type":"review","relevance_tier":0}
        ])
    );
    let row = result
        .as_array()
        .unwrap()
        .iter()
        .find(|t| t["db/id"] == locked)
        .unwrap();
    assert_eq!(row["relevance_tier"], 3);
    assert_eq!(
        row["activity_demands"],
        json!([{"activity_type":"lesson","relevance_tier":0}])
    );
    Ok(())
}
