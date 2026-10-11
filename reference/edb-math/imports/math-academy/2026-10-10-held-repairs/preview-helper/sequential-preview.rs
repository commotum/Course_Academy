//! Read-only, two-source speculative preview. This program has no durable-write API calls.
//! Usage: sequential-preview DATABASE EXPECTED_BASIS STAGE1.edn IDS.edn OUTDIR [STAGE2.edn]
//! IDS.edn is an EDN vector of exactly 26 Math Academy question IDs.

use edb_core::edn::{EdnValue, read_edn, write_edn};
use edb_core::edn_pull::{entity_identifier_from_edn, parse_pull_edn};
use edb_core::edn_value::{edn_keyword, edn_to_value, query_value_to_edn,
    transaction_report_to_edn, value_to_edn};
use edb_core::{DatabaseValue, EntityIdentifier, EntityRef, IndexPrefix, Keyword, Peer,
    PullControl, SpeculativeTransactionReport, Value, postgres_config_from_env};
use std::{collections::BTreeSet, error::Error, fs, path::Path, time::{SystemTime, UNIX_EPOCH}};

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
                       stage2: &SpeculativeTransactionReport,
                       original_ids: &BTreeSet<u64>, ids: &[String]) -> Result<Retirement> {
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
    let historical = stage2.db_after.clone().as_of(stage1.basis_t());
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

fn save_history(out: &Path, before: &DatabaseValue,
                report: &SpeculativeTransactionReport) -> Result<()> {
    let history = report.db_after.clone().history();
    let entities: BTreeSet<u64> = report.tx_data.iter().map(|d| d.entity).collect();
    let mut history_rows = Vec::new();
    for entity in entities {
        let prefix = IndexPrefix::Eavt { entity, attribute: None, value: None };
        let datoms = history.collect_datoms_with_prefix(&prefix)?;
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
    save(&out.join("stage2-changed-entity-history.edn"), &EdnValue::Vector(history_rows))
}

fn save_stage(out: &Path, label: &str, report: &SpeculativeTransactionReport,
              ids: &[String], source: u64) -> Result<()> {
    if report.tx_data.iter().any(|d| d.source != source) {
        return Err(format!("{label} produced a datom with the wrong source").into());
    }
    let mut receipt = transaction_report_to_edn(report.db_before.basis_t(),
        report.db_after.basis_t(), &report.tx_data, &report.tempids)?;
    let EdnValue::Map(fields) = &mut receipt else { unreachable!() };
    fields.push((edn_keyword("edb", "committed"), EdnValue::Bool(false)));
    fields.push((edn_keyword("edb", "speculative"), EdnValue::Bool(true)));
    save(&out.join(format!("{label}-preview.edn")), &receipt)?;
    save(&out.join(format!("{label}-questions.edn")), &question_reads(&report.db_after, ids, true)?)?;
    println!("{label}: speculative {} -> {}, {} datoms, source {source}",
        report.db_before.basis_t(), report.db_after.basis_t(), report.tx_data.len());
    Ok(())
}

fn run() -> Result<()> {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if !(args.len() == 5 || args.len() == 6) {
        return Err("Usage: sequential-preview DATABASE EXPECTED_BASIS STAGE1.edn IDS.edn OUTDIR [STAGE2.edn]".into());
    }
    let database = &args[0];
    let expected: u64 = args[1].parse()?;
    let stage1_text = bounded_read(Path::new(&args[2]))?;
    let ids_value = read_edn(&bounded_read(Path::new(&args[3]))?)?;
    let EdnValue::Vector(items) = ids_value else { return Err("IDS.edn must be a vector".into()) };
    let ids: Vec<String> = items.into_iter().map(|v| match v {
        EdnValue::String(id) if id.starts_with("q-") => Ok(id),
        _ => Err("IDS.edn must contain only q-N strings"),
    }).collect::<std::result::Result<_, _>>()?;
    if ids.len() != 26 || ids.iter().collect::<BTreeSet<_>>().len() != 26 {
        return Err("Expected exactly 26 distinct held question IDs".into());
    }
    let stage2_text = args.get(5).map(|path| bounded_read(Path::new(path))).transpose()?;
    // Parse before connecting. Neither this peer nor DatabaseValue speculation starts a writer.
    read_edn(&stage1_text)?;
    if let Some(text) = &stage2_text { read_edn(text)?; }
    let config = postgres_config_from_env()?;
    let db = Peer::connect_configured(&config, database, 128)?.db();
    if db.basis_t() != expected {
        return Err(format!("Stale preparation basis: expected {expected}, found {}", db.basis_t()).into());
    }
    let ma_source = source_id(&db, "org", "Math-Academy")?;
    let repair_source = source_id(&db, "agent", "gpt-6-astra-ultra")?;
    let out = Path::new(&args[4]);
    fs::create_dir_all(out)?;
    let before_questions = question_reads(&db, &ids, false)?;
    save(&out.join("before-questions.edn"), &before_questions)?;
    let mut base_component_ids = BTreeSet::new();
    component_ids(&before_questions, &mut base_component_ids)?;
    let base_components = component_reads(&db, &base_component_ids)?;
    save(&out.join("before-existing-components.edn"), &base_components)?;
    let instant = i64::try_from(SystemTime::now().duration_since(UNIX_EPOCH)?.as_millis())?;
    let stage1 = db.with_edn(&stage1_text, instant, EntityRef::from_edn(":org/Math-Academy")?)?;
    save_stage(out, "stage1", &stage1, &ids, ma_source)?;
    let base_after_stage1 = component_reads(&stage1.db_after, &base_component_ids)?;
    save(&out.join("stage1-existing-components.edn"), &base_after_stage1)?;
    if base_after_stage1 != base_components {
        return Err("Stage 1 changed a pre-existing field or answer entity".into());
    }
    let mut original_component_ids = base_component_ids;
    component_ids(&question_reads(&stage1.db_after, &ids, true)?, &mut original_component_ids)?;
    let original_components = component_reads(&stage1.db_after, &original_component_ids)?;
    save(&out.join("stage1-original-components.edn"), &original_components)?;
    let mut after = stage1.db_after.basis_t();
    let mut retired_components = 0;
    let mut retired_fields = 0;
    let mut retired_questions = 0;
    if let Some(text) = &stage2_text {
        let stage2 = stage1.db_after.with_edn(text, instant,
            EntityRef::from_edn(":agent/gpt-6-astra-ultra")?)?;
        save_stage(out, "stage2", &stage2, &ids, repair_source)?;
        save(&out.join("stage2-original-components.edn"),
            &component_reads(&stage2.db_after, &original_component_ids)?)?;
        let retiring = validate_retirement(out, &db, &stage1.db_after, &stage2,
            &original_component_ids, &ids)?;
        retired_components = retiring.components.len();
        retired_fields = retiring.fields.len();
        retired_questions = retiring.questions.len();
        save_history(out, &stage1.db_after, &stage2)?;
        after = stage2.db_after.basis_t();
    }
    // A fresh peer read distinguishes durable state from this in-memory branch.
    let live_after = Peer::connect_configured(&config, database, 128)?.db().basis_t();
    let manifest = EdnValue::Map(vec![
        (edn_keyword("preview", "database"), EdnValue::String(database.clone())),
        (edn_keyword("preview", "durable-basis-before"), EdnValue::Long(expected as i64)),
        (edn_keyword("preview", "durable-basis-after"), EdnValue::Long(live_after as i64)),
        (edn_keyword("preview", "speculative-basis-after"), EdnValue::Long(after as i64)),
        (edn_keyword("preview", "stage1-source"), EdnValue::Long(ma_source as i64)),
        (edn_keyword("preview", "stage2-source"), EdnValue::Long(repair_source as i64)),
        (edn_keyword("preview", "tx-instant-millis"), EdnValue::Long(instant)),
        (edn_keyword("preview", "question-count"), EdnValue::Long(ids.len() as i64)),
        (edn_keyword("preview", "original-components-in-history"), EdnValue::Long(original_component_ids.len() as i64)),
        (edn_keyword("preview", "current-original-components-retained"), EdnValue::Long((original_component_ids.len() - retired_components) as i64)),
        (edn_keyword("preview", "retired-components"), EdnValue::Long(retired_components as i64)),
        (edn_keyword("preview", "retired-fields"), EdnValue::Long(retired_fields as i64)),
        (edn_keyword("preview", "retired-question-count"), EdnValue::Long(retired_questions as i64)),
        (edn_keyword("preview", "database-writes"), EdnValue::Long(0)),
        (edn_keyword("edb", "committed"), EdnValue::Bool(false)),
        (edn_keyword("edb", "speculative"), EdnValue::Bool(true)),
    ]);
    save(&out.join("manifest.edn"), &manifest)?;
    if live_after != expected {
        return Err(format!("Concurrent durable change observed: {expected} -> {live_after}; replan before any future submission").into());
    }
    println!("Live basis unchanged at {live_after}; database writes: 0");
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("Read-only speculative preview failed: {error}");
        std::process::exit(1);
    }
}
