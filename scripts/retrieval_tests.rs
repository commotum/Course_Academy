//! Full generic retrieval transactions against an isolated in-memory EDB.
use super::*;
use edb_core::{DB_SOURCE_SYSTEM, Database, TxFunctions};

struct Fixture {
    db: Database,
    learner: u64,
    now: i64,
    // Existing fixtures exercise normal study; focused tests opt in explicitly.
    focused_mode: bool,
}
impl Fixture {
    fn tx(&mut self, forms: Vec<Json>, at: i64) -> Result<()> {
        let mut functions = TxFunctions::new();
        preview_answer_fields::register_answer_field_predicates(&mut functions);
        preview_progress::register_progress_predicates(&mut functions);
        preview_configuration::register_configuration_predicates(&mut functions);
        self.db = self
            .db
            .with_forms(
                &edb_core::edn_transaction::read_edn_transaction(&schema::edn(&json!(forms))?)?,
                &functions,
                at,
                engine_source(),
            )?
            .db_after;
        Ok(())
    }
    fn snapshot(&self) -> Result<EntitySnapshot> {
        let mut captured = snapshot(&self.db.database_value())?;
        captured.focused_mode = self.focused_mode;
        Ok(captured)
    }
    fn act(&mut self, action: &str, body: Json, at: i64) -> Result<EntitySnapshot> {
        let (forms, _) = mutate(
            &self.snapshot()?,
            self.learner,
            action,
            &body,
            DateTime::from_timestamp_millis(at).unwrap(),
        )?;
        if !forms.is_empty() {
            self.tx(forms, at)?;
        }
        self.snapshot()
    }
    fn new(due: bool) -> Result<Self> {
        Self::with_admission(due, 3 * 86400000, true)
    }
    fn with_admission(due: bool, lesson_age_ms: i64, prior_review: bool) -> Result<Self> {
        Self::with_history(due, lesson_age_ms, prior_review, false)
    }
    fn with_history(due: bool, lesson_age_ms: i64, prior_review: bool, migrated: bool) -> Result<Self> {
        let mut db = Database::bootstrap()?;
        for (index, schema) in [
            include_str!("../schema/data/2-course.edn"),
            include_str!("../schema/data/3-unit.edn"),
            include_str!("../schema/data/4-module.edn"),
            include_str!("../schema/data/5-1-topic.edn"),
            include_str!("../schema/data/5-2-encompassing.edn"),
            include_str!("../schema/data/6-knowledge-point.edn"),
            include_str!("../schema/content/0-activity.edn"),
            include_str!("../schema/content/1-step.edn"),
            include_str!("../schema/content/4-question.edn"),
            include_str!("../schema/content/5-answer-field.edn"),
            include_str!("../schema/content/6-answer.edn"),
            include_str!("../schema/content/7-multistep.edn"),
            include_str!("../schema/learner/1-1-learner.edn"),
            include_str!("../schema/learner/1-2-learner-performance.edn"),
            include_str!("../schema/learner/1-3-learner-progress.edn"),
            include_str!("../schema/learner/2-1-learner-task.edn"),
            include_str!("../schema/learner/2-2-learner-task-item.edn"),
            include_str!("../schema/engine/1-fire-policy.edn"),
            include_str!("../schema/engine/2-question-weights.edn"),
        ]
        .into_iter()
        .enumerate()
        {
            db = db
                .with_edn(schema, index as i64 + 1, EntityRef::Id(DB_SOURCE_SYSTEM))?
                .db_after;
        }
        db = db
            .with_edn(
                "[{:db/ident :application/ca-engine}]",
                100,
                EntityRef::Id(DB_SOURCE_SYSTEM),
            )?
            .db_after;
        let now = Utc::now().timestamp_millis() - 60_000;
        let mut f = Self {
            db,
            learner: 0,
            now,
            focused_mode: false,
        };
        let id = |n: u128| json!({"$uuid":uuid(n)});
        let defaults = serde_json::to_value(course_academy_engine::core::Policy::default())?;
        let mut policy = json!({"db/id":"policy","policy/id":id(1),"policy/retention-update-order":kw("policy.retention-update/decay-before-add"),"db/ensure":kw("policy/validate")});
        for (attr, field) in [
            ("base-half-life-days", "base_interval_days"),
            ("interval-growth", "interval_growth"),
            ("maximum-half-life-days", "maximum_interval_days"),
            ("review-threshold", "due_threshold"),
            ("initial-retention", "restored_memory"),
            ("early-practice-discount-power", "discount_power"),
            ("initial-accuracy", "prior_accuracy"),
            ("accuracy-update-rate", "accuracy_alpha"),
            ("speed-exponent", "speed_exponent"),
            ("minimum-speed", "minimum_speed"),
            ("maximum-speed", "maximum_speed"),
            ("overdue-failure-slope", "failure_overdue_slope"),
            ("maximum-failure-multiplier", "maximum_failure_multiplier"),
            ("gate-slow-implicit", "gate_slow_implicit"),
            ("future-horizon-days", "future_horizon_days"),
        ] {
            policy[format!("policy/{attr}")] = defaults[field].clone();
        }
        let mut forms = vec![
            policy,
            json!({"db/id":"course","course/id":id(2),"course/title":"Retrieval fixture","course/units":["unit"]}),
            json!({"db/id":"unit","unit/id":id(3),"unit/modules":["module"]}),
            json!({"db/id":"module","module/id":id(4),"module/topics":(0..5).map(|i| format!("topic-{i}")).collect::<Vec<_>>()}),
            json!({"db/id":"learner","learner/id":"retrieval-test","learner/course":"course","learner/knowledge-profile":(0..5).map(|i|format!("progress-{i}")).collect::<Vec<_>>(),"learner/activity":(0..5).map(|i|format!("mastered-{i}")).collect::<Vec<_>>()}),
        ];
        forms.push(json!({"db/id":"policy","policy/question-selection-weights":[{
            "question-weights/activity-type":kw("activity.type/assessment"),
            "question-weights/initial-easy":50.0,"question-weights/initial-moderate":40.0,"question-weights/initial-hard":10.0,
            "question-weights/remedial-easy":45.0,"question-weights/remedial-moderate":40.0,"question-weights/remedial-hard":15.0,
            "db/ensure":kw("question-weights/validate")
        }]}));
        for topic in 0..5 {
            forms.push(json!({"db/id":format!("topic-{topic}"),"topic/id":id(10+topic),"topic/title":format!("Topic {topic}"),"topic/knowledge-points":[format!("kp-{topic}")]}));
            forms.push(json!({"db/id":format!("kp-{topic}"),"knowledge-point/id":id(20+topic),"knowledge-point/canonical-example":format!("example-{topic}"),"knowledge-point/questions":(0..30).map(|q|format!("q-{topic}-{q}")).collect::<Vec<_>>()}));
            forms.push(json!({"db/id":format!("progress-{topic}"),"progress/id":format!("p-{topic}"),"progress/topic":format!("topic-{topic}"),"progress/policy":"policy","progress/learned":true,"progress/repetitions":2.0,"progress/memory":if due {0.1}else{1.0},"progress/memory-at":{"$instant":now},"progress/interval-days":1.0,"progress/assessment-accuracy":0.5,"progress/practice-accuracy":0.5,"progress/assessment-mass":0.0,"progress/practice-mass":0.0}));
            forms.push(json!({"db/id":format!("lesson-{topic}"),"activity/id":id(30+topic),"activity/title":"Previously learned","activity/type":kw("activity.type/lesson"),"activity/scope":format!("topic-{topic}"),"activity/steps":[format!("lesson-step-{topic}")],"activity/first-step":format!("lesson-step-{topic}")}));
            forms.push(json!({"db/id":format!("example-{topic}"),"question/id":id(800+topic),"question/problem":"One plus one?","question/worked-solution":"Two."}));
            forms.push(json!({"db/id":format!("lesson-step-{topic}"),"step/id":id(810+topic),"step/content":format!("kp-{topic}")}));
            let mut task = json!({"db/id":format!("mastered-{topic}"),"learner-task/id":id(40+topic),"learner-task/activity":format!("lesson-{topic}"),"learner-task/status":kw(if migrated {"learner-task.status/completed"} else {"learner-task.status/started"}),"learner-task/xp-earned":if due {18}else{25}});
            if migrated {
                task["learner-task/finished-at"] = json!({"$instant":now-lesson_age_ms+1000});
            }
            forms.push(task);
            for q in 0..30 {
                let n = 100 + topic * 100 + q * 3;
                forms.push(json!({"db/id":format!("q-{topic}-{q}"),"question/id":id(n),"question/difficulty":kw(["question.difficulty/easy","question.difficulty/moderate","question.difficulty/hard"][q as usize%3]),"question/problem":"Enter two.","question/worked-solution":"One plus one is two.","question/answer-fields":[format!("field-{topic}-{q}")]}));
                forms.push(json!({"db/id":format!("field-{topic}-{q}"),"answer-field/id":id(n+1),"answer-field/type":kw("answer-field.type/blank"),"answer-field/key":"value","answer-field/choices":[format!("answer-{topic}-{q}")],"answer-field/correct":format!("answer-{topic}-{q}")}));
                forms.push(json!({"db/id":format!("answer-{topic}-{q}"),"answer/id":id(n+2),"answer/type":kw("answer.type/math"),"answer/value":"2","answer/feedback":"That is the correct value."}));
            }
        }
        // Retrieval scenarios live at L30+, independent of the queue boundary tests.
        for layer in 0..29 {
            let next = if layer == 28 {
                (0..5).map(|i|format!("topic-{i}")).collect::<Vec<_>>()
            } else { vec![format!("foundation-{}",layer+1)] };
            forms.push(json!({"db/id":format!("foundation-{layer}"),"topic/id":id(90_000_000+layer),"topic/next":next}));
        }
        forms.push(json!({"db/id":"foundation-progress","progress/id":"foundation",
            "progress/topic":"foundation-28","progress/policy":"policy","progress/learned":true,
            "progress/repetitions":1.0,"progress/memory":1.0,"progress/memory-at":{"$instant":now},
            "progress/interval-days":36500.0,"progress/assessment-accuracy":0.5,"progress/practice-accuracy":0.5,
            "progress/assessment-mass":0.0,"progress/practice-mass":0.0}));
        forms.push(add(json!("learner"),"learner/knowledge-profile",json!("foundation-progress")));
        f.tx(forms, if migrated { now - 2000 } else { now - lesson_age_ms })?;
        f.learner = f.snapshot()?.entities.with_attribute("learner/id")[0];
        let mastered = f.snapshot()?.refs(f.learner, "learner/activity")?;
        let completion = mastered
            .iter()
            .map(|t| {
                add(
                    json!(t),
                    "learner-task/status",
                    kw("learner-task.status/completed"),
                )
            })
            .collect();
        if !migrated {
            f.tx(completion, now - lesson_age_ms + 1000)?;
        }
        if prior_review {
            let s = f.snapshot()?;
            let mut forms = vec![];
            for topic in 0..5 {
                let scope = s
                    .entities
                    .with_attribute("topic/id")
                    .into_iter()
                    .find(|t| text(&s, *t, "topic/title") == format!("Topic {topic}"))
                    .unwrap();
                let q = s.refs(
                    s.refs(scope, "topic/knowledge-points")?[0],
                    "knowledge-point/questions",
                )?[0];
                forms.push(json!({"db/id":format!("review-{topic}"),"activity/id":id(700+topic),"activity/type":kw("activity.type/review"),"activity/title":"Prior retrieval","activity/scope":scope}));
                forms.push(json!({"db/id":format!("reviewed-{topic}"),"learner-task/id":id(710+topic),"learner-task/activity":format!("review-{topic}"),"learner-task/status":kw("learner-task.status/started"),"learner-task/xp-earned":5,"learner-task/items":[format!("observed-{topic}")]}));
                forms.push(json!({"db/id":format!("observed-{topic}"),"task-item/id":id(720+topic),"task-item/content":q,"task-item/status":kw("task-item.status/correct"),"task-item/elapsed-seconds":1.0}));
                forms.push(add(
                    json!(f.learner),
                    "learner/activity",
                    json!(format!("reviewed-{topic}")),
                ));
            }
            f.tx(forms, now - 86400000)?;
            let s = f.snapshot()?;
            let completed = s
                .refs(f.learner, "learner/activity")?
                .into_iter()
                .filter(|t| {
                    matches!(
                        status(&s, *t, "learner-task/status").as_deref(),
                        Ok("started")
                    )
                })
                .map(|t| {
                    add(
                        json!(t),
                        "learner-task/status",
                        kw("learner-task.status/completed"),
                    )
                })
                .collect();
            f.tx(completed, now - 86400000 + 1000)?;
        }
        let (forms, _) = queue_preparation(
            &f.snapshot()?,
            f.learner,
            DateTime::from_timestamp_millis(now).unwrap(),
        )?;
        f.tx(forms, now)?;
        Ok(f)
    }
    fn available(&self, kind: &str) -> Result<u64> {
        let s = self.snapshot()?;
        Ok(home(&s, self.learner)?["activities"]
            .as_array()
            .unwrap()
            .iter()
            .find(|a| a["type"] == kind)
            .ok_or("Missing scheduled activity")?["activityId"]
            .as_u64()
            .unwrap())
    }
    fn start(&mut self, kind: &str) -> Result<(u64, EntitySnapshot)> {
        let activity = self.available(kind)?;
        let s = self.act("start", json!({"activityId":activity}), self.now + 100)?;
        Ok((task_for(&s, self.learner, activity)?.unwrap(), s))
    }

    fn mark_multistep(&mut self, question: u64, at: i64) -> Result<()> {
        self.tx(vec![
            json!({"db/id":"multipart-step","step/id":{"$uuid":uid()?},"step/content":question}),
            json!({"db/id":"multipart","multistep/id":{"$uuid":uid()?},"multistep/context":"Shared assignment setup.","multistep/steps":["multipart-step"],"multistep/first-step":"multipart-step"}),
        ], at)
    }
}

