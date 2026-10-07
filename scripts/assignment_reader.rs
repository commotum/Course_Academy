//! Complete schoolwork projection from the same EDB basis as the learner.
//! Reading never creates presentations, starts clocks, or awards credit.

use super::*;

pub(super) fn identity(s: &EntitySnapshot, eid: u64, attr: &str) -> Result<String> {
    Ok(schema::value_id_string(
        s.entity(eid)?
            .get(attr)
            .ok_or_else(|| format!("Missing {attr}"))?,
    )?)
}

fn topic(s: &EntitySnapshot, eid: u64) -> Result<Json> {
    Ok(json!({
        "id": eid,
        "uuid": identity(s, eid, "topic/id")?,
        "mathAcademyId": s.entity(eid)?.get("topic/math-academy-id"),
        "title": text(s, eid, "topic/title"),
    }))
}

pub(super) fn ordered_steps(s: &EntitySnapshot, owner: u64, prefix: &str) -> Result<Vec<u64>> {
    let members: BTreeSet<_> = s
        .refs(owner, &format!("{prefix}/steps"))?
        .into_iter()
        .collect();
    let mut cursor = s.optional_ref(owner, &format!("{prefix}/first-step"))?;
    let mut seen = BTreeSet::new();
    let mut result = vec![];
    while let Some(step) = cursor {
        if !members.contains(&step) || !seen.insert(step) {
            return Err("Assignment steps must form one acyclic owned route".into());
        }
        result.push(step);
        cursor = s.optional_ref(step, "step/next")?;
    }
    if seen != members {
        return Err("Assignment contains unreachable steps".into());
    }
    Ok(result)
}

fn fields(s: &EntitySnapshot, question: u64) -> Result<Vec<Json>> {
    let mut fields = vec![];
    for field in s.refs(question, "question/answer-fields")? {
        let kind = status(s, field, "answer-field/type")?;
        if !matches!(kind.as_str(), "radio" | "select" | "blank") {
            return Err("Unsupported assignment answer field type".into());
        }
        let mut choices = vec![];
        // A blank's choice collection includes its canonical and observed
        // learner values. Neither belongs in a read-only problem display.
        if kind != "blank" {
            for answer in s.refs(field, "answer-field/choices")? {
                choices.push(json!({
                    "id": identity(s, answer, "answer/id")?,
                    "entityId": answer,
                    "type": status(s, answer, "answer/type")?,
                    "value": text(s, answer, "answer/value"),
                }));
            }
        }
        fields.push(json!({
            "id": identity(s, field, "answer-field/id")?,
            "entityId": field,
            "key": text(s, field, "answer-field/key"),
            "type": kind, "presentation": text(s, field, "answer-field/presentation"),
            "answerType": s.optional_ref(field, "answer-field/correct")?
                .map(|id| status(s, id, "answer/type")).transpose()?,
            "choices": choices,
        }));
    }
    fields.sort_by(|a, b| a["key"].as_str().cmp(&b["key"].as_str()));
    Ok(fields)
}

#[derive(Default)]
struct Contents {
    problem_count: usize,
    question_count: usize,
    topics: BTreeSet<u64>,
}

fn steps(
    s: &EntitySnapshot,
    owner: u64,
    prefix: &str,
    ancestors: &mut BTreeSet<u64>,
    summary: &mut Contents,
) -> Result<Vec<Json>> {
    let mut result = vec![];
    for step in ordered_steps(s, owner, prefix)? {
        let content = s.reference(step, "step/content")?;
        result.push(json!({
            "id": identity(s, step, "step/id")?,
            "entityId": step,
            "expectedSeconds": s.entity(step)?.get("step/expected-seconds"),
            "content": content_json(s, content, ancestors, summary)?,
        }));
    }
    Ok(result)
}

fn content_json(
    s: &EntitySnapshot,
    eid: u64,
    ancestors: &mut BTreeSet<u64>,
    summary: &mut Contents,
) -> Result<Json> {
    if ancestors.len() >= 32 || !ancestors.insert(eid) {
        return Err("Assignment content nesting must be acyclic and at most 32 levels deep".into());
    }
    let record = s.entity(eid)?;
    let content = if record.contains_key("assigned-problem/id") {
        summary.problem_count += 1;
        let coverage = s.refs(eid, "assigned-problem/topic-coverage")?;
        summary.topics.extend(coverage.iter().copied());
        let mut topic_coverage = coverage
            .into_iter()
            .map(|eid| topic(s, eid))
            .collect::<Result<Vec<_>>>()?;
        topic_coverage.sort_by(|a, b| a["title"].as_str().cmp(&b["title"].as_str()));
        let inner = s.reference(eid, "assigned-problem/content")?;
        let inner_record = s.entity(inner)?;
        if !inner_record.contains_key("question/id") && !inner_record.contains_key("multistep/id") {
            return Err("Assigned problem must reference a question or multipart problem".into());
        }
        json!({
            "kind": "assigned-problem",
            "id": identity(s, eid, "assigned-problem/id")?,
            "entityId": eid,
            "topicCoverage": topic_coverage,
            "content": content_json(s, inner, ancestors, summary)?,
        })
    } else if record.contains_key("multistep/id") {
        json!({
            "kind": "multistep",
            "id": identity(s, eid, "multistep/id")?,
            "entityId": eid,
            "context": text(s, eid, "multistep/context"),
            "steps": steps(s, eid, "multistep", ancestors, summary)?,
        })
    } else if record.contains_key("question/id") {
        summary.question_count += 1;
        json!({
            "kind": "question",
            "id": identity(s, eid, "question/id")?,
            "entityId": eid,
            "problem": text(s, eid, "question/problem"),
            "isExample": s.is_example(eid),
            "requiresCalculator": record.get("question/requires-calculator"),
            "difficulty": s.optional_ref(eid, "question/difficulty")?.map(|v| s.ident(&json!(v))).transpose()?,
            "fields": fields(s, eid)?,
        })
    } else if record.contains_key("tutorial/id") {
        json!({
            "kind": "tutorial",
            "id": identity(s, eid, "tutorial/id")?,
            "entityId": eid,
            "title": text(s, eid, "tutorial/title"),
            "content": text(s, eid, "tutorial/content"),
        })
    } else {
        return Err("Unsupported assignment content".into());
    };
    ancestors.remove(&eid);
    Ok(content)
}

