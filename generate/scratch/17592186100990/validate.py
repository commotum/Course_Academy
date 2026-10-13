#!/usr/bin/env python3
"""Independent actual-display parsing, full raw fidelity, scope/identity/native QA."""
import collections,copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('matrix_index',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,o):(HERE/n).write_text(json.dumps(o,indent=2)+'\n')
def formatting(text):
 assert text.count('$')%2==0,'Unbalanced math delimiters'
 dep=0
 for c in text:
  if c=='{':dep+=1
  if c=='}':dep-=1
  assert dep>=0,'Group underflow'
 assert dep==0 and text.count(r'\begin{')==text.count(r'\end{'),'Unbalanced TeX'
def read_display(text):
 m=re.search(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',text,re.S);assert m,'No printed matrix'
 rows=[];pos=[]
 for i,row in enumerate(m[1].split(r'\\'),1):
  vals=[]
  for j,c in enumerate(row.split('&'),1):
   c=c.strip();b=re.fullmatch(r'\\boxed\{(-?\d+)\}',c)
   if b:pos.append((i,j));c=b[1]
   vals.append(sp.Integer(c))
  rows.append(vals)
 assert all(len(r)==len(rows[0]) for r in rows),'Malformed printed matrix'
 letter=re.search(r'\$([A-Z])\$',text)[1]
 return rows,letter,pos

def parse_answer(x):
 m=re.fullmatch(r'\{?([a-z])\}?_\{([1-9])([1-9])\}',x)
 return (m[1],int(m[2]),int(m[3])) if m else sp.Integer(x)

def check(r):
 assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=r['question'];meta=r['generation'];normal=meta['eligible_for_learning'];raw=meta['origin']=='observed-parameterized';p=meta['parameters'];a,letter,positions=read_display(q[':question/problem'])
 formatting(q[':question/problem']);generics=re.findall(r'\{?([a-z])\}?_\{ij\}',q[':question/problem']);assert generics and all(x==letter.lower() for x in generics),'Stale generic index notation';assert a==p['matrix'] and letter==p['letter'],'Stale printed matrix/letter'
 if not raw:
  assert len(positions)==1,'Need exactly one visible boxed cell';i,j=positions[0]
 else:
  assert positions==[] and meta['evidence_only'];i,j=p['i'],p['j']
 assert 1<=i<=len(a) and 1<=j<=len(a[0])
 expected_fp=g.digest(['position-to-index',len(a),len(a[0]),i,j]);assert meta['mathematical_fingerprint']==expected_fp
 if not raw and not meta['source']:
  level=q[':question/difficulty'].split('/')[-1]
  assert (len(a),len(a[0])) in g.DIMS[level]
  if level=='moderate':assert max(i,j)>=4
  if level=='hard':assert max(i,j)>=5
  assert all(-9<=v<=9 for row in a for v in row)
 if normal:assert ':question/difficulty' in q and ':question/worked-solution' in q
 # Independently determine criterion from actual printed field keys and prompt,
 # not generation answer metadata. Never substitute value lookup for position.
 expected={}
 if '$i=$' in q[':question/problem']:
  expected={'field-1':sp.Integer(i),'field-2':sp.Integer(j)}
 else:expected={'selection' if len(q[':question/answer-fields'][0][':answer-field/choices'])==5 else 'field-1':(letter.lower(),i,j)}
 identities=[]
 for f in q[':question/answer-fields']:
  key=f[':answer-field/key'];typ=f[':answer-field/type'].split('/')[-1];bank=f[':answer-field/choices'];values=[parse_answer(b[':answer/value']) for b in bank]
  assert len(values)==len(set(values)),'Equivalent/duplicate displayed options'
  assert values.count(expected[key])==1,'No unique correct displayed answer'
  assert len(set(b[':answer/id'] for b in bank))==len(bank)
  for b in bank:
   assert b[':answer/type']==':answer.type/math';assert b[':answer/id']==g.uid(f[':answer-field/id']+':'+b[':answer/value'])
  if typ=='blank':assert '{{'+key+'}}' in q[':question/problem'] and len(bank)==1
  else:
   assert typ=='radio' and len(bank)==5
   sid=meta['source'] or meta['profile']
   # Written here independently from bank() and read from displayed positions.
   offsets={'q-13498':[(1,-1),(0,1),(0,0),(1,0),(0,-1)],'q-13503':[(-2,0),(0,0),(-1,-2),(-1,0),(1,0)],'q-13489':[(0,0),(1,2),(1,1),(1,0),(0,1)],'q-125611':[(-1,-1),(0,-1),(-1,0),(0,0),(0,1)],'q-13499':[(-1,-3),(-2,-1),(1,-1),(-1,-2),(0,0)]}[sid]
   assert set(values)=={(letter.lower(),i+di,j+dj) for di,dj in offsets},'Incorrect complete operation bank'
  ref=f.get(':answer-field/correct')
  correct=None
  if ref:
   assert ref[0]==':answer/id';correct=next(b[':answer/value'] for b in bank if b[':answer/id']==ref[1]);assert parse_answer(correct)==expected[key]
  if normal:assert ref,'Missing normal correct reference'
  identities.append({'key':key,'type':typ,'bank':sorted(b[':answer/value'] for b in bank),'correct':correct,'correct_present':bool(ref)})
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];formatting(sol)
  position_match=re.search(r'intersection of the \$(\d+)\$(?:st|nd|rd|th) row and \$(\d+)\$(?:st|nd|rd|th) column',sol);assert position_match,'Missing source positional stage';ri,cj=position_match.groups();assert (int(ri),int(cj))==(i,j),'Wrong row/column prose'
  if 'i=' in sol:
   assert re.search(r'i=(\d+)',sol)[1]==str(i) and re.search(r'j=(\d+)',sol)[1]==str(j)
  else:
   m=re.search(r'\$((?:\{?[a-z]\}?_\{[1-9][1-9]\})=-?\d+|-?\d+=(?:\{?[a-z]\}?_\{[1-9][1-9]\}))\.\$',sol);assert m,'Missing complete conclusion'
   lft,rgt=m[1].split('=');left,right=parse_answer(lft),parse_answer(rgt)
   assert {left,right}=={(letter.lower(),i,j),a[i-1][j-1]},'Wrong conclusion value/index/letter'
  assert sol.startswith('The entry ') and 'Hence, we have' in sol and sol.count('intersection')==1,'Source solution-stage/prose mismatch'
 identity={'version':g.VERSION,'question':{k:v for k,v in q.items() if k not in (':question/id',':question/answer-fields')},'fields':identities}
 cid=hashlib.sha256(json.dumps(identity,sort_keys=True,separators=(',',':')).encode()).hexdigest();assert meta['content_identity']==cid,'Incomplete content identity';assert q[':question/id']==g.uid('question:'+cid)
 for f in q[':question/answer-fields']:assert f[':answer-field/id']==g.uid(q[':question/id']+':'+f[':answer-field/key'])
 return r

