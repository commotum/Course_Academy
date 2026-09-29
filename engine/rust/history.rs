//! Audit sparse activity evidence without treating completion or XP as mastery.
//! Scenario replay is an explicit sensitivity analysis, not production state.
use crate::{
    Result,
    core::{EncompassingGraph, Event, FireEngine, Policy, TopicState},
};
use chrono::NaiveDateTime;
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};
use std::path::Path;

type Row = BTreeMap<String, String>;

fn source(path: &Path) -> Result<Value> {
    let bytes = std::fs::read(path).map_err(|e| format!("{}: {e}", path.display()))?;
    Ok(json!({"path":path.display().to_string(), "sha256":format!("{:x}", Sha256::digest(bytes))}))
}
fn rows(path: &Path) -> Result<Vec<Row>> {
    let mut reader = csv::Reader::from_path(path).map_err(|e| e.to_string())?;
    reader
        .deserialize()
        .map(|r| r.map_err(|e| e.to_string()))
        .collect()
}
fn field<'a>(row: &'a Row, key: &str) -> Result<&'a str> {
    row.get(key)
        .map(String::as_str)
        .ok_or_else(|| format!("missing CSV field {key}"))
}
fn string<'a>(value: &'a Value, key: &str) -> Result<&'a str> {
    value
        .get(key)
        .and_then(Value::as_str)
        .ok_or_else(|| format!("missing string {key}"))
}
fn array<'a>(value: &'a Value, key: &str) -> Result<&'a Vec<Value>> {
    value
        .get(key)
        .and_then(Value::as_array)
        .ok_or_else(|| format!("missing array {key}"))
}
fn number(value: &str) -> Result<Value> {
    if value.is_empty() {
        Ok(Value::Null)
    } else {
        Ok(json!(value.parse::<i64>().map_err(|e| e.to_string())?))
    }
}
fn datetime(value: &str) -> Result<NaiveDateTime> {
    NaiveDateTime::parse_from_str(value, "%Y-%m-%d %H:%M")
        .map_err(|e| format!("invalid completion time {value}: {e}"))
}
fn counts<'a>(values: impl IntoIterator<Item = &'a str>) -> BTreeMap<String, usize> {
    let mut result = BTreeMap::new();
    for value in values {
        *result.entry(value.to_owned()).or_default() += 1;
    }
    result
}
fn has_questions(value: &Value) -> bool {
    value["question_observations"]
        .as_array()
        .is_some_and(|q| !q.is_empty())
}
fn perfect(value: &Value) -> bool {
    value["question_observations"]
        .as_array()
        .is_some_and(|qs| qs.iter().all(|q| q["correct"] == true))
}
fn duplicate_ids(values: impl IntoIterator<Item = String>, label: &str) -> Result<()> {
    let mut seen = BTreeSet::new();
    let mut duplicates = BTreeSet::new();
    for id in values {
        if !seen.insert(id.clone()) {
            duplicates.insert(id);
        }
    }
    if duplicates.is_empty() {
        Ok(())
    } else {
        Err(format!("Duplicate task IDs in {label}: {duplicates:?}"))
    }
}

