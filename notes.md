

For starters, our pipeline should leave incomplete questions as is. This is not a blocker, this is not a problem to solve, this is not an issue at all. However, it seems to be causing sufficient confusion, so we probably need a more dedicated pathway to handling it.

Update the schema, by adding a cardinality many ref attribute :question-generator/level-coverage to the database and updating /home/jake/Developer/Course_Academy/schema/data/7-question-generator.edn and its counterpart in the database math folder. This attribute will denote which documented difficulty levels we can observe from our imports for each knowledge-point/kp. In addition add enum ident attribute {:db/ident :question.difficulty/unobserved} to the database and update /home/jake/Developer/Course_Academy/schema/content/4-question.edn and its counterpart in the math database folder with it as well. Our new :question-generator/level-coverage will point to one of four entities:

    {:db/ident :question.difficulty/easy}
    {:db/ident :question.difficulty/moderate}
    {:db/ident :question.difficulty/hard}
    {:db/ident :question.difficulty/unobserved}

Once that is in place I need you to make sure that the following is implemented:

The pipeline should take the best examples it has available, and fill in the gaps where we have no evidence. This usually arises in one of the following cases:
    
    1. No complete/whole questions. aka across all difficulty levels there are no complete questions with difficulty levels, answer fields, correct answer choices, or worked solutions.
    2. Semi-complete questions missing some of the above attributes. Either worked solutions, difficulty levels, answer fields or correct answer choices.

In either of these scenarios the pipeline should:

    1. Query the database (make sure this is part of the script, not an agent, and make sure it's optimized according to $edb best practices for query and pull) to find a KP with at least 2 complete questions at each difficulty level with math academy source/provenance. (One of our imported questions from capture)
    2. Study the examples to see their progression, and study what the kp has available that we should be seeking to retain/implement
    3. Create a fully complete exemplar question for that kp at each difficulty level that we can then build the generator from. It should try its best to retain all important scaffolding and structural components of the sparse data it did have available at that kp. 
    4. Let the pipeline pick up with the process we already have implemented using the new three examples to construct the generator.

This means that our generation pipeline has essentially three phases, each run by a headless agent (gpt-6.1-sol high):

    1. Investigation, and if neccessary, exemplar reconstruction/construction using our best judgement and understanding of Math Academy principles of pedagogy
    2. Authorship, create the python script generator
    3. Verification, and if neccessary, repair. The verifier agent should inspect the generator, evaluate it, and then immediately repair the generator of any flaws it finds in the same session. This should include poor pedagogy, improper scripting/locations, anything. It should including adding capabilities to the engine for answer resolution if neccessary.

At each stage, the headless agent is the SOLE judge of whether or not something meets requirements. Requirements stated by an earlier agent can, and often must be, overridden to implement appropriate repairs.

Sound good? 



I agree with most of that. Here are a few notes:

You said: "Those exemplars are clearly identified as authored reconstructions, not captured Math Academy questions." However, they need not be tagged/identified/labeled. Once the three exemplars are written, they should be pushed to the database under their KP but with a source of the agent that wrote them. The source/provenance is sufficient to distinguish. 

Additionally, instead of :question-generator/level-coverage I think it might be better to do :knowlege-point/level-coverage ?? Then we can define the coverage of each KP with a script identifying all imported questions with difficulty level attributes and then creating adding the attributes to each kp where it's observed. This will make scripting the remainder of the investigation phase easier. 

You also said, "I would also define a fallback: if no single qualifying reference KP exists, supply the best available references across KPs and let the investigator construct the progression. Missing reference coverage should not become another automatic dead end." But that will never happen. We have many such kps. It would be a waste of tokens to engineer for an edge case with 0% probability.

You also said, "With six workers, shared changes need isolated working copies and automatic integration checks; resolving conflicts remains the agents’ responsibility. Existing blocked jobs also need explicit recovery under the new rules, so this improves the backlog as well as future jobs." But this shouldn't be an issue either. Each worker is working on an isolated kp, they don't share kps. Right?

Otherwise, I agree. Implement the changes to the pipeline and restart it when finished. 