#[test]
fn required_assessment_stays_visible_with_learned_topics_below_study_floor() -> Result<()> {
    let mut f = Fixture::new(false)?;
    let s = f.snapshot()?;
    let original = f.available("assessment")?;
    let learned = s.refs(f.learner, "learner/activity")?.into_iter()
        .find(|t| matches!(status(&s, *t, "learner-task/status").as_deref(), Ok("completed"))).unwrap();
    let progress = s.refs(f.learner, "learner/knowledge-profile")?.into_iter()
        .find(|p| s.reference(*p, "progress/topic").is_ok_and(|t| s.refs(t, "topic/knowledge-points").is_ok_and(|k| !k.is_empty()))).unwrap();
    let question = learning::lesson_steps(&s, original)?[0].content;
    let first_step = s.reference(original, "activity/first-step")?;
    let mut low_questions = vec![];
    for slot in 0..6 {
        let mut q = s.entity(question)?.clone();
        q.insert("db/id".into(), json!(format!("low-question-{slot}")));
        q.insert("question/id".into(), json!({"$uuid":uid()?}));
        low_questions.push(json!(q));
    }
    let mut low_progress = s.entity(progress)?.clone();
    low_progress.insert("db/id".into(), json!("low-progress"));
    low_progress.insert("progress/id".into(), json!("below-study-floor"));
    low_progress.insert("progress/topic".into(), json!("low-topic"));
    let mut forms = vec![
        json!(low_progress),
        json!({"db/id":"low-topic","topic/id":{"$uuid":uid()?},"topic/knowledge-points":["low-kp"]}),
        json!({"db/id":"low-kp","knowledge-point/id":{"$uuid":uid()?},"knowledge-point/questions":(0..6).map(|slot|format!("low-question-{slot}")).collect::<Vec<_>>()}),
        json!({"db/id":"low-lesson","activity/id":{"$uuid":uid()?},"activity/type":kw("activity.type/lesson"),"activity/scope":"low-topic"}),
        json!({"db/id":"low-task","learner-task/id":{"$uuid":uid()?},"learner-task/activity":"low-lesson","learner-task/status":kw("learner-task.status/completed"),"learner-task/finished-at":{"$instant":f.now-3*86400000},"learner-task/xp-earned":0}),
        add(json!(f.learner),"learner/activity",json!("low-task")),
        add(json!(f.learner),"learner/knowledge-profile",json!("low-progress")),
        add(json!(learned),"learner-task/xp-earned",json!(50)),
        // A quiz that includes a learned topic below the practice floor.
        add(json!(first_step),"step/content",json!("low-question-0")),
    ];
    forms.extend(low_questions);
    // A superseded offer must not revive when the topic pool expands.
    let retired = retrieval::Definition {
        kind: "assessment".into(), topic: None,
        questions: learning::lesson_steps(&s, original)?.iter().map(|step|step.content).collect(),
        title: "Retired quiz".into(), priority: 0.0, expected_seconds: 900.0,
        remediation_for: vec![], retake_of: None, existing_activity: None,
    };
    forms.extend(definition_forms(&s, &retired, "retired-quiz", None)?);
    forms.push(json!({"db/id":"retired-task","learner-task/id":{"$uuid":uid()?},"learner-task/activity":"retired-quiz","learner-task/status":kw("learner-task.status/locked"),"learner-task/priority":0.0}));
    forms.push(add(json!(f.learner),"learner/activity",json!("retired-task")));
    f.tx(forms, f.now+1)?;
    let s = f.snapshot()?;
    let at = DateTime::from_timestamp_millis(f.now+2).unwrap();
    assert_eq!(retrieval::assessment_pools(&s, f.learner, at)?.len(), 6);
    assert!(retrieval::ordinary_assessment_ready(&s, f.learner, original, at)?);
    let (forms, _) = queue_preparation(&s, f.learner, at)?;
    f.tx(forms, f.now+2)?;
    let s = f.snapshot()?;
    for self_directed in [true, false] {
        let mut view = s.clone();
        view.entities.get_mut(&f.learner).unwrap().insert("learner/self-directed".into(), json!(self_directed));
        let home = home(&view, f.learner)?;
        assert_eq!(home["assessmentStatus"]["required"], true);
        let activities = home["activities"].as_array().unwrap();
        assert_eq!(activities.len(), 1);
        assert_eq!(activities[0]["type"], "assessment");
        assert_eq!(activities[0]["activityId"], original);
    }
    // Missing the low-layer question must produce visible required practice.
    let (task, started) = f.start("assessment")?;
    for (slot, step) in learning::lesson_steps(&started, original)?.iter().enumerate() {
        let field = started.refs(step.content, "question/answer-fields")?[0];
        f.act("navigate", json!({"taskId":task,"questionId":step.content}), f.now+200+slot as i64*10)?;
        f.act("draft", json!({"taskId":task,"responses":[{"fieldId":field,"value":if slot==0 {"3"} else {"2"}}]}), f.now+201+slot as i64*10)?;
    }
    let submitted = f.act("submit", json!({"taskId":task}), f.now+300)?;
    let (forms, _) = queue_preparation(&submitted, f.learner, DateTime::from_timestamp_millis(f.now+301).unwrap())?;
    f.tx(forms, f.now+301)?;
    let after = f.snapshot()?;
    let home = home(&after, f.learner)?;
    let activities = home["activities"].as_array().unwrap();
    assert_eq!(activities.len(), 1);
    assert_eq!(activities[0]["type"], "review");
    assert_eq!(activities[0]["reason"], "Required practice after assessment");
    let review = activities[0]["activityId"].as_u64().unwrap();
    let topic = after.reference(review, "activity/scope")?;
    assert_eq!(learning::topic_layers(&after)?[&topic]+1, 1);
    Ok(())
}

#[test]
fn stale_unstarted_multipart_routes_are_replaced_without_presenting_or_grading_them() -> Result<()> {
    for kind in ["review", "assessment"] {
        let mut f = Fixture::new(kind == "review")?;
        let old = f.available(kind)?;
        let before = f.snapshot()?;
        let task = task_for(&before, f.learner, old)?.unwrap();
        let scope = before.optional_ref(old, "activity/scope")?;
        let route = learning::lesson_steps(&before, old)?;
        let part = route.last().unwrap().content;
        f.mark_multistep(part, f.now + 1)?;
        let marked = f.snapshot()?;
        assert!(!retrieval::fresh(&marked, f.learner, old)?);
        assert!(mutate(&marked, f.learner, "start", &json!({"activityId":old}), DateTime::from_timestamp_millis(f.now+2).unwrap()).is_err());
        let after = f.act("queue", json!({}), f.now + 3)?;
        assert_eq!(status(&after, task, "learner-task/status")?, "locked");
        assert!(items(&after, task)?.is_empty());
        assert_eq!(after.entity(old)?, before.entity(old)?, "the original route is immutable");
        let candidates = home(&after, f.learner)?;
        assert!(!candidates["activities"].as_array().unwrap().iter().any(|a| a["activityId"] == old));
        let replacement = candidates["activities"].as_array().unwrap().iter().filter_map(|a| a["activityId"].as_u64())
            .find(|a| retrieval::kind(&after, *a).ok().as_deref() == Some(kind)
                && after.optional_ref(*a, "activity/scope").ok() == Some(scope))
            .ok_or("No clean replacement scheduled")?;
        assert!(learning::lesson_steps(&after, replacement)?.iter().all(|st| learning::validate_practice_question(&after, st.content).is_ok()));
        for progress in before.refs(f.learner, "learner/knowledge-profile")? {
            assert_eq!(after.entity(progress)?, before.entity(progress)?);
        }
    }
    Ok(())
}

#[test]
fn assessment_rejects_new_multipart_navigation_but_preserves_saved_work_and_submission() -> Result<()> {
    let mut f = Fixture::new(false)?;
    let (task, initial) = f.start("assessment")?;
    let activity = initial.reference(task, "learner-task/activity")?;
    let route = learning::lesson_steps(&initial, activity)?;
    let first = route[0].content;
    let forbidden = route.last().unwrap().content;
    let first_item = items(&initial, task)?[0];
    f.mark_multistep(first, f.now + 110)?;
    f.mark_multistep(forbidden, f.now + 120)?;
    let before = f.snapshot()?;
    let error = mutate(&before, f.learner, "navigate", &json!({"taskId":task,"questionId":forbidden}), DateTime::from_timestamp_millis(f.now+130).unwrap()).unwrap_err();
    assert!(error.to_string().contains("multistep questions"));
    assert_eq!(items(&f.snapshot()?, task)?, vec![first_item]);
    let field = before.refs(first, "question/answer-fields")?[0];
    let drafted = f.act("draft", json!({"taskId":task,"responses":[{"fieldId":field,"value":"2"}]}), f.now+140)?;
    assert_eq!(task_json(&drafted, f.learner, task)?["step"]["fields"][0]["response"]["value"], "2");
    f.act("navigate", json!({"taskId":task,"questionId":route[1].content}), f.now+150)?;
    let revisited = f.act("navigate", json!({"taskId":task,"questionId":first}), f.now+160)?;
    assert_eq!(revisited.reference(task, "learner-task/active-item")?, first_item);
    f.act("pause", json!({"taskId":task}), f.now+170)?;
    f.act("resume", json!({"taskId":task}), f.now+180)?;
    let submitted = f.act("submit", json!({"taskId":task}), f.now+190)?;
    assert_eq!(status(&submitted, task, "learner-task/status")?, "completed");
    assert_eq!(status(&submitted, first_item, "task-item/status")?, "correct");
    assert!(!items(&submitted, task)?.iter().any(|i| submitted.optional_ref(*i, "task-item/content").ok().flatten() == Some(forbidden)));
    assert!(task_json(&submitted, f.learner, task).is_ok());
    Ok(())
}

#[test]
fn review_keeps_saved_multipart_answer_but_cannot_present_a_new_part() -> Result<()> {
    let mut f = Fixture::new(true)?;
    let (task, initial) = f.start("review")?;
    let route = learning::lesson_steps(&initial, initial.reference(task, "learner-task/activity")?)?;
    let item = items(&initial, task)?[0];
    f.mark_multistep(route[0].content, f.now+110)?;
    f.mark_multistep(route[1].content, f.now+120)?;
    let field = initial.refs(route[0].content, "question/answer-fields")?[0];
    let answered = f.act("answer", json!({"taskId":task,"itemId":item,"responses":[{"fieldId":field,"value":"2"}]}), f.now+130)?;
    assert_eq!(status(&answered, item, "task-item/status")?, "correct");
    assert!(task_json(&answered, f.learner, task).is_ok());
    let error = mutate(&answered, f.learner, "continue", &json!({"taskId":task,"itemId":item}), DateTime::from_timestamp_millis(f.now+140).unwrap()).unwrap_err();
    assert!(error.to_string().contains("multistep questions"));
    f.act("pause", json!({"taskId":task}), f.now+150)?;
    let resumed = f.act("resume", json!({"taskId":task}), f.now+160)?;
    assert_eq!(items(&resumed, task)?, vec![item]);
    assert_eq!(status(&resumed, item, "task-item/status")?, "correct");
    Ok(())
}
#[test]
fn unstarted_assessments_need_five_new_topics_but_started_routes_survive_eligibility_changes() -> Result<()> {
    let mut f=Fixture::new(false)?;
    let s=f.snapshot()?;
    let activity=f.available("assessment")?;
    let topic=s.topic_for_question(learning::lesson_steps(&s,activity)?[0].content)?;
    let progress=s.refs(f.learner,"learner/knowledge-profile")?.into_iter()
        .find(|p|s.reference(*p,"progress/topic").ok()==Some(topic)).unwrap();
    f.tx(vec![add(json!(progress),"progress/learned",json!(false))],f.now+1)?;
    let s=f.snapshot()?;
    let at=DateTime::from_timestamp_millis(f.now+2).unwrap();
    let eligibility=course_academy_engine::inventory::assessment_status(&s,f.learner,at)?;
    assert_eq!(eligibility["newEligibleTopics"],4);
    assert_eq!(eligibility["ready"],false);
    assert_eq!(eligibility["required"],false);
    assert!(mutate(&s,f.learner,"start",&json!({"activityId":activity}),at).is_err());
    f.tx(vec![add(json!(progress),"progress/learned",json!(true))],f.now+3)?;
    let s=f.act("start",json!({"activityId":activity}),f.now+4)?;
    let task=task_for(&s,f.learner,activity)?.unwrap();
    let frozen=s.refs(activity,"activity/steps")?;
    f.act("pause",json!({"taskId":task}),f.now+5)?;
    f.tx(vec![add(json!(progress),"progress/learned",json!(false))],f.now+6)?;
    let s=f.act("resume",json!({"taskId":task}),f.now+7)?;
    assert_eq!(status(&s,task,"learner-task/status")?,"started");
    assert_eq!(s.refs(activity,"activity/steps")?,frozen);
    Ok(())
}

#[test]
fn migrated_terminal_lessons_count_xp_and_original_learning_age_without_replaying_credit() -> Result<()> {
    let mut f = Fixture::with_history(false, 3 * 86400000, false, true)?;
    let s = f.snapshot()?;
    let before = s.entities.clone();
    let h = course_academy_engine::scheduling::lifecycle(&s, f.learner)?;
    assert_eq!(h.xp, 125.0);
    assert_eq!(h.mastered.len(), 5);
    assert!(h.mastered.values().all(|date| date.timestamp_millis() == f.now - 3*86400000 + 1000));
    assert!(!s.status_history.iter().any(|event| s.ident(&event.value).ok().as_deref() == Some("learner-task.status/started")));
    let eligibility = course_academy_engine::inventory::assessment_status(&s,f.learner,DateTime::from_timestamp_millis(f.now).unwrap())?;
    assert_eq!(eligibility["practiceXp"],125.0);
    assert_eq!(eligibility["eligibleTopics"],5);
    assert_eq!(eligibility["ready"],true);
    assert_eq!(eligibility["required"],false);
    let activity = f.available("assessment")?;
    assert_eq!(s.entities, before, "lifecycle reads must not replay progress or XP writes");
    let task = task_for(&s, f.learner, activity)?.unwrap();
    let s = f.act("start",json!({"activityId":activity}),f.now+100)?;
    assert_eq!(status(&s, task, "learner-task/status")?,"started");
    let again = course_academy_engine::scheduling::lifecycle(&s,f.learner)?;
    assert_eq!(again.xp,125.0);
    Ok(())
}

#[test]
fn zero_progress_lesson_pause_preserves_time_without_pinning_the_queue() -> Result<()> {
    let mut f = Fixture::new(false)?;
    let s = f.snapshot()?;
    let old = s.refs(f.learner, "learner/activity")?.into_iter().find(|task| {
        status(&s, *task, "learner-task/status").ok().as_deref() == Some("completed")
            && retrieval::kind(&s, s.reference(*task, "learner-task/activity").unwrap()).ok().as_deref() == Some("lesson")
    }).unwrap();
    let activity = s.reference(old, "learner-task/activity")?;
    let topic = s.reference(activity, "activity/scope")?;
    f.tx(vec![json!([kw("db/retract"), f.learner, kw("learner/activity"), old])], f.now + 100)?;
    let s = f.act("study-topic", json!({"topicId":topic}), f.now + 200)?;
    let task = task_for(&s, f.learner, activity)?.unwrap();
    let item = items(&s, task)?[0];
    let s = f.act("pause", json!({"taskId":task}), f.now + 5200)?;
    assert_eq!(status(&s, task, "learner-task/status")?, "locked");
    assert_eq!(status(&s, item, "task-item/status")?, "paused");
    assert_eq!(number(&s, task, "learner-task/elapsed-seconds"), 5.0);
    assert_eq!(number(&s, item, "task-item/elapsed-seconds"), 5.0);
    assert!(mutate(&s, f.learner, "pause", &json!({"taskId":task}), DateTime::from_timestamp_millis(f.now + 6000).unwrap())?.0.is_empty());
    assert!(!learning::study_candidates(&s, f.learner, course(&s,f.learner)?, DateTime::from_timestamp_millis(f.now+6000).unwrap())?.iter().any(|p| p.activity == activity), "an accidental open must not bypass ordinary selection");

    // Existing zero-progress paused tasks are normalized by queue preparation.
    f.tx(vec![add(json!(task), "learner-task/status", kw("learner-task.status/paused"))], f.now + 7000)?;
    let s = f.snapshot()?;
    let (forms, _) = queue_preparation(&s, f.learner, DateTime::from_timestamp_millis(f.now+8000).unwrap())?;
    f.tx(forms, f.now+8000)?;
    let s = f.snapshot()?;
    assert_eq!(status(&s, task, "learner-task/status")?, "locked");
    assert_eq!(number(&s, task, "learner-task/elapsed-seconds"), 5.0);
    assert!(reset_unstarted_lessons(&s, f.learner)?.is_empty());

    let s = f.act("study-topic", json!({"topicId":topic}), f.now + 12000)?;
    assert_eq!(task_for(&s, f.learner, activity)?, Some(task));
    assert_eq!(items(&s, task)?, vec![item]);
    assert_eq!(number(&s, item, "task-item/elapsed-seconds"), 5.0);
    let s = f.act("pause", json!({"taskId":task}), f.now + 15000)?;
    assert_eq!(number(&s, task, "learner-task/elapsed-seconds"), 8.0);
    let s = f.act("resume", json!({"taskId":task}), f.now + 20000)?;
    assert_eq!(status(&s, task, "learner-task/status")?, "started");
    assert_eq!(items(&s, task)?, vec![item]);
    let s = f.act("continue", json!({"taskId":task,"itemId":item}), f.now + 21000)?;
    assert!(!learning::lesson_has_no_progress(&s, task)?);
    let s = f.act("pause", json!({"taskId":task}), f.now + 22000)?;
    assert_eq!(status(&s, task, "learner-task/status")?, "paused", "advancing a lesson must retain resumable progress");
    Ok(())
}

