//! Opt-in entity predicates for learner-owned topic progress.
use edb_core::{DatabaseValue, IndexPrefix, Keyword, SemanticError, TxFunctions, Value};
use std::collections::BTreeSet;

fn attr(db: &DatabaseValue, ns: &str, name: &str) -> Result<u32, SemanticError> {
    db.schema()
        .resolve_ident(&Keyword::new(ns, name))
        .ok_or_else(|| {
            SemanticError::incorrect("progress/missing-schema", format!("Missing {ns}/{name}"))
        })
}

fn owners(db: &DatabaseValue, progress: u64) -> Result<Vec<u64>, SemanticError> {
    Ok(db
        .datoms_with_prefix(&IndexPrefix::Vaet {
            value: Value::Ref(progress),
            attribute: Some(attr(db, "learner", "knowledge-profile")?),
            entity: None,
        })?
        .into_iter()
        .map(|datom| datom.entity)
        .collect())
}

pub fn valid_profile(db: &DatabaseValue, learner: u64) -> Result<bool, SemanticError> {
    if db.values(learner, attr(db, "learner", "id")?)?.is_empty() {
        return Ok(false);
    }
    let mut topics = BTreeSet::new();
    for value in db.values(learner, attr(db, "learner", "knowledge-profile")?)? {
        let Value::Ref(progress) = value else {
            return Ok(false);
        };
        if owners(db, progress)? != vec![learner]
            || db.values(progress, attr(db, "progress", "id")?)?.is_empty()
        {
            return Ok(false);
        }
        let values = db.values(progress, attr(db, "progress", "topic")?)?;
        let [Value::Ref(topic)] = values.as_slice() else {
            return Ok(false);
        };
        if db.values(*topic, attr(db, "topic", "id")?)?.is_empty() || !topics.insert(*topic) {
            return Ok(false);
        }
    }
    Ok(true)
}

pub fn valid_progress(db: &DatabaseValue, progress: u64) -> Result<bool, SemanticError> {
    let parents = owners(db, progress)?;
    let [learner] = parents.as_slice() else {
        return Ok(false);
    };
    if !valid_profile(db, *learner)? {
        return Ok(false);
    }
    for name in [
        "repetitions", "memory", "interval-days", "assessment-accuracy",
        "practice-accuracy", "assessment-mass", "practice-mass",
    ] {
        let values = db.values(progress, attr(db, "progress", name)?)?;
        let [Value::Double(value)] = values.as_slice() else {
            return Ok(false);
        };
        if !value.is_finite() || *value < 0.0
            || (name == "interval-days" && *value == 0.0)
            || (name.ends_with("accuracy") && *value > 1.0)
        {
            return Ok(false);
        }
    }
    // The reference must identify a policy, not just any existing EDB entity.
    let policies = db.values(progress, attr(db, "progress", "policy")?)?;
    let [Value::Ref(policy)] = policies.as_slice() else {
        return Ok(false);
    };
    Ok(!db.values(*policy, attr(db, "policy", "id")?)?.is_empty())
}

pub fn register_progress_predicates(functions: &mut TxFunctions) {
    functions.register_entity_predicate("course-academy.progress/valid-profile?", valid_profile);
    functions.register_entity_predicate("course-academy.progress/valid-progress?", valid_progress);
}