fn profile_audit(path: &Path, activities: &[Value]) -> Result<Value> {
    let rows = rows(path)?;
    let mut by_topic: BTreeMap<&str, Vec<&Value>> = BTreeMap::new();
    for activity in activities {
        if let Some(topic) = activity["topic_id"].as_str() {
            by_topic.entry(topic).or_default().push(activity);
        }
    }
    let completed: Vec<&Row> = rows
        .iter()
        .filter(|r| r.get("completed").is_some_and(|v| v == "1"))
        .collect();
    let mut unmatched = vec![];
    let mut stale = vec![];
    for row in &completed {
        let topic = field(row, "topic-id")?;
        let last = field(row, "last-completed-at")?;
        let items = by_topic.get(topic).map(Vec::as_slice).unwrap_or(&[]);
        if !items
            .iter()
            .any(|item| item["completed_at_local"].as_str() == Some(last))
        {
            unmatched.push(topic);
        }
        if items.iter().any(|item| {
            item["completed_at_local"]
                .as_str()
                .is_some_and(|time| time > last)
        }) {
            stale.push(topic);
        }
    }
    let topics: BTreeSet<&str> = rows
        .iter()
        .map(|r| field(r, "topic-id"))
        .collect::<Result<_>>()?;
    let statuses = rows
        .iter()
        .map(|r| field(r, "mastery-status"))
        .collect::<Result<Vec<_>>>()?;
    let evidence = rows
        .iter()
        .map(|r| field(r, "mastery-evidence"))
        .collect::<Result<Vec<_>>>()?;
    let timestamps = rows
        .iter()
        .map(|r| field(r, "last-completed-at"))
        .collect::<Result<Vec<_>>>()?;
    let shared = rows
        .iter()
        .filter(|r| {
            r.get("topic-id")
                .is_some_and(|t| by_topic.contains_key(t.as_str()))
        })
        .map(|r| field(r, "mastery-status"))
        .collect::<Result<Vec<_>>>()?;
    Ok(
        json!({"source":source(path)?, "row_count":rows.len(), "unique_topics":topics.len(),
        "status_counts":counts(statuses), "evidence_counts":counts(evidence), "completed_rows":completed.len(),
        "latest_recorded_completion":timestamps.into_iter().max(),
        "topics_shared_with_history":topics.iter().filter(|t| by_topic.contains_key(**t)).count(),
        "shared_topic_status_counts":counts(shared), "completed_topics_without_matching_history_timestamp":unmatched,
        "completed_topics_with_later_history_events":stale, "ground_truth_for_fire":false,
        "reason":"Statuses mix activity history, queue checkmarks, and local prerequisite-ancestry inference; there are no FIRe state values or observation timestamps."}),
    )
}

