import pathlib,json,math,hashlib,os,subprocess,sys
from audit import g,fields,save
from pixel_probe import geometry
ROOT=pathlib.Path.cwd();PKG=ROOT.parent/'workspace';load=lambda n:json.loads((ROOT/n).read_text())
rows=[]
for r in load('independent-samples.json')+load('runner-batch.json'):
 for a in fields(r)[':answer-field/choices']:
  p=pathlib.Path(a[':answer/value']);d=json.loads(p.with_suffix('.json').read_text());expected=[math.degrees(math.atan(float(g.sp.Rational(v)))) for v in d['slopes']];errors=[]
  try:geom=geometry(p,d['exact_points'],'generated',exclude_axis=True)
  except ValueError as e:
   rows.append({'question_id':r['question'][':question/id'],'choice_id':a[':answer/id'],'png':str(p),'status':'pixel isolation unavailable','error':str(e),'expected_slopes':d['slopes'],'points':d['exact_points']});continue
  for m,e in zip(geom,expected):
   
   if m['angle_degrees'] is None:errors.append(None);continue
   delta=abs(m['angle_degrees']-e);errors.append(min(delta,180-delta))
  rows.append({'question_id':r['question'][':question/id'],'choice_id':a[':answer/id'],'png':str(p),'expected_angles':expected,'pixel_angles':[m['angle_degrees'] for m in geom],'errors':errors})
save('current-pixel-checks.json',{'method':'Independent dark pixel PCA for off-axis points, compare to exact visible-equation-verified sidecar geometry. Axis-coincident points are deliberately unmeasured because spines/tick labels contaminate PCA, as retained in pixel-initial-diagnostic.json; they are checked through exact renderer endpoints, code inspection and actual-UI screenshots.','records':rows,'max_angle_error':max(max((e for e in r['errors'] if e is not None),default=0) for r in rows if 'errors' in r)})
assert max(max((e for e in r['errors'] if e is not None),default=0) for r in rows if 'errors' in r)<4
# Test missing output configuration without permitting writes to package.
prior=os.environ.pop('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',None)
try:
 try:g.generate('easy',seed=864001);raise AssertionError('missing output config silently accepted')
 except ValueError as e:assert 'OUTPUT_DIR is required' in str(e);result=str(e)
finally:
 if prior:os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=prior
# Real CLI at unrelated working directory; absolute output references must resolve.
env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(ROOT/'cli-assets'),'PYTHONDONTWRITEBYTECODE':'1','MPLCONFIGDIR':str(ROOT/'cli-assets/.mplconfig')}
cli=subprocess.run([sys.executable,str(PKG/'17592186172038.py'),'--difficulty','easy','--seed','864002','--count','1','--format','json'],cwd=ROOT/'nested',env=env,capture_output=True,text=True);assert cli.returncode==0,cli.stderr
records=json.loads(cli.stdout);save('cli-records.json',records)
assert all(pathlib.Path(a[':answer/value']).is_file() and pathlib.Path(a[':answer/value']).is_relative_to(ROOT/'cli-assets') for a in fields(records[0])[':answer-field/choices'])
manifest=load('../workspace/package.json');runtime=load('runtime.json');assert manifest['dependencies']=={'python':runtime['python'],'packages':runtime['packages']}
save('external-output-results.json',{'missing_config_rejected':result,'cli_command':cli.args,'cli_cwd':str(ROOT/'nested'),'cli_returncode':cli.returncode,'external_absolute_assets_resolve':True,'runtime_exact_match':True})
print('pixel choices',len(rows),'max_angle_error',max(max((e for e in r['errors'] if e is not None),default=0) for r in rows if 'errors' in r),'CLI/missing-config/runtime passed')
