"""Source replay and independent visible-record witnesses for the finite family."""
import copy
from fractions import Fraction
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('rank_generator',ROOT/'17592186119848.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
E=ROOT/'evidence'
REPO=Path('/home/jake/Developer/Course_Academy')
JOB=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186119848')
PATTERN=re.compile(r'([A-E])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)

def save(name,value):
    (E/name).write_text(json.dumps(value,indent=2,default=str)+'\n')

def visible_bank(q):
    texts=[q[':question/problem']]
    for f in q[':question/answer-fields']:
        texts.append(f[':answer-field/key'])
        texts.extend(a[':answer/value'] for a in f[':answer-field/choices'])
    bank={}
    for text in texts:
        for label,body in PATTERN.findall(text):
            rows=[[Fraction(x.strip()) for x in row.split('&')] for row in body.split(r'\\')]
            assert rows and len(set(map(len,rows)))==1
            if label in bank: assert bank[label]==rows
            bank[label]=rows
    return bank

def rank(rows):
    rows=copy.deepcopy(rows); n=0
    for j in range(len(rows[0])):
        pivot=next((i for i in range(n,len(rows)) if rows[i][j]),None)
        if pivot is None: continue
        rows[n],rows[pivot]=rows[pivot],rows[n]
        d=rows[n][j];rows[n]=[x/d for x in rows[n]]
        for i in range(n+1,len(rows)):
            c=rows[i][j];rows[i]=[a-c*b for a,b in zip(rows[i],rows[n])]
        n+=1
        if n==len(rows):break
    return n

def labels(text): return set(re.findall(r'\$([A-E])(?:\.)?\$',text))
def answer(f):return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])[':answer/value']

def inspect(rec):
    q=rec['question'];bank=visible_bank(q)
    target=int(re.search(r'rank of \$(\d+)',q[':question/problem'])[1])
    ranks={k:rank(m) for k,m in bank.items()};truth={k for k,v in ranks.items() if v==target}
    assert bank and all(re.fullmatch(r'[A-E]',k) for k in bank)
    checks=[];selected=set();positions=[]
    for i,f in enumerate(q[':question/answer-fields']):
        options=f[':answer-field/choices'];values=[a[':answer/value'] for a in options]
        assert len(set(values))==len(values)
        if f[':answer-field/type']==':answer-field.type/checkbox':
            fieldlabels=set(PATTERN.findall(f[':answer-field/key'])[j][0] for j in range(len(PATTERN.findall(f[':answer-field/key']))))
            expected=bool(fieldlabels & truth) if fieldlabels else not truth
            assert fieldlabels or f[':answer-field/key']=='None of the above'
            assert answer(f)==str(expected).lower()
            if expected:selected |= fieldlabels or {'None'};positions.append(i)
        else:
            for a in options:
                labs=set(k for k,_ in PATTERN.findall(a[':answer/value'])) or labels(a[':answer/value'])
                expected=labs==truth
                assert (a[':answer/id']==f[':answer-field/correct'][1])==expected
            selected=truth;positions=[next(j for j,a in enumerate(options) if a[':answer/id']==f[':answer-field/correct'][1])]
        for a in options:
            checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independent displayed matrix rank and full option bank'})
    if any(f[':answer-field/type']==':answer-field.type/checkbox' for f in q[':question/answer-fields']):assert selected
    solution=q[':question/worked-solution']
    final=solution.split('Therefore,')[-1]
    assert labels(final)==truth, (truth,final)
    if not truth: assert 'None' in final
    for lab,n in re.findall(r'\\(?:text|textrm)\{rank\}\(([A-E])\)=(\d+)',solution):assert ranks[lab]==int(n)
    # Dimension explanations are checked from visible rows/columns, not metadata.
    for lab,n,unit in re.findall(r'\$([A-E])\$ since it has only \$(\d+)\$ (rows|columns)',solution):
        assert (len(bank[lab]) if unit=='rows' else len(bank[lab][0]))==int(n)
    return {'truth':sorted(truth),'ranks':ranks,'target':target,'selected':sorted(selected),'positions':positions,'field_count':len(q[':question/answer-fields'])},checks

