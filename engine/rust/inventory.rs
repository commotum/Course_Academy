//! Batched inventory against the scheduler's captured database value.
use crate::{Result, assessment_sampling, learning, scheduling, schema::EntitySnapshot};
use chrono::{DateTime, Utc};
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};

/// Content-change signals for finite-pool conclusions, independent of learner
/// availability and database basis. The caller captures the bounded target,
/// owning/prerequisite topics, their canonical examples and owning lessons.
/// These are invalidation signals, not the publisher's approval source digest.
pub fn content_signals(s: &EntitySnapshot, kp: u64) -> Result<Value> {
    fn closure(s: &EntitySnapshot, roots: BTreeSet<u64>, source: bool, target: u64) -> Result<Value> {
        let mut pending = roots;
        let mut rows = BTreeMap::new();
        while let Some(id) = pending.pop_first() {
            if rows.contains_key(&id) { continue; }
            let original = s.entity(id)?;
            let mut row = original.clone();
            row.retain(|name, _| ["knowledge-point/", "topic/", "activity/", "step/", "question/",
                "answer-field/", "answer/", "multistep/", "multistep-step/", "assigned-problem/",
                "tutorial/", "text/", "image/", "video/"].iter().any(|prefix| name.starts_with(prefix)));
            row.remove("knowledge-point/question-generator");
            if source && row.contains_key("knowledge-point/id") {
                let imports: Vec<_> = if id == target { s.refs(id, "knowledge-point/questions")?.into_iter()
                    .filter(|q| s.entity(*q).is_ok_and(|q| q.contains_key("question/math-academy-id"))).collect() }
                    else { Vec::new() };
                row.insert("knowledge-point/questions".into(), json!(imports));
                pending.extend(imports);
            }
            for attr in ["knowledge-point/canonical-example", "topic/knowledge-points", "activity/steps",
                "step/content", "multistep/steps", "multistep-step/question", "assigned-problem/content",
                "question/answer-fields", "answer-field/choices", "answer-field/correct"] {
                if let Some(value) = original.get(attr) {
                    if let Value::Array(values) = value {
                        for value in values { pending.insert(s.eid(value)?); }
                    } else if !value.is_null() { pending.insert(s.eid(value)?); }
                }
            }
            // EDB cardinality-many order is not instructional sequence; linked
            // step/next remains in each record and preserves actual order.
            for value in row.values_mut() {
                if let Value::Array(values) = value { values.sort_by_key(Value::to_string); }
            }
            rows.insert(id, row);
        }
        Ok(json!(rows))
    }
    let pool: BTreeSet<_> = s.refs(kp, "knowledge-point/questions")?.into_iter().collect();
    let owners: BTreeSet<_> = s.owners(kp, "topic/knowledge-points")?.into_iter().collect();
    let mut roots = owners.clone();
    roots.insert(kp);
    roots.extend(s.refs(kp, "knowledge-point/key-prerequisites")?);
    for topic in owners {
        for activity in s.owners(topic, "activity/scope")? {
            if s.entity(activity)?.get("activity/type").map(|value| s.ident(value)).transpose()?.as_deref() == Some("activity.type/lesson") {
                roots.insert(activity);
            }
        }
    }
    let digest = |value: Value| -> Result<String> {
        Ok(format!("{:x}", Sha256::digest(serde_json::to_vec(&value).map_err(|e|e.to_string())?)))
    };
    Ok(json!({"source_sha256":digest(closure(s, roots, true, kp)?)?,
              "question_pool_sha256":digest(closure(s, pool, false, kp)?)?}))
}

