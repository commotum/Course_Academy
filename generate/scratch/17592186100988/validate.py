#!/usr/bin/env python3
"""Fail-closed source fidelity, independent display math, scope and native QA."""
import collections, copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('entry_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2)+'\n')
def read_display(text):
 body=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',text,re.S)
 assert body,'Displayed matrix missing'
 rows=[[sp.Integer(x.strip()) for x in row.split('&')] for row in body[1].split(r'\\')]
 assert all(len(r)==len(rows[0]) for r in rows)
 idx=re.search(r'\$\{?([a-z])\}?_\{([1-9])([1-9])\}',text)
 assert idx,'Displayed index missing'
 i,j=int(idx[2]),int(idx[3]);v=rows[i-1][j-1] if i<=len(rows) and j<=len(rows[0]) else None
 return rows,idx[1],i,j,v

def formatting(text):
 # All current sources use ordinary balanced TeX groups; no malformed exemptions.
 assert text.count('$')%2==0,'Unbalanced math delimiters'
 depth=0
 for c in text:
  if c=='{':depth+=1
  elif c=='}':depth-=1
  assert depth>=0,'Unbalanced groups'
 assert depth==0,'Unbalanced groups'
 assert text.count(r'\begin{')==text.count(r'\end{')

def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=r['question'];meta=r['generation']
 if meta['eligible_for_learning']:
  assert {':question/worked-solution',':question/difficulty',':question/answer-fields'}<=set(q),'Normal record missing required content'
 a,letter,i,j,value=read_display(q[':question/problem'])
 assert letter.upper()==meta['parameters']['letter']
 assert len(a)!=len(a[0]) and all(-9<=x<=9 for row in a for x in row)
 assert meta['mathematical_fingerprint']==g.digest([len(a),len(a[0]),i,j,int(value) if value is not None else None])
 formatting(q[':question/problem'])
 f,=q[':question/answer-fields'];assert f[':answer-field/type'] in (':answer-field.type/radio',':answer-field.type/blank')
 bank=f[':answer-field/choices'];values=[]
 for b in bank:
  if b[':answer/type']==':answer.type/text':assert b[':answer/value']=='No such entry';v=None
  else:assert b[':answer/type']==':answer.type/math';v=sp.Integer(b[':answer/value'])
  values.append(v)
 assert len(set(values))==len(values),'Duplicate/equivalent options'
 assert values.count(value)==1,'Missing/ambiguous correct entry'
 assert len({b[':answer/id'] for b in bank})==len(bank)
 if meta['eligible_for_learning']:assert ':answer-field/correct' in f,'Normal record missing correct ref'
 if ':answer-field/correct' in f:
  ref=f[':answer-field/correct'];assert ref[0]==':answer/id'
  assert next(v for b,v in zip(bank,values) if b[':answer/id']==ref[1])==value,'Wrong correct designation'
 else:assert meta['origin']=='observed-parameterized' and meta['source'] in ('q-13488','q-13496')
 displayed_question={k:v for k,v in q.items() if k not in (':question/id',':question/answer-fields')}
 correct_value=(':answer.type/text','No such entry') if value is None else (':answer.type/math',str(value))
 identity_content={'version':g.VERSION,'question':displayed_question,'field_type':f[':answer-field/type'].split('/')[-1],'key':f[':answer-field/key'],'bank':sorted((b[':answer/type'],b[':answer/value']) for b in bank),'correct_present':':answer-field/correct' in f,'correct':correct_value if ':answer-field/correct' in f else None}
 actual_identity=hashlib.sha256(json.dumps(identity_content,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 assert meta['content_identity']==actual_identity,'Content identity mismatch'
 assert q[':question/id']==g.uid('question:'+actual_identity)
 if f[':answer-field/type'].endswith('/blank'):
  assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem'] and len(bank)==1
 else:assert len(bank)==5
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];formatting(sol)
  b,sl,si,sj,sv=read_display(sol);assert (b,sl,si,sj,sv)==(a,letter,i,j,value),'Solution has stale matrix/index'
  suffix=lambda k:{1:'st',2:'nd',3:'rd'}.get(k,'th')
  assert '$'+str(i)+'$'+suffix(i)+' row' in sol,'Row prose mismatch'
  assert '$'+str(j)+'$'+suffix(j)+' column' in sol,'Column prose mismatch'
  if value is None:
   assert 'no such entry' in sol and 'has $'+str(len(a))+'$ rows and $'+str(len(a[0]))+'$ columns' in sol
  else:
   final=re.search(r'Therefore,.*?=([-0-9]+)\.\$',sol)
   assert final and sp.Integer(final[1])==value,'Incorrect prose final entry'
 if meta['eligible_for_learning']:
  level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':assert (len(a),len(a[0])) in ((2,3),(3,2),(3,4),(5,4))
  elif level=='moderate':assert (len(a),len(a[0])) in ((5,6),(6,5)) and max(i,j)>=4
  else:assert (len(a),len(a[0])) in ((6,7),(7,6)) and max(i,j)>=5
  # Derive operations directly from the actual printed matrix, not generator bank values.
  m,n=len(a),len(a[0]);ri=i+1 if i<m else i-1;cj=j+1 if j<n else j-1
  profile=meta['profile'];positions=[(i,j)]
  if profile=='overflow_locations':
   assert level=='easy' and f[':answer-field/type']==':answer-field.type/radio' and value is None
   if i==m+1 and 1<=j<=n:
    col=j+1 if j<n else j-1;positions=[None,(m,j),(1,j),(m,col),(1,col)]
   else:
    assert j==n+1 and 1<=i<=m,'Invalid printed overflow bounds'
    row=i+1 if i<m else i-1;positions=[None,(i,n),(i,1),(row,n),(row,1)]
  else:assert 1<=i<=m and 1<=j<=n and value is not None,'Numeric default lacks a displayed existing entry'
  if profile=='location_no_entry':positions +=[(ri,j),(i,cj),(ri,cj),None]
  elif profile=='swap_no_entry':positions +=[(j,i),(ri,j),(i,cj),None]
  elif profile=='four_locations':
   k=j-1 if j>1 and j-1!=cj else j+2 if j+2<=n else j-2
   positions +=[(ri,j),(i,cj),(ri,cj),(i,k)]
  expected=[None if pos is None else a[pos[0]-1][pos[1]-1] for pos in positions]
  assert set(expected)==set(values),'Bank is not the complete displayed indexing-error operation bank'
 return r

def native(label,r):
 f=r['question'][':question/answer-fields'][0]
 assert ':answer-field/correct' in f
 ref=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ref else 'rejected','purpose':'complete radio bank'} for a in f[':answer-field/choices']]
 else:
  c=f[':answer-field/choices'][0][':answer/value']
  # Unreduced arithmetic entries exercise the real scalar parser beyond identity.
  checks=[{'submitted':s,'expected':e,'purpose':p} for s,e,p in [(c,'accepted','canonical scalar'),('('+str(int(c)*2)+')/2','accepted','unreduced equivalent fraction'),('('+c+')+1','rejected','wrong scalar'),('('+c+')-1','rejected','wrong scalar')]]
 return {'label':label,'record':r,'checks':checks}