def fidelity(old,rec):
    q=rec['question']
    if PATTERN.search(old[':question/problem']):
        # Source's one overwide display is replaced with independently wrapping
        # matrices. Prose and every matrix entry are checked separately.
        assert q[':question/problem'].split('\n\n')[0]==g.normalize_prose(old[':question/problem']).split('\n\n')[0]
        assert 'matrix-operands' in q[':question/problem']
    else:
        assert q[':question/problem']==g.normalize_prose(old[':question/problem'])
    assert q[':question/worked-solution']==g.normalize_prose(old[':question/worked-solution']).replace('coumns','columns')
    assert visible_bank(q)==visible_bank(old)
    assert len(q[':question/answer-fields'])==len(old[':question/answer-fields'])
    matched=0
    for oldf,f in zip(old[':question/answer-fields'],q[':question/answer-fields']):
        assert g.normalize_prose(oldf[':answer-field/key'])==f[':answer-field/key']
        def convert(a):
            typ=a[':answer/type'];typ=typ[':db/ident'] if isinstance(typ,dict) else typ
            return typ,g.normalize_tex(a[':answer/value']) if typ==':answer.type/math' else g.normalize_prose(a[':answer/value'])
        assert sorted(map(convert,oldf[':answer-field/choices']))==sorted(map(convert,f[':answer-field/choices']))
        assert convert(oldf[':answer-field/correct'])[1]==answer(f)
        matched+=len(f[':answer-field/choices'])
    return matched

def analyze(records):
    groups={}
    for rec in records:
        witness,_=inspect(rec);sid=rec['generation']['bank_profile']
        bank=visible_bank(rec['question'])
        excluded=','.join(k for k,m in sorted(bank.items()) if min(len(m),len(m[0]))<witness['target'])
        key=sid+' / fields='+str(witness['field_count'])+' / excluded='+excluded+' / bank='+rec['generation'].get('choice_profile',sid)
        groups.setdefault(key,[]).append(witness)
    report={}
    for key,rows in groups.items():
        sets=[set(x['selected']) for x in rows]
        # Each displayed-label answer, full subset, and exact correct-position
        # predictor is evaluated within a recognizable source bank/layout.
        outcomes={tuple(x['selected']) for x in rows};pos={tuple(x['positions']) for x in rows}
        constant_members=sorted(set.intersection(*sets))
        assert len(outcomes)>1 and not constant_members and len(pos)>1,(key,outcomes,pos,constant_members)
        report[key]={'instances':len(rows),'selected_subsets':sorted(outcomes),'correct_positions':sorted(pos),'correct_counts':sorted({len(s) for s in sets}),'always_selected_labels':constant_members,'best_constant_answer_successes':max(sum(tuple(x['selected'])==out for x in rows) for out in outcomes),'attempts':len(rows),'baseline':'modal complete response per source bank and visible field count; no constant complete response reaches 100%'}
    return report

