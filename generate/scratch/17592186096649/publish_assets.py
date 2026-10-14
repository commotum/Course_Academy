"""Publish this KP's validated plots through the existing image library."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from capture.scripts.database.images import ImageLibrary
from inventory_jobs import save
path=Path(sys.argv[1]);assert path.resolve().is_relative_to(HERE/'reference/replenishment')
records=json.loads((path/'generated-local.json').read_text());library=ImageLibrary(Path('/media/jake/SSD/EDB/math'),ROOT)
for rec in records:
    assert rec['knowledge_point']['db_id']==17592186096649
    q=rec['question']
    for key in (':question/problem',':question/worked-solution'):q[key]=library.text(q[key])
    for field in q[':question/answer-fields']:
        for a in field[':answer-field/choices']:a[':answer/value']=library.resolve(a[':answer/value'])
# Transform metadata paths too; keep every UUID from the frozen generator.
def rewrite(obj):
    if isinstance(obj,dict):return {library.saved.get(k,{}).get('path',k):rewrite(v) for k,v in obj.items()}
    if isinstance(obj,list):return [rewrite(v) for v in obj]
    if isinstance(obj,str):return library.saved.get(obj,{}).get('path',obj)
    return obj
records=rewrite(records);save(path/'assets.json',library.saved);save(path/'generated.json',records)
print('Published and verified '+str(len(library.saved))+' plot assets.',flush=True)
