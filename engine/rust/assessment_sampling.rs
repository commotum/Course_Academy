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
                && !s.is_example(*q)
                && learning::validate_question(s, *q).is_ok()
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
        let mut next = if all { [[false; 8]; BUDGET_MINUTES + 1] } else { states };
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

fn completion(states: &Reachable, have: u8, coverage: u32, exact: Option<usize>) -> bool {
    states.iter().enumerate().any(|(minutes, bands)| {
        exact.is_none_or(|target| minutes == target)
            && bands.iter().enumerate().any(|(mask, possible)| {
                *possible && (have | mask as u8).count_ones() == coverage
            })
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
        let mut completions = BTreeMap::new();
        for (&topic, &mask) in &remaining {
            let states = completions.entry(mask).or_insert_with(|| {
                let other_masks = remaining.iter()
                    .filter_map(|(t, m)| (*t != topic).then_some(*m))
                    .collect::<Vec<_>>();
                reachable(&other_masks, minutes, fixed)
            });
            let allowed = pools[&topic].iter().copied().filter(|q| {
                let b = band(s, *q).ok().flatten().unwrap();
                b + 1 <= minutes && completion(
                    states,
                    have | (1 << b),
                    coverage,
                    exact.map(|_| minutes - b - 1),
                ) && (exact.is_some() || states.iter().enumerate().any(|(cost, bands)| {
                    cost <= minutes - b - 1 && bands.iter().enumerate().any(|(m, possible)| {
                        *possible && (have | (1 << b) | m as u8).count_ones() == coverage
                    })
                }))
            }).collect::<Vec<_>>();
            if !allowed.is_empty() {
                choices.insert(topic, allowed);
            }
        }
        let candidates = choices.keys().map(|t| (*t, topic_weights.get(t).copied().unwrap_or(1.0)))
            .collect::<Vec<_>>();
        let Some(topic) = weighted(&candidates, &format!("{seed}-topic-{slot}")) else {
            break;
        };
        let mut distribution = weights;
        // Coverage, fixed-topic completion and the final duration guarantee can
        // require a band whose configured weight is zero. Otherwise preserve
        // the database distribution, renormalized over feasible choices.
        if choices[&topic].iter().all(|q| distribution[band(s, *q).unwrap().unwrap()] == 0.0) {
            distribution = [1.0; 3];
        }
        let q = question_selection::select(
            s, &choices[&topic], Some(distribution), &format!("{seed}-question-{slot}"),
        )?.ok_or("No feasible rated question in assessment sampler")?;
        let b = band(s, q)?.unwrap();
        minutes -= b + 1;
        have |= 1 << b;
        selected.push(q);
        remaining.remove(&topic);
    }
    if have.count_ones() != coverage || fixed && !remaining.is_empty()
        || exact.is_some() && minutes != 0 {
        return Err("Assessment sampler lost completion feasibility".into());
    }
    Ok(Draft { questions: selected, minutes: budget - minutes })
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
        || !weights.iter().sum::<f64>().is_finite() || weights.iter().sum::<f64>() <= 0.0 {
        return Err("invalid question-weight distribution".into());
    }
    if topic_weights.values().any(|w| !w.is_finite() || *w <= 0.0)
        || !topic_weights.values().sum::<f64>().is_finite() {
        return Err("assessment topic weights must be positive and finite".into());
    }
    let masks = pools.iter().map(|(&topic, qs)| {
        let mut mask = 0u8;
        for &q in qs {
            mask |= 1 << band(s, q)?.ok_or("Assessment requires a rated question")?;
        }
        Ok((topic, mask))
    }).collect::<Result<BTreeMap<_, _>>>()?;
    let states = reachable(&masks.values().copied().collect::<Vec<_>>(), BUDGET_MINUTES, fixed);
    // Full coverage has priority when possible. Scarce/overlapping topic bands
    // otherwise retain the maximum achievable coverage without blocking a quiz.
    let optimum = states.iter().enumerate().flat_map(|(minutes, bands)| {
        bands.iter().enumerate().filter_map(move |(mask, possible)| {
            (*possible && minutes > 0).then_some(((mask as u8).count_ones(), minutes))
        })
    }).max();
    let Some((coverage, target)) = optimum else { return Ok(vec![]) };
    let mut best = None;
    for attempt in 0..RESAMPLE_ATTEMPTS {
        let sampled = draft(s, &pools, &masks, weights, &topic_weights, fixed, coverage, None,
            &format!("{seed}-attempt-{attempt}"))?;
        let reached_target = sampled.minutes == target;
        if best.as_ref().is_none_or(|previous: &Draft| sampled.minutes > previous.minutes) {
            best = Some(sampled);
        }
        if reached_target {
            break;
        }
    }
    let mut best = best.unwrap();
    if best.minutes < target {
        best = draft(s, &pools, &masks, weights, &topic_weights, fixed, coverage, Some(target),
            &format!("{seed}-duration-fallback"))?;
    }
    // Deterministic shuffle: exact retries preserve the prepared route.
    best.questions.sort_by_key(|q| Sha256::digest(format!("{seed}-shuffle-{q}")).to_vec());
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
    #[test]
    fn lookahead_reserves_time_and_required_bands() {
        assert!(!feasible(&[1, 1, 1, 1], 3, 0, true));
        assert!(feasible(&[1, 1, 1, 1], 4, 0, true));
        assert!(!feasible(&[1, 1], 10, 4, true));
        assert!(feasible(&[1, 2, 4], 6, 7, true));
        assert!(!feasible(&[1, 2, 4], 5, 7, true));
        assert!(feasible(&[1, 2, 4, 4], 6, 7, false));
    }
}
