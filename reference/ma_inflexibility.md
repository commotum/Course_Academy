# Math Academy's Inflexibility for Students in Formal Coursework

Date: September 26, 2026

## The problem

Math Academy is an excellent learning system, but its prescribed curriculum and study route can conflict with a student's immediate academic needs. A student enrolled in school has an external schedule: lectures, assignments, quizzes, and exams determine which skills matter this week. The learning system needs to accommodate that schedule while still helping the student build the prerequisites required to succeed.

These observations record Jake's reported experience with Math Academy and the needs motivating Course Academy, particularly from the perspective of an electrical engineering student.

The central limitation is that personalization through an initial diagnostic does not provide enough ongoing control over what the student studies. Knowing a student's starting point and responding to their changing priorities are separate requirements.

## Course scope does not necessarily match school

A school course may cover only a small portion of the topics in the closest Math Academy course. Enrolling in the broader course does not give the student a study plan tailored to the actual material their instructor will teach and assess.

The student needs to be able to select the relevant topics and include the prerequisites necessary to learn them. Other material may be valuable, but its value does not automatically make it a priority during a busy academic term.

The reverse mismatch also matters: Math Academy may not contain all the topics required by a particular course or program. A student's academic needs can cross the boundaries of the available courses or extend beyond the content library altogether.

For electrical engineering, this is especially significant. The program spans mathematical methods, computation, and engineering-specific concepts and applications. A study system must support the material the program actually requires, including topics for which no equivalent Math Academy lesson exists.

## The prescribed route can conflict with immediate priorities

Consider a student who has five assignments involving u-substitution in the coming week. They want to work on that lesson now, but the system continues serving lessons or reviews that are less relevant to those assignments.

Suppose the student is missing only two or three prerequisites for the u-substitution lesson. A useful response would be to identify those gaps, help the student close them, and then make the target lesson available. The student needs a way to express that priority and have it affect the route through the material.

In Jake's experience, Math Academy does not provide that level of control. The prescribed route governs what comes next, even when the student has a specific, time-sensitive reason to study another reachable topic.

Prerequisites still matter. The desired flexibility is to choose a destination and receive an appropriate route to it. Urgency should influence which prerequisite chain receives attention, while the system remains honest about what the student needs to know first.

## Several active school courses need simultaneous support

During fall quarter, Jake will take all three of these courses at the same time:

- Vector Calculus II
- Applied Differential Equations
- Linear Algebra

Each course will have its own pace, assignments, and assessments. A useful study system must let all three remain active and allow attention to shift among them as demands change.

Jake reports that Math Academy does not let him enroll in three courses simultaneously or direct his studies across them in this way. A single prescribed course route therefore does not reflect his actual academic workload.

The student needs one view of their learning that can accommodate several concurrent courses. Where those courses share prerequisite knowledge, prior learning should carry across them. Where they require different material, each should retain its own scope and priorities.

## Student agency must continue after the diagnostic

The diagnostic can establish what a student already knows. During the term, the student also needs to communicate changing goals:

- “This assignment requires u-substitution. Help me prepare for it.”
- “Show me the prerequisites I am missing for this lesson.”
- “My school course covers these topics. Build my study scope around them.”
- “I have an assessment in differential equations this week. Prioritize the relevant material.”
- “This engineering topic is missing from the library. I still need instruction and practice for it.”
- “Keep my calculus, differential equations, and linear algebra courses active together.”

These requests provide information that a starting diagnostic cannot capture. Effective personalization needs both knowledge of the student's readiness and knowledge of their current academic obligations.

## Consequences for the student

When the study route cannot respond to those obligations, the student must spend limited time reconciling two schedules: the system's sequence and the school's sequence. Progress in the system may leave an immediate assignment need unresolved.

The student also has to identify useful material outside the prescribed route, fill gaps in topic coverage, and coordinate several subjects manually. That adds planning work precisely when the student needs to concentrate on learning and completing coursework.

For an electrical engineering student taking several demanding mathematical courses together, the ability to choose priorities is a practical requirement.

## Requirements motivating Course Academy

The following requirements follow from this problem statement:

| Need | Desired behavior |
|---|---|
| Match a school's actual curriculum | Select a relevant subset of topics and include the prerequisites needed to support it. |
| Respond to current assignments | Let the student prioritize a target skill or lesson based on immediate coursework. |
| Respect prerequisite readiness | Identify and teach missing prerequisites on the path to the selected target. |
| Support concurrent enrollment | Maintain several active courses and allow priorities to shift among them. |
| Cover program-specific gaps | Add suitable instruction and practice when the existing library lacks a required topic. |
| Reuse shared learning | Recognize knowledge that serves more than one course. |
| Preserve ongoing student control | Accept updated goals and obligations throughout the term. |

The goal is to preserve the quality of focused instruction, staged examples, and closely matched practice while allowing the student to direct the scope and timing of their studies. The student should be able to name what they need to learn, and the system should help them become ready to learn it.

## Relationship to the earlier technical reviews

[skills_v1.md](skills_v1.md) describes an assignment-driven workflow that finds equivalent existing lessons and generates focused instruction for uncovered problems. That workflow begins to address the need to connect learning directly to current coursework.

[skills_vs_ece_pipeline.md](skills_vs_ece_pipeline.md) compares that workflow with a larger curriculum-generation pipeline. It identifies capabilities for building missing lesson content and the integration work needed to connect generated material to a usable study environment.

Those mechanisms support parts of the proposed solution. The broader product problem is how to combine topic coverage, prerequisite readiness, concurrent courses, and student-selected priorities into a coherent learning experience.
