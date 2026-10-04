//! Assignment attempts use the shared learner task, immutable answer, clock,
//! transaction and request-journal boundary. Authored questions and coverage stay intact.
use super::*;
use assignment_reader::identity;

#[cfg(test)]
#[path = "assignment_interaction_tests.rs"]
mod tests;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct Occurrence {
    step: u64,
    question: u64,
}

fn collect(
    s: &EntitySnapshot,
    content: u64,
    step: u64,
    ancestors: &mut BTreeSet<u64>,
    output: &mut Vec<Occurrence>,
) -> Result<()> {
    if ancestors.len() >= 32 || !ancestors.insert(content) {
        return Err("Assignment content must be acyclic and at most 32 levels deep".into());
    }
    let record = s.entity(content)?;
    if record.contains_key("assigned-problem/id") {
        collect(
            s,
            s.reference(content, "assigned-problem/content")?,
            step,
            ancestors,
            output,
        )?;
    } else if record.contains_key("multistep/id") {
        for inner in assignment_reader::ordered_steps(s, content, "multistep")? {
            collect(
                s,
                s.reference(inner, "step/content")?,
                inner,
                ancestors,
                output,
            )?;
        }
    } else if record.contains_key("question/id") {
        if output.iter().any(|entry| entry.step == step) {
            return Err("An assignment cannot present the same leaf step more than once".into());
        }
        output.push(Occurrence {
            step,
            question: content,
        });
    } else if !record.contains_key("tutorial/id") {
        return Err("Unsupported assignment content".into());
    }
    ancestors.remove(&content);
    Ok(())
}

fn occurrences(s: &EntitySnapshot, activity: u64) -> Result<Vec<Occurrence>> {
    let mut result = vec![];
    for step in assignment_reader::ordered_steps(s, activity, "activity")? {
        collect(
            s,
            s.reference(step, "step/content")?,
            step,
            &mut BTreeSet::new(),
            &mut result,
        )?;
    }
    Ok(result)
}

/// The schema separates item identity from question identity. Derive an item's
/// identity from its task and authored leaf step so returning to that occurrence
/// reuses its presentation, even if another step presents the same question.
fn item_uuid(s: &EntitySnapshot, task_uuid: &str, step: u64) -> Result<String> {
    let hash = course_academy_engine::core::fingerprint(&json!([
        "assignment-occurrence-v1",
        task_uuid,
        identity(s, step, "step/id")?
    ]));
    let mut bytes = u128::from_str_radix(&hash[..32], 16)?.to_be_bytes();
    bytes[6] = (bytes[6] & 0x0f) | 0x80; // UUIDv8, application-defined SHA-256 identity.
    bytes[8] = (bytes[8] & 0x3f) | 0x80;
    Ok(uuid(u128::from_be_bytes(bytes)))
}

fn item_map(s: &EntitySnapshot, task: u64, route: &[Occurrence]) -> Result<BTreeMap<u64, u64>> {
    let task_uuid = identity(s, task, "learner-task/id")?;
    let expected = route
        .iter()
        .map(|entry| Ok((item_uuid(s, &task_uuid, entry.step)?, *entry)))
        .collect::<Result<BTreeMap<_, _>>>()?;
    let mut result = BTreeMap::new();
    for item in items(s, task)? {
        if s.owners(item, "learner-task/items")? != vec![task] {
            return Err("Presentation does not belong exclusively to this task".into());
        }
        let id = identity(s, item, "task-item/id")?;
        let entry = expected
            .get(&id)
            .ok_or("Assignment presentation has no matching leaf step")?;
        if s.reference(item, "task-item/content")? != entry.question
            || result.insert(entry.step, item).is_some()
        {
            return Err("Assignment presentation does not match its question occurrence".into());
        }
    }
    Ok(result)
}

fn canonical_responses(s: &EntitySnapshot, question: u64) -> Result<BTreeMap<u64, String>> {
    s.refs(question, "question/answer-fields")?
        .into_iter()
        .map(|field| {
            let correct = s.reference(field, "answer-field/correct")?;
            let value = if status(s, field, "answer-field/type")? == "blank" {
                text(s, correct, "answer/value")
            } else {
                correct.to_string()
            };
            Ok((field, value))
        })
        .collect()
}

fn gradable(s: &EntitySnapshot, question: u64) -> bool {
    canonical_responses(s, question)
        .and_then(|responses| Ok(learning::grade(s, question, &responses)?))
        .unwrap_or(false)
}

fn answer_json(s: &EntitySnapshot, answer: u64, feedback: bool) -> Result<Json> {
    let mut value = json!({
        "id": identity(s, answer, "answer/id")?, "entityId": answer,
        "type": status(s, answer, "answer/type")?, "value": text(s, answer, "answer/value"),
    });
    if feedback {
        if let Some(authored) = s.entity(answer)?.get("answer/feedback") {
            value["feedback"] = authored.clone();
        }
    }
    Ok(value)
}

