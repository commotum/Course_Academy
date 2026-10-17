//! Bounded, read-only content readiness; never starts a task or scans an attribute.
use course_academy_engine::{inventory, learning, schema::{self, EntitySnapshot, Record}};
use edb_core::{Cardinality, DatabaseValue, Datom, IndexPrefix, Keyword, Peer, Value, postgres_config_from_env};
use serde_json::{Value as Json, json};
use std::{collections::{BTreeMap, BTreeSet}, env, error::Error, fs};
type Result<T> = std::result::Result<T, Box<dyn Error>>;
type Records = BTreeMap<u64, Record>;

fn uuid(v: u128) -> String {
    let s = format!("{v:032x}");
    format!("{}-{}-{}-{}-{}", &s[..8], &s[8..12], &s[12..16], &s[16..20], &s[20..])
}
fn value(v: &Value) -> Result<Json> {
    Ok(match v {
        Value::String(v) | Value::Uri(v) => json!(v), Value::Long(v) => json!(v),
        Value::Double(v) => json!(v), Value::Float(v) => json!(v), Value::Bool(v) => json!(v),
        Value::Ref(v) => json!(v), Value::Keyword(v) => schema::keyword(&v.qualified_name()),
        Value::Uuid(v) => json!({"$uuid":uuid(*v)}), Value::Instant(v) => json!({"$instant":v}),
        _ => return Err("Unsupported domain value".into()),
    })
}
fn refs(records: &Records, e: u64, a: &str) -> Vec<u64> {
    match records.get(&e).and_then(|r| r.get(a)) {
        Some(Json::Array(v)) => v.iter().filter_map(Json::as_u64).collect(),
        Some(v) => v.as_u64().into_iter().collect(), None => vec![],
    }
}
fn ident(records: &Records, e: u64, a: &str) -> String {
    refs(records, e, a).first().and_then(|e| records.get(e))
        .and_then(|r| r.get("db/ident")).and_then(|v| v.get("$keyword"))
        .and_then(Json::as_str).unwrap_or("").to_owned()
}
struct Reader<'a> {
    db: &'a DatabaseValue,
    forward_reads: usize,
    reverse_reads: usize,
    datoms: usize,
    tokens: Records,
}
impl Reader<'_> {
    fn attr(&self, name: &str) -> Result<u32> {
        let (ns, n) = name.split_once('/').ok_or("invalid attribute")?;
        self.db.schema().resolve_ident(&Keyword::new(ns, n)).ok_or_else(|| format!("Missing {name}").into())
    }
    fn add(&self, records: &mut Records, d: Datom) -> Result<()> {
        let a = self.db.schema().attribute(d.attribute)?;
        let name = a.ident.qualified_name();
        let v = value(&d.value)?;
        if let Value::Ref(target) = d.value { records.entry(target).or_default(); }
        let row = records.entry(d.entity).or_default();
        if a.cardinality == Cardinality::Many {
            let items = row.entry(name).or_insert(json!([])).as_array_mut().unwrap();
            if !items.contains(&v) { items.push(v); }
        } else { row.insert(name, v); }
        Ok(())
    }
    fn entity(&mut self, records: &mut Records, e: u64) -> Result<()> {
        self.forward_reads += 1;
        records.entry(e).or_default();
        let rows = self.db.collect_datoms_with_prefix(&IndexPrefix::Eavt { entity: e, attribute: None, value: None })?;
        self.datoms += rows.len();
        for d in rows { self.add(records, d)?; }
        Ok(())
    }
    fn field(&mut self, records: &mut Records, e: u64, a: &str) -> Result<()> {
        self.forward_reads += 1;
        records.entry(e).or_default();
        let rows = self.db.collect_datoms_with_prefix(&IndexPrefix::Eavt { entity: e, attribute: Some(self.attr(a)?), value: None })?;
        self.datoms += rows.len();
        for d in rows { self.add(records, d)?; }
        Ok(())
    }
    fn owners(&mut self, records: &mut Records, target: u64, a: &str) -> Result<Vec<u64>> {
        self.reverse_reads += 1;
        let rows = self.db.collect_datoms_with_prefix(&IndexPrefix::Vaet { value: Value::Ref(target), attribute: Some(self.attr(a)?), entity: None })?;
        self.datoms += rows.len();
        let mut owners = BTreeSet::new();
        for d in rows { owners.insert(d.entity); self.add(records, d)?; }
        Ok(owners.into_iter().collect())
    }
    fn tokens(&mut self, records: &mut Records) -> Result<()> {
        let ids: BTreeSet<_> = records.values().flat_map(|r|
            ["activity/type", "learner-task/status", "answer/type", "answer-field/type", "question/difficulty"]
                .into_iter().filter_map(|a| r.get(a).and_then(Json::as_u64))).collect();
        for id in ids {
            if !self.tokens.contains_key(&id) {
                let mut token = Records::new(); self.field(&mut token, id, "db/ident")?;
                self.tokens.extend(token);
            }
            if let Some(row) = self.tokens.get(&id) { records.entry(id).or_default().extend(row.clone()); }
        }
        Ok(())
    }
    fn question(&mut self, records: &mut Records, q: u64) -> Result<()> {
        self.entity(records, q)?;
        for field in refs(records, q, "question/answer-fields") {
            self.entity(records, field)?;
            for answer in refs(records, field, "answer-field/choices") { self.entity(records, answer)?; }
        }
        Ok(())
    }
    fn question_context(&mut self, records: &mut Records, q: u64) -> Result<()> {
        self.owners(records, q, "knowledge-point/canonical-example")?;
        for kp in self.owners(records, q, "knowledge-point/questions")? {
            if !records[&kp].contains_key("knowledge-point/title") { self.field(records, kp, "knowledge-point/title")?; }
        }
        // Match schema::is_multistep_question exactly, including assignment wrappers.
        let mut pending = vec![q]; let mut visited = BTreeSet::new();
        while let Some(content) = pending.pop() {
            if !visited.insert(content) { continue; }
            for attr in ["step/content", "multistep-step/question"] {
                if attr == "multistep-step/question" && self.attr(attr).is_err() { continue; }
                for step in self.owners(records, content, attr)? { self.owners(records, step, "multistep/steps")?; }
            }
            pending.extend(self.owners(records, content, "assigned-problem/content")?);
        }
        Ok(())
    }
}

