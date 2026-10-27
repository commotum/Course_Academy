//! Application policy, changed in code and applied when the app captures data.
//! Restart the study service after changing this switch.
pub const FOCUSED_MODE: bool = true;

pub const TARGET_PREREQUISITE_DEPTH: usize = if FOCUSED_MODE { 0 } else { 2 };
