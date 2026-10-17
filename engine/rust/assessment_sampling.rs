//! Topic-weighted assessment draws with bounded resampling and duration lookahead.
use crate::{Result, learning, question_selection, scheduling, schema::EntitySnapshot};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};

pub fn band(s: &EntitySnapshot, q: u64) -> Result<Option<usize>> {
    let Some(v) = s.entity(q)?.get("question/difficulty") else {
        return Ok(None);
    };
    Ok(["easy", "moderate", "hard"]
        .iter()
        .position(|b| s.ident(v).ok().as_deref() == Some(&format!("question.difficulty/{b}"))))
}
pub fn seconds(s: &EntitySnapshot, q: u64) -> Result<f64> {
    Ok((band(s, q)?.ok_or("Assessment requires a rated question")? + 1) as f64 * 60.0)
}
fn draw(seed: &str) -> f64 {
    let d = Sha256::digest(seed.as_bytes());
    (u64::from_be_bytes(d[..8].try_into().unwrap()) >> 11) as f64 / (1u64 << 53) as f64
}
pub fn weighted(values: &[(u64, f64)], seed: &str) -> Option<u64> {
    let total: f64 = values.iter().map(|(_, w)| w).sum();
    if total <= 0.0 {
        return None;
    }
    let mut n = draw(seed) * total;
    for &(v, w) in values {
        if n < w {
            return Some(v);
        }
        n -= w;
    }
    values.last().map(|v| v.0)
}
pub fn pool(s: &EntitySnapshot, kps: &[u64], seen: &BTreeSet<u64>) -> Result<Vec<u64>> {
    let mut qs = BTreeSet::new();
    for &kp in kps {
        qs.extend(s.refs(kp, "knowledge-point/questions")?);
    }
    Ok(qs
        .into_iter()
        .filter(|q| {
            !seen.contains(q)
                && learning::validate_practice_question(s, *q).is_ok()
                && band(s, *q).ok().flatten().is_some()
        })
        .collect())
}
const BUDGET_MINUTES: usize = 15;
const RESAMPLE_ATTEMPTS: usize = 64;
type Reachable = [[bool; 8]; BUDGET_MINUTES + 1];

/// Reachable duration/band sets, taking at most one question per topic.
/// Retakes must take every original topic; ordinary assessments may omit topics.
fn reachable(masks: &[u8], minutes: usize, all: bool) -> Reachable {
    let mut states = [[false; 8]; BUDGET_MINUTES + 1];
    states[0][0] = true;
    for &mask in masks {
        let mut next = if all {
            [[false; 8]; BUDGET_MINUTES + 1]
        } else {
            states
        };
        for cost in 0..=minutes {
            for have in 0..8 {
                if !states[cost][have] {
                    continue;
                }
                for b in 0..3 {
                    if mask & (1 << b) != 0 && cost + b + 1 <= minutes {
                        next[cost + b + 1][have | (1 << b)] = true;
                    }
                }
            }
        }
        states = next;
    }
    states
}

fn completion(states: &Reachable, remaining: usize, have: u8, coverage: u32, exact: bool) -> bool {
    states.iter().enumerate().any(|(minutes, bands)| {
        minutes <= remaining
            && (!exact || minutes == remaining)
            && bands
                .iter()
                .enumerate()
                .any(|(mask, possible)| *possible && (have | mask as u8).count_ones() == coverage)
    })
}

struct Draft {
    questions: Vec<u64>,
    minutes: usize,
}

