"""Reproduce all evidence. Use the job's pinned Python; no database operations."""
import argparse,copy,json,os,pathlib,shutil,subprocess,sys,tempfile
P=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
E=P/'evidence';E.mkdir(exist_ok=True)
commands=[]
def run(args,log):
    command=[str(x) for x in args];commands.append(command)
    r=subprocess.run(command,cwd=P,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (E/log).write_text(r.stdout)
    if r.returncode:raise RuntimeError(log+': '+r.stdout[-1800:])
def save(name,obj):(E/name).write_text(json.dumps(obj,indent=2)+'\n')
parser=argparse.ArgumentParser();parser.add_argument('--skip-generation',action='store_true');args=parser.parse_args()
if not args.skip_generation:run([sys.executable,'validate.py'],'validation.log')
run([REPO/'generate/runs/current/check-engine',E/'grader-input.json',E/'grading.json'],'grading.log')
run([sys.executable,'additional_checks.py'],'additional-checks.log')
run([sys.executable,'audit_variation.py',E/'test-records.json',E/'variation-before.json'],'variation-before.log')
records=json.loads((E/'test-records.json').read_text());accepted=[];deliveries={}
for band in ('easy','moderate','hard'):
    path=E/(band+'-records.json');path.write_text(json.dumps([r for r in records if r['question'][':question/difficulty'].endswith('/'+band)]))
    out=E/('delivery-'+band)
    run([sys.executable,REPO/'generate/pipeline/check_delivery.py','--input',path,'--source',P.parent/'source/source.json','--inventory',P.parent/'source/inventory.json','--difficulty',band,'--output',out,'--asset-root',E,'--math-root','/media/jake/SSD/EDB/math'],'delivery-'+band+'.log')
    accepted.extend(json.loads((out/'accepted.json').read_text()));deliveries[band]=json.loads((out/'delivery.json').read_text())
save('accepted.json',accepted)
run([sys.executable,'audit_variation.py',E/'accepted.json',E/'variation-after.json'],'variation-after.log')
# The real filter reassigns field-owned stable answer IDs. Check the delivered IDs
# directly; metadata IDs are intentionally not used for post-filter grading.
post=[]
for i,r in enumerate(accepted):
    f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
    correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key)
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'actual post-delivery choice ID'} for a in f[':answer-field/choices']]
    else:
        checks=[{'submitted':correct,'expected':'accepted','purpose':'delivered key'}, {'submitted':'2*('+correct+')/2','expected':'accepted','purpose':'equivalent delivered response'}, {'submitted':'('+correct+')+1','expected':'rejected','purpose':'incorrect delivered response'}]
    post.append({'label':'delivered '+str(i),'record':r,'checks':checks})
save('post-delivery-grader-input.json',post)
run([REPO/'generate/runs/current/check-engine',E/'post-delivery-grader-input.json',E/'post-delivery-grading.json'],'post-delivery-grading.log')
run([sys.executable,REPO/'generate/pipeline/check_delivery.py','--input',E/'samples.json','--source',P.parent/'source/source.json','--inventory',P.parent/'source/inventory.json','--difficulty','easy','--output',E/'delivery-batch','--asset-root',E,'--math-root','/media/jake/SSD/EDB/math'],'delivery-batch.log')
# Public entry point after relocation, with only declared runtime files available.
manifest=json.loads((P/'package.json').read_text())
with tempfile.TemporaryDirectory(prefix='course-academy-relocation-') as temp:
    temp=pathlib.Path(temp)
    for file in manifest['files']:
        target=temp/file;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/file,target)
    env={**os.environ,'PYTHONPATH':'','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(temp/'outputs')}
    cmd=[sys.executable,str(temp/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','18','--format','json']
    result=subprocess.run(cmd,cwd=temp,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,check=True)
    assert json.loads(result.stdout)==json.loads((E/'samples.json').read_text())
    save('relocation.json',{'passed':True,'copied_files':manifest['files'],'count':5,'seed':18,'undeclared_runtime_files':False,'command':cmd,'stderr':result.stderr,'generated_assets':[]})
run(['python3',REPO/'generate/pipeline/render_preview.py','--input',E/'render-records.json','--output',E/'render','--limit','12','--asset-root',E,'--math-root','/media/jake/SSD/EDB/math'],'render.log')
save('commands.json',{'complete_reproduction':[sys.executable,'run_checks.py'],'commands':commands})
print(json.dumps({'delivery':{k:{x:d[x] for x in ('input_count','accepted_count','duplicate_count')} for k,d in deliveries.items()},'relocation':True,'rendered':12}))