fn enrich_content(
    s: &EntitySnapshot,
    content: &mut Json,
    step: u64,
    presentations: &BTreeMap<u64, u64>,
    preview: bool,
    at: DateTime<Utc>,
) -> Result<()> {
    match content["kind"].as_str() {
        Some("assigned-problem") => {
            enrich_content(s, &mut content["content"], step, presentations, preview, at)?
        }
        Some("multistep") => {
            for inner in content["steps"]
                .as_array_mut()
                .ok_or("Missing multipart steps")?
            {
                let step = required(inner, "entityId")?;
                enrich_content(s, &mut inner["content"], step, presentations, preview, at)?;
            }
        }
        Some("question") => {
            let question = required(content, "entityId")?;
            let item = presentations.get(&step).copied();
            let state = item
                .map(|item| status(s, item, "task-item/status"))
                .transpose()?;
            let answered = matches!(state.as_deref(), Some("correct" | "incorrect"));
            let reveal = preview || answered || content["isExample"] == true;
            content["stepId"] = json!(step);
            content["gradable"] = json!(gradable(s, question));
            content["itemId"] = json!(item);
            content["status"] = json!(state);
            content["elapsedSeconds"] =
                json!(item.map(|item| timing::elapsed(s, item, at)).transpose()?);
            let responses = item
                .map(|item| s.refs(item, "task-item/responses"))
                .transpose()?
                .unwrap_or_default();
            for field in content["fields"].as_array_mut().ok_or("Missing fields")? {
                let id = required(field, "entityId")?;
                let choices = s.refs(id, "answer-field/choices")?;
                if answered {
                    if let Some(&response) =
                        responses.iter().find(|answer| choices.contains(answer))
                    {
                        let mut value = answer_json(s, response, true)?;
                        value["choiceId"] = json!(response);
                        field["response"] = value;
                    }
                }
                if reveal {
                    if let Some(correct) = s.optional_ref(id, "answer-field/correct")? {
                        field["correctAnswer"] = answer_json(s, correct, true)?;
                    }
                    if preview {
                        for choice in field["choices"].as_array_mut().ok_or("Missing choices")? {
                            *choice = answer_json(s, required(choice, "entityId")?, true)?;
                        }
                    }
                }
            }
            if reveal {
                if let Some(solution) = s.entity(question)?.get("question/worked-solution") {
                    content["solution"] = solution.clone();
                }
            }
        }
        _ => {}
    }
    Ok(())
}

pub(super) fn enrich(s: &EntitySnapshot, assignment: &mut Json, preview: bool) -> Result<()> {
    let activity = required(assignment, "entityId")?;
    let route = occurrences(s, activity)?;
    let task = assignment["taskId"].as_u64();
    let presentations = task
        .map(|task| item_map(s, task, &route))
        .transpose()?
        .unwrap_or_default();
    let at = Utc::now();
    let mut task_items = vec![];
    for entry in &route {
        if let Some(&item) = presentations.get(&entry.step) {
            task_items.push(json!({
                "itemId": item, "stepId": entry.step, "contentId": entry.question,
                "status": status(s, item, "task-item/status")?, "elapsedSeconds": timing::elapsed(s, item, at)?,
            }));
        }
    }
    assignment["elapsedSeconds"] = if task_items.is_empty() {
        Json::Null
    } else {
        json!(
            task_items
                .iter()
                .map(|item| item["elapsedSeconds"].as_f64().unwrap())
                .sum::<f64>()
        )
    };
    assignment["items"] = json!(task_items);
    for step in assignment["steps"]
        .as_array_mut()
        .ok_or("Missing assignment steps")?
    {
        let id = required(step, "entityId")?;
        enrich_content(s, &mut step["content"], id, &presentations, preview, at)?;
    }
    Ok(())
}

fn assignment_task(s: &EntitySnapshot, learner: u64, task: u64) -> Result<u64> {
    owned(s, learner, task)?;
    let activity = s.reference(task, "learner-task/activity")?;
    if !assignment_reader::assigned(s, learner)?.contains(&activity) {
        return Err("Task is not an assignment for this learner".into());
    }
    Ok(activity)
}

