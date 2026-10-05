//! Deterministic FIRe transitions, encompassing coverage, and review compression.
//! Numeric policies are explicit local choices; only `public_recurrence` is
//! the literal published algebra. Time is elapsed days, independent of XP.
use std::borrow::Borrow;
use std::collections::{BTreeMap, BTreeSet};

use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use sha2::{Digest, Sha256};

use crate::Result;
use crate::calibration::AccuracyEstimate;

pub fn finite(value: f64, name: &str, low: Option<f64>, high: Option<f64>) -> Result<()> {
    if !value.is_finite() {
        return Err(format!("{name} must be finite"));
    }
    if low.is_some_and(|n| value < n) || high.is_some_and(|n| value > n) {
        return Err(format!("{name} outside [{low:?}, {high:?}]"));
    }
    Ok(())
}

/// Deterministic SHA-256 of compact, sorted JSON. Rust's typed floating-point
/// inputs normalize numeric spellings before hashing.
pub fn fingerprint<T: Serialize>(value: &T) -> String {
    let value = serde_json::to_value(value).expect("serializable engine value");
    let encoded = ascii_json(&value);
    format!("{:x}", Sha256::digest(encoded))
}

// Receipt keys use ASCII escapes, including surrogate pairs, for stable identities.
fn ascii_json<T: Serialize>(value: &T) -> String {
    let raw = serde_json::to_string(value).expect("serializable engine value");
    let mut encoded = String::with_capacity(raw.len());
    for character in raw.chars() {
        if character.is_ascii() {
            encoded.push(character);
        } else {
            for unit in character.encode_utf16(&mut [0; 2]) {
                encoded.push_str(&format!("\\u{unit:04x}"));
            }
        }
    }
    encoded
}

