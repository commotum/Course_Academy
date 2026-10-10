//! Offline native transactions: these tests never connect to the durable database.
use super::*;
use edb_core::Database;

const ASSIGNMENT: &str = "00000000-0000-4000-8000-000000000010";

struct Fixture {
    db: Database,
    learner: u64,
    activity: u64,
    first: u64,
    second: u64,
    first_field: u64,
    second_field: u64,
    right: u64,
    lesson_task: u64,
    lesson_item: u64,
    progress: u64,
}

impl Fixture {
    fn new() -> Result<Self> {
        let mut db = Database::bootstrap()?;
        for (index, schema) in [
            include_str!("../schema/data/2-course.edn"),
            include_str!("../schema/data/5-1-topic.edn"),
            include_str!("../schema/content/0-activity.edn"),
            include_str!("../schema/content/1-step.edn"),
            include_str!("../schema/content/2-tutorial.edn"),
            include_str!("../schema/content/4-question.edn"),
            include_str!("../schema/content/5-answer-field.edn"),
            include_str!("../schema/content/6-answer.edn"),
            include_str!("../schema/content/7-multistep.edn"),
            include_str!("../schema/content/8-assigned-problem.edn"),
            include_str!("../schema/learner/1-1-learner.edn"),
            include_str!("../schema/learner/1-3-learner-progress.edn"),
            include_str!("../schema/learner/2-1-learner-task.edn"),
            include_str!("../schema/learner/2-2-learner-task-item.edn"),
        ]
        .into_iter()
        .enumerate()
        {
            db = db.with_edn(schema, index as i64 + 1)?.db_after;
        }
        let report = db.with_edn(r#"[
          {:db/id "course" :course/id #uuid "00000000-0000-4000-8000-000000000001" :course/title "Test course"}
          {:db/id "topic" :topic/id #uuid "00000000-0000-4000-8000-000000000002" :topic/title "Preserved topic"}
          {:db/id "progress" :progress/id "assignment-test-progress" :progress/topic "topic" :progress/repetitions 2.0}
          {:db/id "learner" :learner/id "assignment-test-learner" :learner/course "course" :learner/assignments ["assignment"] :learner/activity ["lesson-task"] :learner/knowledge-profile ["progress"]}
          {:db/id "assignment" :activity/id #uuid "00000000-0000-4000-8000-000000000010" :activity/type :activity.type/assignment :activity/title "Test assignment" :activity/steps ["first" "second"] :activity/first-step "first"}
          {:db/id "first" :step/id #uuid "00000000-0000-4000-8000-000000000011" :step/content "question-one" :step/next "second"}
          {:db/id "second" :step/id #uuid "00000000-0000-4000-8000-000000000012" :step/content "question-two"}
          {:db/id "question-one" :question/id #uuid "00000000-0000-4000-8000-000000000013" :question/problem "Enter two." :question/worked-solution "One plus one is two." :question/answer-fields ["first-field"]}
          {:db/id "first-field" :answer-field/id #uuid "00000000-0000-4000-8000-000000000014" :answer-field/type :answer-field.type/blank :answer-field/key "answer" :answer-field/choices ["two"] :answer-field/correct "two"}
          {:db/id "two" :answer/id #uuid "00000000-0000-4000-8000-000000000015" :answer/type :answer.type/math :answer/value "2" :answer/feedback "Two is correct."}
          {:db/id "question-two" :question/id #uuid "00000000-0000-4000-8000-000000000016" :question/problem "Select four." :question/worked-solution "Two plus two is four." :question/answer-fields ["second-field"]}
          {:db/id "second-field" :answer-field/id #uuid "00000000-0000-4000-8000-000000000017" :answer-field/type :answer-field.type/select :answer-field/key "selection" :answer-field/choices ["right" "wrong"] :answer-field/correct "right"}
          {:db/id "right" :answer/id #uuid "00000000-0000-4000-8000-000000000018" :answer/type :answer.type/text :answer/value "four"}
          {:db/id "wrong" :answer/id #uuid "00000000-0000-4000-8000-000000000019" :answer/type :answer.type/text :answer/value "five"}
          {:db/id "lesson" :activity/id #uuid "00000000-0000-4000-8000-000000000020" :activity/type :activity.type/lesson :activity/title "Preserved lesson" :activity/scope "topic" :activity/steps ["lesson-step"] :activity/first-step "lesson-step"}
          {:db/id "lesson-step" :step/id #uuid "00000000-0000-4000-8000-000000000021" :step/content "tutorial"}
          {:db/id "tutorial" :tutorial/id #uuid "00000000-0000-4000-8000-000000000022" :tutorial/title "Read" :tutorial/content "Keep this lesson."}
          {:db/id "lesson-task" :learner-task/id #uuid "00000000-0000-4000-8000-000000000023" :learner-task/activity "lesson" :learner-task/status :learner-task.status/started :learner-task/priority 5.0 :learner-task/xp-base 12 :learner-task/items ["lesson-item"]}
          {:db/id "lesson-item" :task-item/id #uuid "00000000-0000-4000-8000-000000000024" :task-item/content "tutorial" :task-item/status :task-item.status/started :task-item/elapsed-seconds 0.0}
        ]"#, 1000)?;
        let id = |name: &str| *report.tempids.get(name).unwrap();
        Ok(Self {
            learner: id("learner"),
            activity: id("assignment"),
            first: id("first"),
            second: id("second"),
            first_field: id("first-field"),
            second_field: id("second-field"),
            right: id("right"),
            lesson_task: id("lesson-task"),
            lesson_item: id("lesson-item"),
            progress: id("progress"),
            db: report.db_after,
        })
    }

    fn snapshot(&self) -> Result<EntitySnapshot> {
        snapshot(&self.db.database_value())
    }

    fn act(&mut self, action: &str, mut body: Json, millis: i64) -> Result<EntitySnapshot> {
        body["assignmentId"] = json!(ASSIGNMENT);
        let s = self.snapshot()?;
        let (forms, _) = mutate(
            &s,
            self.learner,
            action,
            &body,
            DateTime::from_timestamp_millis(millis).unwrap(),
        )?;
        if !forms.is_empty() {
            self.db = self
                .db
                .with_edn(&schema::edn(&json!(forms))?, millis)?
                .db_after;
        }
        self.snapshot()
    }

    fn focus(&mut self, step: u64, millis: i64) -> Result<EntitySnapshot> {
        self.act("assignment-focus", json!({"stepId":step}), millis)
    }
}

#[test]
fn profile_settings_validate_and_pause_a_lesson_atomically() -> Result<()> {
    let mut f = Fixture::new()?;
    let current = "00000000-0000-4000-8000-000000000001";
    let other = "00000000-0000-4000-8000-000000000030";
    f.db =
        f.db.with_edn(
            &format!(
                r#"[{{:db/id "other" :course/id #uuid "{other}" :course/title "Other course"}}]"#
            ),
            1500,
        )?
        .db_after;
    let s = f.snapshot()?;
    let at = DateTime::from_timestamp_millis(3000).unwrap();
    let plan = |body: Json| super::super::mutate(&s, f.learner, "profile-settings", &body, at);
    assert!(plan(json!({"courseId":"missing","selfDirected":true})).is_err());
    assert!(plan(json!({"courseId":other,"selfDirected":"true"})).is_err());
    assert!(
        plan(json!({"courseId":current,"selfDirected":false}))?
            .0
            .is_empty()
    );
    let (forms, _) = plan(json!({"courseId":other,"selfDirected":true}))?;
    f.db = f.db.with_edn(&schema::edn(&json!(forms))?, 3000)?.db_after;
    let saved = f.snapshot()?;
    let profile = super::super::profile_json(&saved, f.learner)?;
    assert_eq!(profile["course"]["id"], other);
    assert_eq!(profile["learner"]["selfDirected"], true);
    assert_eq!(profile["courses"].as_array().unwrap().len(), 2);
    assert_eq!(
        status(&saved, f.lesson_task, "learner-task/status")?,
        "paused"
    );
    assert_eq!(status(&saved, f.lesson_item, "task-item/status")?, "paused");
    assert_eq!(
        number(&saved, f.lesson_item, "task-item/elapsed-seconds"),
        2.0
    );
    assert_eq!(saved.entity(f.progress)?, s.entity(f.progress)?);
    Ok(())
}

#[test]
fn study_course_projects_reverse_group_membership_without_level_schema() -> Result<()> {
    let mut f = Fixture::new()?;
    f.db =
        f.db.with_edn(include_str!("../schema/data/1-1-course-group.edn"), 1500)?
            .db_after;
    f.db = f.db.with_edn(r#"[
      {:course-group/id #uuid "00000000-0000-4000-8000-000000000050" :course-group/title "University"
       :course-group/courses [[:course/id #uuid "00000000-0000-4000-8000-000000000001"]]}
      {:course-group/id #uuid "00000000-0000-4000-8000-000000000051" :course-group/title "Advanced Placement"
       :course-group/courses [[:course/id #uuid "00000000-0000-4000-8000-000000000001"]]}
    ]"#, 2000)?.db_after;
    let view = super::super::course_json(&f.snapshot()?, f.learner)?;
    assert!(view.get("level").is_none());
    let groups = view["groups"].as_array().unwrap();
    assert_eq!(groups.len(), 2);
    assert_eq!(groups[0]["title"], "Advanced Placement");
    assert_eq!(groups[1]["title"], "University");
    Ok(())
}

#[test]
fn profile_settings_pause_assignment_timing_and_preserve_work() -> Result<()> {
    let mut f = Fixture::new()?;
    let s = f.focus(f.first, 2000)?;
    let task = task_for(&s, f.learner, f.activity)?.unwrap();
    let before_items = items(&s, task)?;
    let (forms, _) = super::super::mutate(
        &s,
        f.learner,
        "profile-settings",
        &json!({"courseId":"00000000-0000-4000-8000-000000000001","selfDirected":true}),
        DateTime::from_timestamp_millis(4000).unwrap(),
    )?;
    f.db = f.db.with_edn(&schema::edn(&json!(forms))?, 4000)?.db_after;
    let saved = f.snapshot()?;
    assert_eq!(items(&saved, task)?, before_items);
    assert_eq!(status(&saved, task, "learner-task/status")?, "paused");
    assert_eq!(
        status(&saved, before_items[0], "task-item/status")?,
        "paused"
    );
    assert_eq!(
        number(&saved, before_items[0], "task-item/elapsed-seconds"),
        2.0
    );
    Ok(())
}

#[test]
fn assignment_switches_clocks_without_reordering_or_crediting_lessons() -> Result<()> {
    let mut f = Fixture::new()?;
    let original = f.snapshot()?;
    let progress = original.entity(f.progress)?.clone();
    let s = f.focus(f.first, 2000)?;
    let task = task_for(&s, f.learner, f.activity)?.unwrap();
    let first = timing::active_item(&s, f.learner)?.unwrap();
    assert_eq!(status(&s, f.lesson_task, "learner-task/status")?, "paused");
    assert_eq!(number(&s, f.lesson_item, "task-item/elapsed-seconds"), 1.0);
    assert_eq!(number(&s, f.lesson_task, "learner-task/priority"), 5.0);
    let s = f.focus(f.second, 3000)?;
    let second = timing::active_item(&s, f.learner)?.unwrap();
    assert_ne!(first, second);
    let s = f.focus(f.first, 4000)?;
    assert_eq!(timing::active_item(&s, f.learner)?, Some(first));
    assert_eq!(items(&s, task)?, vec![first, second]);
    // Developer-mode enabling uses the ordinary pause action, without an assignment ID.
    let (forms, result) = super::super::mutate(
        &s,
        f.learner,
        "pause",
        &json!({"taskId":task}),
        DateTime::from_timestamp_millis(5000).unwrap(),
    )?;
    assert_eq!(result["assignmentId"], ASSIGNMENT);
    f.db = f.db.with_edn(&schema::edn(&json!(forms))?, 5000)?.db_after;
    let s = f.snapshot()?;
    assert_eq!(timing::active_item(&s, f.learner)?, None);
    assert_eq!(
        timing::task_elapsed(&s, task, DateTime::from_timestamp_millis(6999).unwrap())?,
        3.0
    );
    f.focus(f.first, 7000)?;
    let s = f.act(
        "assignment-answer",
        json!({"itemId":first,"responses":[{"fieldId":f.first_field,"value":"2.0"}]}),
        8000,
    )?;
    assert_eq!(status(&s, first, "task-item/status")?, "correct");
    assert_eq!(status(&s, task, "learner-task/status")?, "paused");
    assert_eq!(number(&s, first, "task-item/elapsed-seconds"), 3.0);
    assert_eq!(number(&s, task, "learner-task/elapsed-seconds"), 4.0);
    assert_eq!(timing::active_item(&s, f.learner)?, None);
    let saved = s.entity(first)?.clone();
    let basis = f.db.basis_t();
    let s = f.act(
        "assignment-answer",
        json!({"itemId":first,"responses":[{"fieldId":f.first_field,"value":"99"}]}),
        8500,
    )?;
    assert_eq!(
        f.db.basis_t(),
        basis,
        "an answered occurrence is immutable under a fresh request"
    );
    assert_eq!(s.entity(first)?, &saved);
    f.focus(f.second, 9000)?;
    let s = f.act(
        "assignment-answer",
        json!({"itemId":second,"responses":[{"fieldId":f.second_field,"choiceId":f.right}]}),
        10000,
    )?;
    assert_eq!(status(&s, task, "learner-task/status")?, "completed");
    assert_eq!(number(&s, task, "learner-task/elapsed-seconds"), 5.0);
    assert_eq!(items(&s, task)?, vec![first, second]);
    assert_eq!(s.entity(f.progress)?, &progress);
    assert_eq!(
        s.refs(f.learner, "learner/knowledge-profile")?,
        vec![f.progress]
    );
    assert_eq!(s.optional_ref(f.learner, "learner/performance")?, None);
    assert!(!s.entity(task)?.contains_key("learner-task/xp-earned"));
    assert!(!s.entity(task)?.contains_key("learner-task/xp-base"));
    assert_eq!(status(&s, f.lesson_task, "learner-task/status")?, "paused");
    assert!(
        s.refs(f.learner, "learner/activity")?
            .contains(&f.lesson_task)
    );
    let members = s.refs(f.learner, "learner/activity")?;
    let queue = queue_forms(
        &s,
        f.learner,
        DateTime::from_timestamp_millis(10001).unwrap(),
    )?;
    if !queue.is_empty() {
        f.db = f.db.with_edn(&schema::edn(&json!(queue))?, 10001)?.db_after;
    }
    let s = f.snapshot()?;
    assert_eq!(s.refs(f.learner, "learner/activity")?, members);
    assert_eq!(status(&s, f.lesson_task, "learner-task/status")?, "paused");
    assert_eq!(s.entity(f.progress)?, &progress);
    Ok(())
}

#[test]
fn assignment_reveals_only_saved_or_preview_answers_and_keeps_blanks_private() -> Result<()> {
    let mut f = Fixture::new()?;
    let s = f.snapshot()?;
    let detail = assignment_reader::detail(&s, f.learner, ASSIGNMENT)?;
    let first = &detail["assignment"]["steps"][0]["content"];
    assert_eq!(first["gradable"], true);
    assert!(first.get("solution").is_none());
    assert!(first["fields"][0].get("correctAnswer").is_none());
    assert!(first["fields"][0]["choices"].as_array().unwrap().is_empty());
    let preview = assignment_reader::detail_mode(&s, f.learner, ASSIGNMENT, true)?;
    assert_eq!(
        preview["assignment"]["steps"][0]["content"]["fields"][0]["correctAnswer"]["value"],
        "2"
    );
    let s = f.focus(f.first, 2000)?;
    let item = timing::active_item(&s, f.learner)?.unwrap();
    let s = f.act(
        "assignment-answer",
        json!({"itemId":item,"responses":[{"fieldId":f.first_field,"value":"3"}]}),
        3000,
    )?;
    let detail = assignment_reader::detail(&s, f.learner, ASSIGNMENT)?;
    let first = &detail["assignment"]["steps"][0]["content"];
    assert_eq!(first["status"], "incorrect");
    assert_eq!(first["fields"][0]["response"]["value"], "3");
    assert_eq!(first["fields"][0]["correctAnswer"]["value"], "2");
    assert_eq!(first["solution"], "One plus one is two.");
    assert!(first["fields"][0]["choices"].as_array().unwrap().is_empty());
    assert!(
        detail["assignment"]["steps"][1]["content"]
            .get("solution")
            .is_none()
    );
    Ok(())
}

#[test]
fn assignment_rejects_incomplete_foreign_and_paused_submissions_without_writes() -> Result<()> {
    let mut f = Fixture::new()?;
    let before = f.db.basis_t();
    assert!(
        f.act(
            "assignment-focus",
            json!({"stepId":f.first,"preview":true}),
            1500
        )
        .is_err()
    );
    assert!(f.focus(f.lesson_item, 1500).is_err());
    assert_eq!(f.db.basis_t(), before);
    let s = f.focus(f.first, 2000)?;
    let first = timing::active_item(&s, f.learner)?.unwrap();
    let before = f.db.basis_t();
    for body in [
        json!({"itemId":f.lesson_item,"responses":[]}),
        json!({"itemId":first,"responses":[]}),
        json!({"itemId":first,"responses":[{"fieldId":f.second_field,"choiceId":f.right}]}),
        json!({"itemId":first,"responses":[{"fieldId":f.first_field,"value":"2"},{"fieldId":f.first_field,"value":"2"}]}),
    ] {
        assert!(f.act("assignment-answer", body, 2500).is_err());
        assert_eq!(f.db.basis_t(), before);
    }
    f.focus(f.second, 3000)?;
    assert!(
        f.act(
            "assignment-answer",
            json!({"itemId":first,"responses":[{"fieldId":f.first_field,"value":"2"}]}),
            3500
        )
        .is_err()
    );
    let s = f.snapshot()?;
    let question = s.reference(f.first, "step/content")?;
    f.db =
        f.db.with_edn(
            &format!(
                "[[:db/retract {question} :question/answer-fields {}]]",
                f.first_field
            ),
            4000,
        )?
        .db_after;
    let before = f.db.basis_t();
    assert!(f.focus(f.first, 5000).is_err());
    assert_eq!(f.db.basis_t(), before);
    let detail = assignment_reader::detail(&f.snapshot()?, f.learner, ASSIGNMENT)?;
    assert_eq!(
        detail["assignment"]["steps"][0]["content"]["gradable"],
        false
    );
    assert_eq!(detail["assignment"]["steps"].as_array().unwrap().len(), 2);
    Ok(())
}

#[test]
fn assignment_repeated_question_steps_have_distinct_owned_presentations() -> Result<()> {
    let mut f = Fixture::new()?;
    let s = f.snapshot()?;
    let question = s.reference(f.first, "step/content")?;
    f.db =
        f.db.with_edn(
            &format!("[[:db/add {} :step/content {question}]]", f.second),
            1500,
        )?
        .db_after;
    let s = f.focus(f.first, 2000)?;
    let task = task_for(&s, f.learner, f.activity)?.unwrap();
    let first = timing::active_item(&s, f.learner)?.unwrap();
    let s = f.focus(f.second, 3000)?;
    let second = timing::active_item(&s, f.learner)?.unwrap();
    assert_ne!(first, second);
    assert_ne!(
        s.entity(first)?["task-item/id"],
        s.entity(second)?["task-item/id"]
    );
    assert_eq!(
        s.reference(first, "task-item/content")?,
        s.reference(second, "task-item/content")?
    );
    let s = f.focus(f.first, 4000)?;
    assert_eq!(items(&s, task)?, vec![first, second]);
    assert_eq!(item_map(&s, task, &occurrences(&s, f.activity)?)?.len(), 2);
    let mut foreign_link = s.clone();
    foreign_link
        .entities
        .get_mut(&second)
        .unwrap()
        .insert("task-item/next".into(), json!(f.lesson_item));
    assert!(item_map(&foreign_link, task, &occurrences(&s, f.activity)?).is_err());
    let mut wrong_content = s.clone();
    wrong_content
        .entities
        .get_mut(&first)
        .unwrap()
        .insert("task-item/content".into(), json!(f.lesson_item));
    assert!(item_map(&wrong_content, task, &occurrences(&s, f.activity)?).is_err());
    Ok(())
}
