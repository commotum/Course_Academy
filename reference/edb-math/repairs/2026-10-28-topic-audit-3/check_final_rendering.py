"""Reuse strict rendering only for byte-equivalent complete presentation inputs."""
import hashlib,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];read=lambda p:json.loads(p.read_text());old=H/'prepublication-check';D=H/'final-check';prior=read(old/'rendering.json');inputs=read(old/'render-input.json');final=read(D/'render-input.json');assert prior['passed']and len(prior['checks'])==len(inputs)
fingerprint=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
cache={fingerprint(x):v for x,v in zip(inputs,prior['checks'])};delta={fingerprint(x):x for x in final if fingerprint(x)not in cache};fresh=list(delta.values());(D/'render-delta-input.json').write_text(json.dumps(fresh,indent=2)+'\n')
if fresh:
 subprocess.run(['/home/jake/Developer/MA/.venv/bin/python',str(R/'scripts/check_math_rendering.py'),str(D/'render-delta-input.json'),str(D/'render-delta.json')],check=True)
 result=read(D/'render-delta.json');assert result['passed']and len(result['checks'])==len(fresh);cache.update({fingerprint(x):v for x,v in zip(fresh,result['checks'])})
checks=[cache[fingerprint(x)]for x in final];failures=[x for x in checks if x['errors']or x['raw_display_delimiters']];assert not failures
report={'passed':True,'strict_undefined_commands':True,'actual_player_renderer':True,'fields':len(checks),'failures':failures,'checks':checks,'database_writes':0,'exact_input_cache':{'source':'prepublication-check/rendering.json','source_input_sha256':hashlib.sha256((old/'render-input.json').read_bytes()).hexdigest(),'source_report_sha256':hashlib.sha256((old/'rendering.json').read_bytes()).hexdigest(),'final_input_sha256':hashlib.sha256((D/'render-input.json').read_bytes()).hexdigest(),'reused_exact_payloads':sum(fingerprint(x)not in delta for x in final),'new_unique_payloads_rendered':len(fresh)}}
(D/'rendering.json').write_text(json.dumps(report,indent=2)+'\n');print('Final strict rendering:',len(checks),'fields;',len(fresh),'new unique complete payloads rendered,0 failures.')