def source_fidelity(source,r):
 old=g.SOURCES[source];q=r['question'];of=old[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
 for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
  assert (key in q)==(key in old),'Source attribute presence mismatch'
 for key in (':question/problem',':question/worked-solution'):
  assert q.get(key)==old.get(key),'Complete source prose/layout/stage mismatch'
 if ':question/difficulty' in old:assert q[':question/difficulty']==old[':question/difficulty'][':db/ident']
 assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
 assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'] and f[':answer-field/key']==of[':answer-field/key']
 oldbank=sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in of[':answer-field/choices'])
 newbank=sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])
 assert oldbank==newbank,'Displayed complete source bank mismatch'
 if ':answer-field/correct' in of:
  ans=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert ans[':answer/value']==of[':answer-field/correct'][':answer/value']
 return {'source_id':source,'template':g.STYLE[source],'matched_values':len(newbank),'complete_bank_matched':True,'raw_key_presence_exact':True,'prompt_exact':True,'solution_exact':True if ':question/worked-solution' in old else None,'correct_designation_matched':True if ':answer-field/correct' in of else None,'missing_original_correct':':answer-field/correct' not in of}

def expect_rejected(call):
 try:call()
 except (ValueError,AssertionError):return
 raise AssertionError('Invalid instance/mutation was accepted')

