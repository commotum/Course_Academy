//! Replay an exact EDN request and retain structured diagnostics or confirmed receipt.
use edb_core::{Connection,EntityRef,TransactionRequest,postgres_config_from_env};
use edb_core::edn::{EdnValue,write_edn};
use edb_core::edn_value::{edn_keyword,transaction_report_to_edn};
use std::{path::Path,time::Duration};
fn main()->Result<(),Box<dyn std::error::Error>>{
 let args:Vec<_>=std::env::args().skip(1).collect();assert_eq!(args.len(),5);
 let directory=Path::new(&args[0]);let text=std::fs::read_to_string(directory.join("transaction.edn"))?;
 let connection=Connection::connect_configured(postgres_config_from_env()?,"math",128)?;
 // Identical construction to EDB src/bin/edb/data.rs. No explicit time override.
 let request=TransactionRequest::from_edn(&args[1],&text,EntityRef::from_edn(&args[2])?)?.comparing_basis(args[3].parse()?);
 match connection.transact_socket(&args[4],request,Duration::from_secs(180)){
  Ok(commit)=>{
   let mut fields=vec![(edn_keyword("edb","committed"),EdnValue::Bool(true)),(edn_keyword("edb","basis-t"),EdnValue::Long(i64::try_from(commit.basis_t)?)),(edn_keyword("edb","replayed"),EdnValue::Bool(commit.replayed)),(edn_keyword("edb","tx-hash"),EdnValue::String(commit.tx_hash.iter().map(|b|format!("{b:02x}")).collect()))];
   // Preserve confirmation before opening/rendering a report.
   std::fs::write(directory.join("confirmed-reconciliation.edn"),write_edn(&EdnValue::Map(fields.clone()))?+"\n")?;
   match commit.report{
    Ok(report)=>{let EdnValue::Map(data)=transaction_report_to_edn(report.db_before.basis_t(),report.db_after.basis_t(),&report.tx_data,&report.tempids)?else{unreachable!()};fields.extend(data);std::fs::write(directory.join("commit.edn"),write_edn(&EdnValue::Map(fields))?+"\n")?;println!("EXACT_REQUEST_COMMITTED {}",commit.basis_t);},
    Err(error)=>{println!("COMMIT_CONFIRMED_REPORT_ERROR {}",error.code);}
   }
  },
  Err(error)=>{
   let fields=vec![(edn_keyword("diagnostic","category"),EdnValue::String(format!("{:?}",error.category))),(edn_keyword("diagnostic","code"),EdnValue::String(error.code.into())),(edn_keyword("diagnostic","message"),EdnValue::String(error.message)),(edn_keyword("diagnostic","details"),EdnValue::Map(error.details.into_iter().map(|(k,v)|(EdnValue::String(k),EdnValue::String(v))).collect()))];
   let value=write_edn(&EdnValue::Map(fields))?;std::fs::write(directory.join("native-reconciliation-error.edn"),value.clone()+"\n")?;println!("{value}");
  }
 }
 Ok(())
}
