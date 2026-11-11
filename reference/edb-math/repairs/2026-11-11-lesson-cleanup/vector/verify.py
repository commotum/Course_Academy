"""Bounded actual delivery, independent exact math, native grading and paired UI."""
import json,os,subprocess,sys,hashlib,copy,shutil,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from generate.pipeline.check_delivery import audit
from scripts.generator_packages import build_manifest,manifest_digest
from scripts.generator_publish import answer_id,enum
AUDIT=ROOT/'generate/reports/lesson-quality-audit-2026-11-11/vector'
spec=importlib.util.spec_from_file_location('audit_math',AUDIT/'math_native.py');math=importlib.util.module_from_spec(spec);spec.loader.exec_module(math)
def read(p):return json.loads(Path(p).read_text())
def save(p,x):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def native_case(kp,r,label):
 vals=math.expected(kp,r);fs=sorted(r['question'][':question/answer-fields'],key=lambda f:f[':answer-field/key']);checks=[]
 if kp==17592186096653 and enum(fs[0][':answer-field/type'])==':answer-field.type/radio':
  p=r['generation']['parameters'];assert math.coeffs(next(a for a in fs[0][':answer-field/choices'] if a[':answer/id']==answer_id(fs[0][':answer-field/correct']))[':answer/value'])=={p['u']:vals[0],p['v']:vals[1]}
 else:
  for f,v in zip(fs,vals):assert math.number(next(a for a in f[':answer-field/choices'] if a[':answer/id']==answer_id(f[':answer-field/correct']))[':answer/value'])==v
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  if enum(f[':answer-field/type'])==':answer-field.type/radio':
   for a in f[':answer-field/choices']:checks.append(dict(field_index=fi,submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==answer_id(f[':answer-field/correct']) else 'rejected',purpose='Independent exact geometry/ordered-ratio calculation; every actual offered choice'))
  else:
   v=vals[int(f[':answer-field/key'].split('-')[-1])-1] if len(vals)>1 else vals[0]
   checks.extend([dict(field_index=fi,submitted=str(v),expected='accepted',purpose='Independent exact calculation'),dict(field_index=fi,submitted=f'{v.numerator*2}/{v.denominator*2}',expected='accepted',control='equivalent',purpose='Unreduced equivalent rational'),dict(field_index=fi,submitted=str(-v),expected='rejected',control='wrong',purpose='Wrong sign'),dict(field_index=fi,submitted=str(v+1),expected='rejected',control='wrong',purpose='Wrong magnitude')])
 return dict(label=label,record=r,checks=checks)
def run(kp):
 d=H/str(kp);package=d/'package';manifest=read(package/'package.json');source=read(d/'source-before/source.json');inv=read(d/'capture/inventory.json')
 cases=[];summary=[]
 for band in ['easy','moderate','hard']:
  out=d/'verification'/band;assets=out/'assets';assets.mkdir(parents=True,exist_ok=True)
  command=[sys.executable,str(package/'generator.py'),'--difficulty',band,'--count','8','--seed','20261112','--format','json']
  if not (out/'records.json').exists():
   records=json.loads(subprocess.check_output(command,env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(assets),'MPLCONFIGDIR':str(out/'mpl')},timeout=300));save(out/'records.json',records)
  records=read(out/'records.json');delivery=audit(records,inv,source,band,out/'delivery',assets,Path('/media/jake/SSD/EDB/math'));accepted=read(out/'delivery/accepted.json');assert len(accepted)>=5
  n=[native_case(kp,r,band+':'+str(i)) for i,r in enumerate(accepted)];save(out/'native-input.json',n)
  subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(out/'native-input.json'),str(out/'native-report.json')],check=True,timeout=240)
  save(out/'math.json',dict(passed=True,method='Exact determinant/ordered ratio independently derived from renderer geometry and displayed givens',records=len(accepted)))
  # All actual survivors are final publication candidates; inspect both states
  # at narrow and desktop widths, not a separately reconstructed fixture.
  subprocess.run([sys.executable,str(ROOT/'generate/pipeline/render_preview.py'),'--input',str(out/'delivery/accepted.json'),'--output',str(out/'render'),'--asset-root',str(out/'delivery/assets'),'--viewport','390x1000','--viewport','1100x1000'],check=True,timeout=300)
  summary.append(dict(band=band,raw=len(records),delivered=len(accepted),native=read(out/'native-report.json')['passed'],ui=read(out/'render/rendering.json')['passed']))
  print(kp,summary[-1],flush=True)
 # Regenerate exact original seed/count counterexamples preserving original
 # parameter stream. These records are filtered through actual delivery too.
 if kp in [17592186096652,17592186096701]:
  regress=[('hard',20261111,1)] if kp==17592186096652 else [('moderate',47,2),('hard',47,3)]
  for band,seed,idx in regress:
   out=d/'counterexamples'/f'{band}-{seed}';assets=out/'assets';assets.mkdir(parents=True,exist_ok=True)
   rows=json.loads(subprocess.check_output([sys.executable,str(package/'generator.py'),'--difficulty',band,'--count','4','--seed',str(seed),'--format','json'],env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(assets),'MPLCONFIGDIR':str(out/'mpl')},timeout=180));save(out/'records.json',rows)
   audit(rows,inv,source,band,out/'delivery',assets,Path('/media/jake/SSD/EDB/math'));delivered=read(out/'delivery/accepted.json');assert len(delivered)==4
   old=read(AUDIT/str(kp)/'samples'/band/str(seed)/'records.json')[idx]['generation'];new=rows[idx]['generation']
   oldp=old.get('instance',old.get('parameters'));newp=new.get('instance',new.get('parameters'))
   assert {k:v for k,v in oldp.items() if k!='renderer_version'}=={k:v for k,v in newp.items() if k!='renderer_version'},'Counterexample mathematical geometry changed'
   subprocess.run([sys.executable,str(ROOT/'generate/pipeline/render_preview.py'),'--input',str(out/'delivery/accepted.json'),'--output',str(out/'render'),'--asset-root',str(out/'delivery/assets'),'--indices',str(idx),'--viewport','390x1000','--viewport','1100x1000'],check=True,timeout=180)
   save(out/'regression.json',dict(passed=True,index=idx,geometry_unchanged=True,old_record_file=str(AUDIT/str(kp)/'samples'/band/str(seed)/'records.json'),new_record_file=str(out/'delivery/accepted.json')))
 save(d/'verification-summary.json',dict(passed=True,bands=summary))
 save(d/'package-candidate.json',dict(sha256=manifest_digest(build_manifest(package,manifest['entrypoint'],manifest['files'],dependencies=manifest['dependencies']))))
if __name__=='__main__':run(int(sys.argv[1]))