pub fn build_audit(
    progress_path: &Path,
    observations_path: &Path,
    knowledge_profile_path: Option<&Path>,
    catalog_path: Option<&Path>,
) -> Result<Value> {
    let rows = rows(progress_path)?;
    let data: Value =
        serde_json::from_slice(&std::fs::read(observations_path).map_err(|e| e.to_string())?)
            .map_err(|e| e.to_string())?;
    let observed = array(&data, "tasks")?;
    let progress_ids = rows
        .iter()
        .map(|r| field(r, "task-id").map(str::to_owned))
        .collect::<Result<Vec<_>>>()?;
    let observed_ids = observed
        .iter()
        .map(|r| string(r, "task_id").map(str::to_owned))
        .collect::<Result<Vec<_>>>()?;
    duplicate_ids(progress_ids.clone(), "progress")?;
    duplicate_ids(observed_ids.clone(), "observations")?;
    let progress_set: BTreeSet<_> = progress_ids.into_iter().collect();
    let unknown: Vec<_> = observed_ids
        .iter()
        .filter(|id| !progress_set.contains(*id))
        .collect();
    if !unknown.is_empty() {
        return Err(format!(
            "Observed task IDs missing from progress: {unknown:?}"
        ));
    }
    let by_id: BTreeMap<String, &Value> = observed_ids.into_iter().zip(observed).collect();
    let catalog = catalog_path
        .map(|p| {
            super::history::rows(p)?
                .into_iter()
                .map(|r| {
                    Ok((
                        field(&r, "topic-id")?.to_owned(),
                        field(&r, "topic-name")?.to_owned(),
                    ))
                })
                .collect::<Result<BTreeMap<_, _>>>()
        })
        .transpose()?;
    let mut activities = vec![];
    for (row_index, row) in rows.iter().enumerate() {
        let completed = field(row, "completed-at")?;
        datetime(completed)?;
        let id = field(row, "task-id")?;
        let task = by_id.get(id).copied();
        let mut issues = vec![];
        let mut questions = vec![];
        let earned = number(field(row, "xp-earned")?)?;
        let base = number(field(row, "xp-possible")?)?;
        if let Some(task) = task {
            for (key, expected) in [
                ("date", json!(field(row, "date")?)),
                ("type", json!(field(row, "activity-type")?)),
                ("name", json!(field(row, "topic-name")?)),
                ("earned", earned.clone()),
                ("base", base.clone()),
                ("url", json!(field(row, "url")?)),
            ] {
                if task[key] != expected {
                    issues.push(json!({"field":key,"progress":expected,"observation":task[key]}));
                }
            }
            for (index, question) in array(task, "questions")?.iter().enumerate() {
                if !question["correct"].is_boolean() {
                    return Err(format!("Task {id}: non-boolean question outcome"));
                }
                if question["elapsed_seconds"].as_i64().is_none_or(|n| n < 0) {
                    return Err(format!("Task {id}: invalid elapsed seconds"));
                }
                if question["number"].as_u64() != Some(index as u64 + 1) {
                    return Err(format!("Task {id}: nonconsecutive question order"));
                }
                questions.push(json!({"occurrence":index+1,"correct":question["correct"], "difficulty":question["difficulty"],
                    "answer_state":question["answer_state"], "elapsed_seconds":question["elapsed_seconds"],
                    "topic_id":null,"knowledge_point_id":null,"question_id":null,"answered_at":null}));
            }
            if let Some(groups) = task.get("group_question_counts").filter(|g| !g.is_null()) {
                let groups = groups.as_array().ok_or("group counts must be an array")?;
                let sum: u64 = groups
                    .iter()
                    .map(|g| g.as_u64().ok_or("invalid group count".to_string()))
                    .collect::<Result<Vec<_>>>()?
                    .into_iter()
                    .sum();
                if sum != questions.len() as u64 {
                    return Err(format!("Task {id}: group counts disagree with questions"));
                }
            }
        }
        let topic = match field(row, "topic-id")? {
            "" => None,
            t => Some(t),
        };
        let catalog_match = match (&catalog, topic) {
            (Some(catalog), Some(topic)) => {
                Some(catalog.get(topic).map(String::as_str) == Some(field(row, "topic-name")?))
            }
            _ => None,
        };
        activities.push(json!({"task_id":id, "progress_csv_row":row_index+2, "url":field(row,"url")?,
            "completed_at_local":completed,"time_zone":null,"activity_type":field(row,"activity-type")?,
            "topic_id":topic,"topic_name":field(row,"topic-name")?,
            "topic_id_provenance":topic.map(|_| "progress.csv; local catalog reconciliation described in progress-notes.md"),
            "catalog_title_and_id_match":catalog_match,"course_code_contextual":field(row,"course-code")?,
            "xp_earned":earned,"xp_base":base,"status_raw":field(row,"status")?,"fire_outcome":null,
            "question_observations":if questions.is_empty() {Value::Null} else {json!(questions)},
            "question_observation_provenance":task.map(|_| "mathacademy-xp-observations.json:tasks/task_id; completed-task DOM"),
            "group_question_counts":task.and_then(|t| t.get("group_question_counts")), "join_issues":issues,
            "chronology_caveats":if id == "4748206" {vec!["Task feed date conflicts with yearless question dates; see activity-schema report."]} else {vec![]}}));
    }
    activities.sort_by(|a, b| {
        (a["completed_at_local"].as_str(), a["task_id"].as_str())
            .cmp(&(b["completed_at_local"].as_str(), b["task_id"].as_str()))
    });
    let question_tasks: Vec<_> = activities.iter().filter(|a| has_questions(a)).collect();
    let scoped_tasks: Vec<_> = question_tasks
        .iter()
        .copied()
        .filter(|a| !a["topic_id"].is_null())
        .collect();
    let questions: Vec<_> = question_tasks
        .iter()
        .flat_map(|a| a["question_observations"].as_array().unwrap())
        .collect();
    let imperfect: Vec<_> = question_tasks
        .iter()
        .copied()
        .filter(|a| !perfect(a))
        .collect();
    let perfect_tasks: Vec<_> = question_tasks
        .iter()
        .copied()
        .filter(|a| perfect(a))
        .collect();
    let positive_imperfect: Vec<_> = imperfect
        .iter()
        .copied()
        .filter(|a| a["xp_earned"].as_i64().is_some_and(|xp| xp > 0))
        .collect();
    let mut timestamps = counts(
        activities
            .iter()
            .map(|a| a["completed_at_local"].as_str().unwrap()),
    );
    timestamps.retain(|_, n| *n > 1);
    let mut by_topic: BTreeMap<&str, Vec<&Value>> = BTreeMap::new();
    for activity in &activities {
        if let Some(topic) = activity["topic_id"].as_str() {
            by_topic.entry(topic).or_default().push(activity);
        }
    }
    let mut pairs = vec![];
    for (topic, items) in &by_topic {
        for pair in items.windows(2) {
            let (earlier, later) = (pair[0], pair[1]);
            let gap = (datetime(string(later, "completed_at_local")?)?
                - datetime(string(earlier, "completed_at_local")?)?)
            .num_seconds() as f64
                / 86400.0;
            pairs.push(json!({"topic_id":topic,"earlier_task_id":earlier["task_id"],"later_task_id":later["task_id"],
                "calendar_gap_days":gap,"later_type":later["activity_type"],"verified_due_interval":false}));
        }
    }
    let xp_counterexamples: Vec<_> = activities
        .iter()
        .filter(|a| match (a["xp_base"].as_i64(), a["xp_earned"].as_i64()) {
            (Some(base), Some(earned)) => earned < 0 || earned > base,
            _ => false,
        })
        .collect();
    let progress_source = source(progress_path)?;
    let snapshot_rows = data["metadata"]["progress_snapshot_rows"]
        .as_i64()
        .ok_or("missing progress_snapshot_rows")?;
    let correct = questions.iter().filter(|q| q["correct"] == true).count();
    Ok(
        json!({"schema_version":1,"sources":{"progress":progress_source,"question_observations":source(observations_path)?,
        "observation_metadata":data["metadata"],"catalog":catalog_path.map(source).transpose()?},
        "summary":{
            "activities":activities.len(),"activity_types":counts(activities.iter().map(|a| a["activity_type"].as_str().unwrap())),
            "first_completion_local":activities.first().map(|a| &a["completed_at_local"]),
            "last_completion_local":activities.last().map(|a| &a["completed_at_local"]),"completion_timestamp_ties":timestamps,
            "activities_with_topic_id":activities.iter().filter(|a| !a["topic_id"].is_null()).count(),"distinct_history_topics":by_topic.len(),
            "observed_tasks":question_tasks.len(),"observed_questions":questions.len(),"correct_questions":correct,
            "incorrect_questions":questions.len()-correct,"observed_tasks_with_task_topic_id":scoped_tasks.len(),
            "observed_questions_with_task_topic_scope":scoped_tasks.iter().map(|a| a["question_observations"].as_array().unwrap().len()).sum::<usize>(),
            "questions_with_direct_topic_id":0,"questions_with_knowledge_point_id":0,
            "observed_elapsed_seconds":questions.iter().map(|q| q["elapsed_seconds"].as_i64().unwrap()).sum::<i64>(),
            "missing_question_detail_tasks":activities.len()-question_tasks.len(),"all_correct_observed_tasks":perfect_tasks.len(),
            "all_correct_observed_tasks_with_task_topic_id":perfect_tasks.iter().filter(|a| !a["topic_id"].is_null()).count(),
            "join_issue_count":activities.iter().map(|a| a["join_issues"].as_array().unwrap().len()).sum::<usize>(),
            "observation_snapshot_hash_matches":data["metadata"]["progress_snapshot_sha256"]==progress_source["sha256"],
            "snapshot_row_count_delta":activities.len() as i64-snapshot_rows,"successive_same_topic_pairs":pairs.len(),
            "verified_fire_state_transitions":0,"verified_due_time_predictions":0,"directly_observed_encompassing_weights":0},
        "contradictions":[
            {"claim":"Completed implies every question was correct","counterexample_count":imperfect.len(),"task_ids":imperfect.iter().map(|a| &a["task_id"]).collect::<Vec<_>>()},
            {"claim":"Positive earned XP implies every question was correct","counterexample_count":positive_imperfect.len(),"task_ids":positive_imperfect.iter().map(|a| &a["task_id"]).collect::<Vec<_>>()},
            {"claim":"Earned XP divided by displayed base is a bounded correctness rate","counterexample_count":xp_counterexamples.len(),"examples":xp_counterexamples.iter().take(5).map(|a| &a["task_id"]).collect::<Vec<_>>()}],
        "identifiability":{
            "observable":["task completion chronology at minute resolution without verified time zone","task topic IDs from prior catalog reconciliation","ordered correctness and displayed elapsed seconds for the 34 sampled tasks","same-topic completion gaps, not scheduled due intervals"],
            "unidentified":["task-level FIRe success/failure criterion","per-question topic/KP identities in the reduced observations","initial repetition state, interval and diagnostic reset/merge policy","encompassing edges and weights","full exercise-time clock, due times and scheduler queue","per-task time of assignment and learner choice/delay","historical calibration parameters and model version"],
            "interpretation":"Agreement of a chosen scenario with activity order is a compatibility check. Without observed due/state values it is not a verified FIRe prediction. Question correctness alone cannot identify repetition-state transitions."},
        "knowledge_profile":knowledge_profile_path.map(|p| profile_audit(p,&activities)).transpose()?,
        "same_topic_completion_pairs":pairs,"activities":activities}),
    )
}

