//! Read-only independent durable audit. No transaction or speculation API is called.
//! Usage: committed-verify DATABASE BEFORE_BASIS AFTER_BASIS STAGE1_RECEIPT STAGE2_RECEIPT IDS OUTDIR
//! Stage 1 must be BEFORE_BASIS+1 and AFTER_BASIS must be BEFORE_BASIS+2.
use edb_core::edn::{EdnValue, read_edn, write_edn};
use edb_core::edn_pull::{entity_identifier_from_edn, parse_pull_edn};
use edb_core::edn_value::{edn_keyword, edn_to_value, query_value_to_edn,
    value_to_edn};
use edb_core::{DatabaseValue, Datom, EntityIdentifier, IndexPrefix, Keyword, Peer,
    PullControl, Value, postgres_config_from_env};
use std::{collections::BTreeSet, error::Error, fs, path::Path};

const QUESTION_PULL: &str = r#"[* {:question/difficulty [:db/id :db/ident]}
 {:knowledge-point/_questions [:knowledge-point/id :knowledge-point/title]}
 {:knowledge-point/_canonical-example [:knowledge-point/id :knowledge-point/title]}
 {:question/answer-fields [* {:answer-field/type [:db/ident]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}
 {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]"#;
// The user explicitly requested current-state retirement of these two superseded
// field/answer graphs, with their original facts retained in immutable history.
const RETIRING_QUESTIONS: [&str; 2] = ["q-79044", "q-79945"];

type Result<T> = std::result::Result<T, Box<dyn Error>>;

fn bounded_read(path: &Path) -> Result<String> {
    if fs::metadata(path)?.len() > 16 * 1024 * 1024 {
        return Err(format!("Input exceeds 16 MiB: {}", path.display()).into());
    }
    Ok(fs::read_to_string(path)?)
}

fn save(path: &Path, value: &EdnValue) -> Result<()> {
    fs::write(path, format!("{}\n", write_edn(value)?))?;
    Ok(())
}

fn source_id(db: &DatabaseValue, namespace: &str, name: &str) -> Result<u64> {
    db.resolve_entity_identifier(&EntityIdentifier::Ident(Keyword::new(namespace, name)))?
        .ok_or_else(|| format!("Required existing source :{namespace}/{name} is absent").into())
}

fn question_reads(db: &DatabaseValue, ids: &[String], require_present: bool) -> Result<EdnValue> {
    let pattern = parse_pull_edn(QUESTION_PULL)?;
    let control = PullControl { max_depth: 12, max_entities: 10_000, ..Default::default() };
    let mut rows = Vec::new();
    for id in ids {
        let lookup = entity_identifier_from_edn(&EdnValue::Vector(vec![
            edn_keyword("question", "math-academy-id"), EdnValue::String(id.clone())]))?;
        if require_present && db.resolve_entity_identifier(&lookup)?.is_none() {
            return Err(format!("Question missing after speculative transaction: {id}").into());
        }
        let pulled = db.pull_with_control(&pattern, lookup, &control)?;
        rows.push(EdnValue::Vector(vec![EdnValue::String(id.clone()), query_value_to_edn(&pulled)?]));
    }
    Ok(EdnValue::Vector(rows))
}

fn component_ids(value: &EdnValue, found: &mut BTreeSet<u64>) -> Result<()> {
    match value {
        EdnValue::Map(entries) => {
            if entries.iter().any(|(k, _)| *k == edn_keyword("answer-field", "id") ||
                *k == edn_keyword("answer", "id")) {
                let raw = entries.iter().find(|(k, _)| *k == edn_keyword("db", "id"))
                    .ok_or("Component pull has no :db/id")?;
                let id = match edn_to_value(&raw.1)? {
                    Value::Ref(id) => id,
                    Value::Long(id) if id >= 0 => id as u64,
                    _ => return Err("Unexpected component :db/id representation".into()),
                };
                found.insert(id);
            }
            for (_, child) in entries { component_ids(child, found)?; }
        }
        EdnValue::Vector(items) | EdnValue::List(items) | EdnValue::Set(items) => {
            for child in items { component_ids(child, found)?; }
        }
        _ => {}
    }
    Ok(())
}

fn component_reads(db: &DatabaseValue, ids: &BTreeSet<u64>) -> Result<EdnValue> {
    let pattern = parse_pull_edn("[*]")?;
    let control = PullControl { max_depth: 12, max_entities: 10_000, ..Default::default() };
    let mut rows = Vec::new();
    for id in ids {
        let value = db.pull_with_control(&pattern, *id, &control)?;
        rows.push(EdnValue::Vector(vec![EdnValue::Long(*id as i64), query_value_to_edn(&value)?]));
    }
    Ok(EdnValue::Vector(rows))
}

fn entity_facts(db: &DatabaseValue, entity: u64) -> Result<Vec<edb_core::Datom>> {
    Ok(db.collect_datoms_with_prefix(&IndexPrefix::Eavt {
        entity, attribute: None, value: None })?)
}

fn attribute_name(db: &DatabaseValue, attribute: u32) -> Result<String> {
    Ok(db.ident(attribute as u64).ok_or("Attribute has no ident")?.qualified_name())
}

struct Retirement {
    components: BTreeSet<u64>,
    fields: BTreeSet<u64>,
    questions: BTreeSet<u64>,
}

fn retirement_scope(base: &DatabaseValue, stage1: &DatabaseValue) -> Result<Retirement> {
    let ids: Vec<String> = RETIRING_QUESTIONS.iter().map(|id| id.to_string()).collect();
    let questions = question_reads(stage1, &ids, true)?;
    let mut components = BTreeSet::new();
    component_ids(&questions, &mut components)?;
    let mut fields = BTreeSet::new();
    let mut owners = BTreeSet::new();
    for id in &ids {
        let lookup = entity_identifier_from_edn(&EdnValue::Vector(vec![
            edn_keyword("question", "math-academy-id"), EdnValue::String(id.clone())]))?;
        if base.resolve_entity_identifier(&lookup)?.is_some() {
            return Err(format!("Retirement scope unexpectedly existed at the durable base: {id}").into());
        }
        owners.insert(stage1.resolve_entity_identifier(&lookup)?.ok_or("Retirement question missing")?);
    }
    for entity in &components {
        if !entity_facts(base, *entity)?.is_empty() {
            return Err(format!("Retired component existed before stage 1: {entity}").into());
        }
        for fact in entity_facts(stage1, *entity)? {
            if attribute_name(stage1, fact.attribute)? == "answer-field/id" {
                fields.insert(*entity);
            }
        }
    }
    if fields.len() != 2 || owners.len() != 2 {
        return Err("Retirement must contain exactly the two authorized original fields".into());
    }
    // retractEntity also retracts incoming ordinary references. Refuse any
    // learner response or reference outside these field graphs and owner links.
    for entity in &components {
        let incoming = stage1.collect_datoms_with_prefix(&IndexPrefix::Vaet {
            value: Value::Ref(*entity), attribute: None, entity: None })?;
        for fact in incoming {
            let name = attribute_name(stage1, fact.attribute)?;
            let internal = fields.contains(&fact.entity) &&
                matches!(name.as_str(), "answer-field/choices" | "answer-field/correct");
            let ownership = fields.contains(entity) && owners.contains(&fact.entity) &&
                name == "question/answer-fields";
            if !internal && !ownership {
                return Err(format!("Retired component {entity} has external reference from {} through {name}", fact.entity).into());
            }
        }
    }
    Ok(Retirement { components, fields, questions: owners })
}

fn validate_retirement(out: &Path, base: &DatabaseValue, stage1: &DatabaseValue,
                       stage2: &AuditReport,
                       original_ids: &BTreeSet<u64>, ids: &[String], stage1_basis: u64) -> Result<Retirement> {
    let retiring = retirement_scope(base, stage1)?;
    let mut removed_fields = BTreeSet::new();
    let mut removed_answers = BTreeSet::new();
    for fact in &stage2.tx_data {
        if !fact.added {
            match attribute_name(stage1, fact.attribute)?.as_str() {
                "answer-field/id" => { removed_fields.insert(fact.entity); }
                "answer/id" => { removed_answers.insert(fact.entity); }
                _ => {}
            }
        }
    }
    let expected_answers: BTreeSet<u64> = retiring.components.difference(&retiring.fields).copied().collect();
    if removed_fields != retiring.fields || removed_answers != expected_answers {
        return Err("Stage 2 retirement differs from the exact two authorized field/answer graphs".into());
    }
    for entity in &retiring.components {
        if !entity_facts(&stage2.db_after, *entity)?.is_empty() {
            return Err(format!("Retired component still has current facts: {entity}").into());
        }
        let incoming = stage2.db_after.collect_datoms_with_prefix(&IndexPrefix::Vaet {
            value: Value::Ref(*entity), attribute: None, entity: None })?;
        if !incoming.is_empty() { return Err(format!("Retired component has remaining incoming references: {entity}").into()); }
    }
    let remaining: BTreeSet<u64> = original_ids.difference(&retiring.components).copied().collect();
    if component_reads(stage1, &remaining)? != component_reads(&stage2.db_after, &remaining)? {
        return Err("Stage 2 altered a non-retiring original field/answer entity".into());
    }
    // Read historical state from the completed stage 2 branch, independently of
    // the saved stage 1 object, to prove retired facts are actually recoverable.
    let historical = stage2.db_after.clone().as_of(stage1_basis);
    let historical_components = component_reads(&historical, original_ids)?;
    save(&out.join("stage2-as-of-stage1-original-components.edn"), &historical_components)?;
    if historical_components != component_reads(stage1, original_ids)? {
        return Err("Original field/answer graph cannot be recovered from stage 2 history".into());
    }
    let historical_questions = question_reads(&historical, ids, true)?;
    save(&out.join("stage2-as-of-stage1-questions.edn"), &historical_questions)?;
    if historical_questions != question_reads(stage1, ids, true)? {
        return Err("Original question graph cannot be recovered from stage 2 history".into());
    }
    save(&out.join("stage2-retirement.edn"), &EdnValue::Map(vec![
        (edn_keyword("retirement", "questions"), EdnValue::Vector(RETIRING_QUESTIONS.iter().map(|v| EdnValue::String(v.to_string())).collect())),
        (edn_keyword("retirement", "field-ids"), EdnValue::Vector(retiring.fields.iter().map(|v| EdnValue::Long(*v as i64)).collect())),
        (edn_keyword("retirement", "answer-ids"), EdnValue::Vector(expected_answers.iter().map(|v| EdnValue::Long(*v as i64)).collect())),
        (edn_keyword("retirement", "external-incoming-references"), EdnValue::Long(0)),
        (edn_keyword("retirement", "all-current-facts-retracted"), EdnValue::Bool(true)),
        (edn_keyword("retirement", "all-originals-recovered-from-history"), EdnValue::Bool(true)),
        (edn_keyword("retirement", "unaffected-components-unchanged"), EdnValue::Bool(true)),
    ]))?;
    Ok(retiring)
}

fn save_history(out: &Path, label: &str, before: &DatabaseValue,
                report: &AuditReport) -> Result<()> {
    let history = report.db_after.clone().history();
    let entities: BTreeSet<u64> = report.tx_data.iter().map(|d| d.entity).collect();
    let mut history_rows = Vec::new();
    for entity in entities {
        let prefix = IndexPrefix::Eavt { entity, attribute: None, value: None };
        let datoms = history.collect_datoms_with_prefix(&prefix)?;
        for receipt_fact in report.tx_data.iter().filter(|d| d.entity == entity) {
            if !datoms.contains(receipt_fact) {
                return Err(format!("{label} receipt fact absent from final history: {receipt_fact:?}").into());
            }
        }
        // Every withdrawn assertion remains attributable to its original source in history.
        for removal in report.tx_data.iter().filter(|d| d.entity == entity && !d.added) {
            let current = before.collect_datoms_with_prefix(&IndexPrefix::Eavt {
                entity, attribute: Some(removal.attribute), value: Some(removal.value.clone()) })?;
            if current.is_empty() || !datoms.contains(removal) ||
                current.iter().any(|assertion| !datoms.contains(assertion)) {
                return Err(format!("Original assertion or repair retraction absent from history for entity {entity}").into());
            }
        }
        for d in datoms {
            history_rows.push(EdnValue::Vector(vec![EdnValue::Long(d.entity as i64),
                EdnValue::Long(d.attribute as i64), value_to_edn(&d.value)?,
                EdnValue::Long(d.tx as i64), EdnValue::Long(d.source as i64), EdnValue::Bool(d.added)]));
        }
    }
    save(&out.join(format!("{label}-changed-entity-history.edn")), &EdnValue::Vector(history_rows))
}


struct AuditReport {
    db_after: DatabaseValue,
    tx_data: Vec<Datom>,
}

fn map_get<'a>(value: &'a EdnValue, name: &str) -> Result<&'a EdnValue> {
    let EdnValue::Map(entries) = value else { return Err("Receipt must be an EDN map".into()) };
    entries.iter().find(|(k, _)| *k == edn_keyword("edb", name)).map(|(_, v)| v)
        .ok_or_else(|| format!("Missing receipt field :edb/{name}").into())
}

