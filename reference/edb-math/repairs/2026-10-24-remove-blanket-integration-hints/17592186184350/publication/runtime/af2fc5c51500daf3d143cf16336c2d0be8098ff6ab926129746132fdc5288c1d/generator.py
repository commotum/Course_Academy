#!/usr/bin/env python3
"""KP 17592186184350: scaffolded substitution."""
import json
from pathlib import Path
import sys
LOCAL=Path(__file__).with_suffix('')
if not (LOCAL/'substitution_pedagogy.py').is_file():LOCAL=Path(__file__).resolve().parent
sys.path.insert(0,str(LOCAL))
import substitution_pedagogy as model
KP=17592186184350
EVIDENCE=json.loads((LOCAL/'source-evidence.json').read_text())
def generate(level,seed=0,template=None,**kwargs):return model.generate(KP,level,seed,template,evidence=EVIDENCE,**kwargs)
def batch(level,count=8,seed=0,template=None):return model.batch(KP,level,count,seed,evidence=EVIDENCE,template=template)
if __name__=='__main__':model.cli(KP,LOCAL)
