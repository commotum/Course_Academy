from pathlib import Path
import json,sys,shutil,copy
ROOT=Path('/home/jake/Developer/Course_Academy');sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from scripts.generator_packages import build_manifest,manifest_digest
H=ROOT/'reference/edb-math/repairs/2026-11-11-lesson-cleanup/normal';M=Path('/media/jake/SSD/EDB/math')
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
for kp in [17592186092384,17592186092385]:
 D=H/str(kp);old=json.loads((D/'package.json').read_text());P=M/Path(old['registration']).parent;N=D/'package';N.mkdir(exist_ok=True)
 for name in old['manifest']['files']:
  if (N/name).exists():(N/name).chmod(0o644)
  shutil.copy2(P/name,N/name);(N/name).chmod(0o644)
 code=(N/'generator.py').read_text()
 if kp==17592186092384:
  start=code.index("    refs = {'easy':");end=code.index("    return {'knowledge_point':KP",start)
  code=code[:start]+"    provenance=json.loads((HERE/'source-provenance.json').read_text())['bands'][level]\n    refs=provenance['source_refs']\n"+code[end:]
  code=code.replace("'content_sha256':digest,'source_refs':refs,'source_basis':SOURCE['basis'],","'content_sha256':digest,'source_refs':refs,'source_inference':provenance['reason'],'source_basis':SOURCE['basis'],")
  bands={'easy':dict(source_refs=['q-308798','q-342142'],reason='Direct quadratic normal-slope examples; vary coefficients and point.'),'moderate':dict(source_refs=['e-148','q-71526'],reason='Eligible cubic normal-slope examples combined with polynomial expansion. Factored cubic presentation is a reasoned algebraic variant, not an exact imported template.'),'hard':dict(source_refs=['q-103531','q-103532','q-342153'],reason='Eligible normal-slope questions require rewriting radicals/reciprocal square roots and applying fractional power rules. Expanding signed (x+b)^2/sqrt(x) is a reasoned composition of those operations, not a claimed exact imported template.')}
  provenance=dict(bands=bands,historical_sources='source-cases.json retains prior captured examples; replay only complete original sources. All ordinary refs above resolve to remaining eligible source.',basis=json.loads((D/'source/source.json').read_text())['basis'])
  sources=['e-148','q-342153'];finding_ids=['minor-slope-notation','incomplete-slope-imports'];check_ids=['independent-normal-work','exact-normal-endpoint','eligible-source-lineage']
 else:
  start=code.index('SUPPORT = ');end=code.index('\n',start)
  support={'quadratic':['q-342200','q-342201'],'cubic':['q-308821'],'sqrt':['e-149'],'cubert':['e-149'],'sqrtcube':['e-149'],'fourth':['e-149'],'reciprocal':['q-308823'],'sqrtlinear':['e-149']}
  code=code[:start]+"PROVENANCE=json.loads(Path(__file__).with_name('source-provenance.json').read_text())\nSUPPORT={k:v['source_refs'] for k,v in PROVENANCE['families'].items()}"+code[end:]
  code=code.replace("'source_references':SUPPORT[family],'domain'","'source_references':SUPPORT[family],'source_inference':PROVENANCE['families'][family]['reason'],'domain'")
  code=code.replace("for q in data['questions']]","for q in data['questions'] if q[':db/id'] not in PROVENANCE['retired_source_entities']]")
  families={k:dict(source_refs=v,reason=('Direct remaining eligible polynomial/reciprocal intercept example; vary coefficients and point.' if k in ['quadratic','cubic','reciprocal'] else 'Canonical e-149 differentiates a square-root-plus-linear curve, forms the normal and intersects an axis. This is a reasoned rational-power variant of the same general method; exact derivative and axis endpoint independently verified. Fractional exponents 2/3,3/2,1/4 retain prior legitimate mathematical families without using retired radio banks as eligible examples.')) for k,v in support.items()}
  retired=[17592186092507,17592186092510,17592186233120,17592186240795,17592186240796,17592186493316,17592186578858,17592186710717,17592186233928,17592186234308]
  provenance=dict(families=families,retired_source_entities=retired,historical_counterexamples='source-replay.json preserves old records for provenance only. Retired source entities are filtered from every replay; they do not serve as ordinary source_references.',basis=json.loads((D/'source/source.json').read_text())['basis'])
  sources=['e-149','q-342200','q-308823'];finding_ids=['finite-intercept-radio-cue','incomplete-intercept-imports'];check_ids=['independent-normal-work','exact-normal-endpoint','eligible-source-lineage']
 (N/'generator.py').write_text(code);save(N/'source-provenance.json',provenance)
 (N/'normal_math.py').write_text((ROOT/'generate/reports/lesson-quality-audit-2026-11-11/normal/math_tools.py').read_text())
 # Checker authored separately below.
 plan=dict(format='course-academy-refill-plan-v1',status='checks',reason='Every final survivor must preserve independent differentiation and normal construction, use the intended blank endpoint, and cite remaining eligible source with explicit reasoned inference.',source_refs=sources,evidence_paths=['repair-rationale.md'],checks=[dict(id=i,purpose={'independent-normal-work':'Require an independent normal question with no supplied derivative, tangent slope or normal formula.','exact-normal-endpoint':'Independently parse the displayed function and point, differentiate and check exact slope/intercept blank keys with native equivalents and wrong controls.','eligible-source-lineage':'Reject refs to retired/incomplete sources; match family source refs and explicit reasoned inference against the retained provenance contract.'}[i],finding_ids=finding_ids if i=='exact-normal-endpoint' else []) for i in check_ids],finding_exemptions=[])
 save(N/'refill-review-plan.json',plan);save(N/'refill-validation.json',dict(format='course-academy-refill-check-v1',script='check_refill.py',args=[],files=['normal_math.py','source-provenance.json']))
 deps=copy.deepcopy(old['manifest']['dependencies']);deps['packages']['sympy']='1.14.0'
 if 'requirements.txt' not in old['manifest']['files']:(N/'requirements.txt').write_text('sympy==1.14.0\n')
 save(D/'package-build.json',dict(previous=old,dependencies=deps,files=sorted(set(old['manifest']['files'])|{'source-provenance.json','normal_math.py','refill-review-plan.json','refill-validation.json','check_refill.py','requirements.txt'})))