fn number(value: &EdnValue) -> Result<u64> {
    match edn_to_value(value)? {
        Value::Long(v) if v >= 0 => Ok(v as u64),
        Value::Ref(v) => Ok(v),
        _ => Err("Expected a nonnegative integer or entity reference".into()),
    }
}

fn read_receipt(path: &Path, before: u64, after: u64, source: u64,
                final_db: &DatabaseValue) -> Result<AuditReport> {
    let data = read_edn(&bounded_read(path)?)?;
    if map_get(&data, "committed")? != &EdnValue::Bool(true) {
        return Err(format!("Receipt is not confirmed committed: {}", path.display()).into());
    }
    if number(map_get(&data, "db-before-t")?)? != before ||
        number(map_get(&data, "db-after-t")?)? != after {
        return Err(format!("Receipt basis differs from the requested durable sequence: {}", path.display()).into());
    }
    let EdnValue::Vector(rows) = map_get(&data, "tx-data")? else {
        return Err("Receipt tx-data must be a vector".into())
    };
    let mut tx_data = Vec::new();
    for row in rows {
        let EdnValue::Vector(values) = row else { return Err("Datom must be a vector".into()) };
        if values.len() != 6 { return Err("Datom must have six coordinates".into()); }
        let added = match values[5] { EdnValue::Bool(v) => v, _ => return Err("Datom addition flag must be boolean".into()) };
        let datom = Datom {
            entity: number(&values[0])?,
            attribute: u32::try_from(number(&values[1])?)?,
            value: edn_to_value(&values[2])?,
            tx: number(&values[3])?,
            source: number(&values[4])?,
            added,
        };
        if datom.source != source { return Err(format!("Receipt has unexpected source {}", datom.source).into()); }
        tx_data.push(datom);
    }
    if tx_data.is_empty() { return Err("Committed receipt unexpectedly has no datoms".into()); }
    // Keep the final historical database for checking both receipts, so stage 1
    // facts retired by stage 2 are checked in the final result's retained history.
    Ok(AuditReport { db_after: final_db.clone(), tx_data })
}

