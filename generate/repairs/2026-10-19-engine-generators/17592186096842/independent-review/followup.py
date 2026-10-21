from audit import *
import copy
samples=json.loads(Path('samples.json').read_text()); runner=json.loads(Path('runner-batch.json').read_text()); cf=json.loads(Path('counterfactual-records.json').read_text()); replay=json.loads(Path('source-replay.json').read_text())
cases=[]
for r in samples[::10]+runner+cf:
 f=field(r);checks=[];v=correct(r);ans=expected(r)[2]
 if f[':answer-field/type'].endswith('/radio'):
  for a in f[':answer-field/choices']:checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if equivalent(untex(a[':answer/value']),ans) else 'rejected','purpose':'independent derivative determines choice'})
 else:
  checks=[{'submitted':v,'expected':'accepted','purpose':'canonical independently differentiated answer'},{'submitted':'('+v+')*2/2','expected':'accepted','purpose':'same-domain scalar equivalent'},{'submitted':'1' if ans==0 else '0','expected':'rejected','purpose':'plausible missing chain factor / zero response'}]
 cases.append({'label':r['generation']['template']+' seed '+str(r['generation']['seed'])+' '+str(len(cases)),'record':r,'checks':checks})
# Power representation is taught in q-342764 and explicitly used in all reciprocal solutions.
r=g.generate('moderate',seed=881109,template='reciprocal_blank',parameters={'a':2,'b':-6})
cases.append({'label':'valid reciprocal fractional-power equivalent','record':r,'checks':[{'submitted':r'-\frac{1}{(2x-6)^{3/2}}','expected':'accepted','purpose':'Same real domain and derivative; engine regression must pass.'}]})
save('grader-input.json',cases)
# Explicit canonical restriction and role-independent scope boundaries.
try:
 g.generate('hard',template='sqrt_quadratic_blank',parameters={'a':-1,'b':0,'c':1})
 restriction={'canonical_e182_rejected':False}
except ValueError as e:restriction={'canonical_e182_rejected':True,'exception':str(e),'parameters':{'a':-1,'b':0,'c':1},'expected':'-x/sqrt(1-x**2)','source':'e-182 (8fcdb2c8-71ca-5bfa-b7fe-49f8f2c05bbb), lesson step 17592186097785'}
save('restriction-results.json',restriction)
# Package relocation uses only files declared in manifest and a cwd unrelated to package.
manifest=json.loads((PKG/'package.json').read_text());relocated=ROOT/'relocated';relocated.mkdir(exist_ok=True)
for name in manifest['files']:
 dest=relocated/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PKG/name,dest)
cmd=[PY,'-B',str(relocated/'generator.py'),'--difficulty','moderate','--seed','617803','--count','5']
p=subprocess.run(cmd,capture_output=True,text=True,cwd=ROOT);Path('relocation.stdout').write_text(p.stdout);Path('relocation.stderr').write_text(p.stderr)
ref=[g.generate('moderate',seed=617803+i) for i in range(5)]
save('relocation-results.json',{'command':cmd,'exit_code':p.returncode,'same_records':json.loads(p.stdout)==ref if p.returncode==0 else False,'declared_files':manifest['files'],'outside_package_import':'sympy only; local math_format and data files copied','asset_outputs':'none'})
# Source solution differences with stage judgments; formatting/reductions do not constitute failures.
sources={q[':question/math-academy-id']:q for q in json.loads((ROOT.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']}
diffs=[]
for r in replay:
 sid=r['generation']['replay_source_id'];s0=sources[sid].get(':question/worked-solution','');s1=r['question'][':question/worked-solution']
 if '={u}^{1/2}' in s0 and '={u}^{1/2}' not in s1:
  diffs.append({'source_id':sid,'missing_stage':'Rewrite sqrt(u) as u^(1/2) and differentiate as (1/2)u^(-1/2) before radical form','source_solution':s0,'generated_solution':s1})
save('source-solution-stage-results.json',{'omissions':diffs,'other_differences':'Reviewed q-107360, q-314192, q-342792, q-342789, q-20181, q-48848, q-342787: equivalent factor cancellation, explicit substitution steps and harmless presentation changes.'})
print('grader cases',len(cases),'restriction',restriction['canonical_e182_rejected'],'missing source power stages',[d['source_id'] for d in diffs],'relocation',p.returncode)