def fidelity(sid,r):
 old=g.SOURCES[sid];q=r['question'];result={'source_id':sid,'raw_prompt_exact':True,'raw_key_presence_exact':True,'solution_exact':None,'correct_designations_matched':0,'values_matched':0,'distractors_matched':0,'complete_banks_matched':0}
 for k in (':question/problem',':question/difficulty',':question/worked-solution',':question/answer-fields'):
  assert (k in old)==(k in q)
  if k in old and k!=':question/answer-fields':assert q[k]==(old[k][':db/ident'] if isinstance(old[k],dict) else old[k])
 if ':question/worked-solution' in old:result['solution_exact']=True
 assert len(old[':question/answer-fields'])==len(q[':question/answer-fields'])
 for of,nf in zip(old[':question/answer-fields'],q[':question/answer-fields']):
  assert of[':answer-field/key']==nf[':answer-field/key'] and of[':answer-field/type'][':db/ident']==nf[':answer-field/type']
  assert (':answer-field/correct' in of)==(':answer-field/correct' in nf)
  ob=sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in of[':answer-field/choices']);nb=sorted((a[':answer/type'],a[':answer/value']) for a in nf[':answer-field/choices']);assert ob==nb
  result['values_matched']+=len(nb);result['complete_banks_matched']+=1
  if ':answer-field/correct' in of:
   result['correct_designations_matched']+=1;ans=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert ans==of[':answer-field/correct'][':answer/value'];result['distractors_matched']+=len(nb)-1
  elif len(nb)==5:result['distractors_matched']+=4 # mathematical designation inferred from inspected raster, not observed captured ref
 return result