#[test]
fn successful_lesson_completion_atomically_clears_its_queue_membership() -> Result<()> {
    let mut f = Fixture::new(false)?;
    let s = f.snapshot()?;
    let old = s.refs(f.learner, "learner/activity")?[0];
    let activity = s.reference(old, "learner-task/activity")?;
    let topic = s.reference(activity, "activity/scope")?;
    let other = s.refs(f.learner, "learner/knowledge-profile")?.into_iter()
        .map(|p| s.reference(p, "progress/topic").unwrap()).find(|p| *p != topic).unwrap();
    f.tx(vec![
        json!([kw("db/retract"), f.learner, kw("learner/activity"), old]),
        add(json!(f.learner), "learner/queue", json!(topic)),
        add(json!(f.learner), "learner/queue", json!(other)),
        add(json!(f.learner), "learner/targets", json!(topic)),
    ], f.now + 100)?;
    let mut s = f.act("study-topic", json!({"topicId":topic}), f.now + 200)?;
    let task = task_for(&s, f.learner, activity)?.unwrap();
    for turn in 0..12 {
        if status(&s, task, "learner-task/status")? == "completed" { break; }
        assert!(s.refs(f.learner, "learner/queue")?.contains(&topic));
        let step = task_json(&s, f.learner, task)?["step"].clone();
        let item = step["itemId"].as_u64().unwrap();
        let at = f.now + 1000 + turn * 1000;
        if step["kind"] == "question" && step["status"] == "started" {
            let field = step["fields"][0]["id"].as_u64().unwrap();
            s = f.act("answer", json!({"taskId":task,"itemId":item,"responses":[{"fieldId":field,"value":"2"}]}), at)?;
        } else {
            s = f.act("continue", json!({"taskId":task,"itemId":item}), at)?;
        }
    }
    assert_eq!(status(&s, task, "learner-task/status")?, "completed");
    assert_eq!(s.refs(f.learner, "learner/queue")?, vec![other]);
    assert_eq!(s.refs(f.learner, "learner/targets")?, vec![topic]);
    assert_eq!(task_json(&s, f.learner, task)?["learner"]["queue"], json!([other]));
    let item = *items(&s, task)?.last().unwrap();
    assert!(mutate(&s, f.learner, "continue", &json!({"taskId":task,"itemId":item}), DateTime::from_timestamp_millis(f.now + 20000).unwrap())?.0.is_empty());
    Ok(())
}

#[test]
fn unstarted_lesson_can_reopen_its_already_presented_first_question() -> Result<()> {
    let mut f = Fixture::new(false)?;
    let s = f.snapshot()?;
    let old = s.refs(f.learner, "learner/activity")?[0];
    let activity = s.reference(old, "learner-task/activity")?;
    let topic = s.reference(activity, "activity/scope")?;
    let step = s.reference(activity, "activity/first-step")?;
    let kp = s.refs(topic, "topic/knowledge-points")?[0];
    let unavailable = learning::unavailable_questions(&s, f.learner)?;
    let question = s.refs(s.refs(topic, "topic/knowledge-points")?[0], "knowledge-point/questions")?
        .into_iter().find(|q| !unavailable.contains(q)).unwrap();
    f.tx(vec![
        json!([kw("db/retract"), f.learner, kw("learner/activity"), old]),
        add(json!(step), "step/content", json!(question)),
        add(json!(step), "step/next", json!("practice-step")),
        json!({"db/id":"practice-step","step/id":{"$uuid":uuid(99001)},"step/content":kp}),
        add(json!(activity), "activity/steps", json!("practice-step")),
        json!({"db/id":"fixed-lesson-task","learner-task/id":{"$uuid":uuid(99002)},
            "learner-task/activity":activity,"learner-task/status":kw("learner-task.status/locked"),
            "learner-task/xp-base":10,"learner-task/elapsed-seconds":0.0}),
        add(json!(f.learner), "learner/activity", json!("fixed-lesson-task")),
    ], f.now + 100)?;
    let s = f.act("study-topic", json!({"topicId":topic}), f.now + 200)
        .map_err(|error| format!("initial question start: {error}"))?;
    let task = task_for(&s, f.learner, activity)?.unwrap();
    let item = items(&s, task)?[0];
    let s = f.act("pause", json!({"taskId":task}), f.now + 1200)?;
    assert_eq!(status(&s, task, "learner-task/status")?, "locked");
    assert!(learning::unavailable_questions(&s, f.learner)?.contains(&question));
    let s = f.act("study-topic", json!({"topicId":topic}), f.now + 5000)
        .map_err(|error| format!("saved question restart: {error}"))?;
    assert_eq!(items(&s, task)?, vec![item]);
    assert_eq!(s.reference(item, "task-item/content")?, question);
    assert_eq!(number(&s, item, "task-item/elapsed-seconds"), 1.0);
    let field = s.refs(question, "question/answer-fields")?[0];
    let s = f.act("answer", json!({"taskId":task,"itemId":item,"responses":[{"fieldId":field,"value":"2"}]}), f.now + 6000)?;
    assert!(!learning::lesson_has_no_progress(&s, task)?);
    let s = f.act("pause", json!({"taskId":task}), f.now + 7000)?;
    assert_eq!(status(&s, task, "learner-task/status")?, "paused");
    Ok(())
}

#[test]
fn assessment_weights_validate_all_six_fields_and_update_from_database_snapshots() -> Result<()> {
    use course_academy_engine::question_selection::{Phase, active_policy, weights_for_phase};
    let mut f = Fixture::new(false)?;
    let before = f.snapshot()?;
    let policy = active_policy(&before)?;
    let child = before.refs(policy, "policy/question-selection-weights")?[0];
    assert_eq!(
        weights_for_phase(&before, policy, "assessment", Phase::Initial)?,
        Some([50.0, 40.0, 10.0])
    );
    assert_eq!(
        weights_for_phase(&before, policy, "assessment", Phase::Remedial)?,
        Some([45.0, 40.0, 15.0])
    );
    let activity = f.available("assessment")?;
    let reserved_steps = before.refs(activity, "activity/steps")?;
    assert!(
        f.tx(
            vec![
                json!([
                    kw("db/retract"),
                    child,
                    kw("question-weights/remedial-hard")
                ]),
                json!([kw("db/ensure"), child, kw("question-weights/validate")]),
            ],
            f.now + 1
        )
        .is_err()
    );
    f.tx(vec![json!({"db/id":child,
        "question-weights/initial-easy":0.0,"question-weights/initial-moderate":0.0,"question-weights/initial-hard":100.0,
        "question-weights/remedial-easy":100.0,"question-weights/remedial-moderate":0.0,"question-weights/remedial-hard":0.0,
        "db/ensure":kw("question-weights/validate")
    })], f.now + 2)?;
    let after = f.snapshot()?;
    assert_eq!(
        weights_for_phase(&after, policy, "assessment", Phase::Initial)?,
        Some([0.0, 0.0, 100.0])
    );
    assert_eq!(
        weights_for_phase(&after, policy, "assessment", Phase::Remedial)?,
        Some([100.0, 0.0, 0.0])
    );
    assert_eq!(
        weights_for_phase(&before, policy, "assessment", Phase::Initial)?,
        Some([50.0, 40.0, 10.0])
    );
    assert_eq!(after.refs(activity, "activity/steps")?, reserved_steps);
    let original = task_for(&after, f.learner, activity)?.unwrap();
    let original_questions: BTreeSet<_> = learning::lesson_steps(&after, activity)?
        .iter()
        .map(|step| step.content)
        .collect();
    let questions = course_academy_engine::assessment_sampling::retake(
        &after,
        f.learner,
        original,
        &learning::unavailable_questions(&after, f.learner)?,
        [100.0, 0.0, 0.0],
        "zero-weight-minimums",
    )?;
    assert_eq!(questions.len(), original_questions.len());
    assert!(questions.iter().all(|q| !original_questions.contains(q)));
    assert_eq!(
        questions
            .iter()
            .map(
                |q| course_academy_engine::assessment_sampling::band(&after, *q)
                    .unwrap()
                    .unwrap()
            )
            .collect::<BTreeSet<_>>(),
        BTreeSet::from([0, 1, 2])
    );
    Ok(())
}

#[test]
fn submitted_answer_clock_ends_before_grading_and_database_admission_finish() -> Result<()> {
    let mut f=Fixture::new(true)?;
    let (task,s)=f.start("review")?;
    let item=*items(&s,task)?.last().unwrap();
    let started=timing::status_at(&s,item,"task-item/status")?.timestamp_millis();
    let question=s.reference(item,"task-item/content")?;
    let field=s.refs(question,"question/answer-fields")?[0];
    let submitted=started+1000;
    let processed=started+30000;
    let after=f.act("answer",json!({"taskId":task,"itemId":item,"submittedAt":submitted,"responses":[{"fieldId":field,"value":"2"}]}),processed)?;
    assert_eq!(number(&after,item,"task-item/elapsed-seconds"),1.);
    assert_eq!(timing::elapsed(&after,item,DateTime::from_timestamp_millis(processed+1000).unwrap())?,1.);
    assert_eq!(timing::task_elapsed(&after,task,DateTime::from_timestamp_millis(processed+1000).unwrap())?,1.);
    assert_eq!(timing::status_at(&after,item,"task-item/status")?.timestamp_millis(),processed);
    assert_eq!(after.entity(item)?["task-item/working-ended-at"],json!({"$instant":submitted}));
    assert_eq!(status(&after,item,"task-item/status")?,"correct");
    Ok(())
}

#[test]
fn automatic_generic_reviews_commit_reservations_grade_streak_award_xp_and_update_fire_once()
-> Result<()> {
    let mut f = Fixture::new(true)?;
    let (task, mut s) = f.start("review")?;
    for slot in 0..3 {
        let item = *items(&s, task)?.last().unwrap();
        let q = s.reference(item, "task-item/content")?;
        let field = s.refs(q, "question/answer-fields")?[0];
        s = f.act(
            "answer",
            json!({"taskId":task,"itemId":item,"responses":[{"fieldId":field,"value":"2"}]}),
            f.now + 200 + slot * 200,
        )?;
        assert_eq!(task_json(&s, f.learner, task)?["step"]["status"], "correct");
        let (duplicate, _) = mutate(
            &s,
            f.learner,
            "answer",
            &json!({"taskId":task,"itemId":item,"responses":[{"fieldId":field,"value":"2"}]}),
            DateTime::from_timestamp_millis(f.now + 200 + slot * 200).unwrap(),
        )?;
        assert!(duplicate.is_empty());
        s = f.act(
            "continue",
            json!({"taskId":task,"itemId":item}),
            f.now + 300 + slot * 200,
        )?;
    }
    assert_eq!(status(&s, task, "learner-task/status")?, "completed");
    assert_eq!(items(&s, task)?.len(), 3);
    assert_eq!(number(&s, task, "learner-task/xp-earned"), 7.0);
    let scope = s.reference(
        s.reference(task, "learner-task/activity")?,
        "activity/scope",
    )?;
    let p = s
        .refs(f.learner, "learner/knowledge-profile")?
        .into_iter()
        .find(|p| s.reference(*p, "progress/topic").ok() == Some(scope))
        .unwrap();
    assert!(number(&s, p, "progress/repetitions") > 2.0);
    assert_eq!(number(&s, p, "progress/practice-mass"), 3.0);
    assert_eq!(number(&s, p, "progress/assessment-mass"), 0.0);
    Ok(())
}
#[test]
fn failed_review_refresh_persists_and_delays_prepared_and_new_reviews_until_due() -> Result<()> {
    let mut f = Fixture::new(true)?;
    let (task, mut s) = f.start("review")?;
    let activity = s.reference(task, "learner-task/activity")?;
    let topic = s.reference(activity, "activity/scope")?;
    let progress = s
        .refs(f.learner, "learner/knowledge-profile")?
        .into_iter()
        .find(|p| s.reference(*p, "progress/topic").ok() == Some(topic))
        .unwrap();
    let before = s.entity(progress)?.clone();
    let mut at = f.now + 200;
    for _ in 0..5 {
        let item = *items(&s, task)?.last().unwrap();
        let q = s.reference(item, "task-item/content")?;
        let field = s.refs(q, "question/answer-fields")?[0];
        s = f.act(
            "answer",
            json!({"taskId":task,"itemId":item,"responses":[{"fieldId":field,"value":"3"}]}),
            at,
        )?;
        at += 100;
        s = f.act("continue", json!({"taskId":task,"itemId":item}), at)?;
        at += 100;
    }
    assert_eq!(status(&s, task, "learner-task/status")?, "failed");
    assert!(
        number(&s, progress, "progress/repetitions")
            < before["progress/repetitions"].as_f64().unwrap()
    );
    assert!(number(&s, progress, "progress/memory") > 0.5);
    assert_eq!(number(&s, progress, "progress/practice-mass"), 5.0);
    assert!(
        course_academy_engine::scheduling::lifecycle(&s, f.learner)?
            .repairs
            .is_empty()
    );
    let anchor = schema::instant_days(&s.entities[&progress]["progress/memory-at"])?;
    let due = anchor
        + number(&s, progress, "progress/interval-days")
            * (number(&s, progress, "progress/memory").log2() - 0.5_f64.log2());
    let due_ms = (due * 86_400_000.0).ceil() as i64;
    assert!(due_ms > at + 60_000);

    // Reopening the database projection preserves the refreshed memory. A
    // previously prepared fresh task for the same topic must also stay hidden.
    s = f.snapshot()?;
    let steps: Vec<_> = (0..5).map(|i| format!("pending-step-{i}")).collect();
    let mut forms = vec![
        json!({"db/id":"pending-review","activity/id":{"$uuid":uuid(99011)},"activity/type":kw("activity.type/review"),"activity/scope":topic,"activity/title":"Previously prepared review","activity/steps":steps,"activity/first-step":"pending-step-0"}),
        json!({"db/id":"pending-review-task","learner-task/id":{"$uuid":uuid(99012)},"learner-task/activity":"pending-review","learner-task/status":kw("learner-task.status/unlocked"),"learner-task/priority":6000.0}),
        add(
            json!(f.learner),
            "learner/activity",
            json!("pending-review-task"),
        ),
    ];
    let pool = s.refs(
        s.refs(topic, "topic/knowledge-points")?[0],
        "knowledge-point/questions",
    )?;
    let seen = learning::unavailable_questions(&s, f.learner)?;
    let pool: Vec<_> = pool
        .into_iter()
        .filter(|q| !seen.contains(q))
        .take(5)
        .collect();
    assert_eq!(pool.len(), 5);
    for (i, question) in pool.iter().enumerate() {
        let mut step = json!({"db/id":steps[i],"step/id":{"$uuid":uuid(99100+i as u128)},"step/content":question});
        if i < 4 {
            step["step/next"] = json!(steps[i + 1]);
        }
        forms.push(step);
    }
    f.tx(forms, at)?;
    s = f.snapshot()?;
    let pending = s
        .refs(f.learner, "learner/activity")?
        .into_iter()
        .find(|t| {
            s.reference(*t, "learner-task/activity")
                .ok()
                .is_some_and(|a| text(&s, a, "activity/title") == "Previously prepared review")
        })
        .unwrap();
    let pending_activity = s.reference(pending, "learner-task/activity")?;
    let course_id = course(&s, f.learner)?;
    let candidates = |s: &EntitySnapshot, at: i64| {
        retrieval::candidates(
            s,
            f.learner,
            course_id,
            DateTime::from_timestamp_millis(at).unwrap(),
            true,
        )
    };
    assert!(!candidates(&s, at)?.iter().any(|p| p.topic == topic));
    assert!(
        !retrieval::schedule(
            &s,
            f.learner,
            course(&s, f.learner)?,
            DateTime::from_timestamp_millis(at).unwrap()
        )?
        .iter()
        .any(|d| d.topic == Some(topic))
    );
    assert!(
        !candidates(&s, due_ms - 1000)?
            .iter()
            .any(|p| p.topic == topic)
    );
    assert!(
        candidates(&s, due_ms + 1000)?
            .iter()
            .any(|p| p.activity == pending_activity)
    );
    let mut without_pending = s.clone();
    without_pending
        .entities
        .get_mut(&f.learner)
        .unwrap()
        .insert(
            "learner/activity".into(),
            json!(
                s.refs(f.learner, "learner/activity")?
                    .into_iter()
                    .filter(|t| *t != pending)
                    .collect::<Vec<_>>()
            ),
        );
    assert!(
        retrieval::schedule(
            &without_pending,
            f.learner,
            course_id,
            DateTime::from_timestamp_millis(due_ms + 1000).unwrap()
        )?
        .iter()
        .any(|d| d.topic == Some(topic))
    );
    Ok(())
}
#[test]
fn assessments_remain_available_and_startable_after_course_and_study_mode_switches() -> Result<()> {
    let mut f = Fixture::new(false)?;
    let activity = f.available("assessment")?;
    let before = f.snapshot()?;
    assert!(before.optional_ref(activity, "activity/course")?.is_none());
    let original_steps = learning::lesson_steps(&before, activity)?;
    f.tx(vec![
        // Legacy prepared assessments can still carry an old course link.
        add(json!(activity), "activity/course", json!(course(&before, f.learner)?)),
        json!({"db/id":"unrelated-course","course/id":{"$uuid":uuid(9000)},"course/title":"Unrelated course","course/units":[]}),
        add(json!(f.learner), "learner/course", json!("unrelated-course")),
        add(json!(f.learner), "learner/self-directed", json!(true)),
    ], f.now + 100)?;
    let switched = f.snapshot()?;
    let (forms, _) = queue_preparation(
        &switched,
        f.learner,
        DateTime::from_timestamp_millis(f.now + 200).unwrap(),
    )?;
    assert!(
        !forms
            .iter()
            .any(|form| form.get("activity/type") == Some(&kw("activity.type/assessment")))
    );
    f.tx(forms, f.now + 200)?;
    assert_eq!(f.available("assessment")?, activity);
    f.now += 300;
    let (task, s) = f.start("assessment")?;
    assert_eq!(status(&s, task, "learner-task/status")?, "started");
    assert_eq!(
        learning::lesson_steps(&s, activity)?
            .iter()
            .map(|step| step.content)
            .collect::<Vec<_>>(),
        original_steps
            .iter()
            .map(|step| step.content)
            .collect::<Vec<_>>()
    );
    Ok(())
}

