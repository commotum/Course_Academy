## FAQ: Diagnostics and Curriculum

**Summary:** (in progress)

## Diagnostics

> Is there anything that I should keep in mind while taking the diagnostic to ensure that I get an accurate placement?

This diagnostic assesses your problem-solving speed and comfort. Be honest about your abilities to ensure an accurate, personalized learning path. The aim is finding your ideal starting point, not achieving a high score.

#### Do:

- Complete within 1-2 days. (It's fine to take breaks.)
- Take when well-rested and focused.
- Skip questions you can't solve quickly (3 minutes max). If you can't solve the question quickly and comfortably, click "I don't know."

#### Don't:

- Drag it out over many days.
- Take it when tired. (This leads to mistakes.)
- Guess, not even if you can narrow down answer choices. (A successful guess may cause you to be placed too far.)
- Attempt questions that are beyond your level of comfort. (Lengthy answer times, even if correct, will receive minimal credit and inflate the length of the diagnostic.)
- Use any external resources.

Remember, we're trying to determine what you can do comfortably and confidently, not what you can barely manage with extended effort.

Young students may require parental supervision to ensure they are following the guidelines above. However, the parent should not provide any information on how to solve problems or even comment on the correctness of answers.

Don't worry if your diagnostic performance differs from expectations. Even students with good grades may have knowledge gaps, as traditional courses often lack comprehensiveness and allow students to get by without truly mastering the material.

Any knowledge gaps identified by the diagnostic will be automatically incorporated into your personalized learning plan, ensuring that you build a solid foundation for your mathematical journey.

> There were way more questions than I expected on the diagnostic!

As discussed in [Chapter 30](../../V-TECHNICAL-DEEP-DIVES/30-Technical-Deep-Dive-on-Diagnostic-Exams/30-Technical-Deep-Dive-on-Diagnostic-Exams.md), diagnostics require a larger-than-expected number of questions because

1. our curriculum is hyper-scaffolded, and
2. we assess students not only on the course content, but also on any lower-level foundations they might be missing.

For higher-level math courses, diagnostics may need to assess your knowledge of over 1,000 math topics! Even if it feels like there are many questions on the diagnostic, each individual question provides decisive information about your knowledge of about 10 different topics on average.

Think of it like going to a serious gym where you start with a body composition analysis and strength/flexibility tests at every muscle/joint in your body. In order to get you progressing towards your mathematical goals as efficiently as possible, we need to figure out exactly where your strengths and weaknesses are so that we can perfectly calibrate your workouts to your personal needs.

Of course, if you just want to go to the gym on weekends and walk around the track a few times, then this is probably not a great fit! But if you want to come for a serious workout most days each week and reach a serious level of fitness as quickly as possible, then this is the way to do it.

> Can't you improve the diagnostic algorithm to cut down on the number of questions?

We have spent a lot of time optimizing our diagnostic algorithm to be as quick and efficient as possible. There are some hard limits in the physics of how small we can reduce the number of diagnostic questions subject to additional constraints on the precision and robustness of the overall conclusions drawn from that information. Our diagnostics are optimized to the point that if we forcibly cut the number of questions in half, your placement wouldn't match up well enough with your true knowledge frontier, and you'd get frustrated doing tasks that are too easy (or worse, too hard).

Yes, people quit if the diagnostic is too long, but they also quit if they're not placed accurately. Math Academy's approach to that tradeoff caters to students who are serious about putting in a large amount of work to learn an even larger amount of math. For such users, an hour or two on the diagnostic is proportionally negligible compared to the amount of work that they plan to commit to learning math. Such users typically find it worthwhile to spend a proportionally tiny amount of extra time at the beginning to ensure a smooth mathematical journey indefinitely into the future.

> I am being served lower-grade lessons that feel irrelevant to my course, and it's taking too long to make progress in my course. What can I do to fix this?

The only time you'd be assigned a lower-course topic is when it's a prerequisite of a topic in the course that you're taking and you got it (or one of its prerequisites) incorrect on the diagnostic. In order to place out of these topics, you would need to provide evidence of being able to solve them (or post-requisite topics) on the diagnostic.

Sometimes, students think that topics are irrelevant to their current course when in fact they are necessary prerequisites. For example, integration might not seem relevant to linear algebra but it's actually necessary to solve problems in inner product spaces. Likewise, the rational roots theorem, synthetic division, and polynomial factoring might not seem relevant but it's actually necessary to compute eigenvalues of 3x3 matrices.

If you think you could have done better on the diagnostic, it would be worth retaking it very carefully. Keep in mind that all the system's decisions are based on your demonstrated ability to solve problems, and it is not uncommon for students to take courses elsewhere yet still not have mastered the content well enough to solve problems correctly, consistently, and in a timely manner.

> I missed some questions on the diagnostic, but I know those topics, I swear! Can't you just give me credit for them?

You are welcome to take another diagnostic and attempt to demonstrate your knowledge by solving problems correctly! Math Academy is a mastery learning system, so the only way to receive credit for topics is to provide evidence of mastery, i.e., to demonstrate your ability to solve the problems correctly. If you miss questions on the diagnostic, the system is going to infer that you don't know those topics (and any topics that depend on them), regardless of how well you think you know them.

> There is a topic that I know how to do, but the diagnostic didn't ask me about it and I didn't get credit for it.

The diagnostic is fully comprehensive; it continues asking questions until it has evidence of knowledge (or lack of knowledge) for every single topic in the student's course and foundations. Whatever topics the student is not given credit for, it's because the student submitted incorrect answers on those topics or their prerequisites. While it is *sometimes possible* to solve questions from a topic despite not fully grasping a prerequisite, this indicates the presence of "holes" in the student's mathematical knowledge, and the diagnostic intentionally places students at the bottom of their lowest knowledge holes so that these holes can be filled in.

Placing students at the bottom of their lowest knowledge holes is absolutely critical to ensure student success. If the diagnostic did the opposite, placing students at the *top* of their *highest* knowledge holes, then students might initially feel like they are closer to their goals as a result of receiving more credit, but these knowledge holes would sooner or later (and likely sooner) derail the student by causing them to become "stuck" while learning new topics that make deeper use of the prerequisite knowledge.

That said, it is not uncommon for adult students to be extremely rusty on their math while taking the initial diagnostic, and then have an outsized portion of their memory come rushing back afterwards as they complete learning tasks. When this happens, it is sometimes possible for a student to place significantly further by retaking the diagnostic.

Additionally, we are working on a button where students can say "I already know this" on any lesson that they receive and evidence their knowledge by answering a couple advanced questions on the topic. That way, it will be fast and easy for a student to continue fine-tuning their knowledge profile after the diagnostic.

> There's a question on the diagnostic that I might know how to solve, but I want to re-learn it from scratch. I don't want to receive credit for it. What should I do?

In general, if you answer a question correctly in a diagnostic, you will likely get credit for it. If you are not comfortable with the question and do not want credit, then what you should do is click the "I don't know" button.

> After the diagnostic, what if I am asked to complete a lesson for which I have not learned a prerequisite?

Math Academy's diagnostic exam is highly accurate, but not necessarily 100% perfect, as guaranteeing a 100% perfect placement would require an infeasibly large number of diagnostic questions to be answered. To drastically cut down on the number of questions, our diagnostic exam leverages some loose forms of inference that, rarely but occasionally, may place a student slightly behind or ahead (but more likely behind) their true knowledge frontier along some learning path.

(For instance, if a student answers a question correctly on a "leaf topic" in some module, then we treat that question as a "representative" for the module and award some credit to other leaf topics in the same module. Otherwise the diagnostic would have to explicitly assess every single leaf topic, which would make the number of questions blow up. The idea is that if a student knows a maximally advanced technique within some cohesive group of topics, then they probably know any other advanced techniques within that group, or they should have enough prior knowledge to brush up on the fly.)

In practice, on the rare occasion that a student's level of knowledge is overestimated and they receive a lesson for which they have not learned a prerequisite, the degree of overestimation is small enough that the student is able to learn the prerequisite by clicking on the prerequisite and viewing its lesson in reference mode. To the best of our knowledge, there has never been an instance where a student was unable to do so, provided that they took the diagnostic properly and submitted answers reflective of their true knowledge. (In the small number of instances where a student was placed too far beyond their true knowledge to make progress on the system, it has always turned out that the student used an external resource for help during the diagnostic.)

Additionally, even on the rare occasion that a student may have to learn a prerequisite by viewing its lesson in reference mode, this issue will quickly disappear as the student completes more work on the system: the student will quickly reach a point where, for all their available lessons, they have explicitly completed lessons on all the prerequisites.

> After the diagnostic, why did failing a single task bring my progress down multiple percent?

After the diagnostic, there may be pockets of math where the system infers student knowledge but has low confidence in that inference. As the student completes learning tasks, the system will adapt more quickly to the student's performance in these areas of low confidence. As discussed in [Chapter 30](../../V-TECHNICAL-DEEP-DIVES/30-Technical-Deep-Dive-on-Diagnostic-Exams/30-Technical-Deep-Dive-on-Diagnostic-Exams.md), these topics are called "conditionally completed" because while the student (just barely) received credit for them based on the diagnostic, retaining this credit is conditional on the student passing tasks that assume knowledge of these topics.

If a student fails a task on a conditionally completed topic, then the system reasons as follows:

Wait, we thought they knew that topic and some more advanced topics that build on it, but they just barely placed out of those topics on the diagnostic, so the fact that they're struggling indicates that they probably don't actually know it. Time to revise our earlier decision and remove the credit we originally awarded.

This mechanism may be subtle in tasks like multisteps and quizzes, where every question is linked to a different topic, because a student may lose credit for a particular topic (from incorrectly answering a question linked to that topic) while gaining credit for other topics (from correctly answering questions linked to other topics) and passing the task overall.

> Why haven't I gotten a supplemental diagnostic to place out of more material? I'm doing really well on my tasks.

As described in [Chapter 30](../../V-TECHNICAL-DEEP-DIVES/30-Technical-Deep-Dive-on-Diagnostic-Exams/30-Technical-Deep-Dive-on-Diagnostic-Exams.md), supplemental diagnostics have nothing to do with student performance. Their purpose is to provide the system with missing information if the knowledge graph shifts around a bit. Students are expected to see supplemental diagnostics rarely if at all.

The original diagnostic exam makes a lot of inferences depending on the structure of the knowledge graph, and if that structure changes even slightly, the system may think "I used to have evidence that the student knows (or doesn't know) topic ABC, but that evidence was conditional on the previous structure, and now I don't actually have evidence anymore, so I need to collect some evidence."

## Curriculum

> With short lessons, is the curriculum really comprehensive?

Yes, our curriculum is fully comprehensive; in fact, we perform curriculum comparisons against all the major textbooks to ensure that we're covering a superset of the material.

How do we cover all the necessary material if the lessons are so limited in scope? By breaking up each course into many, many lessons. A typical course ranges from 150-300 lessons, each lesson containing about 3-4 "knowledge points" of increasing difficulty, each knowledge point consisting of a worked example followed by 2-5 questions of active problem-solving where the number of questions adapts to the student's performance.

Basically, the "learning staircase" is being chopped up into a massive number of tiny stairs. It still reaches all the way to the top, but the individual stairs are small enough that students don't get stuck unable to climb a stair that's too big for them. Each topic is narrow in scope, and they incrementally build up to the deeper abstractions and generalities.

> I passed a lesson, but I don't feel like I have the deepest level of understanding. Is this normal?

First, keep in mind that each topic is narrow in scope, and they incrementally build up to deeper abstractions and generalities. Students with a high generalization ability may partially extrapolate some of those deeper patterns beforehand, leading to a temporary feeling of incompleteness (e.g., "I'm starting to feel something deeper at play here, but I can't quite put my finger on it"). Most likely, we do cover that deeper pattern, but it comes later in the curriculum. (However, if you think there's something we've missed, then please let us know specifically what it is! We're continually refining the curriculum.)

Second, also keep in mind that any lesson you do, it might not feel perfectly intuitive right away, and you might not notice all the connections there are to see. But if you stick with the process and continue periodically reviewing and layering more knowledge on top of that topic, you'll continually increase your intuition for it, all the way up to a deep level of understanding. The more knowledge you build on top of that topic, the more connections you make, the more deeply ingrained it becomes, the greater your level of automaticity, the more intuitive it feels, the more easily you're able to see connections to other topics.

Building knowledge is like working out. Like physical transformations, intellectual transformations are produced by accumulating a massive volume of incremental improvements. Our system will imbue you with a deep level of understanding if you're willing to start at a level where you're able to solve problems correctly, comfortably, and consistently, and then stick with the process consistently for a long enough time horizon that you could reasonably expect a body transformation if you were physically working out at the gym.

> Will taking a Math Academy course for a standardized exam (e.g., AP Calculus BC) fully prepare a student for the actual exam?

Math Academy courses cover the content knowledge that a student needs to be successful on a standardized test. While this constitutes the vast majority of the work necessary to prepare for a standardized test, it is not fully sufficient. After finishing their Math Academy course, a student must also take a number of practice exams for the specific exam that they are planning to take.

The reason why it's so important to take practice exams is that, in addition to being timed, standardized exams will "package" the content knowledge within various question framings, phrasings, and general contexts that may initially be unfamiliar to the student. While nobody can predict the exact problems that will appear on the exam, students can train themselves on the same statistical distribution that the exam problems are going to come from. This is accomplished by working through as many practice exams as possible, ideally real exams from the past, or at least practice exams that come directly from the organization who creates the exam. (If such resources are unavailable, it is critical to acquire practice exams from another organization that has a good reputation for matching up its problem types accurately against the real exam.)

Whenever a student misses a question on a practice exam (or answers the question with a low degree of confidence), they should refer to the solution, identify their mistake, and immediately work it out again correctly. The next day, they should try working out the same problem unassisted. If they solve it correctly, they should wait another several days before attempting the problem again; otherwise, if their attempt is unsuccessful, they should go back to the beginning of this process (refer to the solution, identify their mistake, immediately work it out again correctly, and re-attempt the next day). This is essentially performing spaced repetition on the student's areas of weakness. This process should continue for multiple rounds through all the practice exams, continuing all the way up until the day before the actual exam.

At the same time, the student should also enable "Test Prep Mode" in their Math Academy course so that they continue receiving reviews on course content instead of being promoted to the next course. It is necessary to continue completing these reviews on Math Academy so that the student does not get rusty on any of the course content. At the time the student takes the exam, they need to be 100% solid and 100% fresh on all their Math Academy course content as well as all the problem types covered in the practice exams.

As a rule of thumb, we recommend that at a minimum, students finish their Math Academy course at least 6 weeks prior to their exam, and go through at least 6 practice tests leading up to the exam. During this time, we recommend about 1.5 hours of prep per day: 30-45 XP of review on Math Academy, and 45-60 minutes taking and re-attempting problems from practice tests (the time it takes to grade the practice test should not be counted towards this time). In the week before the exam, we would recommend increasing the test prep sessions to 2-2.5 hours per day, spending the extra time on practice tests.

The practice tests need to be timed, but they can be broken up into smaller increments. For instance, if an entire test is 2 hours long, then a 30-minute segment can be constructed by doing every problem number that is a multiple of 4. It is important to slice the exam longitudinally like this, as opposed to just taking the first fourth of the exam, because exam problems are often arranged from easy to hard, with hard questions expected to take more time.

Lastly, note that when a student is solid on their course content knowledge and starts taking actual practice exams, they will probably be surprised at how low their score is initially. This is normal and it just takes a bit of exposure to get used to the time limit, question types, and phrasing of the exam questions. Math Academy has extensive hands-on experience preparing students for the AP Calculus BC exam, which is graded on a 1-5 scale (5 being the best), and in our experience, even students who end up getting a 5 often start out getting a 2 or maybe a 3 on their first practice exam. By their second exam, they may get a 3 or 4, and then a solid 4 or maybe just barely a 5 on their third exam, and then a more solid 5 on their fourth exam, and then deeper and deeper into 5 territory on their fifth and sixth practice exams.

> Does Math Academy explain the "why" behind procedures? Are all the concepts taught first?

Math Academy explains the "why" behind procedures all throughout the curriculum. Just to name a particular instance:

- In algebra, when we teach how to solve equations, the very first thing we do is introduce the idea of a solution of an equation: it's just a number that can be substituted for the variable to make the equation come out true. If you have the equation 2x=6, that's just saying "2 times something makes 6," and you don't even need algebra to know that the solution is x=3 (since 2 times 3 makes 6).
- We first give students some practice solving simple equations like that, without algebra, and only afterwards do we start talking about algebraic manipulations like "start with 2x=6, divide both sides of the equation by 2, get x=3." That way, students see algebraic manipulations as an extension of the intuitive reasoning that they were using to begin with.

However, concepts and procedures are intermingled throughout our curriculum. We do not teach "all the concepts first" and then "all the procedures after" because it's not possible to do one in proper depth without the other. Concepts and procedures have a bidirectional, mutually reinforcing relationship. In other words, they build on each other:

- low-level concepts support low-level procedures,
- low-level procedures support higher-level concepts, and
- higher-level concepts support higher-level procedures.

#### To provide a concrete example:

- a student must be able to count to understand the concept of a number,
- a student must understand the concept of a number to carry out arithmetic procedures, and
- a student must be able to carry out arithmetic procedures to understand the concept of a variable or an algebraic equation.

> Do your university courses have exercises with proofs or is it just computation?

Our Methods of Proof and Discrete Mathematics courses are proof-based. As of the time of writing (August 2025), our other university courses are computation-based, but that's just because they represent the first course in each subject, whereas a proof-based course would come second. We will eventually be building out those additional proof-based courses, but our current computation-based courses will be prerequisites.

There is sometimes confusion about people thinking Math Academy is stopping at its current level of depth/difficulty, when in reality, we are still building out the curriculum. It is nowhere near finished.

- Does our Methods of Proof course cover epsilon-delta proofs? Yes. Does it cover Papa Rudin? No, because that's well out of scope. Does that mean we're stopping short of Papa Rudin? No, it just means we haven't built up to that yet.
- Another example: we have a computation-based Linear Algebra course that will be a prerequisite for a proof-based Abstract Linear Algebra course later down the road. That second Linear Algebra course will go deeper into the theory and proofs that one might encounter while taking a linear algebra course at an elite university that uses, say, Axler's book.

Unfortunately, people sometimes move the goalposts and say "your [first] Linear Algebra course is not as intense as Axler," when this isn't even an apples-to-apples comparison. That's like pointing at a high school calculus class and complaining that it's not as intense as a real analysis course; of course it's not! It's a completely different course; in fact, a prerequisite course; and it's not meant to cover the same material.

Axler is really a second course in linear algebra, even if some universities throw students into it as their first course (which ends up causing a lot of unnecessary struggle). We often joke that Axler's book *Linear Algebra Done Right* should really be called *Linear Algebra Done a Second Time*.

- More generally: just because a topic is introduced in a course, doesn't mean the proof/derivation is also within scope of that course. For instance, formal proofs of derivative rules are out of scope for Calculus I/II (they would go in Real Analysis), and proving the rational roots theorem is out of scope for Precalculus (it would go in Abstract Algebra).

All of these proof-based courses are on our roadmap, but we are building our curriculum from the ground up, we are scaffolding everything to the max, and it's mastery-based (students are only asked to learn things after having mastered the prerequisites), so, naturally, we are going to be doing computation-based versions of courses before proof-based versions. The proof-based courses are ultimately just different courses, and we are getting the prerequisite courses in place to build up to them.

> Why does the curriculum focus on building procedural fluency before proofs/derivations? Shouldn't it be the other way around, prove/derive the formula and then apply it?

In most math curricula, including ours, it's expected that students will build procedural fluency first and cover full proofs/derivations second, usually in a later course. Why? Because this is the most effective way to get learners to understand the material. You can't really understand a proof/derivation before you've developed procedural fluency. If you try, it will feel like pushing symbols around without really understanding what they mean. Procedural fluency with concrete examples provides scaffolding for learning the proofs/derivations.

In particular, working through concrete examples imbues you with intuition that you will not get if you jump directly to studying the most abstract ideas.

If you go directly to the most abstract ideas, then you might as well be a kid who reads a book of famous quotes about life and thinks they understand everything about life by way of those quotes. You might think you understand the quotes when you're young, but after you accumulate more life experience, you realize that you really had only the most naive, surface-level understanding of the quotes back then, and you really had no idea what you were talking about.

The way you come to understand life is not by just reading quotes. You have to actually accumulate lots of life experiences. It's the same way in math. In general, the purpose and power of an abstract idea is that it compresses a zoo of concrete examples. But if you haven't built up that zoo of concrete examples, then you miss out on that power.

> Does the curriculum cover deep understanding? I have been doing a lot of computational problems and I am unsure whether this will lead to deep understanding.

The courses that we cover, we cover comprehensively. But people who don't know the standard math courses sometimes get confused about what typically goes in what course.

For instance, we sometimes hear people ask why we don't (e.g.) cover proofs of derivative rules in Calc I/II. They don't realize that's beyond the scope of any standard Calc I/II course and is instead covered in Real Analysis, a course that we don't have yet but is on our radar. The same thing happens with our first course in Linear Algebra. Sometimes people point out that it doesn't cover all of Axler's *Linear Algebra Done Right*, not realizing that Axler's book is actually meant to be a second course in linear algebra (and Axler even says this himself in the preface).

The courses on our system are comprehensive and we perform comparisons against the major textbooks to make sure we're covering all the bases. There is definitely room to include projects and challenge problems, which are on our radar, but we have yet to hear a specific example of a piece of knowledge that is properly scoped to one of our existing courses and does not appear in said course. If anyone presents such an example, then we will of course add it.

Personally, every time I have engaged in discussion about this, it has always turned out that

1. the critic does not understand the standard scope of math courses, or
2. their critique is not of Math Academy but of the standard scopes themselves, or
3. the critic has some nebulous "feeling" that we should cover more but can't articulate a specific concrete example, or
4. the critic doesn't want to put in the work to shore up their skills (especially if they did poorly in the diagnostic) and prefers some other resource that waters down material to make it accessible with fewer prerequisites.

(A concrete example of #4: I spoke with someone who, upon starting our calculus content, claimed we didn't cover the concept of the derivative as a rate of change in physical scenarios like the height of water while filling a trapezoidal pool, when in fact we have a bunch of topics on those physical/geometric derivative problems that come later in the course once you're able to interpret the derivative as the slope of the tangent line, compute some basic derivatives, and interpret the meaning of f'(x) given a verbal description of f(x).

He wanted to just go to the most advanced content right away without filling in his prerequisites, and when we placed him at the level that he was truly at, he felt like it was too elementary and mechanical-skill-based to pave the way to deep understanding. Basically, he just didn't want to do the work, and instead wanted to read about the derivative in broad strokes in a complex setting, without being made to solve actual problems.)

> It's hard to believe that 5 hours a week for a year starting from basic multiplication tables will have me completely prepared for university courses. I'd prefer an explanation for people who are not familiar with the XP system.

We realize that this can be a bit shocking! For this to feel more realistic, it's important to first understand that not all the math that children cover in school is necessary for university math. As described in [Chapter 31](../../V-TECHNICAL-DEEP-DIVES/31-Technical-Deep-Dive-on-Learning-Efficiency/31-Technical-Deep-Dive-on-Learning-Efficiency.md), we developed a Mathematical Foundations course sequence specifically for the purpose of getting adults up to speed as quickly and efficiently as possible with all the prerequisites that they would need to know (fractions through calculus) for university-level math courses. Roughly a third of topics in our Traditional sequence are required by school standards but do not actually come up as prerequisite material in university-level math. Those topics have been stripped out of the Foundations sequence.

Now, knowing that the Foundations sequence covers about two-thirds the content in the Traditional sequence, the rest of the argument follows from the success of our original in-school program in Pasadena where 6th graders started at various places in Prealgebra, did about 40-50 minutes of fully focused work per school day for the next 3 years, and covered all of Prealgebra, Algebra 1, Geometry, Algebra 2, Precalculus, and AP Calculus BC, passing the AP exam by the end of 8th grade. While this may also seem shocking, Math Academy has the AP scores to prove it, and there has been plenty of news coverage over the past decade.

Now, look at the numbers: 40-50 fully focused minutes per school day × 180 school days per year × 3 years comes out to about 24,000 minutes or 400 hours, and our Foundations series is about two-thirds the size of that (since roughly a third of topics are not actually prerequisites for university math), which comes out to about 267 hours. Divide by 52 weeks in a year, and you're at about 5 hours per week.

> Why is "holistic mode" (in which students also fill in any missing knowledge in lower-grade topics that are not prerequisites of their enrolled course) disabled for university courses?

Students are most likely to succeed when they break up long-term goals into short-term goals, maintain momentum, and experience plenty of small wins along the way. Suppose an expert tutor works with a Linear Algebra student who makes the following request:

In addition to helping me out with Linear Algebra and any missing prerequisites, can you fill in all my knowledge gaps in all the math I would be expected to know by now?

In this situation, the expert tutor should try to dissuade the student:

Are you sure you want to do this? It's possible, but I wouldn't recommend it. I will have to assess you on 4 years' worth of math and then teach you whatever you're missing, which will probably be the equivalent of 1 or more full years of math. This is not just an extra 15 minutes on top of each tutoring session. It's going to at least double your workload. And that extra work is not going to get you through Linear Algebra any faster.

Instead of trying to eat the whole elephant in one bite, why don't we just focus on Linear Algebra right now (and whatever math you're missing that's necessary for Linear Algebra) and then fill in the rest of your math background as you move on to other university-level courses that require it.

For instance, I know you're shaky on your calculus, but most of that isn't necessary for Linear Algebra, so instead of trying to build that up now let's wait until you get to Multivariable Calculus and build it up then. It will feel more relevant that way. We can do the same thing with your probability/stats knowledge when you take Probability & Statistics after Multivariable Calculus.

It will be more motivating this way. You'll learn linear algebra in 8 months, multivariable calculus in another 8 months, and probability & statistics in another 8 months, and you'll be filling in your math background all throughout that time. But if we front-load it and fill in all of your math background right now, it will take 14 months just to get through linear algebra. You'll get through multivariable calculus in 5 months after that, and probability & statistics in another 5 months after that, assuming that you don't quit in those initial 14 months.

Either way, you'll be at the same point 2 years from now. But it's going to be way more motivating if your wins are spaced 8 months apart, compared to if your first win doesn't happen for an entire 14 months.

If a student gets as far as university-level math but has missing background knowledge, it would be a mistake to front-load that missing knowledge and fill it all in while they complete their first university course. It would reduce friction and increase motivation to instead spread out the work, which is what will happen naturally as the student takes more university courses in non-holistic mode.

> When you introduce additional scaffolding to increase pass rates of lessons, how do you know the increase in pass rate actually represents learning? Couldn't the pass rates increase simply due to greater priming?

It's something to watch out for, but we do watch out for it. We also track review and quiz performance. There is less priming for review tasks, and no priming for quizzes. If students were to bomb those questions on quizzes, that would signal that the learning was superficial or temporary.

Additionally, most topics in our system have many post-requisites, so students are continually made to layer more advanced skills upon what they've learned. If they didn't actually learn a prerequisite, they wouldn't be able to continue executing progressively more advanced skills on top of it, just like if a basketball player can't dribble the ball, they won't be able to successfully complete any plays that involve running across the court with the ball.
