import json,shutil
from pathlib import Path
H=Path(__file__).resolve().parent;old=next(r for r in json.loads((H/'generator-candidates.json').read_text())if r['kp']==17592186129283);src=Path(old['directory']);dest=H/'generator-17592186129283-readonly';dest.mkdir(exist_ok=True)
for name in old['files']:
 out=dest/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src/name,out);out.chmod(0o644)
p=dest/'17592186129283/render.py';s=p.read_text();a="tmp_provenance=HERE/('render-provenance.tmp-'+uuid.uuid4().hex+'.json')";assert a in s;s=s.replace(a,"provenance_root=Path(os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',str(Path(sys.argv[1]).resolve().parent)))\nprovenance_root.mkdir(parents=True,exist_ok=True)\ntmp_provenance=provenance_root/('render-provenance.tmp-'+uuid.uuid4().hex+'.json')");s=s.replace("os.replace(tmp_provenance,HERE/'render-provenance.json')","os.replace(tmp_provenance,provenance_root/'render-provenance.json')");p.write_text(s)
ref=f"generators/{old['approved_digest'][:2]}/{old['approved_digest']}/{old['entrypoint']}";row={**old,'directory':str(dest),'old_reference':ref,'expected_old_reference':ref,'supersedes_digest':old['approved_digest']};row.pop('approved_digest');(H/'readonly-renderer-stage-plan.json').write_text(json.dumps(row,indent=2));print('staged read-only renderer successor',ref)
