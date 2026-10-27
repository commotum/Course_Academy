//! Defaults until the learner saves a Focused mode preference in their profile.
pub const FOCUSED_MODE: bool = true;

pub const TARGET_PREREQUISITE_DEPTH: usize = if FOCUSED_MODE { 0 } else { 2 };
