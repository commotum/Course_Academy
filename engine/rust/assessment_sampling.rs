//! Difficulty-first, topic-weighted sampling with a small feasibility lookahead.
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
/// Minimal remaining duration for a feasible assignment covering missing bands.
/// Optional topics may be omitted; retakes must use every fixed topic.
fn feasible(masks: &[u8], minutes: usize, needed: u8, all: bool) -> bool {
    let mut states = BTreeSet::from([(0usize, 0u8)]);
    for &mask in masks {
        let mut next = if all { BTreeSet::new() } else { states.clone() };
        for &(cost, have) in &states {
            for b in 0..3 {
                if mask & (1 << b) != 0 && cost + b + 1 <= minutes {
                    next.insert((cost + b + 1, have | (1 << b)));
                }
            }
        }
        states = next;
    }
    states.iter().any(|(_, have)| have & needed == needed)
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
    let mut pools = pools;
    let mut selected = vec![];
    let mut minutes = 15;
    let mut have = 0u8;
    let mask = |qs: &Vec<u64>| {
        qs.iter()
            .filter_map(|q| band(s, *q).ok().flatten())
            .fold(0, |m, b| m | (1 << b))
    };
    if !feasible(
        &pools.values().map(mask).collect::<Vec<_>>(),
        minutes,
        7,
        fixed,
    ) {
        return Ok(vec![]);
    }
    // Required-band slots are chosen first for ordinary assessments; retakes
    // instead preserve completion feasibility on every fixed-topic draw.
    let mut required = vec![0usize, 1, 2];
    while !pools.is_empty() && minutes > 0 {
        let slot = selected.len();
        let required_band = if !fixed && !required.is_empty() {
            Some(required[0])
        } else {
            None
        };
        let mut choices = BTreeMap::new();
        for (&topic, qs) in &pools {
            let remaining: Vec<_> = pools
                .iter()
                .filter(|(t, _)| **t != topic)
                .map(|(_, qs)| mask(qs))
                .collect();
            let allowed: Vec<_> = qs
                .iter()
                .copied()
                .filter(|q| {
                    let b = band(s, *q).ok().flatten().unwrap();
                    (fixed || required_band.is_some() || weights[b] > 0.0)
                        && required_band.is_none_or(|r| r == b)
                        && b + 1 <= minutes
                        && feasible(&remaining, minutes - b - 1, 7 & !(have | (1 << b)), fixed)
                })
                .collect();
            if !allowed.is_empty() {
                choices.insert(topic, allowed);
            }
        }
        let Some(topic) = weighted(
            &choices
                .keys()
                .map(|t| (*t, topic_weights.get(t).copied().unwrap_or(1.0)))
                .collect::<Vec<_>>(),
            &format!("{seed}-topic-{slot}"),
        ) else {
            break;
        };
        let mut selected_weights = required_band
            .map(|b| {
                let mut w = [0.0; 3];
                w[b] = 1.0;
                w
            })
            .unwrap_or(weights);
        // Fixed original-topic coverage and mandatory minimums take precedence
        // when a later weight edit leaves only zero-weight feasible bands.
        // Otherwise retain the database distribution exactly.
        if fixed
            && choices[&topic]
                .iter()
                .all(|q| selected_weights[band(s, *q).unwrap().unwrap()] == 0.0)
        {
            selected_weights = [1.0; 3];
        }
        let q = question_selection::select(
            s,
            &choices[&topic],
            Some(selected_weights),
            &format!("{seed}-question-{slot}"),
        )?
        .ok_or("No feasible rated question in assessment sampler")?;
        let b = band(s, q)?.unwrap();
        minutes -= b + 1;
        have |= 1 << b;
        selected.push(q);
        pools.remove(&topic);
        if required_band.is_some() {
            required.remove(0);
        }
    }
    if have != 7 || fixed && !pools.is_empty() {
        return Err("Assessment sampler lost completion feasibility".into());
    }
    // Deterministic shuffle: exact retries preserve the prepared route.
    selected.sort_by_key(|q| Sha256::digest(format!("{seed}-shuffle-{q}")).to_vec());
    let _ = l;
    Ok(selected)
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
