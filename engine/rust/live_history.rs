//! Audit saved completed-task observations without accessing a live account.
//! Observed answers update a declared ability estimator, never inferred task
//! passes, diagnostic placement, or retention credit.
use crate::{Result, calibration::AccuracyEstimate};
use chrono::NaiveDateTime;
use regex::Regex;
use serde_json::{Map, Value, json};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::Path;

pub const CHECKSUM_ENCODING: &str = "FNV-1a32 over JavaScript UTF-16 code units of compact JSON.stringify-compatible arrays; task rows are [question_dom_id,topic_step_href,difficulty_label,displayed_created,displayed_elapsed,result_label], preserving occurrence order; graph rows are [topic_id,ellipse_fill], sorted lexically by the digit-only string topic ID. No ASCII escaping. Checksums detect transcription differences, not authenticity.";
fn array(v: &Value) -> Result<&Vec<Value>> {
    v.as_array().ok_or_else(|| "expected array".into())
}
fn text(v: &Value) -> Result<&str> {
    v.as_str().ok_or_else(|| "expected text".into())
}
fn object(v: &Value) -> Result<&Map<String, Value>> {
    v.as_object().ok_or_else(|| "expected object".into())
}
fn string_id(v: &Value) -> String {
    v.as_str()
        .map(str::to_owned)
        .unwrap_or_else(|| v.to_string())
}
fn source(path: &Path) -> Result<Value> {
    Ok(
        json!({"path":path.to_string_lossy(),"sha256":format!("{:x}",Sha256::digest(fs::read(path).map_err(|e|e.to_string())?))}),
    )
}
fn csv_rows(path: &Path) -> Result<Vec<Value>> {
    let mut reader = csv::Reader::from_path(path).map_err(|e| e.to_string())?;
    let headers = reader.headers().map_err(|e| e.to_string())?.clone();
    reader
        .records()
        .map(|row| {
            let row = row.map_err(|e| e.to_string())?;
            Ok(Value::Object(
                headers
                    .iter()
                    .zip(row.iter())
                    .map(|(k, v)| (k.into(), json!(v)))
                    .collect(),
            ))
        })
        .collect()
}
fn read_json(path: &Path) -> Result<Value> {
    serde_json::from_slice(&fs::read(path).map_err(|e| e.to_string())?).map_err(|e| e.to_string())
}
fn unique<'a>(records: &'a [Value], key: &str, name: &str) -> Result<BTreeMap<String, &'a Value>> {
    let mut out = BTreeMap::new();
    for row in records {
        let id = text(&row[key])?;
        if out.insert(id.to_owned(), row).is_some() {
            return Err(format!("Duplicate {name} ID {id}"));
        }
    }
    Ok(out)
}
fn count<'a>(values: impl Iterator<Item = &'a str>) -> BTreeMap<String, usize> {
    let mut out = BTreeMap::new();
    for value in values {
        *out.entry(value.to_string()).or_default() += 1;
    }
    out
}
fn numeric_sorted(values: impl IntoIterator<Item = String>) -> Result<Vec<String>> {
    let set: BTreeSet<_> = values.into_iter().collect();
    let mut keyed = set
        .into_iter()
        .map(|v| {
            Ok((
                v.parse::<u64>()
                    .map_err(|_| format!("expected numeric identifier {v}"))?,
                v,
            ))
        })
        .collect::<Result<Vec<_>>>()?;
    keyed.sort();
    Ok(keyed.into_iter().map(|(_, v)| v).collect())
}
pub fn elapsed_seconds(label: &str) -> Result<u64> {
    let re = Regex::new(r"^Elapsed: ([0-9]+):([0-5][0-9])$").unwrap();
    let c = re
        .captures(label)
        .ok_or_else(|| format!("Unrecognized elapsed label: {label:?}"))?;
    let mins = c[1].parse::<u64>().map_err(|e| e.to_string())?;
    let seconds = c[2].parse::<u64>().map_err(|e| e.to_string())?;
    mins.checked_mul(60)
        .and_then(|v| v.checked_add(seconds))
        .ok_or("elapsed seconds overflow".into())
}
pub fn fnv1a32_json(value: &Value) -> String {
    let encoded = serde_json::to_string(value).expect("JSON value serialization");
    let mut result = 2_166_136_261u32;
    for unit in encoded.encode_utf16() {
        result = (result ^ u32::from(unit)).wrapping_mul(16_777_619);
    }
    format!("{result:08x}")
}
fn task_checksum(task: &Value) -> Result<Value> {
    let fields = [
        "question_dom_id",
        "topic_step_href",
        "difficulty_label",
        "displayed_created",
        "displayed_elapsed",
        "result_label",
    ];
    let rows: Vec<Value> = array(&task["questions"])?
        .iter()
        .map(|q| json!(fields.iter().map(|f| q[*f].clone()).collect::<Vec<_>>()))
        .collect();
    let actual = fnv1a32_json(&json!(rows));
    let expected = task
        .get("browser_rows_fnv1a32")
        .cloned()
        .unwrap_or(Value::Null);
    if !expected.is_null() && expected != actual {
        return Err(format!(
            "Browser checksum mismatch for task {}: {actual} != {expected}",
            task["task_id"]
        ));
    }
    Ok(
        json!({"expected":expected,"calculated":actual,"verified":if expected.is_null(){Value::Null}else{json!(true)}}),
    )
}
fn completed_local(task: &Value) -> Result<String> {
    let label = format!(
        "{} {}",
        text(&task["date"])?,
        text(&task["displayed_completed"])?
    );
    Ok(
        NaiveDateTime::parse_from_str(&label, "%Y-%m-%d Completed @ %I:%M %p")
            .map_err(|e| e.to_string())?
            .format("%Y-%m-%d %H:%M")
            .to_string(),
    )
}
#[derive(Default)]
struct Catalogs {
    sources: Value,
    topics: BTreeMap<String, String>,
    steps: BTreeMap<String, Vec<Value>>,
    questions: BTreeMap<String, Vec<Value>>,
    example_steps: BTreeMap<(String, String), Vec<String>>,
}
fn catalogs(root: Option<&Path>, topic_ids: Vec<String>) -> Result<Option<Catalogs>> {
    let Some(root) = root else { return Ok(None) };
    let files = [
        ("topics", root.join("Topics.csv")),
        ("steps", root.join("Lesson-Data/Steps.csv")),
        ("questions", root.join("Lesson-Data/Questions.csv")),
    ];
    let mut c = Catalogs::default();
    let mut sources = Map::new();
    for (name, path) in &files {
        sources.insert(name.to_string(), source(path)?);
    }
    for row in csv_rows(&files[0].1)? {
        c.topics.insert(
            text(&row["topic-id"])?.into(),
            text(&row["topic-name"])?.into(),
        );
    }
    for row in csv_rows(&files[1].1)? {
        c.steps
            .entry(text(&row["step-id"])?.into())
            .or_default()
            .push(row);
    }
    for row in csv_rows(&files[2].1)? {
        c.questions
            .entry(text(&row["question-id"])?.into())
            .or_default()
            .push(row);
    }
    let mut content_sources = Map::new();
    for id in numeric_sorted(topic_ids)? {
        let path = root
            .join("Lessons")
            .join(&id)
            .join("Source")
            .join(format!("{id}.json"));
        if !path.is_file() {
            continue;
        }
        let data = read_json(&path)?;
        if string_id(&data["topic_id"]) != id {
            return Err(format!(
                "Catalog content topic identity mismatch in {}",
                path.display()
            ));
        }
        content_sources.insert(id.clone(), source(&path)?);
        for item in array(&data["lesson"]["items"])? {
            if item["item_type"] == "step"
                && item["step_type"] == "example"
                && !item["content_id"].is_null()
            {
                c.example_steps
                    .entry((id.clone(), string_id(&item["content_id"])))
                    .or_default()
                    .push(string_id(&item["step_id"]));
            }
        }
    }
    sources.insert(
        "topic_content_snapshots".into(),
        Value::Object(content_sources),
    );
    c.sources = Value::Object(sources);
    Ok(Some(c))
}
fn catalog_check(question: &Value, catalogs: Option<&Catalogs>) -> Result<Value> {
    let Some(c) = catalogs else {
        return Ok(Value::Null);
    };
    let topic = text(&question["topic_id"])?;
    let anchor = text(&question["step_anchor"])?;
    let qid = text(&question["question_id"])?;
    let steps = c.steps.get(anchor).map(Vec::as_slice).unwrap_or(&[]);
    let records = c.questions.get(qid).map(Vec::as_slice).unwrap_or(&[]);
    let resolved = numeric_sorted(
        c.example_steps
            .get(&(topic.into(), anchor.into()))
            .cloned()
            .unwrap_or_default(),
    )?;
    let step_topics: BTreeSet<_> = steps
        .iter()
        .map(|r| r["topic-id"].clone().as_str().unwrap_or("").to_string())
        .collect();
    let question_steps: BTreeSet<_> = records
        .iter()
        .filter(|r| r["topic-id"] == topic)
        .map(|r| string_id(&r["step-id"]))
        .collect();
    Ok(json!({
        "topic_exists":c.topics.contains_key(topic),"topic_name":c.topics.get(topic),
        "anchor_matches_catalog_step_in_topic":steps.iter().any(|r|r["topic-id"]==topic),
        "anchor_collides_with_other_topic_step":!steps.is_empty()&&steps.iter().all(|r|r["topic-id"]!=topic),
        "catalog_step_topics_at_anchor":step_topics,
        "question_id_found":!records.is_empty(),"question_topic_matches":if records.is_empty(){Value::Null}else{json!(records.iter().any(|r|r["topic-id"]==topic))},
        "catalog_question_step_ids":question_steps,
        "question_topic_and_anchor_match":records.iter().any(|r|r["topic-id"]==topic&&r["step-id"]==anchor),
        "anchor_example_content_id_match":!resolved.is_empty(),"example_content_step_candidates":resolved,
        "resolved_catalog_step_id":if resolved.len()==1{json!(resolved[0])}else{Value::Null},
        "question_matches_resolved_example_step":if records.is_empty()||resolved.len()!=1{Value::Null}else{json!(records.iter().any(|r|r["topic-id"]==topic&&r["step-id"]==resolved[0]))},
        "interpretation":"The href anchor joins topic + example content_id in saved lesson JSON; step_id is the distinct lesson placement identifier. Only a unique content-to-step relation is resolved. Absence of a question from sampled catalog content does not invalidate an observed DOM question ID."
    }))
}
fn channels() -> Value {
    json!({"assessment":"assessment","review":"practice","lesson":"practice","multistep":"practice","diagnostic":null,"supplemental diagnostic":null})
}
fn balanced(a: &AccuracyEstimate) -> Value {
    let mut value = serde_json::to_value(a).unwrap();
    value
        .as_object_mut()
        .unwrap()
        .insert("balanced_accuracy".into(), json!(a.accuracy()));
    value
}
pub fn replay_ability(tasks: &[Value], prior_accuracy: f64, alpha: f64) -> Result<Value> {
    let mut global = AccuracyEstimate::new(prior_accuracy);
    global.validate()?;
    let mut local: BTreeMap<String, AccuracyEstimate> = BTreeMap::new();
    let mut traces = vec![];
    let mut omitted = BTreeMap::<String, usize>::new();
    let mut diagnostics = vec![];
    let channel_map = channels();
    let mut ordered = tasks.iter().collect::<Vec<_>>();
    ordered.sort_by_key(|t| {
        (
            string_id(&t["completed_at_local"]),
            string_id(&t["task_id"]),
        )
    });
    for task in ordered {
        let kind = text(&task["kind"])?;
        let channel = channel_map[kind].as_str();
        for q in array(&task["questions"])? {
            let Some(channel) = channel else {
                *omitted.entry(kind.into()).or_default() += 1;
                diagnostics.push(json!({"occurrence_id":q["occurrence_id"],"topic_id":q["topic_id"],"correct":q["correct"],"result_label":q["result_label"]}));
                continue;
            };
            if q["correct"].is_null() {
                *omitted
                    .entry("unrecognized_result_label".into())
                    .or_default() += 1;
                continue;
            }
            let correct = q["correct"]
                .as_bool()
                .ok_or("question correctness must be boolean or null")?;
            let topic = text(&q["topic_id"])?;
            let estimate = local
                .entry(topic.into())
                .or_insert_with(|| AccuracyEstimate::new(prior_accuracy));
            let before = estimate.clone();
            let global_before = global.clone();
            estimate.update(&[correct], channel == "assessment", alpha, 1.0)?;
            global.update(&[correct], channel == "assessment", alpha, 1.0)?;
            traces.push(json!({"occurrence_id":q["occurrence_id"],"topic_id":topic,"channel":channel,"correct":correct,"local_before":before,"local_after":estimate,"global_before":global_before,"global_after":global}));
        }
    }
    let estimates: BTreeMap<_, _> = local
        .iter()
        .map(|(topic, estimate)| (topic.clone(), balanced(estimate)))
        .collect();
    Ok(json!({
        "model":"direct-answer two-channel EWMA sensitivity replay",
        "policy":{"prior_accuracy_per_channel":prior_accuracy,"alpha":alpha,"channel_classification":channel_map,"unobserved_channel":"keeps prior","combination":"arithmetic mean of assessment and practice estimates"},
        "channel_answer_counts":count(traces.iter().filter_map(|t|t["channel"].as_str())),"omitted_answer_counts":omitted,
        "global_estimate":balanced(&global),"topic_estimates":estimates,"traces":traces,"diagnostic_evidence_separate":diagnostics,
        "retention_events_created":0,"diagnostic_placement_inferred":false,
        "assumptions":["Quiz results are classified as assessment and lesson/review/multistep as practice; this is an explicit local classification.","Each observed answer is counted once globally and once on its linked topic, with no graph propagation.","Only the captured tasks are replayed; missing history and unknown initial ability prevent identifying production accuracy values.","Diagnostic answers remain separate and never become mastery, repetition credit, or ordinary quiz/practice evidence."]
    }))
}