def main():
 fidelity=[];cases=[];reviews=[];native_inputs=[];default=[]
 for sid,old in g.SOURCES.items():
  p=g.source_parameters(sid);r=check(g.generate('easy',profile='raw:'+sid,parameters=p))
  fidelity.append(source_fidelity(sid,r));cases.append({'source_id':sid,'level':'easy','level_origin':'observed' if ':question/difficulty' in old else 'authored API workload only; raw difficulty omitted','template':g.STYLE[sid],'parameters':p,'profile':'raw:'+sid})
  if ':answer-field/correct' in r['question'][':question/answer-fields'][0]:native_inputs.append(native('raw-'+sid,r))
  else:
   completed=check(g.generate('easy',profile='completed:'+sid,parameters=p));native_inputs.append(native('authored-completion-'+sid,completed))
  # Parameter change transported injectively through all source cell recipes and
  # opaque external scalar slots. This verifies masks away from their anchor.
  changed=copy.deepcopy(p);changed['matrix']=[[-v for v in row] for row in p['matrix']];changed['external']={k:-v for k,v in p['external'].items()};changed['letter']='Z'
  v=check(g.generate('easy',profile='raw:'+sid,parameters=changed))
  if ':answer-field/correct' in v['question'][':question/answer-fields'][0]:native_inputs.append(native('changed-raw-'+sid,v))
  reviews.append({'label':'Observed original and parameterized evidence variant '+sid,'original':old,'raw_replay':r,'variant':v})
 # Verify every level-eligible demand family and whole authored bank in default sampling.
 coverage={}
 for level in g.LEVELS:
  rows=[check(g.generate(level,seed)) for seed in range(180)]
  templates=collections.Counter(r['generation']['template'] for r in rows);profiles=collections.Counter(r['generation']['profile'] for r in rows)
  assert set(templates)==set(g.level_templates(level)) and set(profiles)==set(g.level_profiles(level))
  demands=collections.Counter('missing' if read_display(r['question'][':question/problem'])[-1] is None else 'existing' for r in rows)
  assert set(demands)==({'missing','existing'} if level=='easy' else {'existing'})
  if level=='easy':
   directions={('row' if read_display(r['question'][':question/problem'])[2]>len(read_display(r['question'][':question/problem'])[0]) else 'column') for r in rows if read_display(r['question'][':question/problem'])[-1] is None}
   assert directions=={'row','column'}
  coverage[level]={'templates':dict(templates),'profiles':dict(profiles),'assessed_demands':dict(demands)};default+=rows
  native_inputs +=[native(level+'-'+str(k),r) for k,r in enumerate(rows)]
  for t in g.level_templates(level):
   examples=[check(g.generate(level,900+k,template=t)) for k in range(2)]
   reviews +=[{'label':'Generated '+level+' '+t+' '+str(k),'variant':r} for k,r in enumerate(examples)]
 # Exhaustively enumerate the meaningful narrow task domain. Irrelevant cells
 # intentionally remain constant and do not inflate the count.
 counts={};radio_counts={};fingerprints=set()
 dims={'easy':((2,3),(3,2),(3,4),(5,4)),'moderate':((5,6),(6,5)),'hard':((6,7),(7,6))}
 for level in g.LEVELS:
  count=0;radio=collections.Counter()
  for m,n in dims[level]:
   for i in range(1,m+1):
    for j in range(1,n+1):
     if level=='moderate' and max(i,j)<4 or level=='hard' and max(i,j)<5:continue
     for v in range(-9,10):
      p={'matrix':[[0]*n for _ in range(m)],'i':i,'j':j,'letter':'A'};p['matrix'][i-1][j-1]=v
      r=check(g.generate(level,template='display_blank',parameters=p,profile='blank'))
      fp=r['generation']['mathematical_fingerprint'];assert fp not in fingerprints;fingerprints.add(fp);count+=1
      for profile in g.VALID_RADIO_PROFILES:
       try:locs=g.default_positions(p,profile)
       except ValueError:continue
       if len(set(locs))!=len(locs):continue
       pp=copy.deepcopy(p);wrongvalues=iter(x for x in range(-9,10) if x!=v)
       for pos in locs[1:]:
        if pos is not None:pp['matrix'][pos[0]-1][pos[1]-1]=next(wrongvalues)
       check(g.generate(level,template='display_radio',profile=profile,parameters=pp));radio[profile]+=1
  counts[level]=count;radio_counts[level]=dict(radio)
 assert counts=={'easy':836,'moderate':798,'hard':988}
 valid_counts=dict(counts);absent_count=0;absent_records=[]
 # No-entry demand has only dimensions and the bounded overflowing index, not
 #19 scalar possibilities or arbitrary unused matrix cells. Enumerate all26.
 for m,n in dims['easy']:
  for i,j in [(m+1,j) for j in range(1,n+1)]+[(i,n+1) for i in range(1,m+1)]:
   p={'matrix':[[0]*n for _ in range(m)],'i':i,'j':j,'letter':'A'}
   locs=g.default_positions(p,'overflow_locations')
   for pos,v in zip(locs[1:],(-9,-8,-7,-6)):p['matrix'][pos[0]-1][pos[1]-1]=v
   rec=check(g.generate('easy',template='inline_no_entry_radio',profile='overflow_locations',parameters=p))
   fp=rec['generation']['mathematical_fingerprint'];assert fp not in fingerprints;fingerprints.add(fp);absent_count+=1;absent_records.append(rec)
   native_inputs.append(native('exhaustive-no-entry-'+str(m)+'x'+str(n)+'-'+str(i)+str(j),rec))
 assert absent_count==26
 counts['easy']+=absent_count;radio_counts['easy']['overflow_locations']=absent_count
 # Identity/dedup regression: aliases and unused cell values never make a new
 # assessed task. Prompt/bank/solution differences do make a new content ID.
 r=default[0];p=copy.deepcopy(r['generation']['parameters']);level=r['question'][':question/difficulty'].split('/')[-1];template=r['generation']['template'];profile=r['generation']['profile']
 other=g.generate(level,321,template,parameters=p,profile=profile)
 assert r['question'][':question/id']==other['question'][':question/id']
 assert {a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']}=={a[':answer/id'] for a in other['question'][':question/answer-fields'][0][':answer-field/choices']}
 p['letter']='Z';alias=check(g.generate(level,parameters=p,template=template,profile=profile))
 assert alias['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint'] and alias['question'][':question/id']!=r['question'][':question/id']
 pp=copy.deepcopy(p);pp['external']={'zero':1,'two':2};extra=check(g.generate(level,parameters=pp,template=template,profile=profile));assert extra['question'][':question/id']==alias['question'][':question/id']
 blankp={'matrix':[[1,2,3],[4,5,6]],'i':2,'j':3,'letter':'A'}
 one=g.generate('easy',template='display_blank',parameters=blankp);blankp['matrix'][0][0]=-9;two=g.generate('easy',template='display_blank',parameters=blankp)
 assert one['generation']['mathematical_fingerprint']==two['generation']['mathematical_fingerprint'] and one['question'][':question/id']!=two['question'][':question/id']
 absent=absent_records[0];p=copy.deepcopy(absent['generation']['parameters']);p['matrix']=[[-x for x in row] for row in p['matrix']]
 alternate=check(g.generate('easy',template='inline_no_entry_radio',profile='overflow_locations',parameters=p))
 assert alternate['generation']['mathematical_fingerprint']==absent['generation']['mathematical_fingerprint'] and alternate['question'][':question/id']!=absent['question'][':question/id']
 f=absent['question'][':question/answer-fields'][0]
 wrong=copy.deepcopy(absent);wrong['question'][':question/answer-fields'][0][':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/type']==':answer.type/math')];expect_rejected(lambda:check(wrong))
 # Bounds and whole-bank collisions must reject explicit overflow inputs.
 p=copy.deepcopy(absent['generation']['parameters']);m,n=len(p['matrix']),len(p['matrix'][0])
 for i,j in ((m+2,1),(1,n+2),(m+1,n+1),(0,1),(1,0),(1,1)):
  pp=copy.deepcopy(p);pp['i'],pp['j']=i,j;expect_rejected(lambda pp=pp:g.generate('easy',template='inline_no_entry_radio',parameters=pp))
 pp=copy.deepcopy(p);pp['matrix']=[[0]*n for _ in range(m)];expect_rejected(lambda:g.generate('easy',template='inline_no_entry_radio',parameters=pp))
 expect_rejected(lambda:g.generate('easy',template='display_blank',parameters=p))
 for level in ('moderate','hard'):expect_rejected(lambda level=level:g.generate(level,template='inline_no_entry_radio'))
 orders={tuple(a[':answer/value'] for a in g.generate('easy',seed,profile='raw:q-13497')['question'][':question/answer-fields'][0][':answer-field/choices']) for seed in range(20)};assert len(orders)>10
 wrong=copy.deepcopy(one);wrong['question'][':question/worked-solution']=wrong['question'][':question/worked-solution'].replace('=6.$','=5.$');expect_rejected(lambda:check(wrong))
 wrong=copy.deepcopy(one);wrong['question'][':question/worked-solution']=wrong['question'][':question/worked-solution'].replace('$2$nd row','$3$rd row');expect_rejected(lambda:check(wrong))
 wrong=copy.deepcopy(one);del wrong['question'][':question/worked-solution'];expect_rejected(lambda:check(wrong))
 bad=copy.deepcopy(blankp);bad['matrix'][0][0]=True;expect_rejected(lambda:g.generate('easy',parameters=bad,template='display_blank'))
 for level in ('moderate','hard'):
  expect_rejected(lambda level=level:g.generate(level,parameters=blankp,template='display_blank'))
  m,n={'moderate':(5,6),'hard':(6,7)}[level]
  shallow={'matrix':[[0]*n for _ in range(m)],'i':1,'j':1,'letter':'A'}
  expect_rejected(lambda level=level,shallow=shallow:g.generate(level,parameters=shallow,template='display_blank'))
 expect_rejected(lambda:g.generate('easy',profile='blank',template='display_radio'))
 bad=copy.deepcopy(blankp);bad['matrix']=[[0,0,0],[0,0,0]];expect_rejected(lambda:g.generate('easy',parameters=bad,template='display_radio',profile='location_no_entry'))
 save('source-cases.json',cases);save('source-replay.json',{'sources':fidelity,'complete_banks_matched':7,'total_source_values':27,'matched_source_values':27,'observed_correct_designations_matched':5,'observed_correct_designations_total':5,'missing_original_correct_designations':2,'worked_solutions_exact':5,'worked_solutions_available':5,'raw_omissions_preserved':7})
 save('review.json',reviews);save('native-input.json',native_inputs)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 native_result=json.loads((HERE/'native-grading.json').read_text())
 assert native_result['documented_unresolved_checks']==0
 reviewtext='# Matrix entry generator review\n\nFrozen source: math basis 1356. Raw missing references, ratings and solutions stay missing. Authored variants/completions are labeled; larger visual scans do not add arithmetic.\n'
 for item in reviews:
  reviewtext+='\n## '+item['label']+'\n\n'
  if 'original' in item:
   old=item['original'];reviewtext+='Original:\n\n'+old[':question/problem']+'\n\n'+old.get(':question/worked-solution','[Absent worked solution; absent correct designation and rating.]')+'\n\nOriginal bank: '+', '.join(a[':answer/value'] for a in old[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'
  reviewtext+='Variant ('+item['variant']['generation']['origin']+'):\n\n'+g.markdown(item['variant'])+'\n'
 (HERE/'review.md').write_text(reviewtext)
 save('validation.json',{'passed':True,'database':g.CAPTURE['database'],'basis':1356,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_fidelity':{'complete_banks':'7/7','answer_values':'27/27','correct_designations':'5/5 available; 2 remain absent','worked_solutions':'5/5 available','omission_presence':'7/7'},'default_sample_records':len(default),'default_coverage':coverage,'exhaustive_meaningful_tasks':counts,'existing_entry_tasks':valid_counts,'absent_entry_tasks':{'easy':absent_count,'moderate':0,'hard':0},'total_meaningful_tasks':len(fingerprints),'exhaustive_supported_radio_tasks':radio_counts,'native':{k:native_result[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_records':len(native_inputs),'tests':['independent displayed matrix/index/value and solution prose readback','every observed profile original and signed changed parameters','6 easy demand/presentation families and5 banks;5 families and4 banks at moderate/hard','exhaustive bounded task and complete-radio eligibility domains','strict authored level/number-form boundaries and one-index overflow-by-one guard','seed/order identity and cosmetic/irrelevant parameter dedup','deliberate final-entry and row-prose mutation rejection','blank equivalent unreduced fraction and incorrect entries through native grader'],'limitations':['Only easy is an observed label; moderate/hard are authored visual-scan workload claims.','Two raw sources lack ratings, correct refs and worked solutions; native tests use explicitly authored evidence completions.','Two historical external distractor values have unresolved error intent and remain evidence-only parameter slots.','Larger scans increase visual bookkeeping only; no new mathematical method is claimed.'],'hashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'source-cases.json',HERE/'native-grading.json')}})
 print('Validated 7 source replays, 540 default samples, 2648 distinct narrow-domain tasks; native grading passed.')
if __name__=='__main__':main()
