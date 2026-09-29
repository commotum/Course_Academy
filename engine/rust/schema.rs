//! Captured EDB entities and guarded atomic completion transactions.
//! The caller submits the returned EDN with its request key and exact basis guard.
use crate::{
    Result,
    calibration::AccuracyEstimate,
    core::{Edge, EncompassingGraph, FireEngine, Policy, TopicState},
    timing,
};
use chrono::{DateTime, SecondsFormat, Timelike, Utc};
use serde::{Deserialize, Serialize};
use serde_json::{Map, Value, json};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};

pub type Record = Map<String, Value>;
pub fn keyword(value: &str) -> Value {
    json!({"$keyword": value.trim_start_matches(':')})
}
pub fn instant_value(value: DateTime<Utc>) -> Value {
    json!({"$instant": value.to_rfc3339_opts(SecondsFormat::Millis, true)})
}
fn keyword_text(value: &str) -> Result<String> {
    let v = value.strip_prefix(':').unwrap_or(value);
    if v.is_empty()
        || v.chars()
            .any(|c| c.is_whitespace() || "[]{}()\";,".contains(c))
    {
        return Err("invalid EDN keyword".into());
    }
    Ok(v.into())
}
pub fn parse_instant(value: &Value) -> Result<DateTime<Utc>> {
    let v = value.get("$instant").unwrap_or(value);
    let date = if let Some(ms) = v.as_i64() {
        DateTime::from_timestamp_millis(ms).ok_or("instant outside supported range")?
    } else if let Some(s) = v.as_str() {
        DateTime::parse_from_rfc3339(s)
            .map_err(|e| format!("instant requires explicit timezone: {e}"))?
            .with_timezone(&Utc)
    } else {
        return Err("instant requires ISO text or integer epoch milliseconds".into());
    };
    date.with_nanosecond(date.nanosecond() / 1_000_000 * 1_000_000)
        .ok_or("invalid instant".into())
}
pub fn instant_days(value: &Value) -> Result<f64> {
    Ok(timestamp_days(parse_instant(value)?))
}
/// Use the same seconds-to-days conversion on hydration and completion, so an
/// identical millisecond timestamp cannot become older through f64 rounding.
pub fn timestamp_days(at: DateTime<Utc>) -> f64 {
    (at.timestamp_millis() as f64 / 1000.0) / 86400.0
}
fn day_instant(day: f64) -> Result<Value> {
    if !day.is_finite() {
        return Err("engine timestamp must be finite".into());
    }
    let ms = (day * 86_400_000.).round_ties_even();
    if ms < i64::MIN as f64 || ms >= i64::MAX as f64 {
        return Err("engine timestamp out of range".into());
    }
    Ok(instant_value(
        DateTime::from_timestamp_millis(ms as i64).ok_or("engine timestamp out of range")?,
    ))
}
pub fn value_id_string(value: &Value) -> Result<String> {
    value
        .get("$uuid")
        .unwrap_or(value)
        .as_str()
        .map(str::to_owned)
        .ok_or("identity requires text".into())
}
fn uuid(record: &Record, attr: &str) -> Result<String> {
    uuid::Uuid::parse_str(&value_id_string(
        record.get(attr).ok_or_else(|| format!("missing {attr}"))?,
    )?)
    .map(|u| u.to_string())
    .map_err(|_| format!("{attr} requires UUID"))
}
fn number(v: &Value, label: &str, low: Option<f64>, high: Option<f64>) -> Result<f64> {
    let n = v
        .as_f64()
        .filter(|x| x.is_finite())
        .ok_or_else(|| format!("{label} must be finite numeric data"))?;
    if low.is_some_and(|x| n < x) || high.is_some_and(|x| n > x) {
        return Err(format!("{label} outside allowed range"));
    }
    Ok(n)
}
fn normalize(record: &Record) -> Result<Record> {
    let mut out = Record::new();
    for (key, v) in record {
        if out
            .insert(key.trim_start_matches(':').into(), v.clone())
            .is_some()
        {
            return Err("duplicate normalized attribute".into());
        }
    }
    Ok(out)
}

