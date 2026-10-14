# Template extraction

## 1. Describe each original

|Source|Observed rating|Target|Visible local cue|Original solution/key|
|---|---|---|---|---|
|q-140411|unrated|3|non-tangent crossing; decreasing|both absent|
|q-140414|unrated|-2|tangent, touches/reverses; above axis|both absent|
|q-141133|easy|-1|tangent crossing; increasing|present|
|q-141137|easy|-5|tangent crossing; decreasing|present|
|q-141142|easy|9|tangent crossing; increasing|present|
|q-141144|easy|6|tangent, touches/reverses; above axis|present|
|q-141140|easy|-3|non-tangent crossing; increasing|present|

All prompts consist of a360px wide local red polynomial sketch, one labeled intercept and a horizontal arrowed x-axis, then the identical statement-selection question with “given” or “shown.” No y-scale is provided. All fields are radio, key `selection`, five text choices. The two unrated sources have complete banks but no observed correct designation.

## 2. Generalize the shared pattern

Locate the root named by each choice, determine whether the curve is tangent to the x-axis, then if multiple determine whether it crosses (odd) or touches/reverses (even). Return one categorical statement. A simple-root solution ends after the non-tangent conclusion; a multiple-root solution has distinct tangent, parity and final conclusion paragraphs. Higher multiplicity is underdetermined.

## 3. Map every original component and option

The table below is a complete35-choice mapping, including every incorrect option. The predicate recipes parameterize the target root; no numeric distractor fits or unrelated perturbations are used. A misconception interpretation is recorded only when structurally evident.

|Source|Field|Original option|Predicate recipe|Original key?|
|---|---|---|---|---|
|q-140411|selection|$x = 3$ is a simple root|Multiplicity1; overlook flattening if wrong|missing designation|
|q-140411|selection|$x = 3$ is a multiple root of even multiplicity|Multiple and even; confuse bouncing/crossing if wrong|missing designation|
|q-140411|selection|$x = 3$ is a multiple root of odd multiplicity|Multiple and odd; confuse bouncing/crossing or simple/multiple if wrong|missing designation|
|q-140411|selection|$x = 3$ is not a root of $p(x)$|Deny the marked intercept is a root|missing designation|
|q-140411|selection|$x = 3$ is a simple root of even multiplicity|Conjoin simple(m=1) and even(m even), an impossible source misconception|missing designation|
|q-140414|selection|$x =-2$ is a simple root of even multiplicity|Conjoin simple(m=1) and even(m even), an impossible source misconception|missing designation|
|q-140414|selection|$x =-2$ is not a root of $p(x)$|Deny the marked intercept is a root|missing designation|
|q-140414|selection|$x =-2$ is a multiple root of odd multiplicity|Multiple and odd; confuse bouncing/crossing or simple/multiple if wrong|missing designation|
|q-140414|selection|$x =-2$ is a multiple root of even multiplicity|Multiple and even; confuse bouncing/crossing if wrong|missing designation|
|q-140414|selection|$x =-2$ is a simple root|Multiplicity1; overlook flattening if wrong|missing designation|
|q-141133|selection|$x=-1$ is not a root of $p(x)$|Deny the marked intercept is a root|no|
|q-141133|selection|$x=-1$ is a multiple root of even multiplicity|Multiple and even; confuse bouncing/crossing if wrong|no|
|q-141133|selection|$x=-1$ is a multiple root of odd multiplicity|Multiple and odd; confuse bouncing/crossing or simple/multiple if wrong|yes|
|q-141133|selection|$x=-1$ is a simple root of even multiplicity|Conjoin simple(m=1) and even(m even), an impossible source misconception|no|
|q-141133|selection|$x=-1$ is a simple root|Multiplicity1; overlook flattening if wrong|no|
|q-141137|selection|$x=-5$ is not a root of $p(x)$|Deny the marked intercept is a root|no|
|q-141137|selection|$x=-5$ is a simple root of even multiplicity|Conjoin simple(m=1) and even(m even), an impossible source misconception|no|
|q-141137|selection|$x=-5$ is a simple root|Multiplicity1; overlook flattening if wrong|no|
|q-141137|selection|$x=-5$ is a multiple root of even multiplicity|Multiple and even; confuse bouncing/crossing if wrong|no|
|q-141137|selection|$x=-5$ is a multiple root of odd multiplicity|Multiple and odd; confuse bouncing/crossing or simple/multiple if wrong|yes|
|q-141142|selection|$x=9$ is not a root of $p(x)$|Deny the marked intercept is a root|no|
|q-141142|selection|$x=9$ is a simple root|Multiplicity1; overlook flattening if wrong|no|
|q-141142|selection|$x=9$ is a simple root of even multiplicity|Conjoin simple(m=1) and even(m even), an impossible source misconception|no|
|q-141142|selection|$x=9$ is a multiple root of odd multiplicity|Multiple and odd; confuse bouncing/crossing or simple/multiple if wrong|yes|
|q-141142|selection|$x=9$ is a multiple root of even multiplicity|Multiple and even; confuse bouncing/crossing if wrong|no|
|q-141144|selection|$x=6$ is a simple root|Multiplicity1; overlook flattening if wrong|no|
|q-141144|selection|$x=6$ is a multiple root of odd multiplicity|Multiple and odd; confuse bouncing/crossing or simple/multiple if wrong|no|
|q-141144|selection|$x=6$ is not a root of $p(x)$|Deny the marked intercept is a root|no|
|q-141144|selection|$x=6$ is a simple root of even multiplicity|Conjoin simple(m=1) and even(m even), an impossible source misconception|no|
|q-141144|selection|$x=6$ is a multiple root of even multiplicity|Multiple and even; confuse bouncing/crossing if wrong|yes|
|q-141140|selection|$x=-3$ is a multiple root of odd multiplicity|Multiple and odd; confuse bouncing/crossing or simple/multiple if wrong|no|
|q-141140|selection|$x=-3$ is a multiple root of even multiplicity|Multiple and even; confuse bouncing/crossing if wrong|no|
|q-141140|selection|$x=-3$ is a simple root of even multiplicity|Conjoin simple(m=1) and even(m even), an impossible source misconception|no|
|q-141140|selection|$x=-3$ is not a root of $p(x)$|Deny the marked intercept is a root|no|
|q-141140|selection|$x=-3$ is a simple root|Multiplicity1; overlook flattening if wrong|yes|

