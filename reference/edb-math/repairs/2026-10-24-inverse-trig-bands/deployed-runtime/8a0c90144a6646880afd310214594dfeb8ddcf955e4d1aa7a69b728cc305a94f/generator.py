#!/usr/bin/env python3
"""secant integration: repaired role-based generator; source evidence kept separately."""
from pathlib import Path
import sys
_here = Path(__file__).resolve().parent
_local = _here / 'inverse_trig.py'
sys.path.insert(0, str(_here if _local.exists() else _here.parent))
from inverse_trig import Generator
_evidence = _here / 'evidence.json'
if not _evidence.exists(): _evidence = Path(__file__).with_suffix('') / 'band-evidence.json'
_generator = Generator(_evidence)
KP_ID = _generator.kp
KP_UUID = _generator.kp_uuid
CASES = _generator.cases
SUPPORTED_LEVELS = ('easy', 'moderate', 'hard')
generate = _generator.generate
build = _generator.build
batch = _generator.batch
source_original = _generator.source_original
def generate_easy(seed=0, **kwargs): return generate('easy', seed, **kwargs)
def generate_moderate(seed=0, **kwargs): return generate('moderate', seed, **kwargs)
def generate_hard(seed=0, **kwargs): return generate('hard', seed, **kwargs)
if __name__ == '__main__': _generator.main()