#[derive(Clone, Debug)]
pub struct EntitySnapshot {
    pub entities: BTreeMap<u64, Record>,
    pub basis_t: u64,
    pub status_history: Vec<StatusAssertion>,
    idents: BTreeMap<String, u64>,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct StatusAssertion {
    pub entity: u64,
    pub attribute: String,
    pub value: Value,
    pub t: u64,
    pub at: Value,
}
impl EntitySnapshot {
    pub fn from_json_str(data: &str) -> Result<Self> {
        Self::from_json(&serde_json::from_str(data).map_err(|e| e.to_string())?)
    }
    pub fn new(entities: BTreeMap<u64, Record>, basis_t: u64) -> Result<Self> {
        let mut records = BTreeMap::new();
        let mut idents = BTreeMap::new();
        for (eid, raw) in entities {
            let record = normalize(&raw)?;
            if let Some(v) = record.get("db/ident") {
                let ident = keyword_text(
                    v.as_str()
                        .or_else(|| v.get("$keyword").and_then(Value::as_str))
                        .ok_or("invalid ident")?,
                )?;
                if idents.insert(ident, eid).is_some() {
                    return Err("duplicate ident".into());
                }
            }
            records.insert(eid, record);
        }
        Ok(Self {
            entities: records,
            basis_t,
            status_history: vec![],
            idents,
        })
    }
    pub fn from_json(value: &Value) -> Result<Self> {
        let basis = value["basis_t"].as_u64().ok_or("basis_t required")?;
        let records = value["entities"]
            .as_object()
            .ok_or("entities required")?
            .iter()
            .map(|(k, v)| {
                Ok((
                    k.parse::<u64>().map_err(|_| "numeric EID required")?,
                    v.as_object().ok_or("entity must be map")?.clone(),
                ))
            })
            .collect::<Result<_>>()?;
        let mut snapshot = Self::new(records, basis)?;
        snapshot.status_history =
            serde_json::from_value(value.get("status_history").cloned().unwrap_or(json!([])))
                .map_err(|e| e.to_string())?;
        crate::timing::validate_history(&mut snapshot)?;
        Ok(snapshot)
    }
    pub fn eid(&self, v: &Value) -> Result<u64> {
        let v = v.get("$keyword").unwrap_or(v);
        let id = if let Some(s) = v.as_str() {
            self.idents.get(&keyword_text(s)?).copied()
        } else {
            v.as_u64()
        };
        id.filter(|e| self.entities.contains_key(e))
            .ok_or_else(|| format!("unresolved entity reference {v}"))
    }
    pub fn entity(&self, eid: u64) -> Result<&Record> {
        self.entities
            .get(&eid)
            .ok_or_else(|| format!("unresolved entity {eid}"))
    }
    pub fn ident(&self, v: &Value) -> Result<String> {
        let record = self.entity(self.eid(v)?)?;
        let ident = record
            .get("db/ident")
            .ok_or("entity is not an enum ident")?;
        keyword_text(
            ident
                .as_str()
                .or_else(|| ident.get("$keyword").and_then(Value::as_str))
                .ok_or("invalid ident")?,
        )
    }
    pub fn reference(&self, eid: u64, attr: &str) -> Result<u64> {
        self.eid(
            self.entity(eid)?
                .get(attr.trim_start_matches(':'))
                .ok_or_else(|| format!("missing {attr}"))?,
        )
    }
    pub fn optional_ref(&self, eid: u64, attr: &str) -> Result<Option<u64>> {
        self.entity(eid)?
            .get(attr.trim_start_matches(':'))
            .filter(|x| !x.is_null())
            .map(|x| self.eid(x))
            .transpose()
    }
    pub fn refs(&self, eid: u64, attr: &str) -> Result<Vec<u64>> {
        match self.entity(eid)?.get(attr.trim_start_matches(':')) {
            None => Ok(vec![]),
            Some(v) => Ok(v
                .as_array()
                .ok_or_else(|| format!("{attr} must be a collection"))?
                .iter()
                .map(|x| self.eid(x))
                .collect::<Result<BTreeSet<_>>>()?
                .into_iter()
                .collect()),
        }
    }
    pub fn owners(&self, target: u64, attr: &str) -> Result<Vec<u64>> {
        self.entity(target)?;
        let mut owners = vec![];
        for (&id, record) in &self.entities {
            if let Some(v) = record.get(attr) {
                let ids = if v.is_array() {
                    self.refs(id, attr)?
                } else {
                    vec![self.eid(v)?]
                };
                if ids.contains(&target) {
                    owners.push(id);
                }
            }
        }
        Ok(owners)
    }
    pub fn types(&self, eid: u64) -> Result<BTreeSet<String>> {
        Ok(self
            .entity(eid)?
            .keys()
            .filter(|k| k.ends_with("/id") && k.as_str() != "db/id")
            .map(|k| k[..k.len() - 3].to_owned())
            .collect())
    }
    pub fn knowledge_points_for_question(&self, q: u64) -> Result<Vec<u64>> {
        if !self.types(q)?.contains("question") {
            return Err("content is not a question".into());
        }
        let owners = self.owners(q, "knowledge-point/questions")?;
        if owners.len() != 1 || !self.types(owners[0])?.contains("knowledge-point") {
            return Err("question needs exactly one knowledge-point bank".into());
        }
        Ok(owners)
    }
    pub fn topic_for_question(&self, q: u64) -> Result<u64> {
        let mut topics = BTreeSet::new();
        for kp in self.knowledge_points_for_question(q)? {
            let parents = self.owners(kp, "topic/knowledge-points")?;
            if parents.is_empty() {
                return Err("knowledge point needs a topic".into());
            }
            for p in parents {
                if !self.types(p)?.contains("topic") {
                    return Err("knowledge point needs a topic".into());
                }
                topics.insert(p);
            }
        }
        if topics.len() != 1 {
            return Err("question must resolve to exactly one topic".into());
        }
        Ok(*topics.first().unwrap())
    }
    pub fn item_task(&self, item: u64, learner: u64) -> Result<u64> {
        if !self.types(item)?.contains("task-item") {
            return Err("completion target is not task item".into());
        }
        let owners = self.owners(item, "learner-task/items")?;
        if owners.len() != 1 || !self.types(owners[0])?.contains("learner-task") {
            return Err("item must have exactly one task owner".into());
        }
        if self.owners(owners[0], "learner/activity")? != vec![learner] {
            return Err("task must belong exclusively to this learner".into());
        }
        Ok(owners[0])
    }
}

const POLICY_FIELDS: [(&str, &str); 16] = [
    ("base-half-life-days", "base_interval_days"),
    ("interval-growth", "interval_growth"),
    ("maximum-half-life-days", "maximum_interval_days"),
    ("review-threshold", "due_threshold"),
    ("initial-retention", "restored_memory"),
    ("early-practice-discount-power", "discount_power"),
    ("initial-accuracy", "prior_accuracy"),
    ("accuracy-update-rate", "accuracy_alpha"),
    ("speed-exponent", "speed_exponent"),
    ("minimum-speed", "minimum_speed"),
    ("maximum-speed", "maximum_speed"),
    ("overdue-failure-slope", "failure_overdue_slope"),
    ("maximum-failure-multiplier", "maximum_failure_multiplier"),
    ("gate-slow-implicit", "gate_slow_implicit"),
    ("retention-update-order", "memory_order"),
    ("future-horizon-days", "future_horizon_days"),
];
const ABILITY_FIELDS: [&str; 4] = [
    "assessment_accuracy",
    "practice_accuracy",
    "assessment_mass",
    "practice_mass",
];
fn ability(record: &Record, prefix: &str) -> Result<AccuracyEstimate> {
    let fields: Record = ABILITY_FIELDS
        .iter()
        .map(|f| {
            Ok((
                f.to_string(),
                record
                    .get(&format!("{prefix}/{}", f.replace('_', "-")))
                    .ok_or_else(|| format!("incomplete {prefix} accuracy state"))?
                    .clone(),
            ))
        })
        .collect::<Result<_>>()?;
    let a: AccuracyEstimate =
        serde_json::from_value(Value::Object(fields)).map_err(|e| e.to_string())?;
    a.validate()?;
    Ok(a)
}
#[derive(Clone, Debug)]
pub struct LoadedRuntime {
    pub snapshot: EntitySnapshot,
    pub engine: FireEngine,
    pub learner_eid: u64,
    pub learner: String,
    pub policy_eid: u64,
    pub topic_eid_to_id: BTreeMap<u64, String>,
    pub topic_id_to_eid: BTreeMap<String, u64>,
    pub progress_by_topic: BTreeMap<String, u64>,
    pub performance_eid: Option<u64>,
}
pub fn load_runtime(
    snapshot: EntitySnapshot,
    learner_eid: u64,
    policy_eid: u64,
) -> Result<LoadedRuntime> {
    let learner = snapshot
        .entity(learner_eid)?
        .get("learner/id")
        .and_then(Value::as_str)
        .filter(|s| !s.is_empty())
        .ok_or("learner/id must be nonempty string")?
        .to_owned();
    let record = snapshot.entity(policy_eid)?;
    uuid(record, "policy/id")?;
    let mut settings: Record = POLICY_FIELDS
        .iter()
        .map(|(a, f)| {
            Ok((
                f.to_string(),
                record
                    .get(&format!("policy/{a}"))
                    .ok_or_else(|| format!("incomplete persisted policy: {a}"))?
                    .clone(),
            ))
        })
        .collect::<Result<_>>()?;
    let order = snapshot.ident(&settings["memory_order"])?;
    settings.insert(
        "memory_order".into(),
        json!(match order.as_str() {
            "policy.retention-update/decay-before-add" => "decay-before-add",
            "policy.retention-update/add-before-decay" => "literal-add-before-decay",
            _ => return Err("unsupported retention update order".into()),
        }),
    );
    let policy: Policy =
        serde_json::from_value(Value::Object(settings)).map_err(|e| e.to_string())?;
    policy.validate()?;
    let topic_eid_to_id: BTreeMap<u64, String> = snapshot
        .entities
        .iter()
        .filter(|(_, r)| r.contains_key("topic/id"))
        .map(|(e, r)| Ok((*e, uuid(r, "topic/id")?)))
        .collect::<Result<_>>()?;
    let topic_id_to_eid: BTreeMap<String, u64> = topic_eid_to_id
        .iter()
        .map(|(e, id)| (id.clone(), *e))
        .collect();
    if topic_id_to_eid.len() != topic_eid_to_id.len() {
        return Err("duplicate topic UUID".into());
    }
    let mut edges = vec![];
    let mut difficulty = BTreeMap::new();
    let mut neighborhoods = BTreeMap::new();
    for (&eid, id) in &topic_eid_to_id {
        if snapshot
            .refs(eid, "topic/next")?
            .iter()
            .any(|next| !topic_eid_to_id.contains_key(next))
        {
            return Err("topic/next must reference known topics".into());
        }
        if let Some(d) = snapshot.entity(eid)?.get("topic/difficulty") {
            difficulty.insert(
                id.clone(),
                number(d, "topic difficulty", Some(0.), Some(1.))?,
            );
        }
        for e in snapshot.refs(eid, "topic/encompasses")? {
            if snapshot.owners(e, "topic/encompasses")? != vec![eid] {
                return Err("encompassing record must have one source topic".into());
            }
            let target = snapshot.reference(e, "encompassing/topic")?;
            edges.push(Edge {
                advanced: id.clone(),
                component: topic_eid_to_id
                    .get(&target)
                    .ok_or("encompassing target must be topic")?
                    .clone(),
                weight: number(
                    snapshot
                        .entity(e)?
                        .get("encompassing/weight")
                        .unwrap_or(&Value::Null),
                    "coverage",
                    Some(0.),
                    Some(1.),
                )?,
            });
        }
        let mut neighbors: BTreeSet<_> = snapshot
            // topic/next points from each prerequisite to its direct dependents.
            .owners(eid, "topic/next")?
            .into_iter()
            .collect();
        for kp in snapshot.refs(eid, "topic/knowledge-points")? {
            if !snapshot.types(kp)?.contains("knowledge-point") {
                return Err("topic knowledge-points must reference knowledge points".into());
            }
            neighbors.extend(snapshot.refs(kp, "knowledge-point/key-prerequisites")?);
        }
        for m in snapshot.owners(eid, "module/topics")? {
            if !snapshot.types(m)?.contains("module") {
                return Err("topic module owner must be module".into());
            }
            neighbors.extend(snapshot.refs(m, "module/topics")?);
        }
        if neighbors.iter().any(|n| !topic_eid_to_id.contains_key(n)) {
            return Err("curriculum neighbors must reference known topics".into());
        }
        neighbors.remove(&eid);
        if !neighbors.is_empty() {
            neighborhoods.insert(
                id.clone(),
                neighbors
                    .iter()
                    .map(|n| topic_eid_to_id[n].clone())
                    .collect(),
            );
        }
    }
    let mut engine = FireEngine::new(
        EncompassingGraph::new(edges, topic_id_to_eid.keys().cloned().collect())?,
        policy,
        difficulty,
        neighborhoods,
    )?;
    let performance_eid = snapshot.optional_ref(learner_eid, "learner/performance")?;
    if let Some(p) = performance_eid {
        if snapshot.owners(p, "learner/performance")? != vec![learner_eid] {
            return Err("global performance needs one learner owner".into());
        }
        engine.global_ability.insert(
            learner.clone(),
            ability(snapshot.entity(p)?, "performance")?,
        );
    }
    let mut progress_by_topic = BTreeMap::new();
    for p in snapshot.refs(learner_eid, "learner/knowledge-profile")? {
        if snapshot.owners(p, "learner/knowledge-profile")? != vec![learner_eid] {
            return Err("progress needs one learner owner".into());
        }
        let state = snapshot.entity(p)?;
        if state
            .get("progress/id")
            .and_then(Value::as_str)
            .is_none_or(str::is_empty)
        {
            return Err("progress needs stable string identity".into());
        }
        let topic = snapshot.reference(p, "progress/topic")?;
        let id = topic_eid_to_id
            .get(&topic)
            .ok_or("progress needs known topic")?;
        if progress_by_topic.insert(id.clone(), p).is_some() {
            return Err("one progress record per topic required".into());
        }
        uuid(
            snapshot.entity(snapshot.reference(p, "progress/policy")?)?,
            "policy/id",
        )?;
        let mut fields = Record::new();
        for (a, f) in [
            ("repetitions", "repetitions"),
            ("memory", "memory"),
            ("interval-days", "interval_days"),
            ("learned", "learned"),
        ] {
            fields.insert(
                f.into(),
                state
                    .get(&format!("progress/{a}"))
                    .ok_or("incomplete progress state")?
                    .clone(),
            );
        }
        fields.insert(
            "memory_at".into(),
            json!(instant_days(
                state.get("progress/memory-at").ok_or("missing memory-at")?
            )?),
        );
        fields.insert(
            "ability".into(),
            serde_json::to_value(ability(state, "progress")?).map_err(|e| e.to_string())?,
        );
        if let Some(v) = state.get("progress/last-direct-at") {
            fields.insert("last_direct_at".into(), json!(instant_days(v)?));
        }
        let s: TopicState =
            serde_json::from_value(Value::Object(fields)).map_err(|e| e.to_string())?;
        engine.seed(&learner, id, s)?;
    }
    for task in snapshot.refs(learner_eid, "learner/activity")? {
        if snapshot.owners(task, "learner/activity")? != vec![learner_eid] {
            return Err("learner task has multiple associations".into());
        }
        let members = snapshot.refs(task, "learner-task/items")?;
        let times = snapshot
            .status_history
            .iter()
            .filter(|h| h.entity == task || members.contains(&h.entity))
            .map(|h| instant_days(&h.at))
            .collect::<Result<Vec<_>>>()?;
        for at in times {
            let old = engine
                .latest
                .entry(learner.clone())
                .or_insert(f64::NEG_INFINITY);
            *old = old.max(at);
        }
    }
    Ok(LoadedRuntime {
        snapshot,
        engine,
        learner_eid,
        learner,
        policy_eid,
        topic_eid_to_id,
        topic_id_to_eid,
        progress_by_topic,
        performance_eid,
    })
}

/// EDN keywords/UUIDs/instants use explicit tagged JSON objects at this boundary.
pub fn edn(value: &Value) -> Result<String> {
    Ok(match value {
        Value::Null => "nil".into(),
        Value::Bool(b) => b.to_string(),
        Value::Number(n) => n.to_string(),
        Value::String(s) => serde_json::to_string(s).map_err(|e| e.to_string())?,
        Value::Array(v) => format!(
            "[{}]",
            v.iter().map(edn).collect::<Result<Vec<_>>>()?.join(" ")
        ),
        Value::Object(m) => {
            if m.len() == 1 && m.contains_key("$keyword") {
                format!(
                    ":{}",
                    keyword_text(m["$keyword"].as_str().ok_or("invalid keyword")?)?
                )
            } else if m.len() == 1 && m.contains_key("$instant") {
                format!(
                    "#inst {}",
                    serde_json::to_string(
                        &parse_instant(value)?.to_rfc3339_opts(SecondsFormat::Millis, true)
                    )
                    .map_err(|e| e.to_string())?
                )
            } else if m.len() == 1 && m.contains_key("$uuid") {
                let u = uuid::Uuid::parse_str(m["$uuid"].as_str().ok_or("invalid UUID")?)
                    .map_err(|e| e.to_string())?;
                format!("#uuid \"{u}\"")
            } else {
                format!(
                    "{{{}}}",
                    m.iter()
                        .map(|(k, v)| Ok(format!(":{} {}", keyword_text(k)?, edn(v)?)))
                        .collect::<Result<Vec<_>>>()?
                        .join(" ")
                )
            }
        }
    })
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct TransactionPlan {
    pub request_key: String,
    pub compare_basis_t: u64,
    pub edn: String,
    pub forms: Vec<Value>,
}
fn check_task(
    loaded: &LoadedRuntime,
    task: u64,
    at: DateTime<Utc>,
    allow_paused: bool,
) -> Result<()> {
    let s = &loaded.snapshot;
    if s.owners(task, "learner/activity")? != vec![loaded.learner_eid] {
        return Err("task must belong exclusively to learner".into());
    }
    let status = s.ident(&json!(s.reference(task, "learner-task/status")?))?;
    if status != "learner-task.status/started"
        && !(allow_paused && status == "learner-task.status/paused")
    {
        return Err("only a started task can accept completion".into());
    }
    timing::active_item(s, loaded.learner_eid)?;
    if at < timing::status_at(s, task, "learner-task/status")? {
        return Err("timing update predates task status".into());
    }
    if timestamp_days(at)
        < *loaded
            .engine
            .latest
            .get(&loaded.learner)
            .unwrap_or(&f64::NEG_INFINITY)
    {
        return Err("completion predates learner evidence".into());
    }
    if at < timing::task_started(s, task)? {
        return Err("completion predates task start".into());
    }
    Ok(())
}

fn task_change(s: &EntitySnapshot, raw: &Value, task: u64, at: DateTime<Utc>) -> Result<Record> {
    let mut change = normalize(raw.as_object().ok_or("change must be map")?)?;
    let allowed = [
        "db/id",
        "learner-task/status",
        "learner-task/xp-earned",
        "learner-task/xp-base",
    ];
    if change.get("db/id").and_then(Value::as_u64) != Some(task)
        || change.keys().any(|k| !allowed.contains(&k.as_str()))
    {
        return Err("task change has unsupported target/attribute".into());
    }
    if let Some(v) = change.get("learner-task/status") {
        let ident = s.ident(v)?;
        if ![
            "locked",
            "unlocked",
            "started",
            "paused",
            "completed",
            "failed",
        ]
        .iter()
        .any(|status| ident == format!("learner-task.status/{status}"))
        {
            return Err("invalid learner-task/status".into());
        }
    }
    let elapsed = timing::task_elapsed(s, task, at)?;
    change.insert("learner-task/elapsed-seconds".into(), json!(elapsed));
    for k in ["learner-task/xp-earned", "learner-task/xp-base"] {
        if change.get(k).is_some_and(|v| v.as_i64().is_none()) {
            return Err(format!("{k} must be integer"));
        }
    }
    change.insert("db/ensure".into(), keyword("learner-task/validate"));
    Ok(change)
}
fn check_responses(
    s: &EntitySnapshot,
    item: u64,
    additions: &[Value],
    new: &BTreeMap<String, Record>,
) -> Result<()> {
    let mut responses: Vec<Value> = s
        .refs(item, "task-item/responses")?
        .into_iter()
        .map(Value::from)
        .collect();
    responses.extend_from_slice(additions);
    if responses.is_empty() && new.is_empty() {
        return Ok(());
    }
    let q = s.reference(item, "task-item/content")?;
    if !s.types(q)?.contains("question") {
        return Err("only question items carry responses".into());
    }
    let fields = s.refs(q, "question/answer-fields")?;
    let mut seen = BTreeSet::new();
    let mut used = BTreeSet::new();
    for response in responses {
        let field =
            if let Some((temp, r)) = response.as_str().and_then(|x| new.get(x).map(|r| (x, r))) {
                used.insert(temp.to_owned());
                let field = s.eid(&r["learner-response/field"])?;
                if !s.refs(field, "answer-field/answer-choices")?.is_empty() {
                    return Err("selection fields require canonical choice".into());
                }
                field
            } else {
                let id = s.eid(&response)?;
                let r = s.entity(id)?;
                if r.contains_key("learner-response/field") {
                    let field = s.reference(id, "learner-response/field")?;
                    if !s.refs(field, "answer-field/answer-choices")?.is_empty() {
                        return Err("selection fields require canonical choice".into());
                    }
                    field
                } else {
                    let mut owners = vec![];
                    for &f in &fields {
                        if s.refs(f, "answer-field/answer-choices")?.contains(&id) {
                            owners.push(f);
                        }
                    }
                    if owners.len() != 1 || !s.types(id)?.contains("answer") {
                        return Err("selected answer must belong to one field".into());
                    }
                    owners[0]
                }
            };
        if !fields.contains(&field) || !seen.insert(field) {
            return Err("response field outside question or answered twice".into());
        }
    }
    if used != new.keys().cloned().collect() {
        return Err("new entered responses must attach to this item".into());
    }
    Ok(())
}
pub fn completion_transaction(
    loaded: &LoadedRuntime,
    item: u64,
    at: DateTime<Utc>,
    changes: Vec<Value>,
    engine: &FireEngine,
) -> Result<TransactionPlan> {
    let at = parse_instant(&instant_value(at))?;
    let s = &loaded.snapshot;
    let task = s.item_task(item, loaded.learner_eid)?;
    let old_status = s.reference(item, "task-item/status")?;
    if s.ident(&json!(old_status))? != "task-item.status/started" {
        return Err("only a started item can complete".into());
    }
    check_task(loaded, task, at, false)?;
    let elapsed = timing::elapsed(s, item, at)?;
    let terminal = changes
        .iter()
        .find(|c| c.get("db/id").and_then(Value::as_u64) == Some(item))
        .and_then(|c| c.get("task-item/status"))
        .ok_or("completion requires terminal item status")?;
    let terminal_name = s.ident(terminal)?;
    if !timing::terminal(&terminal_name) {
        return Err("completion requires terminal item status".into());
    }
    let content = s.reference(item, "task-item/content")?;
    if s.types(content)?.contains("question") == (terminal_name == "task-item.status/completed") {
        return Err("item terminal status does not match its content".into());
    }
    let mut forms = vec![json!([
        keyword("db/cas"),
        item,
        keyword("task-item/status"),
        old_status,
        terminal
    ])];
    let mut targets = BTreeSet::new();
    let mut responses = vec![];
    let mut new = BTreeMap::new();
    for raw in changes {
        let mut change = normalize(raw.as_object().ok_or("change must be map")?)?;
        let target = change.get("db/id").ok_or("change needs db/id")?.clone();
        if (!target.is_u64() && !target.is_string()) || !targets.insert(target.to_string()) {
            return Err("distinct EID/tempid change targets required".into());
        }
        if target.as_u64() == Some(item) {
            let allowed = [
                "db/id",
                "task-item/status",
                "task-item/responses",
                "task-item/performance",
            ];
            if change.keys().any(|k| !allowed.contains(&k.as_str())) {
                return Err("unsupported item attribute".into());
            }
            change.remove("task-item/status");
            change.insert("task-item/elapsed-seconds".into(), json!(elapsed));
            if terminal_name == "task-item.status/skipped"
                && (change
                    .get("task-item/responses")
                    .and_then(Value::as_array)
                    .is_some_and(|v| !v.is_empty())
                    || !s.refs(item, "task-item/responses")?.is_empty())
            {
                return Err("a skipped question cannot contain submitted responses".into());
            }
            for attr in ["task-item/elapsed-seconds", "task-item/performance"] {
                if let Some(v) = change.get(attr) {
                    let n = number(v, attr, Some(0.), None)?;
                    if attr == "task-item/performance" && n == 0. {
                        return Err("performance must be positive".into());
                    }
                    change.insert(attr.into(), json!(n));
                }
            }
            if let Some(v) = change.get("task-item/responses") {
                responses.extend_from_slice(v.as_array().ok_or("responses must be collection")?);
            }
            change.insert("db/ensure".into(), keyword("task-item/validate"));
        } else if target.as_u64() == Some(task) {
            change = task_change(s, &Value::Object(change), task, at)?;
        } else if let Some(t) = target.as_str().filter(|t| {
            !t.is_empty() && !t.starts_with(':') && !t.starts_with("engine-") && *t != "edb.tx"
        }) {
            if change.keys().map(String::as_str).collect::<BTreeSet<_>>()
                != ["db/id", "learner-response/field", "learner-response/value"]
                    .into_iter()
                    .collect()
            {
                return Err("response requires tempid, field, value".into());
            }
            if !change["learner-response/value"].is_string() {
                return Err("entered response must be text".into());
            }
            let f = s.eid(&change["learner-response/field"])?;
            change.insert("learner-response/field".into(), json!(f));
            new.insert(t.to_owned(), change.clone());
            change.insert("db/ensure".into(), keyword("learner-response/validate"));
        } else {
            return Err("changes may target item, its task, or new response".into());
        }
        forms.push(Value::Object(change));
    }
    check_responses(s, item, &responses, &new)?;
    if !targets.contains(&task.to_string()) {
        forms.push(Value::Object(task_change(
            s,
            &json!({"db/id":task}),
            task,
            at,
        )?));
    }
    forms.push(json!({"db/id":item,"db/ensure":keyword("task-item/validate")}));
    writeback(
        loaded,
        engine,
        forms,
        "complete-item",
        &uuid(s.entity(item)?, "task-item/id")?,
        at,
    )
}
pub fn task_transaction(
    loaded: &LoadedRuntime,
    task: u64,
    at: DateTime<Utc>,
    changes: Vec<Value>,
    engine: &FireEngine,
) -> Result<TransactionPlan> {
    let at = parse_instant(&instant_value(at))?;
    let s = &loaded.snapshot;
    check_task(loaded, task, at, true)?;
    let status = s.reference(task, "learner-task/status")?;
    if changes.len() > 1 {
        return Err("expiry accepts one task change".into());
    }
    let mut change = task_change(
        s,
        changes.first().unwrap_or(&json!({"db/id":task})),
        task,
        at,
    )?;
    if let Some(v) = change.get("learner-task/status")
        && s.ident(v)? != "learner-task.status/completed"
    {
        return Err("expiry must complete task".into());
    }
    change.remove("learner-task/status");
    let mut forms = vec![
        json!([
            keyword("db/cas"),
            task,
            keyword("learner-task/status"),
            status,
            keyword("learner-task.status/completed")
        ]),
        Value::Object(change),
    ];
    for item in s.refs(task, "learner-task/items")? {
        let old = s.reference(item, "task-item/status")?;
        if s.ident(&json!(old))? == "task-item.status/started" {
            forms.push(json!([
                keyword("db/cas"),
                item,
                keyword("task-item/status"),
                old,
                keyword("task-item.status/paused")
            ]));
            forms.push(json!({"db/id":item,"task-item/elapsed-seconds":timing::elapsed(s,item,at)?,"db/ensure":keyword("task-item/validate")}));
        }
    }
    writeback(
        loaded,
        engine,
        forms,
        "expire-task",
        &uuid(s.entity(task)?, "learner-task/id")?,
        at,
    )
}
pub fn transition_transaction(
    loaded: &LoadedRuntime,
    item: u64,
    status: &str,
    at: DateTime<Utc>,
) -> Result<TransactionPlan> {
    let at = parse_instant(&instant_value(at))?;
    let s = &loaded.snapshot;
    let task = s.item_task(item, loaded.learner_eid)?;
    check_task(loaded, task, at, false)?;
    let activity = s.reference(task, "learner-task/activity")?;
    for kind in ["assessment", "diagnostic"] {
        if let Some(limit) = s
            .entity(activity)?
            .get(&format!("{kind}/time-limit-seconds"))
        {
            let limit = number(limit, "time limit", Some(0.0), None)?;
            if limit == 0.0 {
                return Err("time limit must be positive".into());
            }
            if (at - timing::task_started(s, task)?).num_milliseconds() as f64 / 1000.0 > limit {
                return Err("task time limit has expired".into());
            }
        }
    }
    let old = s.reference(item, "task-item/status")?;
    let old_name = s.ident(&json!(old))?;
    let target = format!(
        "task-item.status/{}",
        status
            .trim_start_matches(':')
            .trim_start_matches("task-item.status/")
    );
    if !matches!(
        (old_name.as_str(), target.as_str()),
        ("task-item.status/started", "task-item.status/paused")
            | ("task-item.status/paused", "task-item.status/started")
    ) {
        return Err(
            "item timing transitions are only started to paused or paused to started".into(),
        );
    }
    if target == "task-item.status/started" && timing::active_item(s, loaded.learner_eid)?.is_some()
    {
        return Err("another item is actively timed".into());
    }
    let forms = vec![
        json!([
            keyword("db/cas"),
            item,
            keyword("task-item/status"),
            old,
            keyword(&target)
        ]),
        json!({"db/id":item,"task-item/elapsed-seconds":timing::elapsed(s,item,at)?,"db/ensure":keyword("task-item/validate")}),
        Value::Object(task_change(s, &json!({"db/id":task}), task, at)?),
    ];
    writeback(
        loaded,
        &loaded.engine,
        forms,
        &format!(
            "transition-item-{}-{}",
            target.rsplit('/').next().unwrap(),
            s.basis_t
        ),
        &uuid(s.entity(item)?, "task-item/id")?,
        at,
    )
}
fn hash_pair(a: &str, b: &str) -> String {
    // Python's default json.dumps escapes non-ASCII before hashing identities.
    let raw = serde_json::to_string(&[a, b]).unwrap();
    let mut escaped = String::new();
    for ch in raw.chars() {
        if ch.is_ascii() {
            escaped.push(ch)
        } else {
            let mut buf = [0u16; 2];
            for code in ch.encode_utf16(&mut buf) {
                escaped.push_str(&format!("\\u{code:04x}"));
            }
        }
    }
    format!("{:x}", Sha256::digest(escaped.as_bytes()))
}
fn writeback(
    loaded: &LoadedRuntime,
    engine: &FireEngine,
    mut forms: Vec<Value>,
    operation: &str,
    identity: &str,
    at: DateTime<Utc>,
) -> Result<TransactionPlan> {
    let old = &loaded.engine;
    if serde_json::to_value(&engine.policy).unwrap() != serde_json::to_value(&old.policy).unwrap()
        || engine.graph.id != old.graph.id
        || engine.difficulty_accuracy != old.difficulty_accuracy
        || engine.neighborhoods != old.neighborhoods
    {
        return Err("writeback must use captured policy, graph, difficulty".into());
    }
    for l in old
        .states
        .keys()
        .chain(engine.states.keys())
        .collect::<BTreeSet<_>>()
    {
        if l != &loaded.learner
            && serde_json::to_value(old.states.get(l)).unwrap()
                != serde_json::to_value(engine.states.get(l)).unwrap()
        {
            return Err("cannot change another learner".into());
        }
    }
    for l in old
        .global_ability
        .keys()
        .chain(engine.global_ability.keys())
        .collect::<BTreeSet<_>>()
    {
        if l != &loaded.learner
            && serde_json::to_value(old.global_ability.get(l)).unwrap()
                != serde_json::to_value(engine.global_ability.get(l)).unwrap()
        {
            return Err("cannot change another learner".into());
        }
    }
    let empty = BTreeMap::new();
    let before = old.states.get(&loaded.learner).unwrap_or(&empty);
    let after = engine.states.get(&loaded.learner).unwrap_or(&empty);
    if before.keys().any(|k| !after.contains_key(k)) {
        return Err("cannot delete topic state".into());
    }
    let mut links = vec![];
    for (topic, state) in after {
        let topic_eid = loaded
            .topic_id_to_eid
            .get(topic)
            .ok_or("unknown output topic")?;
        state.validate()?;
        if let Some(b) = before.get(topic)
            && serde_json::to_value(state).unwrap() == serde_json::to_value(b).unwrap()
        {
            continue;
        }
        let target = loaded
            .progress_by_topic
            .get(topic)
            .map(|x| json!(x))
            .unwrap_or_else(|| json!(format!("engine-progress-{topic}")));
        let mut r=json!({"db/id":target,"progress/topic":topic_eid,"progress/policy":loaded.policy_eid,"progress/memory-at":day_instant(state.memory_at)?,"db/ensure":keyword("progress/validate"),"progress/repetitions":state.repetitions,"progress/memory":state.memory,"progress/interval-days":state.interval_days,"progress/learned":state.learned}).as_object().unwrap().clone();
        if target.is_string() {
            links.push(target.clone());
            r.insert(
                "progress/id".into(),
                json!(format!(
                    "learner-topic-{}",
                    hash_pair(&loaded.learner, topic)
                )),
            );
        }
        let ability = serde_json::to_value(&state.ability).unwrap();
        for f in ABILITY_FIELDS {
            r.insert(
                format!("progress/{}", f.replace('_', "-")),
                ability[f].clone(),
            );
        }
        if let Some(at) = state.last_direct_at {
            r.insert("progress/last-direct-at".into(), day_instant(at)?);
        } else if let Some(at) = before.get(topic).and_then(|b| b.last_direct_at) {
            forms.push(json!([
                keyword("db/retract"),
                target,
                keyword("progress/last-direct-at"),
                day_instant(at)?
            ]));
        }
        forms.push(Value::Object(r));
    }
    let before = old.global_ability.get(&loaded.learner);
    let after = engine.global_ability.get(&loaded.learner);
    if before.is_some() && after.is_none() {
        return Err("cannot remove global performance".into());
    }
    let mut learner = json!({"db/id":loaded.learner_eid,"db/ensure":keyword("learner/validate")})
        .as_object()
        .unwrap()
        .clone();
    if !links.is_empty() {
        learner.insert("learner/knowledge-profile".into(), Value::Array(links));
    }
    if let Some(a) = after
        && serde_json::to_value(before).unwrap() != serde_json::to_value(after).unwrap()
    {
        a.validate()?;
        let target = loaded
            .performance_eid
            .map(Value::from)
            .unwrap_or_else(|| json!("engine-global-performance"));
        let mut r = json!({"db/id":target,"db/ensure":keyword("performance/validate")})
            .as_object()
            .unwrap()
            .clone();
        let values = serde_json::to_value(a).unwrap();
        for f in ABILITY_FIELDS {
            r.insert(
                format!("performance/{}", f.replace('_', "-")),
                values[f].clone(),
            );
        }
        forms.push(Value::Object(r));
        if loaded.performance_eid.is_none() {
            learner.insert("learner/performance".into(), target);
        }
    }
    forms.push(Value::Object(learner));
    forms.push(json!({"db/id":"edb.tx","db/txInstant":instant_value(at)}));
    Ok(TransactionPlan {
        request_key: format!("{operation}-{}", hash_pair(&loaded.learner, identity)),
        compare_basis_t: loaded.snapshot.basis_t,
        edn: edn(&Value::Array(forms.clone()))?,
        forms,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn eid_and_basis_use_the_native_edb_unsigned_range() {
        let snapshot = EntitySnapshot::from_json(&json!({
            "basis_t": u64::MAX,
            "entities": {u64::MAX.to_string(): {"db/ident":"topic/example"}}
        }))
        .unwrap();
        assert_eq!(snapshot.eid(&json!(u64::MAX)).unwrap(), u64::MAX);
        assert_eq!(snapshot.eid(&keyword("topic/example")).unwrap(), u64::MAX);
        assert_eq!(snapshot.basis_t, u64::MAX);
        assert!(EntitySnapshot::from_json(&json!({"basis_t":-1,"entities":{}})).is_err());
        assert!(snapshot.eid(&json!(-1)).is_err());
    }

    #[test]
    fn millisecond_clock_and_edn_value_types_stay_distinct() {
        for milliseconds in [-1, 0, 1, 1_790_637_000_123i64] {
            let at = parse_instant(&json!(milliseconds)).unwrap();
            assert_eq!(
                timestamp_days(at),
                instant_days(&json!(milliseconds)).unwrap()
            );
            assert_eq!(
                parse_instant(&day_instant(timestamp_days(at)).unwrap()).unwrap(),
                at
            );
        }
        assert_eq!(
            edn(&json!({"a/text":"a/value","a/ref":keyword("a/value")})).unwrap(),
            "{:a/ref :a/value :a/text \"a/value\"}"
        );
        assert!(parse_instant(&json!("2026-09-28T01:00:00")).is_err());
    }
}
