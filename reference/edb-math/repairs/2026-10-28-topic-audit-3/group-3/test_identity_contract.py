import copy,hashlib,importlib.util,json,os,random,sys,time
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;R=json.loads((H/'identity-contract-stage-plan.json').read_text());samples=[];checks=[]
def load(name,path):
 sys.modules.pop('math_format',None);sys.path.insert(0,str(path.parent));spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
before=load('contract_before',Path(R['source']));after=load('contract_after',Path(R['directory'])/R['entrypoint'])
selectors=sorted({(d['level'],d['template'])for sid,d in before.DEFS.items()if sid not in before.LEVEL_REPAIRS and d['template']!='identity_singular_radio'}|{('hard',before.HARD_MIXED_TEMPLATE)})
for i,(band,template)in enumerate(selectors):
 a=before.generate(band,seed=983700+i,template=template);b=after.generate(band,seed=983700+i,template=template);same=a==b;assert same,(band,template,'output changed');samples.append({'kp':R['kp'],'level':band,'record':b});checks.append({'band':band,'template':template,'all_output_bytes_and_UUIDs_unchanged':True})
# Cover every authored hard outcome with normal default API, preserving selection and IDs.
outcomes={}
for seed in range(60):
 a=before.generate_hard(seed=seed);b=after.generate_hard(seed=seed);assert a==b;kind=b['generation']['solution_class']
 if kind not in outcomes:outcomes[kind]=seed;samples.append({'kp':R['kp'],'level':'hard','record':b});checks.append({'band':'hard','default_seed':seed,'solution_class':kind,'all_output_bytes_and_UUIDs_unchanged':True})
 if len(outcomes)==3:break
assert len(outcomes)==3,outcomes
# The old authored bank explicitly declares identity profiles replay-only; fail before futile sampling.
errors=[]
for kwargs in[{'template':'identity_singular_radio'},{'template':'identity_singular_radio','profile':'authored:q-130626'}]:
 start=time.monotonic()
 try:after.generate_hard(seed=9837,**kwargs);raise AssertionError('must reject unsupported fresh identity selector')
 except ValueError as ex:
  text=str(ex);assert'replay_source(source_id)'in text and'mixed hard'in text;errors.append({'request':kwargs,'error':text,'seconds':time.monotonic()-start})
replays=[]
for sid in before.DEFS:
 a=before.replay_source(sid);b=after.replay_source(sid);assert a==b,(sid,'replay changed');replays.append({'source':sid,'all_retained_output_bytes_and_UUIDs_unchanged':True})
 # Raw/evidence replay is validated separately, never admitted as fresh learning.
# Independent determinant/residual/root-set calculation for every valid fresh sample.
math=[]
for i,sample in enumerate(samples):
 r=sample['record'];g=r['generation'];M=sp.Matrix([[sp.sympify(e)for e in row]for row in g['matrix']]);det=sp.expand(M.det());claimed=sp.sympify(g['determinant']);assert sp.simplify(det-claimed)==0;res=sp.sympify(g['residual']);unknown=list(res.free_symbols);roots=None if res==0 else sp.solve(res,unknown[0]);expected=g['roots'];expected=None if expected is None else[sp.sympify(v)for v in expected];assert(roots is None)==(expected is None)
 if roots is not None:assert len(roots)==len(expected)and all(any(sp.simplify(a-b)==0 for b in expected)for a in roots)
 math.append({'sample':i,'template':g['template'],'matrix_determinant':str(det),'residual':str(res),'solution_set':'all real numbers'if roots is None else list(map(str,roots)),'passed':True})
source_manifest=json.loads(Path(R['source']).with_name('generator-package.json').read_text());raw=[]
for name in source_manifest['files']:
 if name.endswith('.json')and name!='repair-evidence.json':
  a=Path(R['source']).parent/name;b=Path(R['directory'])/name;assert a.read_bytes()==b.read_bytes();raw.append({'file':name,'sha256':hashlib.sha256(a.read_bytes()).hexdigest()})
proof={'kp':R['kp'],'valid_selector_checks':checks,'normal_hard_outcomes':outcomes,'unsupported_fresh_identity_errors':errors,'source_replays':replays,'independent_determinant_rootset_checks':math,'raw_source_JSON_unchanged':raw,'VERSION_unchanged_because_all_valid_outputs_UUIDs_unchanged':before.VERSION==after.VERSION};(H/'identity-contract-proof.json').write_text(json.dumps(proof,indent=2));(H/'identity-contract-samples.json').write_text(json.dumps(samples,indent=2));print('valid selectors',len(selectors),'allhardoutcomes',outcomes,'replays',len(replays),'math',len(math),'allpass')
