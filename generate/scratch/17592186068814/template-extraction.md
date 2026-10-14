# Template extraction

## 1. Specific source descriptions

Every raw source prompt and ordered complete solution is reproduced in review.md before changed variants. The following table records observed parameters, field contract and raw omissions.

|Source|Observed rating|n|d|Family|Bank recipes in source order|

|---|---|---:|---:|---|---|

|q-97958|unrated|3|2|rational|-1, 1, a, -numerator, -a|

|q-97963|unrated|3|1|integer|-a, -rounded_inverse, -1, 1, a|

|q-113335|:question.difficulty/easy|1|6|unit_numerator|-a, -1, -inverse, a, inverse|

|q-113337|:question.difficulty/moderate|5|2|rational|-a, inverse, -inverse, -1, a|

|q-113339|:question.difficulty/moderate|7|3|rational|a, -1, -denominator, -inverse, -a|

|q-113341|:question.difficulty/moderate|5|4|rational|a, -inverse, -a, inverse, -1|

|q-113336|:question.difficulty/easy|6|1|integer|inverse, -a, a, -inverse, -1|

|q-97949|:question.difficulty/moderate|3|4|rational|-a, a, 1, -numerator, -1|

|q-99068|:question.difficulty/easy|1|4|unit_numerator|-1, -inverse, -a, inverse, -double|

## 2. Generalized pattern

Given y=-n/(dx), choose its graph among five complete reciprocal curves. Start with y=-1/x, then multiply every ordinate by positive n/d; branches remain in quadrants II and IV, and both coordinate axes remain asymptotes. A fixed worked solution has opening, base-curve bullet, base image, vertical-stretch bullet, final image; it does not depend on submitted answer. The missing original solutions remain absent in raw profiles.

## 3. Complete component and choice mapping

In this table a=n/d>0 and c is the coefficient in the complete curve y=c/x. Every source bank is chosen as a unit. Correctness compares complete curves by coefficient, for every pair, including incorrect–incorrect pairs. Source images themselves are retained at anchors; changed parameters render the same recipes. Plot-spec.json contains independent per-asset coefficients, axis calibration, two labeled points, native size and checksums.

|Source|Field/key/type|Position|Image asset (exact)|Recipe|Anchor c|Designation|

|---|---|---:|---|---|---|---|

|q-97958|selection / radio / image|0|images/d5/d5d93e12275c683e0a56f0ec9a0c99540a7774879cd0f8fa69151ddba68a44fa.png|-1|-1|original absent; mathematical incorrect|

|q-97958|selection / radio / image|1|images/a3/a32495fcca947d01cf8d3218fc5cfc0cce083a34e6fb6b629d92ba9e47039a6e.png|1|1|original absent; mathematical incorrect|

|q-97958|selection / radio / image|2|images/5a/5a43656a35d47c7321e53d56238cd10f669bc807d57f72fcc002d79fb21aa111.png|a|3/2|original absent; mathematical incorrect|

|q-97958|selection / radio / image|3|images/66/6681008fc3e783b64e6bce7e7e0e9c72beb8761fc8cebb35926d528aac076bd9.png|-numerator|-3|original absent; mathematical incorrect|

|q-97958|selection / radio / image|4|images/e1/e144ab612b3e459d53af52fa81552feb1d2f8bf62ff04b3d91fbf36c02ccbc05.png|-a|-3/2|original absent; mathematical correct|

|q-97963|selection / radio / image|0|images/66/6681008fc3e783b64e6bce7e7e0e9c72beb8761fc8cebb35926d528aac076bd9.png|-a|-3|original absent; mathematical correct|

|q-97963|selection / radio / image|1|images/55/55eaee6d80f39db2ab3337a83ae65c249f886b4f216f0a4856413178f5203d3f.png|-rounded_inverse|-33/100|original absent; mathematical incorrect|

|q-97963|selection / radio / image|2|images/d5/d5d93e12275c683e0a56f0ec9a0c99540a7774879cd0f8fa69151ddba68a44fa.png|-1|-1|original absent; mathematical incorrect|

|q-97963|selection / radio / image|3|images/a3/a32495fcca947d01cf8d3218fc5cfc0cce083a34e6fb6b629d92ba9e47039a6e.png|1|1|original absent; mathematical incorrect|

|q-97963|selection / radio / image|4|images/79/79b496d28a0136f46e594a1b8dfddffcf4ed72557ded658259326e9ed09276ab.png|a|3|original absent; mathematical incorrect|

|q-113335|selection / radio / image|0|images/71/7152303066f322a8179b2e37863cea6367290998e31382fa0470a1ab50b4d2ff.png|-a|-1/6|correct|