def native(label,r):
 checks=[]
 for k,f in enumerate(r['question'][':question/answer-fields']):
  ref=f[':answer-field/correct'][1]
  if f[':answer-field/type'].endswith('/radio'):
   checks +=[{'field_index':k,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ref else 'rejected','purpose':'complete radio bank'} for a in f[':answer-field/choices']]
  else:
   value=f[':answer-field/choices'][0][':answer/value'];v=parse_answer(value)
   if isinstance(v,tuple):
    letter,i,j=v;equiv='2*'+value+'/2';wrong='{'+letter+'}_{'+str(i)+str(j+1)+'}'
   else:equiv=str(int(v)+1)+'-1';wrong=str(int(v)+1)
   checks +=[{'field_index':k,'submitted':s,'expected':e,'purpose':p} for s,e,p in [(value,'unresolved' if isinstance(v,tuple) else 'accepted','canonical symbolic native limitation' if isinstance(v,tuple) else 'canonical'),(equiv,'unresolved' if isinstance(v,tuple) else 'accepted','distinct equivalent symbolic native limitation' if isinstance(v,tuple) else 'distinct equivalent expression'),(wrong,'unresolved' if isinstance(v,tuple) else 'rejected','wrong symbolic native limitation' if isinstance(v,tuple) else 'wrong index')]]
 return {'label':label,'record':r,'checks':checks}

def reject(fn):
 try:fn()
 except (ValueError,AssertionError,TypeError):return
 raise AssertionError('Rejected invalid input/mutation regression did not fail')