fn pause_task(
    s: &EntitySnapshot,
    task: u64,
    at: DateTime<Utc>,
    forms: &mut Vec<Json>,
) -> Result<()> {
    let state = status(s, task, "learner-task/status")?;
    let active = items(s, task)?
        .into_iter()
        .filter(|item| {
            matches!(
                status(s, *item, "task-item/status").as_deref(),
                Ok("started")
            )
        })
        .collect::<Vec<_>>();
    if active.len() > 1 || (!active.is_empty() && state != "started") {
        return Err("Invalid active task timing state".into());
    }
    for item in active {
        transition(s, task, item, "paused", at, forms)?;
    }
    if state == "started" {
        forms.push(cas(
            s,
            task,
            "learner-task/status",
            "learner-task.status/paused",
        )?);
    }
    Ok(())
}

pub(super) fn latest_task(s: &EntitySnapshot, learner: u64, activity: u64) -> Result<Option<u64>> {
    if let Some(task) = task_for(s, learner, activity)? {
        return Ok(Some(task));
    }
    Ok(s.refs(learner, "learner/activity")?
        .into_iter()
        .filter(|task| {
            s.optional_ref(*task, "learner-task/activity")
                .ok()
                .flatten()
                == Some(activity)
        })
        .max_by_key(|task| {
            (
                s.status_history
                    .iter()
                    .filter(|event| {
                        event.entity == *task && event.attribute == "learner-task/status"
                    })
                    .map(|event| event.t)
                    .max()
                    .unwrap_or(0),
                *task,
            )
        }))
}