pub fn build_replay_scenario(
    audit: &Value,
    outcome_policy: &str,
    clock_policy: &str,
) -> Result<Value> {
    if !matches!(outcome_policy, "question_correct" | "all_questions_correct") {
        return Err("Choose question_correct or all_questions_correct explicitly".into());
    }
    if !matches!(clock_policy, "observed_elapsed_hours" | "wall_days") {
        return Err("Choose observed_elapsed_hours or wall_days explicitly".into());
    }
    let activities = array(audit, "activities")?;
    let origin = activities
        .first()
        .map(|a| datetime(string(a, "completed_at_local")?))
        .transpose()?;
    let mut elapsed = 0.0;
    let mut events = vec![];
    let mut omitted: BTreeMap<&str, usize> = BTreeMap::new();
    for activity in activities {
        let Some(questions) = activity["question_observations"]
            .as_array()
            .filter(|q| !q.is_empty())
        else {
            *omitted.entry("unobserved_task").or_default() += 1;
            continue;
        };
        let can_emit =
            !activity["topic_id"].is_null() && array(activity, "join_issues")?.is_empty();
        if !can_emit {
            *omitted.entry("unmapped_or_conflicting_task").or_default() += 1;
        }
        for (index, question) in questions.iter().enumerate() {
            elapsed += question["elapsed_seconds"]
                .as_f64()
                .ok_or("missing question elapsed seconds")?;
            if !can_emit
                || (outcome_policy == "all_questions_correct" && index + 1 != questions.len())
            {
                continue;
            }
            let time = if clock_policy == "observed_elapsed_hours" {
                elapsed / 3600.0
            } else {
                (datetime(string(activity, "completed_at_local")?)?
                    - origin.ok_or("missing origin")?)
                .num_seconds() as f64
                    / 86400.0
            };
            let id = string(activity, "task_id")?;
            let event_id = if outcome_policy == "question_correct" {
                format!("{id}:q{}", question["occurrence"])
            } else {
                id.to_owned()
            };
            events.push(json!({"event_id":event_id,"task_id":id,"topic_id":activity["topic_id"],
                "activity_type":activity["activity_type"],"time":time,
                "success":if outcome_policy=="question_correct" {question["correct"].clone()} else {json!(questions.iter().all(|q|q["correct"]==true))},
                "outcome_provenance":if outcome_policy=="question_correct" {"observed question correctness"} else {"assumed task aggregation: all questions correct"}}));
        }
    }
    Ok(
        json!({"outcome_policy":outcome_policy,"clock_policy":clock_policy,
        "time_unit":if clock_policy=="observed_elapsed_hours" {"hours"} else {"days"},
        "assumptions":[
            "Every retained lesson/review question is assigned to its task's catalog topic; question-level topic links were not retained.",
            "Question correctness is a question-level success flag; task aggregation, when selected, requires every question correct. Neither is a recovered MA FIRe task rule.",
            if clock_policy=="observed_elapsed_hours" {"Observed elapsed clock sums only sampled questions, includes possible pauses and omits time on all unobserved tasks; it is not a recovered exercise clock."} else {"Wall-clock days from the first feed completion are substituted for exercise time; questions share their task's completion time."},
            "Initial repetition state and encompassing graph must be supplied independently as explicit assumptions."],
        "events":events,"omitted_task_counts":omitted,"verified_production_predictions":0}),
    )
}

