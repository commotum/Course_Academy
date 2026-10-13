"""Publish this KP's verified image bytes with the existing ImageLibrary.

Use system Python, where the installed Pillow build matches its interpreter.
The frozen generator runs in the existing SymPy environment.
"""
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'scripts'))
from capture.scripts.database.images import ImageLibrary
from inventory_jobs import save

path=Path(sys.argv[1])
assert path.resolve().is_relative_to(HERE/'reference/replenishment')
records=json.loads((path/'generated-local.json').read_text())
library=ImageLibrary(Path('/media/jake/SSD/EDB/math'),HERE)
for rec in records:
    assert rec['knowledge_point']['db_id']==17592186087819
    for key in (':question/problem',':question/worked-solution'):
        rec['question'][key]=library.text(rec['question'][key])
save(path/'assets.json',library.saved)
save(path/'generated.json',records)
print(f'Published and verified {len(library.saved)} image assets.',flush=True)