fn main() -> Result<()> {
    let args: Vec<_> = env::args().skip(1).collect();
    if args.len() != 2 { return Err("usage: readiness input.json output.json".into()); }
    let input: Json = serde_json::from_str(&fs::read_to_string(&args[0])?)?;
    let learner = input["learner"].as_u64().ok_or("learner missing")?;
    let topics: Vec<_> = input["topics"].as_array().ok_or("topics missing")?.iter()
        .map(|v| v.as_u64().ok_or("invalid topic")).collect::<std::result::Result<_, _>>()?;
    let current = Peer::connect_configured(&postgres_config_from_env()?, input["database"].as_str().ok_or("database missing")?, 512)?.db();
    let lineage = current.snapshot_reference()?.key().lineage_id().to_string();
    if input["lineage"].as_str() != Some(lineage.as_str()) { return Err("Database lineage changed".into()); }
    let basis = input["basis"].as_u64().ok_or("basis missing")?;
    if current.basis_t() < basis { return Err("Requested basis is ahead of captured database".into()); }
    let db = current.as_of(basis);
    let mut reader = Reader { db: &db, forward_reads: 0, reverse_reads: 0, datoms: 0, tokens: Records::new() };
    let mut history = Records::new();
    reader.field(&mut history, learner, "learner/activity")?;
    let tasks = refs(&history, learner, "learner/activity");
    let mut history_items = 0;
    for &task in &tasks {
        for field in ["learner-task/activity", "learner-task/status", "learner-task/items"] { reader.field(&mut history, task, field)?; }
        for item in refs(&history, task, "learner-task/items") {
            history_items += 1; reader.field(&mut history, item, "task-item/content")?;
        }
    }
    reader.tokens(&mut history)?;
    for &task in &tasks {
        if matches!(ident(&history, task, "learner-task/status").as_str(), "learner-task.status/started" | "learner-task.status/paused") {
            for activity in refs(&history, task, "learner-task/activity") {
                for field in ["activity/type", "activity/steps"] { reader.field(&mut history, activity, field)?; }
                for step in refs(&history, activity, "activity/steps") { reader.field(&mut history, step, "step/content")?; }
            }
        }
    }
    reader.tokens(&mut history)?;
    eprintln!("History captured once: {} tasks, {} items; basis {}", tasks.len(), history_items, basis);
    let mut output = vec![];
    let mut peak_entities = 0;
    for (index, &topic) in topics.iter().enumerate() {
        let mut records = history.clone();
        reader.entity(&mut records, topic)?;
        let kps = refs(&records, topic, "topic/knowledge-points");
        let mut questions = BTreeSet::new();
        for &kp in &kps {
            reader.entity(&mut records, kp)?;
            questions.extend(refs(&records, kp, "knowledge-point/questions"));
            questions.extend(refs(&records, kp, "knowledge-point/canonical-example"));
        }
        let scoped = reader.owners(&mut records, topic, "activity/scope")?;
        for &activity in &scoped { reader.field(&mut records, activity, "activity/type")?; }
        reader.tokens(&mut records)?;
        let lessons: Vec<_> = scoped.into_iter().filter(|a| ident(&records, *a, "activity/type") == "activity.type/lesson").collect();
        for &activity in &lessons {
            reader.entity(&mut records, activity)?;
            for step in refs(&records, activity, "activity/steps") {
                reader.entity(&mut records, step)?;
                for content in refs(&records, step, "step/content") {
                    reader.entity(&mut records, content)?;
                    if records[&content].contains_key("question/id") { questions.insert(content); }
                    if records[&content].contains_key("knowledge-point/id") {
                        questions.extend(refs(&records, content, "knowledge-point/questions"));
                        questions.extend(refs(&records, content, "knowledge-point/canonical-example"));
                    }
                }
            }
        }
        for &q in &questions { reader.question(&mut records, q)?; reader.question_context(&mut records, q)?; }
        reader.tokens(&mut records)?;
        peak_entities = peak_entities.max(records.len());
        let s = EntitySnapshot::new(records, basis)?;
        let seen = learning::unavailable_questions(&s, learner)?;
        let mut kp_rows = vec![];
        for &kp in &kps {
            let members = s.refs(kp, "knowledge-point/questions")?;
            let usable = inventory::practice_pool(&s, &[kp], &BTreeSet::new())?;
            let fresh = inventory::practice_pool(&s, &[kp], &seen)?;
            let mut invalid = BTreeMap::<String, usize>::new();
            for &q in &members {
                if let Err(error) = learning::validate_practice_question(&s, q) { *invalid.entry(error.to_string()).or_default() += 1; }
            }
            kp_rows.push(json!({"kp":kp,"title":s.entity(kp)?.get("knowledge-point/title"),"members":members.len(),"usable":usable.len(),"fresh":fresh.len(),"needed":5usize.saturating_sub(fresh.len()),"invalid_reasons":invalid}));
        }
        let mut errors = vec![];
        if lessons.len() != 1 { errors.push(format!("Expected one lesson activity; found {}", lessons.len())); }
        for &activity in &lessons {
            match learning::lesson_steps(&s, activity) {
                Err(error) => errors.push(format!("{activity}: {error}")),
                Ok(steps) => {
                    if !steps.iter().any(|v| v.kind == "knowledge-point" || v.kind == "question") { errors.push(format!("{activity}: no practice steps")); }
                    for step in steps.iter().filter(|v| v.kind == "question") {
                        if seen.contains(&step.content) { errors.push(format!("{activity}: authored question {} already seen or reserved", step.content)); }
                        if let Err(error) = learning::validate_practice_question(&s, step.content) { errors.push(format!("{activity}: authored question {}: {error}", step.content)); }
                    }
                }
            }
        }
        let saved: Vec<_> = tasks.iter().filter_map(|task| {
            let activity = s.optional_ref(*task, "learner-task/activity").ok().flatten()?;
            if !lessons.contains(&activity) { return None; }
            let status = s.ident(&json!(s.reference(*task, "learner-task/status").ok()?)).ok()?;
            matches!(status.as_str(), "learner-task.status/completed" | "learner-task.status/started" | "learner-task.status/paused")
                .then(|| json!({"task":task,"activity":activity,"status":status.rsplit('/').next()}))
        }).collect();
        let bank_ready = inventory::lesson_ready(&s, &kps, &seen)?;
        let ready = bank_ready && errors.is_empty();
        let row = json!({"topic":topic,"title":s.entity(topic)?.get("topic/title"),"content_ready_for_fresh_lesson":ready,"question_bank_ready":bank_ready,"lesson_count":lessons.len(),"lesson_errors":errors,"knowledge_points":kp_rows,"saved_attempts":saved});
        eprintln!("{}/{} topic {}: {}", index+1, topics.len(), topic, if ready {"content ready"} else {"content blocked"});
        output.push(row);
    }
    let blocked = output.iter().filter(|r| r["content_ready_for_fresh_lesson"] == false).count();
    let result = json!({"basis":basis,"lineage":lineage,"database":input["database"],"learner":learner,"topics":output,"summary":{"topics":topics.len(),"content_ready":topics.len()-blocked,"content_blocked":blocked},"read_scope":{"global_attribute_scans":0,"entity_prefix_reads":reader.forward_reads,"exact_reverse_prefix_reads":reader.reverse_reads,"datoms_returned":reader.datoms,"own_learner_tasks":tasks.len(),"own_history_items":history_items,"max_projection_entities":peak_entities},"scope_note":"Fresh-lesson content and question-supply check. Explicit topic study bypasses prerequisite/mastery gates. Saved attempts are reported separately; lifecycle/remediation and runtime transitions were not simulated.","database_writes":0,"learner_attempts_created":0});
    fs::write(&args[1], serde_json::to_string_pretty(&result)? + "\n")?;
    println!("{}", serde_json::to_string(&result["summary"])?);
    Ok(())
}
