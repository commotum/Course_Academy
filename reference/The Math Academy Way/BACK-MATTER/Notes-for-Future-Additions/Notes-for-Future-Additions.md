## Notes for Future Additions

While this working draft contains a lot of information, it's not even halfway done. I am still building out this book, and there is still lots of key information that remains unaddressed. Below are my working notes on items that I need to incorporate into the main body of the book.

#### Habit and Habit-Formation Mechanisms

- https://drive.google.com/file/d/1VpCeXatqMlblu5jHjmZq8J3Yn4ujyf3e/view?usp=drive_link

Streaks might be the most powerful habit-formation mechanism. Should cover the psychology of streaks, streak mechanics, etc.

Gym member retention strategies: academic study of habit frames the problem to solve and theory behind it, but at the end of the day you have to really get your hands dirty and go street-fighting against the problem of getting people to reliably show up, which is what gyms have to do.

- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=exercise+habit+formation&
- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=gym+member+churn+prediction&btnG=
- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=gym+member+retention&btnG=

## Streaks

- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=streaks+habit&btnG=
- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=streaks+habit+formation&oq=streaks+habit
- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=learning+streaks&btnG=
- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=learning+app+streaks&btnG=
- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=broken+streaks+motivation&btnG=
- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=streak+habit+freeze&btnG=
- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=streak+habit+threshold&btnG=
- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=streaks+in+classroom&btn
- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=streak+habit+classroom&btnG=
- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=streak+mechanics+gamification&btnG=
- https://scholar.google.com/scholar?hl=en&as_sdt=0%2C22&q=streak+mechanics+habit&btnG=

https://erringtowardsanswers.substack.com/p/intrinsic-motivation

## Coaching Science

It's really interesting how many parallels there are to coaching. I've got it on my reading list to check out some literature in coaching science. I anticipate it's also going to be a gold mine for motivational techniques, way more so than the standard "science of learning" literature, since coaching literature seems to focus more on high-performance settings whereas the science of learning literature tends to focus on fairly low-performance settings. (Which is unsurprising since there are way better incentive structures and accountability mechanisms to support high performance in the field of athletics, as compared to the field of education.)

#### **Direct Instruction**

Elaborate more on the decades of research behind direct instruction. Also talk about the need for specific direct instruction, not "general" domain-independent problem solving:

- Project Follow Through
  - https://x.com/greg_ashman/status/1926500662734356648
  - https://fillingthepail.substack.com/p/dismissing-project-follow-through
- Zig Engelmann
  - https://education-consumers.org/pdf/CT_111811.pdf (CLEAR TEACHING: With Direct Instruction, Siegfried Engelmann Discovered a Better Way of Teaching. By Shepard Barbash)
  - https://www.zigsite.com/
- Teaching General Problem Solving Skills Is Not a Substitute for, or a Viable Addition to, Teaching Mathematics https://www.ams.org/notices/201010/rtx101001303p.pdf
- Mathematical Ability Relies on Knowledge, Too https://files.eric.ed.gov/fulltext/EJ909939.pdf
- Consequences of History-Cued and Means-End Strategies in Problem Solving https://www.jstor.org/stable/1422136
- Response to De Jong et al.'s (2023) paper "Let's talk evidence: The case for combining inquiry-based and direct instruction"
  - https://www.sciencedirect.com/science/article/pii/S1747938X23000775
- Should also mention that in recent years, unguided instruction is still around and is still leading to subpar learning outcomes: The Efficacy of Inquiry-Based Instruction in Science: a Comparative Analysis of Six Countries Using PISA 2015 https://link.springer.com/article/10.1007/s11165-019-09901-0

#### CS Education

We anticipate that our standard approach to teaching math maps over pretty well to coding, but we still need to make a strong case for it, especially since so many people in coding eschew the idea of building automaticity through repetition of fundamental skills and think students should spend 100% of their time working on projects.

- Active Learning
  - Effects of Active Learning Environments and Instructional Methods in Computer Science Education (ACM)
  - Refactoring a CS0 course for engineering students to use active learning
- Mastery Learning
  - https://dl.acm.org/doi/epdf/10.1145/3649165.3690105 "Teaching CS1 With a Mastery Learning Framework"
- Spaced Repetition
  - "Does a Distributed Practice Strategy for Multiple Choice Questions Help Novices Learn Programming?"
