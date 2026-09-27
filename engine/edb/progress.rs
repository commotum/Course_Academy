//! Opt-in entity predicates for learner-owned topic progress.
use edb_core::{DatabaseValue, IndexPrefix, Keyword, SemanticError, TxFunctions, Value};
use std::collections::BTreeSet;

fn attr(db: &DatabaseValue, ns: &str, name: &str) -> Result<u32, SemanticError> {
    db.schema().resolve_ident(&Keyword::new(ns, name)).ok_or_else(|| {
        SemanticError::incorrect("progress/missing-schema", format!("Missing {ns}/{name}"))
    })
}

fn owners(db: &DatabaseValue, progress: u64) -> Result<Vec<u64>, SemanticError> {
    Ok(db.datoms_with_prefix(&IndexPrefix::Vaet {
        value: Value::Ref(progress),
        attribute: Some(attr(db, "learner", "knowledge-profile")?),
        entity: None,
    })?.into_iter().map(|datom| datom.entity).collect())
}

pub fn valid_profile(db: &DatabaseValue, learner: u64) -> Result<bool, SemanticError> {
    if db.values(learner, attr(db, "fire-learner", "id")?)?.is_empty() {
        return Ok(false);
    }
    let mut topics = BTreeSet::new();
    for value in db.values(learner, attr(db, "learner", "knowledge-profile")?)? {
        let Value::Ref(progress) = value else { return Ok(false) };
        if owners(db, progress)? != vec![learner]
            || db.values(progress, attr(db, "progress", "id")?)?.is_empty() {
            return Ok(false);
        }
        let values = db.values(progress, attr(db, "progress", "topic")?)?;
        let [Value::Ref(topic)] = values.as_slice() else { return Ok(false) };
        if db.values(*topic, attr(db, "topic", "id")?)?.is_empty()
            || !topics.insert(*topic) {
            return Ok(false);
        }
    }
    Ok(true)
}

pub fn valid_progress(db: &DatabaseValue, progress: u64) -> Result<bool, SemanticError> {
    let parents = owners(db, progress)?;
    match parents.as_slice() {
        [learner] => valid_profile(db, *learner),
        _ => Ok(false),
    }
}

pub fn register_progress_predicates(functions: &mut TxFunctions) {
    functions.register_entity_predicate("course-academy.progress/valid-profile?", valid_profile);
    functions.register_entity_predicate("course-academy.progress/valid-progress?", valid_progress);
}
