import importlib.util,json,random,sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True;H=Path(__file__).resolve().parent;R=json.loads((H/'identity-contract-stage-plan.json').read_text());mods=[]
for n,p in [('before',Path(R['source'])),('after',Path(R['directory'])/R['entrypoint'])]:
 sys.modules.pop('math_format',None);sys.path.insert(0,str(p.parent));spec=importlib.util.spec_from_file_location('identity_'+n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);mods.append(m)
before,after=mods;checks=[]
for sid,d in before.DEFS.items():
 if d['template']!='identity_singular_radio':continue
 p=before.parameters(sid);a=before.replay_source(sid)if sid in before.LEVEL_REPAIRS else before.generate_hard(profile=sid,parameters=p);b=after.replay_source(sid)if sid in after.LEVEL_REPAIRS else after.generate_hard(profile=sid,parameters=p);assert a==b;M,det,poly,roots,env=after.build(sid,p);assert det==0 and roots is None
 dependency='row2=-2row1'if sid=='q-130626'else'columns1and3dependent'
 assert all(sp.simplify(z)==0 for z in (M[1,:]+2*M[0,:] if sid=='q-130626'else M[:,0].cross(M[:,2])))
 for seed in range(4):
  M2,det2,poly2,roots2,_=after.build(sid,after.sample(sid,random.Random(seed)));assert det2==0 and roots2 is None
 checks.append({'source':sid,'nonauthored_profile_original_parameter_replay_bytes_and_UUIDs_unchanged':True,'determinant_identically_zero':True,'preserved_dependency':dependency,'why_no_authored_bank':'authored_bank refuses roots=None explicitly; the existing finite-root error recipes cannot create its required bank for this identity family. Default hard mixed has its own all-real-capable bank and remains valid.'})
(H/'identity-evidence-path-proof.json').write_text(json.dumps(checks,indent=2));print('identity rawprofiles',len(checks),'allpreserved; exact algebra dependencies proven')
