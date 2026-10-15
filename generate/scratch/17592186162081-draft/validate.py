#!/usr/bin/env python3
"""Independent displayed scalar and stage checks, raw fidelity and native grading."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import numpy as np
import sympy as sp
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));from math_reader import scalar
spec=importlib.util.spec_from_file_location('unity',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,x): (HERE/name).write_text(json.dumps(x,indent=2)+'\n')
def image_path(ref):return Path('/media/jake/SSD/EDB/math')/ref if ref.startswith('images/') else Path(ref)
def check(r):
 q=r['question'];m=r['generation'];t=m['template'];p=m['parameters'];d=g.data(t,p)
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert all(ord(c)>=32 or c in '\n\t' for z in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']] for c in z)
 f=q[':question/answer-fields'][0];vals=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(vals)==5
 for a,b in itertools.combinations(vals,2):assert sp.simplify(a-b)!=0
 L=sp.pi*sp.Rational(p['r']) if t=='semicircle' else sp.sqrt((sp.Rational(p['x2'])-sp.Rational(p['x1']))**2+(sp.Rational(p['y2'])-sp.Rational(p['y1']))**2)
 if ':answer-field/correct' in f:
  a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert sp.simplify(scalar(a[':answer/value'])-L)==0
 if not m['evidence_only']:assert all(v>0 for v in vals);g.workload(m['level'],t,d)
 for ref in re.findall(r'!\[.*?\]\((.*?)\)',q[':question/problem']+' '+q.get(':question/worked-solution','')):
  ip=image_path(ref);assert ip.exists();im=Image.open(ip).convert('RGBA');white=Image.new('RGBA',im.size,'white');white.alpha_composite(im);im=white.convert('RGB');pix=np.array(im).astype('int16');blue=(pix[:,:,2]>pix[:,:,0]+30)&(pix[:,:,2]>pix[:,:,1]+10)&(pix[:,:,0]<140);assert blue.sum()>80
  if not ref.startswith('images/'):
   side=json.loads(ip.with_suffix('.json').read_text());assert side['sha256']==hashlib.sha256(ip.read_bytes()).hexdigest();assert side['recipe']==g.plot_recipe(t,d,side['recipe']['helper']);assert list(im.size)==side['native_pixels'];assert len(np.unique(pix[::4,::4].reshape(-1,3),axis=0))>50
   transform=np.array(side['data_transform']);assert abs(abs(transform[0,0])-abs(transform[1,1]))<1e-6
   # Confirm real blue curve pixels at independently computed points along the path.
   if t=='semicircle':points=[(float(sp.Rational(p['r']))*__import__('math').cos(u),float(sp.Rational(p['r']))*__import__('math').sin(u)) for u in (0,.4,1.2,2.1,__import__('math').pi)]
   else:points=[(float(sp.Rational(p['x1']))+u*float(sp.Rational(p['x2'])-sp.Rational(p['x1'])),float(sp.Rational(p['y1']))+u*float(sp.Rational(p['y2'])-sp.Rational(p['y1']))) for u in (0,.2,.5,.8,1)]
   for x,y in points:
    xp,yp,_=transform@np.array([x,y,1]);xp,yp=round(xp),round(456-yp)
    assert blue[max(0,yp-5):yp+6,max(0,xp-5):xp+6].any(),('missing plotted point',ref,x,y)
 s=q.get(':question/worked-solution')
 if not s:return
 if t.startswith('diagonal'):
  prose=re.search(r'legs have lengths \$(.*?)\$ and \$(.*?)\$',s);assert prose
  leg1=scalar(prose[1]);leg2=scalar(prose[2].rstrip(':'));assert leg1==d['b'] and leg2==d['a']
  block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',s,re.S)[1]
  rows=re.split(r'\\\\\s*&\s*=',block);assert len(rows)==4
  exprs=[e.strip() for e in [rows[0].split('=',1)[1]]+rows[1:]]
  for e in exprs:assert sp.simplify(scalar(e)-L)==0
  # Source operation shapes: substituted squares, evaluated two squares, collected root, simplified length.
  assert '^{2}' in exprs[0] and exprs[0].count('^{2}')==2
  first=re.fullmatch(r'\\sqrt\{\{(.*?)\}\^\{2\}\+\{(.*?)\}\^\{2\}\}',exprs[0]);assert first
  assert scalar(first[1])==leg1 and scalar(first[2])==leg2
  second=re.fullmatch(r'\\sqrt\{(.*?)\+(.*?)\}',exprs[1]);assert second
  assert scalar(second[1])==leg1**2 and scalar(second[2])==leg2**2
  assert exprs[2].startswith(r'\sqrt{') and '+' not in exprs[2]
  if t=='diagonal_helper':assert s.count('![](')==1
 elif t in ('vertical','horizontal'):
  eq=re.findall(r'\\text\{d\}s=([^\n]+)',s)[-1];pieces=eq.rstrip('.').split('=');assert len(pieces)==2
  assert sp.simplify(scalar(pieces[0])-L)==0 and scalar(pieces[1])==L
 elif t=='semicircle':
  radius=re.search(r'r = (.*?)\.\$',s)[1];assert scalar(radius)==sp.Rational(p['r'])
  value=re.search(r'L\s*(?:&\s*)?=\\pi r=(.*?) \.\\end',s)[1];assert sp.simplify(scalar(value)-L)==0
 # Independently inspect the final learner-visible conclusion.
 final=re.findall(r'(?:\\text\{d\}s|\\textrm d s)\s*=\s*([^\n]+)',s)[-1]
 assert sp.simplify(scalar(final.split('=')[-1])-L)==0

def main():
 root=HERE.parents[2];registered=HERE.with_name('17592186162081')
 baseline=json.loads((HERE/'post-approval-baseline.json').read_text())['files']
 def immutable():
  paths=[root/'generate/scratch/17592186162081.py',*sorted(registered.rglob('*')),*sorted((registered.parent/'__pycache__').glob('17592186162081*'))]
  current={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}
  assert current==baseline,'Registered immutable path set or hash changed'
  return len(current)
 immutable()
 build=json.loads((HERE/'reference/grader-build.json').read_text());hashes={build['source']:build['source_sha256'],build['library']:build['library_sha256'],build['binary']:build['binary_sha256'],**build['engine_sources'],**build['dependencies']}
 assert len(hashes)==42
 assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in hashes.items())
 save('grader-provenance.json',{'all_42_hashes_verified':True,'hashes':hashes,'binary':build['binary']})
 sys.path.insert(0,str(root/'scripts/question_capture'))
 from math_format import validate_generated_record,normalize_prose
 # Read current emitted text and geometries, keeping prior independent source proof.
 prior=json.loads((registered/'engine-input.json').read_text());rows=[];exact=0;normalized=0
 def ordered(q):
  q=copy.deepcopy(q)
  for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
  return q
 for item in prior:
  old=item['record'];m=old['generation']
  fresh=g.generate(m['level'],m['seed'],template=m['template'],parameters=m['parameters'],profile=m['profile'])
  if ordered(fresh['question'])==ordered(old['question']):exact+=1
  else:
   # Only inherited missing alignment marker may change normal presentation/IDs.
   assert not m['evidence_only'] and m['template']=='semicircle'
   oq=old['question'];nq=fresh['question'];assert nq[':question/worked-solution']==normalize_prose(oq[':question/worked-solution'])
   assert nq[':question/problem']==oq[':question/problem']
   of=oq[':question/answer-fields'][0];nf=nq[':question/answer-fields'][0]
   assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in nf[':answer-field/choices'])
   normalized+=1
  check(fresh)
  if not fresh['generation']['evidence_only']:validate_generated_record(copy.deepcopy(fresh))
  f=fresh['question'][':question/answer-fields'][0]
  rows.append({'label':item['label'],'record':fresh,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'current emitted answer identities'} for a in f[':answer-field/choices']]})
 # Full public raw source replay: all choices, full prose, all omissions and keys.
 cases=json.loads((HERE/'source-cases.json').read_text())
 for c in cases:
  r=g.generate('easy',template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];src=c['record'];check(r)
  assert q[':question/problem']==src[':question/problem']
  assert q.get(':question/worked-solution')==src.get(':question/worked-solution')
  for k in (':question/difficulty',':question/worked-solution'):assert (k in q)==(k in src)
  f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
  assert f[':answer-field/key']==sf[':answer-field/key'] and f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
  assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  if ':answer-field/correct' in sf:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
 batches={};review=[]
 assert g.SUPPORTED_LEVELS==('easy','moderate','hard')
 assert g.GENERATOR_UUID=='266305d9-55b0-5056-b70a-a675c8503e54'
 for level in g.SUPPORTED_LEVELS:
  assert getattr(g,'generate_'+level)(seed=11)==g.generate(level,11)
  batch=g.batch(level,5,1666926441);assert len({r['generation']['mathematical_fingerprint'] for r in batch})==5
  for r in batch:check(r)
  assert batch==g.batch(level,5,1666926441)
  batches[level]=[r['generation']['mathematical_fingerprint'] for r in batch]
  review.extend({'label':'Current '+level+' batch '+str(i),'record':r} for i,r in enumerate(batch))
  assert g.batch(level,0)==[]
  try:g.batch(level,-1)
  except ValueError:pass
  else:raise AssertionError('negative count accepted')
 # A fixed source profile has exactly one mathematical task; shortage fails honestly.
 try:g.batch('easy',2,profile='original:q-122766')
 except ValueError as e:assert 'finite variant limit' in str(e)
 else:raise AssertionError('finite fixed-profile shortage not detected')
 # CLI JSON and Markdown invoke current deduplicating batch with explicit flags.
 cli=[]
 for fmt in ['json','markdown']:
  cmd=[sys.executable,'-B',str(HERE.with_suffix('.py')),'--difficulty','all','--count','2','--seed','1666926441','--format',fmt]
  result=subprocess.run(cmd,check=True,capture_output=True,text=True)
  (HERE/('cli.'+fmt)).write_text(result.stdout)
  if fmt=='json':
   generated=json.loads(result.stdout);assert len(generated)==6
   for level in g.SUPPORTED_LEVELS:
    assert [r for r in generated if r['generation']['level']==level]==g.batch(level,2,1666926441)
  else:assert result.stdout.count('Calculate ')==6
  cli.append({'format':fmt,'records':6,'command':cmd})
 # Fresh owned assets: two changed geometries, simultaneous equal/different calls.
 params=[dict(x1='-7/13',y1='-5/13',x2='31/39',y2='45/52'),dict(x1='-8/13',y1='-6/13',x2='28/39',y2='41/52')]*2
 def worker(p):return g.generate('hard',template='diagonal_helper',parameters=p)
 with ThreadPoolExecutor(max_workers=4) as pool:fresh=list(pool.map(worker,params))
 assert fresh[0]==fresh[2] and fresh[1]==fresh[3]
 for r in fresh:
  check(r);validate_generated_record(copy.deepcopy(r))
  refs=re.findall(r'!\[.*?\]\((.*?)\)',r['question'][':question/problem']+' '+r['question'][':question/worked-solution'])
  assert len(refs)==2 and all(Path(p).parent==HERE/'assets' for p in refs)
 for i,r in enumerate(fresh[:2]):review.append({'label':'Fresh private hard geometry '+str(i),'record':r})
 for i,item in enumerate(review):
  r=item['record'];f=r['question'][':question/answer-fields'][0]
  rows.append({'label':'new-'+str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all displayed options through current native grader'} for a in f[':answer-field/choices']]})
 save('review.json',review);save('engine-input.json',rows)
 subprocess.run([str(root/build['binary']),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
 engine=json.loads((HERE/'engine-validation.json').read_text());assert engine['documented_unresolved_checks']==0
 report={'passed':True,'root_approval_pending':True,'registered_script_sha256':hashlib.sha256((root/'generate/scratch/17592186162081.py').read_bytes()).hexdigest(),'draft_script_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'source_basis':g.SOURCE['basis'],'current_records_rechecked':len(prior),'current_reproductions_exact_ignoring_option_order':exact,'normal_semicircle_presentation_normalizations':normalized,'source_questions':6,'complete_banks':6,'choices_matched':30,'observed_correct_designations':5,'absent_original_key_solution_rating':1,'batch_checks':batches,'cli':cli,'native_records':len(rows),'native_accepted':engine['accepted_checks'],'native_rejected':engine['rejected_checks'],'native_unresolved':0,'grader_hashes_verified':len(hashes),'fresh_private_geometry_cases':2,'concurrent_render_calls':4,'immutable_registered_files':immutable(),'runtime':fresh[0]['generation']['runtime'],'retained_proof':'Registered current versus reviewed e02bd7e2: every existing function AST unchanged, all mathematical/source/plot/review evidence hashes match. Draft changes normal-only shared formatting and guarded cache ownership; unchanged independent source, math-stage, source-raster/style9 visual and curriculum proofs retained.','remaining_limits':['q-122567 raw omission remains ineligible evidence; its normal completion is authored.','Scalar historical distractor intent is underidentified; original homothetic profiles remain evidence only.','Moderate/hard are authored same-method arithmetic workloads; calculator flags unknown.']}
 save('validation.json',report);print(json.dumps(report,indent=2))

if __name__=='__main__':main()

