//! JSON replay inputs and the published encompassing example.
use crate::{
    Result,
    core::{Edge, EncompassingGraph, Event, FireEngine, Policy, TopicState},
};
use serde::Deserialize;
use serde_json::{Value, json};
use std::collections::{BTreeMap, BTreeSet};

pub fn replay(data: Value) -> Result<Value> {
    #[derive(Deserialize)]
    struct Seed {
        learner: String,
        topic: String,
        state: TopicState,
    }
    #[derive(Deserialize)]
    #[serde(default)]
    struct Input {
        edges: Vec<Edge>,
        topics: BTreeSet<String>,
        policy: Policy,
        difficulty_accuracy: Option<BTreeMap<String, f64>>,
        neighborhoods: Option<BTreeMap<String, Vec<String>>>,
        initial_states: Vec<Seed>,
        events: Vec<Event>,
        assumptions: Value,
    }
    impl Default for Input {
        fn default() -> Self {
            Self {
                edges: vec![],
                topics: BTreeSet::new(),
                policy: Policy::default(),
                difficulty_accuracy: None,
                neighborhoods: None,
                initial_states: vec![],
                events: vec![],
                assumptions: json!([]),
            }
        }
    }
    let input: Input = serde_json::from_value(data).map_err(|e| e.to_string())?;
    let mut engine = FireEngine::new(
        EncompassingGraph::new(input.edges, input.topics)?,
        input.policy,
        input.difficulty_accuracy.unwrap_or_default(),
        input.neighborhoods.unwrap_or_default(),
    )?;
    for seed in input.initial_states {
        engine.seed(&seed.learner, &seed.topic, seed.state)?;
    }
    let mut receipts = vec![];
    for event in input.events {
        receipts.push(engine.apply(event)?);
    }
    Ok(json!({"assumptions": input.assumptions,
        "receipts": receipts, "snapshot": engine.snapshot()}))
}

pub fn demo() -> Result<Value> {
    let edges = vec![
        Edge::new("two-digit-multiplication", "one-digit-multiplication", 1.0)?,
        Edge::new("two-digit-multiplication", "addition", 1.0)?,
    ];
    let mut engine = FireEngine::new(
        EncompassingGraph::new(edges.clone(), BTreeSet::new())?,
        Policy::default(),
        BTreeMap::new(),
        BTreeMap::new(),
    )?;
    for topic in engine.graph.topics.clone() {
        engine.seed("demo", &topic, TopicState::default())?;
    }
    let before = engine.due("demo", 1.0)?;
    let ranking = engine.rank(
        "demo",
        1.0,
        vec![
            json!({"topic":"two-digit-multiplication", "expected_minutes":5}),
            json!({"topic":"one-digit-multiplication", "expected_minutes":4}),
            json!({"topic":"addition", "expected_minutes":4}),
        ],
    )?;
    let event = Event {
        id: "demo-review".into(),
        learner: "demo".into(),
        topic: "two-digit-multiplication".into(),
        at: 1.0,
        question_results: vec![true, true, true],
        source: "student-selected".into(),
        ..Event::default()
    };
    let receipt = engine.apply(event.clone())?;
    let mut slow = FireEngine::new(
        EncompassingGraph::new(edges.clone(), BTreeSet::new())?,
        Policy::default(),
        BTreeMap::new(),
        BTreeMap::new(),
    )?;
    for topic in slow.graph.topics.clone() {
        slow.seed(
            "demo",
            &topic,
            TopicState::new(if topic == "addition" { 0.4 } else { 0.8 }, true),
        )?;
    }
    let slow_receipt = slow.apply(Event {
        id: "slow-review".into(),
        question_results: vec![],
        source: "direct".into(),
        ..event
    })?;
    Ok(
        json!({"description": "Published encompassing example under our assumed numeric policy; not a fitted MA schedule.",
        "policy": engine.policy, "edges": edges, "due_before": before, "ranking": ranking, "receipt": receipt,
        "due_after": engine.due("demo", 1.0)?,
        "slow_component": {"receipt": slow_receipt, "due_after": slow.due("demo", 1.0)?}}),
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn demo_and_replay_use_full_engine() {
        let output = demo().unwrap();
        assert_eq!(output["due_after"], json!([]));
        assert_eq!(output["slow_component"]["due_after"], json!(["addition"]));
        let output = replay(json!({"topics":["A","B","isolated"], "neighborhoods":{"A":["B"]},
            "initial_states":[{"learner":"learner","topic":"B","state":{"ability":{
                "assessment_accuracy":0.4,"practice_accuracy":0.4,"practice_mass":1
            }}}],
            "events":[{"id":"learn","learner":"learner","topic":"A","at":1,"passed":true,"kind":"lesson","learned":true}]})).unwrap();
        assert_eq!(output["snapshot"]["topics"], json!(["A", "B", "isolated"]));
        assert_eq!(output["receipts"].as_array().unwrap().len(), 1);
        assert!(
            output["snapshot"]["states"]["learner"]["A"]["learned"]
                .as_bool()
                .unwrap()
        );
    }
}
