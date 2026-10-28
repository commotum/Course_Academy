//! Read-only, learner-owned attempt history. Summaries never render question bodies.
use super::*;

#[derive(Default)]
struct Dates {
    last: BTreeMap<u64, DateTime<Utc>>,
    started: BTreeSet<u64>,
}
impl Dates {
    fn capture(s: &EntitySnapshot, relevant: &BTreeSet<u64>) -> Result<Self> {
        let mut dates = Self::default();
        // One pass over captured status assertions, rather than rescanning them
        // for every task/item. No curriculum/entity scan or timing mutation.
        for event in &s.status_history {
            if relevant.contains(&event.entity) {
                dates
                    .last
                    .insert(event.entity, schema::parse_instant(&event.at)?);
                if s.ident(&event.value)?.ends_with("/started") {
                    dates.started.insert(event.entity);
                }
            }
        }
        for &entity in relevant {
            if s.entity(entity)?.contains_key("learner-task/finished-at") {
                if let Some(&recorded) = dates.last.get(&entity) {
                    dates.last.insert(entity, timing::task_finished_at(s, entity, recorded)?);
                }
            }
        }
        Ok(dates)
    }
}
fn terminal(s: &EntitySnapshot, task: u64) -> Result<bool> {
    Ok(matches!(
        status(s, task, "learner-task/status")?.as_str(),
        "completed" | "failed"
    ))
}
fn duration(s: &EntitySnapshot, entity: u64, attr: &str) -> Option<f64> {
    s.entities
        .get(&entity)?
        .get(attr)?
        .as_f64()
        .filter(|v| v.is_finite() && *v >= 0.0)
}
fn summary(s: &EntitySnapshot, task: u64, dates: &Dates, quiz_labels: &QuizLabels) -> Result<Json> {
    let activity = s.reference(task, "learner-task/activity")?;
    let mut counts = BTreeMap::<String, usize>::new();
    let task_items = s.refs(task, "learner-task/items")?;
    let mut elapsed = (!task_items.is_empty()).then_some(0.0);
    for item in task_items {
        let content = s.reference(item, "task-item/content")?;
        if s.is_ordinary_question(content)? {
            *counts
                .entry(status(s, item, "task-item/status")?)
                .or_default() += 1;
        }
        elapsed = elapsed
            .zip(duration(s, item, "task-item/elapsed-seconds"))
            .map(|(a, b)| a + b);
    }
    let course = s
        .optional_ref(activity, "activity/course")?
        .map(|c| text(s, c, "course/title"));
    Ok(json!({
        "taskId": task, "activityId": activity, "title": quiz_labels.title(s, activity, Some(task))?,
        "type": status(s, activity, "activity/type")?, "status": status(s, task, "learner-task/status")?,
        "completedAt": dates.last.get(&task).map(DateTime::to_rfc3339),
        "recordedOnly": !dates.started.contains(&task) && !s.entity(task)?.contains_key("learner-task/finished-at"), "courseTitle": course,
        "elapsedSeconds": duration(s, task, "learner-task/elapsed-seconds").or(elapsed),
        "xp": s.entity(task)?.get("learner-task/xp-earned"), "xpBase": s.entity(task)?.get("learner-task/xp-base"),
        "questionCount": counts.values().sum::<usize>(), "correctCount": counts.get("correct").copied().unwrap_or(0),
        "incorrectCount": counts.get("incorrect").copied().unwrap_or(0), "skippedCount": counts.get("skipped").copied().unwrap_or(0),
    }))
}
pub(super) fn list(s: &EntitySnapshot, learner: u64, body: &Json) -> Result<Json> {
    let quiz_labels = QuizLabels::capture(s, learner)?;
    let tasks = s
        .refs(learner, "learner/activity")?
        .into_iter()
        .filter_map(|t| match terminal(s, t) {
            Ok(true) => Some(Ok(t)),
            Ok(false) => None,
            Err(e) => Some(Err(e)),
        })
        .collect::<Result<BTreeSet<_>>>()?;
    let dates = Dates::capture(s, &tasks)?;
    let mut ordered: Vec<_> = tasks.into_iter().collect();
    ordered.sort_by_key(|t| std::cmp::Reverse((dates.last.get(t).copied(), *t)));
    let total = ordered.len();
    let start = match body.get("beforeTaskId") {
        None => 0,
        Some(v) => {
            let cursor = v.as_u64().ok_or("Invalid activity history cursor")?;
            ordered
                .iter()
                .position(|t| *t == cursor)
                .ok_or("Activity history cursor is unavailable")?
                + 1
        }
    };
    let page = &ordered[start..ordered.len().min(start + 40)];
    // Only the selected page's item references are read; authored bodies and
    // answer fields are fetched by detail() on expansion.
    let activities = page
        .iter()
        .map(|t| summary(s, *t, &dates, &quiz_labels))
        .collect::<Result<Vec<_>>>()?;
    let course = s
        .optional_ref(learner, "learner/course")?
        .map(|c| json!({"id":s.entities[&c].get("course/id").and_then(|v|v.get("$uuid"))}));
    Ok(
        json!({"basis":s.basis_t,"learner":learner_json(s,learner),"course":course,"activities":activities,"total":total,
        "nextCursor": if start + page.len() < total { page.last().copied() } else { None }}),
    )
}
pub(super) fn detail(s: &EntitySnapshot, learner: u64, task: u64) -> Result<Json> {
    owned(s, learner, task)?;
    if !terminal(s, task)? {
        return Err("Activity history is available after an attempt finishes".into());
    }
    let activity = s.reference(task, "learner-task/activity")?;
    let chain = items(s, task)?;
    let mut relevant: BTreeSet<_> = chain.iter().copied().collect();
    relevant.insert(task);
    let dates = Dates::capture(s, &relevant)?;
    let kind = status(s, activity, "activity/type")?;
    let steps = if kind == "assignment" {
        vec![]
    } else {
        learning::lesson_steps(s, activity)?
    };
    let mut history = vec![];
    for (index, &item) in chain.iter().enumerate() {
        let content = s.reference(item, "task-item/content")?;
        let elapsed = duration(s, item, "task-item/elapsed-seconds");
        // Reuse the player's immutable answer/solution projection, without
        // starting clocks or computing eligibility for this completed task.
        let mut entry = task_step_json_with_elapsed(s, &steps, item, elapsed)?;
        if kind == "assessment" && s.entity(content)?.contains_key("question/id") {
            let topic = s.topic_for_question(content)?;
            entry["topic"] = json!({"id":topic,"title":text(s, topic, "topic/title")});
        }
        // A finished/expired assessment may contain its last unanswered item.
        // Reveal authored explanations without manufacturing a response/grade.
        if s.entity(content)?.contains_key("question/id") {
            entry["solution"] = json!(text(s, content, "question/worked-solution"));
            for field in entry["fields"]
                .as_array_mut()
                .ok_or("Missing history fields")?
            {
                if let Some(correct) =
                    s.optional_ref(required(field, "id")?, "answer-field/correct")?
                {
                    field["correctAnswer"] = json!({"id":correct,"type":status(s,correct,"answer/type")?,"value":text(s,correct,"answer/value")});
                }
            }
        }
        entry["order"] = json!(index + 1);
        entry["answeredAt"] = json!(dates.last.get(&item).map(DateTime::to_rfc3339));
        entry["recordedOnly"] = json!(!dates.started.contains(&item));
        entry["difficulty"] = s
            .optional_ref(content, "question/difficulty")?
            .map(|_| status(s, content, "question/difficulty"))
            .transpose()?
            .map_or(Json::Null, |v| json!(v));
        let kp = authored_step(&steps, content)
            .filter(|(_, st)| st.kind == "knowledge-point")
            .map(|(_, st)| st.content);
        entry["group"] = json!(
            kp.map(|kp| text(s, kp, "knowledge-point/title"))
                .filter(|t| !t.is_empty())
        );
        history.push(entry);
    }
    let quiz_labels = QuizLabels::capture(s, learner)?;
    Ok(json!({"basis":s.basis_t,"activity":summary(s,task,&dates,&quiz_labels)?,"items":history}))
}

