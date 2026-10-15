"""Incremental revalidation of current formatting against frozen prior math proof."""
import copy,hashlib,importlib.util,json,re,sys,types,uuid
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def run(vcheck=None):
 vcheck=vcheck or load(D/'validate.py','surface_validate_extra');g=vcheck.g
 approved=types.ModuleType('approved_surface_math');approved.__file__=str(D.with_suffix('.py'))
 approved_source=(D/'reference/approved-script.py').read_text();assert hashlib.sha256(approved_source.encode()).hexdigest()=='35bcfe826e3e5241ddc1bcc34280f2f72e404f77fdd13c19facc5c8292ab83a0'
 exec(compile(approved_source,approved.__file__,'exec'),approved.__dict__)
 snapshot=json.loads((D/'source.json').read_text());frozen=ROOT/'generate/runs/current/refresh-2026-10-14'
 assert snapshot==json.loads((frozen/'sources/17592186119887.json').read_text())
 manifest=json.loads((ROOT/'generate/runs/current/manifest.json').read_text());job=next(j for j in manifest['jobs'] if j['kp_id']==g.KP_ID);assert job['topic_id']==17592186048384
 for name,folder in [('topic-context.json','topics'),('lesson-context.json','lessons')]:assert json.loads((D/name).read_text())==json.loads((frozen/folder/'17592186048384.json').read_text())
 cases=json.loads((D/'source-cases.json').read_text());assert {c['source_id'] for c in cases}==set(g.SOURCES)
 for c in cases:assert c['record']==g.SOURCES[c['source_id']]
 independent=[q for q in snapshot['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q];inv=json.loads((D/'independent-inventory.json').read_text());assert not independent and inv=={k:snapshot[k] for k in ('database','basis','lineage')}|{'questions':[]}
 canonical={'source_id':snapshot['record'][':knowledge-point/canonical-example'][':question/math-academy-id'],'record':snapshot['record'][':knowledge-point/canonical-example']};(D/'canonical-example.json').write_text(json.dumps(canonical,indent=2,ensure_ascii=False)+'\n')
 normal=raw=bankbindings=slots=0;ids=[];repaired=0
 for level,rows in json.loads((D/'accepted-domains.json').read_text()).items():
  for row in rows:
   kwargs={'template':row['template'],'parameters':row['parameters']}
   a=approved.generate(level,seed=17,**kwargs);b=g.generate(level,seed=17,**kwargs);vcheck.verify(b)
   qa,qb=a['question'],b['question'];assert g.normalize_prose(qa[':question/problem'])==qb[':question/problem']
   sa,sb=g.normalize_prose(qa[':question/worked-solution']),qb[':question/worked-solution'];base=row['template'].split(':')[-1]
   if base=='q-109911':
    # Only this one historical zero-derivative input may differ. Full-coordinate
    # equality, including its constant, is independently enforced by verify().
    pat=r'(\\frac\{∂\}\{∂v\}\()(.*?)(\)(?=,|⟩))'
    aa=list(re.finditer(pat,sa));bb=list(re.finditer(pat,sb));assert len(aa)==len(bb)==3
    assert sa[:aa[0].start(2)]+sa[aa[0].end(2):]==sb[:bb[0].start(2)]+sb[bb[0].end(2):]
    assert not vcheck.equal(vcheck.scalar(aa[0][2]),vcheck.scalar(bb[0][2]));repaired+=1
   else:assert sa==sb,('Unexplained solution change',base)
   assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
   # Formatter must retain all components and the correct answer must remain
   # bound to its normalized field-owned value through deterministic shuffling.
   for fa,fb in zip(qa[':question/answer-fields'],qb[':question/answer-fields']):
    before={g.normalize_tex(z[':answer/value']) for z in fa[':answer-field/choices']};after={z[':answer/value'] for z in fb[':answer-field/choices']};assert before==after
    ca=next(z[':answer/value'] for z in fa[':answer-field/choices'] if z[':answer/id']==fa[':answer-field/correct'][1]);cb=next(z[':answer/value'] for z in fb[':answer-field/choices'] if z[':answer/id']==fb[':answer-field/correct'][1]);assert g.normalize_tex(ca)==cb;bankbindings+=1
    if base!='q-167648':assert all(len(vcheck.vector(z[':answer/value']))==3 for z in fb[':answer-field/choices'])
    for z in fb[':answer-field/choices']:assert z[':answer/id']==g.uid(fb[':answer-field/id']+':'+z[':answer/value'])
   # Full actual IDs, ownership and key must survive a different shuffle seed.
   c=g.generate(level,seed=733,**kwargs)
   assert qb[':question/id']==c['question'][':question/id'];assert b['generation']['content_hash']==c['generation']['content_hash']
   for fb,fc in zip(qb[':question/answer-fields'],c['question'][':question/answer-fields']):
    assert fb[':answer-field/id']==fc[':answer-field/id'] and fb[':answer-field/correct']==fc[':answer-field/correct']
    assert {z[':answer/id']:z[':answer/value'] for z in fb[':answer-field/choices']}=={z[':answer/id']:z[':answer/value'] for z in fc[':answer-field/choices']}
   ids.append(qb[':question/id']);normal+=1;slots+=0 if base=='q-167648' else 6
 assert len(set(ids))==len(ids)==400
 # Public historical replay remains byte-exact, including the known omission,
 # across anchors and changed parameters; it is never learner-eligible.
 for base in g.SOURCES:
  for p in ({'a':1,'b':1,'c':1},{'a':2,'b':3,'c':3 if base=='q-167648' else 2}):
   kw={'template':base,'parameters':p,'profile':'observed:'+base};a=approved.generate('easy',**kw);b=g.generate('easy',**kw);assert a['question']==b['question'];assert b['generation']['evidence_only'] and not b['generation']['eligible_for_learning'];raw+=1
 # Regression: a constant omitted only in the derivative-zero argument must fail.
 r=g.generate('hard',template='hard:q-109911',parameters={'a':2,'b':3,'c':4});mut=copy.deepcopy(r);old=r'\frac{∂}{∂v}(2\left({u}^{2}+1\right))';new=r'\frac{∂}{∂v}(2\left({u}^{2}\right))';assert old in mut['question'][':question/worked-solution'];mut['question'][':question/worked-solution']=mut['question'][':question/worked-solution'].replace(old,new,1)
 try:vcheck.verify(mut)
 except AssertionError:pass
 else:raise AssertionError('Derivative-zero coordinate omission escaped')
 for name in ('correct-binding','vector-component','conclusion'):
  mut=copy.deepcopy(r);f=mut['question'][':question/answer-fields'][0]
  if name=='correct-binding':f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
  elif name=='vector-component':f[':answer-field/choices'][0][':answer/value']='⟨1,2⟩'
  else:
   text=mut['question'][':question/worked-solution'];m=list(re.finditer('⟨[^⟨⟩]*⟩',text))[-1];mut['question'][':question/worked-solution']=text[:m.start()]+'⟨1,2,3⟩'+text[m.end():]
  try:vcheck.verify(mut)
  except (AssertionError,ValueError,TypeError):pass
  else:raise AssertionError('Mutation escaped:'+name)
 # The public wrapper must reject a corrupt learner payload before returning it.
 original=g._generate
 try:
  bad=copy.deepcopy(r);bad['question'][':question/problem']+='\f';g._generate=lambda *a,**k:bad
  try:g.generate('hard')
  except ValueError:pass
  else:raise AssertionError('Public wrapper failed to reject malformed content')
 finally:g._generate=original
 provenance=json.loads((D/'grader-provenance.json').read_text());assert len(provenance['checked_hashes'])==42
 for p,h in provenance['checked_hashes'].items():assert sha(ROOT/p)==h,p
 assert sha(D/'check-engine')==provenance['copied_binary_sha256']
 baseline=json.loads((D/'registered-baseline.json').read_text());assert all(sha(ROOT/p)==h for p,h in baseline.items())
 native=json.loads((D/'engine-report.json').read_text());assert native['documented_unresolved_checks']==3
 report={'status':'pass','root_approval':'pending','prior_approved_script_sha256':sha(D/'reference/approved-script.py'),'current_registered_baseline_sha256':baseline['generate/scratch/17592186119887.py'],'draft_sha256':sha(D.with_suffix('.py')),'normal_instances_compared_to_normalized_prior_content':normal,'normal_complete_bank_correct_bindings':bankbindings,'complete_printed_partial_inputs':slots,'q109911_full_input_repairs':repaired,'raw_original_and_changed_records_exact_against_prior':raw,'source_counts':{'original_MA':7,'independent_inventory':0,'canonical_separate':1,'fields':8,'values':36,'solutions':6,'present_correct_refs':6,'missing_correct_refs':2},'identity_checks':'All400 complete IDs/field ownership/key/answer IDs stable under seed/order; unique across full allowed domain','new_mutations_rejected':['zero-derivative omitted coordinate constant','wrong correct-reference binding','truncated vector component','stale final vector','public wrapper C0 malformed content'],'prior_proof_retained':'Prior independent root readback and approved script retained; all unchanged prompt/solution/bank content compared, current complete-domain math/stage checks rerun','grader_provenance_hashes':42,'registered_files_unchanged':len(baseline),'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'limits':['Opaque historical distractor intent is unresolved and raw profiles remain ineligible.','Three genuine uncollected-norm equivalence parser gaps remain unresolved.','Moderate/hard labels are conservative arithmetic-only design claims, not observed labels.'],'database_writes':0,'registration_changes':0}
 (D/'postqa.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');return report
if __name__=='__main__':print(json.dumps(run(),indent=2))