#[test]
fn assessment_drafts_navigation_batch_submission_and_remediation_are_atomic() -> Result<()> {
    let mut f = Fixture::new(false)?;
    let (task, mut s) = f.start("assessment")?;
    let activity = s.reference(task, "learner-task/activity")?;
    let questions: Vec<_> = learning::lesson_steps(&s, activity)?
        .iter()
        .map(|st| st.content)
        .collect();
    let first_item = items(&s, task)?[0];
    let field = s.refs(questions[0], "question/answer-fields")?[0];
    s = f.act(
        "draft",
        json!({"taskId":task,"responses":[{"fieldId":field,"value":"3"}]}),
        f.now + 200,
    )?;
    assert!(retrieval::outcomes(&s, &[first_item])?.is_empty());
    let view = task_json(&s, f.learner, task)?;
    assert!(view["step"]["fields"][0].get("correctAnswer").is_none());
    assert_eq!(view["step"]["fields"][0]["response"]["value"], "3");
    assert_eq!(
        s.refs(f.learner, "learner/knowledge-profile")?
            .iter()
            .map(|p| number(&s, *p, "progress/assessment-mass"))
            .sum::<f64>(),
        0.0
    );
    // Visit out of order, preserve and revise a previously drafted answer.
    s = f.act(
        "navigate",
        json!({"taskId":task,"questionId":questions[2]}),
        f.now + 300,
    )?;
    assert_eq!(
        s.reference(
            s.reference(task, "learner-task/active-item")?,
            "task-item/content"
        )?,
        questions[2]
    );
    s = f.act(
        "navigate",
        json!({"taskId":task,"questionId":questions[0]}),
        f.now + 400,
    )?;
    s = f.act(
        "draft",
        json!({"taskId":task,"responses":[{"fieldId":field,"value":"2"}]}),
        f.now + 500,
    )?;
    for (slot, &q) in questions.iter().enumerate().skip(1) {
        s = f.act(
            "navigate",
            json!({"taskId":task,"questionId":q}),
            f.now + 600 + slot as i64 * 200,
        )?;
        let field = s.refs(q, "question/answer-fields")?[0];
        s=f.act("draft",json!({"taskId":task,"responses":[{"fieldId":field,"value":if slot==1 {"3"}else{"2"}}]}),f.now+700+slot as i64*200)?;
    }
    assert!(
        mutate(
            &s,
            f.learner,
            "skip",
            &json!({"taskId":task}),
            DateTime::from_timestamp_millis(f.now + 1900).unwrap()
        )
        .is_err()
    );
    s = f.act("submit", json!({"taskId":task}), f.now + 2000)?;
    assert_eq!(status(&s, task, "learner-task/status")?, "completed");
    assert_eq!(status(&s, first_item, "task-item/status")?, "correct");
    assert_eq!(
        s.refs(f.learner, "learner/knowledge-profile")?
            .iter()
            .map(|p| number(&s, *p, "progress/assessment-mass"))
            .sum::<f64>(),
        5.0
    );
    assert!(
        mutate(
            &s,
            f.learner,
            "submit",
            &json!({"taskId":task}),
            DateTime::from_timestamp_millis(f.now + 2001).unwrap()
        )?
        .0
        .is_empty()
    );
    let repairs = course_academy_engine::scheduling::lifecycle(&s, f.learner)?.repairs;
    assert_eq!(repairs.len(), 1);
    let (forms, _) = queue_preparation(
        &s,
        f.learner,
        DateTime::from_timestamp_millis(f.now + 2100).unwrap(),
    )?;
    f.tx(forms, f.now + 2100)?;
    let home = home(&f.snapshot()?, f.learner)?;
    assert!(
        home["activities"]
            .as_array()
            .unwrap()
            .iter()
            .all(|a| a["type"] == "review")
    );
    Ok(())
}
#[test]
fn completed_assessment_reveals_feedback_for_empty_and_never_opened_questions() -> Result<()> {
    let mut f = Fixture::new(false)?;
    let (task, s) = f.start("assessment")?;
    let activity = s.reference(task, "learner-task/activity")?;
    let questions: Vec<_> = learning::lesson_steps(&s, activity)?.iter().map(|step| step.content).collect();
    let first = s.refs(questions[0], "question/answer-fields")?[0];
    f.act("draft", json!({"taskId":task,"responses":[{"fieldId":first,"value":"2"}]}), f.now + 200)?;
    let s = f.act("navigate", json!({"taskId":task,"questionId":questions[1]}), f.now + 300)?;
    let second = s.refs(questions[1], "question/answer-fields")?[0];
    f.act("draft", json!({"taskId":task,"responses":[{"fieldId":second,"value":"3"}]}), f.now + 400)?;
    let s = f.act("navigate", json!({"taskId":task,"questionId":questions[2]}), f.now + 500)?;
    let active = task_json(&s, f.learner, task)?;
    for step in active["history"].as_array().unwrap().iter().map(|entry| &entry["step"])
        .chain(std::iter::once(&active["step"])) {
        assert!(step.get("solution").is_none());
        assert!(step["fields"].as_array().unwrap().iter().all(|field| field.get("correctAnswer").is_none()));
    }
    let finished = f.act("submit", json!({"taskId":task,"responses":[]}), f.now + 600)?;
    let recorded = finished.entities.clone();
    let view = task_json(&finished, f.learner, task)?;
    let mut feedback: Vec<_> = view["history"].as_array().unwrap().iter()
        .map(|entry| entry["step"].clone()).chain(std::iter::once(view["step"].clone())).collect();
    feedback.sort_by_key(|step| questions.iter().position(|&q| step["contentId"] == q).unwrap());
    assert_eq!(feedback.len(), questions.len());
    assert_eq!(feedback[0]["status"], "correct");
    assert_eq!(feedback[1]["status"], "incorrect");
    assert_eq!(feedback[0]["fields"][0]["response"]["value"], "2");
    assert_eq!(feedback[1]["fields"][0]["response"]["value"], "3");
    for (index, step) in feedback.iter().enumerate() {
        assert_eq!(step["contentId"], questions[index]);
        assert_eq!(step["solution"], "One plus one is two.");
        assert_eq!(step["fields"][0]["correctAnswer"]["value"], "2");
        assert_eq!(step["unanswered"], index >= 2);
        if index >= 2 { assert_eq!(step["status"], "incorrect"); }
        if index >= 3 {
            assert!(step["itemId"].is_null());
            assert_eq!(step["reviewKey"], format!("assessment-question-{}", questions[index]));
        }
    }
    assert_eq!(view["assessmentScore"], json!({"correct":1,"total":questions.len(),"unanswered":questions.len()-2}));
    assert_eq!(items(&finished, task)?.len(), 3);
    let last = *items(&finished, task)?.last().unwrap();
    assert_eq!(status(&finished, last, "task-item/status")?, "paused");
    assert_eq!(finished.entities, recorded, "reviewing must not fabricate presentation or grading facts");
    if let Ok(path) = std::env::var("COURSE_ACADEMY_ASSESSMENT_FEEDBACK_FIXTURE") {
        std::fs::write(path, serde_json::to_vec_pretty(&json!({"active":active,"completed":view}))?)?;
    }
    Ok(())
}

#[test]
fn paused_assessment_expires_at_original_deadline_without_fabricating_unanswered_evidence()
-> Result<()> {
    let mut f = Fixture::new(false)?;
    let (task, s) = f.start("assessment")?;
    let item = *items(&s, task)?.last().unwrap();
    let s = f.act("pause", json!({"taskId":task}), f.now + 1000)?;
    assert!(
        retrieval::remaining(
            &s,
            task,
            DateTime::from_timestamp_millis(f.now + 899000).unwrap()
        )?
        .unwrap()
            > 0.0
    );
    assert!(
        mutate(
            &s,
            f.learner,
            "expire",
            &json!({"taskId":task}),
            DateTime::from_timestamp_millis(f.now + 899000).unwrap()
        )
        .is_err()
    );
    let deadline = f.now + 900100;
    assert_eq!(
        envelope(
            mutate(
                &s,
                f.learner,
                "resume",
                &json!({"taskId":task}),
                DateTime::from_timestamp_millis(deadline).unwrap()
            )
            .map(|_| json!({}))
        )["code"],
        "assessment-expired"
    );
    let before = s
        .refs(f.learner, "learner/knowledge-profile")?
        .iter()
        .map(|p| s.entities[p].clone())
        .collect::<Vec<_>>();
    let s = f.act("expire", json!({"taskId":task}), deadline)?;
    assert_eq!(status(&s, task, "learner-task/status")?, "completed");
    assert_eq!(status(&s, item, "task-item/status")?, "paused");
    assert_eq!(items(&s, task)?.len(), 1);
    let expired_view = task_json(&s, f.learner, task)?;
    let all_feedback: Vec<_> = expired_view["history"].as_array().unwrap().iter()
        .map(|entry| &entry["step"]).chain(std::iter::once(&expired_view["step"])).collect();
    assert_eq!(all_feedback.len(), learning::lesson_steps(&s, s.reference(task, "learner-task/activity")?)?.len());
    assert!(all_feedback.iter().all(|step| step["status"] == "incorrect" && step["unanswered"] == true
        && step["fields"][0].get("correctAnswer").is_some() && step.get("solution").is_some()));
    assert_eq!(number(&s, task, "learner-task/xp-earned"), -1.0);
    assert_eq!(
        before,
        s.refs(f.learner, "learner/knowledge-profile")?
            .iter()
            .map(|p| s.entities[p].clone())
            .collect::<Vec<_>>()
    );
    assert!(
        mutate(
            &s,
            f.learner,
            "expire",
            &json!({"taskId":task}),
            DateTime::from_timestamp_millis(deadline + 1).unwrap()
        )?
        .0
        .is_empty()
    );
    Ok(())
}