#[allow(clippy::too_many_arguments)]
pub fn public_recurrence(
    repetitions: f64,
    memory: f64,
    speed: f64,
    decay: f64,
    failed: bool,
    raw_delta: f64,
    days: f64,
    interval: f64,
) -> Result<(f64, f64)> {
    for (name, value) in [
        ("repetitions", repetitions),
        ("memory", memory),
        ("speed", speed),
        ("decay", decay),
        ("days", days),
        ("interval", interval),
    ] {
        finite(value, name, Some(0.0), None)?;
    }
    finite(raw_delta, "raw_delta", None, None)?;
    if interval <= 0.0 || speed <= 0.0 || decay < 1.0 {
        return Err("positive interval/speed, decay >= 1 required".into());
    }
    let r = (repetitions + speed * if failed { decay } else { 1.0 } * raw_delta).max(0.0);
    let m = (memory + raw_delta).max(0.0) * 2.0_f64.powf(-days / interval);
    finite(r, "updated repetitions", Some(0.0), None)?;
    finite(m, "updated memory", Some(0.0), None)?;
    Ok((r, m))
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Edge {
    pub advanced: String,
    pub component: String,
    pub weight: f64,
}

impl Edge {
    pub fn new(
        advanced: impl Into<String>,
        component: impl Into<String>,
        weight: f64,
    ) -> Result<Self> {
        let result = Self {
            advanced: advanced.into(),
            component: component.into(),
            weight,
        };
        result.validate()?;
        Ok(result)
    }
    pub fn validate(&self) -> Result<()> {
        if self.advanced.is_empty() || self.component.is_empty() || self.advanced == self.component
        {
            return Err("distinct, nonempty topic IDs required".into());
        }
        finite(self.weight, "weight", Some(0.0), Some(1.0))
    }
}

#[derive(Clone, Debug)]
pub struct EncompassingGraph {
    pub edges: Vec<Edge>,
    pub topics: BTreeSet<String>,
    pub id: String,
    direct: BTreeMap<(String, String), f64>,
    out: BTreeMap<String, Vec<(String, f64)>>,
    order: Vec<String>,
}

impl Default for EncompassingGraph {
    fn default() -> Self {
        Self::new(vec![], BTreeSet::new()).expect("empty graph")
    }
}

impl EncompassingGraph {
    /// A DAG with max-product inferred coverage. Explicit pairs (including
    /// zero) override inferred coverage; failure uses this relation's transpose.
    pub fn new(mut edges: Vec<Edge>, mut topics: BTreeSet<String>) -> Result<Self> {
        if topics.iter().any(String::is_empty) {
            return Err("graph topic IDs must be nonempty".into());
        }
        for edge in &edges {
            edge.validate()?;
            topics.extend([edge.advanced.clone(), edge.component.clone()]);
        }
        edges.sort_by(|a, b| (&a.advanced, &a.component).cmp(&(&b.advanced, &b.component)));
        let mut direct = BTreeMap::new();
        let mut out: BTreeMap<String, Vec<(String, f64)>> =
            topics.iter().map(|t| (t.clone(), vec![])).collect();
        let mut indegree: BTreeMap<String, usize> = topics.iter().map(|t| (t.clone(), 0)).collect();
        for edge in &edges {
            if direct
                .insert((edge.advanced.clone(), edge.component.clone()), edge.weight)
                .is_some()
            {
                return Err(format!(
                    "duplicate encompassing pair: {}, {}",
                    edge.advanced, edge.component
                ));
            }
            out.get_mut(&edge.advanced)
                .unwrap()
                .push((edge.component.clone(), edge.weight));
            *indegree.get_mut(&edge.component).unwrap() += 1;
        }
        let mut ready: BTreeSet<String> = indegree
            .iter()
            .filter(|(_, n)| **n == 0)
            .map(|(t, _)| t.clone())
            .collect();
        let mut order = vec![];
        while let Some(topic) = ready.pop_first() {
            for (child, _) in &out[&topic] {
                let degree = indegree.get_mut(child).unwrap();
                *degree -= 1;
                if *degree == 0 {
                    ready.insert(child.clone());
                }
            }
            order.push(topic);
        }
        if order.len() != topics.len() {
            return Err("encompassing cycles require resolution before use".into());
        }
        let id = fingerprint(&json!({"topics": topics, "edges": edges}));
        Ok(Self {
            edges,
            topics,
            id,
            direct,
            out,
            order,
        })
    }

    pub fn coverage(&self, advanced: &str) -> BTreeMap<String, f64> {
        let mut weights = BTreeMap::from([(advanced.to_owned(), 1.0)]);
        for topic in &self.order {
            if topic != advanced
                && let Some(weight) = self.direct.get(&(advanced.to_owned(), topic.clone()))
            {
                weights.insert(topic.clone(), *weight);
            }
            for (child, weight) in &self.out[topic] {
                let inferred = weights.get(topic).copied().unwrap_or(0.0) * weight;
                let entry = weights.entry(child.clone()).or_insert(0.0);
                *entry = entry.max(inferred);
            }
        }
        weights.retain(|_, w| *w > 0.0);
        weights
    }

    pub fn affected(&self, topic: &str, passed: bool) -> BTreeMap<String, f64> {
        if passed {
            return self.coverage(topic);
        }
        let mut topics = self.topics.clone();
        topics.insert(topic.to_owned());
        topics
            .into_iter()
            .filter_map(|candidate| {
                let weight = self.coverage(&candidate).get(topic).copied().unwrap_or(0.0);
                (weight > 0.0).then_some((candidate, weight))
            })
            .collect()
    }
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(default, deny_unknown_fields)]
pub struct Policy {
    pub name: String,
    pub base_interval_days: f64,
    pub interval_growth: f64,
    pub maximum_interval_days: f64,
    pub due_threshold: f64,
    pub restored_memory: f64,
    pub discount_power: f64,
    pub failure_overdue_slope: f64,
    pub maximum_failure_multiplier: f64,
    pub prior_accuracy: f64,
    pub accuracy_alpha: f64,
    pub speed_exponent: f64,
    pub minimum_speed: f64,
    pub maximum_speed: f64,
    pub gate_slow_implicit: bool,
    pub memory_order: String,
    pub future_horizon_days: f64,
}

impl Default for Policy {
    fn default() -> Self {
        Self {
            name: "fire-reconstruction-v1".into(),
            base_interval_days: 1.0,
            interval_growth: 2.0,
            maximum_interval_days: 36500.0,
            due_threshold: 0.5,
            restored_memory: 1.0,
            discount_power: 1.0,
            failure_overdue_slope: 1.0,
            maximum_failure_multiplier: 4.0,
            prior_accuracy: 0.8,
            accuracy_alpha: 0.2,
            speed_exponent: 2.0,
            minimum_speed: 0.25,
            maximum_speed: 4.0,
            gate_slow_implicit: true,
            memory_order: "decay-before-add".into(),
            future_horizon_days: 7.0,
        }
    }
}

impl Policy {
    pub fn validate(&self) -> Result<()> {
        for (name, value) in [
            ("base_interval_days", self.base_interval_days),
            ("interval_growth", self.interval_growth),
            ("maximum_interval_days", self.maximum_interval_days),
            ("due_threshold", self.due_threshold),
            ("restored_memory", self.restored_memory),
            ("discount_power", self.discount_power),
            ("failure_overdue_slope", self.failure_overdue_slope),
            (
                "maximum_failure_multiplier",
                self.maximum_failure_multiplier,
            ),
            ("prior_accuracy", self.prior_accuracy),
            ("accuracy_alpha", self.accuracy_alpha),
            ("speed_exponent", self.speed_exponent),
            ("minimum_speed", self.minimum_speed),
            ("maximum_speed", self.maximum_speed),
            ("future_horizon_days", self.future_horizon_days),
        ] {
            finite(value, name, Some(0.0), None)?;
        }
        if !(self.base_interval_days > 0.0
            && self.interval_growth > 1.0
            && self.maximum_interval_days >= self.base_interval_days
            && self.due_threshold > 0.0
            && self.due_threshold < self.restored_memory
            && self.prior_accuracy > 0.0
            && self.prior_accuracy < 1.0
            && self.accuracy_alpha > 0.0
            && self.accuracy_alpha <= 1.0
            && self.minimum_speed > 0.0
            && self.minimum_speed <= 1.0
            && self.maximum_speed >= 1.0
            && self.maximum_failure_multiplier >= 1.0
            && self.discount_power > 0.0)
        {
            return Err("invalid FIRe policy bounds".into());
        }
        if !matches!(
            self.memory_order.as_str(),
            "decay-before-add" | "literal-add-before-decay"
        ) {
            return Err("unknown memory timestamp convention".into());
        }
        Ok(())
    }

    pub fn id(&self) -> String {
        fingerprint(self)
    }

    pub fn interval(&self, repetitions: f64) -> Result<f64> {
        finite(repetitions, "repetitions", Some(0.0), None)?;
        let (log_base, log_growth) = (self.base_interval_days.ln(), self.interval_growth.ln());
        let ceiling = (self.maximum_interval_days.ln() - log_base) / log_growth;
        if repetitions >= ceiling {
            return Ok(self.maximum_interval_days);
        }
        let power = self.interval_growth.powf(repetitions);
        let interval = if power.is_infinite() {
            (log_base + repetitions * log_growth).exp()
        } else {
            self.base_interval_days * power
        };
        Ok(self.maximum_interval_days.min(interval))
    }

    pub fn speed(&self, accuracy: f64) -> Result<f64> {
        finite(accuracy, "accuracy", Some(0.0), Some(1.0))?;
        if self.speed_exponent == 0.0 {
            return Ok(1.0);
        }
        if accuracy == 0.0 {
            return Ok(self.minimum_speed);
        }
        let baseline = self.prior_accuracy.ln();
        let log_speed = self.speed_exponent * (accuracy.ln() - baseline);
        if log_speed <= self.minimum_speed.ln() {
            return Ok(self.minimum_speed);
        }
        if log_speed >= self.maximum_speed.ln() {
            return Ok(self.maximum_speed);
        }
        Ok(log_speed
            .exp()
            .max(self.minimum_speed)
            .min(self.maximum_speed))
    }

    pub fn discount(&self, memory_now: f64) -> Result<f64> {
        finite(memory_now, "memory_now", Some(0.0), None)?;
        Ok(
            ((self.restored_memory - memory_now) / (self.restored_memory - self.due_threshold))
                .clamp(0.0, 1.0)
                .powf(self.discount_power),
        )
    }

    pub fn failure_multiplier(&self, memory_now: f64) -> Result<f64> {
        finite(memory_now, "memory_now", Some(0.0), None)?;
        if memory_now >= self.due_threshold || self.failure_overdue_slope == 0.0 {
            return Ok(1.0);
        }
        if memory_now == 0.0 {
            return Ok(self.maximum_failure_multiplier);
        }
        let overdue = self.due_threshold.log2() - memory_now.log2();
        Ok((1.0 + self.failure_overdue_slope * overdue).min(self.maximum_failure_multiplier))
    }
}

#[derive(Clone, Debug, PartialEq, Serialize)]
pub struct TopicState {
    pub repetitions: f64,
    pub memory: f64,
    pub memory_at: f64,
    pub interval_days: f64,
    pub ability: AccuracyEstimate,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expected_assessment_accuracy: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expected_practice_accuracy: Option<f64>,
    pub learned: bool,
    pub last_direct_at: Option<f64>,
}

impl Default for TopicState {
    fn default() -> Self {
        Self {
            repetitions: 0.0,
            memory: 1.0,
            memory_at: 0.0,
            interval_days: 1.0,
            ability: AccuracyEstimate::default(),
            expected_assessment_accuracy: None,
            expected_practice_accuracy: None,
            learned: true,
            last_direct_at: None,
        }
    }
}

// Validate deserialized state before it can enter the engine.
impl<'de> Deserialize<'de> for TopicState {
    fn deserialize<D: serde::Deserializer<'de>>(
        deserializer: D,
    ) -> std::result::Result<Self, D::Error> {
        #[derive(Deserialize)]
        #[serde(default, deny_unknown_fields)]
        struct Fields {
            repetitions: f64,
            memory: f64,
            memory_at: f64,
            interval_days: f64,
            ability: AccuracyEstimate,
            expected_assessment_accuracy: Option<f64>,
            expected_practice_accuracy: Option<f64>,
            learned: bool,
            last_direct_at: Option<f64>,
        }
        impl Default for Fields {
            fn default() -> Self {
                Self {
                    repetitions: 0.0,
                    memory: 1.0,
                    memory_at: 0.0,
                    interval_days: 1.0,
                    ability: AccuracyEstimate::default(),
                    expected_assessment_accuracy: None,
                    expected_practice_accuracy: None,
                    learned: true,
                    last_direct_at: None,
                }
            }
        }
        let fields = Fields::deserialize(deserializer)?;
        let result = Self {
            repetitions: fields.repetitions,
            memory: fields.memory,
            memory_at: fields.memory_at,
            interval_days: fields.interval_days,
            ability: fields.ability,
            expected_assessment_accuracy: fields.expected_assessment_accuracy,
            expected_practice_accuracy: fields.expected_practice_accuracy,
            learned: fields.learned,
            last_direct_at: fields.last_direct_at,
        };
        result.validate().map_err(serde::de::Error::custom)?;
        Ok(result)
    }
}