## 4. Stable backbone, slots and guards

Fixed: one categorical target, source five-predicate radio bank, original reference table/rules, exact conditional operative solution paths. Source bank selected whole before parameters, correct category computed first, all required other predicates derived next, then any semantic collision rejects the complete instance. No first-valid option pooling. All pairs compare their multiplicity sets; two different false statements are not equivalent merely because both are false for one graph.

|Slot|Meaningful domain|Dependencies|
|---|---|---|
|target root/position|easy integer−9..9; moderate two integers−6..6; hard three strict half-integers−13/2..13/2|axis tick, all five choices, every conclusion, plot and fingerprint|
|local category|simple, even multiple, odd multiple|curve vanishing order, tangent/parity solution, correct choice|
|orientation|±1|curve side signs; no change to category|
|visible context|easy1 root; moderate2 different categories; hard3 all categories|overview plot and target-selection reading demand|
|target index|any visible root, sorted canonical ordering|all references and local panel|

Separation≥3 for moderate/hard; level guards apply identically to sampler and explicit parameters. Moderate always has two integer roots and different categories. Hard always has three strict half-integer roots and all categories. Neither can reproduce easy, and hard cannot reproduce moderate. All within-level variants have the same number-form, context-selection and tangent/parity demand; no progression is encoded. Integer bounds include the observed signed/zero-nearby root forms and extrema−5,9. Half-integer axis reading is a conservative authored number-form extension anchored to prerequisite88’s rational roots (±2/3 and ±1/2), not a recovered source parameter.

Lesson order is Introduction → this KP → true statements regarding graphs → factored-polynomial recovery → graph selection. This KP stops at its first graph-reading step. Sibling canonical e-5814 demonstrates three root types, supporting two/three-root visual context, while equation recovery, end behavior and multi-statement selection remain outside scope. Authored moderate adds locating one named root among two integer intercepts; authored hard uses three signed half-integer intercepts and matching the target to its local view. The local panel aids flatness visibility without adding a calculation.

Finite meaningful task catalogs enumerate positions/configurations, category assignment, orientation and target. Positive amplitude, representative higher exponents, seed, shuffle, source/profile and notation aliases never count toward mathematical variety. Canonical sorting normalizes root-order spelling. Content identity separately includes actual prompt, full bank, fixed solution and supplied difficulty.

Raw profiles are `raw-q-…`, completed profiles `completed-q-…`, default `observed-five`. Raw original omissions are maintained at changed parameters as well. Only original anchor assets are reused; changed parameters invoke normal rendering, shared solution construction and categorical banks. No literal source-payload/answer lookup branch exists.
