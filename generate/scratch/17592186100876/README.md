# Basis vector matrix multiplication generator

Only KP 17592186100876 is covered. Entry script: `generate/scratch/17592186100876.py`.

Run with `.venv/bin/python generate/scratch/17592186100876.py --difficulty easy --seed 19 --count 5 --format json`. `moderate` is also supported; `hard` raises an unsupported-band error. `--template` selects a source-specific bank and layout. Imported `generate` additionally accepts replay and explicit matrix/target parameters. Previews never access the database.

`validate.py` checks source fidelity, mathematics, slot coverage and real learner grading. `replenish.py` uses the existing application EDB integration, captures current inventory, acquires the same application `api.lock`, rechecks basis and source evidence, excludes used/reserved/invalid/duplicate tasks, and adds only the shortage at supported bands. It registers the stable generator identity with the installed id/script/ref schema. Every exact transaction, preview, immutable lineage, basis guard, source attribution, request key, receipt and exact-basis readback is retained in reference/replenishment/.

New variants never replace source questions or historical learner data. Source anomalies and exclusions are in classification.md. Hard remains unsupported, with an explicit five-question reserve shortage. The q-130247 special structured profile has four variants under the declared d-domain; it does not limit the other templates' pools. Zero new instances are fabricated to fill unsupported bands.
