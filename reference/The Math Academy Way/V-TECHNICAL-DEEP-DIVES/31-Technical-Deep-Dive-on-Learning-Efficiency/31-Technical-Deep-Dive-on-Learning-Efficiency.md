# Chapter 31. Technical Deep Dive on Learning Efficiency

**Note:** this chapter elaborates on concepts introduced in chapter 17 and chapter 21.

Summary: We introduce the concept of theoretical maximum learning efficiency, analogous to the physical phenomenon that nothing can travel faster than the speed of light. The maximum learning efficiency for a given knowledge graph depends on its encompassing density – however, a knowledge graph does not have to be fully encompassed, or even nearly fully encompassed, for its maximum learning efficiency to approach the theoretical limit. Math Academy's mathematical knowledge graph contains enough encompassings that its maximum learning efficiency is close to the theoretical limit. In practice, the actual learning efficiency attained by an individual student depends primarily on the student's quality of performance, and to a lesser extent on their pace (the average amount of work completed each day).

## What is Learning Efficiency?

### Theoretical Maximum Learning Efficiency

In physics, nothing can travel faster than the speed of light. It is the theoretical maximum speed that any physical object can attain. A universal constant.

In the context of spaced repetition, there is an analogous concept: theoretical maximum learning efficiency. In theory, given a sufficiently encompassed body of knowledge, it is possible to complete all your spaced repetitions without ever having to explicitly review previously-learned material.

As a simple demonstration, consider a sequence of topics where the first topic is fully encompassed by the second, which is fully encompassed by the third, which is fully encompassed by the fourth, and so on.

![](Images/_page_383_Picture_2.jpeg)

Each time you learn the next topic, all the topics below receive full implicit repetitions. Assuming that you never run out of new topics to learn, the only reason you would ever need to do an explicit repetition is if you get stuck repeatedly attempting and failing to learn the next topic.

It's important to realize that a graph does not have to be fully encompassed, or even nearly fully encompassed, for its maximum learning efficiency to approach the theoretical limit. Even if most relationships between topics are non-encompassing, a considerable minority of encompassings goes a long way.

For instance, Math Academy's mathematical knowledge graph contains enough encompassings that its maximum learning efficiency is close to the theoretical limit. We have empirically observed that, in practice, most mathematical courses can be learned with roughly only one explicit review per topic on average. In theory, a perfect student who aced every single learning task would need even fewer explicit reviews.

### Theoretical Minimum Learning Efficiency

By contrast, there is also a concept of theoretical minimum learning efficiency. This is precisely the setting of independent flashcards - or equivalently, a set of topics without any encompassings.

![](Images/_page_383_Picture_8.jpeg)

In this setting, no topic can receive implicit repetitions from any other topic. Every single review must be done explicitly.

![](Images/_page_384_Figure_3.jpeg)

It's worth emphasizing that, unlike Math Academy, other spaced repetition systems do not leverage the power of encompassings and therefore implement theoretical minimum learning efficiency.

## Factors that Impact Learning Efficiency

Remember that to achieve maximum learning efficiency, Math Academy uses a process that we call repetition compression. We gather all topics that have due repetitions, and then compress this set into a much smaller set of tasks that

1. covers all of the due repetitions, and
2. will lead to the greatest overall gain in spaced repetitions across your entire knowledge profile (while simultaneously climbing the knowledge graph evenly to maintain a broad spread of choices for future optimization).

You can think of Math Academy as a turbo-boosted educational engine, where repetition compression is our combustion mechanism.

But remember that an engine can't actually move a car unless it is supplied with gas and oil. The gas is needed to produce the energy that moves the car, and the oil is needed to prevent friction from locking up the engine.

The same applies to Math Academy. In order to experience the turbo-boosting,

1. you have to put in a sufficient amount of work that can be converted into educational progress, and
2. the quality of your work has to be high enough to avoid excessive friction during the learning process.

#### Performance

By looking at your **performance** (pass rate and accuracy) across various types of learning tasks, we are able to calculate a learning efficiency percentage that estimates how close you are to the maximum possible efficiency for your course.

