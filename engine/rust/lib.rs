//! Course Academy's FIRe retention model and activity completion engine.
pub type Result<T> = std::result::Result<T, String>;

pub mod activities;
pub mod base_xp;
pub mod calibration;
pub mod core;
pub mod graph_snapshots;
pub mod history;
pub mod learning;
pub mod live_history;
pub mod question_selection;
pub mod replay;
pub mod retrieval;
pub mod runtime;
pub mod scheduling;
pub mod study_mode;
pub mod assessment_sampling;
pub mod inventory;
pub mod schema;
pub mod symbolic;
pub mod timing;
pub mod wire;

mod set_answers;