impl TopicState {
    pub fn new(prior_accuracy: f64, learned: bool) -> Self {
        Self {
            ability: AccuracyEstimate::new(prior_accuracy),
            learned,
            ..Self::default()
        }
    }
    pub fn accuracy(&self) -> f64 {
        self.ability.accuracy()
    }
    pub fn evidence_mass(&self) -> f64 {
        self.ability.assessment_mass + self.ability.practice_mass
    }
    pub fn set_accuracy(&mut self, value: f64) -> Result<()> {
        finite(value, "accuracy", Some(0.0), Some(1.0))?;
        self.ability.assessment_accuracy = value;
        self.ability.practice_accuracy = value;
        Ok(())
    }
    pub fn validate(&self) -> Result<()> {
        self.ability.validate()?;
        for (name, value) in [
            (
                "expected_assessment_accuracy",
                self.expected_assessment_accuracy,
            ),
            (
                "expected_practice_accuracy",
                self.expected_practice_accuracy,
            ),
        ] {
            if let Some(value) = value {
                finite(value, name, Some(0.0), Some(1.0))?;
            }
        }
        for (name, value) in [
            ("repetitions", self.repetitions),
            ("memory", self.memory),
            ("interval_days", self.interval_days),
            ("evidence_mass", self.evidence_mass()),
        ] {
            finite(value, name, Some(0.0), None)?;
        }
        finite(self.memory_at, "memory_at", None, None)?;
        finite(self.accuracy(), "accuracy", Some(0.0), Some(1.0))?;
        if self.interval_days <= 0.0 {
            return Err("positive interval required".into());
        }
        if let Some(at) = self.last_direct_at {
            finite(at, "last_direct_at", None, None)?;
        }
        Ok(())
    }
    pub fn memory_now(&self, at: f64) -> Result<f64> {
        finite(at, "at", None, None)?;
        if at < self.memory_at {
            return Err("cannot read a state before its observation time".into());
        }
        Ok(self.memory * 2.0_f64.powf(-(at - self.memory_at) / self.interval_days))
    }
    pub fn due_at(&self, policy: &Policy) -> f64 {
        if self.memory <= policy.due_threshold {
            self.memory_at
        } else {
            self.memory_at + self.interval_days * (self.memory.log2() - policy.due_threshold.log2())
        }
    }
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Event {
    pub id: String,
    pub learner: String,
    pub topic: String,
    pub at: f64,
    pub passed: bool,
    #[serde(default = "one")]
    pub quality: f64,
    #[serde(default = "review")]
    pub kind: String,
    #[serde(default)]
    pub learned: bool,
    #[serde(default)]
    pub question_results: Vec<bool>,
    #[serde(default = "direct")]
    pub source: String,
    #[serde(default)]
    pub assessment: bool,
}
fn one() -> f64 {
    1.0
}
fn review() -> String {
    "review".into()
}
fn direct() -> String {
    "direct".into()
}
impl Default for Event {
    fn default() -> Self {
        Self {
            id: String::new(),
            learner: String::new(),
            topic: String::new(),
            at: 0.0,
            passed: true,
            quality: 1.0,
            kind: review(),
            learned: false,
            question_results: vec![],
            source: direct(),
            assessment: false,
        }
    }
}
impl Event {
    pub fn validate(&self) -> Result<()> {
        if [
            &self.id,
            &self.learner,
            &self.topic,
            &self.kind,
            &self.source,
        ]
        .iter()
        .any(|s| s.is_empty())
        {
            return Err("nonempty event/learner/topic/kind/source required".into());
        }
        finite(self.at, "at", None, None)?;
        finite(self.quality, "quality", Some(0.0), None)?;
        if self.quality <= 0.0 {
            return Err("positive quality required".into());
        }
        if self.learned && !self.passed {
            return Err("failed evidence cannot initialize learned status".into());
        }
        Ok(())
    }
}

#[derive(Clone, Debug)]
pub struct FireEngine {
    pub graph: EncompassingGraph,
    pub policy: Policy,
    pub states: BTreeMap<String, BTreeMap<String, TopicState>>,
    pub receipts: BTreeMap<String, Value>,
    pub latest: BTreeMap<String, f64>,
    pub global_ability: BTreeMap<String, AccuracyEstimate>,
    pub neighborhoods: BTreeMap<String, Vec<String>>,
}

impl Default for FireEngine {
    fn default() -> Self {
        Self::new(
            EncompassingGraph::default(),
            Policy::default(),
            BTreeMap::new(),
        )
        .expect("default engine")
    }
}

impl FireEngine {
    pub fn new(
        graph: EncompassingGraph,
        policy: Policy,
        mut neighborhoods: BTreeMap<String, Vec<String>>,
    ) -> Result<Self> {
        policy.validate()?;
        for neighbors in neighborhoods.values_mut() {
            neighbors.sort();
            neighbors.dedup();
        }
        Ok(Self {
            graph,
            policy,
            neighborhoods,
            states: BTreeMap::new(),
            receipts: BTreeMap::new(),
            latest: BTreeMap::new(),
            global_ability: BTreeMap::new(),
        })
    }