|q-113335|selection / radio / image|1|images/9d/9da0db2e6c97e507e82b7ca801e46802fabf91ad31ff53ad3cc9ae580151370a.png|-1|-1|incorrect|

|q-113335|selection / radio / image|2|images/6e/6e6a7fcfd10a7c70ee44e1a7cd909de72486c89b8e670c90bb4eb006c6abff0e.png|-inverse|-6|incorrect|

|q-113335|selection / radio / image|3|images/e4/e4247c7cea75f1b89cd9bb161a96213de3529ce3c17926adf8633ae9483f154b.png|a|1/6|incorrect|

|q-113335|selection / radio / image|4|images/3d/3d188a16edf9add98edd1a5088392baae36c50b3a2fc1f806cc2cf320cc601fc.png|inverse|6|incorrect|

|q-113337|selection / radio / image|0|images/3b/3bc730306eaa88729b46b20ddb32782c89186f6db66c51fd924b2622804396aa.png|-a|-5/2|correct|

|q-113337|selection / radio / image|1|images/2d/2dc7eb6d95c2bba3a4465a4631a0443addabf3ae728a7c99839a924fdf194eea.png|inverse|2/5|incorrect|

|q-113337|selection / radio / image|2|images/22/22a5600f9104cbb34a4274f09af767862e7b7bc21dc2edbca2a55e5207947142.png|-inverse|-2/5|incorrect|

|q-113337|selection / radio / image|3|images/d5/d5d93e12275c683e0a56f0ec9a0c99540a7774879cd0f8fa69151ddba68a44fa.png|-1|-1|incorrect|

|q-113337|selection / radio / image|4|images/cd/cd9cfc5f59e164633c0c733428813519ad03d56f9da767e4ddeed4bcae072451.png|a|5/2|incorrect|

|q-113339|selection / radio / image|0|images/31/310ef143ec2c93eb46bbf15ab972197d8e1c42fa0cdfccc68cb7c6f156d7d720.png|a|7/3|incorrect|

|q-113339|selection / radio / image|1|images/d5/d5d93e12275c683e0a56f0ec9a0c99540a7774879cd0f8fa69151ddba68a44fa.png|-1|-1|incorrect|

|q-113339|selection / radio / image|2|images/66/6681008fc3e783b64e6bce7e7e0e9c72beb8761fc8cebb35926d528aac076bd9.png|-denominator|-3|incorrect|

|q-113339|selection / radio / image|3|images/08/08d95ddb62305aa1d73de83367472fc594c2bbe37f5d3acf1e14a3ef5f6d8fee.png|-inverse|-3/7|incorrect|

|q-113339|selection / radio / image|4|images/ed/ed5613c7614ab24b823ba0729ed1a19e2d0e57a4b81c0ba7868ccb61a52e7904.png|-a|-7/3|correct|

|q-113341|selection / radio / image|0|images/16/16989adc9499c3ec35bb3375d4f7b726dd24d4e57cb9fc9774ed3f7b746cf483.png|a|5/4|incorrect|

|q-113341|selection / radio / image|1|images/65/65557d7d1cecf94ef310ee267d78d662395d314d5b7b3d2f9771565ad67717c2.png|-inverse|-4/5|incorrect|

|q-113341|selection / radio / image|2|images/6e/6e56262645ef598cacb1377193398f1f3a59a2637193d05c813ffa075603c262.png|-a|-5/4|correct|

|q-113341|selection / radio / image|3|images/9f/9f4baec4c35b55d40261d6d4b058c241edf4644b2b8a46c5baebf6dc0e9ecea4.png|inverse|4/5|incorrect|

|q-113341|selection / radio / image|4|images/d5/d5d93e12275c683e0a56f0ec9a0c99540a7774879cd0f8fa69151ddba68a44fa.png|-1|-1|incorrect|

|q-113336|selection / radio / image|0|images/e4/e4247c7cea75f1b89cd9bb161a96213de3529ce3c17926adf8633ae9483f154b.png|inverse|1/6|incorrect|

|q-113336|selection / radio / image|1|images/c5/c525edcf937bfdc311acd0d7cac778802e1939dc2bd61fd3a5bf58f808712220.png|-a|-6|correct|

|q-113336|selection / radio / image|2|images/f0/f00fdde9e08069b5b0253fd2a871bf0c652644a30d38f4b5f09d003c44bc119f.png|a|6|incorrect|

|q-113336|selection / radio / image|3|images/71/7152303066f322a8179b2e37863cea6367290998e31382fa0470a1ab50b4d2ff.png|-inverse|-1/6|incorrect|

