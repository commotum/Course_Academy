//! Difficulty-first sampling. A task and its completed prefix seed a stable
//! draw, so rereading or retrying a continuation cannot reshuffle its question.
use crate::{Result, schema::EntitySnapshot};
use sha2::{Digest, Sha256};
use std::collections::BTreeSet;

const BANDS: [&str; 3] = ["easy", "moderate", "hard"];

pub fn weights(
    s: &EntitySnapshot,
    policy: u64,
    activity_type: &str,
    answered: usize,
) -> Result<Option<[f64; 3]>> {
    let initial_count = match activity_type {
        "lesson" => 2,
        "review" => 3,
        _ => return Err("weighted selection supports lessons and reviews".into()),
    };
    let mut types = BTreeSet::new();
    let mut selected = None;
    for child in s.refs(policy, "policy/question-selection-weights")? {
        if s.owners(child, "policy/question-selection-weights")? != [policy] {
            return Err("question weights must have exactly one policy owner".into());
        }
        let kind = s.ident(&serde_json::json!(
            s.reference(child, "question-weights/activity-type")?
        ))?;
        if !matches!(
            kind.as_str(),
            "activity.type/lesson" | "activity.type/review"
        ) || !types.insert(kind.clone())
        {
            return Err(
                "policy needs at most one question-weight record per supported activity type"
                    .into(),
            );
        }
        for phase in ["initial", "remedial"] {
            let mut distribution = [0.0; 3];
            for (index, band) in BANDS.iter().enumerate() {
                let key = format!("question-weights/{phase}-{band}");
                distribution[index] = s
                    .entity(child)?
                    .get(&key)
                    .and_then(|v| v.as_f64())
                    .filter(|v| v.is_finite() && *v >= 0.0)
                    .ok_or_else(|| format!("{key} must be finite and nonnegative"))?;
            }
            let total: f64 = distribution.iter().sum();
            if !total.is_finite() || total <= 0.0 {
                return Err(
                    "each question-weight distribution needs a positive finite total".into(),
                );
            }
            if kind == format!("activity.type/{activity_type}")
                && phase
                    == if answered < initial_count {
                        "initial"
                    } else {
                        "remedial"
                    }
            {
                selected = Some(distribution);
            }
        }
    }
    Ok(selected)
}

pub fn active_policy(s: &EntitySnapshot) -> Result<u64> {
    let policies: Vec<_> = s
        .entities
        .iter()
        .filter(|(_, r)| r.contains_key("policy/id"))
        .map(|(id, _)| *id)
        .collect();
    match policies.as_slice() {
        [policy] => Ok(*policy),
        _ => Err("question selection requires exactly one configured policy".into()),
    }
}

/// Exclude previous tasks; the caller separately excludes its current prefix.
/// This also lets completion validate an already-reserved current question.
pub fn seen_before_task(s: &EntitySnapshot, learner: u64, task: u64) -> Result<BTreeSet<u64>> {
    let mut seen = BTreeSet::new();
    for other in s.refs(learner, "learner/activity")? {
        if other == task {
            continue;
        }
        for item in s.refs(other, "learner-task/items")? {
            if let Some(content) = s.optional_ref(item, "task-item/content")? {
                seen.insert(content);
            }
        }
    }
    Ok(seen)
}

