//! Batched inventory against the scheduler's captured database value.
use crate::{Result, assessment_sampling, learning, scheduling, schema::EntitySnapshot};
use chrono::{DateTime, Utc};
use serde_json::{Value, json};
use std::collections::{BTreeMap, BTreeSet};

pub fn triggers(
    s: &EntitySnapshot,
    l: u64,
    at: DateTime<Utc>,
) -> Result<BTreeMap<u64, BTreeSet<&'static str>>> {
    let mut triggers: BTreeMap<u64, BTreeSet<&str>> = BTreeMap::new();
    for attr in ["learner/queue", "learner/targets"] {
        for topic in s.refs(l, attr)? {
            triggers.entry(topic).or_default().insert("lesson");
        }
    }
    for task in s.refs(l, "learner/activity")? {
        if !matches!(
            scheduling::state(s, task)?.as_str(),
            "unlocked" | "started" | "paused"
        ) {
            continue;
        }
        let activity = s.reference(task, "learner-task/activity")?;
        let kind = crate::retrieval::kind(s, activity)?;
        if let Some(topic) = s.optional_ref(activity, "activity/scope")? {
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
    if let Some(course) = s.optional_ref(l, "learner/course")? {
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
        let count = practice_pool(s, &[kp], seen)?.len();
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
    let aged = crate::retrieval::assessment_topics(s, l, at)?.len();
    let pools = crate::retrieval::assessment_pools(s, l, at)?;
    let eligible = pools.len();
    let new_eligible = pools.keys().filter(|topic| !h.assessed.contains(topic)).count();
    let minimum_new = crate::retrieval::ASSESSMENT_MIN_NEW_TOPICS;
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
                        ) || crate::retrieval::ordinary_assessment_ready(s, l, a, at).unwrap_or(false))
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
