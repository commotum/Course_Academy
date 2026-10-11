//! Opt-in, type-specific validation of field-owned answer banks.
use edb_core::{DatabaseValue, IndexPrefix, Keyword, SemanticError, TxFunctions, Value};
use std::collections::BTreeSet;

fn attr(db: &DatabaseValue, ns: &str, name: &str) -> Result<u32, SemanticError> {
    db.schema()
        .resolve_ident(&Keyword::new(ns, name))
        .ok_or_else(|| {
            SemanticError::incorrect(
                "answer-field/missing-schema",
                format!("Missing {ns}/{name}"),
            )
        })
}
fn values(
    db: &DatabaseValue,
    entity: u64,
    ns: &str,
    name: &str,
) -> Result<Vec<Value>, SemanticError> {
    db.values(entity, attr(db, ns, name)?)
}
fn ident(db: &DatabaseValue, entity: u64) -> Result<Option<Keyword>, SemanticError> {
    let found = values(db, entity, "db", "ident")?;
    Ok(match found.as_slice() {
        [Value::Keyword(k)] => Some(k.clone()),
        _ => None,
    })
}

pub fn valid_field(db: &DatabaseValue, field: u64) -> Result<bool, SemanticError> {
    if !matches!(
        values(db, field, "answer-field", "id")?.as_slice(),
        [Value::Uuid(_)]
    ) || !matches!(values(db, field, "answer-field", "key")?.as_slice(), [Value::String(k)] if !k.trim().is_empty())
    {
        return Ok(false);
    }
    let kind_values = values(db, field, "answer-field", "type")?;
    let [Value::Ref(kind)] = kind_values.as_slice() else {
        return Ok(false);
    };
    let Some(kind) = ident(db, *kind)? else {
        return Ok(false);
    };
    let kind = kind.qualified_name();
    if ![
        "answer-field.type/radio",
        "answer-field.type/blank",
        "answer-field.type/select",
        "answer-field.type/checkbox",
        "answer-field.type/free",
    ]
    .contains(&kind.as_str())
    {
        return Ok(false);
    }
    let choices = values(db, field, "answer-field", "choices")?;
    let correct = values(db, field, "answer-field", "correct")?;
    if !matches!(correct.as_slice(), [] | [Value::Ref(_)]) {
        return Ok(false);
    }
    if kind != "answer-field.type/free" && (choices.is_empty() || correct.is_empty()) {
        return Ok(false);
    }
    if correct
        .first()
        .is_some_and(|answer| !choices.contains(answer))
    {
        return Ok(false);
    }
    let ownership_attr = attr(db, "answer-field", "choices")?;
    let mut distinct = BTreeSet::new();
    let mut boolean_values = BTreeSet::new();
    for choice in &choices {
        let Value::Ref(answer) = choice else {
            return Ok(false);
        };
        if !matches!(
            values(db, *answer, "answer", "id")?.as_slice(),
            [Value::Uuid(_)]
        ) {
            return Ok(false);
        }
        let owners: BTreeSet<_> = db
            .datoms_with_prefix(&IndexPrefix::Vaet {
                value: Value::Ref(*answer),
                attribute: Some(ownership_attr),
                entity: None,
            })?
            .into_iter()
            .map(|d| d.entity)
            .collect();
        if owners != BTreeSet::from([field]) {
            return Ok(false);
        }
        let representations = values(db, *answer, "answer", "type")?;
        let [Value::Ref(representation)] = representations.as_slice() else {
            return Ok(false);
        };
        let Some(representation) = ident(db, *representation)? else {
            return Ok(false);
        };
        let representation = representation.qualified_name();
        if !["answer.type/math", "answer.type/text", "answer.type/image"]
            .contains(&representation.as_str())
        {
            return Ok(false);
        }
        let contents = values(db, *answer, "answer", "value")?;
        let [Value::String(content)] = contents.as_slice() else {
            return Ok(false);
        };
        if !distinct.insert((representation.clone(), content.clone())) {
            return Ok(false);
        }
        if kind == "answer-field.type/checkbox" {
            if representation != "answer.type/text"
                || !["true", "false"].contains(&content.as_str())
            {
                return Ok(false);
            }
            boolean_values.insert(content.clone());
        }
        if kind == "answer-field.type/blank"
            && correct.contains(choice)
            && (content.trim().is_empty()
                || !["answer.type/math", "answer.type/text"].contains(&representation.as_str()))
        {
            return Ok(false);
        }
    }
    Ok(kind != "answer-field.type/checkbox"
        || (choices.len() == 2
            && boolean_values == BTreeSet::from(["true".into(), "false".into()])))
}

pub fn register_answer_field_predicates(functions: &mut TxFunctions) {
    functions.register_entity_predicate("course-academy.answer-field/valid?", valid_field);
}
