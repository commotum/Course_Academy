#!/usr/bin/env python3
"""Repaired KP 17592186068917: controlled substitution practice."""
import json
from pathlib import Path
import sys
LOCAL=Path(__file__).with_suffix('')
if not (LOCAL/'trig_substitution.py').is_file(): LOCAL=Path(__file__).resolve().parent
sys.path.insert(0,str(LOCAL))
import trig_substitution as model
KP=17592186068917
EVIDENCE=json.loads((LOCAL/'source-evidence.json').read_text())
def generate(level,seed=0,template=None,**kwargs):
    return model.generate(KP,level,seed,template,evidence=EVIDENCE,**kwargs)
def batch(level,count=8,seed=0,template=None):
    return model.batch(KP,level,count,seed,evidence=EVIDENCE,template=template)
if __name__=='__main__': model.cli(KP,LOCAL)
