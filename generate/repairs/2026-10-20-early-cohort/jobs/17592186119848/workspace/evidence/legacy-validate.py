"""Replay all source banks and exhaust the bounded rank-mask catalog."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('rank_inspection',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def fingerprint(q):return g.fingerprint(q)
def rank(matrix):
    rows=[[Fraction(int(x)) for x in matrix.row(i)] for i in range(matrix.rows)];n=0
    for j in range(matrix.cols):
        pivot=next((i for i in range(n,len(rows)) if rows[i][j]),None)
        if pivot is None:continue
        rows[n],rows[pivot]=rows[pivot],rows[n];d=rows[n][j];rows[n]=[x/d for x in rows[n]]
        for i in range(n+1,len(rows)):
            c=rows[i][j];rows[i]=[a-c*b for a,b in zip(rows[i],rows[n])]
        n+=1
        if n==len(rows):break
    return n
def native(label,rec):
    checks=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            check={'field_index':i,'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each field-owned option via application learner grader'}
            check['submitted_answer_id']=a[':answer/id']
            checks.append(check)
    return {'label':label,'record':rec,'checks':checks}
def check(rec):
    q=rec['question'];meta=rec['generation'];sid=meta['bank_profile'];bank=g.matrices(q);r=g.target(q)
    ranks={k:rank(m) for k,m in bank.items()};matches=tuple(k for k in sorted(bank) if ranks[k]==r)
    assert rec['knowledge_point']['db_id']==g.KP_ID and q[':question/difficulty']==':question.difficulty/easy'
    assert matches==tuple(meta['parameters']['matches']) and ranks==meta['ranks']
    assert set(bank)==set(g.matrices(g.CASES[sid]))
    for label,m in bank.items():
        assert m.shape==g.matrices(g.CASES[sid])[label].shape
        if label not in g.eligible(sid):assert m==g.matrices(g.CASES[sid])[label]
    for f in q[':question/answer-fields']:
        answers=f[':answer-field/choices'];assert len({(a[':answer/type'],a[':answer/value']) for a in answers})==len(answers)
        correct=next(a for a in answers if a[':answer/id']==f[':answer-field/correct'][1])[':answer/value']
        if f[':answer-field/type']==':answer-field.type/checkbox':assert correct==('true' if f[':answer-field/key'] in matches else 'false')
        elif g.kind(sid)=='five-matrix-radio':assert tuple(g.parse_matrices(correct))==matches and len(matches)==1
        else:assert g.subset(correct)==matches
    sol=q[':question/worked-solution']
    # Independently read concrete rank assertions and final selected objects.
    for label,value in re.findall(r'\\text\{rank\}\(([A-E])\)=(\d+)',sol):assert ranks[label]==int(value)
    final=sol.split('Therefore,')[-1];assert set(re.findall(r'\$([A-E])(?:\.?)\$',final))==set(matches)
    if not matches:assert 'None' in final
    for label in g.eligible(sid):
        assert (r'\text{rank}('+label+')=') in sol or not meta['extension']
    assert fingerprint(q)==meta['mathematical_fingerprint']
    assert g.generate('easy',meta['seed'],sid,meta['parameters'])==rec
    return rec
def fidelity(old,rec):
    check(rec);q=rec['question']
    assert q[':question/problem']==g.normalize_prose(old[':question/problem'])
    assert q[':question/worked-solution']==g.normalize_prose(old[':question/worked-solution']).replace('coumns','columns')
    assert len(old[':question/answer-fields'])==len(q[':question/answer-fields'])
    for oldf,f in zip(old[':question/answer-fields'],q[':question/answer-fields']):
        convert=lambda a:(a[':answer/type'][':db/ident'],g.normalize_tex(a[':answer/value']) if a[':answer/type'][':db/ident']==':answer.type/math' else g.normalize_prose(a[':answer/value']))
        assert sorted(map(convert,oldf[':answer-field/choices']))==sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])
        correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        assert convert(oldf[':answer-field/correct'])==(correct[':answer/type'],correct[':answer/value'])
def main():
    inputs=[];replay=[];components=[];coverage={};review=[]
    for sid,old in sorted(g.CASES.items()):
        orig=g.generate('easy',0,sid,{'matches':list(g.original_matches(sid))});fidelity(old,orig)
        n=sum(len(f[':answer-field/choices']) for f in old[':question/answer-fields']);d=n-len(old[':question/answer-fields'])
        replay.append({'source':sid,'template':g.kind(sid),'profile':sid,'complete_banks':len(old[':question/answer-fields']),'matched_choices':n,'matched_distractors':d,'missing':[],'extra':[],'correct_designation':True})
        components.append({'source':sid,'db_id':old[':db/id'],'target_rank':g.target(old),'matrices':{k:{'shape':m.shape,'entries':list(m),'rank':rank(m),'eligible':k in g.eligible(sid)} for k,m in g.matrices(old).items()},'fields':[{'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'choices':[{'id':a[':answer/id'],'value':a[':answer/value'],'recipe':('source labeled matrix, changed via rank_adjust only when dimension-eligible' if a[':answer/type'][':db/ident']==':answer.type/math' else 'fixed source literal Boolean or subset of matrix labels'),'original_reproduced':True} for a in f[':answer-field/choices']]} for f in old[':question/answer-fields']]})
        for matches in g.domain(sid):
            rec=check(g.generate('easy',0,sid,{'matches':list(matches)}));inputs.append(native(sid+' '+str(matches),rec))
            alt=g.generate('easy',73,sid,{'matches':list(matches)});assert alt['question']==rec['question']
            if matches!=g.original_matches(sid):
                assert fingerprint(rec['question'])!=fingerprint(old)
                review.append('## '+sid+' '+str(matches)+'\n\nOriginal\n\n'+g.markdown(orig)+'\n\nPivot variant\n\n'+g.markdown(rec))
                for key in (':question/worked-solution',':question/answer-fields'):
                    stale=copy.deepcopy(rec);stale['question'][key]=orig['question'][key]
                    try:check(stale)
                    except (AssertionError,StopIteration):pass
                    else:raise AssertionError('Stale component accepted: '+key)
        coverage[sid]={'fixed_target_rank':g.target(old),'eligible_matrix_labels':g.eligible(sid),'allowed_match_subsets':g.domain(sid),'covered_match_subsets':g.domain(sid),'uncovered':[],'source_matches':g.original_matches(sid),'fixed_shapes':True,'dimension_excluded_matrices_unchanged':True}
    records=g.catalog();sourcefps={fingerprint(q) for q in g.CASES.values()};assert len(records)==len({fingerprint(r['question']) for r in records})
    for level in ('moderate','hard','unclassified'):
        try:g.batch(level,1)
        except ValueError:pass
        else:raise AssertionError('Unsupported level admitted')
    try:g.batch('easy',len(records)+1)
    except ValueError:pass
    else:raise AssertionError('Finite limit ignored')
    save('source-replay.json',{'passed':True,'matched_questions':len(replay),'total_questions':len(g.CASES),'matched_banks':sum(x['complete_banks'] for x in replay),'matched_distractors':sum(x['matched_distractors'] for x in replay),'profiles':replay,'source_corrections':[{'source':'q-34824','correction':'coumns -> columns; spelling only; source unchanged'}],'excluded_incomplete_sources':['q-34807','q-35270']})
    save('source-components.json',components);save('slot-coverage.json',coverage);save('native-input.json',inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    report=json.loads((HERE/'native-grading.json').read_text());assert report['documented_unresolved_checks']==0
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n');save('previews.json',g.batch('easy',5,119848))
    caps={'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'finite_distinct_tasks':len(records),'finite_new_variants':len({fingerprint(r['question']) for r in records}-sourcefps),'exceptions':[{'levels':['moderate','hard'],'scope':'current source-backed bounded package','reason':'All ten complete source questions are easy. No moderate/hard instructional backbone is evidenced. This package retains dimension exclusion and immediate pivot inspection; more demanding row reduction would change the assessed method. New evidence reopens classification.','shortage_each':5,'filled':False},{'scope':'easy finite catalog','reason':'Only complete observed choice profiles and explicitly enumerated pivot-rank edits are supported. Numerical rescaling, option order, seed and relabeling never add capacity. This is a package limit, not global mathematical impossibility.','limit':len(records)}]};save('capabilities.json',caps)
    save('validation.json',{'passed':True,'source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'exhaustive_instances':len(inputs),'distinct_catalog':len(records),'new_variants':caps['finite_new_variants'],'fidelity':'10/10 source question replays; all 14 complete field banks and all correct designations; normalized presentation with one spelling correction','correctness':'independent exact Fraction Gaussian elimination from rendered matrices, parsed rank and final label assertions, original dimensions and excluded matrices preserved, stale solution/key negative controls','grading':{'accepted':report['accepted_checks'],'rejected':report['rejected_checks'],'unresolved':0},'slot_coverage':'every declared match subset for all profiles; fixed requested rank and shapes; pivot-only edits; no numeric or label shuffle capacity','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',ROOT/'generate/runs/current/check-engine')}})
    print(json.dumps({'passed':True,'catalog':len(records),'new_variants':caps['finite_new_variants'],'grading':[report['accepted_checks'],report['rejected_checks']]}))
if __name__=='__main__':main()
