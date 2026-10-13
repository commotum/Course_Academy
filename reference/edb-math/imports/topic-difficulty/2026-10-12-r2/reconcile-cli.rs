// Use the ordinary CLI request encoding; expose only the remote semantic code.
#[path = "/home/jake/Developer/EDB/src/bin/edb/data.rs"]
mod data;
fn transaction_defaults(partition: Option<&str>) -> Result<edb_core::TransactionDefaults, edb_core::SemanticError> {
    assert!(partition.is_none());
    Ok(Default::default())
}
fn main() {
    let raw: Vec<String> = std::env::args().skip(1).collect();
    assert_eq!(raw.first().map(String::as_str), Some("transact"));
    match data::dispatch(&raw).unwrap() {
        Ok(()) => (),
        Err(error) => {
            eprintln!("ERROR category={:?} code={}", error.category, error.code);
            if let Some(code) = error.details.get("remote_code") {
                if code.bytes().all(|b| b.is_ascii_alphanumeric() || b"/-_.".contains(&b)) {
                    eprintln!("remote_code={code}");
                }
            }
            std::process::exit(1);
        }
    }
}