/// Candidates must already be fresh and usable. Unknown ratings are a uniform
/// fallback only when no eligible, positively weighted rated band remains.
/// Explicitly zero-weight rated bands are never used as that fallback.
pub fn select(
    s: &EntitySnapshot,
    candidates: &[u64],
    distribution: Option<[f64; 3]>,
    seed: &str,
) -> Result<Option<u64>> {
    let candidates: Vec<_> = candidates
        .iter()
        .copied()
        .collect::<BTreeSet<_>>()
        .into_iter()
        .collect();
    // Preserve old, unconfigured policies; the default policy supplies weights.
    let Some(distribution) = distribution else {
        return Ok(candidates.first().copied());
    };
    if distribution.iter().any(|w| !w.is_finite() || *w < 0.0)
        || !distribution.iter().sum::<f64>().is_finite()
        || distribution.iter().sum::<f64>() <= 0.0
    {
        return Err("invalid question-weight distribution".into());
    }
    let mut bands: [Vec<u64>; 3] = std::array::from_fn(|_| vec![]);
    let mut unrated = vec![];
    for q in candidates {
        let Some(value) = s
            .entity(q)?
            .get("question/difficulty")
            .filter(|v| !v.is_null())
        else {
            unrated.push(q);
            continue;
        };
        let difficulty = s.ident(value)?;
        let band = BANDS
            .iter()
            .position(|b| difficulty == format!("question.difficulty/{b}"))
            .ok_or("question has an unsupported difficulty enum")?;
        bands[band].push(q);
    }
    let digest = Sha256::digest(format!("course-academy/question-selection/v1/{seed}"));
    let uniform = |offset| {
        let bits = u64::from_be_bytes(digest[offset..offset + 8].try_into().unwrap()) >> 11;
        bits as f64 / (1u64 << 53) as f64
    };
    let total: f64 = distribution
        .iter()
        .enumerate()
        .filter(|(i, _)| !bands[*i].is_empty())
        .map(|(_, w)| *w)
        .sum();
    let pool = if total > 0.0 {
        let mut draw = uniform(0) * total;
        let mut chosen = None;
        for (i, w) in distribution.iter().enumerate() {
            if bands[i].is_empty() || *w == 0.0 {
                continue;
            }
            chosen = Some(i);
            if draw < *w {
                break;
            }
            draw -= *w;
        }
        &bands[chosen.unwrap()]
    } else {
        &unrated
    };
    Ok(if pool.is_empty() {
        None
    } else {
        Some(pool[(uniform(8) * pool.len() as f64) as usize])
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;
    use std::collections::BTreeMap;

    fn snapshot() -> EntitySnapshot {
        let mut e = BTreeMap::new();
        for (id, band) in BANDS.iter().enumerate() {
            e.insert(
                id as u64 + 1,
                json!({"db/ident":{"$keyword":format!("question.difficulty/{band}")}})
                    .as_object()
                    .unwrap()
                    .clone(),
            );
        }
        for q in 10..110 {
            e.insert(
                q,
                json!({"question/difficulty":if q == 10 {1} else if q == 11 {2} else {3}})
                    .as_object()
                    .unwrap()
                    .clone(),
            );
        }
        e.insert(200, serde_json::Map::new());
        EntitySnapshot::new(e, 1).unwrap()
    }

    #[test]
    fn draws_bands_before_questions_and_is_stable() {
        let s = snapshot();
        let pool: Vec<_> = (10..110).collect();
        let mut counts = [0; 3];
        for trial in 0..10000 {
            let seed = trial.to_string();
            let q = select(&s, &pool, Some([6.0, 3.0, 1.0]), &seed)
                .unwrap()
                .unwrap();
            assert_eq!(
                Some(q),
                select(&s, &pool, Some([6.0, 3.0, 1.0]), &seed).unwrap()
            );
            counts[if q == 10 {
                0
            } else if q == 11 {
                1
            } else {
                2
            }] += 1;
        }
        for (count, expected) in counts.into_iter().zip([6000i32, 3000, 1000]) {
            assert!((count - expected).abs() < 200, "{counts:?}");
        }
    }

    #[test]
    fn missing_supply_renormalizes_without_using_excluded_bands_or_inventing_ratings() {
        let s = snapshot();
        assert_eq!(
            select(&s, &[11, 12, 200], Some([6.0, 3.0, 0.0]), "x").unwrap(),
            Some(11)
        );
        assert_eq!(
            select(&s, &[12, 200], Some([6.0, 3.0, 0.0]), "x").unwrap(),
            Some(200)
        );
        assert_eq!(select(&s, &[12], Some([6.0, 3.0, 0.0]), "x").unwrap(), None);
        assert!(select(&s, &[10], Some([0.0; 3]), "x").is_err());
    }

    #[test]
    fn phases_and_activity_types_are_independent_and_bad_configuration_fails() {
        let mut s = snapshot();
        for (id, kind) in [(300, "lesson"), (301, "review")] {
            s.entities.insert(
                id,
                json!({"db/ident":{"$keyword":format!("activity.type/{kind}")}})
                    .as_object()
                    .unwrap()
                    .clone(),
            );
            s.entities.insert(id+10, json!({"question-weights/activity-type":id,
                "question-weights/initial-easy":1.0,"question-weights/initial-moderate":2.0,"question-weights/initial-hard":3.0,
                "question-weights/remedial-easy":4.0,"question-weights/remedial-moderate":5.0,"question-weights/remedial-hard":0.0}).as_object().unwrap().clone());
        }
        s.entities.insert(
            400,
            json!({"policy/question-selection-weights":[310,311]})
                .as_object()
                .unwrap()
                .clone(),
        );
        assert_eq!(
            weights(&s, 400, "lesson", 1).unwrap(),
            Some([1.0, 2.0, 3.0])
        );
        assert_eq!(
            weights(&s, 400, "lesson", 2).unwrap(),
            Some([4.0, 5.0, 0.0])
        );
        assert_eq!(
            weights(&s, 400, "review", 2).unwrap(),
            Some([1.0, 2.0, 3.0])
        );
        assert_eq!(
            weights(&s, 400, "review", 3).unwrap(),
            Some([4.0, 5.0, 0.0])
        );
        s.entities
            .get_mut(&311)
            .unwrap()
            .insert("question-weights/remedial-easy".into(), json!(-1.0));
        assert!(weights(&s, 400, "lesson", 0).is_err());
    }
}
