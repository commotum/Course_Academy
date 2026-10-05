//! Inspection reads: no task creation, response persistence, timing, or credit.

use super::*;

pub(super) fn home(s: &EntitySnapshot, learner: u64) -> Result<Json> {
    let activities = learning::study_candidates(s, learner, course(s, learner)?, Utc::now())?
        .into_iter()
        .take(5)
        .map(|candidate| {
            json!({
                "activityId": candidate.activity,
                "taskId": null,
                "title": text(s, candidate.activity, "activity/title"),
                "type": "lesson",
                "status": "preview",
                "priority": candidate.priority,
                "reason": candidate.reason,
                "targetCount": candidate.target_count,
                "targetTopics": candidate.target_topics,
                "expectedSeconds": null,
            })
        })
        .collect::<Vec<_>>();
    Ok(json!({
        "preview": true,
        "basis": s.basis_t,
        "learner": learner_json(s, learner),
        "course": course_json(s, learner)?,
        "activities": activities,
        "queueDescription": "Developer mode · inspect activities without recording work.",
        "practiceNotice": "Preview includes the complete captured question bank. Answers and navigation do not change your progress.",
    }))
}

pub(super) fn active_tasks(s: &EntitySnapshot, learner: u64) -> Result<Json> {
    let mut tasks = vec![];
    for task in s.refs(learner, "learner/activity")? {
        if status(s, task, "learner-task/status")? == "started" {
            tasks.push(task);
        }
    }
    Ok(json!({"taskIds": tasks}))
}

fn activity_id(s: &EntitySnapshot, learner: u64, body: &Json) -> Result<u64> {
    let from_task = if let Some(task) = body.get("taskId").filter(|v| !v.is_null()) {
        let task = task.as_u64().ok_or("Task ID must be an entity ID")?;
        owned(s, learner, task)?;
        Some(s.reference(task, "learner-task/activity")?)
    } else {
        None
    };
    let activity = body
        .get("activityId")
        .filter(|v| !v.is_null())
        .map(|v| v.as_u64().ok_or("Activity ID must be an entity ID"))
        .transpose()?
        .or(from_task)
        .ok_or("Activity or task ID required")?;
    if from_task.is_some_and(|id| id != activity) {
        return Err("Task does not reference this activity".into());
    }
    if !s.entity(activity)?.contains_key("activity/id") {
        return Err("Preview requires an activity definition".into());
    }
    Ok(activity)
}

fn answer(s: &EntitySnapshot, id: u64) -> Result<Json> {
    Ok(json!({"id": id, "type": status(s, id, "answer/type")?,
        "value": text(s, id, "answer/value"), "feedback": text(s, id, "answer/feedback")}))
}

fn fields(s: &EntitySnapshot, question: u64) -> Result<Vec<Json>> {
    let mut fields = vec![];
    for field in s.refs(question, "question/answer-fields")? {
        let kind = status(s, field, "answer-field/type")?;
        let choices = if kind == "blank" {
            vec![]
        } else {
            s.refs(field, "answer-field/choices")?
                .into_iter()
                .map(|id| answer(s, id))
                .collect::<Result<Vec<_>>>()?
        };
        fields.push(json!({
            "id": field, "key": text(s, field, "answer-field/key"),
            "type": kind, "choices": choices,
            "correctAnswer": s.optional_ref(field, "answer-field/correct")?
                .map(|id| answer(s, id)).transpose()?,
        }));
    }
    fields.sort_by(|a, b| a["key"].as_str().cmp(&b["key"].as_str()));
    Ok(fields)
}

/// Inspect every branch, including unvisited diagnostic branches. This is an
/// authored-content tour, not an execution of the learner's adaptive route.
fn ordered_steps(s: &EntitySnapshot, owner: u64, prefix: &str) -> Result<Vec<u64>> {
    let members: BTreeSet<_> = s
        .refs(owner, &format!("{prefix}/steps"))?
        .into_iter()
        .collect();
    let first = s.optional_ref(owner, &format!("{prefix}/first-step"))?;
    let mut pending = first.into_iter().collect::<Vec<_>>();
    let mut seen = BTreeSet::new();
    let mut result = vec![];
    while let Some(step) = pending.pop() {
        if !members.contains(&step) {
            return Err("Step continuation leaves its activity or multipart problem".into());
        }
        if !seen.insert(step) {
            continue;
        }
        result.push(step);
        for key in [
            "diagnostic-probe/on-silly-mistake",
            "diagnostic-probe/on-skipped",
            "diagnostic-probe/on-incorrect",
            "diagnostic-probe/on-correct",
            "step/next",
        ] {
            if let Some(next) = s.optional_ref(step, key)? {
                pending.push(next);
            }
        }
    }
    // Unconnected content still matters when inspecting an incomplete import.
    result.extend(members.difference(&seen).copied());
    Ok(result)
}

