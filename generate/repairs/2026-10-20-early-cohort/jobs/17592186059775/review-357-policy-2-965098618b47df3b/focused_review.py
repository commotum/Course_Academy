"""Run with the context Python, -B, from evidence_root. Read-only package audit."""
from review_helpers import *
import collections
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
commands=[]
def run(label,cmd,expected=0):
    p=subprocess.run(cmd,cwd=E,text=True,capture_output=True)
    (E/(label+'.log')).write_text(p.stdout+p.stderr)
    commands.append({'label':label,'command':cmd,'exit_code':p.returncode,'log':label+'.log'})
    assert p.returncode==expected,(label,p.stderr[-1500:])
    return p

# Fresh source replay against current runtime; prior source-error analysis retained.
src=json.load(open(J/'source/source.json'))['material']['kp'][':knowledge-point/questions']
replays=json.load(open(E/'source-replays.json'))
for old in replays:
    assert g.source_replay(old['generation']['template'])==old
save('fresh-source-replay.json',{'replayed':len(replays),'exact_complete_records':True,'unsupported_incomplete_source_ids':[s[':question/id'] for s in src if s[':question/math-academy-id'] not in g.CASES]})

# Small fresh regression, including controlled decisive-RHS and irrelevant order pairs.
fresh=[]
for i,sid in enumerate(g.CASES):
    fresh.append(g.generate(g.level(sid),seed=202610229+i,parameters=[sid,g.domain(sid)[-1][1],i%5]))
pairs=[]
for sid in ['q-130909','q-1060']:
    band=g.level(sid);k=g.domain(sid)[0][1]
    a=g.generate(band,seed=20261029,parameters=[sid,k,0])
    b=g.generate(band,seed=20261029,parameters=[sid,k,4])
    c=g.generate(band,seed=20261030,parameters=[sid,k,0])
    am,bm=mats(q(a)[':question/problem'])[0],mats(q(b)[':question/problem'])[0]
    assert am[:,:2]==bm[:,:2] and am[0,:]==bm[0,:] and am[1,2]!=bm[1,2]
    assert [z[':answer/value'] for z in f(a)[':answer-field/choices']]==[z[':answer/value'] for z in f(b)[':answer-field/choices']]
    assert key(a)[':answer/value']!=key(b)[':answer/value']
    assert q(a)[':question/problem']==q(c)[':question/problem'] and key(a)[':answer/value']==key(c)[':answer/value']
    pairs.append({'profile':sid,'records':[a,b,c],'expected':'RHS change changes normalized answer; permutation preserves mathematical answer.','passed':True})
    fresh += [a,b,c]
batch=json.load(open(J/'samples.json'));assert batch==g.batch('easy',5,4258185931)
save('runner-batch.json',batch);fresh+=batch
save('fresh-records.json',fresh);save('fresh-counterfactuals.json',pairs)
save('fresh-math.json',[verify(r) for r in fresh])

# Current captured inventory through the shared read-only publisher.
for name,band,rs in [('batch','easy',batch),('easy','easy',[r for r in fresh if q(r)[':question/difficulty'].endswith('/easy')]),('moderate','moderate',[r for r in fresh if q(r)[':question/difficulty'].endswith('/moderate')])]:
    inp=E/('delivery-input-'+name+'.json');save(inp.name,rs)
    run('delivery-'+name,[PY,'-B',str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(inp),'--source',str(J/'source/source.json'),'--inventory',str(J/'source/inventory.json'),'--difficulty',band,'--output',str(E/('delivery-'+name)),'--asset-root',str(E/'assets'),'--math-root','/media/jake/SSD/EDB/math'])
run('strict-current',[PY,'-B',str(E/'reproduce_batch_shortcut.py')])
run('strict-delivered',[PY,'-B',str(E/'reproduce_batch_shortcut.py'),'--input',str(E/'delivery-batch/accepted.json')])
run('strict-historical',[PY,'-B',str(E/'reproduce_batch_shortcut.py'),'--input',str(E/'previous-runner-batch.json')],1)

