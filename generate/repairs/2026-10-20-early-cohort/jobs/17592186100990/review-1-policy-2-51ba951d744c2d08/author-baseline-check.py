#!/usr/bin/env python3
"""Current-package regressions, independent visible-coordinate checks, shared filters."""
import argparse, copy, importlib.util, json, os, re, subprocess, sys
from collections import defaultdict
from pathlib import Path
W=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186100990/review-1-policy-2-51ba951d744c2d08/baseline-package')
ROOT=next(p for p in W.parents if (p/'generate/pipeline/check_delivery.py').is_file())
E=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186100990/review-1-policy-2-51ba951d744c2d08/author-baseline');E.mkdir(exist_ok=True)
PYTHON=ROOT/'.venv/bin/python'; ENGINE=ROOT/'generate/runs/current/check-engine'
spec=importlib.util.spec_from_file_location('generator',W/'17592186100990.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SOURCE=json.loads(Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186100990/source/source.json').read_text())
SOURCES=SOURCE['material']['kp'][':knowledge-point/questions']
COMMANDS=[]
def save(name,data):
 p=E/name;p.write_text(json.dumps(data,indent=2)+'\n');return p
def run(args):
 args=list(map(str,args));r=subprocess.run(args,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(E/'assets')))
 COMMANDS.append({'command':args,'exit_code':r.returncode,'stdout':r.stdout[:1000] if '--format' not in args else '(saved parsed records)','stderr':r.stderr[:3000]})
 if r.returncode:raise AssertionError(f'Command failed: {args}\n{r.stderr}\n{r.stdout[:1000]}')
 return r.stdout

def cli(seed=3782988951,count=5,profile=None,template=None):
 args=[PYTHON,'-B',W/'17592186100990.py','--difficulty','easy','--count',count,'--seed',seed,'--format','json']
 if profile:args+=['--profile',profile]
 if template:args+=['--template',template]
 return json.loads(run(args))

def matrix(q):
 text=q[':question/problem']
 body=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',text,re.S)[1]
 rows=body.split(r'\\');a=[];targets=[]
 for i,row in enumerate(rows,1):
  values=[]
  for j,cell in enumerate(row.split('&'),1):
   box=re.search(r'\\(?:boxed|bbox\[[^\]]*\])\{(-?\d+)\}',cell)
   if box:targets.append((i,j));cell=cell.replace(box[0],box[1])
   values.append(int(cell.strip()))
  a.append(values)
 return a,targets

