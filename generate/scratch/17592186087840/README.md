# Tall ellipse generator

Script: `../17592186087840.py`. Local review data only; no EDB registration/transactions.

Verification: `.venv/bin/python generate/scratch/17592186087840/validate.py`.
Evidence rebuild before freeze: add `--write-evidence`, then run `build_evidence.py`.
CLI: `.venv/bin/python generate/scratch/17592186087840.py --difficulty all --seed 2 --count 2 --format json`.

Observed integer-radio, integer-blank and half-blank templates replay all21 sources, all69 values, all20 present solutions and correct designations; q-7605's missing attributes are retained in raw public profile replay. The explicit supported q-7605 repair infers its correct equation and fixes its lower intercept label. Source banks have complete public q-ID profiles and are never default sampled. Opaque operations remain labeled evidence only. Normal radio banks are authored assessed-method operations. Hard rational-blank is an authored same-skill extension to thirds/quarters, with no observed hard label claimed.

See classification, extraction, per-asset plot evidence, labeled review and validation/native-grading results. `manifest.json` records SHA256 after private producers freeze; running generation later may append new assets and requires a refreshed manifest if those new artifacts are handed off.