    /// Separate mass-weighted forecasts using direct prerequisites only.
    /// Fallback is all other observed topic states in the same channel, then
    /// the policy prior. Global outcome EWMA is not a mass-weighted topic mean.
    pub fn expected_accuracy(&self, learner: &str, topic: &str) -> (f64, f64) {
        let neighbors: BTreeSet<String> = self
            .neighborhoods
            .get(topic)
            .into_iter()
            .flatten()
            .cloned()
            .collect();
        let channel = |assessment: bool, direct_only: bool| -> Option<f64> {
            let mut values = vec![];
            for (id, state) in self.states.get(learner).into_iter().flat_map(|s| s.iter()) {
                if id == topic || (direct_only && !neighbors.contains(id)) {
                    continue;
                }
                let (accuracy, mass) = if assessment {
                    (
                        state.ability.assessment_accuracy,
                        state.ability.assessment_mass,
                    )
                } else {
                    (state.ability.practice_accuracy, state.ability.practice_mass)
                };
                if mass > 0.0 {
                    values.push((accuracy, mass));
                }
            }
            let scale = values.iter().map(|(_, mass)| *mass).reduce(f64::max)?;
            let total: f64 = values.iter().map(|(_, mass)| mass / scale).sum();
            Some(
                values
                    .iter()
                    .map(|(accuracy, mass)| accuracy * (mass / scale))
                    .sum::<f64>()
                    / total,
            )
        };
        let predict = |assessment| {
            channel(assessment, true)
                .or_else(|| channel(assessment, false))
                .unwrap_or(self.policy.prior_accuracy)
        };
        (predict(true), predict(false))
    }

    pub fn initial_state(&self, learner: &str, topic: &str, learned: bool) -> TopicState {
        let (assessment, practice) = self.expected_accuracy(learner, topic);
        let mut state = TopicState::new(self.policy.prior_accuracy, learned);
        state.ability.assessment_accuracy = assessment;
        state.ability.practice_accuracy = practice;
        state.expected_assessment_accuracy = Some(assessment);
        state.expected_practice_accuracy = Some(practice);
        state
    }

    pub fn seed(&mut self, learner: &str, topic: &str, state: TopicState) -> Result<()> {
        if learner.is_empty() || topic.is_empty() {
            return Err("learner and topic IDs must be nonempty".into());
        }
        if self
            .states
            .get(learner)
            .is_some_and(|s| s.contains_key(topic))
        {
            return Err("seed cannot overwrite learner state".into());
        }
        state.validate()?;
        let latest = self
            .latest
            .get(learner)
            .copied()
            .unwrap_or(f64::NEG_INFINITY)
            .max(state.memory_at)
            .max(state.last_direct_at.unwrap_or(f64::NEG_INFINITY));
        self.states
            .entry(learner.into())
            .or_default()
            .insert(topic.into(), state);
        self.latest.insert(learner.into(), latest);
        Ok(())
    }

    pub fn speed(&self, _topic: &str, state: &TopicState) -> Result<f64> {
        self.policy.speed(state.accuracy())
    }

    pub fn due(&self, learner: &str, at: f64) -> Result<Vec<String>> {
        finite(at, "at", None, None)?;
        let mut due = vec![];
        for (topic, state) in self.states.get(learner).into_iter().flat_map(|s| s.iter()) {
            if !state.learned {
                continue;
            }
            let now = state.memory_now(at)?;
            let threshold = self.policy.due_threshold;
            if now <= threshold || (now - threshold).abs() <= 1e-12 * now.abs().max(threshold.abs())
            {
                due.push(topic.clone());
            }
        }
        Ok(due)
    }

    pub fn apply(&mut self, event: impl Borrow<Event>) -> Result<Value> {
        self.apply_mode(event.borrow(), "combined")
    }
    pub fn apply_accuracy(&mut self, event: impl Borrow<Event>) -> Result<Value> {
        if event.borrow().learned {
            return Err("accuracy evidence cannot establish learned status".into());
        }
        self.apply_mode(event.borrow(), "accuracy")
    }
    pub fn apply_retention(&mut self, event: impl Borrow<Event>) -> Result<Value> {
        self.apply_mode(event.borrow(), "retention")
    }

