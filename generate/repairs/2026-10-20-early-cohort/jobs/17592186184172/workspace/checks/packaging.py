"""Retained legacy_packaging_or_sampling failure: exercise declared closure."""
import json
from pathlib import Path
from validate import relocation
if __name__=='__main__':
 result=relocation()
 Path(__file__).resolve().parents[1].joinpath('evidence/relocation.json').write_text(json.dumps(result,indent=2)+'\n')
 print('Relocated manifest-only moderate/hard CLI: pass')