fn quiz_comparison(tasks: &[Value], progress: &[Value]) -> Result<Value> {
    let by_id = unique(tasks, "task_id", "task")?;
    let (Some(first), Some(later)) = (by_id.get("13553418"), by_id.get("13682227")) else {
        return Ok(Value::Null);
    };
    let first_q = array(&first["questions"])?;
    let later_q = array(&later["questions"])?;
    let incorrect = numeric_sorted(
        first_q
            .iter()
            .filter(|q| q["correct"] == false)
            .map(|q| string_id(&q["topic_id"])),
    )?;
    let first_time = text(&first["completed_at_local"])?;
    let later_time = text(&later["completed_at_local"])?;
    let reviews: Vec<_> = progress
        .iter()
        .filter(|r| {
            r["activity-type"] == "Review"
                && r["completed-at"]
                    .as_str()
                    .is_some_and(|at| first_time < at && at < later_time)
        })
        .collect();
    let topics1: BTreeSet<_> = first_q.iter().map(|q| string_id(&q["topic_id"])).collect();
    let topics2: BTreeSet<_> = later_q.iter().map(|q| string_id(&q["topic_id"])).collect();
    let questions1: BTreeSet<_> = first_q
        .iter()
        .map(|q| string_id(&q["question_id"]))
        .collect();
    let questions2: BTreeSet<_> = later_q
        .iter()
        .map(|q| string_id(&q["question_id"]))
        .collect();
    let mut per_topic = vec![];
    for topic in &incorrect {
        let mut intervening = vec![];
        for row in reviews.iter().filter(|r| r["topic-id"] == *topic) {
            let results = match by_id.get(text(&row["task-id"])?) {
                Some(t) => json!(
                    array(&t["questions"])?
                        .iter()
                        .map(|q| q["result_label"].clone())
                        .collect::<Vec<_>>()
                ),
                None => Value::Null,
            };
            intervening.push(json!({"task_id":row["task-id"],"completed_at_local":row["completed-at"],"observed_results":results}));
        }
        let subsequent:Vec<_>=later_q.iter().filter(|q|q["topic_id"]==*topic).map(|q|json!({"occurrence_id":q["occurrence_id"],"question_id":q["question_id"],"result_label":q["result_label"]})).collect();
        per_topic.push(json!({"topic_id":topic,"intervening_reviews":intervening,"later_quiz_occurrences":subsequent}));
    }
    let mut sorted_reviews = reviews.clone();
    sorted_reviews.sort_by_key(|r| string_id(&r["completed-at"]));
    Ok(json!({
        "first_task_id":first["task_id"],"later_task_id":later["task_id"],
        "relationship":"Compared by explicit analyst selection of displayed Quiz 4 and Quiz 4 (Retake); no internal retake_of relation is assumed.",
        "incorrect_topics":incorrect,"per_incorrect_topic":per_topic,"intervening_review_task_ids":sorted_reviews.iter().map(|r|r["task-id"].clone()).collect::<Vec<_>>(),
        "topics_only_in_first_quiz":numeric_sorted(topics1.difference(&topics2).cloned())?,"topics_only_in_later_quiz":numeric_sorted(topics2.difference(&topics1).cloned())?,
        "question_ids_shared_between_quizzes":numeric_sorted(questions1.intersection(&questions2).cloned())?,"causal_scheduler_rule_verified":false,
        "interpretation":"Exact topic matches establish observed sequencing and later performance, not why reviews were assigned, scheduled due times, retention deltas, or a universal retake policy."
    }))
}

