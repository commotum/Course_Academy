"""Full mathematical source bank replay and actual radio grading."""
import importlib.util,json,hashlib,sys,subprocess,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from parser import scalar,prompt,same,X
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
native=[]
def validate(rec,collect=True):
    q=rec['question'];assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    level=q[':question/difficulty'].split('/')[-1];assert level in g.SUPPORTED_LEVELS
    c=g.case(rec['generation']['template']);assert level==c[1]
    assert len(q[':question/answer-fields'])==1
    f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];assert len(vals)==5
    assert all(not same(v,w)for i,v in enumerate(vals)for w in vals[i+1:])
    integrand=prompt(q[':question/problem']);expected=g.data(rec['generation']['parameters'])[6];assert same(integrand,expected)
    cid=f[':answer-field/correct'][1];correct=next(scalar(a[':answer/value'])for a in f[':answer-field/choices']if a[':answer/id']==cid)
    assert same(g.sp.diff(correct,X),integrand)
    assert sum(same(g.sp.diff(v,X),integrand)for v in vals)==1
    assert g.fingerprint(q)==rec['generation']['mathematical_fingerprint']
    # Independently parse displayed substitution, derivative and all final rows.
    blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==4
    u=scalar(blocks[0].split('=',1)[1]);_,_,_,_,n,expected_u,_,ratio,_=g.data(rec['generation']['parameters']);assert same(u,expected_u)
    du=scalar(blocks[1].split('=',1)[1].split(r'\quad')[0]);assert same(du,g.sp.diff(u,X))
    rr=scalar(blocks[1].split(r'\Longrightarrow\quad ')[1].split(r'\,\text{d}u')[0]);assert same(rr,ratio)
    rows=blocks[3].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==3
    for row in rows:
        rhs=scalar(row.split('&=',1)[1]).subs(g.sp.Symbol('u',positive=True),u)
        assert same(g.sp.diff(rhs,X),integrand),rhs
    for t in (q[':question/problem'],q[':question/worked-solution']):
        assert t.count('$')%2==0 and t.count('{')==t.count('}')
    checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==cid else 'rejected','purpose':'every owned radio option'}for a in f[':answer-field/choices']]
    if collect:native.append({'label':q[':question/id'],'record':rec,'checks':checks})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build_engine():
    deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps';harness=ROOT/'generate/runs/current/check-engine.rs'
    libraries={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns)for name in ('course_academy_engine','serde_json')}
    cmd=['rustc','--edition=2024','-O',str(harness)]
    for name,p in libraries.items():cmd+=['--extern',name+'='+str(p)]
    cmd+=['-L','dependency='+str(edb),'-L','dependency='+str(deps),'-o',str(HERE/'check-current-engine')];subprocess.run(cmd,check=True)
    (HERE/'engine-build.json').write_text(json.dumps({'harness_sha256':sha(harness),'libraries':{str(p):sha(p)for p in libraries.values()},'executable_sha256':sha(HERE/'check-current-engine')},indent=2))
def main():
    replay=[];review=[];distinct=set()
    for c in g.CASES:
        s=g.SOURCES[c[0]];r=g.generate(c[1],19,c[0],g.defaults(c));validate(r)
        assert same(prompt(s[':question/problem']),prompt(r['question'][':question/problem']))
        original=[scalar(a[':answer/value'])for a in s[':question/answer-fields'][0][':answer-field/choices']]
        generated=[scalar(a[':answer/value'])for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
        for v in original:
            matches=[i for i,w in enumerate(generated)if same(v,w)];assert len(matches)==1,(c[0],v,generated);generated.pop(matches[0])
        assert not generated
        sf=s[':question/answer-fields'][0]
        if ':answer-field/correct'in sf:assert same(g.sp.diff(scalar(sf[':answer-field/correct'][':answer/value']),X),prompt(s[':question/problem']))
        replay.append({'source':c[0],'complete_bank':True,'matched_options':5,'matched_distractors':4,'correct_designation':'matched'if ':answer-field/correct'in sf else 'missing source designation; independently derived repair'})
        variant=g.generate(c[1],91,c[0]);validate(variant);review.append({'source':s,'replay':r,'variant':variant})
        for seed in range(12):
            rec=g.generate(c[1],seed,c[0]);validate(rec);distinct.add(rec['generation']['mathematical_fingerprint'])
            rr=g.generate(c[1],seed+777,c[0],rec['generation']['parameters']);assert rr['question'][':question/id']==rec['question'][':question/id']
        for b in (1,20):
            p=g.defaults(c);p['b']=b*(-1 if c[5]<0 else 1)
            try:validate(g.generate(c[1],0,c[0],p))
            except ValueError as e:assert str(e)=='whole-bank collision'
    try:g.generate('hard')
    except ValueError:pass
    else:raise AssertionError('unsupported hard accepted')
    build_engine();(HERE/'native-input.json').write_text(json.dumps(native,indent=2));subprocess.run([str(HERE/'check-current-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    report=json.loads((HERE/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
    (HERE/'source-replay.json').write_text(json.dumps(replay,indent=2));(HERE/'review.json').write_text(json.dumps(review,indent=2))
    md=['# Source, replay and variant review','All complete banks match mathematically. Prompt TeX and final solution layouts are standardized; the substitution sequence and shared instructional prose are preserved. The incomplete unrated source is preserved and repaired only in generated instances.']
    for x in review:
        md+=['## '+x['source'][':question/math-academy-id']]
        for label,q in [('Source',x['source']),('Replay',x['replay']['question']),('Variant',x['variant']['question'])]:
            md+=[label,q[':question/problem'],str([a[':answer/value']for a in q[':question/answer-fields'][0][':answer-field/choices']]),q.get(':question/worked-solution','Missing source solution')]
    (HERE/'review.md').write_text('\n\n'.join(md))
    files=[HERE.with_suffix('.py'),HERE/'parser.py',HERE/'validate.py',HERE/'source.json',HERE/'check-current-engine']
    result={'passed':True,'source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'complete_banks_matched':10,'source_options_matched':50,'source_distractors_matched':40,'correct_designations_matched':9,'source_repair':'q-12494 lacks rating, correct ref and solution; easy workload inferred from complete bank and same small-integer family; originals unchanged','supported_levels':['easy','moderate'],'unsupported_levels':['hard'],'distinct_sample_tasks':len(distinct),'native':{k:report[k]for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):sha(p)for p in files}}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
