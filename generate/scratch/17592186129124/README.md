# Sinusoidal range generator

Local draft at basis 1356; stops after steps 3–7. No registration or database operations.

```sh
.venv/bin/python generate/scratch/17592186129124/validate.py
.venv/bin/python generate/scratch/17592186129124/build_evidence.py
.venv/bin/python generate/scratch/17592186129124.py --difficulty all --seed 12 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186129124.py --difficulty moderate --profile raw_q-25512 --format json
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard. Twelve source-shaped range/minimum × sin/cos × linear/degree/radian families; all supported at all three levels. Normal fields are five-choice radios, from complete method banks. Explicit raw source profiles preserve missing attributes and exact original strings/banks, including the q-25512 error; all raw evidence is ineligible for learning. Exact coverage: 9/9 prompts, 7/7 stored solutions, 7/7 banks (35/35 choices), 5/5 stored correct refs. Missing refs and fieldless records are not native-gradable raw fixtures; five complete original banks and all normal family/profile variations are checked with the native engine. See validation.json for independent printed-math and scope checks, and review.md/review.json for originals and variants.

Hard uses authored small rational scale/translation arithmetic. Task counts exclude horizontal/notation/bank aliases: easy 96 range + 76 minimum, moderate 96 + 76, hard 1080 + 1016. Source difficulty overlaps are preserved, while normal authored bounds distinguish easy positive integers, moderate negative integers and hard negative noninteger rationals.

Generator version 1.0.0 frozen for parent QA. Validation records actual Python/SymPy versions and native executable hash. No plots required.