fn run() -> Result<()> {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.len() != 7 {
        return Err("Usage: committed-verify DATABASE BEFORE_BASIS AFTER_BASIS STAGE1_RECEIPT STAGE2_RECEIPT IDS OUTDIR".into());
    }
    let database = &args[0];
    let before: u64 = args[1].parse()?;
    let after: u64 = args[2].parse()?;
    let stage1_basis = before.checked_add(1).ok_or("Invalid before basis")?;
    if before.checked_add(2) != Some(after) { return Err("Expected exactly two adjacent committed transactions".into()); }
    let ids_value = read_edn(&bounded_read(Path::new(&args[5]))?)?;
    let EdnValue::Vector(items) = ids_value else { return Err("IDS must be a vector".into()) };
    let ids: Vec<String> = items.into_iter().map(|v| match v {
        EdnValue::String(id) if id.starts_with("q-") => Ok(id),
        _ => Err("IDS must contain only q-N strings"),
    }).collect::<std::result::Result<_, _>>()?;
    if ids.len() != 26 || ids.iter().collect::<BTreeSet<_>>().len() != 26 {
        return Err("Expected exactly 26 distinct question IDs".into());
    }
    let config = postgres_config_from_env()?;
    let final_db = Peer::connect_configured(&config, database, 128)?.db();
    if final_db.basis_t() != after {
        return Err(format!("Expected durable basis {after}, found {}", final_db.basis_t()).into());
    }
    let ma_source = source_id(&final_db, "org", "Math-Academy")?;
    let repair_source = source_id(&final_db, "agent", "gpt-6-astra-ultra")?;
    let stage1_receipt = read_receipt(Path::new(&args[3]), before, stage1_basis, ma_source, &final_db)?;
    let stage2_receipt = read_receipt(Path::new(&args[4]), stage1_basis, after, repair_source, &final_db)?;
    let base = final_db.clone().as_of(before);
    let stage1 = final_db.clone().as_of(stage1_basis);
    let out = Path::new(&args[6]);
    fs::create_dir_all(out)?;
    let before_questions = question_reads(&base, &ids, false)?;
    let original_questions = question_reads(&stage1, &ids, true)?;
    let final_questions = question_reads(&final_db, &ids, true)?;
    save(&out.join("before-questions.edn"), &before_questions)?;
    save(&out.join("stage1-questions.edn"), &original_questions)?;
    save(&out.join("stage2-questions.edn"), &final_questions)?;
    let mut base_ids = BTreeSet::new();
    component_ids(&before_questions, &mut base_ids)?;
    if component_reads(&base, &base_ids)? != component_reads(&stage1, &base_ids)? {
        return Err("Committed stage 1 altered base field/answer definitions".into());
    }
    let mut original_ids = base_ids;
    component_ids(&original_questions, &mut original_ids)?;
    let original_components = component_reads(&stage1, &original_ids)?;
    save(&out.join("stage1-original-components.edn"), &original_components)?;
    save(&out.join("stage2-original-components.edn"), &component_reads(&final_db, &original_ids)?)?;
    let retired = validate_retirement(out, &base, &stage1, &stage2_receipt,
        &original_ids, &ids, stage1_basis)?;
    if original_ids.len() != 174 || retired.components.len() != 12 || retired.fields.len() != 2 {
        return Err(format!("Unexpected component counts: {} originals, {} retired, {} retired fields", original_ids.len(), retired.components.len(), retired.fields.len()).into());
    }
    save_history(out, "stage1", &base, &stage1_receipt)?;
    save_history(out, "stage2", &stage1, &stage2_receipt)?;
    let observed_after = Peer::connect_configured(&config, database, 128)?.db().basis_t();
    if observed_after != after { return Err(format!("Live basis advanced during audit: {after} -> {observed_after}").into()); }
    let manifest = EdnValue::Map(vec![
        (edn_keyword("audit", "verified"), EdnValue::Bool(true)),
        (edn_keyword("audit", "database"), EdnValue::String(database.clone())),
        (edn_keyword("audit", "durable-basis-before"), EdnValue::Long(before as i64)),
        (edn_keyword("audit", "durable-stage1-basis"), EdnValue::Long(stage1_basis as i64)),
        (edn_keyword("audit", "durable-basis-after"), EdnValue::Long(after as i64)),
        (edn_keyword("audit", "stage1-source"), EdnValue::Long(ma_source as i64)),
        (edn_keyword("audit", "stage2-source"), EdnValue::Long(repair_source as i64)),
        (edn_keyword("audit", "question-count"), EdnValue::Long(ids.len() as i64)),
        (edn_keyword("audit", "stage1-receipt-datoms-in-history"), EdnValue::Long(stage1_receipt.tx_data.len() as i64)),
        (edn_keyword("audit", "stage2-receipt-datoms-in-history"), EdnValue::Long(stage2_receipt.tx_data.len() as i64)),
        (edn_keyword("audit", "original-components-in-history"), EdnValue::Long(original_ids.len() as i64)),
        (edn_keyword("audit", "current-original-components-retained"), EdnValue::Long((original_ids.len() - retired.components.len()) as i64)),
        (edn_keyword("audit", "retired-components"), EdnValue::Long(retired.components.len() as i64)),
        (edn_keyword("audit", "retired-fields"), EdnValue::Long(retired.fields.len() as i64)),
        (edn_keyword("audit", "retired-question-count"), EdnValue::Long(retired.questions.len() as i64)),
        (edn_keyword("audit", "originals-recovered-from-final-history"), EdnValue::Bool(true)),
        (edn_keyword("audit", "database-writes"), EdnValue::Long(0)),
        (edn_keyword("audit", "committed-receipts-verified"), EdnValue::Bool(true)),
    ]);
    save(&out.join("manifest.edn"), &manifest)?;
    println!("Verified durable {before} -> {stage1_basis} -> {after}; 26 questions, 174 original components in history, 12 retired, 162 unchanged; both receipts matched final history; audit database writes: 0");
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("Read-only durable audit failed: {error}");
        std::process::exit(1);
    }
}
