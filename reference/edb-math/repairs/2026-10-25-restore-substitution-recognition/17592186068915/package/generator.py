#!/usr/bin/env python3
"""KP 17592186068915: scaffolded substitution with controlled prerequisite work."""
import json
from pathlib import Path
import sys
LOCAL=Path(__file__).with_suffix('')
if not (LOCAL/'trig_scaffold.py').is_file():LOCAL=Path(__file__).resolve().parent
sys.path.insert(0,str(LOCAL))
import trig_scaffold as model
KP=17592186068915
EVIDENCE=json.loads((LOCAL/'source-evidence.json').read_text())
def generate(level,seed=0,template=None,**kwargs):
    return model.generate(KP,level,seed,template,evidence=EVIDENCE,**kwargs)
def batch(level,count=8,seed=0,template=None):
    return model.batch(KP,level,count,seed,evidence=EVIDENCE,template=template)
if __name__=='__main__':model.cli(KP,LOCAL)
