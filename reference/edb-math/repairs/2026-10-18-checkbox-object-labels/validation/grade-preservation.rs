//! Read-only before/after grading of existing checkbox identities.
use course_academy_engine::{learning, schema::{EntitySnapshot, Record}};
use serde_json::{Value, json};
use std::{collections::BTreeMap, error::Error, fs};

fn ident(v: &Value) -> Result<String, Box<dyn Error>> {
    Ok(v.as_str().or_else(|| v[":db/ident"].as_str()).ok_or("ident required")?.trim_start_matches(':').to_owned())
}
fn eid(v: &Value) -> Result<u64, Box<dyn Error>> {
    Ok(v.as_u64().or_else(|| v[":db/id"].as_u64()).ok_or("entity id required")?)
}
fn record(v: Value) -> Record { v.as_object().unwrap().clone() }
fn snapshot(q: &Value) -> Result<EntitySnapshot, Box<dyn Error>> {
    let mut entities = BTreeMap::new();
    entities.insert(1,record(json!({"db/ident":"answer-field.type/checkbox"})));
    entities.insert(2,record(json!({"db/ident":"answer.type/text"})));
    let mut fields = vec![];
    let qid=eid(q)?;
    // Enum idents are accepted directly by EntitySnapshot, as in the application fixtures.
    for f in q[":question/answer-fields"].as_array().ok_or("fields required")? {
        let fid=eid(f)?; fields.push(fid); let mut answers=vec![];
        for a in f[":answer-field/choices"].as_array().ok_or("choices required")? {
            let aid=eid(a)?; answers.push(aid);
            entities.insert(aid, record(json!({"answer/type": ident(&a[":answer/type"])?, "answer/value": a[":answer/value"]})));
        }
        entities.insert(fid, record(json!({"answer-field/key":f[":answer-field/key"],
            "answer-field/type":ident(&f[":answer-field/type"])?, "answer-field/choices":answers,
            "answer-field/correct":eid(&f[":answer-field/correct"])?})));
    }
    entities.insert(qid, record(json!({"question/id":q[":question/id"], "question/problem":q[":question/problem"], "question/answer-fields":fields})));
    // Grading uses the question's KP title as optional context; label-only repairs do not change it.
    let kp=q[":knowledge-point/_questions"].as_array().and_then(|v|v.first())
        .or_else(||q[":knowledge-point/_canonical-example"].as_array().and_then(|v|v.first()));
    if let Some(kp)=kp {
        entities.insert(eid(kp)?, record(json!({"knowledge-point/title":kp[":knowledge-point/title"], "knowledge-point/questions":[qid]})));
    }
    Ok(EntitySnapshot::new(entities,0)?)
}
fn grade(s:&EntitySnapshot, q:u64, responses:&BTreeMap<u64,String>)->Value {
    match learning::grade(s,q,responses) {Ok(v)=>json!({"grade":v}),Err(e)=>json!({"error":e})}
}
fn main()->Result<(),Box<dyn Error>> {
    let args:Vec<_>=std::env::args().skip(1).collect();
    if args.len()!=2 {return Err("usage: grade-preservation INPUT.json REPORT.json".into())}
    let document:Value=serde_json::from_str(&fs::read_to_string(&args[0])?)?;
    let mut report=vec![];let (mut subsets,mut flips,mut saved)=(0usize,0usize,0usize);
    for case in document["cases"].as_array().ok_or("cases required")? {
        let before=&case["before"];let after=&case["after"];let qid=eid(before)?;
        let b=snapshot(before)?;let a=snapshot(after)?;
        let mut fields=before[":question/answer-fields"].as_array().ok_or("fields")?.iter().collect::<Vec<_>>();
        fields.sort_by_key(|f|eid(f).unwrap());
        if fields.iter().any(|f|ident(&f[":answer-field/type"]).unwrap()!="answer-field.type/checkbox") {
            return Err(format!("{qid}: expected pure checkbox question").into());
        }
        let canonical:BTreeMap<_,_>=fields.iter().map(|f|Ok((eid(f)?,eid(&f[":answer-field/correct"])?.to_string()))).collect::<Result<_,Box<dyn Error>>>()?;
        let accepted=json!({"grade":true});let rejected=json!({"grade":false});
        if grade(&b,qid,&canonical)!=accepted || grade(&a,qid,&canonical)!=accepted {return Err(format!("{qid}: canonical rejected: before {}; after {}",grade(&b,qid,&canonical),grade(&a,qid,&canonical)).into())}
        for f in &fields {
            let fid=eid(f)?;let wrong=f[":answer-field/choices"].as_array().unwrap().iter().find(|x|eid(x).unwrap().to_string()!=canonical[&fid]).ok_or("wrong choice missing")?;
            let mut response=canonical.clone();response.insert(fid,eid(wrong)?.to_string());
            if grade(&b,qid,&response)!=rejected || grade(&a,qid,&response)!=rejected {return Err(format!("{qid}: flipped checkbox accepted").into())}
            flips+=1;
        }
        let mut missing=canonical.clone();missing.remove(&eid(fields[0])?);
        if grade(&b,qid,&missing)["error"].is_null() || grade(&a,qid,&missing)!=grade(&b,qid,&missing) {return Err(format!("{qid}: incomplete grading changed").into())}
        let total=if fields.len()<=12 {1usize<<fields.len()}else{0};
        for mask in 0..total {
            let responses=fields.iter().enumerate().map(|(i,f)| {
                let value=if (mask>>i)&1==1 {"true"}else{"false"};
                let ans=f[":answer-field/choices"].as_array().unwrap().iter().find(|x|x[":answer/value"]==value).unwrap();
                (eid(f).unwrap(),eid(ans).unwrap().to_string())
            }).collect();
            let expected=json!({"grade":responses==canonical});
            if grade(&b,qid,&responses)!=expected || grade(&a,qid,&responses)!=expected {return Err(format!("{qid}: subset {mask} changed").into())}
            subsets+=1;
        }
        let mut saved_reports=vec![];
        for item in case["saved_responses"].as_array().ok_or("saved_responses required")? {
            let mut response=BTreeMap::new();
            for pair in item["responses"].as_array().ok_or("responses required")? {
                response.insert(pair[0].as_u64().ok_or("field id")?,pair[1].as_u64().ok_or("answer id")?.to_string());
            }
            let old=grade(&b,qid,&response);let new=grade(&a,qid,&response);
            if old!=new {return Err(format!("{qid}: saved response {} changed",item["item"]).into())}
            saved_reports.push(json!({"item":item["item"],"before":old,"after":new}));saved+=1;
        }
        report.push(json!({"question":qid,"fields":fields.len(),"exhaustive_subsets":total,
            "canonical_accepted":true,"single_flips_rejected":fields.len(),"incomplete_rejected":true,"saved_responses":saved_reports}));
    }
    fs::write(&args[1],serde_json::to_string_pretty(&json!({"passed":true,"database_writes":0,
        "entry_point":"course_academy_engine::learning::grade", "questions":report.len(),
        "exhaustive_subsets":subsets,"single_flips":flips,"saved_responses":saved,"cases":report}))?+"\n")?;
    println!("Native grading preserved: {} subsets, {} flips, {} saved responses",subsets,flips,saved);
    Ok(())
}