fn append_content(
    s: &EntitySnapshot,
    content: u64,
    step: u64,
    title: &str,
    contexts: &[String],
    ancestors: &mut BTreeSet<u64>,
    output: &mut Vec<Json>,
) -> Result<()> {
    if ancestors.len() >= 32 || !ancestors.insert(content) {
        return Err("Preview content nesting must be acyclic and at most 32 levels deep".into());
    }
    let record = s.entity(content)?;
    if record.contains_key("assigned-problem/id") {
        append_content(
            s,
            s.reference(content, "assigned-problem/content")?,
            step,
            title,
            contexts,
            ancestors,
            output,
        )?;
    } else if record.contains_key("multistep/id") {
        let mut contexts = contexts.to_vec();
        let context = text(s, content, "multistep/context");
        if !context.trim().is_empty() {
            contexts.push(context);
        }
        for inner in ordered_steps(s, content, "multistep")? {
            append_content(
                s,
                s.reference(inner, "step/content")?,
                inner,
                title,
                &contexts,
                ancestors,
                output,
            )?;
        }
    } else if record.contains_key("knowledge-point/id") {
        let title = text(s, content, "knowledge-point/title");
        let example = s.optional_ref(content, "knowledge-point/canonical-example")?;
        if let Some(example) = example {
            append_content(s, example, step, &title, contexts, ancestors, output)?;
        }
        let questions: BTreeSet<_> = s
            .refs(content, "knowledge-point/questions")?
            .into_iter()
            .collect();
        for question in questions {
            if Some(question) != example {
                append_content(s, question, step, &title, contexts, ancestors, output)?;
            }
        }
    } else if record.contains_key("tutorial/id") || record.contains_key("question/id") {
        let tutorial = record.contains_key("tutorial/id");
        let example = s.is_example(content);
        let kind = if tutorial {
            "tutorial"
        } else if example {
            "example"
        } else {
            "question"
        };
        let mut markdown = contexts.to_vec();
        markdown.push(text(
            s,
            content,
            if tutorial {
                "tutorial/content"
            } else {
                "question/problem"
            },
        ));
        let title = if tutorial {
            text(s, content, "tutorial/title")
        } else if !title.is_empty() {
            title.to_owned()
        } else if example {
            "Worked example".into()
        } else {
            "Practice".into()
        };
        output.push(json!({
            "preview": true, "itemId": null, "stepId": step, "contentId": content,
            "mathAcademyId": content_math_academy_id(record),
            "kind": kind, "title": title, "markdown": markdown.join("\n\n"),
            "fields": if tutorial { vec![] } else { fields(s, content)? },
            "solution": text(s, content, "question/worked-solution"),
            "requiresCalculator": record.get("question/requires-calculator"),
            "difficulty": s.optional_ref(content, "question/difficulty")?.map(|id| s.ident(&json!(id))).transpose()?,
            "status": "started", "canContinue": true, "elapsedSeconds": 0,
        }));
    } else {
        return Err("Unsupported content in activity preview".into());
    }
    ancestors.remove(&content);
    Ok(())
}

fn presentations(s: &EntitySnapshot, activity: u64) -> Result<Vec<Json>> {
    let mut output = vec![];
    for step in ordered_steps(s, activity, "activity")? {
        append_content(
            s,
            s.reference(step, "step/content")?,
            step,
            "",
            &[],
            &mut BTreeSet::new(),
            &mut output,
        )?;
    }
    Ok(output)
}