pub fn build_live_audit(
    capture_path: &Path,
    progress_path: &Path,
    prior_path: &Path,
    catalog_root: Option<&Path>,
) -> Result<Value> {
    let capture = read_json(capture_path)?;
    let progress = csv_rows(progress_path)?;
    let prior_data = read_json(prior_path)?;
    let capture_tasks = array(&capture["tasks"])?;
    let prior_tasks = array(&prior_data["tasks"])?;
    let progress_by_id = unique(&progress, "task-id", "progress task")?;
    let prior_by_id = unique(prior_tasks, "task_id", "prior task")?;
    unique(capture_tasks, "task_id", "live task")?;
    let mut topic_ids = vec![];
    for task in capture_tasks {
        for q in array(&task["questions"])? {
            topic_ids.push(text(&q["topic_id"])?.into());
        }
    }
    let catalogs = catalogs(catalog_root, topic_ids)?;
    let mut tasks = vec![];
    let mut conflicts = vec![];
    let mut occurrences: BTreeMap<String, Vec<Value>> = BTreeMap::new();
    let mut prior_matches = 0;
    let mut unreobserved = BTreeMap::<String, usize>::new();
    let href_re = Regex::new(r"^(?:https://mathacademy\.com)?/topics/([0-9]+)#([0-9]+)$").unwrap();
    for task in capture_tasks {
        let checksum = task_checksum(task)?;
        let tid = text(&task["task_id"])?;
        let completed = completed_local(task)?;
        let row = progress_by_id.get(tid).copied();
        let previous = prior_by_id.get(tid).copied();
        let mut comparisons = vec![];
        if let Some(row) = row {
            let base = if text(&row["xp-possible"])?.is_empty() {
                Value::Null
            } else {
                json!(
                    text(&row["xp-possible"])?
                        .parse::<i64>()
                        .map_err(|e| e.to_string())?
                )
            };
            for (field, old, live) in [
                (
                    "completed_at_local",
                    row["completed-at"].clone(),
                    json!(completed),
                ),
                (
                    "kind",
                    json!(text(&row["activity-type"])?.to_lowercase()),
                    task["kind"].clone(),
                ),
                ("title", row["topic-name"].clone(), task["title"].clone()),
                (
                    "earned_xp",
                    json!(
                        text(&row["xp-earned"])?
                            .parse::<i64>()
                            .map_err(|e| e.to_string())?
                    ),
                    task["earned_xp"].clone(),
                ),
                ("base_xp", base, task["base_xp"].clone()),
                ("url", row["url"].clone(), task["url"].clone()),
            ] {
                if old != live {
                    conflicts.push(json!({"task_id":tid,"source":"progress.csv","field":field,"previous":old,"live":live}));
                }
            }
        }
        if let Some(previous) = previous {
            for (field, old, live) in [
                ("date", previous["date"].clone(), task["date"].clone()),
                (
                    "kind",
                    json!(text(&previous["type"])?.to_lowercase()),
                    task["kind"].clone(),
                ),
                ("title", previous["name"].clone(), task["title"].clone()),
                (
                    "earned_xp",
                    previous["earned"].clone(),
                    task["earned_xp"].clone(),
                ),
                ("base_xp", previous["base"].clone(), task["base_xp"].clone()),
                ("url", previous["url"].clone(), task["url"].clone()),
            ] {
                if old != live {
                    conflicts.push(json!({"task_id":tid,"source":"prior observations","field":field,"previous":old,"live":live}));
                }
            }
        }
        let mut previous_questions = BTreeMap::new();
        if let Some(previous) = previous {
            for q in array(&previous["questions"])? {
                previous_questions
                    .insert(q["number"].as_u64().ok_or("question number required")?, q);
            }
        }
        let original_questions = array(&task["questions"])?;
        if previous.is_some() && previous_questions.len() != original_questions.len() {
            conflicts.push(json!({"task_id":tid,"source":"prior observations","field":"question_count","previous":previous_questions.len(),"live":original_questions.len()}));
        }
        let mut questions = vec![];
        for (i, original) in original_questions.iter().enumerate() {
            let ordinal = i + 1;
            if original["ordinal"].as_u64() != Some(ordinal as u64) {
                return Err(format!("Nonconsecutive occurrence ordinals for {tid}"));
            }
            let href = href_re
                .captures(text(&original["topic_step_href"])?)
                .ok_or_else(|| format!("Inconsistent topic/anchor href in {tid}:{ordinal}"))?;
            if href[1] != *text(&original["topic_id"])?
                || href[2] != *text(&original["step_anchor"])?
            {
                return Err(format!("Inconsistent topic/anchor href in {tid}:{ordinal}"));
            }
            if original["question_dom_id"]
                != format!("question-{}", text(&original["question_id"])?)
            {
                return Err(format!("Inconsistent question DOM ID in {tid}:{ordinal}"));
            }
            let mut question = object(original)?.clone();
            question.insert("occurrence_id".into(), json!(format!("{tid}:{ordinal}")));
            question.insert(
                "correct".into(),
                match original["result_label"].as_str() {
                    Some("Correct") => json!(true),
                    Some("Incorrect") => json!(false),
                    _ => Value::Null,
                },
            );
            question.insert(
                "elapsed_seconds".into(),
                json!(elapsed_seconds(text(&original["displayed_elapsed"])?)?),
            );
            question.insert("answer_state".into(), Value::Null);
            let old = previous_questions.get(&(ordinal as u64)).copied();
            question.insert(
                "prior_observation".into(),
                old.cloned().unwrap_or(Value::Null),
            );
            question.insert(
                "prior_answer_state_reobserved".into(),
                if old.is_some() {
                    json!(false)
                } else {
                    Value::Null
                },
            );
            if let Some(old) = old {
                let mut mismatch = false;
                for (field, a, b) in [
                    ("correct", &old["correct"], &question["correct"]),
                    (
                        "difficulty",
                        &old["difficulty"],
                        &original["difficulty_label"],
                    ),
                    (
                        "elapsed_seconds",
                        &old["elapsed_seconds"],
                        &question["elapsed_seconds"],
                    ),
                ] {
                    if a != b {
                        mismatch = true;
                        conflicts.push(json!({"task_id":tid,"ordinal":ordinal,"source":"prior observations","field":field,"previous":a,"live":b}));
                    }
                }
                if !mismatch {
                    prior_matches += 1;
                }
                *unreobserved
                    .entry(text(&old["answer_state"])?.into())
                    .or_default() += 1;
                comparisons.push(json!({"occurrence_id":question["occurrence_id"],"compared_fields_agree":!mismatch,"previous_answer_state":old["answer_state"],"live_result_label":original["result_label"],"live_answer_state":null,"interpretation":"Correct/Incorrect is an outcome label, not an observation of submitted-answer content. Prior no_answer/shown/not_shown subtype remains separately sourced and unverified by this capture."}));
            }
            let mut question = Value::Object(question);
            let check = catalog_check(&question, catalogs.as_ref())?;
            question
                .as_object_mut()
                .unwrap()
                .insert("catalog_check".into(), check);
            occurrences.entry(text(&question["question_id"] )?.into()).or_default().push(json!({"occurrence_id":question["occurrence_id"],"task_id":tid,"topic_id":question["topic_id"],"step_anchor":question["step_anchor"],"result_label":question["result_label"]}));
            questions.push(question);
        }
        let mut task = object(task)?.clone();
        task.insert("completed_at_local".into(), json!(completed));
        task.insert("time_zone".into(), Value::Null);
        task.insert("in_original_progress".into(), json!(row.is_some()));
        task.insert("in_prior_observations".into(), json!(previous.is_some()));
        task.insert("questions".into(), json!(questions));
        task.insert("prior_comparisons".into(), json!(comparisons));
        task.insert("transcription_checksum".into(), checksum);
        tasks.push(Value::Object(task));
    }
    tasks.sort_by_key(|t| {
        (
            string_id(&t["completed_at_local"]),
            string_id(&t["task_id"]),
        )
    });
    let all_questions: Vec<_> = tasks
        .iter()
        .flat_map(|t| t["questions"].as_array().unwrap().iter())
        .collect();
    let checks: Vec<_> = all_questions
        .iter()
        .map(|q| &q["catalog_check"])
        .filter(|v| !v.is_null())
        .collect();
    let repeated: BTreeMap<_, _> = occurrences
        .iter()
        .filter(|(_, items)| {
            items
                .iter()
                .map(|i| string_id(&i["task_id"]))
                .collect::<BTreeSet<_>>()
                .len()
                > 1
        })
        .map(|(q, items)| (q.clone(), items.clone()))
        .collect();
    let mut prior_ids = BTreeSet::new();
    let mut live_ids = BTreeSet::new();
    for task in prior_tasks {
        for q in array(&task["questions"])? {
            prior_ids.insert((
                text(&task["task_id"])?.to_owned(),
                q["number"].as_u64().ok_or("question number required")?,
            ));
        }
    }
    for task in &tasks {
        for q in array(&task["questions"])? {
            live_ids.insert((
                text(&task["task_id"])?.to_owned(),
                q["ordinal"].as_u64().ok_or("ordinal required")?,
            ));
        }
    }
    let remaining = prior_ids
        .difference(&live_ids)
        .filter(|(tid, _)| {
            progress_by_id
                .get(tid)
                .and_then(|r| r["topic-id"].as_str())
                .is_some_and(|s| !s.is_empty())
        })
        .count();
    let mut graph_audit = Value::Null;
    if let Some(graph) = capture.get("graph_snapshot").filter(|g| !g.is_null()) {
        let mut nodes = array(&graph["nodes"])?.clone();
        nodes.sort_by_key(|n| string_id(&n[0]));
        let hash = fnv1a32_json(&json!(nodes));
        if graph["browser_nodes_fnv1a32"] != hash
            || graph["node_count"].as_u64() != Some(nodes.len() as u64)
            || nodes
                .iter()
                .map(|n| string_id(&n[0]))
                .collect::<BTreeSet<_>>()
                .len()
                != nodes.len()
        {
            return Err("Graph snapshot count, identity, or checksum validation failed".into());
        }
        graph_audit = json!({"captured_at":graph["captured_at"],"course_id":graph["course_id"],"node_count":nodes.len(),"checksum_verified":true,"calculated_checksum":hash,"fill_counts":count(nodes.iter().filter_map(|n|n[1].as_str())),"numeric_fire_state_observed":false});
    }
    let bool_count = |field: &str| checks.iter().filter(|c| c[field] == true).count();
    let ids: BTreeSet<_> = tasks.iter().map(|t| string_id(&t["task_id"])).collect();
    let summary = json!({
        "captured_tasks":tasks.len(),"captured_questions":all_questions.len(),"distinct_question_ids":occurrences.len(),
        "distinct_topic_ids":all_questions.iter().map(|q|string_id(&q["topic_id"])).collect::<BTreeSet<_>>().len(),
        "distinct_topic_anchor_pairs":all_questions.iter().map(|q|(string_id(&q["topic_id"]),string_id(&q["step_anchor"]))).collect::<BTreeSet<_>>().len(),
        "task_kind_counts":count(tasks.iter().filter_map(|t|t["kind"].as_str())),"result_label_counts":count(all_questions.iter().filter_map(|q|q["result_label"].as_str())),
        "displayed_elapsed_seconds_total":all_questions.iter().map(|q|q["elapsed_seconds"].as_u64().unwrap()).sum::<u64>(),
        "tasks_joined_to_original_progress":tasks.iter().filter(|t|t["in_original_progress"]==true).count(),
        "new_task_ids_outside_original_progress":tasks.iter().filter(|t|t["in_original_progress"]==false).map(|t|t["task_id"].clone()).collect::<Vec<_>>(),
        "tasks_joined_to_prior_observations":tasks.iter().filter(|t|t["in_prior_observations"]==true).count(),
        "prior_question_features_agree":prior_matches,"prior_answer_state_counts_not_reobserved":unreobserved,"source_conflict_count":conflicts.len(),
        "question_ids_repeated_across_tasks":repeated.len(),"browser_task_checksums_verified":tasks.iter().filter(|t|t["transcription_checksum"]["verified"]==true).count(),
        "catalog_topic_matches":bool_count("topic_exists"),"catalog_question_ids_found":bool_count("question_id_found"),"catalog_question_topic_matches":bool_count("question_topic_matches"),
        "catalog_topic_anchor_step_matches":bool_count("anchor_matches_catalog_step_in_topic"),"bare_anchor_collisions_with_other_topic_steps":bool_count("anchor_collides_with_other_topic_step"),
        "topic_anchor_matches_example_content_id":bool_count("anchor_example_content_id_match"),"unambiguous_content_to_step_joins":checks.iter().filter(|c|!c["resolved_catalog_step_id"].is_null()).count(),
        "known_questions_matching_resolved_example_step":bool_count("question_matches_resolved_example_step"),"verified_retention_transitions":0,
        "union_progress_and_live_task_ids":progress_by_id.keys().cloned().chain(ids.iter().cloned()).collect::<BTreeSet<_>>().len(),
        "union_observed_task_ids":prior_by_id.keys().cloned().chain(ids.iter().cloned()).collect::<BTreeSet<_>>().len(),
        "union_question_occurrences":prior_ids.union(&live_ids).count(),"union_question_occurrences_with_direct_topic_link":live_ids.len(),
        "additional_prior_occurrences_with_task_topic_scope_only":remaining
    });
    Ok(json!({
        "schema_version":1,"checksum_encoding":CHECKSUM_ENCODING,
        "sources":{"live_capture":source(capture_path)?,"original_progress":source(progress_path)?,"prior_observations":source(prior_path)?,"catalogs":catalogs.as_ref().map(|c|c.sources.clone()),
            "implementation":source(&Path::new(env!("CARGO_MANIFEST_DIR")).join("engine/rust/live_history.rs"))?,"calibration_implementation":source(&Path::new(env!("CARGO_MANIFEST_DIR")).join("engine/rust/calibration.rs"))?},
        "summary":summary,"source_conflicts":conflicts,"repeated_question_ids_across_tasks":repeated,"quiz4_comparison":quiz_comparison(&tasks,&progress)?,
        "ability_channel_replay":replay_ability(&tasks,0.8,0.2)?,"graph_snapshot_audit":graph_audit,
        "limitations":["The captured topic and anchor hrefs establish direct occurrence scope, unlike the earlier reduced observations.","No task-level FIRe pass/fail, credit magnitude, diagnostic state/reset result, encompassing weight, current repetition state or due timestamp is exposed here.","Catalog question/step inventories are sampled content and may use different identifier namespaces or versions; missing IDs do not invalidate observed DOM identities.","Answer labels and submitted-answer content are distinct. Previously recorded no_answer is neither disproved nor confirmed by a newly captured Incorrect result label.","Repeated question IDs remain separate task-plus-ordinal occurrences; cross-task duplication is not deduplicated away.","Completion and answer timestamps lack verified time zone; quiz answer timestamps do not provide individual answer chronology."],
        "tasks":tasks
    }))
}

