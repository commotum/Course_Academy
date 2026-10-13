# Native grading observations

The final harness checks every selected radio UUID, canonical blank fragments, independently unreduced termwise derivative/evaluation expressions, correct equivalent blank aliases, and incorrect fragments. It uses the real `course_academy_engine::learning::grade_field` with memory-only fixtures.

An exploratory alternate entry for the linear blank included `12*(1*x^0)`. The native grader returned `answer comparison has unresolved domain differences`: the expression introduces a possible zero-to-zero-power domain issue at x=0. Final alternate entries use the ordinary derivative of x, namely 1, and preserve unreduced coefficient/formula operations for the remaining terms. The generator never displays x^0 in a derivative answer. This exploratory result is not counted as an accepted equivalent-entry test or a final unresolved check.

The stale q-340280 alias `5^x ln(5)−18x²+4` is a complete derivative, whereas the field asks for slope at zero. It is explicitly rejected by the native grader and excluded from normal banks. Its exact original value remains replayable under observed/raw_source profiles.

The captured q-17388 malformed formal dy/dx notation is repaired in normal worked solutions. Worked solutions are independently checked from printed stages; radio selection grading alone cannot detect that defect.
