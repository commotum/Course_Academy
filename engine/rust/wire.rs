//! JSON boundary for command-line clients.
use crate::{
    Result,
    core::{Event, FireEngine},
    runtime::{self, ActivityRules, CompletionOptions},
    schema::{self, EntitySnapshot},
};
use serde_json::{Value, json};
fn decode<T: serde::de::DeserializeOwned>(v: &Value) -> Result<T> {
    serde_json::from_value(v.clone()).map_err(|e| e.to_string())
}
fn id(v: &Value) -> Result<u64> {
    v.as_u64().ok_or("nonnegative integer EID required".into())
}
fn options(v: &Value) -> Result<CompletionOptions> {
    let fields = v.as_object().ok_or("options must be an object")?;
    let allowed = [
        "completed_at",
        "result",
        "performance",
        "response_refs",
        "response_entities",
        "take_retry",
        "xp_award",
        "rules",
    ];
    if let Some(name) = fields.keys().find(|name| !allowed.contains(&name.as_str())) {
        return Err(format!("unknown completion option {name}"));
    }
    let mut options = CompletionOptions::new(schema::parse_instant(&v["completed_at"])?);
    if let Some(x) = v.get("result") {
        options.result = decode(x)?;
    }
    if let Some(x) = v.get("performance") {
        options.performance = decode(x)?;
    }
    if let Some(x) = v.get("response_refs") {
        options.response_refs = decode(x)?;
    }
    if let Some(x) = v.get("response_entities") {
        options.response_entities = decode(x)?;
    }
    if let Some(x) = v.get("take_retry") {
        options.take_retry = decode(x)?;
    }
    if let Some(x) = v.get("xp_award") {
        options.xp_award = decode(x)?;
    }
    if let Some(x) = v.get("rules").filter(|x| !x.is_null()) {
        options.rules = decode(x)?;
    }
    Ok(options)
}
/// Execute one request without database or filesystem side effects.
pub fn execute(input: &Value) -> Result<Value> {
    let op = input["op"].as_str().ok_or("op required")?;
    match op {
        "estimate_lesson_xp" | "calibrate_lesson_xp" => {
            let features = if let Some(features) = input.get("features") {
                decode::<crate::base_xp::Features>(features)?
            } else {
                crate::base_xp::Features::from_content(
                    &input["content"],
                    input["tutorial_words"]
                        .as_u64()
                        .ok_or("tutorial word count required")? as usize,
                    true,
                )?
            };
            let weights = input
                .get("weights")
                .map(decode)
                .transpose()?
                .unwrap_or(crate::base_xp::DEFAULT_WEIGHTS);
            let result = if op == "calibrate_lesson_xp" {
                crate::base_xp::calibrate(
                    features,
                    weights,
                    input["base_xp"]
                        .as_i64()
                        .ok_or("authoritative base XP required")?,
                )?
            } else {
                crate::base_xp::estimate(
                    features,
                    weights,
                    input
                        .get("multiplier")
                        .map(|v| v.as_f64().ok_or("multiplier must be numeric"))
                        .transpose()?
                        .unwrap_or(1.0),
                )?
            };
            serde_json::to_value(result).map_err(|e| e.to_string())
        }
        "apply" | "apply_accuracy" | "apply_retention" | "rank" | "due" | "restore" => {
            let mut engine = FireEngine::restore(input["engine"].clone())?;
            let output = match op {
                "apply" => engine.apply(decode::<Event>(&input["event"])?)?,
                "apply_accuracy" => engine.apply_accuracy(decode::<Event>(&input["event"])?)?,
                "apply_retention" => engine.apply_retention(decode::<Event>(&input["event"])?)?,
                "rank" => json!(engine.rank(
                    input["learner"].as_str().ok_or("learner required")?,
                    decode(&input["at"])?,
                    decode(&input["candidates"])?
                )?),
                "due" => json!(engine.due(
                    input["learner"].as_str().ok_or("learner required")?,
                    decode(&input["at"])?
                )?),
                _ => Value::Null,
            };
            Ok(json!({"output":output,"engine":engine.snapshot()}))
        }
        "load_runtime"
        | "complete_item"
        | "expire_task"
        | "transition_item"
        | "completion_transaction"
        | "task_transaction" => {
            let snapshot = EntitySnapshot::from_json(&input["snapshot"])?;
            let mut loaded = schema::load_runtime(
                snapshot,
                id(&input["learner_eid"])?,
                id(&input["policy_eid"])?,
            )?;
            if let Some(e) = input.get("engine") {
                loaded.engine = FireEngine::restore(e.clone())?;
            }
            if op == "load_runtime" {
                return Ok(json!({"engine":loaded.engine.snapshot()}));
            }
            let target = id(&input["target"])?;
            if op == "transition_item" {
                return Ok(
                    json!({"transaction":runtime::transition_item(&loaded,target,input["status"].as_str().ok_or("status required")?,schema::parse_instant(&input["at"])?)?}),
                );
            }
            if op == "completion_transaction" || op == "task_transaction" {
                let engine = FireEngine::restore(input["updated_engine"].clone())?;
                let at = schema::parse_instant(&input["completed_at"])?;
                let changes = decode(&input["changes"])?;
                let plan = if op == "completion_transaction" {
                    schema::completion_transaction(&loaded, target, at, changes, &engine)?
                } else {
                    schema::task_transaction(&loaded, target, at, changes, &engine)?
                };
                return Ok(json!({"transaction":plan}));
            }
            let done = if op == "complete_item" {
                runtime::complete_item(&loaded, target, options(&input["options"])?)?
            } else {
                let opts = &input["options"];
                runtime::expire_task(
                    &loaded,
                    target,
                    schema::parse_instant(&opts["completed_at"])?,
                    decode(opts.get("xp_award").unwrap_or(&Value::Null))?,
                    decode::<ActivityRules>(
                        opts.get("rules")
                            .filter(|x| !x.is_null())
                            .unwrap_or(&json!({})),
                    )?,
                )?
            };
            Ok(
                json!({"transaction":done.transaction,"delivery":done.delivery,"engine":done.engine.snapshot()}),
            )
        }
        _ => Err(format!("unknown engine operation {op}")),
    }
}