pub fn triggers(
    s: &EntitySnapshot,
    l: u64,
    at: DateTime<Utc>,
) -> Result<BTreeMap<u64, BTreeSet<&'static str>>> {
    let mut triggers: BTreeMap<u64, BTreeSet<&str>> = BTreeMap::new();
    let scoped_lessons = if s.entity(l)?.get("learner/self-directed") == Some(&json!(true)) {
        let learned = learning::known_lesson_topics(s, l)?;
        Some(learning::study_lesson_scope(s, l)?.difference(&learned).copied().collect::<BTreeSet<_>>())
    } else {
        None
    };
    if let Some(topics) = &scoped_lessons {
        // Missing banks must still request supply; readiness only filters offers.
        for &topic in topics {
            triggers.entry(topic).or_default().insert("lesson");
        }
    } else {
        for attr in ["learner/queue", "learner/targets"] {
            for topic in s.refs(l, attr)? {
                triggers.entry(topic).or_default().insert("lesson");
            }
        }
    }
    for task in s.refs(l, "learner/activity")? {
        let state = scheduling::state(s, task)?;
        if !matches!(
            state.as_str(),
            "unlocked" | "started" | "paused"
        ) {
            continue;
        }
        let activity = s.reference(task, "learner-task/activity")?;
        let kind = crate::retrieval::kind(s, activity)?;
        if let Some(topic) = s.optional_ref(activity, "activity/scope")? {
            if kind == "lesson" && state == "unlocked"
                && scoped_lessons.as_ref().is_some_and(|scope| !scope.contains(&topic))
                && s.refs(task, "learner-task/remediation-for")?.is_empty()
            {
                continue;
            }
            if matches!(kind.as_str(), "lesson" | "review") {
                triggers
                    .entry(topic)
                    .or_default()
                    .insert(if kind == "lesson" { "lesson" } else { "review" });
            }
        } else if kind == "assessment" {
            for step in learning::lesson_steps(s, activity)? {
                triggers
                    .entry(s.topic_for_question(step.content)?)
                    .or_default()
                    .insert("assessment");
            }
        }
    }
    for topic in crate::retrieval::due_topics(s, l, at)? {
        triggers.entry(topic).or_default().insert("review");
    }
    let h = scheduling::lifecycle(s, l)?;
    for (&(_, topic), kind) in &h.repairs {
        triggers
            .entry(topic)
            .or_default()
            .insert(if kind == "lesson" { "lesson" } else { "review" });
    }
    // Admission precedes supply filtering: empty banks still produce jobs.
    if h.xp >= 120.0 {
        for (&topic, &learned) in &h.mastered {
            if at - learned >= chrono::Duration::hours(48) {
                triggers.entry(topic).or_default().insert("assessment");
            }
        }
    }
    for &original in &h.retakes {
        for step in learning::lesson_steps(s, s.reference(original, "learner-task/activity")?)? {
            triggers
                .entry(s.topic_for_question(step.content)?)
                .or_default()
                .insert("assessment");
        }
    }
    Ok(triggers)
}

