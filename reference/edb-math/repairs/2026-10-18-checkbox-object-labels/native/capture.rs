//! Read-only exhaustive checkbox census, bounded by native index prefixes.
use edb_core::{Connection, IndexPrefix, Keyword, Value, postgres_config_from_env};
use edb_core::edn::{EdnValue, write_edn};
use edb_core::edn_pull::parse_pull_edn;
use edb_core::edn_value::query_value_to_edn;
use std::{collections::BTreeSet, error::Error, fs, path::Path};
fn main()->Result<(),Box<dyn Error>>{
 let args:Vec<_>=std::env::args().skip(1).collect();
 if args.len()!=2{return Err("usage: capture DIRECTORY AS_OF_BASIS".into())}
 let dir=Path::new(&args[0]);let pinned:u64=args[1].parse()?;
 let conn=Connection::connect_configured(postgres_config_from_env()?,"math",256)?;
 let current=conn.db();if current.basis_t()<pinned{return Err("Basis unavailable".into())}
 let db=current.as_of(pinned);
 let aid=db.entid(&Keyword::new("answer-field","type")).ok_or("Missing type")? as u32;
 let checkbox=db.entid(&Keyword::new("answer-field.type","checkbox")).ok_or("Missing checkbox")?;
 let mut fields=BTreeSet::new();
 for row in db.prefix_cursor(&IndexPrefix::Aevt{attribute:aid,entity:None,value:None})?{
  let d=row?;if d.value==Value::Ref(checkbox){fields.insert(d.entity);}
 }
 let qa=db.entid(&Keyword::new("question","answer-fields")).ok_or("Missing fields")? as u32;
 let mut questions=BTreeSet::new();let mut links=Vec::new();let mut owned=BTreeSet::new();
 for row in db.prefix_cursor(&IndexPrefix::Aevt{attribute:qa,entity:None,value:None})?{
  let d=row?;if let Value::Ref(f)=d.value {if fields.contains(&f){questions.insert(d.entity);owned.insert(f);links.push(EdnValue::Vector(vec![EdnValue::Long(d.entity as i64),EdnValue::Long(f as i64)]));}}
 }
 fs::write(dir.join("checkbox-links.edn"),write_edn(&EdnValue::Vector(links))?+"\n")?;
 fs::write(dir.join("question-ids.json"),format!("{:?}\n",questions.iter().collect::<Vec<_>>()))?;
 fs::write(dir.join("unattached-checkbox-field-ids.json"),format!("{:?}\n",fields.difference(&owned).collect::<Vec<_>>()))?;
 let pattern=parse_pull_edn(&fs::read_to_string(dir.join("question-pull.edn"))?)?;
 for (n,ids) in questions.into_iter().collect::<Vec<_>>().chunks(100).enumerate(){
  let mut rows=Vec::new();
  for id in ids {rows.push(query_value_to_edn(&db.pull(&pattern,*id)?)?);}
  fs::write(dir.join(format!("capture-{n}.edn")),write_edn(&EdnValue::Vector(rows))?+"\n")?;
  println!("Captured chunk {n}: {} questions",ids.len());
 }
 fs::write(dir.join("capture-complete.json"),format!("{{\"basis\":{pinned},\"checkbox_fields\":{},\"completed_to_end\":true,\"database_writes\":0}}\n",fields.len()))?;
 Ok(())
}
