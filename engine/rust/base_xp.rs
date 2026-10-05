//! Lesson workload only: expected difficulty distribution, never learner outcomes.
//! Reference and calibration provenance: reference/THE_PLAN/README.md.
use crate::{Result, learning, question_selection, schema::EntitySnapshot};
use regex::Regex;
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use std::{
    collections::{BTreeMap, BTreeSet},
    sync::OnceLock,
};

pub const VERSION: &str = "lesson-content-expected-distribution-v1";
pub const DEFAULT_WEIGHTS: [f64; 3] = [60.0, 30.0, 10.0];

fn regex(pattern: &'static str) -> &'static Regex {
    static PATTERNS: OnceLock<BTreeMap<&'static str, Regex>> = OnceLock::new();
    &PATTERNS.get_or_init(|| {
        [
            r"!\[[^\]]*\]\([^)]*\)",
            r"\{\{[^}]*\}\}",
            r"(?s)\$\$(.*?)\$\$|\$([^$]*)\$",
            r"\\[A-Za-z]+|\d+(?:\.\d+)?|[A-Za-z]|[+*/=^_−-]",
            r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b",
        ]
        .into_iter()
        .map(|p| (p, Regex::new(p).unwrap()))
        .collect()
    })[pattern]
}
pub fn clean_markdown(text: &str) -> String {
    let text = regex(r"!\[[^\]]*\]\([^)]*\)").replace_all(text, "");
    regex(r"\{\{[^}]*\}\}").replace_all(&text, "").into_owned()
}
pub fn math_tokens(text: &str) -> usize {
    let text = clean_markdown(text);
    regex(r"(?s)\$\$(.*?)\$\$|\$([^$]*)\$")
        .captures_iter(&text)
        .map(|c| {
            regex(r"\\[A-Za-z]+|\d+(?:\.\d+)?|[A-Za-z]|[+*/=^_−-]")
                .find_iter(c.get(1).or_else(|| c.get(2)).unwrap().as_str())
                .count()
        })
        .sum()
}
pub fn prose_words(text: &str) -> usize {
    let text = clean_markdown(text);
    let text = regex(r"(?s)\$\$(.*?)\$\$|\$([^$]*)\$").replace_all(&text, "");
    regex(r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b")
        .find_iter(&text)
        .count()
}

#[derive(Clone, Debug, Default, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Features {
    pub kp_count: usize,
    pub solution_math_100: f64,
    pub reading_100: f64,
    pub question_steps: f64,
    pub example_steps: f64,
    pub question_math_100: f64,
    pub extra_fields: f64,
    pub blank_kp: f64,
}
impl Features {
    pub fn score(&self, weights: [f64; 3]) -> Result<f64> {
        if self.kp_count == 0 {
            return Err("lesson XP requires knowledge points".into());
        }
        for value in [
            self.solution_math_100,
            self.reading_100,
            self.question_steps,
            self.example_steps,
            self.question_math_100,
            self.extra_fields,
            self.blank_kp,
        ] {
            if !value.is_finite() || value < 0.0 {
                return Err("invalid lesson workload measurement".into());
            }
        }
        let probabilities = distribution(weights)?;
        let weighted = self.solution_math_100
            * (probabilities[0] + 2.0 * probabilities[1] + 4.0 * probabilities[2]);
        let score = 0.7727506490727063 * weighted
            + 0.07513004637186382 * self.reading_100
            + 0.001586056170966394 * self.question_steps
            + 0.034422123109798704 * self.example_steps
            + 2.7349018409710975 * self.question_math_100
            + 0.06047150091696244 * self.extra_fields
            + 0.5742034148595132 * self.blank_kp
            + 0.8708735238642493 * (probabilities[1] * self.kp_count as f64)
            + 2.041850919949942 * (probabilities[2] * self.kp_count as f64);
        if !score.is_finite() || score <= 0.0 {
            return Err("invalid unscaled lesson score".into());
        }
        Ok(score)
    }

    /// Saved capture arrays retain presentation order. No difficulty is read.
    pub fn from_content(content: &Value, tutorial_words: usize, first_two: bool) -> Result<Self> {
        let questions = content["questions"]
            .as_array()
            .ok_or("lesson questions required")?;
        let mut grouped: BTreeMap<String, Vec<&Value>> = BTreeMap::new();
        let mut seen = BTreeSet::new();
        for q in questions {
            let id = q["math_academy_id"]
                .as_str()
                .ok_or("question identity required")?;
            if !seen.insert(id) {
                continue;
            }
            let kp = q["knowledge_point_id"]
                .as_str()
                .ok_or("question KP required")?;
            let pool = grouped.entry(kp.into()).or_default();
            if !first_two || pool.len() < 2 {
                pool.push(q);
            }
        }
        if first_two && grouped.values().any(|qs| qs.len() < 2) {
            return Err("calibration requires two distinct questions for every KP".into());
        }
        let examples = content["canonical_examples"]
            .as_array()
            .ok_or("canonical examples required")?;
        let mut example_kps = BTreeSet::new();
        let mut result = Self {
            kp_count: grouped.len(),
            ..Self::default()
        };
        for qs in grouped.values() {
            let n = qs.len() as f64;
            for q in qs {
                let solution = q["worked_solution"]
                    .as_str()
                    .filter(|s| !s.trim().is_empty())
                    .ok_or("worked solution required")?;
                let problem = q["problem"]
                    .as_str()
                    .filter(|s| !s.trim().is_empty())
                    .ok_or("question problem required")?;
                let fields = q["answer_fields"]
                    .as_array()
                    .filter(|v| !v.is_empty())
                    .ok_or("answer fields required")?;
                result.solution_math_100 += math_tokens(solution) as f64 / n / 100.0;
                result.question_steps += clean_markdown(solution).matches('=').count() as f64 / n;
                result.question_math_100 += math_tokens(problem) as f64 / n / 100.0;
                result.extra_fields += fields.len().saturating_sub(1) as f64 / n;
                result.blank_kp += f64::from(fields.iter().any(|f| f["type"] == "blank")) / n;
            }
        }
        result.reading_100 = tutorial_words as f64 / 100.0;
        for example in examples {
            let kp = example["knowledge_point_id"]
                .as_str()
                .ok_or("example KP required")?;
            if !example_kps.insert(kp.to_string()) {
                return Err("duplicate canonical KP example".into());
            }
            let problem = example["problem"]
                .as_str()
                .ok_or("example problem required")?;
            let solution = example["worked_solution"]
                .as_str()
                .filter(|s| !s.trim().is_empty())
                .ok_or("example solution required")?;
            result.reading_100 += (prose_words(problem) + prose_words(solution)) as f64 / 100.0;
            result.example_steps += clean_markdown(solution).matches('=').count() as f64;
        }
        if example_kps != grouped.keys().cloned().collect() {
            return Err("complete KP/example coverage required".into());
        }
        Ok(result)
    }
}
pub fn distribution(weights: [f64; 3]) -> Result<[f64; 3]> {
    let total: f64 = weights.iter().sum();
    if !total.is_finite() || total <= 0.0 || weights.iter().any(|w| !w.is_finite() || *w < 0.0) {
        return Err("invalid expected difficulty distribution".into());
    }
    Ok(weights.map(|w| w / total))
}

#[derive(Debug, Serialize)]
pub struct Estimate {
    pub formula_version: &'static str,
    pub features: Features,
    pub distribution: [f64; 3],
    pub unscaled_score: f64,
    pub multiplier: f64,
    pub base_xp: i64,
    pub expected_seconds: f64,
    pub canonical_solution_proxy_count: usize,
}
pub fn estimate(features: Features, weights: [f64; 3], multiplier: f64) -> Result<Estimate> {
    if !multiplier.is_finite() || multiplier <= 0.0 {
        return Err("topic multiplier must be positive and finite".into());
    }
    let score = features.score(weights)?;
    let rounded = (multiplier * score + 0.5).floor().max(7.0);
    if !rounded.is_finite() || rounded >= i64::MAX as f64 {
        return Err("base XP overflow".into());
    }
    let base_xp = rounded as i64;
    Ok(Estimate {
        formula_version: VERSION,
        features,
        distribution: distribution(weights)?,
        unscaled_score: score,
        multiplier,
        base_xp,
        expected_seconds: base_xp as f64 * 60.0,
        canonical_solution_proxy_count: 0,
    })
}
pub fn calibrate(
    features: Features,
    weights: [f64; 3],
    authoritative_base: i64,
) -> Result<Estimate> {
    if authoritative_base < 7 {
        return Err("authoritative lesson base is below model floor".into());
    }
    let initial = estimate(features.clone(), weights, 1.0)?;
    let multiplier = if authoritative_base == 7 && initial.base_xp == 7 {
        1.0
    } else {
        authoritative_base as f64 / initial.unscaled_score
    };
    let calibrated = estimate(features, weights, multiplier)?;
    if calibrated.base_xp != authoritative_base {
        return Err("calibration cannot reproduce authoritative base".into());
    }
    Ok(calibrated)
}

/// Catalog estimates use the whole unordered practice pool. The first-two rule
/// applies to recorded captures, where actual presentation order is available.
pub fn activity_estimate(s: &EntitySnapshot, activity: u64) -> Result<Estimate> {
    let policy = question_selection::active_policy(s)?;
    let weights = question_selection::weights(s, policy, "lesson", 0)?.unwrap_or(DEFAULT_WEIGHTS);
    activity_estimate_with_weights(s, activity, weights)
}

pub fn activity_estimate_with_weights(
    s: &EntitySnapshot,
    activity: u64,
    weights: [f64; 3],
) -> Result<Estimate> {
    let steps = learning::lesson_steps(s, activity)?;
    let mut questions = vec![];
    let mut examples = vec![];
    let mut tutorial_words = 0;
    let mut seen_kps = BTreeSet::new();
    let question = |eid: u64, kp: u64, example: bool| -> Result<Value> {
        let r = s.entity(eid)?;
        let mut fields = vec![];
        if !example {
            for f in s.refs(eid, "question/answer-fields")? {
                fields.push(json!({"type":s.ident(&json!(s.reference(f,"answer-field/type")?))?.rsplit('/').next().unwrap()}));
            }
        }
        let observed_solution = r
            .get("question/worked-solution")
            .filter(|v| v.as_str().is_some_and(|s| !s.trim().is_empty()));
        let solution = if observed_solution.is_some() || example {
            observed_solution
        } else {
            s.entity(s.reference(kp, "knowledge-point/canonical-example")?)?
                .get("question/worked-solution")
        };
        Ok(
            json!({"math_academy_id":eid.to_string(), "knowledge_point_id":kp.to_string(),
            "problem":r.get("question/problem"), "worked_solution":solution, "answer_fields":fields,
            "canonical_solution_proxy":!example && observed_solution.is_none()}),
        )
    };
    for step in steps {
        match step.kind.as_str() {
            "tutorial" => {
                tutorial_words += prose_words(
                    s.entity(step.content)?["tutorial/content"]
                        .as_str()
                        .ok_or("tutorial content required")?,
                )
            }
            "knowledge-point" => {
                if !seen_kps.insert(step.content) {
                    continue;
                }
                examples.push(question(
                    step.example.ok_or("canonical example required")?,
                    step.content,
                    true,
                )?);
                for q in step.questions {
                    questions.push(question(q, step.content, false)?);
                }
            }
            "example" => {} // Already counted as its KP's canonical example.
            _ => return Err("lesson XP requires KP-based lesson structure".into()),
        }
    }
    let topic = s.reference(activity, "activity/scope")?;
    let multiplier = match s.entity(topic)?.get("topic/difficulty") {
        Some(v) => v.as_f64().ok_or("invalid topic multiplier")?,
        None => 1.0,
    };
    let proxy_count = questions
        .iter()
        .filter(|q| q["canonical_solution_proxy"] == true)
        .count();
    let mut result = estimate(
        Features::from_content(
            &json!({"questions":questions,"canonical_examples":examples}),
            tutorial_words,
            false,
        )?,
        weights,
        multiplier,
    )?;
    result.canonical_solution_proxy_count = proxy_count;
    Ok(result)
}

/// Freeze the allocated base on the attempt. Stored activity duration is the
/// authoritative/cache value; calculate content only when no estimate exists.
pub fn activity_base(s: &EntitySnapshot, activity: u64) -> Result<i64> {
    if let Some(value) = s.entity(activity)?.get("activity/expected-seconds") {
        let seconds = value
            .as_f64()
            .filter(|v| v.is_finite() && *v > 0.0)
            .ok_or("invalid activity expected seconds")?;
        let base = (seconds / 60.0 + 0.5).floor().max(1.0);
        if base >= i64::MAX as f64 {
            return Err("activity base XP overflow".into());
        }
        return Ok(base as i64);
    }
    Ok(activity_estimate(s, activity)?.base_xp)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn captured_content_needs_no_labels_and_matches_saved_predictions() {
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
        let report: Value = serde_json::from_str(
            &std::fs::read_to_string(
                root.join("reference/mathacademy-base-xp/expected-distribution-comparison.json"),
            )
            .unwrap(),
        )
        .unwrap();
        let mut error = 0;
        for row in report["lessons"].as_array().unwrap() {
            let task = row["task_id"].as_i64().unwrap();
            let mut content: Value = serde_json::from_str(
                &std::fs::read_to_string(root.join(format!(
                    "reference/mathacademy/question-capture/{task}/content.json"
                )))
                .unwrap(),
            )
            .unwrap();
            for q in content["questions"].as_array_mut().unwrap() {
                q.as_object_mut().unwrap().remove("difficulty");
            }
            for (mode, first_two) in [("all", false), ("first_two", true)] {
                let recorded = &row[mode]["features"];
                let canonical_words: usize = content["canonical_examples"]
                    .as_array()
                    .unwrap()
                    .iter()
                    .map(|q| {
                        prose_words(q["problem"].as_str().unwrap())
                            + prose_words(q["worked_solution"].as_str().unwrap())
                    })
                    .sum();
                let tutorial_words =
                    (recorded["R"].as_f64().unwrap() * 100.0).round() as usize - canonical_words;
                let features = Features::from_content(&content, tutorial_words, first_two).unwrap();
                let result = estimate(features.clone(), DEFAULT_WEIGHTS, 1.0).unwrap();
                assert_eq!(
                    result.base_xp,
                    row[mode]["prediction"].as_i64().unwrap(),
                    "task {task} {mode}"
                );
                let authoritative = row["base_xp"].as_i64().unwrap();
                assert_eq!(
                    calibrate(features, DEFAULT_WEIGHTS, authoritative)
                        .unwrap()
                        .base_xp,
                    authoritative
                );
                if first_two {
                    error += (result.base_xp - authoritative).abs();
                }
            }
        }
        assert_eq!(error, 143);
    }
    #[test]
    fn rounding_floor_and_invalid_inputs() {
        let f = Features {
            kp_count: 1,
            ..Features::default()
        };
        assert_eq!(
            calibrate(f.clone(), DEFAULT_WEIGHTS, 7).unwrap().multiplier,
            1.0
        );
        assert!(estimate(f.clone(), DEFAULT_WEIGHTS, 0.0).is_err());
        assert!(estimate(f.clone(), [0.0; 3], 1.0).is_err());
        assert!(estimate(f.clone(), DEFAULT_WEIGHTS, f64::INFINITY).is_err());
        let score = f.score(DEFAULT_WEIGHTS).unwrap();
        assert_eq!(
            estimate(f, DEFAULT_WEIGHTS, 7.5 / score).unwrap().base_xp,
            8
        );
    }

    #[test]
    fn catalog_proxies_missing_solutions_without_reading_difficulty() {
        let mut records = BTreeMap::new();
        for (id, record) in [
            (
                1,
                json!({"activity/id":"lesson","activity/type":"activity.type/lesson","activity/scope":2,"activity/steps":[3],"activity/first-step":3}),
            ),
            (2, json!({"topic/id":"topic","topic/difficulty":2.5})),
            (3, json!({"step/content":4})),
            (
                4,
                json!({"knowledge-point/id":"kp","knowledge-point/canonical-example":5,"knowledge-point/questions":[6,7]}),
            ),
            (
                5,
                json!({"question/id":"example","question/problem":"Find $x$.","question/worked-solution":"$x=2$"}),
            ),
            (
                6,
                json!({"question/id":"practice1","question/problem":"Find $x$.","question/worked-solution":"$x=1+1=2$","question/answer-fields":[8]}),
            ),
            (
                7,
                json!({"question/id":"practice2","question/problem":"Find $x$.","question/answer-fields":[8]}),
            ),
            (8, json!({"answer-field/type":"answer-field.type/blank"})),
            (9, json!({"policy/id":"policy"})),
            (
                10,
                json!({"db/ident":crate::schema::keyword("activity.type/lesson")}),
            ),
            (
                11,
                json!({"db/ident":crate::schema::keyword("answer-field.type/blank")}),
            ),
        ] {
            records.insert(id, record.as_object().unwrap().clone());
        }
        let s = EntitySnapshot::new(records, 1).unwrap();
        let estimate = activity_estimate(&s, 1).unwrap();
        assert_eq!(estimate.canonical_solution_proxy_count, 1);
        assert!((estimate.features.solution_math_100 - 0.05).abs() < 1e-12);
        assert_eq!(estimate.features.question_steps, 1.5);
        assert_eq!(estimate.multiplier, 2.5);
        assert_eq!(s.entity(7).unwrap().get("question/worked-solution"), None);
    }
}