pub(super) fn preview(s: &EntitySnapshot, learner: u64, body: &Json) -> Result<Json> {
    let activity = activity_id(s, learner, body)?;
    Ok(json!({
        "preview": true, "basis": s.basis_t, "learner": learner_json(s, learner),
        "course": course_json(s, learner)?, "activityId": activity, "taskId": null,
        "activityUuid": schema::value_id_string(s.entity(activity)?.get("activity/id").ok_or("Missing activity identity")?)?,
        "title": text(s, activity, "activity/title"), "type": status(s, activity, "activity/type")?,
        "status": "preview", "elapsedSeconds": 0, "xp": 0, "xpBase": 0,
        "steps": presentations(s, activity)?,
    }))
}

pub(super) fn check_answer(s: &EntitySnapshot, learner: u64, body: &Json) -> Result<Json> {
    let activity = activity_id(s, learner, body)?;
    let question = required(body, "questionId")?;
    let mut presentation = presentations(s, activity)?
        .into_iter()
        .find(|p| p["contentId"].as_u64() == Some(question) && p["kind"] == "question")
        .ok_or("Question is not a practice question in this activity")?;
    let responses = body["responses"]
        .as_array()
        .ok_or("responses must be a list")?;
    let fields = s.refs(question, "question/answer-fields")?;
    let mut submitted = BTreeMap::new();
    let mut selected = BTreeMap::new();
    for response in responses {
        let field = required(response, "fieldId")?;
        if !fields.contains(&field) || submitted.contains_key(&field) {
            return Err("Each answer field must appear exactly once".into());
        }
        let (value, response) = if status(s, field, "answer-field/type")? == "blank" {
            let value = response["value"]
                .as_str()
                .ok_or("Blank response must contain a string value")?;
            let existing = s
                .refs(field, "answer-field/choices")?
                .into_iter()
                .find(|id| text(s, *id, "answer/value") == value);
            (
                value.to_owned(),
                json!({"value":value, "feedback":existing.map(|id|text(s,id,"answer/feedback")).unwrap_or_default()}),
            )
        } else {
            let choice = required(response, "choiceId")?;
            if !s.refs(field, "answer-field/choices")?.contains(&choice) {
                return Err("Choice does not belong to this field".into());
            }
            let mut response = answer(s, choice)?;
            response["choiceId"] = json!(choice);
            (choice.to_string(), response)
        };
        submitted.insert(field, value);
        selected.insert(field, response);
    }
    let correct = learning::grade(s, question, &submitted)?;
    for field in presentation["fields"].as_array_mut().unwrap() {
        field["response"] = selected.remove(&field["id"].as_u64().unwrap()).unwrap();
    }
    presentation["status"] = json!(if correct { "correct" } else { "incorrect" });
    presentation["basis"] = json!(s.basis_t);
    Ok(presentation)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> EntitySnapshot {
        let mut entries = BTreeMap::new();
        for (id, value) in [
            (
                1,
                json!({"learner/id":"preview-test","learner/course":2,"learner/activity":[30]}),
            ),
            (
                2,
                json!({"course/id":{"$uuid":"00000000-0000-0000-0000-000000000002"},"course/title":"Test course"}),
            ),
            (
                10,
                json!({"activity/id":"test","activity/type":"activity.type/lesson","activity/title":"Test lesson","activity/steps":[99,100],"activity/first-step":99}),
            ),
            (
                20,
                json!({"activity/id":"assignment","activity/type":"activity.type/assignment","activity/title":"Test assignment","activity/steps":[101],"activity/first-step":101}),
            ),
            (
                30,
                json!({"learner-task/activity":10,"learner-task/status":"learner-task.status/started"}),
            ),
            (99, json!({"step/content":201,"step/next":100})),
            (100, json!({"step/content":200})),
            (101, json!({"step/content":210})),
            (102, json!({"step/content":301})),
            (
                200,
                json!({"knowledge-point/id":"kp","knowledge-point/title":"Fractions","knowledge-point/canonical-example":300,"knowledge-point/questions":[301,302]}),
            ),
            (
                201,
                json!({"tutorial/id":"intro","tutorial/math-academy-id":123,"tutorial/title":"Introduction","tutorial/content":"Start here."}),
            ),
            (
                210,
                json!({"assigned-problem/id":"problem","assigned-problem/content":211}),
            ),
            (
                211,
                json!({"multistep/id":"parts","multistep/context":"Shared diagram and context.","multistep/steps":[102],"multistep/first-step":102}),
            ),
            (
                300,
                json!({"question/id":"example","question/math-academy-id":456,"question/problem":"Worked problem.","question/worked-solution":"Worked solution."}),
            ),
            (
                301,
                json!({"question/id":"practice","question/math-academy-id":789,"question/problem":"Enter one half.","question/answer-fields":[400],"question/worked-solution":"Divide one by two."}),
            ),
            (
                302,
                json!({"question/id":"unkeyed","question/problem":"Imported question awaiting a key."}),
            ),
            (
                400,
                json!({"answer-field/id":"field","answer-field/key":"half","answer-field/type":"answer-field.type/blank","answer-field/choices":[500],"answer-field/correct":500}),
            ),
            (
                500,
                json!({"answer/id":"half","answer/type":"answer.type/math","answer/value":"1/2","answer/feedback":"One of two equal parts."}),
            ),
        ] {
            entries.insert(id, value.as_object().unwrap().clone());
        }
        for (index, ident) in [
            "activity.type/lesson",
            "activity.type/assignment",
            "answer-field.type/blank",
            "answer.type/math",
            "learner-task.status/started",
        ]
        .iter()
        .enumerate()
        {
            entries.insert(
                1000 + index as u64,
                json!({"db/ident":kw(ident)}).as_object().unwrap().clone(),
            );
        }
        EntitySnapshot::new(entries, 42).unwrap()
    }

    #[test]
    fn preview_includes_complete_bank_without_creating_a_task_or_requiring_keys() {
        let s = fixture();
        let before = s.entities.clone();
        let view = preview(&s, 1, &json!({"taskId":30})).unwrap();
        assert_eq!(view["steps"].as_array().unwrap().len(), 4);
        assert_eq!(view["steps"][0]["kind"], "tutorial");
        assert_eq!(view["steps"][1]["kind"], "example");
        assert_eq!(view["steps"][0]["mathAcademyId"], "123");
        assert_eq!(view["steps"][1]["mathAcademyId"], "456");
        assert_eq!(view["steps"][2]["mathAcademyId"], "789");
        assert!(view["steps"][3]["mathAcademyId"].is_null());
        assert_eq!(view["steps"][3]["contentId"], 302);
        assert_eq!(
            view["steps"][2]["fields"][0]["correctAnswer"]["value"],
            "1/2"
        );
        assert!(view["taskId"].is_null());
        assert_eq!(view["elapsedSeconds"], 0);
        assert_eq!(active_tasks(&s, 1).unwrap()["taskIds"], json!([30]));
        assert!(preview(&s, 1, &json!({"activityId":20,"taskId":30})).is_err());
        assert_eq!(s.entities, before);
        assert!(s.status_history.is_empty());
    }

    #[test]
    fn preview_preserves_assignment_shared_context() {
        let s = fixture();
        let view = preview(&s, 1, &json!({"activityId":20})).unwrap();
        assert_eq!(
            view["steps"][0]["markdown"],
            "Shared diagram and context.\n\nEnter one half."
        );
        assert_eq!(view["steps"][0]["stepId"], 102);
    }

    #[test]
    fn preview_grading_uses_normal_grader_without_storing_entered_values() {
        let s = fixture();
        let before = s.entities.clone();
        let result = check_answer(
            &s,
            1,
            &json!({"activityId":10,"questionId":301,"responses":[{"fieldId":400,"value":"0.5"}]}),
        )
        .unwrap();
        assert_eq!(result["status"], "correct");
        assert_eq!(result["fields"][0]["response"]["value"], "0.5");
        assert_eq!(result["solution"], "Divide one by two.");
        let wrong = check_answer(
            &s,
            1,
            &json!({"activityId":10,"questionId":301,"responses":[{"fieldId":400,"value":"0.4"}]}),
        )
        .unwrap();
        assert_eq!(wrong["status"], "incorrect");
        assert!(
            check_answer(
                &s,
                1,
                &json!({"activityId":20,"questionId":302,"responses":[]})
            )
            .is_err()
        );
        assert_eq!(s.entities, before);
        assert_eq!(s.basis_t, 42);
    }
}
