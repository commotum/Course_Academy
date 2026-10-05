//! Isolated API evaluation; not the production answer checker.
use mathcore::{Expr, MathCore};
use serde_json::{Value, json};
use std::{collections::HashMap, fs, time::Instant};

fn output(result: Result<Expr, mathcore::MathError>) -> Value {
    match result {
        Ok(e) => json!({"ok":true,"display":e.to_string(),"ast":format!("{e:?}"),"is_zero":e.is_zero()}),
        Err(e) => json!({"ok":false,"error":e.to_string()}),
    }
}

fn main() {
    let args: Vec<_> = std::env::args().collect();
    let input: Value = serde_json::from_str(&fs::read_to_string(&args[1]).unwrap()).unwrap();
    let math = MathCore::new();
    let start = Instant::now();
    let mut fields = vec![];
    for f in input["fields"].as_array().unwrap() {
        let mut row = f.clone();
        row["raw_parse"] = output(MathCore::parse(f["original"].as_str().unwrap()));
        if let Some(expression) = f["adapted"].as_str() {
            let vars: HashMap<String, f64> = f["variables"].as_array().unwrap().iter().enumerate()
                .map(|(i,v)| (v.as_str().unwrap().to_owned(), 1.37 + i as f64 * 0.173)).collect();
            row["adapted_parse"] = output(MathCore::parse(expression));
            row["adapted_simplify"] = output(MathCore::simplify(expression));
            row["sample_substitution"] = json!(vars);
            row["sample_evaluation"] = match math.evaluate_with_vars(expression, &vars) {
                Ok(value) => json!({"ok":true,"value":value}),
                Err(e) => json!({"ok":false,"error":e.to_string()}),
            };
        }
        fields.push(row);
    }
    let mut pairs = vec![];
    for p in input["pairs"].as_array().unwrap() {
        let mut row = p.clone();
        let (a,b) = (p["a"].as_str().unwrap(),p["b"].as_str().unwrap());
        let left = MathCore::simplify(a);
        let right = MathCore::simplify(b);
        // Expr lacks PartialEq; debug AST comparison is for this probe only.
        let same = matches!((&left,&right), (Ok(l),Ok(r)) if format!("{l:?}") == format!("{r:?}"));
        let difference = MathCore::simplify(&format!("({a})-({b})"));
        let zero = matches!(&difference, Ok(e) if e.is_zero());
        row["left_simplified"] = output(left);
        row["right_simplified"] = output(right);
        row["difference_simplified"] = output(difference);
        row["simplified_ast_equal"] = json!(same);
        row["difference_is_zero"] = json!(zero);
        row["combined_verdict"] = json!(same || zero);
        pairs.push(row);
    }
    let behavior: Vec<_> = input["behavior"].as_array().unwrap().iter().map(|p| {
        let expression = p["expression"].as_str().unwrap();
        let vars: HashMap<String, f64> = serde_json::from_value(p["variables"].clone()).unwrap();
        json!({"label":p["label"],"expression":expression,"variables":vars,
            "parsed":output(MathCore::parse(expression)),
            "simplified":output(MathCore::simplify(expression)),
            "evaluated":match math.evaluate_with_vars(expression,&vars) {
                Ok(value)=>json!({"ok":true,"value":value}),
                Err(e)=>json!({"ok":false,"error":e.to_string()}),
            }})
    }).collect();
    let result = json!({"mathcore_version":"0.3.1","fields":fields,"pairs":pairs,"behavior":behavior,
        "elapsed_microseconds":start.elapsed().as_micros(),"database_writes":0,"engine_changes":false});
    fs::write(&args[2],serde_json::to_string_pretty(&result).unwrap()+"\n").unwrap();
}
