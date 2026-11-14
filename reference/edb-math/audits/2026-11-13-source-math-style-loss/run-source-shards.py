from pathlib import Path
import subprocess,sys,time,json,collections
root=Path('reference/edb-math/audits/2026-11-13-source-math-style-loss')
processes=[]
for i in range(8):
 out=root/f'shard-{i}';out.mkdir(exist_ok=True); log=(root/f'shard-{i}.log').open('w')
 proc=subprocess.Popen([sys.executable,'scripts/audit_capture_math_styles_sources.py','--files',str(root/f'primary-files-{i}.txt'),'--out',str(out)],stdout=log,stderr=subprocess.STDOUT)
 processes.append((i,proc,log));print('launched',i,flush=True)
for i,proc,log in processes:
 code=proc.wait();log.close();print('completed',i,code,flush=True)
 if code:raise SystemExit(code)
records={};counts=collections.Counter();summaries=[]
for i in range(8):
 directory=root/f'shard-{i}';summaries.append(json.loads((directory/'source-summary.json').read_text()));counts.update(summaries[-1]['counts'])
 for line in (directory/'source-formulas.jsonl').open():
  r=json.loads(line);key=r['formula_hash']
  if key in records:
   records[key]['evidence_count']+=r['evidence_count']
   for e in r['evidence']:
    if len(records[key]['evidence'])<12 and e not in records[key]['evidence']:records[key]['evidence'].append(e)
  else:records[key]=r
with (root/'source-formulas.jsonl').open('w') as f:
 for key in sorted(records):f.write(json.dumps(records[key],ensure_ascii=False,separators=(',',':'))+'\n')
for name in ['source-inventory.jsonl','source-unknowns.jsonl','source-evidence.jsonl']:
 with (root/name).open('w') as dst:
  for i in range(8):
   with (root/f'shard-{i}'/name).open() as src:
    for line in src:dst.write(line)
census=json.loads((root/'source-census-summary.json').read_text())
summary={'complete':True,'scope':'Primary original capture sources selected by imported identity/role; census covers all original source tree HTML/JSON/gzip paths. Alternate and aggregate sources explicitly deferred.','counts':dict(counts),'census':census,'unique_formulas':len(records),'unique_styled_formulas':sum(r['styled'] for r in records.values()),'identities':len({r['math_academy_id'] for r in records.values()}),'by_role':dict(collections.Counter(r['role'] for r in records.values())),'formula_errors':sum(bool(r['errors']) for r in records.values()),'limitations':summaries[0]['limitations']+census['limitations'],'shard_elapsed_seconds':[s['elapsed_seconds'] for s in summaries]}
(root/'source-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