pub fn requests(s: &EntitySnapshot, l: u64, at: DateTime<Utc>) -> Result<Vec<Value>> {
    let triggers = triggers(s, l, at)?;
    let h = scheduling::lifecycle(s, l)?;
    let seen = learning::unavailable_questions(s, l)?;
    let queued: BTreeSet<_> = s.refs(l, "learner/queue")?.into_iter().collect();
    let targeted: BTreeSet<_> = s.refs(l, "learner/targets")?.into_iter().collect();
    let mut jobs: BTreeMap<(u64, usize), Value> = BTreeMap::new();
    let mut priorities: BTreeMap<u64, f64> = BTreeMap::new();
    for task in s.refs(l, "learner/activity")? {
        let activity = s.reference(task, "learner-task/activity")?;
        if let Some(topic) = s.optional_ref(activity, "activity/scope")? {
            let p = s
                .entity(task)?
                .get("learner-task/priority")
                .and_then(Value::as_f64)
                .unwrap_or(0.0);
            priorities
                .entry(topic)
                .and_modify(|v| *v = v.max(p))
                .or_insert(p);
        }
    }
    if s.entity(l)?.get("learner/self-directed") == Some(&json!(true)) {
        for (topic, priority) in learning::inventory_priorities(s, l, at)? {
            priorities.entry(topic).and_modify(|p| *p = p.max(priority.priority))
                .or_insert(priority.priority);
        }
    } else if let Some(course) = s.optional_ref(l, "learner/course")? {
        for candidate in learning::plan_candidates_with_supply(s, l, course, at, 0, false)? {
            priorities.insert(candidate.topic, candidate.priority);
        }
    }
    for (topic, kinds) in triggers {
        let kps = s.refs(topic, "topic/knowledge-points")?;
        let available = assessment_sampling::pool(s, &kps, &seen)?;
        for &kp in &kps {
            let own = s.refs(kp, "knowledge-point/questions")?;
            let generator = s.optional_ref(kp, "knowledge-point/question-generator")?;
            let script = generator.and_then(|g| {
                s.entity(g)
                    .ok()?
                    .get("question-generator/script")?
                    .as_str()
                    .map(str::to_owned)
            });
            for b in 0..3 {
                let supported = own
                    .iter()
                    .any(|q| assessment_sampling::band(s, *q).ok().flatten() == Some(b));
                if !supported {
                    continue;
                }
                let count = available
                    .iter()
                    .filter(|q| {
                        assessment_sampling::band(s, **q).ok().flatten() == Some(b)
                            && (!kinds.contains("lesson") || own.contains(q))
                    })
                    .count();
                if count >= 5 {
                    continue;
                }
                // Topic-scoped shortages can be supplied by any supporting KP;
                // use one job per band unless this topic also needs KP stock.
                if !kinds.contains("lesson")
                    && kps.iter().copied().find(|k| {
                        s.refs(*k, "knowledge-point/questions")
                            .unwrap_or_default()
                            .iter()
                            .any(|q| assessment_sampling::band(s, *q).ok().flatten() == Some(b))
                    }) != Some(kp)
                {
                    continue;
                }
                let urgency = if count == 0 {
                    0
                } else if count == 1 {
                    1
                } else if count == 2 {
                    2
                } else {
                    3
                };
                jobs.insert((kp,b),json!({"knowledgePoint":kp,"topic":topic,"difficulty":(["easy","moderate","hard"][b]),"available":count,"missing":5-count,"urgency":urgency,"proximity":if h.repairs.keys().any(|(_,t)|*t==topic){0}else if queued.contains(&topic){1}else if targeted.contains(&topic){2}else{3},"priority":priorities.get(&topic).copied().unwrap_or(0.0),"activityTypes":kinds,"generator":generator,"script":script,"stage":if script.is_some(){"generate"}else{"create-generator"},"basis":s.basis_t}));
            }
            if own.is_empty()
                || generator.is_none()
                    && (0..3).any(|band| {
                        !own.iter()
                            .any(|q| assessment_sampling::band(s, *q).ok().flatten() == Some(band))
                    })
            {
                jobs.insert((kp,3),json!({"knowledgePoint":kp,"topic":topic,"difficulty":"unclassified","available":0,"missing":0,"urgency":0,"proximity":if queued.contains(&topic){1}else{2},"priority":priorities.get(&topic).copied().unwrap_or(0.0),"activityTypes":kinds,"stage":"classify","basis":s.basis_t}));
            }
        }
    }
    // A pooled topic can have ample stock while its original retake KP is
    // exhausted. Request exact-KP alternatives independently of pooled quotas.
    let mut originals: BTreeSet<_> = h.retakes.iter().copied().collect();
    for task in s.refs(l, "learner/activity")? {
        if matches!(
            scheduling::state(s, task)?.as_str(),
            "locked" | "unlocked" | "started" | "paused"
        ) {
            if let Some(original) = s.optional_ref(task, "learner-task/retake-of")? {
                originals.insert(original);
            }
        }
    }
    for original in originals {
        let steps = learning::lesson_steps(s, s.reference(original, "learner-task/activity")?)?;
        let mut excluded = seen.clone();
        excluded.extend(steps.iter().map(|st| st.content));
        for step in &steps {
            let kp = scheduling::original_kp(s, step.content)?;
            let topic = s.topic_for_question(step.content)?;
            let all = assessment_sampling::pool(s, &[kp], &BTreeSet::new())?;
            let fresh = assessment_sampling::pool(s, &[kp], &excluded)?;
            let generator = s.optional_ref(kp, "knowledge-point/question-generator")?;
            let script = generator.and_then(|g| {
                s.entity(g)
                    .ok()?
                    .get("question-generator/script")?
                    .as_str()
                    .map(str::to_owned)
            });
            for band in 0..3 {
                if !all
                    .iter()
                    .any(|q| assessment_sampling::band(s, *q).ok().flatten() == Some(band))
                    || fresh
                        .iter()
                        .any(|q| assessment_sampling::band(s, *q).ok().flatten() == Some(band))
                {
                    continue;
                }
                jobs.entry((kp,band)).or_insert(json!({"knowledgePoint":kp,"topic":topic,"difficulty":(["easy","moderate","hard"][band]),"available":0,"missing":1,"urgency":0,"proximity":0,"priority":priorities.get(&topic).copied().unwrap_or(0.0),"activityTypes":["assessment-retake"],"generator":generator,"script":script,"stage":if script.is_some(){"generate"}else{"create-generator"},"basis":s.basis_t}));
            }
        }
    }
    let mut jobs: Vec<_> = jobs.into_values().collect();
    jobs.sort_by_key(|j| {
        (
            j["urgency"].as_u64(),
            j["proximity"].as_u64(),
            j["knowledgePoint"].as_u64(),
        )
    });
    Ok(jobs)
}

