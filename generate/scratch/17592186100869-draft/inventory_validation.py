"""Revalidate the frozen generator with current grading; no durable mutations."""
import ast,copy,hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2];OUT=D/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('g00869',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Reuse the independently written display parser without the old run's global
# baseline assertions (those deliberately required no registration at stage 7).
module=ast.parse((D/'validate.py').read_text());defs=[n for n in module.body if isinstance(n,ast.FunctionDef)]
exec(compile(ast.Module(body=defs,type_ignores=[]),str(D/'validate.py'),'exec'))

def checks(rec):
 return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Complete Boolean bank'} for i,f in enumerate(rec['question'][':question/answer-fields']) for a in f[':answer-field/choices']]

def item(rec,label=None):
 truth=read_display(rec)
 return {'label':label or rec['question'][':question/id'],'record':rec,'checks':checks(rec),'subset_expected':[all(bool(mask&(1<<i))==v for i,v in enumerate(truth)) for mask in range(8)]}

def native(records,path):
 path.mkdir(parents=True,exist_ok=True)
 (path/'native-input.json').write_text(json.dumps([item(r) for r in records]))
 subprocess.run([str(OUT/'current-whole-check'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)

def main():
 frozen=json.loads((D/'freeze.json').read_text());assert hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()==frozen['script_sha256']
 records=[];banks=0
 for c in json.loads((D/'source-cases.json').read_text()):
  r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);read_display(r)
  old=g.SOURCES[c['template']];q=r['question']
  assert q[':question/problem']==g.normalize_prose(old[':question/problem'])
  assert q[':question/worked-solution']==g.normalize_prose(old[':question/worked-solution'])
  for f in q[':question/answer-fields']:
   source=next(x for x in old[':question/answer-fields'] if x[':answer-field/key']==f[':answer-field/key'])
   assert sorted(a[':answer/value'] for a in source[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
   assert source[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);banks+=1
  records.append(r)
 coverage={};changed=0
 for level in g.LEVELS:
  slots=set();fps=set()
  for seed in range(240):
   r=g.generate(level,seed);read_display(r);records.append(r);slots.update(tuple(p) for p in r['generation']['parameters']['products']);fps.add(r['generation']['task_fingerprint'])
   assert g.generate(level,seed)==r
   assert g.generate(level,seed+1000,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile'])['question']==r['question']
  assert slots==set(itertools.permutations(range(3),2)) and len(fps)>150
  base=g.generate(level,19)
  for pairs in itertools.permutations(list(itertools.permutations(range(3),2)),3):
   p=copy.deepcopy(base['generation']['parameters']);p['products']=list(map(list,pairs))
   try:r=g.generate(level,template=base['generation']['template'],parameters=p)
   except ValueError:assert level=='hard';continue
   read_display(r);changed+=1
  coverage[level]={'ordered_pair_slots':sorted(slots),'distinct_tasks':len(fps)}
 rendered=json.loads((D/'render-validation.json').read_text())
 for x in rendered['reports']:
  r=x['exact_record'];m=r['generation'];assert g.generate(m['level'],m['seed'],template=m['template'],parameters=m['parameters'],profile=m['profile'])==r
  assert hashlib.sha256((D/x['screenshot']).read_bytes()).hexdigest()==x['screenshot_sha256'];records.append(r)
 subprocess.run(['cargo','build','--release','--lib','--offline'],cwd=ROOT,check=True)
 deps=ROOT/'target/release/deps';lib=max(deps.glob('libcourse_academy_engine-*.rlib'),key=lambda p:p.stat().st_mtime_ns);serde=max(deps.glob('libserde_json-*.rlib'),key=lambda p:p.stat().st_mtime_ns)
 cmd=['rustc','--edition=2024',str(D/'whole-check.rs'),'-L','dependency='+str(deps),'--extern','course_academy_engine='+str(lib),'--extern','serde_json='+str(serde),'-o',str(OUT/'current-whole-check')]
 subprocess.run(cmd,check=True);native(records,OUT/'validation')
 report={'passed':True,'script':str(D.with_suffix('.py').relative_to(ROOT)),'script_sha256':frozen['script_sha256'],'source_questions':10,'source_banks_matched':banks,'source_choices_matched':banks*2,'sampled_records':720,'fixed_arrays_changed_target_checks':changed,'coverage':coverage,'render_records_exact_replay':len(rendered['reports']),'current_native_records':len(records),'native_field_checks':len(records)*6,'whole_question_subsets':len(records)*8,'current_library_sha256':hashlib.sha256(lib.read_bytes()).hexdigest(),'build_command':cmd,'sympy_version':__import__('sympy').__version__,'python_version':sys.version,'unsupported_levels':[],'hard':'Explicitly authored mixed row/column vector band; bounded same comparison rule, supported by extraction and canonical example.'}
 (OUT/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='build_command'}))
if __name__=='__main__':main()