- Increase Performance in CS2 via a Spiral Design of CS1 https://dl.acm.org/doi/abs/10.1145/3478431.3499339
- The Testing Effect / Retrieval Practice
  - Retrieval-based Teaching Incentivizes Spacing and Improves Grades in Computer Science Education
  - Retrieval Practices Enhance Computational and Scientific Thinking Skills https://dl.acm.org/doi/abs/10.1145/3478431.3499408
- Gamification
  - A Study on the Active Methodologies Applied to Teaching and Learning Process in the Computing Area https://ieeexplore.ieee.org/document/9252881

## Knowledge Spaces

Explain similarities & differences between ALEKS knowledge space theory and MA's approach.

Knowledge spaces are another way to describe mastery learning on a knowledge graph data structure. The researchers behind ALEKS and knowledge space theory did a great job formalizing, setting up definitions, proving rigorous theorems about mastery learning and diagnostic exams in a knowledge graph, but in order for our system to do what we want it to do, we had to introduce a bunch of other cognitive learning strategies and capabilities, resulting in needing to wrangle a lot more complexity.

In particular, the combinatorial perspective taken in the knowledge space papers & textbooks becomes intractable, which we've worked around by taking the approach of having quantities physically flowing through the graph, "constructing" the particular knowledge state in question as opposed to filtering it out of an exhaustive list of possible knowledge states. You kind of have to take the constructive, flowing-quantities approach when you're incorporating spaced repetition into the system.

There are also problems of scale. Several years ago I reimplemented the ALEKS diagnostic assessment algorithm and found that it became prohibitively computationally expensive when the knowledge graph contained more than a hundred or so nodes, whereas MA's diagnostic algorithm can and needs to handle many hundreds, even sometimes over a thousand nodes since our content is so much more scaffolded, we're assessing prerequisite knowledge, and we're going deep into high-level math that has tons of prerequisites.

Here are some of my old notes from that reimplementation project:

- The adaptive assessment method in the ALEKS paper seems intractable.
- Running it on a straight graph line, the number of knowledge states is roughly equal to the number of nodes.
- Running it on a binary tree graph, we find that when we double the number of splits, the number of knowledge states (KS) gets squared:
  - ~2 splits --> ~4 KS
  - ~4 splits --> ~16 KS
  - ~8 splits --> ~256 KS
  - ~16 splits --> ~65,536 KS
  - ~32 splits --> ~4,294,967,296 KS
  - ~64 splits --> ~1.8 x 10^19 KS
  - ~128 splits --> ~3.2 x 10^38 KS
- For recombining binary tree, it's a comparable (but less precise) trend (the numbers fit into the range suggested by the non-recombining binary tree).
- This places constraints on the graph. Beyond about 20 splits, it becomes intractable. This matches up with what's in their picture: about 20 splits (about 100 nodes) for Beginning Algebra, corresponding to 60,000 KS.
- We have about 150 splits (about 300 nodes) just in our MVC/LA course, so this isn't going to work for us, especially given that we're also assessing prerequisite knowledge. Our diagnostics need to cover up to about a thousand nodes.

## Spaced Repetition Visualization

I created the following visualization of spaced repetition. It's already worked into the main body of the document.

![](Images/_page_500_Figure_18.jpeg)

Spaced Repetition: fully-optimized minimum effective doses of review

However, it needs some additional clarification. In the spaced repetition graphic, the first blue rectangle corresponds to initial learning of the first topic within the blue unit, learning to the level of mastery.

The next blue rectangle with a slower forgetting curve would correspond to the first spaced review of that topic. And so on for future spaced reviews.

Same for the red rectangles: the first one corresponds to initial learning of the first topic within the red unit, learning to the level of mastery. The next red rectangle with a slower forgetting curve would correspond to the second spaced review of that topic. And so on.

This same process would be happening for the second topic in each unit, the third topic, and so on, all interleaved together. For simplicity, this is not shown in the graphic.

Just considering Blue and Red units, it would look something like this:

![](Images/_page_501_Figure_7.jpeg)

## Chunking

I haven't yet done any explicit literature searches on chunking. I should make sure I'm referencing "chunking" vocabulary whenever I'm essentially describing it in the body of this book, and check if there's any other relevant info surrounding chunking that I need to address in this book.

## Biological Basis of Neuroplasticity