#[test]
fn study_now_and_lesson_resume_bypass_required_queue_work_without_changing_it() -> Result<()> {
    for remediation in [false, true] {
        for self_directed in [false, true] {
            let mut f = Fixture::new(false)?;
            let mut at = f.now + 300;
            if remediation {
                let (assessment, _) = f.start("assessment")?;
                let s = f.act("submit", json!({"taskId":assessment}), f.now + 200)?;
                let (forms, _) = queue_preparation(
                    &s,
                    f.learner,
                    DateTime::from_timestamp_millis(at).unwrap(),
                )?;
                f.tx(forms, at)?;
            }

            let s = f.snapshot()?;
            let queued_topic = s.entities.with_attribute("topic/id").into_iter()
                .find(|t| text(&s,*t,"topic/title") == "Topic 0").unwrap();
            let kp = s.refs(queued_topic, "topic/knowledge-points")?[0];
            let question = s.refs(kp, "knowledge-point/questions")?[0];
            let fields = s.refs(question, "question/answer-fields")?;
            let mut forms = vec![
                json!({"db/id":"manual-topic","topic/id":{"$uuid":uuid(90000)},"topic/title":"Explicit study outside the course","topic/knowledge-points":["manual-kp"]}),
                json!({"db/id":"manual-kp","knowledge-point/id":{"$uuid":uuid(90001)},"knowledge-point/canonical-example":"manual-example","knowledge-point/questions":(0..6).map(|n|format!("manual-question-{n}")).collect::<Vec<_>>()}),
                json!({"db/id":"manual-example","question/id":{"$uuid":uuid(90002)},"question/problem":"One plus one?","question/worked-solution":"Two."}),
                json!({"db/id":"manual-step","step/id":{"$uuid":uuid(90003)},"step/content":"manual-kp"}),
                json!({"db/id":"manual-lesson","activity/id":{"$uuid":uuid(90004)},"activity/title":"Explicit study","activity/type":kw("activity.type/lesson"),"activity/scope":"manual-topic","activity/steps":["manual-step"],"activity/first-step":"manual-step"}),
                add(json!(f.learner), "learner/self-directed", json!(self_directed)),
                add(json!(f.learner), "learner/queue", json!(queued_topic)),
            ];
            for n in 0..6 {
                forms.push(json!({"db/id":format!("manual-question-{n}"),"question/id":{"$uuid":uuid(90100+n)},"question/problem":"Enter two.","question/worked-solution":"Two.","question/difficulty":kw("question.difficulty/easy"),"question/answer-fields":fields}));
            }
            // Exercise both a prepared locked attempt and a new lesson attempt.
            if self_directed {
                forms.push(json!({"db/id":"manual-task","learner-task/id":{"$uuid":uuid(90005)},"learner-task/activity":"manual-lesson","learner-task/status":kw("learner-task.status/locked"),"learner-task/priority":1.0}));
                forms.push(add(json!(f.learner), "learner/activity", json!("manual-task")));
            }
            at += 100;
            f.tx(forms, at)?;
            let before = f.snapshot()?;
            let topic = before.entities.with_attribute("topic/id").into_iter()
                .find(|t| text(&before, *t, "topic/title") == "Explicit study outside the course")
                .unwrap();
            let activity = topic_lesson(&before, topic)?;
            let required = learning::study_candidates(
                &before, f.learner, course(&before, f.learner)?,
                DateTime::from_timestamp_millis(at).unwrap(),
            )?;
            assert!(!required.is_empty());
            assert!(required.iter().all(|p| p.priority >= 11000.0));
            assert!(required.iter().all(|p| retrieval::kind(&before, p.activity).unwrap()
                == if remediation { "review" } else { "assessment" }));
            assert!(mutate(
                &before, f.learner, "start", &json!({"activityId":activity}),
                DateTime::from_timestamp_millis(at + 1).unwrap(),
            ).unwrap_err().to_string().contains("required activity"));

            at += 100;
            let mut s = f.act("study-topic", json!({"topicId":topic}), at)?;
            let task = task_for(&s, f.learner, activity)?.unwrap();
            if self_directed {
                assert_eq!(Some(task), task_for(&before, f.learner, activity)?);
            } else {
                assert!(task_for(&before, f.learner, activity)?.is_none());
            }
            assert_eq!(status(&s, task, "learner-task/status")?, "started");
            let first_items = items(&s, task)?;

            // Pausing before doing work returns the attempt to an unstarted
            // state. Resume must still honor the learner's explicit selection.
            at += 100;
            s = f.act("pause", json!({"taskId":task}), at)?;
            assert_eq!(status(&s, task, "learner-task/status")?, "locked");
            at += 100;
            s = f.act("resume", json!({"taskId":task}), at)?;
            assert_eq!(status(&s, task, "learner-task/status")?, "started");
            assert_eq!(items(&s, task)?, first_items);

            at += 100;
            s = f.act("continue", json!({"taskId":task,"itemId":first_items[0]}), at)?;
            let item = *items(&s, task)?.last().unwrap();
            let question = s.reference(item, "task-item/content")?;
            let field = s.refs(question, "question/answer-fields")?[0];
            at += 100;
            s = f.act("answer", json!({"taskId":task,"itemId":item,"responses":[{"fieldId":field,"value":"2"}]}), at)?;
            let saved_items = items(&s, task)?;
            let saved_answer = s.entity(item)?.clone();
            at += 100;
            s = f.act("pause", json!({"taskId":task}), at)?;
            assert_eq!(status(&s, task, "learner-task/status")?, "paused");
            at += 100;
            s = f.act("resume", json!({"taskId":task}), at)?;
            assert_eq!(status(&s, task, "learner-task/status")?, "started");
            assert_eq!(items(&s, task)?, saved_items);
            assert_eq!(s.entity(item)?, &saved_answer);

            let after = learning::study_candidates(
                &s, f.learner, course(&s, f.learner)?,
                DateTime::from_timestamp_millis(at).unwrap(),
            )?;
            assert_eq!(serde_json::to_value(after)?, serde_json::to_value(required)?);
            for attr in ["learner/queue", "learner/course", "learner/self-directed"] {
                assert_eq!(s.entity(f.learner)?.get(attr), before.entity(f.learner)?.get(attr));
            }
            let required_tasks: Vec<_> = before.refs(f.learner, "learner/activity")?.into_iter()
                .filter(|t| before.reference(*t, "learner-task/activity").unwrap() != activity)
                .collect();
            for task in required_tasks {
                assert_eq!(s.entity(task)?, before.entity(task)?);
            }
        }
    }
    Ok(())
}

#[test]
fn required_review_failure_becomes_lesson_and_optional_retake_uses_original_kps() -> Result<()> {
    let mut f = Fixture::new(false)?;
    let (original, mut s) = f.start("assessment")?;
    let a = s.reference(original, "learner-task/activity")?;
    let original_questions: Vec<_> = learning::lesson_steps(&s, a)?
        .iter()
        .map(|st| st.content)
        .collect();
    // One correct and four unanswered: both visited and unvisited misses require repair.
    let q = s.reference(items(&s, original)?[0], "task-item/content")?;
    let field = s.refs(q, "question/answer-fields")?[0];
    s = f.act(
        "submit",
        json!({"taskId":original,"responses":[{"fieldId":field,"value":"2"}]}),
        f.now + 200,
    )?;
    assert_eq!(
        course_academy_engine::scheduling::lifecycle(&s, f.learner)?
            .repairs
            .len(),
        4
    );
    let mut at = f.now + 300;
    let (forms, _) =
        queue_preparation(&s, f.learner, DateTime::from_timestamp_millis(at).unwrap())?;
    f.tx(forms, at)?;
    s = f.snapshot()?;
    let home_view = home(&s, f.learner)?;
    assert_eq!(home_view["activities"].as_array().unwrap().len(), 4);
    assert!(
        home_view["activities"]
            .as_array()
            .unwrap()
            .iter()
            .all(|v| v["type"] == "review")
    );
    // Queue starts still honor required work. Explicit study can reopen a saved
    // completed lesson without changing its outcome or awarding more credit.
    let correct_topic = s.topic_for_question(q)?;
    let correct_lesson = topic_lesson(&s, correct_topic)?;
    assert!(
        mutate(
            &s,
            f.learner,
            "start",
            &json!({"activityId":correct_lesson}),
            DateTime::from_timestamp_millis(at + 1).unwrap()
        )
        .is_err()
    );
    let (forms, result) = mutate(
        &s,
        f.learner,
        "study-topic",
        &json!({"topicId":correct_topic}),
        DateTime::from_timestamp_millis(at + 1).unwrap(),
    )?;
    assert!(forms.is_empty());
    assert_eq!(result["taskId"], completed_task_for(&s, f.learner, correct_lesson)?.unwrap());
    let review = home_view["activities"][0]["activityId"].as_u64().unwrap();
    at += 100;
    s = f.act("start", json!({"activityId":review}), at)?;
    let task = task_for(&s, f.learner, review)?.unwrap();
    let repair_topic = s.reference(review, "activity/scope")?;
    for _ in 0..5 {
        let item = *items(&s, task)?.last().unwrap();
        let q = s.reference(item, "task-item/content")?;
        let field = s.refs(q, "question/answer-fields")?[0];
        at += 100;
        s = f.act(
            "answer",
            json!({"taskId":task,"itemId":item,"responses":[{"fieldId":field,"value":"3"}]}),
            at,
        )?;
        at += 100;
        s = f.act("continue", json!({"taskId":task,"itemId":item}), at)?;
    }
    assert_eq!(status(&s, task, "learner-task/status")?, "failed");
    at += 100;
    let (forms, _) =
        queue_preparation(&s, f.learner, DateTime::from_timestamp_millis(at).unwrap())?;
    f.tx(forms, at)?;
    s = f.snapshot()?;
    let lesson_task = s
        .refs(f.learner, "learner/activity")?
        .into_iter()
        .find(|t| {
            s.refs(*t, "learner-task/remediation-for")
                .unwrap_or_default()
                .contains(&original)
                && s.reference(*t, "learner-task/activity")
                    .ok()
                    .is_some_and(|a| retrieval::kind(&s, a).ok().as_deref() == Some("lesson"))
        })
        .ok_or("Required replacement lesson was not created")?;
    assert_eq!(
        s.optional_ref(
            s.reference(lesson_task, "learner-task/activity")?,
            "activity/scope"
        )?,
        Some(repair_topic)
    );
    // Replenish the affected KP before the replacement lesson.
    let kp = s.refs(repair_topic, "topic/knowledge-points")?[0];
    let source = s.refs(kp, "knowledge-point/questions")?[0];
    let fields = s.refs(source, "question/answer-fields")?;
    let mut fresh = vec![];
    for n in 0..6 {
        let key = format!("repair-fresh-{n}");
        fresh.push(json!({"db/id":key,"question/id":{"$uuid":uuid(90000+n)},"question/problem":"Enter two.","question/worked-solution":"Two.","question/difficulty":kw(["question.difficulty/easy","question.difficulty/moderate","question.difficulty/hard"][n as usize%3]),"question/answer-fields":fields}));
        fresh.push(add(json!(kp), "knowledge-point/questions", json!(key)));
    }
    at += 100;
    f.tx(fresh, at)?;
    s = f.snapshot()?;
    at += 100;
    s = f.act(
        "start",
        json!({"activityId":s.reference(lesson_task,"learner-task/activity")?}),
        at,
    )?;
    let example = *items(&s, lesson_task)?.last().unwrap();
    at += 100;
    s = f.act(
        "continue",
        json!({"taskId":lesson_task,"itemId":example}),
        at,
    )?;
    for _ in 0..2 {
        let item = *items(&s, lesson_task)?.last().unwrap();
        let q = s.reference(item, "task-item/content")?;
        let field = s.refs(q, "question/answer-fields")?[0];
        at += 100;
        s = f.act(
            "answer",
            json!({"taskId":lesson_task,"itemId":item,"responses":[{"fieldId":field,"value":"2"}]}),
            at,
        )?;
        at += 100;
        s = f.act("continue", json!({"taskId":lesson_task,"itemId":item}), at)?;
    }
    assert_eq!(status(&s, lesson_task, "learner-task/status")?, "completed");
    assert!(
        !course_academy_engine::scheduling::lifecycle(&s, f.learner)?
            .repairs
            .contains_key(&(original, repair_topic))
    );
    // Pass every remaining required review.
    loop {
        at += 100;
        let (forms, _) =
            queue_preparation(&s, f.learner, DateTime::from_timestamp_millis(at).unwrap())?;
        f.tx(forms, at)?;
        s = f.snapshot()?;
        let h = course_academy_engine::scheduling::lifecycle(&s, f.learner)?;
        if h.repairs.is_empty() {
            break;
        }
        let review = home(&s, f.learner)?["activities"][0]["activityId"]
            .as_u64()
            .ok_or("Missing required review")?;
        at += 100;
        s = f.act("start", json!({"activityId":review}), at)?;
        let task = task_for(&s, f.learner, review)?.unwrap();
        for _ in 0..3 {
            let item = *items(&s, task)?.last().unwrap();
            let q = s.reference(item, "task-item/content")?;
            let field = s.refs(q, "question/answer-fields")?[0];
            at += 100;
            s = f.act(
                "answer",
                json!({"taskId":task,"itemId":item,"responses":[{"fieldId":field,"value":"2"}]}),
                at,
            )?;
            at += 100;
            s = f.act("continue", json!({"taskId":task,"itemId":item}), at)?;
        }
    }
    let retake = s
        .refs(f.learner, "learner/activity")?
        .into_iter()
        .find(|t| s.optional_ref(*t, "learner-task/retake-of").ok().flatten() == Some(original))
        .ok_or("Optional retake not created")?;
    let retake_activity = s.reference(retake, "learner-task/activity")?;
    let retake_questions: Vec<_> = learning::lesson_steps(&s, retake_activity)?
        .iter()
        .map(|st| st.content)
        .collect();
    assert_eq!(retake_questions.len(), original_questions.len());
    assert_eq!(
        original_questions
            .iter()
            .map(|q| course_academy_engine::scheduling::original_kp(&s, *q).unwrap())
            .collect::<BTreeSet<_>>(),
        retake_questions
            .iter()
            .map(|q| course_academy_engine::scheduling::original_kp(&s, *q).unwrap())
            .collect()
    );
    assert!(retake_questions.iter().all(|q| {
        !s.refs(f.learner, "learner/activity")
            .unwrap()
            .iter()
            .any(|t| {
                s.refs(*t, "learner-task/items")
                    .unwrap()
                    .iter()
                    .any(|i| s.optional_ref(*i, "task-item/content").ok().flatten() == Some(*q))
            })
    }));
    assert!(
        retake_questions
            .iter()
            .map(|q| course_academy_engine::assessment_sampling::seconds(&s, *q).unwrap())
            .sum::<f64>()
            <= 900.0
    );
    assert!(
        learning::study_candidates(
            &s,
            f.learner,
            course(&s, f.learner)?,
            DateTime::from_timestamp_millis(at).unwrap()
        )?
        .iter()
        .any(|p| p.activity == retake_activity && p.priority < 11000.0)
    );
    // Six unfinished lessons used to push this ready retake past the home's
    // five-card cutoff. Exercise the real planner and home in both study modes.
    let mut crowded = s.clone();
    let source_lesson = topic_lesson(&s, correct_topic)?;
    let source_step = s.refs(source_lesson, "activity/steps")?[0];
    let example = learning::lesson_steps(&s, source_lesson)?[0].example.unwrap();
    for index in 0..6u64 {
        let activity = 9_000_000 + index * 4;
        let step = activity + 1;
        let task = activity + 2;
        let item = activity + 3;
        let mut definition = s.entity(source_lesson)?.clone();
        definition.insert("activity/id".into(), json!({"$uuid":uuid(activity.into())}));
        definition.insert("activity/steps".into(), json!([step]));
        definition.insert("activity/first-step".into(), json!(step));
        crowded.entities.insert(activity, definition);
        let mut placement = s.entity(source_step)?.clone();
        placement.insert("step/id".into(), json!({"$uuid":uuid(step.into())}));
        crowded.entities.insert(step, placement);
        crowded.entities.insert(task, json!({"learner-task/id":{"$uuid":uuid(task.into())},
            "learner-task/activity":activity,"learner-task/status":kw("learner-task.status/paused"),
            "learner-task/items":[item],"learner-task/elapsed-seconds":0.0}).as_object().unwrap().clone());
        crowded.entities.insert(item, json!({"task-item/id":{"$uuid":uuid(item.into())},
            "task-item/content":example,"task-item/status":kw("task-item.status/paused"),"task-item/elapsed-seconds":0.0}).as_object().unwrap().clone());
        for (entity, attribute, state) in [(task,"learner-task/status","learner-task.status/paused"),
            (item,"task-item/status","task-item.status/paused")] {
            crowded.status_history.push(StatusAssertion {entity,attribute:attribute.into(),value:kw(state),
                t:crowded.basis_t,at:schema::instant_value(DateTime::from_timestamp_millis(at).unwrap())});
        }
        crowded.entities.get_mut(&f.learner).unwrap().get_mut("learner/activity").unwrap().as_array_mut().unwrap().push(json!(task));
    }
    for self_directed in [false, true] {
        crowded.entities.get_mut(&f.learner).unwrap().insert("learner/self-directed".into(), json!(self_directed));
        let before = json!({"entities":crowded.entities,"history":crowded.status_history});
        let plan = learning::study_candidates(&crowded, f.learner, course(&crowded, f.learner)?,
            DateTime::from_timestamp_millis(at).unwrap())?;
        assert_eq!(plan[0].activity, retake_activity);
        assert!(plan[0].priority < 11000.0, "retake remains optional");
        assert_eq!(plan.iter().filter(|p| (9_000_000..9_000_024).contains(&p.activity)).count(), 6);
        let view = home(&crowded, f.learner)?;
        assert_eq!(view["activities"].as_array().unwrap().len(), 5);
        assert_eq!(view["activities"][0]["taskId"], retake);
        assert_eq!(view["activities"][0]["title"], "Retake Quiz 1");
        let resumed = mutate(&crowded, f.learner, "start", &json!({"activityId":9_000_000}),
            DateTime::from_timestamp_millis(at).unwrap());
        assert!(resumed.is_ok(), "optional retake must not block resuming lessons: {:?}", resumed.err());
        assert_eq!(json!({"entities":crowded.entities,"history":crowded.status_history}), before);
    }
    Ok(())
}

