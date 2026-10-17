"""Losslessly compress large derived audit files, verifying every uncompressed hash."""
from pathlib import Path
import gzip,hashlib,json,shutil
HERE=Path(__file__).resolve().parent
names=['content.jsonl','baseline-comparison.jsonl','entities.json','relations.json']
rows=[]
for name in names:
 source=HERE/name;target=HERE/(name+'.gz')
 if not source.exists():continue
 with source.open('rb') as f:before=hashlib.file_digest(f,'sha256').hexdigest()
 size=source.stat().st_size
 with source.open('rb') as f,gzip.open(target,'wb',compresslevel=6) as g:shutil.copyfileobj(f,g)
 with gzip.open(target,'rb') as g:assert hashlib.file_digest(g,'sha256').hexdigest()==before
 with target.open('rb') as f:compressed=hashlib.file_digest(f,'sha256').hexdigest()
 rows.append({'file':name,'uncompressed_sha256':before,'uncompressed_bytes':size,
  'compressed_file':target.name,'compressed_sha256':compressed,'compressed_bytes':target.stat().st_size})
 source.unlink();print(name,size,'->',target.stat().st_size,flush=True)
if rows:(HERE/'derived-compression.json').write_text(json.dumps(rows,indent=2)+'\n')