/// Lesson admission is separate from the per-band replenishment target.
/// The five-question adaptive allowance needs five usable questions per skill
/// in total. Lessons can also use the selector's existing unrated fallback.
pub fn practice_pool(s: &EntitySnapshot, kps: &[u64], seen: &BTreeSet<u64>) -> Result<Vec<u64>> {
    let mut questions = BTreeSet::new();
    for &kp in kps {
        questions.extend(s.refs(kp, "knowledge-point/questions")?);
    }
    Ok(questions
        .into_iter()
        .filter(|q| !seen.contains(q) && learning::validate_practice_question(s, *q).is_ok())
        .collect())
}

pub fn lesson_shortages(
    s: &EntitySnapshot,
    kps: &[u64],
    seen: &BTreeSet<u64>,
) -> Result<Vec<(u64, usize)>> {
    let mut shortages = vec![];
    for &kp in kps {
        let count = s.refs(kp, "knowledge-point/questions")?
            .into_iter()
            .filter(|q| !seen.contains(q) && learning::validate_practice_question(s, *q).is_ok())
            .take(5)
            .count();
        if count < 5 {
            shortages.push((kp, count));
        }
    }
    Ok(shortages)
}

pub fn lesson_ready(s: &EntitySnapshot, kps: &[u64], seen: &BTreeSet<u64>) -> Result<bool> {
    Ok(lesson_shortages(s, kps, seen)?.is_empty())
}