pub(super) fn assigned(s: &EntitySnapshot, learner: u64) -> Result<Vec<u64>> {
    let assignments = s.refs(learner, "learner/assignments")?;
    for &activity in &assignments {
        if status(s, activity, "activity/type")? != "assignment" {
            return Err("Learner assignments must reference assignment activities".into());
        }
    }
    Ok(assignments)
}

fn assignment(s: &EntitySnapshot, learner: u64, activity: u64, detail: bool) -> Result<Json> {
    let mut summary = Contents::default();
    let route = steps(s, activity, "activity", &mut BTreeSet::new(), &mut summary)?;
    let due = s
        .entity(activity)?
        .get("activity/due")
        .map(schema::parse_instant)
        .transpose()?;
    // Prefer the latest real status assertion. Merely opening this view never
    // manufactures a status, task, answer, or learner timing record.
    let task = super::assignment_interaction::latest_task(s, learner, activity)?;
    let course = s
        .optional_ref(activity, "activity/course")?
        .map(|course| -> Result<Json> {
            Ok(json!({
                "id": identity(s, course, "course/id")?,
                "entityId": course,
                "title": text(s, course, "course/title"),
            }))
        })
        .transpose()?;
    let mut value = json!({
        "id": identity(s, activity, "activity/id")?,
        "entityId": activity,
        "title": text(s, activity, "activity/title"),
        "course": course,
        "due": due.map(|at| at.to_rfc3339_opts(chrono::SecondsFormat::Millis, true)),
        "problemCount": summary.problem_count,
        "questionCount": summary.question_count,
        "topics": summary.topics.into_iter().map(|eid| topic(s, eid)).collect::<Result<Vec<_>>>()?,
        "status": task.map(|task| status(s, task, "learner-task/status")).transpose()?,
        "taskId": task,
        "expectedSeconds": s.entity(activity)?.get("activity/expected-seconds"),
    });
    if detail {
        value["steps"] = json!(route);
    }
    Ok(value)
}

pub(super) fn list(s: &EntitySnapshot, learner: u64) -> Result<Json> {
    let mut assignments = assigned(s, learner)?
        .into_iter()
        .map(|activity| assignment(s, learner, activity, false))
        .collect::<Result<Vec<_>>>()?;
    assignments.sort_by(|a, b| {
        let key = |v: &Json| {
            (
                v["status"].as_str() == Some("completed"),
                v["due"].is_null(),
                v["due"].as_str().unwrap_or("").to_owned(),
                v["title"].as_str().unwrap_or("").to_owned(),
                v["id"].as_str().unwrap_or("").to_owned(),
            )
        };
        key(a).cmp(&key(b))
    });
    Ok(json!({
        "basis": s.basis_t,
        "learner": learner_json(s, learner),
        "course": course_json(s, learner)?,
        "assignments": assignments,
    }))
}

pub(super) fn resolve(s: &EntitySnapshot, learner: u64, selector: &str) -> Result<u64> {
    assigned(s, learner)?
        .into_iter()
        .find(|activity| identity(s, *activity, "activity/id").ok().as_deref() == Some(selector))
        .ok_or_else(|| "Assignment not found for this learner".into())
}

pub(super) fn detail(s: &EntitySnapshot, learner: u64, selector: &str) -> Result<Json> {
    detail_mode(s, learner, selector, false)
}

