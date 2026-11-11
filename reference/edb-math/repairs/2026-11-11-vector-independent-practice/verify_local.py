"""Validate actual publication survivors and relocation without database writes."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

H=Path(__file__).resolve().parent
ROOT=H.parents[3]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts'),str(H/'package')]
from scripts.generator_native_build import ensure_native_grader
from scripts.generator_packages import build_manifest,manifest_digest
from scripts.generator_refill import validate_survivors
from scripts.generator_refill_plan import validate_refill_plan
from scripts.generator_publish import normalized_question,content_fingerprint,localize_record
from generate.pipeline.check_delivery import audit,AuditImages

def read(p):return json.loads(Path(p).read_text())
def save(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')

package=H/'package';manifest=read(package/'package.json')
save(H/'native-build.json',ensure_native_grader(ROOT))
binding=validate_refill_plan(package,manifest,[dict(id='premature-vector-construction')],H/'review')
source=read(H/'source/source.json');inventory=read(H/'capture/inventory.json')
summary=[]
with tempfile.TemporaryDirectory(prefix='vector-package-relocation-') as temporary:
    relocated=Path(temporary)/'package';relocated.mkdir()
    for name in manifest['files']:shutil.copy2(package/name,relocated/name)
    for band in ['easy','moderate','hard']:
        directory=H/'verification'/band;directory.mkdir(parents=True,exist_ok=True)
        assets=directory/'plots';env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(assets)}
        command=[sys.executable,str(package/'generator.py'),'--difficulty',band,'--count','12','--seed','20261111','--format','json']
        records=json.loads(subprocess.check_output(command,env=env));save(directory/'records.json',records)
        relocated_assets=Path(temporary)/band
        repeated=json.loads(subprocess.check_output([sys.executable,str(relocated/'generator.py'),*command[2:]],env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(relocated_assets)},cwd=relocated))
        assert records==repeated
        assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in assets.glob('*.png')}=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in relocated_assets.glob('*.png')}
        delivery=audit(records,inventory,source,band,directory/'delivery',assets,Path('/media/jake/SSD/EDB/math'))
        survivors=read(directory/'delivery/accepted.json')
        report=validate_survivors(survivors,inventory,directory/'refill',root=package,manifest=manifest,band=band,python=sys.executable,repo_root=ROOT,environment=os.environ.copy(),expected_plan=binding)
        assert report['status']=='passed'
        summary.append(dict(band=band,records=len(records),survivors=len(survivors),deterministic_relocation=True,asset_bytes_identical=True,refill_status=report['status']))
        print(band,summary[-1],flush=True)

# Preserve all field and answer identities on the one stored repair.
import generator
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(H/'stored/plots')
q=next(q for q in read(H/'capture/kp.json')[':knowledge-point/questions'] if q[':db/id']==17592186735164)
p={'a':[2,0],'b':[1,1],'k':'2','r':'1'}
assets=generator.render_plots(p)
proposed=copy.deepcopy(q)
proposed[':question/problem']='The three vectors share an origin, and each grid square has the same side length.\n\n![]('+assets['prompt']+')\n\nGiven $\\mathbf{c}=\\lambda\\mathbf{a}+2\\mathbf{b}$, find $\\lambda$.'
old_asset='images/ce/cee2a501a390c40bc1100336ff4a7cda3e7a070dff7dc0470b1762833a7a677a.png'
proposed[':question/worked-solution']='Draw $2\\mathbf{b}$ from the common origin $O$ to a point $P$, then complete the path from $P$ to the endpoint $C$ of $\\mathbf{c}$.\n\n![]('+old_asset+')\n\n'+q[':question/worked-solution'].replace('Following the drawn path gives','Adding the two path vectors gives')
record={'knowledge_point':{'db_id':17592186235285,'id':'58a49d00-cc58-5228-af38-9369cf31d8c8'},'question':normalized_question(proposed)}
record=localize_record(record,H/'stored/assets',H/'stored/plots',library=AuditImages(H/'stored/assets',H/'stored/plots',Path('/media/jake/SSD/EDB/math')))
proposed[':question/problem']=record['question'][':question/problem'];proposed[':question/worked-solution']=record['question'][':question/worked-solution']
assert proposed[':question/answer-fields']==q[':question/answer-fields']
save(H/'stored/before.json',q);save(H/'stored/proposed.json',proposed);save(H/'stored/records.json',[record])
checks=[]
field=record['question'][':question/answer-fields'][0]
for a in field[':answer-field/choices']:
    checks.append(dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/value']=='-1' else 'rejected',purpose='Stored choices preserve the independently counted negative unit coefficient'))
save(H/'stored/engine-input.json',[dict(label='stored-repair',record=record,checks=checks)])
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'stored/engine-input.json'),str(H/'stored/engine-report.json')],check=True)
save(H/'package-candidate.json',dict(sha256=manifest_digest(build_manifest(package,manifest['entrypoint'],manifest['files'],dependencies=manifest['dependencies'])),refill_plan=binding))
save(H/'preflight-verification.json',dict(passed=True,database_writes=0,bands=summary,stored_key_and_fields_unchanged=True))