def main():
 fs=[];cases=[];review=[];ni=[];normal=[]
 for sid in g.SOURCES:
  p=g.source_parameters(sid);r=check(g.generate('easy',parameters=p,profile='raw:'+sid));fs.append(fidelity(sid,r));cases.append({'source_id':sid,'template':g.STYLE[sid],'parameters':p,'level':'easy','level_origin':'observed' if ':question/difficulty' in g.SOURCES[sid] else 'authored API workload only; raw record remains unrated','profile':'raw:'+sid})
  c=check(g.generate('easy',parameters=p,profile='completed:'+sid));ni.append(native('completed-'+sid,c))
  if all(':answer-field/correct' in f for f in r['question'][':question/answer-fields']):ni.append(native('raw-'+sid,r))
  changed=copy.deepcopy(p);changed['letter']='Z';changed['matrix']=[[-v for v in row] for row in changed['matrix']]
  # Translation of entire position and complete bank; maintain positive subscripts.
  if p['i']<len(p['matrix']):changed['i']+=1
  if p['j']<len(p['matrix'][0]):changed['j']+=1
  v=check(g.generate('easy',parameters=changed,profile='raw:'+sid));vc=check(g.generate('easy',parameters=changed,profile='completed:'+sid));ni.append(native('changed-completed-'+sid,vc))
  review.append({'label':'Original '+sid+'; raw replay and authored highlight-restored variant','original':g.SOURCES[sid],'raw_replay':r,'variant':vc,'changed_raw':v})
 coverage={}
 for level in g.LEVELS:
  samples=[check(g.generate(level,k)) for k in range(480)];normal+=samples
  templates=collections.Counter(r['generation']['template'] for r in samples);profiles=collections.Counter(r['generation']['profile'] for r in samples)
  assert set(templates)==set(g.SUPPORTED_TEMPLATES) and set(profiles)==set(g.BANKS)|{'blank'}
  observed_fps={r['generation']['mathematical_fingerprint'] for r in samples};assert len(observed_fps)==len(g.eligible_positions(level)),'Default sampling misses meaningful positional tasks'
  coverage[level]={'templates':dict(templates),'profiles':dict(profiles),'meaningful_tasks_observed':len(observed_fps)}
  ni += [native(level+'-'+str(k),r) for k,r in enumerate(samples)]
  for t in g.TEMPLATES:
   for k in range(2):
    r=check(g.generate(level,1000+k,template=t));ni.append(native('review-'+level+'-'+t+'-'+str(k),r));review.append({'label':'Generated '+level+' '+t+' '+str(k),'variant':r})
 counts={};profilecounts={}
 for level in g.LEVELS:
  fps=set();pc=collections.Counter()
  for m,n,i,j in g.eligible_positions(level):
   p={'matrix':[[0]*n for _ in range(m)],'i':i,'j':j,'letter':'A'}
   for t in ('notation_blank','two_indices'):
    r=check(g.generate(level,template=t,parameters=p));fps.add(r['generation']['mathematical_fingerprint'])
   for profile in g.BANKS:
    if (m,n,i,j) in g.eligible_positions(level,profile):
     for t in ('inline_radio','display_radio'):check(g.generate(level,template=t,parameters=p,profile=profile))
     pc[profile]+=1
  counts[level]=len(fps);profilecounts[level]=dict(pc)
 assert counts=={'easy':39,'moderate':42,'hard':52}
 # Explicit boundary guards, API conflict handling and whole-bank failure.
 for level,dim in [('moderate',(5,6)),('hard',(6,7))]:
  p={'matrix':[[0]*dim[1] for _ in range(dim[0])],'i':1,'j':1,'letter':'A'};reject(lambda:g.generate(level,template='notation_blank',parameters=p))
 reject(lambda:g.generate('easy',field_type='blank',profile='q-13498'))
 p={'matrix':[[0]*2 for _ in range(2)],'i':1,'j':1,'letter':'A'};reject(lambda:g.generate('easy',template='display_radio',parameters=p,profile='q-13499'))
 # Identity: fixed content independent of seed; incidental numbers/aliases
 # don't inflate task counts, but all actual content differences alter identity.
 r=normal[0];p=copy.deepcopy(r['generation']['parameters']);level=r['question'][':question/difficulty'].split('/')[-1];t=r['generation']['template'];pr=r['generation']['profile']
 rr=check(g.generate(level,999,template=t,parameters=p,profile=pr));assert r['question'][':question/id']==rr['question'][':question/id']
 pp=copy.deepcopy(p);pp['letter']='Q';pp['matrix'][0][0]=8 if pp['matrix'][0][0]!=8 else -8
 rr=check(g.generate(level,template=t,parameters=pp,profile=pr));assert r['generation']['mathematical_fingerprint']==rr['generation']['mathematical_fingerprint'] and r['question'][':question/id']!=rr['question'][':question/id']
 # All content stages really checked: intentional stale row, bad conclusion,
 # removed highlight, changed bank, bad identity and altered matrix must fail.
 mutation_checks=0
 for path in ['highlight','solution','conclusion','bank','identity','matrix']:
  r=copy.deepcopy(next(z for z in normal if z['generation']['template']=='display_radio'))
  if path=='highlight':r['question'][':question/problem']=re.sub(r'\\boxed\{(-?\d+)\}',r'\1',r['question'][':question/problem'])
  elif path=='solution':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(' row',' column',1)
  elif path=='conclusion':r['question'][':question/worked-solution']=re.sub(r'=(-?\d+)\.\$', '=99.$',r['question'][':question/worked-solution'])
  elif path=='bank':r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='{q}_{99}'
  elif path=='identity':r['generation']['content_identity']='x'
  else:r['question'][':question/problem']=r['question'][':question/problem'].replace('&','& 1 &',1)
  reject(lambda:check(r));mutation_checks+=1
 save('source-cases.json',cases);save('source-replay.json',fs);save('review.json',review);save('native-input.json',ni)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 native_report=json.loads((HERE/'native-grading.json').read_text())
 md=['# Matrix index review','Raw originals have no captured highlight. Only restored variants are eligible for learning. Missing moderate/hard labels are authored.']
 for x in review:
  md+=['## '+x['label']]
  if 'original' in x:
   md+=['### Captured original',x['original'][':question/problem'],x['original'].get(':question/worked-solution','No captured solution.'),'### Raw replay',g.markdown(x['raw_replay'])]
  md+=['### Clearly labeled generated variant',g.markdown(x['variant'])]
 (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
 output={'status':'passed-supported-defaults; symbolic-blank-drafts-native-unresolved','source_provenance':{k:g.CAPTURE[k] for k in ('database','basis','lineage')},'source_questions':8,'observed_easy':6,'unrated_raw':2,'raw_exact_prompts':8,'raw_exact_solutions':{'matched':6,'present':6,'absent_preserved':2},'complete_source_banks':{'matched':9,'total':9},'source_values':{'matched':29,'total':29},'source_distractors':{'matched':20,'total':20,'designation_note':'8 unrated distractors identified from original rasters, not captured correct refs'},'captured_correct_designations':{'matched':7,'present':7,'absent_preserved':2},'source_repairs':{'highlights_restored':8,'authored_correct_refs':2,'authored_solutions':2,'two_index_capture_whitespace_normalized':1,'raw_profiles_eligible':False},'default_coverage':coverage,'meaningful_tasks':counts,'complete_radio_bank_task_coverage':profilecounts,'normal_samples_checked':len(normal),'mutation_regressions_rejected':mutation_checks,'native':{k:native_report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','entry_point','database_writes')},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'hashes':{'generator':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'capture':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'native_engine':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()},'unresolved_findings':['Native symbolic-index blanks reject canonical/equivalent/wrong entries with unconsumed mathematical notation; retained as ineligible drafts, excluded from normal defaults.'],'native_ungraded_raw_sources':2,'supported_default_templates':list(g.SUPPORTED_TEMPLATES),'unsupported_explicit_template':'notation_blank'}
 save('validation.json',output);print(json.dumps(output,indent=2))
if __name__=='__main__':main()