/// Background replenishment quota, never an activity admission requirement.
/// Unobserved bands are classified separately; their absence is not proof that
/// a template can produce them. Reviews need five usable total questions and
/// assessments need one fresh rated question per eligible topic instead.
pub fn ready(s: &EntitySnapshot, kps: &[u64], seen: &BTreeSet<u64>, per_kp: bool) -> Result<bool> {
    let groups = if per_kp {
        kps.iter().map(|kp| vec![*kp]).collect::<Vec<_>>()
    } else {
        vec![kps.to_vec()]
    };
    for group in groups {
        let all = assessment_sampling::pool(s, &group, &BTreeSet::new())?;
        let fresh = assessment_sampling::pool(s, &group, seen)?;
        for band in 0..3 {
            if all
                .iter()
                .any(|q| assessment_sampling::band(s, *q).ok().flatten() == Some(band))
                && fresh
                    .iter()
                    .filter(|q| assessment_sampling::band(s, **q).ok().flatten() == Some(band))
                    .count()
                    < 5
            {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

/// Inspectable cadence/fallback state, captured alongside durable inventory jobs.
pub fn assessment_status(s: &EntitySnapshot, l: u64, at: DateTime<Utc>) -> Result<Value> {
    let h = scheduling::lifecycle(s, l)?;
    let eligible_topics=crate::retrieval::assessment_topics(s,l,at)?;
    let aged = eligible_topics.len();
    let pools = crate::retrieval::assessment_pools(s, l, at)?;
    let eligible = pools.len();
    let new_eligible = pools.keys().filter(|topic| !h.assessed.contains(topic)).count();
    let minimum_new = crate::retrieval::ASSESSMENT_MIN_NEW_TOPICS;
    let seen=learning::unavailable_questions(s,l)?;
    let ready = s.refs(l, "learner/activity")?.into_iter().any(|task| {
        s.optional_ref(task, "learner-task/retake-of")
            .ok()
            .flatten()
            .is_none()
            && matches!(
                scheduling::state(s, task).ok().as_deref(),
                Some("unlocked" | "locked" | "started" | "paused")
            )
            && s.optional_ref(task, "learner-task/activity")
                .ok()
                .flatten()
                .is_some_and(|a| {
                    crate::retrieval::kind(s, a).ok().as_deref() == Some("assessment")
                        && (matches!(
                            scheduling::state(s, task).ok().as_deref(),
                            Some("started" | "paused")
                        ) || crate::retrieval::ordinary_assessment_ready_with_context(
                            s,a,&seen,&h.assessed,&eligible_topics).unwrap_or(false))
                })
    });
    Ok(
        json!({"practiceXp":h.xp,"eligibleTopics":eligible,"agedLearnedTopics":aged,
            "newEligibleTopics":new_eligible,"minimumNewTopics":minimum_new,
            "availableQuestions":pools.values().map(Vec::len).sum::<usize>(),
            "ready":ready,"required":ready&&h.xp>=150.0,
            "unavailableReason":if h.xp>=120.0&&!ready {Some(if aged==0 {
                "Waiting for learned topics at least 48 hours old".to_owned()
            }else if eligible==0 {
                "Waiting for fresh rated questions for eligible topics".to_owned()
            }else if new_eligible<minimum_new {
                format!("Waiting for five eligible topics not previously assessed ({new_eligible}/{minimum_new} ready)")
            }else {"Preparing an assessment from eligible questions".to_owned()})}else{None}}),
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn finite_content_signals_follow_teaching_and_pool_not_learner_churn() -> Result<()> {
        let mut records: BTreeMap<_, _> = [
            (1, json!({"topic/id":"topic", "topic/knowledge-points":[2]})),
            (2, json!({"knowledge-point/id":"kp", "knowledge-point/title":"Compute a sum",
                       "knowledge-point/questions":[3], "knowledge-point/canonical-example":4})),
            (3, json!({"question/id":"generated", "question/problem":"Compute 2+1.",
                       "question/answer-fields":[5]})),
            (4, json!({"question/id":"canonical", "question/problem":"Compute 1+1."})),
            (5, json!({"answer-field/id":"field", "answer-field/choices":[6], "answer-field/correct":6})),
            (6, json!({"answer/id":"answer", "answer/value":"3"})),
            (7, json!({"activity/id":"lesson", "activity/type":8, "activity/scope":1, "activity/steps":[9]})),
            (8, json!({"db/ident":"activity.type/lesson"})),
            (9, json!({"step/id":"step", "step/content":10})),
            (10, json!({"tutorial/id":"tutorial", "tutorial/content":"Add the operands."})),
            (11, json!({"learner/id":"learner", "learner/activity":[]})),
        ].into_iter().map(|(id,row)|(id,row.as_object().unwrap().clone())).collect();
        let signal = |records: &BTreeMap<u64, crate::schema::Record>, basis| -> Result<Value> {
            content_signals(&EntitySnapshot::new(records.clone(), basis)?, 2)
        };
        let initial = signal(&records, 1)?;
        records.get_mut(&11).unwrap().insert("learner/activity".into(), json!([7]));
        assert_eq!(initial, signal(&records, 50)?);
        records.get_mut(&6).unwrap().insert("answer/value".into(), json!("4"));
        let changed_answer = signal(&records, 51)?;
        assert_eq!(initial["source_sha256"], changed_answer["source_sha256"]);
        assert_ne!(initial["question_pool_sha256"], changed_answer["question_pool_sha256"]);
        records.get_mut(&3).unwrap().insert("question/retired".into(), json!(true));
        assert_ne!(changed_answer["question_pool_sha256"], signal(&records, 52)?["question_pool_sha256"]);
        records.get_mut(&4).unwrap().insert("question/problem".into(), json!("Compute 1+2."));
        assert_ne!(initial["source_sha256"], signal(&records, 53)?["source_sha256"]);
        let before_tutorial = signal(&records, 53)?;
        records.get_mut(&10).unwrap().insert("tutorial/content".into(), json!("Recall addition without a supplied sum."));
        assert_ne!(before_tutorial["source_sha256"], signal(&records, 54)?["source_sha256"]);
        Ok(())
    }

    #[test]
    fn scoped_lesson_demand_includes_empty_banks_without_expanding_or_blocking_other_work() -> Result<()> {
        let mut s = crate::learning::tests::fixture();
        for topic in 500..=535 {
            s.entities.insert(topic, json!({"topic/id":format!("topic-{topic}"),
                "topic/next":if topic < 535 {vec![topic+1]} else {vec![]}}).as_object().unwrap().clone());
        }
        for topic in 700..=704 {
            s.entities.insert(topic, json!({"topic/id":format!("topic-{topic}")}).as_object().unwrap().clone());
        }
        s.entities.insert(900, json!({"knowledge-point/id":"key-only",
            "knowledge-point/key-prerequisites":[704]}).as_object().unwrap().clone());
        s.entities.get_mut(&533).unwrap().insert("topic/knowledge-points".into(),json!([900]));
        s.entities.insert(1200,json!({"db/ident":"learner-task.status/unlocked"}).as_object().unwrap().clone());
        s.entities.insert(1201,json!({"db/ident":"activity.type/review"}).as_object().unwrap().clone());
        s.entities.insert(800,json!({"progress/topic":532,"progress/learned":true}).as_object().unwrap().clone());
        let mut tasks = vec![];
        for (topic, status, kind, repair) in [
            (700,"unlocked","lesson",false), (701,"paused","lesson",false),
            (702,"unlocked","review",false), (703,"unlocked","lesson",true),
        ] {
            let task = 2000+topic;
            let activity = 3000+topic;
            tasks.push(task);
            s.entities.insert(activity,json!({"activity/type":format!("activity.type/{kind}"),
                "activity/scope":topic}).as_object().unwrap().clone());
            s.entities.insert(task,json!({"learner-task/activity":activity,
                "learner-task/status":format!("learner-task.status/{status}"),
                "learner-task/remediation-for":if repair {vec![9999]} else {vec![]}}).as_object().unwrap().clone());
        }
        s.entities.insert(9999,json!({}).as_object().unwrap().clone());
        s.entities.get_mut(&1).unwrap().extend(json!({"learner/self-directed":true,
            "learner/targets":[533],"learner/queue":[535],
            "learner/knowledge-profile":[800],"learner/activity":tasks}).as_object().unwrap().clone());
        s = EntitySnapshot::new(s.entities.into(),s.basis_t)?;
        let demands = triggers(&s,1,Utc::now())?;
        assert_eq!(demands.keys().copied().collect::<BTreeSet<_>>(),
            BTreeSet::from([531,533,534,535,701,702,703]));
        assert_eq!(demands[&531],BTreeSet::from(["lesson"]));
        assert_eq!(demands[&702],BTreeSet::from(["review"]));
        assert!(!demands.contains_key(&530),"depth-three preparation stays outside demand");
        assert!(!demands.contains_key(&532),"learned topics do not request new lessons");
        assert!(!demands.contains_key(&704),"hidden KP prerequisites do not widen graph scope");
        s.entities.insert(801,json!({"progress/topic":533,"progress/learned":false,
            "progress/repetitions":1.0}).as_object().unwrap().clone());
        s.entities.insert(802,json!({"progress/topic":534,
            "progress/repetitions":0.5}).as_object().unwrap().clone());
        s.entities.get_mut(&1).unwrap().insert("learner/knowledge-profile".into(),json!([800,801,802]));
        let demands = triggers(&s,1,Utc::now())?;
        assert!(!demands.contains_key(&533),"band one never requests an ordinary new lesson");
        assert!(demands[&534].contains("lesson"),"fractional progress below one remains new");
        Ok(())
    }

    #[test]
    fn lesson_admission_uses_total_supply_while_replenishment_still_checks_bands() -> Result<()> {
        let mut s = crate::learning::tests::fixture();
        for (id, band) in [(1100, "easy"), (1101, "moderate"), (1102, "hard")] {
            s.entities.insert(
                id,
                json!({"db/ident":format!("question.difficulty/{band}")})
                    .as_object()
                    .unwrap()
                    .clone(),
            );
        }
        let mut kps = vec![];
        let mut banks = vec![];
        for (i, counts) in [[5, 3, 2], [5, 2, 0], [2, 5, 2], [4, 2, 2]]
            .iter()
            .enumerate()
        {
            let kp = 5000 + i as u64;
            kps.push(kp);
            let mut bank = vec![];
            for (band, count) in counts.iter().enumerate() {
                for n in 0..*count {
                    let q = 10000 + i as u64 * 100 + band as u64 * 20 + n;
                    let mut row = s.entities[&100].clone();
                    row.insert("question/id".into(), json!(format!("practice-{q}")));
                    row.insert("question/difficulty".into(), json!(1100 + band as u64));
                    s.entities.insert(q, row);
                    bank.push(q);
                }
            }
            s.entities.insert(kp,json!({"knowledge-point/id":format!("skill-{kp}"),"knowledge-point/questions":bank}).as_object().unwrap().clone());
            banks.push(bank);
        }
        s = EntitySnapshot::new(s.entities.into(), s.basis_t)?;
        assert!(lesson_ready(&s, &kps, &BTreeSet::new())?);
        assert!(!ready(&s, &kps, &BTreeSet::new(), true)?);
        let seen = banks[1][..3].iter().copied().collect();
        assert_eq!(lesson_shortages(&s, &kps, &seen)?, vec![(kps[1], 4)]);
        Ok(())
    }

    #[test]
    fn lesson_admission_excludes_seen_examples_duplicates_and_ungradable_questions() -> Result<()> {
        let mut s = crate::learning::tests::fixture();
        s.entities.get_mut(&41).unwrap().insert(
            "knowledge-point/questions".into(),
            json!([100, 101, 102, 103, 104, 104, 42]),
        );
        s = EntitySnapshot::new(s.entities.into(), s.basis_t)?;
        assert!(lesson_ready(&s, &[41], &BTreeSet::new())?);
        assert_eq!(
            lesson_shortages(&s, &[41], &BTreeSet::from([100]))?,
            vec![(41, 4)]
        );
        s.entities
            .get_mut(&104)
            .unwrap()
            .remove("question/answer-fields");
        assert_eq!(
            lesson_shortages(&s, &[41], &BTreeSet::new())?,
            vec![(41, 4)]
        );
        Ok(())
    }
}
