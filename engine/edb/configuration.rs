//! Native EDB checks for typed policy settings and optional topic difficulty.
use edb_core::{DatabaseValue, Keyword, SemanticError, TxFunctions, Value};

fn value(
    db: &DatabaseValue,
    entity: u64,
    ns: &str,
    name: &str,
) -> Result<Option<Value>, SemanticError> {
    let attr = db
        .schema()
        .resolve_ident(&Keyword::new(ns, name))
        .ok_or_else(|| {
            SemanticError::incorrect(
                "configuration/missing-schema",
                format!("Missing {ns}/{name}"),
            )
        })?;
    Ok(db.values(entity, attr)?.into_iter().next())
}

fn enum_is(
    db: &DatabaseValue,
    candidate: &Option<Value>,
    ns: &str,
    name: &str,
) -> Result<bool, SemanticError> {
    let Some(Value::Ref(entity)) = candidate else {
        return Ok(false);
    };
    Ok(value(db, *entity, "db", "ident")? == Some(Value::Keyword(Keyword::new(ns, name))))
}

pub fn valid_policy(db: &DatabaseValue, entity: u64) -> Result<bool, SemanticError> {
    let get = |name| value(db, entity, "policy", name);
    if !matches!(get("gate-slow-implicit")?, Some(Value::Bool(_))) {
        return Ok(false);
    }
    let order = get("retention-update-order")?;
    if !enum_is(db, &order, "policy.retention-update", "decay-before-add")?
        && !enum_is(db, &order, "policy.retention-update", "add-before-decay")?
    {
        return Ok(false);
    }
    let number = |name| -> Result<f64, SemanticError> {
        match get(name)? {
            Some(Value::Double(x)) if x.is_finite() && x >= 0.0 => Ok(x),
            _ => Err(SemanticError::incorrect(
                "policy/invalid-number",
                format!("{name} must be a finite nonnegative double"),
            )),
        }
    };
    let base = number("base-half-life-days")?;
    let growth = number("interval-growth")?;
    let maximum = number("maximum-half-life-days")?;
    let threshold = number("review-threshold")?;
    let initial_retention = number("initial-retention")?;
    let discount = number("early-practice-discount-power")?;
    let accuracy = number("initial-accuracy")?;
    let rate = number("accuracy-update-rate")?;
    let min_speed = number("minimum-speed")?;
    let max_speed = number("maximum-speed")?;
    let max_failure = number("maximum-failure-multiplier")?;
    number("speed-exponent")?;
    number("overdue-failure-slope")?;
    number("future-horizon-days")?;
    Ok(base > 0.0
        && growth > 1.0
        && maximum >= base
        && threshold > 0.0
        && threshold < initial_retention
        && discount > 0.0
        && accuracy > 0.0
        && accuracy < 1.0
        && rate > 0.0
        && rate <= 1.0
        && min_speed > 0.0
        && min_speed <= 1.0
        && max_speed >= 1.0
        && max_failure >= 1.0)
}

pub fn valid_topic_difficulty(db: &DatabaseValue, entity: u64) -> Result<bool, SemanticError> {
    match value(db, entity, "topic", "difficulty")? {
        // General topic validation permits unknown difficulty.
        None => Ok(true),
        Some(Value::Double(difficulty)) => {
            Ok(difficulty.is_finite() && (0.0..=1.0).contains(&difficulty))
        }
        _ => Ok(false),
    }
}

pub fn register_configuration_predicates(functions: &mut TxFunctions) {
    functions.register_entity_predicate("course-academy.policy/valid?", valid_policy);
    functions.register_entity_predicate(
        "course-academy.topic/valid-difficulty?",
        valid_topic_difficulty,
    );
}
