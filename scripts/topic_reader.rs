//! Read-only lesson reference projection. It follows authored placements and
//! never expands a knowledge point's practice pool or invokes grading rules.

use super::*;

fn load_attrs(
    db: &DatabaseValue,
    facts: &mut Facts,
    eid: u64,
    attrs: &[&'static str],
) -> Result<()> {
    let selected: BTreeMap<_, _> = attrs
        .iter()
        .filter_map(|attr| {
            let (ns, name) = attr.split_once('/')?;
            db.schema()
                .resolve_ident(&Keyword::new(ns, name))
                .map(|id| (id, *attr))
        })
        .collect();
    // An entity prefix keeps content reads local to this lesson. In particular,
    // no attribute-wide scan of questions, answers, or tutorial prose is needed.
    for datom in db.collect_datoms_with_prefix(&IndexPrefix::Eavt {
        entity: eid,
        attribute: None,
        value: None,
    })? {
        if let Some(attr) = selected.get(&datom.attribute) {
            let slot = facts.entry(eid).or_default().entry(*attr).or_default();
            if !slot.contains(&datom.value) {
                slot.push(datom.value);
            }
        }
    }
    Ok(())
}

fn referrers(db: &DatabaseValue, eid: u64, attr: &str) -> Result<Vec<u64>> {
    let (ns, name) = attr.split_once('/').ok_or("Invalid reference attribute")?;
    let Some(attribute) = db.schema().resolve_ident(&Keyword::new(ns, name)) else {
        return Ok(vec![]);
    };
    Ok(db
        .collect_datoms_with_prefix(&IndexPrefix::Vaet {
            value: Value::Ref(eid),
            attribute: Some(attribute),
            entity: None,
        })?
        .into_iter()
        .map(|datom| datom.entity)
        .collect())
}

fn enum_name(db: &DatabaseValue, facts: &Facts, eid: u64, attr: &str) -> Option<String> {
    refs(facts, eid, attr)
        .first()
        .and_then(|eid| db.ident(*eid))
        .map(|ident| ident.qualified_name())
}

fn short_enum(db: &DatabaseValue, facts: &Facts, eid: u64, attr: &str) -> String {
    enum_name(db, facts, eid, attr)
        .map(|ident| ident.rsplit('/').next().unwrap_or(&ident).to_string())
        .unwrap_or_else(|| "unknown".into())
}

fn display_id(facts: &Facts, eid: u64, attr: &str) -> String {
    uuid(facts, eid, attr).unwrap_or_else(|| eid.to_string())
}

fn topic_identity(facts: &Facts, eid: u64) -> Result<Json> {
    if eid > 9_007_199_254_740_991 {
        return Err("Topic entity ID exceeds JavaScript safe integer range".into());
    }
    Ok(json!({
        "id": eid,
        "uuid": required_uuid(facts, eid, "topic/id")?,
        "mathAcademyId": long(facts, eid, "topic/math-academy-id"),
        "title": title(facts, eid, "topic"),
    }))
}

fn ordered_steps(facts: &Facts, activity: u64) -> Result<Vec<u64>> {
    let members: BTreeSet<_> = refs(facts, activity, "activity/steps")
        .into_iter()
        .collect();
    let mut current = refs(facts, activity, "activity/first-step")
        .first()
        .copied();
    let mut visited = BTreeSet::new();
    let mut ordered = Vec::new();
    while let Some(step) = current {
        if !members.contains(&step) || !visited.insert(step) {
            return Err("Lesson steps must form one acyclic owned route".into());
        }
        ordered.push(step);
        current = refs(facts, step, "step/next").first().copied();
    }
    if members != visited {
        return Err("Lesson contains unreachable steps".into());
    }
    Ok(ordered)
}

// A section is either a tutorial or a worked example. An ordinary question
// encountered directly in the authored route is skipped without grading it.
fn section_content(facts: &Facts, content: u64) -> Result<Option<(&'static str, u64, String)>> {
    if scalar(facts, content, "tutorial/id").is_some() {
        return Ok(Some((
            "tutorial",
            content,
            title(facts, content, "tutorial"),
        )));
    }
    if scalar(facts, content, "knowledge-point/id").is_some() {
        let Some(example) = refs(facts, content, "knowledge-point/canonical-example")
            .first()
            .copied()
        else {
            return Ok(None); // An identity-only KP has no imported example yet.
        };
        if scalar(facts, example, "question/is-example") != Some(&Value::Bool(true)) {
            return Err("Knowledge point canonical example is not a worked example".into());
        }
        return Ok(Some((
            "example",
            example,
            title(facts, content, "knowledge-point"),
        )));
    }
    if scalar(facts, content, "question/is-example") == Some(&Value::Bool(true)) {
        return Ok(Some(("example", content, "Worked example".into())));
    }
    if scalar(facts, content, "question/id").is_some() {
        return Ok(None);
    }
    Err("Unsupported content in topic lesson".into())
}

fn example_fields(db: &DatabaseValue, facts: &mut Facts, question: u64) -> Result<Vec<Json>> {
    let field_ids = refs(facts, question, "question/answer-fields");
    let mut fields = Vec::new();
    for field in field_ids {
        load_attrs(
            db,
            facts,
            field,
            &[
                "answer-field/id",
                "answer-field/key",
                "answer-field/type",
                "answer-field/choices",
                "answer-field/correct",
            ],
        )?;
        let choice_ids = refs(facts, field, "answer-field/choices");
        let correct = refs(facts, field, "answer-field/correct").first().copied();
        let mut choices = Vec::new();
        for choice in &choice_ids {
            load_attrs(
                db,
                facts,
                *choice,
                &[
                    "answer/id",
                    "answer/type",
                    "answer/value",
                    "answer/feedback",
                ],
            )?;
            choices.push(json!({
                "id": display_id(facts, *choice, "answer/id"),
                "type": short_enum(db, facts, *choice, "answer/type"),
                "value": text(facts, *choice, "answer/value").unwrap_or_default(),
                "feedback": text(facts, *choice, "answer/feedback"),
            }));
        }
        let mut value = json!({
            "id": display_id(facts, field, "answer-field/id"),
            "key": text(facts, field, "answer-field/key").unwrap_or_default(),
            "type": short_enum(db, facts, field, "answer-field/type"),
            "choices": choices,
        });
        // Incomplete captured answer keys must not prevent reading instruction.
        // Correct is a choice identity, never an inferred value or grade.
        if let Some(correct) = correct.filter(|eid| choice_ids.contains(eid)) {
            value["correct"] = json!(display_id(facts, correct, "answer/id"));
        }
        fields.push(value);
    }
    Ok(fields)
}

const CONTENT_ATTRS: &[&str] = &[
    "tutorial/id",
    "tutorial/title",
    "tutorial/content",
    "knowledge-point/id",
    "knowledge-point/title",
    "knowledge-point/canonical-example",
    "question/id",
    "question/is-example",
    "question/problem",
    "question/worked-solution",
    "question/requires-calculator",
    "question/answer-fields",
];

fn lesson_sections(db: &DatabaseValue, facts: &mut Facts, topic: u64) -> Result<Vec<Json>> {
    let mut lessons = Vec::new();
    for activity in referrers(db, topic, "activity/scope")? {
        load_attrs(
            db,
            facts,
            activity,
            &[
                "activity/id",
                "activity/type",
                "activity/steps",
                "activity/first-step",
            ],
        )?;
        if enum_name(db, facts, activity, "activity/type").as_deref()
            == Some("activity.type/lesson")
        {
            lessons.push(activity);
        }
    }
    let Some(activity) = lessons.first().copied() else {
        return Ok(vec![]);
    };
    if lessons.len() > 1 {
        return Err("Topic has multiple lesson activities; reference lesson is ambiguous".into());
    }
    for step in refs(facts, activity, "activity/steps") {
        load_attrs(db, facts, step, &["step/id", "step/content", "step/next"])?;
    }
    let mut sections = Vec::new();
    for step in ordered_steps(facts, activity)? {
        let content = refs(facts, step, "step/content")
            .first()
            .copied()
            .ok_or("Lesson step has no content")?;
        load_attrs(db, facts, content, CONTENT_ATTRS)?;
        if let Some(example) = refs(facts, content, "knowledge-point/canonical-example")
            .first()
            .copied()
        {
            load_attrs(db, facts, example, CONTENT_ATTRS)?;
        }
        let Some((kind, content, heading)) = section_content(facts, content)? else {
            continue;
        };
        let markdown = text(
            facts,
            content,
            if kind == "tutorial" {
                "tutorial/content"
            } else {
                "question/problem"
            },
        )
        .unwrap_or_default();
        let solution = text(facts, content, "question/worked-solution");
        if markdown.trim().is_empty()
            && solution
                .as_deref()
                .is_none_or(|text| text.trim().is_empty())
        {
            continue;
        }
        let mut section = json!({
            "id": display_id(facts, step, "step/id"),
            "stepId": step.to_string(),
            "kind": kind, "title": heading, "markdown": markdown,
        });
        if kind == "example" {
            if let Some(solution) = solution {
                section["workedSolution"] = json!(solution);
            }
            if let Some(Value::Bool(required)) =
                scalar(facts, content, "question/requires-calculator")
            {
                section["requiresCalculator"] = json!(required);
            }
            let fields = example_fields(db, facts, content)?;
            if !fields.is_empty() {
                section["fields"] = json!(fields);
            }
        }
        sections.push(section);
    }
    Ok(sections)
}

pub(super) fn topic(db: &DatabaseValue, learner_id: &str, selector: &str) -> Result<Option<Json>> {
    let mut facts = project(db)?;
    let learner_eid = facts
        .keys()
        .copied()
        .find(|eid| text(&facts, *eid, "learner/id").as_deref() == Some(learner_id))
        .ok_or("Learner not found")?;
    let academy_id = selector.parse::<i64>().ok();
    let topic_eid = facts.keys().copied().find(|eid| {
        uuid(&facts, *eid, "topic/id").is_some_and(|id| {
            id.eq_ignore_ascii_case(selector)
                || academy_id
                    .is_some_and(|id| long(&facts, *eid, "topic/math-academy-id") == Some(id))
        })
    });
    let Some(topic_eid) = topic_eid else {
        return Ok(None);
    };
    let mut courses = Vec::new();
    for eid in facts.keys().copied() {
        let Some(id) = uuid(&facts, eid, "course/id") else {
            continue;
        };
        let member = refs(&facts, eid, "course/units").into_iter().any(|unit| {
            refs(&facts, unit, "unit/modules")
                .into_iter()
                .any(|module| refs(&facts, module, "module/topics").contains(&topic_eid))
        });
        if member {
            courses.push(json!({
                "id": id,
                "title": title(&facts, eid, "course"),
                "groups": course_groups(&facts, eid),
            }));
        }
    }
    courses.sort_by(|a, b| {
        a["title"]
            .as_str()
            .cmp(&b["title"].as_str())
            .then_with(|| a["id"].as_str().cmp(&b["id"].as_str()))
    });
    let mut prerequisite_ids: Vec<_> = facts
        .keys()
        .copied()
        .filter(|eid| refs(&facts, *eid, "topic/next").contains(&topic_eid))
        .collect();
    prerequisite_ids.sort_by_key(|eid| (title(&facts, *eid, "topic"), *eid));
    let prerequisites = prerequisite_ids
        .into_iter()
        .map(|eid| topic_identity(&facts, eid))
        .collect::<Result<Vec<_>>>()?;
    let sections = lesson_sections(db, &mut facts, topic_eid)?;
    Ok(Some(json!({
        "basis": db.basis_t(),
        "learner": learner_json(&facts, learner_eid, learner_id),
        "topic": topic_identity(&facts, topic_eid)?,
        "courses": courses,
        "prerequisites": prerequisites,
        "available": !sections.is_empty(),
        "sections": sections,
    })))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fact(facts: &mut Facts, eid: u64, attr: &'static str, value: Value) {
        facts
            .entry(eid)
            .or_default()
            .entry(attr)
            .or_default()
            .push(value);
    }

    #[test]
    fn lesson_order_follows_owned_route_and_rejects_cycles_or_unreachable_steps() {
        let mut facts = Facts::new();
        for step in [21, 20, 22] {
            fact(&mut facts, 1, "activity/steps", Value::Ref(step));
        }
        fact(&mut facts, 1, "activity/first-step", Value::Ref(22));
        fact(&mut facts, 22, "step/next", Value::Ref(20));
        fact(&mut facts, 20, "step/next", Value::Ref(21));
        assert_eq!(ordered_steps(&facts, 1).unwrap(), vec![22, 20, 21]);
        fact(&mut facts, 21, "step/next", Value::Ref(22));
        assert!(ordered_steps(&facts, 1).is_err());
        facts.get_mut(&21).unwrap().remove("step/next");
        facts.get_mut(&20).unwrap().remove("step/next");
        assert!(ordered_steps(&facts, 1).is_err());
    }

    #[test]
    fn reference_content_excludes_practice_and_does_not_require_answer_keys_or_bank() {
        let mut facts = Facts::new();
        fact(&mut facts, 1, "knowledge-point/id", Value::Uuid(1));
        fact(
            &mut facts,
            1,
            "knowledge-point/title",
            Value::String("Example title".into()),
        );
        fact(
            &mut facts,
            1,
            "knowledge-point/canonical-example",
            Value::Ref(2),
        );
        fact(&mut facts, 2, "question/is-example", Value::Bool(true));
        fact(&mut facts, 3, "question/id", Value::Uuid(3));
        fact(&mut facts, 3, "question/is-example", Value::Bool(false));
        assert_eq!(
            section_content(&facts, 1).unwrap(),
            Some(("example", 2, "Example title".into()))
        );
        assert_eq!(
            section_content(&facts, 2).unwrap(),
            Some(("example", 2, "Worked example".into()))
        );
        assert_eq!(section_content(&facts, 3).unwrap(), None);
        facts
            .get_mut(&2)
            .unwrap()
            .insert("question/is-example", vec![Value::Bool(false)]);
        assert!(section_content(&facts, 1).is_err());
    }
}