fn finish(
    f: &mut Fixture,
    activity: u64,
    question: Option<u64>,
    passed: bool,
    xp: i64,
    at: i64,
) -> Result<u64> {
    finish_origin(f, activity, question, passed, xp, at, None)
}

fn finish_origin(
    f: &mut Fixture,
    activity: u64,
    question: Option<u64>,
    passed: bool,
    xp: i64,
    at: i64,
    origin: Option<u64>,
) -> Result<u64> {
    let key = uid()?;
    let task = format!("record-{key}");
    let mut forms = vec![
        json!({"db/id":task,"learner-task/id":{"$uuid":key},"learner-task/activity":activity,"learner-task/status":kw("learner-task.status/started")}),
        add(json!(f.learner), "learner/activity", json!(task)),
    ];
    if let Some(origin) = origin {
        forms.push(add(
            json!(task),
            "learner-task/remediation-for",
            json!(origin),
        ));
    }
    if let Some(q) = question {
        forms.push(json!({"db/id":"record-item","task-item/id":{"$uuid":uid()?},"task-item/content":q,"task-item/status":kw("task-item.status/started")}));
        forms.push(add(json!(task), "learner-task/items", json!("record-item")));
    }
    f.tx(forms, at)?;
    let s = f.snapshot()?;
    let t = s
        .entities
        .with_attribute("learner-task/id")
        .into_iter()
        .find(|t| s.entities[t]["learner-task/id"] == json!({"$uuid":key}))
        .unwrap();
    let mut forms = vec![
        cas(
            &s,
            t,
            "learner-task/status",
            if passed {
                "learner-task.status/completed"
            } else {
                "learner-task.status/failed"
            },
        )?,
        add(json!(t), "learner-task/xp-earned", json!(xp)),
    ];
    for i in items(&s, t)? {
        forms.push(cas(
            &s,
            i,
            "task-item/status",
            if passed {
                "task-item.status/correct"
            } else {
                "task-item.status/incorrect"
            },
        )?);
    }
    f.tx(forms, at + 1)?;
    Ok(t)
}

#[test]
fn signed_cadence_lesson_break_and_key_prerequisite_path_are_history_derived() -> Result<()> {
    let mut f = Fixture::new(true)?;
    let s = f.snapshot()?;
    let topic = s.refs(course(&s, f.learner)?, "course/units")?[0];
    let module = s.refs(topic, "unit/modules")?[0];
    let topics = s.refs(module, "module/topics")?;
    let topic = topics[0];
    let prerequisite = topics[1];
    let kp = s.refs(topic, "topic/knowledge-points")?[0];
    let question = s.refs(kp, "knowledge-point/questions")?[10];
    let lesson = s
        .entities
        .with_attribute("activity/id")
        .into_iter()
        .find(|a| {
            retrieval::kind(&s, *a).ok().as_deref() == Some("lesson")
                && s.optional_ref(*a, "activity/scope").ok().flatten() == Some(topic)
        })
        .unwrap();
    let mut at = f.now + 100;
    f.tx(
        vec![add(
            json!(kp),
            "knowledge-point/key-prerequisites",
            json!(prerequisite),
        )],
        at,
    )?;
    at += 10;
    finish(&mut f, lesson, Some(question), false, -1, at)?;
    let h = course_academy_engine::scheduling::lifecycle(&f.snapshot()?, f.learner)?;
    assert_eq!(h.xp, 114.0);
    assert!(!h.retry_ready(topic));
    let s = f.snapshot()?;
    let other = s
        .entities
        .with_attribute("activity/id")
        .into_iter()
        .find(|a| {
            retrieval::kind(&s, *a).ok().as_deref() == Some("lesson")
                && s.optional_ref(*a, "activity/scope").ok().flatten() == Some(prerequisite)
        })
        .unwrap();
    for count in 1..=5 {
        at += 10;
        finish(&mut f, other, None, true, 0, at)?;
        assert_eq!(
            course_academy_engine::scheduling::lifecycle(&f.snapshot()?, f.learner)?
                .retry_ready(topic),
            count == 5
        );
    }
    at += 10;
    let second = finish(
        &mut f,
        lesson,
        Some(s.refs(kp, "knowledge-point/questions")?[11]),
        false,
        -1,
        at,
    )?;
    let s = f.snapshot()?;
    let h = course_academy_engine::scheduling::lifecycle(&s, f.learner)?;
    assert_eq!(
        h.repairs.get(&(second, prerequisite)).map(String::as_str),
        Some("review")
    );
    assert!(h.lesson_blocked(&s, topic)?);
    assert!(!h.lesson_blocked(&s, topics[2])?);
    assert!(!h.assessment_origin(&s, second)?);
    // Adopt a fresh already-prepared ordinary review instead of creating a
    // second simultaneous review for the same topic.
    at += 10;
    let (forms, _) =
        queue_preparation(&s, f.learner, DateTime::from_timestamp_millis(at).unwrap())?;
    f.tx(forms, at)?;
    let s = f.snapshot()?;
    assert_eq!(
        s.refs(f.learner, "learner/activity")?
            .into_iter()
            .filter(|t| s
                .refs(*t, "learner-task/remediation-for")
                .unwrap_or_default()
                .contains(&second))
            .count(),
        1
    );
    assert!(
        mutate(
            &s,
            f.learner,
            "study-topic",
            &json!({"topicId":topic}),
            DateTime::from_timestamp_millis(at).unwrap()
        )
        .is_err()
    );
    Ok(())
}

/// Durable checks own their course and sufficiently stocked banks, so their
/// outcome never depends on gaps in the real learner's captured questions.
pub(super) fn durable_fixture(
    conn: &Connection,
    endpoint: &str,
    assessment: bool,
) -> Result<(EntitySnapshot, u64, String)> {
    let s = snapshot(&conn.sync()?)?;
    let policy = course_academy_engine::question_selection::active_policy(&s)?;
    let nonce = uid()?;
    let prefix = u128::from_str_radix(&nonce.replace('-', ""), 16)? & (!0u128 << 32);
    let id = |n| json!({"$uuid":uuid(prefix|n)});
    let learner = format!("scheduler-fixture-{nonce}");
    let mut forms = vec![
        json!({"db/id":"fixture-course","course/id":id(1),"course/title":"Isolated scheduler verification","course/units":["fixture-unit"]}),
        json!({"db/id":"fixture-unit","unit/id":id(2),"unit/modules":["fixture-module"]}),
        json!({"db/id":"fixture-module","module/id":id(3),"module/topics":(0..5).map(|i|format!("fixture-topic-{i}")).collect::<Vec<_>>()}),
        json!({"db/id":"fixture-learner","learner/id":learner,"learner/name":"Temporary scheduler verification","learner/course":"fixture-course","learner/self-directed":false,"learner/knowledge-profile":(0..5).map(|i|format!("fixture-progress-{i}")).collect::<Vec<_>>(),"learner/activity":if assessment {(0..5).map(|i|format!("fixture-mastered-{i}")).collect::<Vec<_>>()}else{vec![]},"db/ensure":kw("learner/validate")}),
    ];
    for topic in 0..5u128 {
        forms.push(json!({"db/id":format!("fixture-topic-{topic}"),"topic/id":id(10+topic),"topic/title":format!("Verification topic {topic}"),"topic/knowledge-points":[format!("fixture-kp-{topic}")]}));
        forms.push(json!({"db/id":format!("fixture-kp-{topic}"),"knowledge-point/id":id(20+topic),"knowledge-point/title":format!("Verification skill {topic}"),"knowledge-point/canonical-example":format!("fixture-example-{topic}"),"knowledge-point/questions":(0..30).map(|i|format!("fixture-question-{topic}-{i}")).collect::<Vec<_>>(),"db/ensure":kw("knowledge-point/validate")}));
        forms.push(json!({"db/id":format!("fixture-example-{topic}"),"question/id":id(30+topic),"question/problem":"One plus one?","question/worked-solution":"Two.","db/ensure":kw("question/validate")}));
        forms.push(json!({"db/id":format!("fixture-lesson-{topic}"),"activity/id":id(40+topic),"activity/title":format!("Verification lesson {topic}"),"activity/type":kw("activity.type/lesson"),"activity/course":"fixture-course","activity/scope":format!("fixture-topic-{topic}"),"activity/steps":[format!("fixture-step-{topic}")],"activity/first-step":format!("fixture-step-{topic}"),"db/ensure":kw("activity/validate")}));
        forms.push(json!({"db/id":format!("fixture-step-{topic}"),"step/id":id(50+topic),"step/content":format!("fixture-kp-{topic}"),"step/expected-seconds":300.0,"db/ensure":kw("step/validate")}));
        forms.push(json!({"db/id":format!("fixture-progress-{topic}"),"progress/id":format!("fixture-{nonce}-{topic}"),"progress/topic":format!("fixture-topic-{topic}"),"progress/policy":policy,"progress/learned":assessment,"progress/repetitions":if assessment {2.0}else{0.0},"progress/memory":if assessment {1.0}else{0.0},"progress/memory-at":{"$instant":Utc::now().timestamp_millis()},"progress/interval-days":4.0,"progress/assessment-accuracy":0.8,"progress/practice-accuracy":0.8,"progress/assessment-mass":0.0,"progress/practice-mass":0.0,"db/ensure":kw("progress/validate")}));
        if assessment {
            forms.push(json!({"db/id":format!("fixture-mastered-{topic}"),"learner-task/id":id(60+topic),"learner-task/activity":format!("fixture-lesson-{topic}"),"learner-task/status":kw("learner-task.status/started"),"learner-task/xp-earned":30,"db/ensure":kw("learner-task/validate")}));
        }
        for offset in 0..30u128 {
            let n = 1000 + topic * 100 + offset * 3;
            forms.push(json!({"db/id":format!("fixture-question-{topic}-{offset}"),"question/id":id(n),"question/problem":"Enter two.","question/worked-solution":"One plus one is two.","question/difficulty":kw(["question.difficulty/easy","question.difficulty/moderate","question.difficulty/hard"][offset as usize%3]),"question/answer-fields":[format!("fixture-field-{topic}-{offset}")],"db/ensure":kw("question/validate")}));
            forms.push(json!({"db/id":format!("fixture-field-{topic}-{offset}"),"answer-field/id":id(n+1),"answer-field/type":kw("answer-field.type/blank"),"answer-field/key":"value","answer-field/choices":[format!("fixture-answer-{topic}-{offset}")],"answer-field/correct":format!("fixture-answer-{topic}-{offset}"),"db/ensure":kw("answer-field/validate")}));
            forms.push(json!({"db/id":format!("fixture-answer-{topic}-{offset}"),"answer/id":id(n+2),"answer/type":kw("answer.type/math"),"answer/value":"2","db/ensure":kw("answer/validate")}));
        }
    }
    // Meet the same L30 cutoff as real Study topics, with known foundations
    // so the course planner can admit lessons without bypassing prerequisites.
    for foundation in 0..learning::MIN_STUDY_LAYER - 1 {
        let next: Vec<_> = if foundation + 1 == learning::MIN_STUDY_LAYER - 1 {
            (0..5).map(|i| format!("fixture-topic-{i}")).collect()
        } else {
            vec![format!("fixture-foundation-{}", foundation + 1)]
        };
        forms.push(json!({"db/id":format!("fixture-foundation-{foundation}"),"topic/id":id(10000+foundation as u128),"topic/next":next}));
        forms.push(json!({"db/id":format!("fixture-foundation-progress-{foundation}"),"progress/id":format!("fixture-{nonce}-foundation-{foundation}"),"progress/topic":format!("fixture-foundation-{foundation}"),"progress/policy":policy,"progress/learned":true,"progress/repetitions":1.0,"progress/memory":1.0,"progress/memory-at":{"$instant":Utc::now().timestamp_millis()},"progress/interval-days":4.0,"progress/assessment-accuracy":0.8,"progress/practice-accuracy":0.8,"progress/assessment-mass":0.0,"progress/practice-mass":0.0,"db/ensure":kw("progress/validate")}));
        forms[3]["learner/knowledge-profile"].as_array_mut().unwrap().push(json!(format!("fixture-foundation-progress-{foundation}")));
    }
    let start = Utc::now();
    let mut s = super::integration::commit(
        conn,
        endpoint,
        &s,
        forms,
        &format!("{learner}-setup"),
        start,
    )?;
    let l = s
        .entities
        .with_attribute("learner/id")
        .into_iter()
        .find(|l| s.entities[l]["learner/id"] == json!(learner))
        .unwrap();
    if assessment {
        let mut forms = vec![];
        for task in s.refs(l, "learner/activity")? {
            forms.push(cas(&s, task, "learner-task/status", "learner-task.status/completed")?);
            // Preserve the original source learning date while recording the
            // fixture now, just as imported terminal lessons do.
            forms.push(add(json!(task), "learner-task/finished-at", schema::instant_value(start-chrono::Duration::days(3))));
        }
        s = super::integration::commit(
            conn,
            endpoint,
            &s,
            forms,
            &format!("{learner}-mastered"),
            start + chrono::Duration::seconds(1),
        )?;
    }
    if assessment {
        // Live writers require monotonic transaction instants. Author this
        // admitted route explicitly using the original learning dates above,
        // without backdating any live transaction instants.
        let qs = (0..5)
            .map(|topic| {
                let t = s
                    .entities
                    .with_attribute("topic/id")
                    .into_iter()
                    .find(|t| text(&s, *t, "topic/title") == format!("Verification topic {topic}"))
                    .unwrap();
                let kp = s.refs(t, "topic/knowledge-points").unwrap()[0];
                s.refs(kp, "knowledge-point/questions").unwrap()[topic % 3]
            })
            .collect::<Vec<_>>();
        let mut forms = vec![
            json!({"db/id":"fixture-assessment","activity/id":id(70),"activity/title":"Admitted verification assessment","activity/type":kw("activity.type/assessment"),"activity/steps":(0..5).map(|i|format!("fixture-assessment-step-{i}")).collect::<Vec<_>>(),"activity/first-step":"fixture-assessment-step-0","activity/time-limit-seconds":900.0,"activity/expected-seconds":540.0,"db/ensure":kw("activity/validate")}),
            json!({"db/id":"fixture-assessment-task","learner-task/id":id(71),"learner-task/activity":"fixture-assessment","learner-task/status":kw("learner-task.status/unlocked"),"learner-task/priority":11000.0,"db/ensure":kw("learner-task/validate")}),
            add(
                json!(l),
                "learner/activity",
                json!("fixture-assessment-task"),
            ),
        ];
        for (i, q) in qs.iter().enumerate() {
            let mut record = json!({"db/id":format!("fixture-assessment-step-{i}"),"step/id":id(80+i as u128),"step/content":q,"db/ensure":kw("step/validate")});
            if i < 4 {
                record["step/next"] = json!(format!("fixture-assessment-step-{}", i + 1));
            }
            forms.push(record);
        }
        s = super::integration::commit(
            conn,
            endpoint,
            &s,
            forms,
            &format!("{learner}-admitted"),
            Utc::now(),
        )?;
    }
    Ok((s, l, nonce))
}

