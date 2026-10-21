from pathlib import Path
import shutil,json
E=Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';prev=J/'review-0-policy-2-4c6625aaf57ad834'
(E/'runtime/tmp').mkdir(parents=True,exist_ok=True)
# package-copy contains exact current files; bytecode and assets go elsewhere.
PK=E/'runtime/package'
if not PK.exists():shutil.copytree(W,PK,ignore=shutil.ignore_patterns('evidence','__pycache__'))
shutil.copyfile(J/'samples.json',E/'batch-records.json')
helper=(prev/'review.py').read_text().split("if __name__=='__main__':")[0]
helper=helper.replace("'TMPDIR':str(RT/'tmp')","'TMPDIR':str(RT/'tmp'),'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(E/'assets')")
(E/'review.py').write_text(helper)
sample=(prev/'sample.py').read_text().replace('[891273,560834,190427,378213,601902]','[426107,913582,657903]')
sample=sample.replace("# independently use the explicit source x+y to replay canonical easy method; no canonical bank replay API exists.","# Retained canonical failing case now replayed explicitly.")
sample=sample.replace("canonical=g.generate('easy',seed=991,template='possible_linear',parameters=p)","canonical=g.generate('easy',seed=991,profile='e-8507')")
(E/'sample.py').write_text(sample)
for n in ['boundary-probes.py','finish-tests.py','audit-evidence.py','relocation-check.py']:
 s=(prev/n).read_text().replace("PK/KP,'--math-root'","E/'assets','--asset-root',PK/KP,'--math-root'")
 if n=='relocation-check.py': s=s.replace("PK/KP,'--math-root'","E/'assets','--asset-root',PK/KP,'--math-root'")
 if n=='finish-tests.py':
  s=s.split("dump('dependencies.json'")[0]
 (E/n).write_text(s)
# Independent probes retained with provenance, author regression scripts adapted only for output location.
for n in ['cold_dependency_probe.py','canonical_replay_probe.py']:
 s=(W/'checks'/n).read_text()
 s=s.replace("W=pathlib.Path(__file__).resolve().parents[1]", "ROOT=pathlib.Path(__file__).resolve().parent\nW=pathlib.Path(os.environ.get('REVIEW_PACKAGE',str(ROOT.parent/'workspace')))") if n.startswith('cold') else s.replace('import importlib.util,json,pathlib,re,sys','import importlib.util,json,pathlib,re,sys,os').replace("W=pathlib.Path(__file__).resolve().parents[1];E=W/'evidence';E.mkdir(exist_ok=True)","ROOT=pathlib.Path(__file__).resolve().parent\nW=pathlib.Path(os.environ.get('REVIEW_PACKAGE',str(ROOT.parent/'workspace')))\nE=ROOT/os.environ.get('REVIEW_CASE','retained-canonical');E.mkdir(exist_ok=True)")
 s=s.replace("E=W/'evidence';E.mkdir(exist_ok=True)","E=ROOT/os.environ.get('REVIEW_CASE','retained-cold');E.mkdir(exist_ok=True)")
 s=s.replace("'--tmpfs','/tmp'", "'--bind',str(E/'tmp'),'/tmp'")
 if n.startswith('cold'): s=s.replace("manifest=json.loads", "(E/'tmp').mkdir(exist_ok=True)\nmanifest=json.loads")
 (E/('retained-'+n)).write_text(s)
(E/'test-provenance.json').write_text(json.dumps({'reused_independent_scripts':str(prev),'adaptations':['evidence paths relative to new review','fresh seeds 426107,913582,657903','canonical profile now explicit','external output directory for changed contract'],'retained_author_regression_scripts':str(W/'checks'),'verification':'scripts inspected; run against current and earlier failing package, with outputs redirected solely to this review'},indent=2))
