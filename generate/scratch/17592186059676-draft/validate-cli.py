"""Private CLI contract checks; output changes only, no engine/EDB access."""
from pathlib import Path
import sys,json,subprocess,importlib.util
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('draft_tangent',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def run(*args):return subprocess.check_output([sys.executable,str(HERE.with_suffix('.py')),*args],text=True)
checks=[]
for level in (*g.SUPPORTED_LEVELS,'all'):
 for count in (1,2):
  args=('--difficulty',level,'--count',str(count),'--seed','7','--format','json');out=json.loads(run(*args));levels=g.SUPPORTED_LEVELS if level=='all' else [level]
  assert isinstance(out,list) and len(out)==len(levels)*count
  assert out==[rec for l in levels for rec in g.batch(l,count,7)]
  assert run(*args)==run(*args)
  checks.append({'difficulty':level,'count_per_level':count,'records':len(out),'top_level':'list','matches_public_API':True,'deterministic':True})
raw=json.loads(run('--difficulty','easy','--template','q-30990','--profile','observed_raw','--format','json'))
assert isinstance(raw,list) and len(raw)==1 and raw[0]['question']==g.SOURCES['q-30990']
markdown=run('--difficulty','all','--count','1','--seed','7','--format','markdown');assert markdown=='\n\n'.join(g.markdown(g.batch(l,1,7)[0]) for l in g.SUPPORTED_LEVELS)+'\n'
report={'passed':True,'scope':'CLI JSON top-level list; counts; difficulty order; deterministic/API equality; raw evidence omission preservation; existing Markdown output','normal_cases':checks,'raw_evidence_list':True,'markdown_unchanged':True,'database_writes':0}
(HERE/'cli-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('CLI contract passed:',len(checks),'normal cases plus raw and Markdown')
