"""Validate visible equations/options, complete source banks, and native grading."""
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('arc_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SUPPORTED_LEVELS=g.LEVELS

def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def task(q):
 text=q[':question/problem'];m=re.search(r'\$x\s*=\s*(.*?),\s*(?:\\,)?\s*y\s*=\s*(.*?)\$',text,re.S);assert m
 x,y=map(g.parse_tex,m.groups());m=re.search(r'from \$t\s*=\s*(.*?)\$ to \$t\s*=\s*(.*?)\$',text);assert m
 a,b=map(g.parse_tex,m.groups());return x,y,a,b

def fingerprint(q):
 try:return g.fingerprint(q)
 except (ValueError,AssertionError,AttributeError):return 'unparsed:'+hashlib.sha256(q[':question/problem'].encode()).hexdigest()

def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'field-owned visible radio choice'}for a in f[':answer-field/choices']]

def independent(r):
 q=r['question'];meta=r['generation'];x,y,a,b=task(q);f=q[':question/answer-fields'][0];assert len(f[':answer-field/choices'])==5 and f[':answer-field/type']==':answer-field.type/radio'
 target=s.diff(x,g.T)**2+s.diff(y,g.T)**2;vals=[];correct=[]
 for answer in f[':answer-field/choices']:
  z=g.parse_tex(answer[':answer/value']);assert isinstance(z,s.Integral) and z.limits==((g.T,a,b),)
  valid=g.square_equal(z.function,s.sqrt(target))
  if answer[':answer/id']==f[':answer-field/correct'][1]:assert valid;correct.append(answer)
  else:assert not valid
  for v in vals:assert not g.square_equal(z.function,v.function),'Equivalent complete options'
  vals.append(z)
 assert len(correct)==1
 if not meta['evidence_only']:
  assert meta['eligible_for_learning'] and meta['mathematical_fingerprint']==fingerprint(q)
  assert r==g.generate(q[':question/difficulty'].split('/')[-1],meta['seed'],meta['template'],meta['parameters'],meta['bank_profile'])
  blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==4
  # Read derivative operands and printed results, independently of metadata.
  for block,fun in zip(blocks[1:3],(x,y)):
   rhs=block.rsplit('=',1)[1].rstrip('.');assert g.eq(g.parse_tex(rhs),s.diff(fun,g.T))
   operand=block.split(r'\left(',1)[1].rsplit(r'\right)=',1)[0];assert g.eq(g.parse_tex(operand),fun)
  rows=blocks[-1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')
  assert len(rows)==(4 if meta['template']=='q-123027'else 3)
  for row in rows[1:]:
   integral=g.parse_tex(row.split('=',1)[1]);assert integral.limits==((g.T,a,b),)
   assert g.square_equal(integral.function,s.sqrt(target)),'Printed arc-length stage wrong'
 return True

def main():
 fidelity=[];replays=[];all_records=[]
 for mid,old in g.SOURCES.items():
  if ':question/difficulty' not in old:continue
  level=old[':question/difficulty'][':db/ident'].split('/')[-1];r=g.generate(level,template=mid,profile='source-replay');independent(r);new=r['question'];f=new[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  originals=[g.parse_tex(a[':answer/value'])for a in of[':answer-field/choices']];generated=[g.parse_tex(a[':answer/value'])for a in f[':answer-field/choices']]
  for z in originals:assert sum(g.eq(z,w)for w in generated)==1,(mid,z)
  assert new[':question/problem']==g.normalize_prose(old[':question/problem']);assert new[':question/worked-solution']==g.normalize_prose(old[':question/worked-solution'])
  expected=g.parse_tex(of[':answer-field/correct'][':answer/value']);actual=g.parse_tex(next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]));assert g.eq(expected,actual)
  fidelity.append({'source':mid,'matched_options':5,'total_options':5,'matched_distractors':4,'complete_bank':True,'correct_designation':True,'prompt_solution':'exact after shared notation normalization','normal_sampler':mid in g.DEFAULTS.values()});replays.append(r)
  print('Replay',mid,flush=True)
 coverage={}
 for level,mid in g.DEFAULTS.items():
  domain=g.domain(mid);fps=set()
  for i,p in enumerate(domain):
   r=g.generate(level,i,mid,p);independent(r);fps.add(fingerprint(r['question']));all_records.append(r)
   r2=g.generate(level,i+100,mid,p);assert r['question'][':question/id']==r2['question'][':question/id']
   assert g.generate(level,i,mid,p)==r
  assert len(fps)==len(domain)
  coverage[level]={'domain_size':len(domain),'distinct_tasks':len(fps),'A':sorted({p['A']for p in domain}),'B':sorted({p['B']for p in domain}),'exhaustive':True}
  print('Validated domain',level,len(domain),flush=True)
 # Reject deliberate printed solution and key faults.
 r=g.generate('hard',1);bad=copy.deepcopy(r);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('Computing','Wrong',1)
 try:independent(bad)
 except AssertionError:pass
 else:raise AssertionError('Replay identity check missed solution mutation')
 bad=copy.deepcopy(r);f=bad['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id']for a in f[':answer-field/choices']if a[':answer/id']!=f[':answer-field/correct'][1])
 try:independent(bad)
 except AssertionError:pass
 else:raise AssertionError('Wrong key accepted')
 numeric=[]
 for r in all_records:
  q=r['question'];f=q[':question/answer-fields'][0];_,_,a,b=task(q);values=[];errors=[]
  for ans in f[':answer-field/choices']:
   expr=g.parse_tex(ans[':answer/value']).function;fun=s.lambdify(g.T,expr,'numpy');est=[]
   for n in (16,32):
    nodes,weights=np.polynomial.legendre.leggauss(n);width=float(b-a)/64;ts=float(a)+(np.arange(64)[:,None]+(nodes+1)/2)*width;vs=fun(ts);assert np.isfinite(vs).all() and (vs>=0).all();est.append(float(np.sum(vs*weights)*width/2))
   values.append(est[1]);errors.append(abs(est[1]-est[0]))
  gap=min(abs(u-v)for i,u in enumerate(values)for v in values[:i]);assert gap>100*max(max(errors),1e-9),'Numerically colliding definite-integral options'
  numeric.append({'question_id':q[':question/id'],'lengths':values,'minimum_separation':gap,'resolution_difference':max(errors)})
 save('numerical-option-separation.json',numeric)
 engine=[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)}for r in replays+all_records];save('native-input.json',engine)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-validation.json')],check=True)
 native=json.loads((HERE/'native-validation.json').read_text())
 save('source-fidelity.json',fidelity);save('validated-domain.json',all_records)
 examples=[g.generate('moderate',template='q-15163',parameters={'A':3,'B':4}),g.generate('hard',template='q-123027',parameters={'A':5,'B':9})]
 (HERE/'review.md').write_text('\n\n'.join(['# Original and variant review']+[f'## {mid}\n\n### Source\n\n'+g.SOURCES[mid][':question/problem']+'\n\n'+g.SOURCES[mid][':question/worked-solution']+'\n\n### Normal replay at original parameters\n\n'+g.markdown(g.generate(level,template=mid,parameters=p))+'\n\n### Changed coefficients\n\n'+g.markdown(ex) for level,mid,p,ex in [('moderate','q-15163',{'A':2,'B':2},examples[0]),('hard','q-123027',{'A':3,'B':8},examples[1])]])+'\n')
 result={'status':'pass','basis':g.SNAP['basis'],'lineage':g.SNAP['lineage'],'source_complete_banks':len(fidelity),'source_distractors_matched':4*len(fidelity),'source_options_matched':5*len(fidelity),'normal_supported_source_banks':2,'coverage':coverage,'native_grading':{k:native[k]for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'mutations_rejected':2,'fidelity':'All 11 complete source banks replay; nine are evidence-only, not normal samplers. Normal source solutions retain wording and operative stages with normalized notation.','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'validated-domain.json',HERE/'validate.py']},'dependency_versions':{'sympy':s.__version__},'database_writes':0,'numerical_option_separation':len(numeric),'normal_source_bank_replay':'The two normal families use the same data() at original source parameters as source-replay, establishing complete-bank identity.'}
 save('validation.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':main()