def canonical(s):return re.sub(r'[{}\s$]','',s)
def correct(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def visible(r):
 q=r['question'];a,targets=matrix(q);assert len(targets)==1,(q[':question/id'],targets)
 i,j=targets[0]
 letter=re.search(r'\$([A-Z])\$',q[':question/problem'])[1].lower()
 for f in q[':question/answer-fields']:
  value=canonical(correct(f))
  want=str(i if f[':answer-field/key']=='field-1' else j) if len(q[':question/answer-fields'])==2 else f'{letter}_{i}{j}'
  assert value==want,(value,want,q[':question/id'])
 sol=q[':question/worked-solution']
 assert re.search(r'intersection of the \$'+str(i)+r'\$(?:st|nd|rd|th) row and \$'+str(j)+r'\$(?:st|nd|rd|th) column',sol),sol
 if len(q[':question/answer-fields'])==2:
  assert 'i='+str(i) in sol and 'j='+str(j) in sol
 else:
  v=str(a[i-1][j-1]);s=canonical(sol);key=f'{letter}_{i}{j}'
  assert key+'='+v in s or v+'='+key in s,s
 return len(a),len(a[0]),i,j,letter

def delivery(records,name,allow_duplicates=False):
 path=save(name+'.json',records);out=E/(name+'-delivery')
 run([PYTHON,ROOT/'generate/pipeline/check_delivery.py','--input',path,'--source','/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186100990/source/source.json','--inventory','/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186100990/source/inventory.json','--difficulty','easy','--output',out,'--asset-root',E/'assets','--math-root','/media/jake/SSD/EDB/math'])
 accepted=json.loads((out/'accepted.json').read_text());assert accepted,name
 if not allow_duplicates:assert len(accepted)==len(records),(name,len(records),len(accepted))
 return accepted

def cue(records,name):
 path=save(name+'-records.json',records)
 run([PYTHON,W/'regression_shortcut.py',path,E/(name+'-cue.json')])
 return json.loads((E/(name+'-cue.json')).read_text())

def group_roles(records,require_contrasts=False):
 groups=defaultdict(list)
 for r in records:
  m,n,i,j,letter=visible(r)
  f=r['question'][':question/answer-fields'][0]
  if not f[':answer-field/type'].endswith('/radio'):continue
  opts=[tuple(map(int,re.search(r'_\{(\d)(\d)\}',a[':answer/value']).groups())) for a in f[':answer-field/choices']]
  # This is visible bank geometry, matrix shape and prompt layout, no profile metadata.
  template='inline' if '$$' not in r['question'][':question/problem'] else 'display'
  key=(template,m,n,tuple(sorted(opts)))
  groups[key].append((opts.index((i,j)),(i,j),opts))
 report=[]
 for k,items in groups.items():
  roles=set(x[1] for x in items)
  if require_contrasts:assert len(roles)>1,('fixed visible-bank answer role',k,roles)
  report.append({'group':str(k),'count':len(items),'targets':sorted(roles),'option_positions':sorted(set(x[0] for x in items))})
 return report

def source_check():
 records=[];summaries=[]
 for q in SOURCES:
  sid=q[':question/math-academy-id'];r=cli(73,1,'completed:'+sid)[0];records.append(r)
  visible(r);assert matrix(q)[0]==matrix(r['question'])[0],sid
  if sid=='q-139629':
   assert [f[':answer-field/key'] for f in r['question'][':question/answer-fields']]==[f[':answer-field/key'] for f in q[':question/answer-fields']]
  fs={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']}
  for f in q[':question/answer-fields']:
   rf=fs[f[':answer-field/key']]
   assert sorted(canonical(a[':answer/value']) for a in f[':answer-field/choices'])==sorted(canonical(a[':answer/value']) for a in rf[':answer-field/choices']),sid
   if ':answer-field/correct' in f:assert canonical(f[':answer-field/correct'][':answer/value'])==canonical(correct(rf)),sid
  if ':question/worked-solution' in q:assert canonical(q[':question/worked-solution'])==canonical(r['question'][':question/worked-solution']),sid
  summaries.append({'source_id':q[':question/id'],'source_profile':sid,'complete_bank':True,'fields':len(fs)})
 # Explicit missing-family boundary: all 16 target assignments using source values.
 original=next(r for r in records if r['generation']['source']=='q-139629')
 controls=[]
 for i in range(1,5):
  for j in range(1,5):
   p=dict(original['generation']['parameters'],i=i,j=j)
   r=g.generate('easy',73,profile='completed:q-139629',parameters=p);visible(r);controls.append(r)
 assert len({tuple(visible(r)[2:4]) for r in controls})==16
 save('source-replays.json',records);save('source-4x4-controls.json',controls)
 save('source-results.json',{'cases':summaries,'four_by_four_targets':16,'missing_highlight_restored_at':[3,1]})
 return records+controls

def shortcut_check():
 batch=cli();assert batch==cli(),'nondeterministic CLI';save('prospective-batch.json',batch)
 summaries={'batch_raw':group_roles(batch,True)}
 summaries['retained_batch_cue']=cue(batch,'prospective')
 accepted=delivery(batch,'prospective-batch')
 summaries['batch_delivered']=group_roles(accepted,True)
 summaries['delivered_cue']=cue(accepted,'prospective-delivered')
 # Every source bank through the actual --count interface, including retained bank.
 fresh=[]
 for bank in g.BANKS:
  for count in (2,3,5):
   rs=cli(19,count,bank)
   group_roles(rs,True)
   if count==5:fresh+=rs
 # Each fixed bank with all of its five target roles. The 4x4 shape fits all
 # observed arrangements and permits holding all other visible evidence fixed.
 controlled=[];irrelevant=[]
 for k,bank in enumerate(g.BANKS):
  offsets=g.BANKS[bank];mi=min(i for i,j in offsets);mj=min(j for i,j in offsets)
  cells=[(i-mi+1,j-mj+1) for i,j in offsets]
  for t,(i,j) in enumerate(cells):
   p={'matrix':[[r*4+c-8 for c in range(4)] for r in range(4)],'i':i,'j':j,'letter':'A'}
   r=g.assemble('easy',101,'inline_radio' if k<2 else 'display_radio',p,bank,cells=cells)
   visible(r);controlled.append(r)
   p2=copy.deepcopy(p);p2['matrix']=[[v+1 for v in row] for row in p['matrix']]
   r2=g.assemble('easy',101,r['generation']['template'],p2,bank,cells=cells);visible(r2)
   assert [canonical(correct(f)) for f in r['question'][':question/answer-fields']]==[canonical(correct(f)) for f in r2['question'][':question/answer-fields']]
   irrelevant.append(r2)
 for rs in (fresh,controlled):
  group_roles(rs,True)
 assert cue(fresh,'all-bank-batches')['attempts']>0
 assert cue(controlled,'controlled')['attempts']==5
 # Two source profiles normalize to the same visible bank shape. Their
 # identical controlled records should deduplicate, preserving all targets.
 controlled_delivered=delivery(controlled,'controlled',allow_duplicates=True)
 assert {x['group']:x['targets'] for x in group_roles(controlled,True)}=={x['group']:x['targets'] for x in group_roles(controlled_delivered,True)}
 fresh_delivered=delivery(fresh,'all-bank-batches',allow_duplicates=True)
 assert {x['group']:x['targets'] for x in group_roles(fresh,True)}=={x['group']:x['targets'] for x in group_roles(fresh_delivered,True)}
 summaries['all_bank_batches']=group_roles(fresh_delivered,True)
 summaries['controlled']=group_roles(controlled_delivered,True)
 summaries['controlled_cue_after_delivery']=cue(controlled_delivered,'controlled-delivered')
 summaries['fresh_cue_after_delivery']=cue(fresh_delivered,'all-bank-delivered')
 # All five fixed option positions and sorted coordinate roles are exercised in
 # every controlled bank. An option-position cue cannot choose every target.
 assert all(x['option_positions']==list(range(5)) for x in summaries['controlled'])
 save('irrelevant-entry-controls.json',irrelevant)
 save('shortcut-results.json',summaries)
 return batch+fresh+controlled+irrelevant

def grading_check(records=None):
 if records is None:
  records=[cli(73,1,'completed:'+sid)[0] for sid in ('q-279553','q-279556')]
  records+=cli(41,5,template='notation_blank')
  defaults=[r for seed in (0,1,2) for r in cli(seed)]
  # Inspect actual fields, rather than trusting a declared supported-template
  # list. The missing family must also occur in ordinary practice generation.
  assert any(len(r['question'][':question/answer-fields'])==1 and
    r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/blank') and
    re.search(r'_\{\d\d\}',correct(r['question'][':question/answer-fields'][0])) for r in defaults)
  records+=defaults
 cases=[]
 for idx,r in enumerate(records):
  m,n,i,j,letter=visible(r);q=r['question'];checks=[]
  for fi,f in enumerate(q[':question/answer-fields']):
   if f[':answer-field/type'].endswith('/radio'):
    for a in f[':answer-field/choices']:
     checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independently checked visible coordinate'})
   elif len(q[':question/answer-fields'])==2:
    value=i if f[':answer-field/key']=='field-1' else j
    for v,expect in [(str(value),'accepted'),(str(value*2)+'/2','accepted'),(str(value+1),'rejected'),('0','rejected')]:
     checks.append({'field_index':fi,'submitted':v,'expected':expect,'purpose':'row or column from visible box'})
   else:
    for v,expect in [(f'{{{letter}}}_{{{i}{j}}}','accepted'),(f'{letter}_{{{i}{j}}}','accepted'),(f'{{{{{letter}}}}}_{{{{{i}}}{{{j}}}}}','accepted'),(f'{letter}_{{{i}{j% n+1}}}','rejected'),(f'{letter}_{{{i%m+1}{j}}}','rejected'),(f'k_{{{i}{j}}}','rejected'),(letter,'rejected'),(str(matrix(q)[0][i-1][j-1]),'rejected')]:
     checks.append({'field_index':fi,'submitted':v,'expected':expect,'purpose':'indexed symbol equivalence or wrong notation/value'})
  cases.append({'label':f'visible-record-{idx}','record':r,'checks':checks})
 path=save('current-grader-input.json',cases)
 run([ENGINE,path,E/'current-grader-report.json'])
 # Assert actual normal generation delivers symbolic blanks, not evidence-only.
 normal=cli(41,5,template='notation_blank')
 assert all(not r['generation']['evidence_only'] and r['generation']['eligible_for_learning'] for r in normal)
 delivered=delivery(normal,'symbolic-practice');assert len(delivered)==5
 return cases

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',choices=['all','source','shortcut','grading'],default='all');args=ap.parse_args()
 try:
  records=[]
  if args.check in ('all','source'):records+=source_check()
  if args.check in ('all','shortcut'):records+=shortcut_check()
  if args.check in ('all','grading'):grading_check(records if records else None)
  if args.check=='all':
   save('render-records.json',[records[0],records[4],records[8],json.loads((E/'prospective-batch.json').read_text())[0]])
  print(json.dumps({'check':args.check,'status':'passed','records_checked':len(records)}))
 finally:save('commands-'+args.check+'.json',COMMANDS)
if __name__=='__main__':main()