#[cfg(test)]
mod tests {
    use super::*;
    fn audit() -> Value {
        let r = Path::new(env!("CARGO_MANIFEST_DIR"));
        build_live_audit(
            &r.join("reference/fire-live-observations-2026-09-26.json"),
            &r.join("reference/progress.csv"),
            &r.join("reference/mathacademy-xp-observations.json"),
            None,
        )
        .unwrap()
    }
    #[test]
    fn retained_capture_checksums_counts_and_evidence_limits() {
        let a = audit();
        let s = &a["summary"];
        for (key, n) in [
            ("browser_task_checksums_verified", 9),
            ("captured_questions", 162),
            ("prior_question_features_agree", 74),
            ("source_conflict_count", 0),
            ("union_question_occurrences", 396),
            ("union_observed_task_ids", 39),
            ("union_progress_and_live_task_ids", 220),
            (
                "additional_prior_occurrences_with_task_topic_scope_only",
                67,
            ),
        ] {
            assert_eq!(s[key], n, "{key}");
        }
        assert_eq!(a["graph_snapshot_audit"]["checksum_verified"], true);
        let replay = &a["ability_channel_replay"];
        assert_eq!(
            replay["channel_answer_counts"],
            json!({"assessment":18,"practice":18})
        );
        assert_eq!(replay["omitted_answer_counts"], json!({"diagnostic":126}));
        assert_eq!(replay["retention_events_created"], 0);
        assert_eq!(
            a["quiz4_comparison"]["incorrect_topics"],
            json!(["88", "161", "1610"])
        );
        assert_eq!(
            a["quiz4_comparison"]["topics_only_in_first_quiz"],
            json!(["161", "436"])
        );
        assert_eq!(
            a["quiz4_comparison"]["question_ids_shared_between_quizzes"],
            json!([])
        );
        assert_eq!(
            a["repeated_question_ids_across_tasks"]
                .as_object()
                .unwrap()
                .keys()
                .cloned()
                .collect::<BTreeSet<_>>(),
            BTreeSet::from(["79870".into(), "112044".into()])
        );
        let task = a["tasks"]
            .as_array()
            .unwrap()
            .iter()
            .find(|t| t["task_id"] == "12563189")
            .unwrap();
        let incorrect: Vec<_> = task["questions"]
            .as_array()
            .unwrap()
            .iter()
            .filter(|q| q["correct"] == false)
            .collect();
        assert_eq!(incorrect.len(), 13);
        for q in incorrect {
            assert_eq!(q["prior_observation"]["answer_state"], "no_answer");
            assert_eq!(q["answer_state"], Value::Null);
            assert_eq!(q["prior_answer_state_reobserved"], false);
        }
    }
    #[test]
    fn unknown_answers_do_not_become_failures_and_checksums_detect_changes() {
        let a = audit();
        let mut tasks = a["tasks"].as_array().unwrap().clone();
        let review = tasks.iter_mut().find(|t| t["kind"] == "review").unwrap();
        review["questions"][0]["correct"] = Value::Null;
        let replay = replay_ability(&tasks, 0.8, 0.2).unwrap();
        assert_eq!(replay["channel_answer_counts"]["practice"], 17);
        assert_eq!(
            replay["omitted_answer_counts"]["unrecognized_result_label"],
            1
        );
        let mut task = a["tasks"][0].clone();
        task["questions"][0]["result_label"] = json!("tampered");
        assert!(
            task_checksum(&task)
                .err()
                .unwrap()
                .contains("checksum mismatch")
        );
        assert_eq!(elapsed_seconds("Elapsed: 3:59").unwrap(), 239);
        assert!(elapsed_seconds("Elapsed: 3:99").is_err());
    }
    #[test]
    fn catalog_example_content_is_distinct_from_step_identity() {
        let mut c = Catalogs::default();
        c.topics.insert("161".into(), "Rules".into());
        c.steps
            .insert("5085".into(), vec![json!({"topic-id":"999"})]);
        c.questions.insert(
            "1806".into(),
            vec![json!({"topic-id":"161","step-id":"18562"})],
        );
        c.example_steps
            .insert(("161".into(), "5085".into()), vec!["18562".into()]);
        let q = json!({"topic_id":"161","step_anchor":"5085","question_id":"1806"});
        let check = catalog_check(&q, Some(&c)).unwrap();
        assert_eq!(check["anchor_collides_with_other_topic_step"], true);
        assert_eq!(check["resolved_catalog_step_id"], "18562");
        assert_eq!(check["question_matches_resolved_example_step"], true);
        c.example_steps
            .get_mut(&("161".into(), "5085".into()))
            .unwrap()
            .push("9999".into());
        assert!(catalog_check(&q, Some(&c)).unwrap()["resolved_catalog_step_id"].is_null());
    }
}