|q-113336|selection / radio / image|4|images/d5/d5d93e12275c683e0a56f0ec9a0c99540a7774879cd0f8fa69151ddba68a44fa.png|-1|-1|incorrect|

|q-97949|selection / radio / image|0|images/76/76d779da22082439eb40586ddbeb325368b1f49f15fef3158ebaa0eee90f4d84.png|-a|-3/4|correct|

|q-97949|selection / radio / image|1|images/64/647f80eeaea16048c9ba2677624ff6f3393183f6ea0df1529defa5fd55881f52.png|a|3/4|incorrect|

|q-97949|selection / radio / image|2|images/a3/a32495fcca947d01cf8d3218fc5cfc0cce083a34e6fb6b629d92ba9e47039a6e.png|1|1|incorrect|

|q-97949|selection / radio / image|3|images/66/6681008fc3e783b64e6bce7e7e0e9c72beb8761fc8cebb35926d528aac076bd9.png|-numerator|-3|incorrect|

|q-97949|selection / radio / image|4|images/d5/d5d93e12275c683e0a56f0ec9a0c99540a7774879cd0f8fa69151ddba68a44fa.png|-1|-1|incorrect|

|q-99068|selection / radio / image|0|images/9d/9da0db2e6c97e507e82b7ca801e46802fabf91ad31ff53ad3cc9ae580151370a.png|-1|-1|incorrect|

|q-99068|selection / radio / image|1|images/20/20395852a0e436d54029140fe79c4feadd9de30b091f744256b2e2e628d27725.png|-inverse|-4|incorrect|

|q-99068|selection / radio / image|2|images/34/344a3615421b88df05cb666ca90395991f3aa6af75c9095a60c73be89124b7e9.png|-a|-1/4|correct|

|q-99068|selection / radio / image|3|images/18/1813663317cf30286f540a84a5cba64248b2f268aa8c34cb3435f693b385c840.png|inverse|4|incorrect|

|q-99068|selection / radio / image|4|images/ec/ec84a88fe3cb4b404c2332ae0cb05fe9fc5f34077505ba6b086420cae93b9c5b.png|-double|-1/2|incorrect|

### Recipe interpretation

The bank operations are: `-a` correct negative stretch; `a` omitted reflection; `-1` omitted stretch; `1` omitted both; `inverse` reciprocal factor and omitted reflection; `-inverse` reciprocal factor; `-numerator` omitted denominator; `-denominator` used the denominator itself as the stretch. These are defensible method-derived interpretations, not proven author intent. The `-double` extra in q-99068 equals twice the required ordinate but no source explains why: its parameterized extension remains opaque and evidence-only, ineligible for defaults. q-97963 visibly labels its reciprocal-error curve -0.33 rather than -1/3. Its raw `-rounded_inverse` recipe rounds the reciprocal magnitude to two decimal places, preserving that actual displayed source value (33/100); no claim of exact 1/3 raster recovery. Normal defaults use exact fractions. Raw missing correct refs are not counted as matched designations.

## 4. Reusable masks, slots and guards

Fixed backbone: negative unshifted reciprocal target, graph selection, five image options, selection radio key, two transformation steps when solution exists, no learner-facing diagnoses or added feedback. Slots n,d are positive reduced integers; base coefficient remains -1. Unit-numerator easy n=1,d=2..12; integer easy n=2..12,d=1. Moderate n=2..24,d=2..5, gcd=1 and 1/3≤n/d≤4. Authored hard n=2..24,d=6..12, gcd=1 and same ratio bounds, nonunit marked x=±2. Bounds apply to explicit calls and samplers. Each bank is complete and rejects the entire instance if any pair agrees. q-99068 d=2 is rejected because -2a=-1.

The raw mask replaces complete target formula components, the complete stretch-factor token and each ordered image slot; punctuation, spacing, shared sentences, optional attribute presence and exact answer shape stay fixed. At original parameters all seven solutions and nine prompts are raw-exact. At changed parameters only these slots differ. Source options use their own axis scales; apparent silhouette is insufficient to recover c. Normal solutions use the source two-bullet phrasing, exact factor, negative base graph and final correct plot.

Identity: content includes version, actual difficulty presence, actual displayed prompt, fixed solution and complete sorted bank. Seed/order/profile aliases do not enter identity. Mathematical fingerprint includes negative reduced coefficient and nonunit-coordinate workload, excludes answer bank and aliases. Original/raw answers have generated owned UUIDs and exact source values; enum wrappers normalize to strings as required by local API. Raw feedback omission is exact.