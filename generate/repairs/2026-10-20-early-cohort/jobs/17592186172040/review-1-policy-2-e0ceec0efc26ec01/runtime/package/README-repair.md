The runtime package is defined by package.json. It uses Python 3.13.5, SymPy 1.14.0 and Matplotlib 3.11.2. Example:

```sh
COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=/tmp/slope-field-output /home/jake/Developer/Course_Academy/.venv/bin/python 17592186172040.py --difficulty moderate --count 5 --seed 801239 --format json
```

The output directory must be set whenever new plots are needed. Runtime source images already published under images/ retain their canonical paths. Generated images, sidecars, temporary inputs and the Matplotlib cache are written only under the explicit output directory. No external renderer interpreter, uv archive paths or bundled plot cache is needed.

Explicit canonical replay: --difficulty easy --profile e-8507 --seed 991 --count 1 --format json. Its exact source composite and worked text remain fixed, with four labeled selections. The supplied canonical source lacks a captured answer field and difficulty; the radio adapter and easy assignment are documented in instructional-account.md. Default authored linear sampling remains separate. All existing practice replay profiles and moderate/hard families are retained.

Retained finding checks are registered in repair-regressions.json. Reproduction, validation commands, samples and results are in evidence/commands.md. The older files under 17592186172040/ remain historical author evidence; only package.json's listed files are runtime dependencies. No registration/publication was performed by this repair.