pub(super) fn detail_mode(
    s: &EntitySnapshot,
    learner: u64,
    selector: &str,
    preview: bool,
) -> Result<Json> {
    let activity = resolve(s, learner, selector)?;
    let mut assignment = assignment(s, learner, activity, true)?;
    super::assignment_interaction::enrich(s, &mut assignment, preview)?;
    Ok(json!({
        "preview": preview,
        "basis": s.basis_t,
        "learner": learner_json(s, learner),
        "course": course_json(s, learner)?,
        "assignment": assignment,
    }))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> EntitySnapshot {
        EntitySnapshot::from_json(&json!({"basis_t": 7, "entities": {
            "1": {"learner/id":"learner", "learner/course":2, "learner/assignments":[10,11,12]},
            "2": {"course/id":{"$uuid":"course"}, "course/title":"Math"},
            "3": {"db/ident":"activity.type/assignment"},
            "4": {"db/ident":"answer-field.type/blank"},
            "5": {"db/ident":"answer.type/text"},
            "6": {"course/id":{"$uuid":"science"}, "course/title":"Science"},
            "10": {"activity/id":{"$uuid":"later"}, "activity/type":3, "activity/title":"Later", "activity/course":2, "activity/due":{"$instant":"2026-10-05T23:59:59-07:00"}, "activity/steps":[20], "activity/first-step":20},
            "11": {"activity/id":{"$uuid":"earlier"}, "activity/type":3, "activity/title":"Earlier", "activity/course":6, "activity/due":{"$instant":"2026-10-02T23:59:59-07:00"}, "activity/steps":[21], "activity/first-step":21},
            "12": {"activity/id":{"$uuid":"undated"}, "activity/type":3, "activity/title":"Undated", "activity/steps":[22], "activity/first-step":22},
            "20": {"step/id":{"$uuid":"step-20"}, "step/content":30},
            "21": {"step/id":{"$uuid":"step-21"}, "step/content":30},
            "22": {"step/id":{"$uuid":"step-22"}, "step/content":30},
            "30": {"assigned-problem/id":{"$uuid":"problem"}, "assigned-problem/content":40, "assigned-problem/topic-coverage":[90]},
            "40": {"multistep/id":{"$uuid":"multipart"}, "multistep/context":"Shared setup", "multistep/steps":[50,51], "multistep/first-step":51},
            "50": {"step/id":{"$uuid":"part-b"}, "step/content":61},
            "51": {"step/id":{"$uuid":"part-a"}, "step/content":60, "step/next":50},
            "60": {"question/id":{"$uuid":"question-a"}, "question/problem":"Part A {{answer}}",  "question/worked-solution":"Secret solution", "question/answer-fields":[70]},
            "61": {"question/id":{"$uuid":"question-b"}, "question/problem":"Part B", },
            "70": {"answer-field/id":{"$uuid":"field"}, "answer-field/key":"answer", "answer-field/type":4, "answer-field/choices":[80], "answer-field/correct":80},
            "80": {"answer/id":{"$uuid":"answer"}, "answer/type":5, "answer/value":"Secret answer", "answer/feedback":"Secret feedback"},
            "90": {"topic/id":{"$uuid":"topic"}, "topic/title":"A mapped topic", "topic/math-academy-id":42}
        }})).unwrap()
    }

    #[test]
    fn assignment_reader_orders_deadlines_and_preserves_nested_content_without_answer_keys() {
        let s = fixture();
        let list = list(&s, 1).unwrap();
        assert_eq!(
            list["assignments"]
                .as_array()
                .unwrap()
                .iter()
                .map(|a| a["id"].as_str().unwrap())
                .collect::<Vec<_>>(),
            ["earlier", "later", "undated"]
        );
        assert_eq!(list["assignments"][0]["due"], "2026-10-03T06:59:59.000Z");
        assert_eq!(
            list["assignments"][0]["course"],
            json!({"id":"science","entityId":6,"title":"Science"})
        );
        assert_eq!(list["assignments"][1]["course"]["id"], "course");
        assert!(list["assignments"][2]["course"].is_null());
        assert_eq!(list["assignments"][0]["problemCount"], 1);
        assert_eq!(list["assignments"][0]["questionCount"], 2);
        assert!(list["assignments"][0]["status"].is_null());
        let detail = detail(&s, 1, "earlier").unwrap();
        assert_eq!(detail["assignment"]["course"]["id"], "science");
        let problem = &detail["assignment"]["steps"][0]["content"];
        assert_eq!(problem["topicCoverage"][0]["mathAcademyId"], 42);
        assert_eq!(problem["content"]["context"], "Shared setup");
        let parts = &problem["content"]["steps"];
        assert_eq!(parts[0]["id"], "part-a");
        assert_eq!(parts[1]["id"], "part-b");
        assert_eq!(parts[0]["content"]["fields"][0]["choices"], json!([]));
        assert_eq!(parts[0]["content"]["fields"][0]["answerType"], "text");
        assert!(!detail.to_string().contains("Secret"));
        assert_eq!(s.basis_t, 7);
        assert!(!s.entity(1).unwrap().contains_key("learner/activity"));
    }

    #[test]
    fn assignment_reader_limits_access_and_rejects_broken_routes() {
        let mut s = fixture();
        assert!(detail(&s, 1, "not-assigned").is_err());
        s.entities
            .get_mut(&50)
            .unwrap()
            .insert("step/next".into(), json!(51));
        assert!(
            detail(&s, 1, "earlier")
                .unwrap_err()
                .to_string()
                .contains("acyclic")
        );
    }
}