pub(super) fn durable_cleanup(
    conn: &Connection,
    endpoint: &str,
    l: u64,
    nonce: &str,
) -> Result<()> {
    let s = snapshot(&conn.sync()?)?;
    let prefix = &nonce[..24];
    let mut entities: BTreeSet<_> = s
        .entities
        .iter()
        .filter_map(|(e, r)| {
            r.values()
                .any(|v| {
                    v.get("$uuid")
                        .and_then(Json::as_str)
                        .is_some_and(|v| v.starts_with(prefix))
                })
                .then_some(*e)
        })
        .collect();
    entities.insert(l);
    for task in s.refs(l, "learner/activity")? {
        entities.insert(task);
        let a = s.reference(task, "learner-task/activity")?;
        entities.insert(a);
        entities.extend(s.refs(a, "activity/steps")?);
    }
    let fields: Vec<_> = entities
        .iter()
        .copied()
        .filter(|e| s.entities[e].contains_key("answer-field/id"))
        .collect();
    for f in fields {
        entities.extend(s.refs(f, "answer-field/choices")?);
    }
    let forms = entities
        .into_iter()
        .map(|e| json!([kw("db/retractEntity"), e]))
        .collect();
    let after = super::integration::commit(
        conn,
        endpoint,
        &s,
        forms,
        &format!("fixture-{nonce}-cleanup"),
        Utc::now(),
    )?;
    assert!(!after.entities.contains_key(&l));
    assert!(!after.entities.values().any(|r| r.values().any(|v| {
        v.get("$uuid")
            .and_then(Json::as_str)
            .is_some_and(|v| v.starts_with(prefix))
    })));
    Ok(())
}

#[test]
#[ignore = "requires local writer; creates and removes isolated scheduler content"]
fn durable_scheduler_lifecycle() -> Result<()> {
    let database = std::env::var("EDB_DATABASE").unwrap_or("math".into());
    let endpoint = std::env::var("EDB_ENDPOINT").unwrap_or("/tmp/edb-math/writer.sock".into());
    let conn = Connection::connect_configured(postgres_config_from_env()?, database.clone(), 256)?;
    let (s, l, nonce) = durable_fixture(&conn, &endpoint, true)?;
    let learner = s.entities[&l]["learner/id"].as_str().unwrap().to_string();
    let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| -> Result<()> {
        let mut app = Application::connect(database.clone(), learner.clone(), endpoint.clone())?;
        fn request(app: &mut Application, action: &str, mut body: Json) -> Result<Json> {
            body["action"] = json!(action);
            body["requestId"] = json!(uid()?);
            app.process(&body)
        }
        let queue = request(&mut app, "queue", json!({}))?;
        let a = queue["activities"][0]["activityId"].as_u64().unwrap();
        assert_eq!(queue["activities"][0]["type"], "assessment");
        let mut view = request(&mut app, "start", json!({"activityId":a}))?;
        let task = view["taskId"].as_u64().unwrap();
        let original: Vec<_> = view["questions"]
            .as_array()
            .unwrap()
            .iter()
            .map(|q| q["questionId"].as_u64().unwrap())
            .collect();
        let field = view["step"]["fields"][0]["id"].as_u64().unwrap();
        let body = json!({"taskId":task,"itemId":view["step"]["itemId"],"responses":[{"fieldId":field,"value":"2"}]});
        request(&mut app, "draft", body.clone())?;
        request(&mut app, "draft", body)?;
        // Reconnect before final submission: saved drafts and reservations survive.
        drop(app);
        let mut app = Application::connect(database.clone(), learner.clone(), endpoint.clone())?;
        view = request(&mut app, "task", json!({"taskId":task}))?;
        assert_eq!(view["step"]["fields"][0]["response"]["value"], "2");
        assert!(view["step"]["fields"][0].get("grade").is_none());
        view = request(&mut app, "submit", json!({"taskId":task}))?;
        assert_eq!(view["assessmentScore"]["correct"], 1);
        assert!(app.cached_home(true).is_some(), "completion must retain the freshly prepared home");
        loop {
            let queue = request(&mut app, "queue", json!({}))?;
            let h = course_academy_engine::scheduling::lifecycle(&app.snapshot, l)?;
            if h.repairs.is_empty() {
                break;
            }
            assert!(
                queue["activities"]
                    .as_array()
                    .unwrap()
                    .iter()
                    .all(|v| v["type"] == "review")
            );
            let a = queue["activities"][0]["activityId"].as_u64().unwrap();
            let mut view = request(&mut app, "start", json!({"activityId":a}))?;
            let t = view["taskId"].as_u64().unwrap();
            for _ in 0..3 {
                let i = view["step"]["itemId"].as_u64().unwrap();
                let f = view["step"]["fields"][0]["id"].as_u64().unwrap();
                request(
                    &mut app,
                    "answer",
                    json!({"taskId":t,"itemId":i,"responses":[{"fieldId":f,"value":"2"}]}),
                )?;
                view = request(&mut app, "continue", json!({"taskId":t,"itemId":i}))?;
            }
            assert_eq!(view["status"], "completed");
            assert!(app.cached_home(true).is_some(), "review completion must retain the newly planned home");
        }
        let s = &app.snapshot;
        let retake = s
            .refs(l, "learner/activity")?
            .into_iter()
            .find(|t| s.optional_ref(*t, "learner-task/retake-of").ok().flatten() == Some(task))
            .ok_or("durable retake missing")?;
        let a = s.reference(retake, "learner-task/activity")?;
        let next: Vec<_> = learning::lesson_steps(s, a)?
            .iter()
            .map(|st| st.content)
            .collect();
        assert_eq!(next.len(), original.len());
        assert!(next.iter().all(|q| !original.contains(q)));
        assert_eq!(
            next.iter()
                .map(|q| course_academy_engine::scheduling::original_kp(s, *q).unwrap())
                .collect::<BTreeSet<_>>(),
            original
                .iter()
                .map(|q| course_academy_engine::scheduling::original_kp(s, *q).unwrap())
                .collect()
        );
        let before = course_academy_engine::scheduling::lifecycle(s, l)?.xp;
        request(&mut app, "start", json!({"activityId":a}))?;
        for q in next {
            let view = request(
                &mut app,
                "navigate",
                json!({"taskId":retake,"questionId":q}),
            )?;
            let field = view["step"]["fields"][0]["id"].as_u64().unwrap();
            request(
                &mut app,
                "draft",
                json!({"taskId":retake,"itemId":view["step"]["itemId"],"responses":[{"fieldId":field,"value":"2"}]}),
            )?;
        }
        let view = request(&mut app, "submit", json!({"taskId":retake}))?;
        assert_eq!(
            view["assessmentScore"]["correct"],
            view["assessmentScore"]["total"]
        );
        assert_eq!(
            course_academy_engine::scheduling::lifecycle(&app.snapshot, l)?.xp,
            before
        );
        assert!(
            course_academy_engine::scheduling::lifecycle(&app.snapshot, l)?
                .retakes
                .is_empty()
        );
        Ok(())
    }));
    durable_cleanup(&conn, &endpoint, l, &nonce)?;
    match result {
        Ok(r) => r,
        Err(e) => std::panic::resume_unwind(e),
    }
}

#[test]
fn assessment_admission_opens_at_48_hours_without_any_prior_retrieval() -> Result<()> {
    let f = Fixture::with_admission(false, 48 * 3_600_000, false)?;
    let s = f.snapshot()?;
    assert!(s.refs(f.learner, "learner/activity")?.iter().all(|t| {
        retrieval::kind(&s, s.reference(*t, "learner-task/activity").unwrap()).unwrap() == "lesson"
    }));
    assert_eq!(
        course_academy_engine::scheduling::lifecycle(&s, f.learner)?.xp,
        125.0
    );
    let before = DateTime::from_timestamp_millis(f.now + 999).unwrap();
    assert!(
        retrieval::schedule(&s, f.learner, course(&s, f.learner)?, before)?
            .iter()
            .all(|d| d.kind != "assessment")
    );
    let admitted = DateTime::from_timestamp_millis(f.now + 1000).unwrap();
    assert!(
        retrieval::schedule(&s, f.learner, course(&s, f.learner)?, admitted)?
            .iter()
            .any(|d| d.kind == "assessment")
    );
    Ok(())
}

#[test]
fn three_ordinary_reviews_offer_a_lesson_and_only_an_actual_offer_resets_the_streak() -> Result<()>
{
    use course_academy_engine::{learning::PlannedActivity, scheduling::filter_candidates};
    let mut f = Fixture::new(true)?;
    let s = f.snapshot()?;
    let lesson = s
        .refs(f.learner, "learner/activity")?
        .into_iter()
        .find(|t| {
            retrieval::kind(&s, s.reference(*t, "learner-task/activity").unwrap()).unwrap()
                == "lesson"
        })
        .unwrap();
    let lesson_activity = s.reference(lesson, "learner-task/activity")?;
    let mut plan = Vec::new();
    for activity in s.entities.with_attribute("activity/type") {
        let kind = retrieval::kind(&s, activity)?;
        if kind == "review"
            && s.owners(activity, "learner-task/activity")?
                .iter()
                .any(|task| {
                    matches!(
                        status(&s, *task, "learner-task/status").as_deref(),
                        Ok("unlocked")
                    )
                })
            || activity == lesson_activity
        {
            plan.push(PlannedActivity {
                activity,
                topic: s.reference(activity, "activity/scope")?,
                priority: if kind == "review" { 6000.0 } else { 100.0 },
                target_count: 0,
                target_topics: vec![],
                remaining_topics: 0,
                nearest_target_steps: None,
                due: None,
                reason: "Eligible fixture candidate".into(),
            });
        }
    }
    plan.sort_by(|a, b| b.priority.total_cmp(&a.priority));
    assert!(plan.len() >= 6);
    // Preparation without an actual offer leaves the existing review streak due.
    assert_eq!(
        filter_candidates(&s, f.learner, plan.clone())?[0].activity,
        lesson_activity
    );
    f.tx(
        vec![add(
            json!(lesson),
            "learner-task/offered-at",
            json!({"$instant":f.now+10}),
        )],
        f.now + 10,
    )?;
    assert_ne!(
        filter_candidates(&f.snapshot()?, f.learner, plan.clone())?[0].activity,
        lesson_activity
    );
    let review = plan
        .iter()
        .find(|p| p.activity != lesson_activity)
        .unwrap()
        .activity;
    for (i, passed) in [true, false, true].into_iter().enumerate() {
        let at = f.now + 20 + i as i64 * 2;
        finish(&mut f, review, None, passed, 0, at)?;
    }
    assert_eq!(
        filter_candidates(&f.snapshot()?, f.learner, plan.clone())?[0].activity,
        lesson_activity
    );
    let at = f.now + 1000;
    f.tx(
        vec![add(
            json!(lesson),
            "learner-task/offered-at",
            json!({"$instant":at}),
        )],
        at,
    )?;
    assert_ne!(
        filter_candidates(&f.snapshot()?, f.learner, plan)?[0].activity,
        lesson_activity
    );
    Ok(())
}

#[test]
fn failed_required_lesson_releases_global_gate_until_five_other_successes() -> Result<()> {
    let mut f = Fixture::new(false)?;
    let (original, mut s) = f.start("assessment")?;
    s = f.act("submit", json!({"taskId":original}), f.now + 200)?;
    let mut at = f.now + 300;
    let (forms, _) =
        queue_preparation(&s, f.learner, DateTime::from_timestamp_millis(at).unwrap())?;
    f.tx(forms, at)?;
    s = f.snapshot()?;
    let reviews: Vec<_> = s
        .refs(f.learner, "learner/activity")?
        .into_iter()
        .filter_map(|t| {
            s.refs(t, "learner-task/remediation-for")
                .ok()?
                .contains(&original)
                .then(|| s.reference(t, "learner-task/activity").unwrap())
        })
        .collect();
    let topic = s.reference(reviews[0], "activity/scope")?;
    at += 10;
    finish_origin(&mut f, reviews[0], None, false, -1, at, Some(original))?;
    s = f.snapshot()?;
    let lesson = topic_lesson(&s, topic)?;
    let kp = s.refs(topic, "topic/knowledge-points")?[0];
    let q = s.refs(kp, "knowledge-point/questions")?[10];
    at += 10;
    finish_origin(&mut f, lesson, Some(q), false, -1, at, Some(original))?;
    let h = course_academy_engine::scheduling::lifecycle(&f.snapshot()?, f.learner)?;
    assert!(!h.retry_ready(topic));
    assert_eq!(
        h.repairs.get(&(original, topic)).map(String::as_str),
        Some("lesson")
    );
    for review in reviews.iter().skip(1) {
        at += 10;
        finish_origin(&mut f, *review, None, true, 0, at, Some(original))?;
    }
    s = f.snapshot()?;
    let h = course_academy_engine::scheduling::lifecycle(&s, f.learner)?;
    assert_eq!(h.repairs.len(), 1);
    assert!(!h.retry_ready(topic));
    assert!(!h.retake_ready(&s, original)?);
    let plan = learning::study_candidates(
        &s,
        f.learner,
        course(&s, f.learner)?,
        DateTime::from_timestamp_millis(at).unwrap(),
    )?;
    assert!(!plan.iter().any(|p| p.priority >= 11000.0));
    // Four successful repairs on other topics advance the break; one further
    // ordinary success reaches five. Failures never count as that fifth.
    let other = s.reference(reviews[1], "activity/scope")?;
    let other_lesson = topic_lesson(&s, other)?;
    at += 10;
    finish(&mut f, other_lesson, None, false, 0, at)?;
    assert!(
        !course_academy_engine::scheduling::lifecycle(&f.snapshot()?, f.learner)?
            .retry_ready(topic)
    );
    at += 10;
    finish(&mut f, other_lesson, None, true, 0, at)?;
    s = f.snapshot()?;
    assert!(course_academy_engine::scheduling::lifecycle(&s, f.learner)?.retry_ready(topic));
    at += 10;
    let (forms, _) =
        queue_preparation(&s, f.learner, DateTime::from_timestamp_millis(at).unwrap())?;
    f.tx(forms, at)?;
    s = f.snapshot()?;
    let view = home(&s, f.learner)?;
    assert!(view["activities"].as_array().unwrap().iter().all(|v|v["activityId"]==json!(lesson)&&v["priority"].as_f64().unwrap()>=12000.0));
    assert!(!view["activities"].as_array().unwrap().is_empty());
    Ok(())
}

#[test]
fn focused_regeneration_preserves_the_quiz_task_and_requires_five_target_topics() -> Result<()> {
    let mut f = Fixture::with_admission(false, 3 * 86400000, false)?;
    let old = f.available("assessment")?;
    let before = f.snapshot()?;
    let task = task_for(&before, f.learner, old)?.unwrap();
    let at = DateTime::from_timestamp_millis(f.now + 100).unwrap();
    let topics: Vec<_> = retrieval::assessment_pools(&before, f.learner, at)?.into_keys().collect();
    assert_eq!(topics.len(), 5);
    f.tx(vec![json!({"db/id":f.learner,"learner/targets":topics.clone()})], f.now + 1)?;
    f.focused_mode = true;
    let mut short = f.snapshot()?;
    short.entities.get_mut(&f.learner).unwrap().insert("learner/targets".into(), json!(&topics[..4]));
    assert!(mutate(&short, f.learner, "regenerate-assessment", &json!({"activityId":old}), at).is_err());
    let focused = f.snapshot()?;
    let (forms, result) = mutate(&focused, f.learner, "regenerate-assessment", &json!({"activityId":old}), at)?;
    assert_eq!(result["taskId"], task);
    f.tx(forms, f.now + 100)?;
    let after = f.snapshot()?;
    let new = after.reference(task, "learner-task/activity")?;
    assert_ne!(old, new);
    assert!(learning::activity_in_study_focus(&after, f.learner, new)?);
    assert_eq!(after.entity(old)?, focused.entity(old)?);
    assert_eq!(after.refs(f.learner, "learner/activity")?, focused.refs(f.learner, "learner/activity")?);
    assert_eq!(status(&after, task, "learner-task/status")?, "unlocked");
    assert!(items(&after, task)?.is_empty());
    assert_eq!(serde_json::to_value(&after.status_history)?, serde_json::to_value(&focused.status_history)?);
    Ok(())
}

