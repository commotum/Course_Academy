import json,re,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];D=json.loads((H/'current.json').read_text());wanted={q.get(':question/math-academy-id')for q in D['questions']};old=set((H/'source-paths-fresh.txt').read_text().splitlines());paths=set();n=0
with subprocess.Popen(['rg','--files','--hidden','--no-ignore','reference/mathacademy'],cwd=R,text=True,stdout=subprocess.PIPE)as p:
 for line in p.stdout:
  n+=1;path=line.strip()
  if not path.endswith('.json'):continue
  name=Path(path).name;m=re.search(r'(q-\d+)|(?:example|e)-(\d+)',name)
  ident=m[1]or'e-'+m[2]if m else None
  if ident is not None and ident in wanted:paths.add(path)
 assert p.wait()==0
added=paths;(H/'source-paths-added.txt').write_text('\n'.join(sorted(added))+'\n');(H/'source-paths-fresh.txt').write_text('\n'.join(sorted(paths))+'\n');(H/'source-index-provenance.json').write_text(json.dumps({'basis_t':9837,'command':'rg --files --hidden --no-ignore reference/mathacademy','paths_examined':n,'scoped_json_candidates':len(paths),'new_hashed_or_other_capture_variants':len(added),'identity_matcher':'(q-ID) anywhere in filename, including history-q-ID-hash and before/after-hash; source loader additionally checks genuine source HTML/DOM identity.'},indent=2)+'\n');print('candidates',len(paths),'added',len(added))
