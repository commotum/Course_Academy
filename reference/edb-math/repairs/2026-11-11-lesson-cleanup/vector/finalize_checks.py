import argparse,copy,hashlib,importlib.util,json,os,re,subprocess,sys,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from scripts.generator_packages import build_manifest,manifest_digest
from scripts.generator_refill_plan import validate_refill_plan
from scripts.generator_refill import validate_survivors
from scripts.generator_publish import digest
from generate.pipeline.check_delivery import audit

def read(p):return json.loads(Path(p).read_text())
def save(p,x):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def main(kp):
 d=H/str(kp);package=d/'package';manifest=read(package/'package.json');plan=read(package/'refill-review-plan.json');findings=[dict(id=x) for row in plan['checks'] for x in row['finding_ids']]
 binding=validate_refill_plan(package,manifest,findings,d/'review');source=read(d/'source/source.json');inv=read(d/'capture-after-retirement/inventory.json');summary=[]
 for band in ['easy','moderate','hard']:
  out=d/'verification'/band;rows=read(out/'records.json');previous=read(out/'delivery/accepted.json')
  result=audit(rows,inv,source,band,out/'delivery-postretirement',out/'assets',Path('/media/jake/SSD/EDB/math'));actual=read(out/'delivery-postretirement/accepted.json');assert actual==previous,'Final post-retirement delivery changed reviewed UI/native objects'
  result=validate_survivors(actual,inv,out/'refill',root=package,manifest=manifest,band=band,python=sys.executable,repo_root=ROOT,environment=os.environ.copy(),expected_plan=binding);assert result['status']=='passed'
  summary.append(dict(band=band,raw=len(rows),delivered=len(actual),postretirement_exact_objects_unchanged=True,refill_status=result['status']))
  print(kp,band,'refill passed',flush=True)
 sys.path.insert(0,str(package));spec=importlib.util.spec_from_file_location('checks',package/'check_refill.py');checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)
 r=read(d/'verification/easy/delivery-postretirement/accepted.json')[0];mutations=[]
 x=copy.deepcopy(r);x['question'][':question/problem']+=' The path is drawn.';mutations.append(('supplied-route-prose',x))
 x=copy.deepcopy(r);f=x['question'][':question/answer-fields'][0];key=checks.answer_id(f[':answer-field/correct']);next(a for a in f[':answer-field/choices'] if a[':answer/id']==key)[':answer/value']='37';mutations.append(('wrong-key',x))
 if kp in [17592186096652,17592186096701]:
  x=copy.deepcopy(r);pr=x['question'][':question/problem'];sol=x['question'][':question/worked-solution'];a=re.search(r'!\[[^]]*\]\(([^)]+)\)',pr)[1];b=re.search(r'!\[[^]]*\]\(([^)]+)\)',sol)[1];x['question'][':question/problem']=pr.replace(a,b);mutations.append(('solution-image-before-answer',x))
  # Old ambiguity is retained as the exact old delivered image at unchanged
  # counterexample geometry, and must fail the current renderer/role binding.
  band,seed,idx=('hard',20261111,1) if kp==17592186096652 else ('hard',47,3)
  current=read(d/'counterexamples'/f'{band}-{seed}'/'delivery/accepted.json')[idx];old=read(ROOT/'generate/reports/lesson-quality-audit-2026-11-11/vector'/str(kp)/'samples'/band/str(seed)/'delivery/accepted.json')[idx]
  x=copy.deepcopy(current);oldref=re.search(r'!\[[^]]*\]\(([^)]+)\)',old['question'][':question/problem'])[1];newref=re.search(r'!\[[^]]*\]\(([^)]+)\)',x['question'][':question/problem'])[1];x['question'][':question/problem']=x['question'][':question/problem'].replace(newref,oldref);mutations.append(('retained-old-ambiguous-reference-image',x))
 results=[]
 with tempfile.TemporaryDirectory(prefix='vector-refill-regressions-') as t:
  checks.check(r,Path(t)/'good')
  for name,x in mutations:
   try:checks.check(x,Path(t)/name)
   except (AssertionError,ValueError,StopIteration) as e:results.append(dict(id=name,rejected=True,reason=str(e)))
   else:raise AssertionError('Regression mutation passed: '+name)
 save(d/'refill-regressions.json',dict(passed=True,mutations=results))
 save(d/'package-candidate.json',dict(sha256=manifest_digest(build_manifest(package,manifest['entrypoint'],manifest['files'],dependencies=manifest['dependencies'])),refill_plan=binding))
 save(d/'preflight-verification.json',dict(passed=True,bands=summary,regressions=results,source_sha256=source['source_sha256'],database_writes=0))
if __name__=='__main__':main(int(sys.argv[1]))
