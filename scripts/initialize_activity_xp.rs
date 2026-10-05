//! Read-only native planner for initial catalog workload estimates.
//! Writes a reviewable JSON plan; the Python wrapper handles guarded commits.
use course_academy_engine::{base_xp, question_selection, schema::{self, EntitySnapshot, Record}};
use edb_core::{Cardinality, IndexOrder, Peer, Value, postgres_config_from_env};
use serde_json::{Value as Json, json};
use std::{collections::BTreeMap, error::Error, fs};

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.len() != 2 { return Err("usage: initialize_activity_xp DATABASE PLAN.json".into()); }
    let db = Peer::connect_configured(&postgres_config_from_env()?, &args[0], 256)?.db();
    let mut entities = BTreeMap::<u64, Record>::new();
    for d in db.collect_datoms(IndexOrder::Eavt)? {
        let a = db.schema().attribute(d.attribute)?;
        let name = a.ident.qualified_name();
        if (name.starts_with("db/") || name.starts_with("db.")) && name != "db/ident" { continue; }
        let v = match d.value {
            Value::String(v) | Value::Uri(v) => json!(v),
            Value::Long(v) => json!(v), Value::Double(v) => json!(v), Value::Float(v) => json!(v),
            Value::Bool(v) => json!(v), Value::Ref(v) => json!(v),
            Value::Keyword(v) => schema::keyword(&v.qualified_name()),
            Value::Uuid(v) => { let h = format!("{v:032x}"); json!({"$uuid":format!("{}-{}-{}-{}-{}", &h[..8],&h[8..12],&h[12..16],&h[16..20],&h[20..])}) },
            Value::Instant(v) => json!({"$instant":v}),
            _ => return Err("unsupported domain value".into()),
        };
        let entity = entities.entry(d.entity).or_default();
        if a.cardinality == Cardinality::Many {
            entity.entry(name).or_insert(json!([])).as_array_mut().unwrap().push(v);
        } else { entity.insert(name, v); }
    }
    let s = EntitySnapshot::new(entities, db.basis_t())?;
    let policy = question_selection::active_policy(&s)?;
    let weights = question_selection::weights(&s, policy, "lesson", 0)?.unwrap_or(base_xp::DEFAULT_WEIGHTS);
    let mut forms = vec![];
    let mut estimates = vec![];
    let mut preserved = vec![];
    let mut skipped = vec![];
    for (activity, r) in &s.entities {
        if !r.contains_key("activity/id") { continue; }
        if r.contains_key("activity/expected-seconds") { preserved.push(activity); continue; }
        let kind = s.ident(r.get("activity/type").ok_or("activity type required")?)?;
        if kind == "activity.type/lesson" {
            match base_xp::activity_estimate_with_weights(&s, *activity, weights) {
                Ok(estimate) => {
                    forms.push(json!({"db/id":activity,"activity/expected-seconds":estimate.expected_seconds}));
                    estimates.push(json!({"activity":activity,"title":r.get("activity/title"),"estimate":estimate}));
                }
                Err(error) => skipped.push(json!({"activity":activity,"type":kind,"title":r.get("activity/title"),"reason":error})),
            }
        } else {
            // Other activity types can use explicit time limits or authored step
            // durations. Never apply a lesson floor/formula to an assignment.
            let limit = r.get("activity/time-limit-seconds").and_then(Json::as_f64)
                .filter(|v| v.is_finite() && *v > 0.0 && matches!(kind.as_str(), "activity.type/assessment" | "activity.type/quiz"));
            let steps = s.refs(*activity,"activity/steps")?;
            let durations: Option<Vec<f64>> = steps.iter().map(|step| s.entity(*step).ok()?
                .get("step/expected-seconds")?.as_f64().filter(|v| v.is_finite() && *v > 0.0)).collect();
            let seconds = limit.or_else(|| durations.filter(|v| !v.is_empty()).map(|v| v.iter().sum()));
            if let Some(seconds) = seconds.filter(|v| v.is_finite() && *v > 0.0) {
                forms.push(json!({"db/id":activity,"activity/expected-seconds":seconds}));
                estimates.push(json!({"activity":activity,"title":r.get("activity/title"),"expected_seconds":seconds,"source":"explicit time limit or complete step durations"}));
            } else { skipped.push(json!({"activity":activity,"type":kind,"title":r.get("activity/title"),"reason":"no duration model or complete step durations for this activity type"})); }
        }
    }
    let report = json!({"basis":s.basis_t,"formula_version":base_xp::VERSION,
        "sampling":"whole unordered database KP pool; capture calibration uses first two in presentation order",
        "estimated_count":estimates.len(),"preserved_count":preserved.len(),"skipped_count":skipped.len(),
        "forms":forms,"estimates":estimates,"preserved":preserved,"skipped":skipped});
    fs::write(&args[1], serde_json::to_vec_pretty(&report)?)?;
    println!("{}",json!({"basis":s.basis_t,"estimated":estimates.len(),"preserved":preserved.len(),"skipped":skipped.len()}));
    Ok(())
}