If you maintain a high learning efficiency, then you can make a lot of progress in your course by doing a relatively small amount of work. But if you have a low learning efficiency, then you will have to do significantly more work to make the same amount of progress.

| Learning Efficiency | How Much Work to Complete a Course |
|---------------------|------------------------------------|
| 1.00                | 1x                                 |
| 0.80                | 1.25x                              |
| 0.67                | 1.5x                               |
| 0.50                | 2x                                 |
| 0.25                | 4x                                 |

#### Pace

In Math Academy, work is measured in **eXperience Points** (**XP**). One XP represents one minute of fully-focused, fully-productive work for an average serious (but imperfect) student. The amount of XP that you complete per weekday (on average) is called your pace.

#### Learning Efficiency vs Pace

Although the quality of your work is the single greatest factor that affects your learning efficiency, your pace can affect your learning efficiency as well. The faster you push your knowledge frontier forward, the further your knowledge frontier is ahead of your due reviews, and the more likely it is that we can find good topics to "knock out" a large number of your due reviews.

We empirically determined the following relationship:

learning efficiency
$$\propto$$
pace<sup>0.1</sup>

This means that if you double your pace, your learning efficiency increases by about $2^{0.1} = 7\%$. Likewise, if you cut your pace in half, your learning efficiency decreases by about 7%.

#### Pace vs Time to Completion

In a normal class period during a school day, it's reasonable to expect at least 40 minutes of fully-focused, fully-productive work. This corresponds to a baseline pace of 40 XP per weekday.

When we benchmark the amount of XP in our courses, we simulate an average student who is serious but imperfect and works at a pace of 40 XP per weekday. On average, courses contain about 3000 XP assuming that a student knows all the necessary prerequisites (though this can vary a lot depending on the amount of material that must be covered, e.g. prealgebra is ~2000 XP but precalculus is ~4000 XP).

Below is a table that shows how long it would take you to complete a 3000 XP course, depending on your pace. Note that learning efficiencies are computed relative to the baseline pace of 40 XP/weekday (so a pace of 40 XP/weekday corresponds to an efficiency of 1, and higher paces correspond to efficiencies greater than 1).

| Pace<br>(XP/weekday) | Efficiency Multiplier<br>(pace/40)<sup>0.1</sup> | How Long To Complete a Course<br>Benchmarked at 3000 XP<br>weekdays = 3000/(pace*multiplier) |
|----------------------|--------------------------------------------------|------------------------------------------------------------------------------------------------|
| 160                  | 1.15                                             | 3 weeks                                                                                        |
| 80                   | 1.07                                             | 7 weeks                                                                                        |
| 40                   | 1.00                                             | 15 weeks                                                                                       |
| 20                   | 0.93                                             | 32 weeks                                                                                       |
| 10                   | 0.87                                             | 69 weeks (~1.3 years)                                                                          |
| 5                    | 0.81                                             | 148 weeks (~3 years)                                                                           |

To put this in perspective: in a traditional classroom, each weekday involves 50 minutes of class plus the same duration of homework after school. On this schedule, it takes students a full school year (36 weeks) to complete a course.

![](Images/_page_388_Figure_2.jpeg)

But if you spent the same amount of time working on Math Academy (100 XP/weekday), you could finish in just 5-6 weeks! That's more than a 6x speedup - and you don't have to be a genius to achieve it. Remember, we're talking about an average student who is serious but imperfect.

Even for a massive course like AP Calculus BC (which is benchmarked at about 6000 XP, twice as big as an average course), the speedup is still over 3x. And if you factor in all the extra time you'd spend studying for quizzes, midterms, finals, and the AP test itself in a traditional class, which is already included in Math Academy's 6000 XP benchmark, it's a 4x speedup.

On the flipside, if you tried to use Math Academy like a phone game and only did a couple of minutes per day, it could take you nearly a decade to learn a traditional school year's worth of math.

For this reason, we highly recommend that you maintain a pace of at least 15 XP per weekday if you want to experience the benefits of Math Academy. But really, the higher your pace, the better.
