"""Real delivery against whole old pool plus earlier staged bands; retain UI mapping."""
import copy,json,os,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from generate.pipeline.check_delivery import audit
from scripts.generator_evidence import record_sha256,batch_sha256
from scripts.generator_publish import content_fingerprint
from scripts.generator_refill import validate_survivors

def read(p):return json.loads(Path(p).read_text())
def save(p,x):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def main(kp):
 d=H/str(kp);root=d/'package';manifest=read(root/'package.json');inv=copy.deepcopy(read(d/'capture-after-retirement/inventory.json'));source=read(d/'source/source.json');binding=read(d/'package-candidate.json')['refill_plan'];summary=[];allfps=set()
 for band in ['easy','moderate','hard']:
  out=d/'publish'/band;original=d/'verification'/band;delivery=audit(read(original/'records.json'),inv,source,band,out/'delivery',original/'assets',Path('/media/jake/SSD/EDB/math'));accepted=read(out/'delivery/accepted.json');assert len(accepted)>=5
  checked=validate_survivors(accepted,inv,out/'refill',root=root,manifest=manifest,band=band,python=sys.executable,repo_root=ROOT,environment=os.environ.copy(),expected_plan=binding);assert checked['status']=='passed'
  original_rows=read(original/'delivery-postretirement/accepted.json');render=read(original/'render/rendering.json');mapping=[]
  for r in accepted:
   h=record_sha256(r);indices=[i for i,x in enumerate(original_rows) if x==r];assert len(indices)==1;idx=indices[0];cases=[c for c in render['cases'] if c['record_sha256']==h];assert len(cases)==4 and {c['state'] for c in cases}=={'active','completed'} and {c['viewport']['width'] for c in cases}=={390,1100}
   assert all(c['passed'] for c in cases)
   fp=content_fingerprint(r['question']);assert fp not in allfps;allfps.add(fp)
   mapping.append(dict(record_sha256=h,source_index=idx,render_report=str(original/'render/rendering.json'),cases=[dict(state=c['state'],viewport=c['viewport'],screenshot=c['screenshot'],screenshot_sha256=c['screenshot_sha256']) for c in cases]))
  save(out/'ui-coverage.json',dict(passed=True,exact_final_record_objects=True,record_count=len(accepted),records=mapping))
  inv['questions'].extend(r['question'] for r in accepted);inv['fingerprints']=sorted(set(inv['fingerprints'])|{content_fingerprint(r['question']) for r in accepted})
  summary.append(dict(band=band,accepted=len(accepted),batch_sha256=batch_sha256(accepted),raw=len(read(original/'records.json')),duplicates=delivery['duplicate_count'] if 'duplicate_count' in delivery else delivery.get('duplicates'),passed=True));print(kp,band,len(accepted),flush=True)
 save(d/'publication-selection.json',dict(passed=True,total=len(allfps),all_content_unique_across_bands_and_whole_old_pool=True,bands=summary))
if __name__=='__main__':main(int(sys.argv[1]))