Every concept is ultimately represented as a pattern of neural activity. Your brain can only devote so much effort to maintaining neural activity, but as you practice activating those neural patterns, biological changes occur that make the patterns easier to activate with less effort. As I recall, these biological changes are thought to primarily take place within synapses (https://en.wikipedia.org/wiki/Synaptic_plasticity), though there is also research into changes that occur elsewhere, e.g., in dendrites. Cover the neural mechanisms of retrieval-induced plasticity and how synaptic tagging/consolidation processes impact skill automation.

## Automaticity and Intuition

Need to lay out an explicit connection between repetition, automaticity, intuition, and creativity. I have a section on the relationship between automaticity and creativity, and the relationship between automaticity and intuition should fit right in around there.

Also need to really emphasize how important repetition is in mathematics to get to the point where you can even attempt to think creatively.

Doing the grunt work yourself really drills into you what those operations are. Like, you don't just think about the definition from afar, you really "feel" what it is, close up and in your bones, almost in a physical sense.

Talk about the importance of developing computational (procedural) & conceptual knowledge in tandem.

### More Case Studies

Look into other cases where a university changed their instructional methods and got some kind of feedback on the outcome.

For instance: https://people.math.harvard.edu/~knill/pedagogy/harvardcalculus/

## Spaced Repetition in Math vs Language

Mark (on Discord) mentioned that spaced repetition systems (SRS) have been shown to have very positive effects when used for discrete unrelated pieces of information (e.g. state capitals or the pronunciation of letters in a syllabary), but for language learners a focus on SRS decks of words typically underperforms extensive reading/conversation. It makes perfect sense that our fractional implicit repetition (FIRe) solution works well for math, but it is covered later on and it is only tangentially explained how FIRe solves those shortcomings affecting SRS decks with language learning. We need to address this more directly and early on in the spaced repetition section.

## Disambiguating Interleaving, Non-Interference, and Spaced Repetition

May also want to have a section on Interleaving, Non-Interference, and Spaced Repetition that clarifies the difference between all these things and how we balance all of them. Related resources:

- https://blog.innerdrive.co.uk/interleaving-dos-and-donts
- https://blog.innerdrive.co.uk/are-spacing-and-interleaving-the-same-thing

## Visualization of Macro-Interleaving

Maybe show some diagrams of interleaved paths through the knowledge graph vs. non-interleaved paths.

### Grade Inflation

UCSD faculty wrote a report about the effects since implementing "holistic admissions," and needing remedial math support for many more students than before: https://senate.ucsd.edu/media/740347/sawg-report-on-admissions-review-docs.pdf

Opening paragraph is unbelievably punchy: "Over the past five years, UC San Diego has experienced a steep decline in the academic preparation of its entering first-year students particularly in mathematics, but also in writing and language skills. Between 2020 and 2025, the number of students whose math skills fall below middle-school level increased nearly thirtyfold, reaching roughly one in eight members of the entering cohort. This deterioration coincided with the COVID-19 pandemic and its effects on education, the elimination of standardized testing, grade inflation, and the expansion of admissions from under-resourced high schools. The combination of these factors has produced an incoming class increasingly unprepared for the quantitative and analytical rigor expected at UC San Diego."

## Elaborative Interrogation

Should also talk about how we scaffold elaborative interrogation once we have more of that in the system (and should also have a chapter on elaborative interrogation as its own learning strategy). Some resources:

- https://www.learningscientists.org/blog/2016/7/7-1
- https://blog.innerdrive.co.uk/retrieval-practice-generative-learning

## **Optimal Manual Teaching**

Another chapter about how teachers can leverage these cognitive learning strategies as much as possible if they do not have access to technology. (How would you get the most bang for your buck teaching manually, without totally blowing up your workload to an inhuman degree? Obviously not going to capitalize on the full effects of what our tech can do, but you can still do a lot better than what the status quo is.)

### **Elaborative Interrogation**

Why/how questions like this: "Why does the parabola $y-k=a(x-h)^2$ have its vertex at (h,k)?" "Starting with the formula for slope, how do you get to the point-slope formula for a line?"

We don't do much of that at the moment, but now that we have select questions, we can probably use those for elaborative interrogation.

#### Miscellaneous Resources to Check Out

- Differentiation in Cognitive Abilities Beyond g: The Emergence of Domain-Specific Variance in Childhood https://journals.sagepub.com/doi/full/10.1177/09567976251321382
- Go through my own recent blog posts and check for anything to be worked in
- Carpenter, S. K., Witherby, A. E., & Tauber, S. K. (2020). On students' (mis)judgments of learning and teaching effectiveness. Journal of Applied Research in Memory and Cognition, 9(2), 137-151. https://doi.org/10.1016/j.jarmac.2019.12.009
- Book: Uncommon Sense Learning
- https://www.thescienceofmath.com/timed-tests-cause-math-anxiety
- https://x.com/seventhmeal/status/1838296108369612918 https://dominiccummings.com/the-odyssean-project-2/
- https://x.com/justinskycak/status/1841508577443496260
- https://gwern.net/doc/psychology/chess/2014-hambrick.pdf
- https://notes.andymatuschak.org/zBmSSpM1WfFDehxNCBcqSZp?stackedNotes=zMX9Lfuz8sGfDUivWZcyWT
- Tons of great references here: https://scienceoflearning.substack.com/p/should-we-teach-children-to-memorize?triedRedirect=true
- https://scottbarrykaufman.com/wp-content/uploads/2011/06/Protzko-Kaufman-2010.pdf
- https://www.colorado.edu/ics/sites/default/files/attached-files/91-06.pdf
- https://www.researchgate.net/publication/51129143_Spaced_Retrieval_Absolute_Spacing_Enhances_Learning_Regardless_of_Relative_Spacing
- https://arxiv.org/abs/2006.01581
- https://gwern.net/doc/psychology/chess/2014-hambrick.pdf Deliberate practice: Is that all it takes to become an expert?
- https://www.rocketmath.com/about-rocket-math/research_studies-and-results/
- https://www.rocketmath.com/wp-content/uploads/2016/03/Math-Facts-research.1.pdf
- https://www.rocketmath.com/wp-content/uploads/2016/03/Third-stage-of-Learning-Math-Facts.pdf
- https://www.rocketmath.com/wp-content/uploads/2016/03/How-fast-is-fast-enough-to-be-automatic.pdf
- Individual Differences in Arithmetic: Implications for Psychology, Neuroscience and Education by Ann Dowker
- Working Memory and Learning: A Practical Guide for Teachers by Susan Gathercole and Tracy Packiam Alloway
- Children's Mathematical Development: Research and Practical Applications by David C. Geary
- Visible Learning: Feedback by John Hattie & Shirley Clarke
- Visible Learning: The Sequel: A Synthesis of Over 2,100 Meta-Analyses Relating to Achievement by John Hattie
- Acquisition of Complex Arithmetic Skills and Higher-Order Mathematics Concepts, Volume 3 edited by David C. Geary, Daniel B. Berch, Robert Ochsendorf, & Kathleen Mann Koepke
- Cognitive Foundations for Improving Mathematical Learning, Volume 5 edited by David C. Geary, Daniel B. Berch, & Kathleen Mann Koepke
- Summing up hours of any type of practice versus identifying optimal practice activities: Commentary on Macnamara, Moreau, & Hambrick (2016). (link)
- Deliberate practice and proposed limits on the effects of practice on the acquisition of expert performance: Why the original definition matters and recommendations for future research. (link)
- Given that the detailed original criteria for deliberate practice have not changed, could the understanding of this complex concept have improved over time? A response to Macnamara and Hambrick (2020). (link)
- Self-Construction, Self-Protection, and Self-Enhancement: A Homeostatic Model of Identity Protection. (link)
- Self-enhancement and self-protection: What they are and what they do (link)
- Illusions of comprehension, competence, and remembering. (link)
- Assessing our own competence: Heuristics and illusions. (link)
- Can research inform classroom practice?: The particular case of buggy algorithms and subtraction errors (link)
- <a href="https://www.johndcook.com/blog/2013/02/04/four-hours-of-concentration/">https://www.johndcook.com/blog/2013/02/04/four-hours-of-concentration/</a>
- "Forgetting focuses remembering and fosters learning; remembering generates learning and causes forgetting; learning causes forgetting, begets remembering, and supports new learning." (Robert Bjork, "On the symbiosis of remembering, forgetting, and learning," 2011 p. 16)

#### Books to check out

- Instructional Illusions by Kirshner, Hendrick, Heal
- Teach Like a Champion
- A Coach's Guide to Teaching
- Teach to Learn (Catherine Scott)
- Urban Myths about Learning and Education by Bruyckere, Kirschner, Hulshof
- Accelerated Expertise Robert R. Hoffman
- Ultralearning Scott Young
- The Science of Rapid Skill Acquisition Peter Hollins
- Hidden Potential by Adam Grant
- 10 to 25: The Science of Motivating Young People
