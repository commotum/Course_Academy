"""Run copied read-only packages twice; compare mathematics and stable IDs."""
import concurrent.futures,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from generator_publish import validate_question
candidates=json.loads((H/'generator-candidates.json').read_text());checks=[];render=[]
def plain(value):
    if isinstance(value,list):return[plain(x)for x in value]
    if isinstance(value,dict):return{k:plain(v)for k,v in value.items()if k not in {':question/id',':answer-field/id',':answer/id',':answer-field/correct'}}
    if isinstance(value,str):
        value=re.sub(r'\\(?:left|right)\.', '',value)
        value=re.sub(r'\\(?:left|right)(?![A-Za-z])','',value)
        return value
    return value
def rights(q):
    return[[a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]]for f in q[':question/answer-fields']]
def run(c):
    out=[];rs=[]
    for band in c['supported_difficulties']:
        copies=[]
        for copy_index in range(2):
            with tempfile.TemporaryDirectory(prefix='table-generator-')as td:
                root=Path(td);pkg=root/'package';shutil.copytree(c['directory'],pkg)
                for p in pkg.rglob('*'):p.chmod(0o555 if p.is_dir()else 0o444)
                pkg.chmod(0o555);output=root/'output';output.mkdir();env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(output),'TMPDIR':str(output)}
                args=[sys.executable,str(pkg/c['entrypoint']),'--difficulty',band,'--count','3','--seed','29102977','--format','json']
                p=subprocess.run(args,env=env,capture_output=True,text=True,timeout=100)
                if p.returncode:raise RuntimeError((c['kp'],band,p.stderr))
                raw=json.loads(p.stdout);rows=raw.get('records',[])if isinstance(raw,dict)else raw
                copies.append(rows)
                # Restore directory permissions for cleanup without writing its inputs.
                for d in[pkg]+[p for p in pkg.rglob('*')if p.is_dir()]:d.chmod(0o755)
        assert copies[0]==copies[1],('Relocation changed output',c['kp'],band)
        before=json.loads((H.parent/'generator-probes'/f"{c['kp']}-{band}"/'stdout.json').read_text());before=before.get('records',[])if isinstance(before,dict)else before
        for i,(old,new)in enumerate(zip(before,copies[0])):
            assert plain(old['question'])==plain(new['question']),(c['kp'],band,i,'Mathematics changed')
            assert plain(rights(old['question']))==plain(rights(new['question']))
            validate_question(new['question']);q=new['question']
            for a in[':question/problem',':question/worked-solution']:rs.append({'entity':str(c['kp'])+'-'+band+'-'+str(i),'attribute':a,'value':q[a]})
        out.append({'kp':c['kp'],'band':band,'records':len(copies[0]),'read_only_relocation_parity':True,'mathematics_and_correct_choices_preserved':True})
        (H/f"verified-{c['kp']}-{band}.json").write_text(json.dumps(copies[0],indent=2)+'\n')
    return out,rs
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
    for cs,rs in pool.map(run,candidates):checks+=cs;render+=rs
(H/'candidate-verification.json').write_text(json.dumps({'passed':True,'checks':checks,'records':sum(c['records']for c in checks),'database_writes':0},indent=2)+'\n');(H/'render-input.json').write_text(json.dumps(render,indent=2)+'\n');print('Verified',len(candidates),'packages;',len(checks),'supported bands;',sum(c['records']for c in checks),'records twice from read-only relocated packages')