/// A weighted draft; exact is used only by the bounded-resampling fallback.
/// It fixes a duration, never a difficulty-count combination or topic order.
fn draft(
    s: &EntitySnapshot,
    pools: &BTreeMap<u64, Vec<u64>>,
    masks: &BTreeMap<u64, u8>,
    weights: [f64; 3],
    topic_weights: &BTreeMap<u64, f64>,
    fixed: bool,
    coverage: u32,
    exact: Option<usize>,
    seed: &str,
) -> Result<Draft> {
    let mut remaining = masks.clone();
    let mut selected = vec![];
    let mut minutes = exact.unwrap_or(BUDGET_MINUTES);
    let budget = minutes;
    let mut have = 0u8;
    while !remaining.is_empty() && minutes > 0 {
        let slot = selected.len();
        let mut choices = BTreeMap::new();
        // Topics with the same available bands have the same lookahead. Reuse
        // those seven possible states instead of recomputing for each topic.
        let mut feasible_bands = BTreeMap::new();
        for (&topic, &mask) in &remaining {
            let allowed_mask = feasible_bands.entry(mask).or_insert_with(|| {
                let other_masks = remaining
                    .iter()
                    .filter_map(|(t, m)| (*t != topic).then_some(*m))
                    .collect::<Vec<_>>();
                let states = reachable(&other_masks, minutes, fixed);
                (0..3)
                    .filter(|b| {
                        mask & (1 << b) != 0
                            && b + 1 <= minutes
                            && completion(
                                &states,
                                minutes - b - 1,
                                have | (1 << b),
                                coverage,
                                exact.is_some(),
                            )
                    })
                    .fold(0u8, |allowed, b| allowed | (1 << b))
            });
            let allowed = pools[&topic]
                .iter()
                .copied()
                .filter(|q| {
                    let b = band(s, *q).ok().flatten().unwrap();
                    *allowed_mask & (1 << b) != 0
                })
                .collect::<Vec<_>>();
            if !allowed.is_empty() {
                choices.insert(topic, allowed);
            }
        }
        let candidates = choices
            .keys()
            .map(|t| (*t, topic_weights.get(t).copied().unwrap_or(1.0)))
            .collect::<Vec<_>>();
        let Some(topic) = weighted(&candidates, &format!("{seed}-topic-{slot}")) else {
            break;
        };
        let mut distribution = weights;
        // Coverage, fixed-topic completion and the final duration guarantee can
        // require a band whose configured weight is zero. Otherwise preserve
        // the database distribution, renormalized over feasible choices.
        if choices[&topic]
            .iter()
            .all(|q| distribution[band(s, *q).unwrap().unwrap()] == 0.0)
        {
            distribution = [1.0; 3];
        }
        let q = question_selection::select(
            s,
            &choices[&topic],
            Some(distribution),
            &format!("{seed}-question-{slot}"),
        )?
        .ok_or("No feasible rated question in assessment sampler")?;
        let b = band(s, q)?.unwrap();
        minutes -= b + 1;
        have |= 1 << b;
        selected.push(q);
        remaining.remove(&topic);
    }
    if have.count_ones() != coverage
        || fixed && !remaining.is_empty()
        || exact.is_some() && minutes != 0
    {
        return Err("Assessment sampler lost completion feasibility".into());
    }
    Ok(Draft {
        questions: selected,
        minutes: budget - minutes,
    })
}

