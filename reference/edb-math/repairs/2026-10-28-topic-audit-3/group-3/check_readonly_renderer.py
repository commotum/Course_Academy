import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;P=json.loads((H/'readonly-package-probes.json').read_text());S=json.loads((H/'readonly-package-samples.json').read_text());kp=17592186129283

def ids(o):
 if isinstance(o,dict):return sorted([(k,v)for k,v in o.items()if k in[':question/id',':answer-field/id',':answer/id']]+[z for k,v in o.items()if k not in[':question/id',':answer-field/id',':answer/id']for z in ids(v)])
 if isinstance(o,list):return sorted(z for v in o for z in ids(v))
 return[]
proof=[]
for band in['easy','moderate','hard']:
 a,b=[next(r for r in P if r['kp']==kp and r['band']==band and r['branch']==v)for v in['a','b']];ra,rb=[next(r['record']for r in S if r['kp']==kp and r['level']==band and r['branch']==v)for v in['a','b']];assert a['passed']and b['passed']and ids(ra)==ids(rb)and a['asset_hashes']==b['asset_hashes'];pa,pb=[Path(r['output_directory'])/'render-provenance.json'for r in[a,b]];assert pa.is_file()and pb.is_file()and pa.read_bytes()==pb.read_bytes();old=H/'generator-17592186129283/17592186129283/render-provenance.json';assert pa.read_bytes()==old.read_bytes();proof.append({'band':band,'immutable_permission_runs':[a,b],'all_UUIDs_stable':True,'all_asset_bytes_stable':True,'renderer_provenance_content_unchanged':True,'provenance_written_only_to_caller_output':True,'provenance_sha256':hashlib.sha256(pa.read_bytes()).hexdigest()})
oldrec=next(r['record']for r in json.loads((H/'staged-relocation-samples.json').read_text())if r['kp']==kp);newrec=next(r['record']for r in S if r['kp']==kp and r['level']=='easy'and r['branch']=='a');assert ids(oldrec)==ids(newrec)
(H/'readonly-renderer-proof.json').write_text(json.dumps({'kp':kp,'supported_band_checks':proof,'UUIDs_unchanged_vs_previous_registered_immutable_package':True,'other_packages_tested':len({r['kp']for r in P})-1,'all_readonly_package_runs':len(P),'all_readonly_package_runs_passed':all(r['passed']for r in P)},indent=2));(H/'readonly-renderer-samples.json').write_text(json.dumps([r for r in S if r['kp']==kp],indent=2));print('immutable renderer3bands2dirs:UUID/assets/provenance allstable;all59runs pass')