    fn apply_mode(&mut self, event: &Event, mode: &str) -> Result<Value> {
        event.validate()?;
        self.policy.validate()?;
        let update_accuracy = mode != "retention";
        let update_retention = mode != "accuracy";
        let key = ascii_json(&[&event.learner, &event.id]);
        let digest = if mode == "combined" {
            fingerprint(event)
        } else {
            fingerprint(&json!({"mode": mode, "event": event}))
        };
        if let Some(receipt) = self.receipts.get(&key) {
            let same_mode = receipt.get("mode").and_then(Value::as_str) == Some(mode);
            let same_hash =
                receipt.get("event_hash").and_then(Value::as_str) == Some(digest.as_str());
            if !same_mode || !same_hash {
                return Err("event ID reused with different evidence or update mode".into());
            }
            return Ok(receipt.clone());
        }
        if event.at
            < self
                .latest
                .get(&event.learner)
                .copied()
                .unwrap_or(f64::NEG_INFINITY)
        {
            return Err("events must be chronological; rebuild to insert older evidence".into());
        }
        let mut working = self.states.get(&event.learner).cloned().unwrap_or_default();
        let p = &self.policy;
        let global_before = self
            .global_ability
            .get(&event.learner)
            .cloned()
            .unwrap_or_else(|| AccuracyEstimate::new(p.prior_accuracy));
        global_before.validate()?;
        let mut global_after = global_before.clone();
        let fallback = [event.passed];
        let answers = if event.question_results.is_empty() {
            &fallback[..]
        } else {
            &event.question_results[..]
        };
        if update_accuracy {
            global_after.update(answers, event.assessment, p.accuracy_alpha, 1.0)?;
        }
        let initializing = update_retention
            && event.learned
            && working.get(&event.topic).is_none_or(|s| !s.learned);
        let retention_coverage = if update_retention {
            self.graph.affected(&event.topic, event.passed)
        } else {
            BTreeMap::new()
        };
        let mut accuracy_evidence: BTreeMap<String, Vec<(bool, f64)>> = BTreeMap::new();
        if update_accuracy {
            for &correct in answers {
                for (target, weight) in self.graph.affected(&event.topic, correct) {
                    accuracy_evidence
                        .entry(target)
                        .or_default()
                        .push((correct, weight));
                }
            }
        }
        let targets: BTreeSet<String> = retention_coverage
            .keys()
            .chain(accuracy_evidence.keys())
            .cloned()
            .collect();
        let mut updates = vec![];
        for topic in targets {
            let coverage = retention_coverage.get(&topic).copied().unwrap_or(0.0);
            let created = !working.contains_key(&topic);
            let initial = self.initial_state(&event.learner, &topic, false);
            let state = working.entry(topic.clone()).or_insert_with(|| TopicState {
                memory: 0.0,
                memory_at: event.at,
                learned: false,
                interval_days: p.base_interval_days,
                ..initial.clone()
            });
            // Existing outcome evidence is preserved; missing legacy forecasts
            // are explicitly filled at this observation, not reconstructed past.
            state.expected_assessment_accuracy = state
                .expected_assessment_accuracy
                .or(initial.expected_assessment_accuracy);
            state.expected_practice_accuracy = state
                .expected_practice_accuracy
                .or(initial.expected_practice_accuracy);
            state.validate()?;
            let before = serde_json::to_value(&*state).map_err(|e| e.to_string())?;
            if event.at < state.memory_at {
                return Err("event predates the topic state".into());
            }
            if initializing && topic == event.topic {
                state.learned = true;
            }
            let evidence = accuracy_evidence.get(&topic).cloned().unwrap_or_default();
            if !update_retention || !state.learned {
                for &(correct, weight) in &evidence {
                    state
                        .ability
                        .update(&[correct], event.assessment, p.accuracy_alpha, weight)?;
                }
                if topic == event.topic {
                    state.last_direct_at = Some(event.at);
                }
                updates.push(json!({"topic": topic, "coverage": coverage,
                    "skipped": if !update_retention { "accuracy-only" } else { "not-learned" },
                    "created": created, "accuracy_evidence": evidence, "before": before, "after": state}));
                continue;
            }
            let direct = topic == event.topic;
            let now = state.memory_now(event.at)?;
            let speed = self.speed(&topic, state)?;
            let gated = coverage > 0.0
                && event.passed
                && !direct
                && p.gate_slow_implicit
                && speed < 1.0 - 1e-12;
            let discount = if initializing && direct {
                1.0
            } else {
                p.discount(now)?
            };
            let mut raw =
                if event.passed { 1.0 } else { -1.0 } * event.quality * coverage * discount;
            if gated {
                raw = 0.0;
            }
            let decay = if event.passed {
                1.0
            } else {
                p.failure_multiplier(now)?
            };
            let (repetitions, memory) = if initializing && direct {
                (speed * event.quality, p.restored_memory)
            } else {
                let repetitions = (state.repetitions + speed * decay * raw).max(0.0);
                let memory = if p.memory_order == "literal-add-before-decay" {
                    public_recurrence(
                        state.repetitions,
                        state.memory,
                        speed,
                        decay,
                        !event.passed,
                        raw,
                        event.at - state.memory_at,
                        state.interval_days,
                    )?
                    .1
                } else {
                    (now + raw).max(0.0)
                };
                (repetitions, memory)
            };
            for &(correct, weight) in &evidence {
                state
                    .ability
                    .update(&[correct], event.assessment, p.accuracy_alpha, weight)?;
            }
            finite(repetitions, "updated repetitions", Some(0.0), None)?;
            finite(memory, "updated memory", Some(0.0), None)?;
            state.repetitions = repetitions;
            state.memory = memory;
            state.memory_at = event.at;
            if raw != 0.0 || initializing && direct {
                state.interval_days = p.interval(repetitions)?;
            }
            if direct {
                state.last_direct_at = Some(event.at);
            }
            let due_at = state.due_at(p);
            // Reject nonfinite receipt data before committing the event.
            finite(due_at, "due_at", None, None)?;
            finite(raw, "raw_delta", None, None)?;
            updates.push(json!({"topic": topic, "direct": direct, "coverage": coverage, "created": created,
                "memory_before_decay": before["memory"], "memory_now": now, "discount": discount, "raw_delta": raw,
                "speed": speed, "accuracy_evidence": evidence, "failure_multiplier": decay, "implicit_gated": gated,
                "before": before, "after": state, "due_at": due_at}));
        }
        let receipt = json!({"event": event, "event_hash": digest, "mode": mode, "policy_id": p.id(),
            "graph_id": self.graph.id, "updates": updates, "global_ability_before": global_before,
            "global_ability_after": global_after,
            "neighborhood_id": fingerprint(&self.neighborhoods)});
        self.states.insert(event.learner.clone(), working);
        if update_accuracy {
            self.global_ability
                .insert(event.learner.clone(), global_after);
        }
        self.latest.insert(event.learner.clone(), event.at);
        self.receipts.insert(key, receipt.clone());
        Ok(receipt)
    }

    pub fn rank(&self, learner: &str, at: f64, candidates: Vec<Value>) -> Result<Vec<Value>> {
        let due: BTreeSet<String> = self.due(learner, at)?.into_iter().collect();
        let mut ranked = vec![];
        for candidate in candidates {
            let topic = candidate
                .get("topic")
                .and_then(Value::as_str)
                .ok_or("candidate requires topic")?;
            let minutes = candidate
                .get("expected_minutes")
                .and_then(Value::as_f64)
                .ok_or("candidate requires expected_minutes")?;
            finite(minutes, "expected_minutes", Some(0.0), None)?;
            if minutes <= 0.0 {
                return Err("candidate expected time must be positive".into());
            }
            let mut trial = self.clone();
            let mut preview_id = format!("preview:{topic}");
            let mut suffix = 0;
            while trial
                .receipts
                .contains_key(&ascii_json(&[learner, &preview_id]))
            {
                suffix += 1;
                preview_id = format!("preview:{topic}:{suffix}");
            }
            let kind = candidate
                .get("kind")
                .and_then(Value::as_str)
                .unwrap_or("review");
            trial.apply_retention(Event {
                id: preview_id,
                learner: learner.into(),
                topic: topic.into(),
                at,
                learned: kind == "lesson",
                kind: kind.into(),
                ..Event::default()
            })?;
            let after_due: BTreeSet<String> = trial.due(learner, at)?.into_iter().collect();
            let removed: Vec<String> = due.difference(&after_due).cloned().collect();
            let mut future_gain = 0.0;
            for (t, before) in self.states.get(learner).into_iter().flat_map(|s| s.iter()) {
                if !before.learned {
                    continue;
                }
                let after = &trial.states[learner][t];
                let b = (before.due_at(&self.policy) - at)
                    .min(self.policy.future_horizon_days)
                    .max(0.0);
                let a = (after.due_at(&self.policy) - at)
                    .min(self.policy.future_horizon_days)
                    .max(0.0);
                future_gain += (a - b).max(0.0);
            }
            let removed_rate = removed.len() as f64 / minutes;
            let gain_rate = future_gain / minutes;
            finite(removed_rate, "due_removed_per_minute", Some(0.0), None)?;
            finite(gain_rate, "future_days_gained_per_minute", Some(0.0), None)?;
            let mut result = candidate
                .as_object()
                .ok_or("candidate must be a map")?
                .clone();
            result.insert("due_removed".into(), json!(removed));
            result.insert("due_removed_per_minute".into(), json!(removed_rate));
            result.insert("future_days_gained_per_minute".into(), json!(gain_rate));
            ranked.push(Value::Object(result));
        }
        ranked.sort_by(|a, b| {
            b["due_removed_per_minute"]
                .as_f64()
                .unwrap()
                .total_cmp(&a["due_removed_per_minute"].as_f64().unwrap())
                .then_with(|| {
                    b["future_days_gained_per_minute"]
                        .as_f64()
                        .unwrap()
                        .total_cmp(&a["future_days_gained_per_minute"].as_f64().unwrap())
                })
                .then_with(|| a["topic"].as_str().cmp(&b["topic"].as_str()))
        });
        Ok(ranked)
    }

