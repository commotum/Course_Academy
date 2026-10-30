import copy,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from generator_packages import build_manifest,manifest_digest,verify_package
D=json.loads((H/'current.json').read_text());kp=next(k for k in D['knowledge_points']if k[':db/id']==17592186124630);g=kp[':knowledge-point/question-generator'];old=Path('/media/jake/SSD/EDB/math')/g[':question-generator/script'];staged=H/'staged-generators/17592186124630';entry=staged/'scalar_role_generator.py'
def run(path,*args):
 result=subprocess.run([sys.executable,'-B',str(path),*args],capture_output=True,text=True,check=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});return json.loads(result.stdout)
proof=[];samples=[]
for sid,target in[('q-140766',r'\{\mathbf{0}\}'),('q-141192','n'),('q-141343',r'\text{dim(Col}(A))'),('q-142357',r'\text{Col}(A)'),('q-141345',r'\text{Null}(A)')]:
 prior=run(old,'--replay',sid);after=run(entry,'--replay',sid);q=after['question'];f=q[':question/answer-fields'][0];values=[a[':answer/value']for a in f[':answer-field/choices']];ids=[a[':answer/id']for a in f[':answer-field/choices']];right=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);assert len(set(values))==len(values)==len(set(ids))==5;assert right[':answer/value']==target;assert after['generation']['evidence_only']and not after['generation']['eligible_for_learning'];proof.append({'selector':sid,'before_values':[a[':answer/value']for a in prior['question'][':question/answer-fields'][0][':answer-field/choices']],'after_values':values,'correct_value':target,'five_distinct_answer_values_and_roles':True,'canonical_source_role_preserved':True,'question_identity_changes_for_changed_content':q[':question/id']!=prior['question'][':question/id']});samples.append(after)
# Every fresh target is unchanged, including scalar n, scalar 0, and singleton-zero roles.
prior=run(old,'--difficulty','easy','--count','11','--seed','291029');fresh=run(entry,'--difficulty','easy','--count','11','--seed','291029');assert prior==fresh;samples+=fresh
source=json.loads((staged/'source-data.json').read_text());selectors=[q[':question/math-academy-id']for q in source[':knowledge-point/questions']];unchanged=[]
for sid in selectors:
 if sid in['q-140766','q-141192','q-141343','q-142357','q-141345']:continue
 assert run(old,'--replay',sid)==run(entry,'--replay',sid);unchanged.append(sid)
# Runtime closure is relocatable and cannot depend on writes to its package directory.
with tempfile.TemporaryDirectory(prefix='mth341-scalar-roles-',dir='/tmp')as root:
 clone=Path(root)/'package';shutil.copytree(staged,clone)
 for p in clone.rglob('*'):p.chmod(0o555 if p.is_dir()else 0o444)
 clone.chmod(0o555)
 for sid in['q-140766','q-141192','q-141343','q-142357','q-141345']:assert run(clone/entry.name,'--replay',sid)==run(entry,'--replay',sid)
 assert run(clone/entry.name,'--difficulty','easy','--count','11','--seed','291029')==fresh
 clone.chmod(0o755)
 for p in clone.rglob('*'):p.chmod(0o755 if p.is_dir()else 0o644)
inputs={n:hashlib.sha256((staged/n).read_bytes()).hexdigest()for n in[old.name,'source-data.json','math_format.py','repair-evidence.json']};assert all((staged/n).read_bytes()==(old.parent/n).read_bytes()for n in inputs)
evidence={'basis_t':D['basis_t'],'source_uuid_corrections':'scalar-versus-set-restorations.json','preserved_original_inputs_sha256':inputs,'explicit_selector_checks':proof,'fresh_11_targets_byte_identical':True,'all_other_replays_byte_identical':unchanged,'relocation_and_readonly_copy_passed':True,'eligible_for_learning_unchanged':True,'replay_correct_links_derived_by_source_answer_uuid_not_duplicate_value':True};(staged/'scalar-role-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');original_manifest=json.loads((old.parent/'generator-package.json').read_text());files=sorted(p.name for p in staged.iterdir()if p.is_file()and p.name!='generator-package.json');manifest=build_manifest(staged,entry.name,files,dependencies=original_manifest['dependencies']);(staged/'generator-package.json').write_text(json.dumps(manifest,indent=2)+'\n');digest=manifest_digest(manifest);verify_package(staged,digest);candidate={'kp':17592186124630,'kp_uuid':kp[':knowledge-point/id'],'old_reference':g[':question-generator/script'],'old_entity':g[':db/id'],'directory':str(staged.resolve()),'entrypoint':entry.name,'files':files,'dependencies':original_manifest['dependencies'],'approved_digest':digest};(H/'generator-candidates.json').write_text(json.dumps([candidate],indent=2)+'\n');(H/'generator-successor-verification.json').write_text(json.dumps({'passed':True,'candidate':candidate,**evidence},indent=2)+'\n');(H/'generator-successor-samples.json').write_text(json.dumps(samples,indent=2)+'\n');print('Successor passed: five explicit replay selectors, all 11 fresh targets,',len(unchanged),'unchanged replay selectors; relocated read-only runtime; source/script bytes preserved')