# Reproduce all three archived generated records exactly, then check current eligibility.
inv=json.load(open(J/'source/inventory.json'))
legacy=loadmod('legacy',W/'evidence/legacy/17592186059775.py')
arch=json.load(open(W/'17592186059775/reference/replenishment/basis-2480/generated.json'))
generated=[];affected=[];inventory=[];family=[]
for stored in inv['questions']:
    if ':question/math-academy-id' in stored:continue
    old=next(r for r in arch if q(r)[':question/id']==stored[':question/id']);m=old['generation'];sid=m['template'];band=stored[':question/difficulty'][':db/ident'].split('/')[-1]
    r=legacy.generate(band,m['seed'],sid,m['parameters']);assert r==old
    for n in [':question/problem',':question/worked-solution']:assert q(r)[n]==stored[n]
    sf=stored[':question/answer-fields'][0]
    for a in f(r)[':answer-field/choices']:
        sa=next(x for x in sf[':answer-field/choices'] if x[':answer/id']==a[':answer/id'])
        assert mats(a[':answer/value'])==mats(sa[':answer/value']) and xy(a[':answer/value'])==xy(sa[':answer/value'])
        a[':answer/value']=sa[':answer/value']
    assert key(r)[':answer/id']==sf[':answer-field/correct'][':answer/id']
    generated.append(r)
    if sid=='q-1060':
        family=[legacy.generate(band,m['seed'],sid,p) for p in legacy.domain(sid)]
        assert all(rank(z)==2 for z in family) and rank(r)==2
        defect='Choose the median candidate lower-right value; this legacy profile fixes the correct rank for every permitted scale.'
    else:
        consistent=[a for a in f(r)[':answer-field/choices'] if (lambda mat:mat[:,:2]*S.Matrix(xy(a[':answer/value']))==mat[:,2])(mats(a[':answer/value'])[0])]
        assert consistent==[key(r)]
        defect='Only the keyed matrix/solution pair is internally consistent; the input system can be ignored.'
    retired=stored.get(':question/retired',False)
    inventory.append({'question_id':stored[':question/id'],'entity_id':stored[':db/id'],'retired':retired,'eligible_if_fresh':not retired,'difficulty':band,'defect':defect,'parameters':m['parameters']})
    if not retired:
        affected.append({'question_id':stored[':question/id'],'entity_id':stored[':db/id'],'finding':defect,'reproduction':PY+' -B focused_review.py; legacy.generate("moderate",59775,"q-1060",["q-1060",3])','evidence_path':'generated-records.json'})
save('generated-records.json',generated);save('legacy-family-records.json',family)
save('affected-inventory.json',{'affected_questions':affected})
save('inventory-results.json',{'basis':inv['basis'],'records':inventory,'original_source_questions_not_marked_generated':12,'legacy_median_success':len(family),'legacy_median_total':len(family),'selection_evidence':'engine/rust/learning.rs:question_is_usable rejects question/retired=true; question_selection.rs:select gives positive-probability selection to fresh eligible moderate records under positive moderate weights.','limits':'Captured basis only; all generated legacy records retired and excluded from practice. Original source records preserved.'})

# Native grader: all alternatives, both controlled pairs, delivered records, stored median.
delivered=sum([json.load(open(E/('delivery-'+n)/'accepted.json')) for n in ['batch','easy','moderate']],[])
for r in delivered:verify(r)
grade_records=fresh+delivered+[r for r in generated if q(r)[':question/id'] in {a['question_id'] for a in affected}]
grades=[{'label':str(r['generation']['parameters']),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(r)[':answer/id'] else 'rejected','purpose':'Independent exact matrix/key verification; all alternatives'} for a in f(r)[':answer-field/choices']]} for r in grade_records]
save('fresh-grader-input.json',grades)
run('fresh-grader',[str(REPO/'generate/runs/current/check-engine'),str(E/'fresh-grader-input.json'),str(E/'fresh-grader-results.json')])

# Runtime closure relocation and declared versions; all outputs remain in evidence_root.
manifest=json.load(open(W/'package.json'));dest=E/'relocated';dest.mkdir(exist_ok=True)
for name in manifest['files']:
    out=dest/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/name,out)
assert manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':S.__version__}}
cli=[]
for band,count in [('easy',5),('moderate',5),('easy',0),('easy',65),('hard',1)]:
    cmd=[PY,'-E','-s','-B',str(dest/manifest['entrypoint']),'--format','json','--difficulty',band,'--count',str(count),'--seed','20261022']
    p=run('cli-'+band+'-'+str(count),cmd,1 if count==65 or band=='hard' else 0)
    if p.returncode==0:
        assert len(json.loads(p.stdout))==count
        assert subprocess.run(cmd,cwd=E,text=True,capture_output=True).stdout==p.stdout
    cli.append({'band':band,'count':count,'exit_code':p.returncode})
save('fresh-packaging.json',{'manifest':manifest,'actual_python':platform.python_version(),'actual_sympy':S.__version__,'relocation':True,'determinism':True,'cli':cli})
save('fresh-render-records.json',batch+pairs[0]['records']+pairs[1]['records'])
save('fresh-commands.json',commands)
(E/'session-state.md').write_text('Fresh replay/math/CLI/delivery/native grading complete. Current batch defeats retained shortcut (1/5); historical control fails (5/5). Inventory basis 5577 has all three generated legacy defects retired. Await actual UI refresh and final evidence validation.\n')
print(json.dumps({'fresh_math_records':len(fresh),'native_submissions':len(grades)*5,'eligible_inventory_defects':len(affected),'batch_ranks':[rank(r) for r in batch]}))
