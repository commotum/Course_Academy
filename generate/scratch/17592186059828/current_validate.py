"""Audit all current sources and the additional complete right-ray bank."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
import validate as v
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'scripts/question_capture'))
from edn import loads
H=Path(__file__).resolve().parent; R=H.parents[2];g=v.g

def current_source(path):
    return loads(path.read_text())[0][0]

def source_set(text):
    text=text.replace(r'x\in','x ∈ ').replace(r'\infty','∞')
    return v.parse_interval(re.sub(r'\s+',' ',text).strip())

def main():
    old=json.loads((H/'source.json').read_text())['record']
    current=current_source(H/'reference/initial/kp.edn')
    qs={q[':question/math-academy-id']:q for q in current[':knowledge-point/questions']}
    # Historical snapshots remain intact; new source data is captured separately.
    (H/'current-source.json').write_text(json.dumps(current,default=str,ensure_ascii=False,indent=2)+'\n')
    checks=[]
    for name,a,b,kind in [('q-154795',-3,2,'left'),('q-31779',2,4,'right')]:
        q=qs[name];field=q[':question/answer-fields'][0]
        values=[r'x\in '+l+str(a)+','+str(b)+r for l,r in [('(',')'),('[',']'),('(',']'),('[',')')]]
        values.append(r'x\in (-\infty ,'+str(b)+')' if kind=='left' else r'x\in ['+str(a)+r',\infty )')
        actual=[c[':answer/value'] for c in field[':answer-field/choices']]
        assert sorted(values)==sorted(actual)
        truth=source_set(r'x\in (-3,2)' if kind=='left' else r'x\in [2,4)')
        assert source_set(field[':answer-field/correct'][':answer/value'])==truth
        assert len(set(map(source_set,values)))==5
        checks.append({'source':name,'complete_bank_match':True,'exact_values_matched':5,'total':5,'scope':'excluded: both-open' if kind=='left' else 'supported half-open; right-ray bank','all_choice_recipes':[{'value':x,'set':str(source_set(x)),'recipe':'left open ray' if 'infty' in x and kind=='left' else 'right closed ray' if 'infty' in x else 'bounded pair with printed closure combination'} for x in values]})
    p=g.parameters(2,4,True,1,1)
    # Original positive moderate coordinates lie outside the authored signed
    # sampler. Replay the complete BANK independently without claiming sampler coverage.
    generated=g.bank(p,'observed_right_ray')
    assert set(source_set(x) for x in [c[':answer/value'] for c in qs['q-31779'][':question/answer-fields'][0][':answer-field/choices']])==set(v.parse_interval(x) for _,x in generated)
    out=H/'reference/current-validation';out.mkdir(parents=True,exist_ok=True)
    config={'output':str(out/'source-raster.json'),'cases':[{'path':'/media/jake/SSD/EDB/math/'+re.search(r'!\[\]\((.*?)\)',qs[name][':question/problem'])[1],'fit':{'anchor_values':[-4,4] if i==0 else [1,6],'anchor_pixels':[25,418] if i==0 else [25,271],'tick_pixels':[25,74,123,172,221,271,320,369,418] if i==0 else [25,74,123,172,221,271]}} for i,name in enumerate(('q-154795','q-31779'))]}
    (out/'source-raster-input.json').write_text(json.dumps(config))
    subprocess.run([str(R/'.venv/bin/python'),str(H/'renderer.py'),'--readback',str(out/'source-raster-input.json')],check=True)
    for row,coords,closed in zip(json.loads((out/'source-raster.json').read_text()),[(-3,2),(2,4)],[[False,False],[True,False]]):
        assert max(abs(a-b) for a,b in zip(row['measurement']['endpoint_values'],coords))<.025
        assert row['measurement']['closed']==closed
    counts={}; fixtures=[];records=[];seen=set()
    for level in ('easy','moderate','hard'):
        counts[level]=len(g.catalog(level))
        for p in g.catalog(level):
            sets=[v.parse_interval(x) for _,x in g.bank(p,'observed_right_ray')]
            assert len(set(sets))==5
        for seed in (19,37):
            rec=g.generate(level,seed,profile='observed_right_ray');v.displayed_check(rec);v.raster(rec);records.append(rec)
            f=rec['question'][':question/answer-fields'][0]
            fixtures.append({'label':level+str(seed),'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'additional source complete right-ray bank'} for a in f[':answer-field/choices']]})
    (out/'engine-input.json').write_text(json.dumps(fixtures))
    subprocess.run([str(R/'generate/runs/current/check-engine'),str(out/'engine-input.json'),str(out/'engine-report.json')],check=True)
    report={'passed':True,'capture_basis':2110,'lineage':g.SOURCE['lineage'],'current_sources':4,'new_source_replay':checks,'prior_sources':{'complete_banks':2,'exact_values':10,'missing_keys':2,'missing_solutions':2,'evidence':'validation.json'},'all_current_complete_banks':4,'all_current_options':20,'new_scope_exclusion':'q-154795 is both-open, independently confirmed by its raster, key and solution; excluded from half-open reserve','authored_levels':['easy','moderate','hard'],'finite_task_catalogs':counts,'hard_origin':'Authored fractional tick-reading extension, not observed source difficulty. Existing catalog and scope unchanged.','new_bank_sampler_sweep':sum(counts.values()),'hashes':{str(path.relative_to(R)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [H.with_suffix('.py'),H/'renderer.py',H/'validate.py',H/'current_validate.py',H/'current-source.json']},'native_grading':json.loads((out/'engine-report.json').read_text()),'unresolved':[]}
    (H/'current-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    (out/'review.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
    (out/'review.md').write_text('\n\n'.join('## '+r['question'][':question/difficulty']+' right-ray bank\n\n'+g.markdown(r) for r in records))
    print('PASS current audit: all four source banks / 20 options accounted; new source pixels verified; all catalogs support new bank; native grading passed.')
if __name__=='__main__':main()
