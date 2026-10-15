"""Verify registered immutable baseline and freeze/check owned draft outputs."""
import sys;sys.dont_write_bytecode=True
import pathlib,hashlib,json
D=pathlib.Path(__file__).resolve().parent;ROOT=D.parents[2];BASE=D.parent;KP='17592186129122'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def baseline_rows():
 paths=[BASE/(KP+'.py')]+sorted((BASE/KP).rglob('*'))+sorted((BASE/'__pycache__').glob(KP+'.*.pyc'))
 return [{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} if p.is_file() else {'path':str(p.relative_to(ROOT)),'kind':'directory'} for p in paths if p.is_file() or p.is_dir()]
def owned():
 paths=[D.with_suffix('.py')]+sorted(D.rglob('*'))
 return {str(p.relative_to(ROOT)):sha(p) for p in paths if p.is_file() and p!=D/'freeze.json'}
expected=json.loads((D/'immutable-baseline.json').read_text())['files'];actual=baseline_rows();assert expected==actual,'Registered numeric script/tree/bytecode changed'
if '--check' in sys.argv:
 frozen=json.loads((D/'freeze.json').read_text());assert frozen['files']==owned(),'Owned draft hash/pathset changed after freeze'
 print('PASS: registered baseline exact; all',len(frozen['files']),'owned draft hashes/pathset exact')
else:
 (D/'immutable-verification.json').write_text(json.dumps({'status':'pass','registered_script_sha256':sha(BASE/(KP+'.py')),'baseline_paths':len(actual),'entire_recursive_tree_and_matching_sibling_bytecode_unchanged':True,'database_writes':0},indent=2)+'\n')
 files=owned();(D/'freeze.json').write_text(json.dumps({'status':'frozen for independent parent review','draft_sha256':sha(D.with_suffix('.py')),'files':files},indent=2)+'\n');print('FROZEN',sha(D.with_suffix('.py')),len(files),'owned files;',len(actual),'immutable baseline paths exact')