#[cfg(test)]
mod tests {
    use super::*;
    fn fixture() -> EntitySnapshot {
        let mut records = BTreeMap::new();
        let rows = [
            (
                1,
                json!({"learner/id":"mine","learner/activity":[10,11,12]}),
            ),
            (2, json!({"learner/id":"other","learner/activity":[13]})),
            (
                5,
                json!({"activity/id":{"$uuid":uuid(5)},"activity/type":"activity.type/lesson","activity/title":"A lesson","activity/steps":[6],"activity/first-step":6}),
            ),
            (6, json!({"step/id":{"$uuid":uuid(6)},"step/content":20})),
            (
                10,
                json!({"learner-task/id":{"$uuid":uuid(10)},"learner-task/activity":5,"learner-task/status":"learner-task.status/completed","learner-task/items":[31,30],"learner-task/xp-base":10,"learner-task/xp-earned":8,"learner-task/elapsed-seconds":21.0}),
            ),
            (
                11,
                json!({"learner-task/activity":5,"learner-task/status":"learner-task.status/paused"}),
            ),
            (
                12,
                json!({"learner-task/activity":5,"learner-task/status":"learner-task.status/failed"}),
            ),
            (
                13,
                json!({"learner-task/activity":5,"learner-task/status":"learner-task.status/completed"}),
            ),
            (
                20,
                json!({"question/id":{"$uuid":uuid(20)},"question/problem":"What is two?","question/worked-solution":"Add one and one.","question/difficulty":"question.difficulty/moderate","question/answer-fields":[21]}),
            ),
            (
                21,
                json!({"answer-field/type":"answer-field.type/blank","answer-field/key":"value","answer-field/choices":[22,23],"answer-field/correct":22}),
            ),
            (
                22,
                json!({"answer/type":"answer.type/math","answer/value":"2"}),
            ),
            (
                23,
                json!({"answer/type":"answer.type/math","answer/value":"3"}),
            ),
            (
                30,
                json!({"task-item/content":20,"task-item/status":"task-item.status/incorrect","task-item/next":31,"task-item/responses":[23],"task-item/elapsed-seconds":9.0}),
            ),
            (
                31,
                json!({"task-item/content":20,"task-item/status":"task-item.status/correct","task-item/responses":[22],"task-item/elapsed-seconds":12.0}),
            ),
        ];
        for (id, row) in rows {
            records.insert(id, row.as_object().unwrap().clone());
        }
        for (index, ident) in [
            "activity.type/lesson",
            "activity.type/assignment",
            "learner-task.status/completed",
            "learner-task.status/failed",
            "learner-task.status/paused",
            "task-item.status/correct",
            "task-item.status/incorrect",
            "task-item.status/paused",
            "answer-field.type/blank",
            "answer.type/math",
            "question.difficulty/moderate",
        ]
        .iter()
        .enumerate()
        {
            records.insert(
                1000 + index as u64,
                json!({"db/ident":kw(ident)}).as_object().unwrap().clone(),
            );
        }
        EntitySnapshot::new(records, 42).unwrap()
    }
    #[test]
    fn summaries_are_owned_terminal_and_lightweight() -> Result<()> {
        let s = fixture();
        let before = json!({"entities":s.entities,"history":s.status_history,"basis":s.basis_t});
        let view = list(&s, 1, &json!({}))?;
        assert_eq!(view["total"], 2);
        assert_eq!(view["activities"][0]["taskId"], 12);
        assert_eq!(view["activities"][1]["correctCount"], 1);
        assert!(view["activities"][1].get("items").is_none());
        assert!(detail(&s, 1, 11).is_err());
        assert!(detail(&s, 1, 13).is_err());
        assert_eq!(
            before,
            json!({"entities":s.entities,"history":s.status_history,"basis":s.basis_t})
        );
        Ok(())
    }
    #[test]
    fn details_preserve_presentations_answers_and_observed_metadata() -> Result<()> {
        let s = fixture();
        let view = detail(&s, 1, 10)?;
        assert_eq!(view["items"][0]["itemId"], 30);
        assert_eq!(view["items"][1]["itemId"], 31);
        assert_eq!(view["items"][0]["fields"][0]["response"]["value"], "3");
        assert_eq!(view["items"][0]["fields"][0]["correctAnswer"]["value"], "2");
        assert_eq!(view["items"][0]["fields"][0]["grade"], "incorrect");
        assert_eq!(view["items"][0]["difficulty"], "moderate");
        assert_eq!(view["items"][0]["elapsedSeconds"], 9.0);
        assert_eq!(view["items"][0]["solution"], "Add one and one.");
        assert!(view["activity"]["completedAt"].is_null());
        Ok(())
    }
    #[test]
    fn assessment_questions_show_their_own_topics_without_changing_history() -> Result<()> {
        let mut s = fixture();
        s.entities.insert(1200, json!({"db/ident":kw("activity.type/assessment")}).as_object().unwrap().clone());
        s.entities.get_mut(&5).unwrap()["activity/type"] = json!("activity.type/assessment");
        s.entities.get_mut(&5).unwrap().insert("activity/scope".into(), json!(40));
        s.entities.get_mut(&5).unwrap()["activity/steps"] = json!([6,7]);
        s.entities.get_mut(&6).unwrap().insert("step/next".into(), json!(7));
        s.entities.insert(7, json!({"step/id":{"$uuid":uuid(7)},"step/content":25}).as_object().unwrap().clone());
        let mut second = s.entities[&20].clone();
        second.insert("question/id".into(), json!({"$uuid":uuid(25)}));
        s.entities.insert(25, second);
        s.entities.get_mut(&31).unwrap()["task-item/content"] = json!(25);
        for (id, record) in [
            (40, json!({"topic/id":{"$uuid":uuid(40)},"topic/title":"Linear equations","topic/knowledge-points":[41]})),
            (41, json!({"knowledge-point/id":{"$uuid":uuid(41)},"knowledge-point/questions":[20]})),
            (43, json!({"topic/id":{"$uuid":uuid(43)},"topic/title":"Fractions","topic/knowledge-points":[44]})),
            (44, json!({"knowledge-point/id":{"$uuid":uuid(44)},"knowledge-point/questions":[25]})),
        ] { s.entities.insert(id, record.as_object().unwrap().clone()); }
        let s = EntitySnapshot::new(s.entities.into(), 42)?;
        let before = s.entities.clone();
        let view = detail(&s, 1, 10)?;
        assert_eq!(view["items"][0]["topic"], json!({"id":40,"title":"Linear equations"}));
        assert_eq!(view["items"][1]["topic"], json!({"id":43,"title":"Fractions"}));
        assert_eq!(s.entities, before);
        Ok(())
    }
    #[test]
    fn finished_unanswered_items_reveal_solutions_without_inventing_answers() -> Result<()> {
        let mut s = fixture();
        s.entities.get_mut(&31).unwrap()["task-item/status"] = json!("task-item.status/paused");
        s.entities
            .get_mut(&31)
            .unwrap()
            .remove("task-item/responses");
        let view = detail(&s, 1, 10)?;
        let last = &view["items"][1];
        assert_eq!(last["status"], "paused");
        assert!(last["fields"][0].get("response").is_none());
        assert_eq!(last["fields"][0]["correctAnswer"]["value"], "2");
        assert_eq!(last["solution"], "Add one and one.");
        Ok(())
    }
    #[test]
    fn assignment_history_uses_the_attempt_chain_even_when_authored_steps_repeat() -> Result<()> {
        let mut s = fixture();
        s.entities.get_mut(&5).unwrap()["activity/type"] = json!("activity.type/assignment");
        let view = detail(&s, 1, 10)?;
        assert_eq!(view["activity"]["type"], "assignment");
        assert_eq!(view["items"].as_array().unwrap().len(), 2);
        assert_eq!(view["items"][0]["fields"][0]["response"]["value"], "3");
        assert_eq!(view["items"][1]["fields"][0]["response"]["value"], "2");
        Ok(())
    }
    #[test]
    fn completion_sort_uses_dates_and_missing_measurements_stay_unknown() -> Result<()> {
        let mut s = fixture();
        for (task, seconds) in [(10, 30), (12, 20)] {
            s.status_history.push(StatusAssertion {
                entity: task,
                attribute: "learner-task/status".into(),
                value: s.entity(task)?["learner-task/status"].clone(),
                t: seconds,
                at: schema::instant_value(DateTime::from_timestamp(seconds as i64, 0).unwrap()),
            });
        }
        let view = list(&s, 1, &json!({}))?;
        assert_eq!(view["activities"][0]["taskId"], 10);
        assert!(view["activities"][1]["elapsedSeconds"].is_null());
        assert_eq!(
            view["activities"][0]["completedAt"],
            "1970-01-01T00:00:30+00:00"
        );
        s.entities.get_mut(&10).unwrap().insert("learner-task/finished-at".into(),schema::instant_value(DateTime::from_timestamp(10,0).unwrap()));
        let recovered = list(&s,1,&json!({}))?;
        assert_eq!(recovered["activities"][0]["taskId"],12);
        assert_eq!(recovered["activities"][1]["completedAt"],"1970-01-01T00:00:10+00:00");
        assert_eq!(recovered["activities"][1]["recordedOnly"],false);
        Ok(())
    }
    #[test]
    fn pagination_is_stable_when_a_newer_attempt_arrives() -> Result<()> {
        let mut s = fixture();
        for id in 100..145 {
            s.entities.insert(id,json!({"learner-task/activity":5,"learner-task/status":"learner-task.status/completed"}).as_object().unwrap().clone());
        }
        s.entities.get_mut(&1).unwrap()["learner/activity"] = json!((100..145).collect::<Vec<_>>());
        let first = list(&s, 1, &json!({}))?;
        assert_eq!(first["activities"].as_array().unwrap().len(), 40);
        let cursor = first["nextCursor"].clone();
        s.entities.insert(999,json!({"learner-task/activity":5,"learner-task/status":"learner-task.status/completed"}).as_object().unwrap().clone());
        s.entities.get_mut(&1).unwrap()["learner/activity"]
            .as_array_mut()
            .unwrap()
            .push(json!(999));
        let next = list(&s, 1, &json!({"beforeTaskId":cursor}))?;
        assert_eq!(next["activities"].as_array().unwrap().len(), 5);
        assert!(next["nextCursor"].is_null());
        Ok(())
    }
}