pub fn assemble(
    s: &EntitySnapshot,
    l: u64,
    pools: BTreeMap<u64, Vec<u64>>,
    weights: [f64; 3],
    topic_weights: BTreeMap<u64, f64>,
    fixed: bool,
    seed: &str,
) -> Result<Vec<u64>> {
    if weights.iter().any(|w| !w.is_finite() || *w < 0.0)
        || !weights.iter().sum::<f64>().is_finite()
        || weights.iter().sum::<f64>() <= 0.0
    {
        return Err("invalid question-weight distribution".into());
    }
    if topic_weights.values().any(|w| !w.is_finite() || *w <= 0.0)
        || !topic_weights.values().sum::<f64>().is_finite()
    {
        return Err("assessment topic weights must be positive and finite".into());
    }
    let masks = pools
        .iter()
        .map(|(&topic, qs)| {
            let mut mask = 0u8;
            for &q in qs {
                mask |= 1 << band(s, q)?.ok_or("Assessment requires a rated question")?;
            }
            Ok((topic, mask))
        })
        .collect::<Result<BTreeMap<_, _>>>()?;
    let states = reachable(
        &masks.values().copied().collect::<Vec<_>>(),
        BUDGET_MINUTES,
        fixed,
    );
    // Full coverage has priority when possible. Scarce/overlapping topic bands
    // otherwise retain the maximum achievable coverage without blocking a quiz.
    let optimum = states
        .iter()
        .enumerate()
        .flat_map(|(minutes, bands)| {
            bands
                .iter()
                .enumerate()
                .filter_map(move |(mask, possible)| {
                    (*possible && minutes > 0).then_some(((mask as u8).count_ones(), minutes))
                })
        })
        .max();
    let Some((coverage, target)) = optimum else {
        return Ok(vec![]);
    };
    let mut best = None;
    for attempt in 0..RESAMPLE_ATTEMPTS {
        let sampled = draft(
            s,
            &pools,
            &masks,
            weights,
            &topic_weights,
            fixed,
            coverage,
            None,
            &format!("{seed}-attempt-{attempt}"),
        )?;
        let reached_target = sampled.minutes == target;
        if best
            .as_ref()
            .is_none_or(|previous: &Draft| sampled.minutes > previous.minutes)
        {
            best = Some(sampled);
        }
        if reached_target {
            break;
        }
    }
    let mut best = best.unwrap();
    if best.minutes < target {
        best = draft(
            s,
            &pools,
            &masks,
            weights,
            &topic_weights,
            fixed,
            coverage,
            Some(target),
            &format!("{seed}-duration-fallback"),
        )?;
    }
    // Deterministic shuffle: exact retries preserve the prepared route.
    best.questions
        .sort_by_key(|q| Sha256::digest(format!("{seed}-shuffle-{q}")).to_vec());
    let _ = l;
    Ok(best.questions)
}
pub fn retake(
    s: &EntitySnapshot,
    l: u64,
    original: u64,
    seen: &BTreeSet<u64>,
    weights: [f64; 3],
    seed: &str,
) -> Result<Vec<u64>> {
    let activity = s.reference(original, "learner-task/activity")?;
    let mut excluded = seen.clone();
    excluded.extend(
        learning::lesson_steps(s, activity)?
            .iter()
            .map(|step| step.content),
    );
    let mut pools = BTreeMap::new();
    for step in learning::lesson_steps(s, activity)? {
        pools.insert(
            s.topic_for_question(step.content)?,
            pool(s, &[scheduling::original_kp(s, step.content)?], &excluded)?,
        );
    }
    assemble(s, l, pools, weights, BTreeMap::new(), true, seed)
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    fn fixture(masks: &[u8]) -> (EntitySnapshot, BTreeMap<u64, Vec<u64>>) {
        let mut records = BTreeMap::new();
        for (id, ident) in [
            (1, "question.difficulty/easy"),
            (2, "question.difficulty/moderate"),
            (3, "question.difficulty/hard"),
            (4, "answer-field.type/blank"),
            (5, "answer.type/math"),
            (6, "activity.type/assessment"),
        ] {
            records.insert(id, json!({"db/ident":ident}).as_object().unwrap().clone());
        }
        let mut pools = BTreeMap::new();
        for (index, &mask) in masks.iter().enumerate() {
            let topic = 100 + index as u64;
            let kp = 1000 + index as u64;
            let mut qs = vec![];
            for b in 0..3u64 {
                if mask & (1 << b) == 0 {
                    continue;
                }
                for copy in 0..2 {
                    let q = 10000 + index as u64 * 100 + b * 10 + copy;
                    let field = q * 10;
                    records.insert(q, json!({"question/id":format!("q-{q}"),
                        "question/difficulty":b+1, "question/problem":"Square 2.",
                        "question/worked-solution":"2 times 2 is 4.", "question/answer-fields":[field]
                    }).as_object().unwrap().clone());
                    records.insert(
                        field,
                        json!({"answer-field/id":format!("field-{field}"),
                            "answer-field/type":4,"answer-field/key":"answer",
                            "answer-field/choices":[field+1],"answer-field/correct":field+1
                        })
                        .as_object()
                        .unwrap()
                        .clone(),
                    );
                    records.insert(
                        field + 1,
                        json!({"answer/id":format!("answer-{field}"),
                        "answer/type":5,"answer/value":"4"})
                        .as_object()
                        .unwrap()
                        .clone(),
                    );
                    qs.push(q);
                }
            }
            records.insert(
                topic,
                json!({"topic/id":format!("topic-{topic}"),
                "topic/knowledge-points":[kp]})
                .as_object()
                .unwrap()
                .clone(),
            );
            records.insert(
                kp,
                json!({"knowledge-point/id":format!("kp-{kp}"),
                "knowledge-point/questions":qs})
                .as_object()
                .unwrap()
                .clone(),
            );
            pools.insert(topic, qs);
        }
        (EntitySnapshot::new(records, 1).unwrap(), pools)
    }

    fn result(s: &EntitySnapshot, qs: &[u64]) -> (usize, u32) {
        let minutes = qs
            .iter()
            .map(|q| seconds(s, *q).unwrap() as usize / 60)
            .sum();
        let mask = qs
            .iter()
            .fold(0u8, |mask, q| mask | (1 << band(s, *q).unwrap().unwrap()));
        let topics = qs
            .iter()
            .map(|q| s.topic_for_question(*q).unwrap())
            .collect::<BTreeSet<_>>();
        assert_eq!(topics.len(), qs.len(), "One question per distinct topic");
        (minutes, mask.count_ones())
    }

    #[test]
    fn replay_is_deterministic_and_exact_fifteen_is_reached_when_feasible() {
        let (s, pools) = fixture(&[7; 8]);
        for seed in ["one", "two", "three"] {
            let first = assemble(
                &s,
                1,
                pools.clone(),
                [50.0, 40.0, 10.0],
                BTreeMap::new(),
                false,
                seed,
            )
            .unwrap();
            let replay = assemble(
                &s,
                1,
                pools.clone(),
                [50.0, 40.0, 10.0],
                BTreeMap::new(),
                false,
                seed,
            )
            .unwrap();
            assert_eq!(first, replay);
            assert_eq!(result(&s, &first), (15, 3));
        }
    }

    #[test]
    fn supplied_topic_weights_remain_soft_priorities_without_replacement() {
        let (s, pools) = fixture(&[4; 10]);
        let topic_weights = pools
            .keys()
            .map(|t| (*t, if *t < 105 { 4.0 } else { 1.0 }))
            .collect::<BTreeMap<_, _>>();
        let mut preferred = 0;
        for seed in 0..200 {
            let qs = assemble(
                &s,
                1,
                pools.clone(),
                [50.0, 40.0, 10.0],
                topic_weights.clone(),
                false,
                &format!("weighted-{seed}"),
            )
            .unwrap();
            assert_eq!(result(&s, &qs), (15, 1));
            preferred += qs
                .iter()
                .filter(|q| s.topic_for_question(**q).unwrap() < 105)
                .count();
        }
        assert!(
            preferred > 620 && preferred < 850,
            "preferred topics selected {preferred}/1000 times"
        );
    }

    #[test]
    fn bounded_drafts_are_actually_resampled_before_duration_fallback() {
        let (s, pools) = fixture(&[7; 8]);
        let masks = pools.keys().map(|t| (*t, 7)).collect::<BTreeMap<_, _>>();
        let weights = [50.0, 40.0, 10.0];
        let seed = (0..100)
            .map(|n| format!("resample-{n}"))
            .find(|seed| {
                draft(
                    &s,
                    &pools,
                    &masks,
                    weights,
                    &BTreeMap::new(),
                    false,
                    3,
                    None,
                    &format!("{seed}-attempt-0"),
                )
                .unwrap()
                .minutes
                    < 15
                    && (1..RESAMPLE_ATTEMPTS).any(|attempt| {
                        draft(
                            &s,
                            &pools,
                            &masks,
                            weights,
                            &BTreeMap::new(),
                            false,
                            3,
                            None,
                            &format!("{seed}-attempt-{attempt}"),
                        )
                        .unwrap()
                        .minutes
                            == 15
                    })
            })
            .expect("fixture should exercise a shorter initial draft followed by an exact draft");
        let mut expected = (0..RESAMPLE_ATTEMPTS)
            .map(|attempt| {
                draft(
                    &s,
                    &pools,
                    &masks,
                    weights,
                    &BTreeMap::new(),
                    false,
                    3,
                    None,
                    &format!("{seed}-attempt-{attempt}"),
                )
                .unwrap()
            })
            .find(|candidate| candidate.minutes == 15)
            .unwrap()
            .questions;
        expected.sort_by_key(|q| Sha256::digest(format!("{seed}-shuffle-{q}")).to_vec());
        assert_eq!(
            assemble(&s, 1, pools, weights, BTreeMap::new(), false, &seed).unwrap(),
            expected
        );
    }

    #[test]
    fn fallback_finds_best_short_duration_and_does_not_retry_forever() {
        let (s, pools) = fixture(&[7; 5]);
        // Every natural weighted draft prefers easy where coverage permits,
        // so reaching the twelve-minute optimum requires the guided fallback.
        let qs = assemble(
            &s,
            1,
            pools,
            [100.0, 0.0, 0.0],
            BTreeMap::new(),
            false,
            "short",
        )
        .unwrap();
        assert_eq!(result(&s, &qs), (12, 3));
        assert_eq!(qs.len(), 5);
        let (s, pools) = fixture(&[7; 6]);
        let qs = assemble(
            &s,
            1,
            pools,
            [100.0, 0.0, 0.0],
            BTreeMap::new(),
            false,
            "exact-fallback",
        )
        .unwrap();
        assert_eq!(result(&s, &qs), (15, 3));
    }

    #[test]
    fn missing_bands_and_overlapping_scarce_topics_keep_best_feasible_coverage() {
        for (masks, expected) in [
            (vec![1; 8], (8, 1)),
            (vec![3; 2], (3, 2)),
            (vec![5, 6], (5, 2)),
            (vec![7; 3], (6, 3)),
            (vec![2, 4, 4, 4, 4, 4], (14, 2)),
        ] {
            let (s, pools) = fixture(&masks);
            let qs = assemble(
                &s,
                1,
                pools,
                [50.0, 40.0, 10.0],
                BTreeMap::new(),
                false,
                "scarce",
            )
            .unwrap();
            assert_eq!(result(&s, &qs), expected, "masks={masks:?}");
        }
    }

    #[test]
    fn retake_preserves_every_original_topic_and_kp_and_excludes_original_questions() {
        let (mut s, pools) = fixture(&[1, 3, 4, 7]);
        let original = pools.values().take(3).map(|qs| qs[0]).collect::<Vec<_>>();
        for (i, q) in original.iter().enumerate() {
            let mut step = json!({"step/id":format!("step-{i}"),"step/content":q});
            if i < 2 {
                step["step/next"] = json!(61 + i);
            }
            s.entities
                .insert(60 + i as u64, step.as_object().unwrap().clone());
        }
        s.entities.insert(
            50,
            json!({"activity/id":"original-assessment","activity/type":6,
            "activity/steps":[60,61,62],"activity/first-step":60})
            .as_object()
            .unwrap()
            .clone(),
        );
        s.entities.insert(
            51,
            json!({"learner-task/id":"original-task","learner-task/activity":50})
                .as_object()
                .unwrap()
                .clone(),
        );
        let s = EntitySnapshot::new(s.entities.into(), 1).unwrap();
        let qs = retake(&s, 1, 51, &BTreeSet::new(), [45.0, 40.0, 15.0], "retake").unwrap();
        assert_eq!(result(&s, &qs), (6, 3));
        assert!(qs.iter().all(|q| !original.contains(q)));
        assert_eq!(
            qs.iter()
                .map(|q| scheduling::original_kp(&s, *q).unwrap())
                .collect::<BTreeSet<_>>(),
            BTreeSet::from([1000, 1001, 1002])
        );
        let seen = pools[&101].iter().copied().collect();
        assert!(
            retake(&s, 1, 51, &seen, [45.0, 40.0, 15.0], "missing-alternative")
                .unwrap()
                .is_empty()
        );
    }

    #[test]
    fn fixed_topics_with_missing_bands_are_allowed_but_over_budget_is_not() {
        let (s, pools) = fixture(&[1, 3]);
        let qs = assemble(
            &s,
            1,
            pools,
            [45.0, 40.0, 15.0],
            BTreeMap::new(),
            true,
            "fixed",
        )
        .unwrap();
        assert_eq!(result(&s, &qs), (3, 2));
        let (s, pools) = fixture(&[4; 6]);
        assert!(
            assemble(
                &s,
                1,
                pools,
                [45.0, 40.0, 15.0],
                BTreeMap::new(),
                true,
                "too-long"
            )
            .unwrap()
            .is_empty()
        );
    }
}
