"""Current-CLI regression for 79a24ab401bd284df93a, with real delivery filtering."""
import argparse, collections, json, os, subprocess, sys
from pathlib import Path
from check_repair import HERE, inspect, save
OUT=HERE/'evidence/batch-repair'
REPO=Path('/home/jake/Developer/Course_Academy')

def run(args, **kw):
 p=subprocess.run([str(x) for x in args],text=True,capture_output=True,**kw)
 if p.returncode: raise AssertionError(f'{args}: exit {p.returncode}\n{p.stderr}\n{p.stdout[:1500]}')
 return p.stdout

def probe(rows):
 groups=collections.defaultdict(list)
 for r in rows:
  bank,ci=inspect(r)
  mags=tuple(collections.Counter(abs(z[d]) for z in bank).most_common(1)[0][0] for d in (0,1))
  outlier=next(z for z in bank if tuple(map(abs,z))!=mags)
  shape=('unit-first' if abs(outlier[1])==mags[1] else 'unit-second' if abs(outlier[0])==mags[0] else 'swapped-magnitude')
  groups[shape].append({'id':r['question'][':question/id'],'correct':bank[ci],'outlier':outlier,'position':ci,
                        'matches':[outlier[d]*bank[ci][d]>0 for d in (0,1)]})
 report={}
 for shape,items in groups.items():
  n=len(items);hits=[sum(i['matches'][d] for i in items) for d in (0,1)]
  assert all(0<h<n for h in hits),(shape,hits,n,'uniform sign cue')
  if len(rows)>=4:
   assert {tuple(1 if x>0 else -1 for x in i['correct']) for i in items}=={(-1,-1),(-1,1),(1,-1),(1,1)},(shape,'missing signed decision case')
  report[shape]={'count':n,'same_sign_successes':hits,'opposite_sign_successes':[n-h for h in hits],
                 'correct_positions':sorted({i['position'] for i in items}),'records':items}
 return report

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--small-sample',action='store_true');a=ap.parse_args()
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'assets').mkdir(exist_ok=True)
 manifest=json.loads((HERE/'package.json').read_text())
 env=dict(os.environ,COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(OUT/'assets'),PYTHONDONTWRITEBYTECODE='1')
 def generate(seed,count):
  cmd=[sys.executable,'-B',HERE/manifest['entrypoint'],'--difficulty','easy','--count',count,'--seed',seed,'--format','json']
  return json.loads(run(cmd,cwd=HERE,env=env)),list(map(str,cmd))
 rows,cmd=generate(1278010737,5)
 prospective=OUT/'prospective.json';prospective.write_text(json.dumps(rows,indent=2)+'\n')
 before=probe(rows)

 assert generate(1278010737,5)[0]==rows,'CLI is not deterministic'
 replay=[]
 for r in rows:
  from check_repair import g
  assert g.generate(seed=r['generation']['seed'],bank_profile=r['generation']['bank_profile'])['question']==r['question']
 for records,label in [(prospective,'raw')]:
  result=run([sys.executable,'-B',HERE/'reproduce_batch_shortcut.py',records])
  (OUT/f'reviewer-{label}.json').write_text(result)
 deliverycmd=[sys.executable,'-B',REPO/'generate/pipeline/check_delivery.py','--input',prospective,'--source','/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186161967/source/source.json','--inventory','/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186161967/source/inventory.json','--difficulty','easy','--output',OUT/'delivery','--asset-root',OUT/'assets','--math-root','/media/jake/SSD/EDB/math']
 run(deliverycmd)
 accepted=OUT/'delivery/accepted.json';survivors=json.loads(accepted.read_text())
 assert len(survivors)==len(rows),'Delivery removed a batch witness'
 after=probe(survivors)
 assert set(after)==set(before)
 (OUT/'reviewer-delivered.json').write_text(run([sys.executable,'-B',HERE/'reproduce_batch_shortcut.py',accepted]))
 extra=[];sample=[]
 if a.small_sample:
  for seed,count in [(0,2),(1,3),(38191,4),(20261022,5),(19,10),(20,30)]:
   rr,cc=generate(seed,count);summary=probe(rr);extra+=rr
   sample.append({'seed':seed,'count':count,'groups':summary})
  assert {r['generation']['bank_profile'] for r in extra}==set(g.PROFILES)
  for count in (0,1):
   rr,_=generate(0,count);assert len(rr)==count
   for r in rr:inspect(r)
 (OUT/'small-sample.json').write_text(json.dumps(extra,indent=2)+'\n')
 cases=[]
 for i,r in enumerate(survivors+extra):
  _,ci=inspect(r);choices=r['question'][':question/answer-fields'][0][':answer-field/choices']
  cases.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':v[':answer/id'],'expected':'accepted' if j==ci else 'rejected','purpose':'Complete independently evaluated row additions'} for j,v in enumerate(choices)]})
 (OUT/'grader-input.json').write_text(json.dumps(cases,indent=2)+'\n')
 report={'status':'pass','cli_command':cmd,'delivery_command':list(map(str,deliverycmd)),'deterministic':True,'raw':before,'delivered':after,'small_sample':sample,'graded_record_count':len(cases)}
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'status':'pass','raw_count':len(rows),'survivors':len(survivors),'groups':{k:{kk:vv for kk,vv in v.items() if kk!='records'} for k,v in after.items()},'small_sample_count':len(extra)}))
if __name__=='__main__':main()
