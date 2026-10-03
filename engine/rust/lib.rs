//! Course Academy's FIRe retention model and activity completion engine.
pub type Result<T> = std::result::Result<T, String>;

pub mod activities;
pub mod calibration;
pub mod core;
pub mod graph_snapshots;
pub mod history;
pub mod learning;
pub mod live_history;
pub mod question_selection;
pub mod replay;
pub mod runtime;
pub mod schema;
pub mod timing;
pub mod wire;
