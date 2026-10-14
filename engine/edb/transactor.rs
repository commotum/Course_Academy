//! Durable EDB writer with Course Academy's native schema predicates.
mod answer_fields;
mod configuration;
mod progress;

use edb_core::{
    BackgroundIndexingConfig, LocalTransactionServer, LocalTransportConfig, NativeRegistry,
    RuntimeValue, SemanticError, Symbol, TransactionExecutionOptions, TransactionService,
    TransactionServiceConfig, Value, postgres_config_from_env,
};
use std::{error::Error, io::Write, sync::mpsc, time::Duration};

fn wait_for_stop(stop: &mpsc::Receiver<()>, available: impl Fn() -> bool) -> bool {
    loop {
        if !available() {
            return false;
        }
        match stop.recv_timeout(Duration::from_millis(250)) {
            Ok(()) | Err(mpsc::RecvTimeoutError::Disconnected) => return true,
            Err(mpsc::RecvTimeoutError::Timeout) => {}
        }
    }
}

fn registry() -> Result<NativeRegistry, SemanticError> {
    let mut builder = NativeRegistry::builder();
    builder.entity_predicate(
        Symbol::new("course-academy.topic", "valid-difficulty?"),
        |db, entity, control| {
            control.check(1)?;
            Ok(RuntimeValue::Scalar(Value::Bool(
                configuration::valid_topic_difficulty(db, entity)?,
            )))
        },
    )?;
    builder.entity_predicate(
        Symbol::new("course-academy.policy", "valid?"),
        |db, entity, control| {
            control.check(1)?;
            Ok(RuntimeValue::Scalar(Value::Bool(
                configuration::valid_policy(db, entity)?,
            )))
        },
    )?;
    builder.entity_predicate(
        Symbol::new("course-academy.progress", "valid-profile?"),
        |db, entity, control| {
            control.check(1)?;
            Ok(RuntimeValue::Scalar(Value::Bool(progress::valid_profile(
                db, entity,
            )?)))
        },
    )?;
    builder.entity_predicate(
        Symbol::new("course-academy.progress", "valid-progress?"),
        |db, entity, control| {
            control.check(1)?;
            Ok(RuntimeValue::Scalar(Value::Bool(progress::valid_progress(
                db, entity,
            )?)))
        },
    )?;
    builder.entity_predicate(
        Symbol::new("course-academy.answer-field", "valid?"),
        |db, entity, control| {
            control.check(1)?;
            Ok(RuntimeValue::Scalar(Value::Bool(
                answer_fields::valid_field(db, entity)?,
            )))
        },
    )?;
    Ok(builder.build())
}

fn run() -> Result<(), Box<dyn Error>> {
    let mut args = std::env::args().skip(1);
    let database = args.next().ok_or("usage: transactor DATABASE ENDPOINT")?;
    let endpoint = args.next().ok_or("usage: transactor DATABASE ENDPOINT")?;
    if args.next().is_some() {
        return Err("usage: transactor DATABASE ENDPOINT".into());
    }
    let service = TransactionService::start_with_indexing_and_execution_options(
        TransactionServiceConfig {
            connection: postgres_config_from_env()?,
            database_id: database,
            holder_id: format!("course-academy-{}", std::process::id()),
            lease_duration: Duration::from_secs(5),
            renew_interval: Duration::from_millis(500),
            queue_capacity: 64,
            capacity_limits: Default::default(),
        },
        BackgroundIndexingConfig::default(),
        TransactionExecutionOptions {
            native: registry()?,
            ..Default::default()
        },
    )?;
    let server = LocalTransactionServer::start_at(
        service.client(),
        LocalTransportConfig::default(),
        endpoint,
    )?;
    // Imports below EDB's automatic indexing threshold can still leave a large
    // replay tail on every exact transaction-receipt read. Compact that tail
    // in the normal background indexer when bringing this application online.
    // This is physical maintenance; it does not create a learner transaction.
    let backlog = service.background_indexing_stats();
    if backlog.memory_index_bytes > 1024 * 1024 {
        let requested = service.client().request_index()?;
        println!(
            "INDEX target={} scheduled={} backlog_bytes={}",
            requested.target_t, requested.scheduled, backlog.memory_index_bytes
        );
    }
    println!("READY endpoint={}", server.endpoint().display());
    std::io::stdout().flush()?;
    let (stop_tx, stop_rx) = mpsc::channel();
    std::thread::spawn(move || {
        let mut stop = String::new();
        let _ = std::io::stdin().read_line(&mut stop);
        let _ = stop_tx.send(());
    });
    let clean_stop = wait_for_stop(&stop_rx, || {
        service.client().is_available() && server.is_available()
    });
    if !clean_stop {
        let stats = service.background_indexing_stats();
        for failure in [stats.last_failure, stats.fulltext.last_failure, stats.excision_failure]
            .into_iter().flatten()
        {
            eprintln!("TRANSACTOR_FAILURE category={:?} code={}", failure.category, failure.code);
        }
        eprintln!("TRANSACTOR_UNAVAILABLE code=service/unavailable");
    }
    drop(server);
    service.shutdown();
    if !clean_stop {
        return Err(SemanticError::new(edb_core::ErrorCategory::Unavailable,
            "service/unavailable", "writer lost availability; supervisor must recover it").into());
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unavailable_service_exits_without_waiting_for_stdin() {
        let (_sender, receiver) = mpsc::channel();
        assert!(!wait_for_stop(&receiver, || false));
    }

    #[test]
    fn requested_stop_or_closed_stdin_is_clean() {
        let (sender, receiver) = mpsc::channel();
        sender.send(()).unwrap();
        assert!(wait_for_stop(&receiver, || true));
        let (sender, receiver) = mpsc::channel();
        drop(sender);
        assert!(wait_for_stop(&receiver, || true));
    }
}

fn main() {
    if let Err(error) = run() {
        if let Some(error) = error.downcast_ref::<SemanticError>() {
            eprintln!("ERROR category={:?} code={}", error.category, error.code);
        } else {
            eprintln!("ERROR starting Course Academy EDB transactor: {error}");
        }
        std::process::exit(1);
    }
}