pub fn run_history_scenarios(audit: &Value) -> Result<Value> {
    let learner = "sparse-history-scenario";
    let by_task: BTreeMap<&str, &Value> = array(audit, "activities")?
        .iter()
        .map(|a| Ok((string(a, "task_id")?, a)))
        .collect::<Result<_>>()?;
    let mut runs = vec![];
    for outcome in ["question_correct", "all_questions_correct"] {
        for clock in ["wall_days", "observed_elapsed_hours"] {
            for initial_repetitions in [0.0, 4.0] {
                for growth in [2.0, 1.5] {
                    for memory_order in ["decay-before-add", "literal-add-before-decay"] {
                        let scenario = build_replay_scenario(audit, outcome, clock)?;
                        let events = array(&scenario, "events")?;
                        let topics: BTreeSet<String> = events
                            .iter()
                            .map(|e| string(e, "topic_id").map(str::to_owned))
                            .collect::<Result<_>>()?;
                        let policy = Policy {
                            name: "sparse-history-sensitivity".into(),
                            base_interval_days: if clock == "wall_days" {
                                1.0
                            } else {
                                1.0 / 24.0
                            },
                            interval_growth: growth,
                            memory_order: memory_order.into(),
                            ..Policy::default()
                        };
                        let mut engine = FireEngine::new(
                            EncompassingGraph::new(vec![], topics.clone())?,
                            policy.clone(),
                            BTreeMap::new(),
                            BTreeMap::new(),
                        )?;
                        for topic in &topics {
                            engine.seed(
                                learner,
                                topic,
                                TopicState {
                                    repetitions: initial_repetitions,
                                    interval_days: policy.interval(initial_repetitions)?,
                                    ..TopicState::new(policy.prior_accuracy, true)
                                },
                            )?;
                        }
                        let mut traces = vec![];
                        let mut review_compatibility = vec![];
                        let mut reviewed_tasks = BTreeSet::new();
                        for event in events {
                            let task_id = string(event, "task_id")?;
                            let task = by_task
                                .get(task_id)
                                .ok_or("scenario references unknown task")?;
                            let topic = string(event, "topic_id")?;
                            let time = event["time"].as_f64().ok_or("missing event time")?;
                            let at = if clock == "wall_days" {
                                time
                            } else {
                                time / 24.0
                            };
                            let due_before = engine.states[learner][topic].due_at(&policy);
                            if task["activity_type"] == "Review" && reviewed_tasks.insert(task_id) {
                                review_compatibility.push(json!({"task_id":task_id,"topic_id":topic,"observed_event_at_days":at,
                    "model_due_at_days":due_before,"model_due_when_review_observed":due_before<=at+1e-12,"is_verified_prediction":false}));
                            }
                            let success =
                                event["success"].as_bool().ok_or("missing event success")?;
                            let outcomes = if outcome == "question_correct" {
                                vec![success]
                            } else {
                                array(task, "question_observations")?
                                    .iter()
                                    .map(|q| {
                                        q["correct"].as_bool().ok_or("missing correctness".into())
                                    })
                                    .collect::<Result<_>>()?
                            };
                            let event_id = string(event, "event_id")?;
                            let receipt = engine.apply(Event {
                                id: event_id.into(),
                                learner: learner.into(),
                                topic: topic.into(),
                                at,
                                passed: success,
                                kind: string(task, "activity_type")?.to_lowercase(),
                                question_results: outcomes,
                                source: "explicit-sparse-history-assumption".into(),
                                ..Event::default()
                            })?;
                            traces.push(json!({"event_id":event_id,"task_id":task_id,"event_hash":receipt["event_hash"],"at_days":at,
                "passed":success,"updates":receipt["updates"]}));
                        }
                        let end = traces
                            .iter()
                            .filter_map(|t| t["at_days"].as_f64())
                            .fold(0.0, f64::max);
                        let mut final_states = BTreeMap::new();
                        for (topic, state) in engine
                            .states
                            .get(learner)
                            .into_iter()
                            .flat_map(|s| s.iter())
                        {
                            let mut value =
                                serde_json::to_value(state).map_err(|e| e.to_string())?;
                            value["due_at_days"] = json!(state.due_at(&policy));
                            value["memory_at_last_replay_event"] = json!(state.memory_now(end)?);
                            final_states.insert(topic.clone(), value);
                        }
                        let mut assumptions = array(&scenario, "assumptions")?.clone();
                        assumptions.extend([
            json!(format!("All {} retained topics are assumed previously learned at time zero with repetitions={initial_repetitions}, memory=1, accuracy={}; no initialization/reset information is recoverable.",topics.len(),policy.prior_accuracy)),
            json!("Encompassing graph is empty, so only direct evidence is replayed; prerequisite links are not imported as practice coverage."),
            json!("Every emitted event has quality=1; diagnostics and unsampled tasks supply no outcomes. No parameters are fitted to this history.")]);
                        let suffix = if memory_order == "literal-add-before-decay" {
                            ":literal-add-before-decay"
                        } else {
                            ""
                        };
                        runs.push(json!({"id":format!("{outcome}:{clock}:r{initial_repetitions}:growth{growth}{suffix}"),
            "outcome_policy":outcome,"clock_policy":clock,"memory_order":memory_order,"initial_repetitions_assumption":initial_repetitions,
            "policy":policy,"policy_id":policy.id(),"graph_id":engine.graph.id,"event_count":traces.len(),
            "passed_events":events.iter().filter(|e|e["success"]==true).count(),"failed_events":events.iter().filter(|e|e["success"]==false).count(),
            "topic_count":topics.len(),"final_states":final_states,"observed_review_compatibility":review_compatibility,
            "assumptions":assumptions,"traces":traces}));
                    }
                }
            }
        }
    }
    let mut ranges: BTreeMap<String, Value> = BTreeMap::new();
    for run in &runs {
        for (topic, state) in run["final_states"]
            .as_object()
            .ok_or("invalid final states")?
        {
            let repetitions = state["repetitions"].as_f64().ok_or("invalid repetitions")?;
            let record = ranges.entry(topic.clone()).or_insert_with(
                || json!({"minimum_repetitions":repetitions,"maximum_repetitions":repetitions}),
            );
            record["minimum_repetitions"] = json!(
                record["minimum_repetitions"]
                    .as_f64()
                    .unwrap()
                    .min(repetitions)
            );
            record["maximum_repetitions"] = json!(
                record["maximum_repetitions"]
                    .as_f64()
                    .unwrap()
                    .max(repetitions)
            );
        }
    }
    Ok(
        json!({"schema_version":1,"source_hashes":{"progress":audit["sources"]["progress"]["sha256"],
        "question_observations":audit["sources"]["question_observations"]["sha256"]},
        "implementation_hashes":{"core.rs":format!("{:x}",Sha256::digest(include_bytes!("core.rs"))),
            "calibration.rs":format!("{:x}",Sha256::digest(include_bytes!("calibration.rs"))),
            "history.rs":format!("{:x}",Sha256::digest(include_bytes!("history.rs")))},
        "scenario_count":runs.len(),"scenarios":runs,"final_repetition_ranges_across_assumptions":ranges,
        "verified_production_predictions":0,
        "interpretation":"These are actual executions of the reconstructed engine on observed answers. Due-at-review agreement is compatibility only: scheduled due values, learner delays, intervening outcomes, and initial state are missing. The partial elapsed clock is a sensitivity control, not recovered exercise time. Distinct resulting states cannot be adjudicated against this history."}),
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    fn audit() -> Value {
        let root = Path::new(env!("CARGO_MANIFEST_DIR"));
        build_audit(
            &root.join("reference/progress.csv"),
            &root.join("reference/mathacademy-xp-observations.json"),
            None,
            None,
        )
        .unwrap()
    }
    #[test]
    fn real_history_preserves_unknowns_and_join_coverage() {
        let audit = audit();
        assert_eq!(audit["summary"]["activities"], 217);
        assert_eq!(audit["summary"]["observed_tasks"], 34);
        assert_eq!(audit["summary"]["observed_questions"], 308);
        assert_eq!(audit["summary"]["correct_questions"], 205);
        assert_eq!(
            audit["summary"]["observed_questions_with_task_topic_scope"],
            70
        );
        assert_eq!(audit["summary"]["join_issue_count"], 0);
        assert_eq!(audit["summary"]["snapshot_row_count_delta"], 3);
        assert_eq!(audit["summary"]["observation_snapshot_hash_matches"], false);
        for activity in audit["activities"].as_array().unwrap() {
            assert!(activity["fire_outcome"].is_null());
            assert!(activity["time_zone"].is_null());
        }
        let question =
            build_replay_scenario(&audit, "question_correct", "observed_elapsed_hours").unwrap();
        assert_eq!(question["events"].as_array().unwrap().len(), 70);
        assert_eq!(
            question["omitted_task_counts"],
            json!({"unobserved_task":183,"unmapped_or_conflicting_task":23})
        );
        let zeros: Vec<_> = question["events"]
            .as_array()
            .unwrap()
            .iter()
            .filter(|e| e["task_id"] == "13409092")
            .map(|e| e["success"].clone())
            .collect();
        assert_eq!(
            zeros,
            vec![
                json!(true),
                json!(true),
                json!(false),
                json!(true),
                json!(false)
            ]
        );
        let task = build_replay_scenario(&audit, "all_questions_correct", "wall_days").unwrap();
        assert_eq!(task["events"].as_array().unwrap().len(), 11);
        assert_eq!(
            task["events"]
                .as_array()
                .unwrap()
                .iter()
                .filter(|e| e["success"] == true)
                .count(),
            2
        );
        assert!(build_replay_scenario(&audit, "xp_positive", "wall_days").is_err());
    }
    #[test]
    fn full_sensitivity_grid_executes_real_transitions() {
        let audit = audit();
        let result = run_history_scenarios(&audit).unwrap();
        assert_eq!(result["scenario_count"], 32);
        for run in result["scenarios"].as_array().unwrap() {
            assert_eq!(run["topic_count"], 8);
            assert_eq!(
                run["observed_review_compatibility"]
                    .as_array()
                    .unwrap()
                    .len(),
                6
            );
            for trace in run["traces"].as_array().unwrap() {
                assert_eq!(trace["updates"].as_array().unwrap().len(), 1);
                assert_eq!(trace["updates"][0]["direct"], true);
            }
        }
        let range = &result["final_repetition_ranges_across_assumptions"]["1042"];
        assert!(
            range["maximum_repetitions"].as_f64().unwrap()
                > range["minimum_repetitions"].as_f64().unwrap()
        );
    }
}