pub(super) fn mutate(
    s: &EntitySnapshot,
    learner: u64,
    action: &str,
    body: &Json,
    at: DateTime<Utc>,
) -> Result<(Vec<Json>, Json)> {
    if body["preview"] == true {
        return Err("Developer preview cannot record assignment work".into());
    }
    let mut forms = vec![];
    let from_task = body["taskId"]
        .as_u64()
        .map(|task| assignment_task(s, learner, task))
        .transpose()?;
    let selected = body["assignmentId"]
        .as_str()
        .map(|id| assignment_reader::resolve(s, learner, id))
        .transpose()?;
    if from_task.is_some() && selected.is_some() && from_task != selected {
        return Err("Task does not reference this assignment".into());
    }
    let activity = from_task
        .or(selected)
        .ok_or("Assignment or task ID required")?;
    let result = json!({"assignmentId": identity(s, activity, "activity/id")?});
    let task = body["taskId"]
        .as_u64()
        .or(latest_task(s, learner, activity)?);
    if let Some(task) = task {
        owned(s, learner, task)?;
    }
    let route = occurrences(s, activity)?;
    let presentations = task
        .map(|task| item_map(s, task, &route))
        .transpose()?
        .unwrap_or_default();
    // Validate the global invariant before generating any state changes.
    let active = timing::active_item(s, learner)?;
    if let Some(item) = active {
        let owners = s.owners(item, "learner-task/items")?;
        if owners.len() != 1 || status(s, owners[0], "learner-task/status")? != "started" {
            return Err("An actively timed question requires one started parent task".into());
        }
    }
    if action == "assignment-pause" || action == "pause" {
        if let Some(task) = task {
            pause_task(s, task, at, &mut forms)?;
        }
        return Ok((forms, result));
    }
    if action == "assignment-focus" {
        let step = required(body, "stepId")?;
        let entry = route
            .iter()
            .find(|entry| entry.step == step)
            .ok_or("Question step is not part of this assignment")?;
        if !gradable(s, entry.question) {
            return Err("This question has no supported, complete answer fields".into());
        }
        let existing = presentations.get(&step).copied();
        if let Some(item) = existing {
            if timing::terminal(&timing::status(s, item, "task-item/status")?) {
                return Ok((forms, result));
            }
        }
        if let Some(task) = task {
            if matches!(
                status(s, task, "learner-task/status")?.as_str(),
                "completed" | "failed"
            ) {
                return Err("Assignment task is already finished".into());
            }
        }
        // Switching questions or activities closes the previous clock in this
        // same transaction. No paused lesson or question resumes implicitly.
        for other in s.refs(learner, "learner/activity")? {
            if Some(other) != task && status(s, other, "learner-task/status")? == "started" {
                owned(s, learner, other)?;
                pause_task(s, other, at, &mut forms)?;
            }
        }
        if let Some(item) = active {
            if Some(item) != existing
                && task.is_some_and(|task| {
                    s.refs(task, "learner-task/items")
                        .unwrap_or_default()
                        .contains(&item)
                })
            {
                transition(s, task.unwrap(), item, "paused", at, &mut forms)?;
            }
        }
        let (target, task_uuid, tail) = if let Some(task) = task {
            owned(s, learner, task)?;
            if status(s, task, "learner-task/status")? != "started" {
                forms.push(cas(
                    s,
                    task,
                    "learner-task/status",
                    "learner-task.status/started",
                )?);
            }
            (
                json!(task),
                identity(s, task, "learner-task/id")?,
                items(s, task)?.last().copied(),
            )
        } else {
            let id = uid()?;
            forms.push(json!({"db/id":"assignment-task", "learner-task/id":{"$uuid":id}, "learner-task/activity":activity,
                "learner-task/status":kw("learner-task.status/started"), "learner-task/elapsed-seconds":0.0,
                "db/ensure":kw("learner-task/validate")}));
            forms.push(add(
                json!(learner),
                "learner/activity",
                json!("assignment-task"),
            ));
            (json!("assignment-task"), id, None)
        };
        if let Some(item) = existing {
            match status(s, item, "task-item/status")?.as_str() {
                "paused" => {
                    forms.push(cas(
                        s,
                        item,
                        "task-item/status",
                        "task-item.status/started",
                    )?);
                }
                "started" => {}
                _ => return Err("Question cannot be focused".into()),
            }
        } else {
            forms.push(json!({"db/id":"assignment-item", "task-item/id":{"$uuid":item_uuid(s, &task_uuid, step)?},
                "task-item/content":entry.question, "task-item/status":kw("task-item.status/started"),
                "task-item/elapsed-seconds":0.0, "db/ensure":kw("task-item/validate")}));
            forms.push(add(target, "learner-task/items", json!("assignment-item")));
            if let Some(tail) = tail {
                forms.push(add(json!(tail), "task-item/next", json!("assignment-item")));
            }
        }
        return Ok((forms, result));
    }
    if action != "assignment-answer" {
        return Err("Unknown assignment action".into());
    }
    let task = task.ok_or("Focus a question before answering")?;
    let item = required(body, "itemId")?;
    let entry = route
        .iter()
        .find(|entry| presentations.get(&entry.step) == Some(&item))
        .ok_or("Question presentation does not belong to this assignment")?;
    if timing::terminal(&timing::status(s, item, "task-item/status")?) {
        return Ok((forms, result)); // A saved response is immutable, even under a new request ID.
    }
    if status(s, task, "learner-task/status")? != "started" || active != Some(item) {
        return Err("Focus this question before submitting an answer".into());
    }
    let fields = s.refs(entry.question, "question/answer-fields")?;
    let mut submitted = BTreeMap::new();
    let mut answers = vec![];
    for response in body["responses"]
        .as_array()
        .ok_or("responses must be a list")?
    {
        let field = required(response, "fieldId")?;
        if !fields.contains(&field) || submitted.contains_key(&field) {
            return Err("Each answer field must appear exactly once".into());
        }
        let choices = s.refs(field, "answer-field/choices")?;
        let (value, answer) = if status(s, field, "answer-field/type")? == "blank" {
            let value = response["value"]
                .as_str()
                .ok_or("Blank response must contain a string value")?;
            if value.len() > 4096 {
                return Err("Response is too long".into());
            }
            let existing = choices
                .into_iter()
                .find(|answer| text(s, *answer, "answer/value") == value);
            let answer = if let Some(answer) = existing {
                json!(answer)
            } else {
                let temp = format!("assignment-response-{field}");
                let correct = s.reference(field, "answer-field/correct")?;
                forms.push(json!({"db/id":temp,"answer/id":{"$uuid":uid()?},"answer/type":s.reference(correct,"answer/type")?,"answer/value":value,"db/ensure":kw("answer/validate")}));
                forms.push(add(json!(field), "answer-field/choices", json!(temp)));
                json!(temp)
            };
            (value.to_owned(), answer)
        } else {
            let answer = required(response, "choiceId")?;
            if !choices.contains(&answer) {
                return Err("Choice does not belong to this field".into());
            }
            (answer.to_string(), json!(answer))
        };
        submitted.insert(field, value);
        answers.push(answer);
    }
    let correct = learning::grade(s, entry.question, &submitted)?;
    for answer in answers {
        forms.push(add(json!(item), "task-item/responses", answer));
    }
    transition(
        s,
        task,
        item,
        if correct { "correct" } else { "incorrect" },
        at,
        &mut forms,
    )?;
    // Missing fields are still real unfinished questions. Never manufacture
    // completion or credit from the mapped topics or a partial import.
    let complete = route
        .iter()
        .filter(|entry| !s.is_example(entry.question))
        .all(|entry| {
            gradable(s, entry.question)
                && presentations.get(&entry.step).is_some_and(|other| {
                    *other == item
                        || matches!(
                            status(s, *other, "task-item/status").as_deref(),
                            Ok("correct" | "incorrect")
                        )
                })
        });
    forms.push(cas(
        s,
        task,
        "learner-task/status",
        if complete {
            "learner-task.status/completed"
        } else {
            "learner-task.status/paused"
        },
    )?);
    Ok((forms, result))
}