#[test]
fn explicit_regeneration_replaces_only_never_started_route_and_reprices_estimate() -> Result<()> {
    let mut f = Fixture::with_admission(false, 3 * 86400000, false)?;
    let old = f.available("assessment")?;
    let before = f.snapshot()?;
    let task = task_for(&before, f.learner, old)?.unwrap();
    // Simulate the stale fixed allocation on a prepared short assessment.
    f.tx(vec![add(json!(task), "learner-task/xp-base", json!(15))], f.now + 1)?;
    let before = f.snapshot()?;
    let at = DateTime::from_timestamp_millis(f.now + 100).unwrap();
    let expected_pools = retrieval::assessment_pools(&before, f.learner, at)?;
    assert_eq!(expected_pools.len(), 5);
    let (forms, result) = mutate(&before, f.learner, "regenerate-assessment", &json!({"activityId":old}), at)?;
    assert_eq!(result["regeneration"]["eligibleTopicCount"], 5);
    assert_eq!(result["regeneration"]["previousActivityId"], old);
    f.tx(forms, f.now + 100)?;
    let after = f.snapshot()?;
    let new = after.reference(task, "learner-task/activity")?;
    assert_ne!(old, new);
    assert_eq!(after.entity(old)?, before.entity(old)?, "old definition remains intact");
    assert_eq!(serde_json::to_value(&after.status_history)?, serde_json::to_value(&before.status_history)?, "regeneration must not start work");
    assert!(items(&after, task)?.is_empty());
    assert_eq!(status(&after, task, "learner-task/status")?, "unlocked");
    assert_eq!(after.refs(f.learner, "learner/activity")?, before.refs(f.learner, "learner/activity")?);
    for progress in before.refs(f.learner, "learner/knowledge-profile")? {
        assert_eq!(after.entity(progress)?, before.entity(progress)?);
    }
    let route = learning::lesson_steps(&after, new)?;
    let seconds: f64 = route.iter().map(|step| course_academy_engine::assessment_sampling::seconds(&after,step.content).unwrap()).sum();
    assert_eq!(seconds, 720.0, "five distinct topics with all three bands can reach twelve minutes");
    assert_eq!(number(&after,new,"activity/expected-seconds"), seconds);
    assert_eq!(number(&after,new,"activity/time-limit-seconds"), 900.0);
    assert_eq!(number(&after,task,"learner-task/xp-base"), 12.0);
    let bands: BTreeSet<_> = route.iter().map(|step|course_academy_engine::assessment_sampling::band(&after,step.content).unwrap().unwrap()).collect();
    assert_eq!(bands.len(),3);
    let card = home(&after,f.learner)?["activities"].as_array().unwrap().iter().find(|a|a["activityId"]==new).unwrap().clone();
    assert_eq!(card["xpBase"],12);
    let mut legacy = after.clone();
    legacy.entities.get_mut(&new).unwrap().remove("activity/expected-seconds");
    legacy.entities.get_mut(&task).unwrap().remove("learner-task/xp-base");
    let legacy_home = home(&legacy,f.learner)?;
    assert_eq!(legacy_home["activities"].as_array().unwrap().iter().find(|a|a["activityId"]==new).unwrap()["xpBase"],12);

    // Ordinary queue refresh continues to preserve the selected route.
    let unchanged = f.act("queue",json!({}),f.now+200)?;
    assert_eq!(unchanged.reference(task,"learner-task/activity")?,new);
    assert!(mutate(&unchanged,f.learner,"regenerate-assessment",&json!({"activityId":old}),at).is_err());
    Ok(())
}

#[test]
fn regeneration_rejects_started_history_retake_and_foreign_task() -> Result<()> {
    let mut f = Fixture::new(false)?;
    let activity = f.available("assessment")?;
    let initial = f.snapshot()?;
    let task = task_for(&initial,f.learner,activity)?.unwrap();
    let at = DateTime::from_timestamp_millis(f.now+500).unwrap();
    let attempt = |s:&EntitySnapshot,l| mutate(s,l,"regenerate-assessment",&json!({"activityId":activity}),at);
    let mut retake = initial.clone();
    retake.entities.get_mut(&task).unwrap().insert("learner-task/retake-of".into(),json!(task));
    assert!(attempt(&retake,f.learner).unwrap_err().to_string().contains("ordinary assessment"));
    let mut foreign = initial.clone();
    foreign.entities.get_mut(&f.learner).unwrap().insert("learner/activity".into(),json!([]));
    assert!(attempt(&foreign,f.learner).is_err());
    f.tx(vec![json!({"db/id":"other-learner","learner/id":"regeneration-other","learner/activity":[task]})],f.now+1)?;
    assert!(attempt(&f.snapshot()?,f.learner).unwrap_err().to_string().contains("does not belong"));
    let shared = f.snapshot()?;
    let other = shared.owners(task,"learner/activity")?.into_iter().find(|l|*l!=f.learner).unwrap();
    f.tx(vec![json!([kw("db/retract"),other,kw("learner/activity"),task])],f.now+2)?;
    let (_,started) = f.start("assessment")?;
    assert!(attempt(&started,f.learner).unwrap_err().to_string().contains("never-started"));
    let paused = f.act("pause",json!({"taskId":task}),f.now+200)?;
    assert!(attempt(&paused,f.learner).is_err());
    // Even an accidentally reset status cannot erase the evidence of a start.
    f.tx(vec![add(json!(task),"learner-task/status",kw("learner-task.status/unlocked"))],f.now+300)?;
    assert!(attempt(&f.snapshot()?,f.learner).is_err());
    assert_eq!(base_xp::duration_base(360.0)?,6);
    assert_eq!(base_xp::duration_base(900.0)?,15);
    Ok(())
}

#[test]
fn selected_topic_review_uses_regular_policies_and_reuses_unfinished_attempts() -> Result<()> {
    for due in [false, true] {
        let mut f = Fixture::with_admission(due, 3*86400000, false)?;
        let before = f.snapshot()?;
        let topic = before.entities.with_attribute("topic/title").into_iter()
            .find(|topic| text(&before, *topic, "topic/title") == "Topic 0").unwrap();
        let existing: Vec<_> = before.refs(f.learner, "learner/activity")?.into_iter().filter(|task| {
            let activity = before.reference(*task, "learner-task/activity").unwrap();
            retrieval::kind(&before, activity).unwrap() == "review"
                && before.optional_ref(activity, "activity/scope").unwrap() == Some(topic)
                && matches!(status(&before, *task, "learner-task/status").unwrap().as_str(), "locked" | "unlocked")
        }).collect();
        let basis = f.db.basis_t();
        let available = topic_study_availability(&before, f.learner, topic, DateTime::from_timestamp_millis(f.now+100).unwrap());
        assert_eq!(available["review"]["available"], true);
        assert_eq!(available["review"]["resumable"], false);
        assert_eq!(f.db.basis_t(), basis);
        let mut s = f.act("review-topic", json!({"topicId":topic}), f.now+100)?;
        let available = topic_study_availability(&s, f.learner, topic, DateTime::from_timestamp_millis(f.now+150).unwrap());
        assert_eq!(available["review"]["available"], true);
        assert_eq!(available["review"]["resumable"], true);
        let task = s.refs(f.learner, "learner/activity")?.into_iter().find(|task| {
            status(&s, *task, "learner-task/status").unwrap() == "started"
        }).unwrap();
        if let Some(expected) = existing.first() { assert_eq!(task, *expected); }
        let activity = s.reference(task, "learner-task/activity")?;
        assert_eq!(retrieval::kind(&s, activity)?, "review");
        assert_eq!(s.reference(activity, "activity/scope")?, topic);
        assert_eq!(learning::lesson_steps(&s, activity)?.len(), 5);
        assert_eq!(number(&s, task, "learner-task/xp-base"), base_xp::activity_base(&s, activity)? as f64);
        for key in ["learner/course", "learner/queue", "learner/targets", "learner/self-directed"] {
            assert_eq!(before.entities[&f.learner].get(key), s.entities[&f.learner].get(key));
        }
        let count = s.refs(f.learner, "learner/activity")?.len();
        let item = items(&s, task)?[0];
        s = f.act("review-topic", json!({"topicId":topic}), f.now+200)?;
        assert_eq!(s.refs(f.learner, "learner/activity")?.len(), count);
        assert_eq!(items(&s, task)?, vec![item]);
        let paused = f.act("pause", json!({"taskId":task}), f.now+300)?;
        assert_eq!(topic_study_availability(&paused, f.learner, topic, DateTime::from_timestamp_millis(f.now+350).unwrap())["review"]["resumable"], true);
        s = f.act("review-topic", json!({"topicId":topic}), f.now+400)?;
        assert_eq!(status(&s, task, "learner-task/status")?, "started");
        assert_eq!(items(&s, task)?, vec![item]);
        let mut at = f.now+500;
        for _ in 0..3 {
            let item = *items(&s, task)?.last().unwrap();
            let question = s.reference(item, "task-item/content")?;
            let field = s.refs(question, "question/answer-fields")?[0];
            f.act("answer", json!({"taskId":task,"itemId":item,"responses":[{"fieldId":field,"value":"2"}]}), at)?;
            at+=100;
            s = f.act("continue", json!({"taskId":task,"itemId":item}), at)?;
            at+=100;
        }
        assert_eq!(status(&s, task, "learner-task/status")?, "completed");
        assert_eq!(items(&s, task)?.len(), 3);
        assert_eq!(number(&s, task, "learner-task/xp-earned"), retrieval::xp(&s, activity, &items(&s, task)?, base_xp::activity_base(&s, activity)?)? as f64);
    }
    Ok(())
}

#[test]
fn topic_menu_review_availability_explains_rejected_starts_without_writes() -> Result<()> {
    let f = Fixture::with_admission(false, 3*86400000, false)?;
    let original = f.snapshot()?;
    let topic = original.entities.with_attribute("topic/title").into_iter()
        .find(|topic| text(&original, *topic, "topic/title") == "Topic 0").unwrap();
    let at = DateTime::from_timestamp_millis(f.now+100).unwrap();
    for scenario in ["exhausted", "invalid"] {
        let mut s = original.clone();
        let mut selected = topic;
        if scenario == "invalid" { selected = f.learner; }
        else {
            for kp in s.refs(topic, "topic/knowledge-points")? {
                s.entities.get_mut(&kp).unwrap().insert("knowledge-point/questions".into(), json!([]));
            }
        }
        let s = EntitySnapshot::new(s.entities.into(), s.basis_t)?;
        let before = s.entities.clone();
        let view = topic_study_availability(&s, f.learner, selected, at);
        assert_eq!(view["review"]["available"], false, "{scenario}: {view}");
        assert!(!view["review"]["reason"].as_str().unwrap().is_empty());
        let error = mutate(&s, f.learner, "review-topic", &json!({"topicId":selected}), at).unwrap_err();
        assert_eq!(view["review"]["reason"], error.to_string());
        assert_eq!(s.entities, before);
    }
    Ok(())
}

#[test]
fn explicit_topic_reviews_ignore_unrelated_required_work_and_remain_resumable() -> Result<()> {
    for self_directed in [false, true] {
        let mut f = Fixture::new(false)?;
        f.tx(vec![add(json!(f.learner), "learner/self-directed", json!(self_directed))], f.now+10)?;
        let before = f.snapshot()?;
        let at = DateTime::from_timestamp_millis(f.now+100).unwrap();
        let required = learning::study_candidates(&before, f.learner, course(&before,f.learner)?, at)?;
        assert!(required.iter().any(|candidate|candidate.priority>=11000.0));
        let topic = before.entities.with_attribute("topic/title").into_iter()
            .find(|topic|text(&before,*topic,"topic/title")=="Topic 0").unwrap();
        let view = topic_study_availability(&before,f.learner,topic,at);
        assert_eq!(view["review"]["available"],true,"{view}");
        assert_eq!(f.snapshot()?.entities,before.entities);
        let started = f.act("review-topic",json!({"topicId":topic}),f.now+100)?;
        let task = started.refs(f.learner,"learner/activity")?.into_iter().find(|task| {
            let activity=started.reference(*task,"learner-task/activity").unwrap();
            retrieval::kind(&started,activity).unwrap()=="review"
                && started.optional_ref(activity,"activity/scope").unwrap()==Some(topic)
                && status(&started,*task,"learner-task/status").unwrap()=="started"
        }).unwrap();
        let presentations=items(&started,task)?;
        for (resume,offset) in [("review-topic",200),("resume",400)] {
            f.act("pause",json!({"taskId":task}),f.now+offset)?;
            let paused=f.snapshot()?;
            assert_eq!(topic_study_availability(&paused,f.learner,topic,DateTime::from_timestamp_millis(f.now+offset+50).unwrap())["review"]["available"],true);
            let resumed=f.act(resume,json!({"taskId":task,"topicId":topic}),f.now+offset+100)?;
            assert_eq!(status(&resumed,task,"learner-task/status")?,"started");
            assert_eq!(items(&resumed,task)?,presentations);
        }
        let after=f.snapshot()?;
        for candidate in required.iter().filter(|candidate|candidate.priority>=11000.0) {
            let required_task=task_for(&before,f.learner,candidate.activity)?.unwrap();
            assert_eq!(after.entity(required_task)?,before.entity(required_task)?);
        }
    }
    Ok(())
}

#[test]
fn manual_review_before_a_first_lesson_can_start_answer_and_complete() -> Result<()> {
    for missing_progress in [false, true] {
        let mut f = Fixture::with_admission(false,3*86400000,false)?;
        let snapshot=f.snapshot()?;
        let topic=snapshot.entities.with_attribute("topic/title").into_iter()
            .find(|topic|text(&snapshot,*topic,"topic/title")=="Topic 0").unwrap();
        let progress=snapshot.refs(f.learner,"learner/knowledge-profile")?.into_iter()
            .find(|progress|snapshot.optional_ref(*progress,"progress/topic").unwrap()==Some(topic)).unwrap();
        let mut forms=vec![];
        for task in snapshot.refs(f.learner,"learner/activity")? {
            let activity=snapshot.reference(task,"learner-task/activity")?;
            if snapshot.optional_ref(activity,"activity/scope")?==Some(topic) {
                forms.push(json!([kw("db/retract"),f.learner,kw("learner/activity"),task]));
            }
        }
        if missing_progress {
            forms.push(json!([kw("db/retract"),f.learner,kw("learner/knowledge-profile"),progress]));
        } else { forms.push(add(json!(progress),"progress/learned",json!(false))); }
        f.tx(forms,f.now+10)?;
        let before=f.snapshot()?;
        let view=topic_study_availability(&before,f.learner,topic,DateTime::from_timestamp_millis(f.now+20).unwrap());
        assert_eq!(view["review"]["available"],true,"{view}");
        assert_eq!(f.snapshot()?.entities,before.entities);
        let mut s=f.act("review-topic",json!({"topicId":topic}),f.now+100)?;
        let task=s.refs(f.learner,"learner/activity")?.into_iter().find(|task| {
            let activity=s.reference(*task,"learner-task/activity").unwrap();
            retrieval::kind(&s,activity).unwrap()=="review" && s.optional_ref(activity,"activity/scope").unwrap()==Some(topic)
        }).unwrap();
        assert_eq!(status(&s,task,"learner-task/status")?,"started");
        let mut at=f.now+200;
        for _ in 0..3 {
            let item=*items(&s,task)?.last().unwrap();
            let question=s.reference(item,"task-item/content")?;
            let field=s.refs(question,"question/answer-fields")?[0];
            f.act("answer",json!({"taskId":task,"itemId":item,"responses":[{"fieldId":field,"value":"2"}]}),at)?;
            at+=100;
            s=f.act("continue",json!({"taskId":task,"itemId":item}),at)?;
            at+=100;
        }
        assert_eq!(status(&s,task,"learner-task/status")?,"completed");
        assert_eq!(items(&s,task)?.len(),3);
    }
    Ok(())
}