def main():
    native=[];replays=[];choice_count=0
    for sid,old in sorted(g.CASES.items()):
        rec=g.generate('easy',0,sid,{'matches':list(g.original_matches(sid))},source_replay=True)
        choice_count+=fidelity(old,rec);w,c=inspect(rec)
        native.append({'label':'source replay '+sid,'record':rec,'checks':c});replays.append(rec)
    records=g.catalog();coverage={};counterfactuals=[]
    for rec in records:
        w,c=inspect(rec);meta=rec['generation'];sid=meta['bank_profile']
        assert g.generate('easy',meta['seed'],sid,meta['parameters'])==rec
        alt=g.generate('easy',73,sid,meta['parameters']);assert alt['question']==rec['question']
        assert w['truth']==meta['parameters']['matches'] and w['ranks']==meta['ranks']
        native.append({'label':sid+' '+json.dumps(meta['parameters']),'record':rec,'checks':c})
        coverage.setdefault(sid,[]).append({'assignment':meta['parameters']['assignment'],'qualifying':w['truth']})
    for sid in sorted(g.CASES):
        for assignment in g.assignments(sid):
            subset=[r for r in records if r['generation']['bank_profile']==sid and r['generation']['parameters']['assignment']==list(assignment)]
            assert len(subset)==len(g.domain(sid,assignment))
            if len(subset)<2:continue
            a,b=subset[:2];aw,_=inspect(a);bw,_=inspect(b)
            assert aw['truth']!=bw['truth']
            ab=visible_bank(a['question']);bb=visible_bank(b['question'])
            excluded=[k for k,m in ab.items() if min(len(m),len(m[0]))<aw['target']]
            assert all(ab[k]==bb[k] for k in excluded)
            assert a['question'][':question/worked-solution']!=b['question'][':question/worked-solution']
            # Stale key and solution negative controls must fail an independent read.
            for part in (':question/answer-fields',':question/worked-solution'):
                bad=copy.deepcopy(b);bad['question'][part]=a['question'][part]
                try:inspect(bad)
                except (AssertionError,StopIteration):pass
                else:raise AssertionError('stale component accepted '+sid+' '+part)
            counterfactuals.append({'profile':sid,'assignment':list(assignment),'before_question':a['question'][':question/id'],'after_question':b['question'][':question/id'],'before':aw['truth'],'after':bw['truth'],'unchanged_excluded_matrices':excluded,'stale_solution_and_key_rejected':True})
    # Irrelevant numeric scaling must preserve the independently derived response.
    scaling=[]
    for sid in ('q-139965','q-34824','q-79568','q-35283'):
        rec=next(r for r in records if r['generation']['bank_profile']==sid)
        p=dict(rec['generation']['parameters'],scale=1)
        alt=g.generate('easy',0,sid,p)
        rw,_=inspect(rec);aw,c=inspect(alt)
        assert rw['truth']==aw['truth'] and rw['ranks']==aw['ranks']
        assert visible_bank(rec['question'])!=visible_bank(alt['question'])
        assert rec['question'][':question/id']!=alt['question'][':question/id'], 'Different visible matrices share an identity'
        native.append({'label':'irrelevant scale '+sid,'record':alt,'checks':c})
        scaling.append({'profile':sid,'scale_before':1,'scale_after':2,'response_preserved':True,'independent_ranks_preserved':True})
    for level in ('moderate','hard','unclassified'):
        try:g.batch(level,1)
        except ValueError:pass
        else:raise AssertionError('unsupported difficulty admitted')
    capacity=len({r['generation']['mathematical_fingerprint'] for r in records})
    try:g.batch('easy',capacity+1)
    except ValueError:pass
    else:raise AssertionError('semantic capacity limit ignored')
    assert len(g.batch('easy',capacity,7))==capacity
    before=analyze(records)
    save('catalog.json',records);save('source-replay-records.json',replays);save('grader-input.json',native)
    result=subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'grader-input.json'),str(E/'grading.json')],capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr
    grading=json.loads((E/'grading.json').read_text());assert grading['documented_unresolved_checks']==0
    save('source-replay.json',{'passed':True,'questions':len(replays),'complete_banks':sum(len(x['question'][':question/answer-fields']) for x in replays),'choices':choice_count,'excluded_incomplete':['q-34807','q-35270'],'normal_sampling_extension':'q-79568 adds source-family None option; exact replay retains its three fields'})
    save('counterfactuals.json',counterfactuals)
    save('scale-invariance.json',scaling)
    save('coverage.json',{'per_profile':coverage,'catalog_presentations':len(records),'semantic_structures':len({r['generation']['mathematical_fingerprint'] for r in records}),'role_permutations_count_as_extra_semantic_capacity':False})
    save('pedagogical-variation-before.json',before)
    # Native grading checks counterfactuals above in the same batch, all choices.
    save('validation.json',{'passed':True,'source_questions':len(replays),'generated_presentations':len(records),'counterfactual_pairs':len(counterfactuals),'accepted_grades':grading['accepted_checks'],'rejected_grades':grading['rejected_checks'],'unresolved':0,'commands':['python checks/check_runtime.py','python checks/validate_content.py'],'independent_witness':'exact Fraction elimination on visible prompt, choice and checkbox-label matrices; independently decoded answer subsets and solution references'})
    print(json.dumps(json.loads((E/'validation.json').read_text())))

if __name__=='__main__':main()