    pub fn snapshot(&self) -> Value {
        json!({"format": 1, "policy": self.policy, "graph": self.graph.edges, "topics": self.graph.topics,
            "states": self.states, "receipts": self.receipts,
            "latest": self.latest, "global_ability": self.global_ability, "neighborhoods": self.neighborhoods})
    }

    pub fn restore(data: Value) -> Result<Self> {
        #[derive(Deserialize)]
        struct Snapshot {
            format: u64,
            policy: Policy,
            graph: Vec<Edge>,
            topics: BTreeSet<String>,
            #[serde(default)]
            difficulty_accuracy: BTreeMap<String, f64>,
            states: BTreeMap<String, BTreeMap<String, TopicState>>,
            receipts: BTreeMap<String, Value>,
            latest: BTreeMap<String, f64>,
            #[serde(default)]
            global_ability: BTreeMap<String, AccuracyEstimate>,
            #[serde(default)]
            neighborhoods: BTreeMap<String, Vec<String>>,
        }
        let data: Snapshot = serde_json::from_value(data).map_err(|e| e.to_string())?;
        if data.format != 1 {
            return Err("unsupported snapshot format".into());
        }
        if !data.difficulty_accuracy.is_empty() {
            return Err(
                "legacy topic accuracy calibration must be retired before restoring this snapshot"
                    .into(),
            );
        }
        let mut result = Self::new(
            EncompassingGraph::new(data.graph, data.topics)?,
            data.policy,
            data.neighborhoods,
        )?;
        for (learner, states) in data.states {
            for (topic, state) in states {
                result.seed(&learner, &topic, state)?;
            }
        }
        result.receipts = data.receipts;
        for (learner, at) in data.latest {
            if learner.is_empty() {
                return Err("learner IDs must be nonempty".into());
            }
            finite(at, "latest observation time", None, None)?;
            let observed = result.latest.entry(learner).or_insert(at);
            *observed = observed.max(at);
        }
        for value in data.global_ability.values() {
            value.validate()?;
        }
        result.global_ability = data.global_ability;
        Ok(result)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn graph(edges: &[(&str, &str, f64)]) -> EncompassingGraph {
        EncompassingGraph::new(
            edges
                .iter()
                .map(|(a, b, w)| Edge::new(*a, *b, *w).unwrap())
                .collect(),
            BTreeSet::new(),
        )
        .unwrap()
    }
    fn engine(edges: &[(&str, &str, f64)]) -> FireEngine {
        let mut engine = FireEngine::new(graph(edges), Policy::default(), BTreeMap::new()).unwrap();
        for topic in ["A", "B", "C"] {
            engine
                .seed("learner", topic, TopicState::default())
                .unwrap();
        }
        engine
    }
    fn event(id: &str, topic: &str, at: f64, passed: bool) -> Event {
        Event {
            id: id.into(),
            learner: "learner".into(),
            topic: topic.into(),
            at,
            passed,
            ..Event::default()
        }
    }
    fn close(a: f64, b: f64) {
        assert!((a - b).abs() < 1e-12, "{a} != {b}");
    }

    #[test]
    fn json_rejects_unknown_fields_and_missing_required_event_data() {
        assert!(serde_json::from_value::<Policy>(json!({"magic": 1})).is_err());
        assert!(serde_json::from_value::<AccuracyEstimate>(json!({"magic": 1})).is_err());
        assert!(serde_json::from_value::<TopicState>(json!({"magic": 1})).is_err());
        let valid = json!({"id":"e","learner":"l","topic":"A","at":1,"passed":true});
        for field in ["id", "learner", "topic", "at", "passed"] {
            let mut missing = valid.clone();
            missing.as_object_mut().unwrap().remove(field);
            assert!(serde_json::from_value::<Event>(missing).is_err());
        }
        let mut unknown = valid;
        unknown["magic"] = json!(1);
        assert!(serde_json::from_value::<Event>(unknown).is_err());
    }

    #[test]
    fn published_recurrence_and_extreme_values() {
        assert_eq!(
            public_recurrence(3.0, 1.0, 2.0, 1.0, false, 0.5, 2.0, 2.0).unwrap(),
            (4.0, 0.75)
        );
        assert_eq!(
            public_recurrence(1.0, 0.2, 2.0, 3.0, true, -0.5, 2.0, 2.0).unwrap(),
            (0.0, 0.0)
        );
        assert!(public_recurrence(0.0, 1.0, 2.0, 1.0, false, 1e308, 0.0, 1.0).is_err());
        let policy = Policy {
            base_interval_days: 1e-300,
            maximum_interval_days: 1e300,
            interval_growth: 1e300,
            speed_exponent: 1e308,
            ..Policy::default()
        };
        policy.validate().unwrap();
        close(policy.interval(1.5).unwrap() / 1e150, 1.0);
        assert_eq!(policy.interval(1e308).unwrap(), 1e300);
        assert_eq!(policy.speed(0.81).unwrap(), policy.maximum_speed);
        assert_eq!(policy.speed(0.79).unwrap(), policy.minimum_speed);
        assert_eq!(policy.speed(0.0).unwrap(), policy.minimum_speed);
        assert_eq!(
            Policy {
                speed_exponent: 0.0,
                ..Policy::default()
            }
            .speed(0.0)
            .unwrap(),
            1.0
        );
    }

    #[test]
    fn graph_diamonds_overrides_transpose_and_validation() {
        let diamond = graph(&[
            ("A", "B", 0.5),
            ("A", "C", 0.8),
            ("B", "D", 0.5),
            ("C", "D", 0.5),
        ]);
        assert_eq!(diamond.coverage("A")["D"], 0.4);
        assert_eq!(diamond.affected("D", false)["A"], 0.4);
        for override_weight in [0.0, 0.1] {
            let overridden = graph(&[
                ("A", "B", 1.0),
                ("B", "C", 1.0),
                ("A", "C", override_weight),
            ]);
            assert_eq!(
                overridden.coverage("A").get("C").copied().unwrap_or(0.0),
                override_weight
            );
            assert_eq!(
                overridden
                    .affected("C", false)
                    .get("A")
                    .copied()
                    .unwrap_or(0.0),
                override_weight
            );
        }
        assert!(
            EncompassingGraph::new(
                vec![
                    Edge::new("A", "B", 1.0).unwrap(),
                    Edge::new("B", "A", 1.0).unwrap()
                ],
                BTreeSet::new()
            )
            .is_err()
        );
        assert!(
            EncompassingGraph::new(vec![Edge::new("A", "B", 1.0).unwrap(); 2], BTreeSet::new())
                .is_err()
        );
        assert!(Edge::new("A", "A", 1.0).is_err());
        assert!(Edge::new("A", "B", f64::NAN).is_err());
    }

    #[test]
    fn success_down_failure_up_and_local_discounts() {
        let mut engine = engine(&[("A", "B", 1.0), ("A", "C", 1.0)]);
        let receipt = engine.apply(event("e", "A", 1.0, true)).unwrap();
        assert_eq!(receipt["updates"].as_array().unwrap().len(), 3);
        for state in engine.states["learner"].values() {
            close(state.repetitions, 1.0);
        }
        let receipt = engine.apply(event("f", "B", 3.0, false)).unwrap();
        let topics: Vec<_> = receipt["updates"]
            .as_array()
            .unwrap()
            .iter()
            .map(|u| u["topic"].as_str().unwrap())
            .collect();
        assert_eq!(topics, ["A", "B"]);
        let mut engine = super::tests::engine(&[("A", "B", 1.0)]);
        engine
            .states
            .get_mut("learner")
            .unwrap()
            .get_mut("A")
            .unwrap()
            .memory_at = 1.0;
        let receipt = engine.apply(event("e", "A", 1.0, true)).unwrap();
        assert_eq!(receipt["updates"][0]["raw_delta"], 0.0);
        assert_eq!(receipt["updates"][1]["raw_delta"], 1.0);
    }

    #[test]
    fn slow_implicit_gate_does_not_block_graph_transit() {
        let mut engine = engine(&[("A", "B", 1.0), ("B", "C", 1.0)]);
        engine
            .states
            .get_mut("learner")
            .unwrap()
            .get_mut("B")
            .unwrap()
            .set_accuracy(0.4)
            .unwrap();
        engine.apply(event("e", "A", 1.0, true)).unwrap();
        assert_eq!(engine.states["learner"]["B"].repetitions, 0.0);
        assert_eq!(engine.states["learner"]["C"].repetitions, 1.0);
        engine.apply(event("explicit", "B", 2.0, true)).unwrap();
        assert!(engine.states["learner"]["B"].repetitions > 0.0);
    }

    #[test]
    fn failed_first_lesson_informs_ability_then_initializes_without_double_counting() {
        let mut engine = FireEngine::new(
            graph(&[("A", "B", 1.0)]),
            Policy::default(),
            BTreeMap::new(),
        )
        .unwrap();
        engine
            .apply_accuracy(event("wrong", "A", 0.0, false))
            .unwrap();
        engine
            .apply_accuracy(event("right", "A", 0.1, true))
            .unwrap();
        let before = engine.states["learner"]["A"].clone();
        assert!(!before.learned);
        assert_eq!(before.memory, 0.0);
        assert_eq!(before.evidence_mass(), 2.0);
        let speed = engine.speed("A", &before).unwrap();
        engine
            .apply_retention(Event {
                learned: true,
                kind: "lesson".into(),
                ..event("unit", "A", 0.2, true)
            })
            .unwrap();
        let after = &engine.states["learner"]["A"];
        assert!(after.learned);
        assert_eq!(after.memory, 1.0);
        close(after.repetitions, speed);
        assert_eq!(before.ability, after.ability);
        assert!(!engine.states["learner"]["B"].learned);
        assert_eq!(engine.global_ability["learner"].practice_mass, 2.0);
    }

    #[test]
    fn mixed_answers_route_accuracy_independently_of_unit_outcome() {
        let mut engine = engine(&[("A", "B", 1.0), ("C", "A", 1.0)]);
        engine
            .apply(Event {
                question_results: vec![true, false, true],
                ..event("e", "A", 1.0, true)
            })
            .unwrap();
        assert!(engine.states["learner"]["B"].accuracy() > 0.8);
        assert!(engine.states["learner"]["C"].accuracy() < 0.8);
        assert_eq!(engine.states["learner"]["C"].repetitions, 0.0);
        assert_eq!(engine.global_ability["learner"].practice_mass, 3.0);
    }

    #[test]
    fn accuracy_only_preserves_retention_and_fractional_channels() {
        let mut engine = engine(&[("A", "B", 0.5), ("C", "A", 0.25)]);
        let before = engine.states["learner"].clone();
        engine
            .apply_accuracy(Event {
                assessment: true,
                ..event("e", "A", 1.0, false)
            })
            .unwrap();
        assert_eq!(engine.states["learner"]["C"].ability.assessment_mass, 0.25);
        assert_eq!(engine.states["learner"]["B"].evidence_mass(), 0.0);
        for (topic, state) in &engine.states["learner"] {
            let original = &before[topic];
            assert_eq!(
                (
                    state.repetitions,
                    state.memory,
                    state.memory_at,
                    state.interval_days,
                    state.learned
                ),
                (
                    original.repetitions,
                    original.memory,
                    original.memory_at,
                    original.interval_days,
                    original.learned
                )
            );
        }
        assert_eq!(engine.states["learner"]["A"].last_direct_at, Some(1.0));
        assert_eq!(engine.states["learner"]["C"].last_direct_at, None);
    }

    #[test]
    fn retries_and_snapshot_round_trip_preserve_state() {
        let mut engine = engine(&[("A", "B", 0.5)]);
        let event = event("e", "A", 1.0, true);
        let receipt = engine.apply(&event).unwrap();
        let mut restored = FireEngine::restore(engine.snapshot()).unwrap();
        assert_eq!(restored.apply(&event).unwrap(), receipt);
        let before = restored.snapshot();
        assert!(
            restored
                .apply(Event {
                    passed: false,
                    ..event.clone()
                })
                .is_err()
        );
        assert!(restored.apply_retention(&event).is_err());
        assert_eq!(restored.snapshot(), before);
        let next = Event {
            id: "next".into(),
            at: 4.0,
            ..event
        };
        assert_eq!(restored.apply(&next).unwrap(), engine.apply(&next).unwrap());
    }

    #[test]
    fn receipt_fingerprints_and_modes_are_required_for_retries() {
        let mut engine = engine(&[]);
        let event = event("e", "A", 1.0, true);
        engine.apply(&event).unwrap();
        for field in ["mode", "event_hash"] {
            let mut snapshot = engine.snapshot();
            let receipt = snapshot["receipts"]
                .as_object_mut()
                .unwrap()
                .values_mut()
                .next()
                .unwrap();
            receipt.as_object_mut().unwrap().remove(field);
            let mut restored = FireEngine::restore(snapshot).unwrap();
            let before = restored.snapshot();
            assert!(restored.apply(&event).is_err());
            assert_eq!(restored.snapshot(), before);
        }
        let mut engine = FireEngine::default();
        let unicode = Event {
            learner: "élève🧑".into(),
            id: "é1".into(),
            ..super::tests::event("e", "A", 1.0, true)
        };
        let original = engine.apply(&unicode).unwrap();
        assert!(
            engine
                .receipts
                .contains_key("[\"\\u00e9l\\u00e8ve\\ud83e\\uddd1\",\"\\u00e91\"]")
        );
        let mut restored = FireEngine::restore(engine.snapshot()).unwrap();
        assert_eq!(restored.apply(unicode).unwrap(), original);
    }

    #[test]
    fn invalid_target_and_nonfinite_results_do_not_partially_commit() {
        for mode in ["combined", "accuracy", "retention"] {
            let mut engine = engine(&[("A", "B", 1.0)]);
            engine
                .states
                .get_mut("learner")
                .unwrap()
                .get_mut("B")
                .unwrap()
                .memory_at = 3.0;
            let before = engine.snapshot();
            assert!(
                engine
                    .apply_mode(&event("e", "A", 1.0, true), mode)
                    .is_err()
            );
            assert_eq!(engine.snapshot(), before);
        }
        let mut engine = engine(&[]);
        engine
            .states
            .get_mut("learner")
            .unwrap()
            .get_mut("A")
            .unwrap()
            .set_accuracy(1.0)
            .unwrap();
        let before = engine.snapshot();
        assert!(
            engine
                .apply(Event {
                    quality: 1.7e308,
                    ..event("e", "A", 1.0, true)
                })
                .is_err()
        );
        assert_eq!(engine.snapshot(), before);
    }

    #[test]
    fn restoration_cannot_move_observation_clock_backward() {
        let mut engine = FireEngine::default();
        engine
            .seed(
                "learner",
                "B",
                TopicState {
                    memory_at: 5.0,
                    last_direct_at: Some(6.0),
                    ..TopicState::default()
                },
            )
            .unwrap();
        let mut snapshot = engine.snapshot();
        snapshot["latest"]["learner"] = json!(0);
        let mut restored = FireEngine::restore(snapshot).unwrap();
        assert_eq!(restored.latest["learner"], 6.0);
        assert!(
            restored
                .apply_accuracy(event("old", "A", 1.0, true))
                .is_err()
        );
        let state: TopicState = serde_json::from_value(json!({"ability": {
            "assessment_accuracy": 0.4, "practice_accuracy": 0.4, "practice_mass": 2
        }}))
        .unwrap();
        assert_eq!(state.accuracy(), 0.4);
        assert_eq!(state.evidence_mass(), 2.0);
        assert!(serde_json::from_value::<TopicState>(json!({"accuracy": 0.4})).is_err());
        assert!(serde_json::from_value::<TopicState>(json!({"evidence_mass": 2})).is_err());
    }

    #[test]
    fn missing_assessment_evidence_does_not_borrow_practice_accuracy() {
        let mut engine = FireEngine::new(
            graph(&[]),
            Policy::default(),
            BTreeMap::from([("A".into(), vec!["B".into()])]),
        )
        .unwrap();
        let mut state = TopicState::new(0.4, true);
        state.ability.practice_mass = 1.0;
        engine.seed("learner", "B", state).unwrap();
        engine
            .apply_retention(Event {
                learned: true,
                ..event("learn", "A", 1.0, true)
            })
            .unwrap();
        let state = &engine.states["learner"]["A"];
        assert_eq!(state.expected_assessment_accuracy, Some(0.8));
        assert_eq!(state.expected_practice_accuracy, Some(0.4));
        close(state.accuracy(), 0.6);
        assert!(engine.global_ability.is_empty());
    }

    #[test]
    fn forecasts_use_separate_mass_weighted_direct_prerequisites_and_freeze() {
        let mut engine = FireEngine::new(
            graph(&[]),
            Policy::default(),
            BTreeMap::from([("A".into(), vec!["B".into(), "C".into()])]),
        )
        .unwrap();
        for (topic, assessment, amass, practice, pmass) in [
            ("B", 0.2, 1.0, 0.9, 3.0),
            ("C", 0.8, 3.0, 0.1, 1.0),
            ("D", 1.0, 100.0, 1.0, 100.0),
        ] {
            let mut state = TopicState::new(0.8, true);
            state.ability.assessment_accuracy = assessment;
            state.ability.assessment_mass = amass;
            state.ability.practice_accuracy = practice;
            state.ability.practice_mass = pmass;
            engine.seed("learner", topic, state).unwrap();
        }
        let (assessment, practice) = engine.expected_accuracy("learner", "A");
        close(assessment, 0.65);
        close(practice, 0.7);
        let fallback = engine.expected_accuracy("learner", "other");
        close(fallback.0, 102.6 / 104.0);
        close(fallback.1, 102.8 / 104.0);
        engine
            .apply_accuracy(Event {
                question_results: vec![false],
                ..event("first", "A", 1.0, false)
            })
            .unwrap();
        let initial = engine.states["learner"]["A"].clone();
        assert!(!initial.learned);
        close(initial.expected_assessment_accuracy.unwrap(), 0.65);
        close(initial.expected_practice_accuracy.unwrap(), 0.7);
        close(initial.ability.practice_accuracy, 0.56);
        assert_eq!(initial.ability.practice_mass, 1.0);
        engine
            .apply_accuracy(Event {
                question_results: vec![true],
                ..event("second", "A", 2.0, true)
            })
            .unwrap();
        assert_eq!(
            engine.states["learner"]["A"].expected_practice_accuracy,
            initial.expected_practice_accuracy
        );
        assert_eq!(
            FireEngine::restore(engine.snapshot()).unwrap().states,
            engine.states
        );
    }

    #[test]
    fn memory_order_and_policy_change_are_explicit() {
        let mut standard = engine(&[]);
        let mut literal = standard.clone();
        literal.policy.memory_order = "literal-add-before-decay".into();
        standard.apply(event("e", "A", 1.0, true)).unwrap();
        literal.apply(event("e", "A", 1.0, true)).unwrap();
        assert_eq!(standard.states["learner"]["A"].memory, 1.5);
        assert_eq!(literal.states["learner"]["A"].memory, 1.0);
        standard.policy.base_interval_days = 3.0;
        let interval = standard.states["learner"]["A"].interval_days;
        standard
            .apply_accuracy(event("answer", "A", 2.0, true))
            .unwrap();
        assert_eq!(standard.states["learner"]["A"].interval_days, interval);
        standard
            .apply_retention(event("unit", "A", 3.0, true))
            .unwrap();
        let state = &standard.states["learner"]["A"];
        assert_eq!(
            state.interval_days,
            standard.policy.interval(state.repetitions).unwrap()
        );
    }

    #[test]
    fn rank_is_nonmutating_and_avoids_real_event_ids() {
        let mut engine = engine(&[("A", "B", 1.0), ("A", "C", 1.0)]);
        engine.apply(event("preview:A", "A", 0.0, true)).unwrap();
        engine.apply(event("preview:A:1", "A", 0.0, true)).unwrap();
        let before = engine.snapshot();
        let ranked = engine
            .rank(
                "learner",
                1.0,
                vec![
                    json!({"topic":"A", "expected_minutes":5}),
                    json!({"topic":"B", "expected_minutes":3}),
                ],
            )
            .unwrap();
        assert_eq!(ranked[0]["topic"], "A");
        assert_eq!(ranked[0]["due_removed"], json!(["A", "B", "C"]));
        assert_eq!(engine.snapshot(), before);
        engine.policy.due_threshold = 1e-20;
        engine
            .states
            .get_mut("learner")
            .unwrap()
            .get_mut("A")
            .unwrap()
            .memory = 1e-13;
        assert!(engine.due("learner", 0.0).unwrap().is_empty());
    }
}
