#!/usr/bin/env python3
"""Independent display, source, scope, identity and native-grader checks."""
import copy,hashlib,importlib.util,json,random,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('square',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SOURCE=json.loads((HERE/'source.json').read_text());CASES=json.loads((HERE/'source-cases.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}

def scalar(text):
    # Independent from generator's parser: actual cell syntax only.
    m=re.fullmatch(r'\\sqrt\{(\d+)\}',text.strip())
    return sp.sqrt(int(m[1])) if m else sp.Rational(text.strip())
def display(text):
    m=re.search(r'([a-z])\}?_\{(\d)(\d)\}',text);assert m,'Missing requested entry'
    name,i,j=m.groups();i,j=int(i),int(j)
    mat=re.search(r'\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\1\}',text,re.S);assert mat,'Missing displayed matrix'
    rows=[[x.strip() for x in row.split('&')] for row in mat.group(2).split('\\\\')]
    assert len(rows)>=2 and all(len(row)==len(rows) for row in rows),'Not square'
    for row in rows:
        for cell in row:scalar(cell)
    assert re.search(r'\$'+name.upper()+r'\$',text),'Matrix name mismatch'
    value=rows[i-1][j-1] if i<=len(rows) and j<=len(rows) else 'No such entry'
    return name,i,j,rows,value

def formatting(text):
    assert not any(ord(c)<32 and c not in '\n\t\r' for c in text),'Unintended control character'
    assert text.count('$$')%2==0
    assert text.replace('$$','').count('$')%2==0
    depth=0
    for c in text:
        if c=='{':depth+=1
        elif c=='}':depth-=1;assert depth>=0
    assert depth==0
    assert '--' not in text and '+-' not in text

def check_record(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=r['question'];meta=r['generation'];name,i,j,rows,value=display(q[':question/problem']);n=len(rows)
    formatting(q[':question/problem'])
    assert len(q[':question/answer-fields'])==1
    f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];kind=f[':answer-field/type'].split('/')[-1]
    assert kind in ('radio','blank') and len(choices)==(1 if kind=='blank' else 5)
    if kind=='blank':assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    bank={}
    for a in choices:
        formatting(a[':answer/value'])
        assert not any('feedback' in k for k in a),'Absent source feedback was invented'
        assert a[':answer/type']==(':answer.type/text' if a[':answer/value']=='No such entry' else ':answer.type/math')
        v=a[':answer/value'];canon=v if v=='No such entry' else scalar(v)
        assert canon not in bank,'Ambiguous actual displayed bank';bank[canon]=a[':answer/id']
    correct=value if value=='No such entry' else scalar(value)
    assert correct in bank,'Display-derived answer absent'
    if ':answer-field/correct' in f:assert f[':answer-field/correct']==[':answer/id',bank[correct]]
    # Read all option recipes from printed rows; no mathematical generation metadata.
    p={'matrix':rows,'i':i,'j':j};profile=meta['bank_profile'].removeprefix('raw_');recipes=g.BANKS[profile][1]
    expected=[]
    coords={'target':(i,j),'left':(i,j-1),'right':(i,j+1),'up':(i-1,j),'down':(i+1,j),'transpose':(j,i),'transposed_first':(j,1),'last_diagonal':(n,n),'previous_diagonal':(n-1,n-1),'cell11':(1,1),'cell12':(1,2),'cell21':(2,1),'cell22':(2,2),'cell23':(2,3)}
    for recipe in recipes:
        if recipe=='missing':v='No such entry'
        elif recipe.startswith('opaque'):v=meta['parameters']['opaque'][int(recipe[-1])]
        else:
            row,col=coords[recipe];assert 1<=row<=n and 1<=col<=n;v=rows[row-1][col-1]
        expected.append(v if v=='No such entry' else scalar(v))
    assert set(expected)==set(bank),'Displayed whole-bank operations disagree'
    if ':question/worked-solution' in q:
        sol=q[':question/worked-solution'];formatting(sol)
        assert f'${i}$'+g.ordinal(i)[len(str(i)):]+' row' in sol
        assert f'${j}$'+g.ordinal(j)[len(str(j)):]+' column' in sol
        # Every printed target, including the final conclusion, must move together.
        for symbol,I,J in re.findall(r'\{?([a-z])\}?_\{(\d)(\d)\}',sol):
            assert symbol==name and (int(I),int(J))==(i,j),'Stale solution target'
        if value!='No such entry':
            assert re.search(r'\}\$' if False else r'='+re.escape(value)+r'\.\$',sol),'Wrong displayed conclusion'
            matrix=re.search(r'\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\1\}',sol,re.S)
            assert matrix and matrix.group(2)==r' \\ '.join(' & '.join(row) for row in rows)
            if not meta['evidence_only']:assert name.upper()+'=' in sol or name.upper()+' =' in sol,'Solution matrix name mismatch'
            assert sol.count('intersection of')==1 and sol.count('Therefore,')==1
            assert len(re.findall(r'\\begin\{(?:aligned|bmatrix)\}',sol))==1,'Changed solution stage count'
        else:
            axis='row' if i>n else 'column';idx=i if i>n else j
            assert f'${n}\\times {n}$ matrix' in sol and g.ordinal(idx)[len(str(idx)):]+' '+axis in sol
            assert len(re.findall(r'\\begin\{(?:aligned|bmatrix)\}',sol))==0
    if not meta['evidence_only']:
        assert r'\begin{aligned}' not in q[':question/problem']
        assert r'\begin{aligned}' not in q[':question/worked-solution']
        assert meta['eligible_for_learning'] and ':question/difficulty' in q and ':question/worked-solution' in q and ':answer-field/correct' in f
        level=q[':question/difficulty'].split('/')[-1]
        if level=='easy':assert 2<=n<=4
        if level=='moderate':assert n==5 and 4<=max(i,j)<=5
        if level=='hard':assert n==6 and 5<=max(i,j)<=6
    else:assert not meta['eligible_for_learning']
    return value

def source_check():
    results=[];records=[]
    for case in CASES:
        r=g.generate(case['level'],37,case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=r['question'];src=SOURCES[case['source_id']]
        for key in (':question/problem',':question/difficulty',':question/worked-solution',':question/answer-fields'):
            assert (key in q)==(key in src),(case['source_id'],key,'presence')
            if key in q and key!=':question/answer-fields':
                expected=src[key][':db/ident'] if isinstance(src[key],dict) else src[key]
                assert q[key]==expected,(case['source_id'],key,q[key],expected)
        f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
        for key in (':answer-field/key',':answer-field/type'):
            expected=sf[key][':db/ident'] if isinstance(sf[key],dict) else sf[key];assert f[key]==expected
        assert sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in sf[':answer-field/choices'])
        assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
        if ':answer-field/correct' in sf:
            val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert val==sf[':answer-field/correct'][':answer/value']
        check_record(r);records.append(r);results.append({'source_id':case['source_id'],'prompt_exact':True,'solution_exact':True if ':question/worked-solution' in src else None,'bank_exact':True,'correct_matched':True if ':answer-field/correct' in sf else None,'presence_parity':True,'choices':len(sf[':answer-field/choices'])})
    return results,records

def normal_source_check():
    """Only presentation normalization/name repair may change observed prose."""
    results=[]
    for case in CASES:
        src=SOURCES[case['source_id']]
        if ':question/worked-solution' not in src:continue
        profile=case['bank_profile'].removeprefix('raw_')
        if profile=='q-13490':profile='right_up_left' # Opaque source bank remains raw-only.
        q=g.generate(case['level'],37,case['template'],parameters=case['parameters'],profile=profile)['question']
        for key in (':question/problem',':question/worked-solution'):
            expected=src[key].replace(r'[\begin{aligned}',r'\begin{bmatrix}').replace(r'\end{aligned}]',r'\end{bmatrix}')
            if case['source_id']=='q-125593' and key==':question/worked-solution':expected=expected.replace('E=', 'R=')
            assert q[key]==expected,(case['source_id'],key,'normal sequence/prose mismatch')
        results.append(case['source_id'])
    return results

def current_context_check():
    """2275 context must differ only by enclosure and the supported E/R repair."""
    current=json.loads((HERE/'source-current-context.json').read_text())
    assert current['database']==SOURCE['database'] and current['basis']==2275 and current['lineage']==SOURCE['lineage']
    fresh={q[':question/math-academy-id']:q for q in current['record'][':knowledge-point/questions']}
    assert set(fresh)==set(SOURCES)
    results=[]
    for source_id,old in SOURCES.items():
        expected=copy.deepcopy(old);changed=[]
        for key in (':question/problem',':question/worked-solution'):
            if key not in expected:continue
            expected[key]=expected[key].replace(r'[\begin{aligned}',r'\begin{bmatrix}').replace(r'\end{aligned}]',r'\end{bmatrix}')
            if source_id=='q-125593' and key==':question/worked-solution':expected[key]=expected[key].replace('E=', 'R=')
            if expected[key]!=old[key]:changed.append(key)
        # All field layouts/types/banks/refs/feedback and omissions stay exact.
        assert expected==fresh[source_id],(source_id,'unexpected refreshed source change')
        results.append({'source_id':source_id,'changed_attributes':changed,'notation_only':source_id!='q-125593',
            'supported_name_repair':source_id=='q-125593','all_other_attributes_exact':True})
    report={'passed':True,'original_provenance':{k:SOURCE[k] for k in ('database','basis','lineage')},
        'current_context_provenance':{k:current[k] for k in ('database','basis','lineage')},'records':results,
        'context_capture_sha256':hashlib.sha256((HERE/'source-current-context.json').read_bytes()).hexdigest()}
    (HERE/'current-source-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

def slot_checks():
    """Enumerate complete-bank target roles; never pad a colliding bank."""
    coverage={};records=[];rejections=0
    for level in ('easy','moderate','hard'):
        sizes=(2,3,4) if level=='easy' else ({'moderate':5,'hard':6}[level],)
        for template in g.TEMPLATES:
            if level!='easy' and template=='absent_radio':continue
            for profile in g.eligible_banks(level,template):
                targets=[]
                for n in sizes:
                    pairs=[(i,j) for i in range(1,n+1) for j in range(1,n+1)]
                    if template=='absent_radio':
                        if n!=2:continue
                        pairs=[(3,1),(3,2),(1,3),(2,3)]
                    for i,j in pairs:
                        if level!='easy' and max(i,j)<{'moderate':4,'hard':5}[level]:continue
                        p={'matrix':[[g.VALUES[(row*n+col)%len(g.VALUES)] for col in range(n)] for row in range(n)],'name':'Z','i':i,'j':j}
                        coords=[g.coordinates(recipe,p) for recipe in g.BANKS[profile][1] if recipe!='missing']
                        valid=all(1<=row<=n and 1<=col<=n for row,col in coords) and len(set(coords))==len(coords)
                        if valid:
                            for k,(row,col) in enumerate(coords):p['matrix'][row-1][col-1]=g.VALUES[k]
                            record=g.generate(level,51,template,parameters=p,profile=profile);check_record(record);records.append(record);targets.append([n,i,j])
                            same=g.generate(level,991,template,parameters=p,profile=profile)
                            assert same['question'][':question/id']==record['question'][':question/id']
                        else:
                            try:g.generate(level,51,template,parameters=p,profile=profile)
                            except g.SampleRejected:rejections+=1
                            else:raise AssertionError('Structurally colliding/out-of-range bank accepted')
                coverage[level+'/'+profile]=targets
                assert targets,'Supported profile has no exercised targets'
    # Change only the target against a fixed matrix, retaining the complete bank.
    p={'matrix':[[str(-8+row*4+col) for col in range(4)] for row in range(4)],'name':'Q','i':1,'j':4}
    first=g.generate_easy(template='inline_radio',parameters=p,profile='inline_diagonal');check_record(first)
    p['i'],p['j']=4,1
    second=g.generate_easy(template='inline_radio',parameters=p,profile='inline_diagonal');check_record(second)
    assert display(first['question'][':question/problem'])[3]==display(second['question'][':question/problem'])[3]
    assert first['question'][':question/id']!=second['question'][':question/id']
    records.extend([first,second])
    # Whole-bank choice precedes sampling and stays fixed through rejection retries.
    original=g.sample;calls=[]
    def tracked(level,template,bank,rng):
        calls.append(bank)
        if len(calls)==1:return {'matrix':[['1']*3 for _ in range(3)],'name':'A','i':3,'j':2,'inline':False}
        return original(level,template,bank,rng)
    g.sample=tracked
    try:r=g.generate_easy(91,template='aligned_radio')
    finally:g.sample=original
    check_record(r);assert len(calls)>1 and set(calls)=={r['generation']['bank_profile']}
    # Profile aliases have identical content/IDs; no extra mathematical tasks.
    case=CASES[0]
    a=g.generate_easy(17,parameters=case['parameters'],profile='q-13495')
    b=g.generate_easy(93,parameters=case['parameters'],profile='transpose_neighbors')
    assert a['question'][':question/id']==b['question'][':question/id']
    assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
    for level,n,depth in [('easy',4,4),('moderate',5,4),('hard',6,5)]:
        good={'matrix':[['0']*n for _ in range(n)],'name':'A','i':depth,'j':n}
        invalid=[]
        for value in ('14','-14',r'\sqrt{4}'):
            p=copy.deepcopy(good);p['matrix'][0][0]=value;invalid.append(p)
        for i,j in ((0,1),(1,0),(n+1,1),(1,n+1)):
            p=copy.deepcopy(good);p['i'],p['j']=i,j;invalid.append(p)
        p=copy.deepcopy(good);p['matrix'][0].append('1');invalid.append(p)
        for p in invalid:
            try:g.generate(level,template='aligned_blank',parameters=p,profile='blank')
            except ValueError:pass
            else:raise AssertionError('Explicit parameter domain guard escaped')
    return coverage,records,rejections

def mutation_checks(r):
    # Each intentional error must be detected by actual-display inspection.
    for kind in ('matrix','solution','bank','shape','target','control','stage'):
        bad=copy.deepcopy(r)
        if kind=='matrix':bad['question'][':question/problem']=bad['question'][':question/problem'].replace(' & ',' & 99 & ',1)
        elif kind=='solution':bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(' row',' column',1)
        elif kind=='bank':bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='999'
        elif kind=='shape':bad['knowledge_point'][':db/id']=g.KP_ID
        elif kind=='target':bad['question'][':question/worked-solution']=re.sub(r'_\{\d\d\}', '_{11}',bad['question'][':question/worked-solution'],count=1)
        elif kind=='control':bad['question'][':question/problem']+='\x0c'
        else:bad['question'][':question/worked-solution']+='\n\n'+bad['question'][':question/worked-solution'].split('\n\n')[-1]
        try:check_record(bad)
        except (AssertionError,ValueError):pass
        else:raise AssertionError('Mutation escaped '+kind)

def main():
    fidelity,raw=source_check();normal_sequence=normal_source_check();current_context=current_context_check();slot_coverage,slot_records,slot_rejections=slot_checks();generated=[];counts={};families={};profiles={}
    for level in ('easy','moderate','hard'):
        records=[g.generate(level,seed) for seed in range(250)]
        for r in records:check_record(r)
        generated+=records;counts[level]=len({r['generation']['parameter_fingerprint'] for r in records});families[level]=sorted({r['generation']['template'] for r in records});profiles[level]=sorted({r['generation']['bank_profile'] for r in records})
        assert len(families[level])==(4 if level=='easy' else 3)
        assert set(profiles[level])==({'transpose_neighbors','right_up_left','local_neighbors','blank','inline_diagonal','all_four'} if level=='easy' else {'transpose_neighbors','right_up_left','local_neighbors','blank','inline_diagonal'})
        assert counts[level]>100
    # All explicit cases keep identity across seed and options; incidental cells
    # alter full content identity but cannot inflate mathematical task count.
    for r in generated[:40]:
        m=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
        other=g.generate(level,987,m['template'],parameters=m['parameters'],profile=m['bank_profile'])
        assert r['question'][':question/id']==other['question'][':question/id']
        assert m['parameter_fingerprint']==other['generation']['parameter_fingerprint']
    r=g.generate_easy(0,template='aligned_blank');p=copy.deepcopy(r['generation']['parameters']);row,col=p['i']-1,p['j']-1
    otherrow,othercol=next((a,b) for a in range(len(p['matrix'])) for b in range(len(p['matrix'])) if (a,b)!=(row,col));p['matrix'][otherrow][othercol]='13' if p['matrix'][otherrow][othercol]!='13' else '12'
    changed=g.generate_easy(777,template='aligned_blank',parameters=p,profile='blank');assert changed['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint'];assert changed['question'][':question/id']!=r['question'][':question/id']
    # Enumerate every meaningful domain task through public blank/absent APIs.
    enumerated={}
    for level in ('easy','moderate','hard'):
        fingerprints=set()
        for n in ((2,3,4) if level=='easy' else ({'moderate':5,'hard':6}[level],)):
            for i in range(1,n+1):
                for j in range(1,n+1):
                    if level!='easy' and max(i,j)<{'moderate':4,'hard':5}[level]:continue
                    for value in g.VALUES:
                        p={'matrix':[['0']*n for _ in range(n)],'name':'A','i':i,'j':j};p['matrix'][i-1][j-1]=value
                        item=g.generate(level,template='aligned_blank',parameters=p,profile='blank');check_record(item);fingerprints.add(item['generation']['parameter_fingerprint'])
        if level=='easy':
            for i,j in ((3,1),(3,2),(1,3),(2,3)):
                item=g.generate_easy(template='absent_radio',parameters={'matrix':[['1','2'],['3','4']],'name':'A','i':i,'j':j},profile='all_four');check_record(item);fingerprints.add(item['generation']['parameter_fingerprint'])
        enumerated[level]=len(fingerprints)
    assert enumerated=={'easy':845,'moderate':464,'hard':580}
    mutation_checks(next(r for r in generated if r['generation']['template']=='aligned_radio'))
    # Explicit level violation and whole-bank collision must reject, never repair.
    for level,size,index in [('moderate',4,4),('moderate',5,3),('hard',5,5),('hard',6,4)]:
        try:g.generate(level,template='aligned_blank',parameters={'matrix':[['1']*size for _ in range(size)],'name':'A','i':index,'j':1})
        except ValueError:pass
        else:raise AssertionError('Level guard escaped')
    try:g.generate_easy(template='aligned_radio',parameters={'matrix':[['1']*3 for _ in range(3)],'name':'A','i':3,'j':2},profile='transpose_neighbors')
    except g.SampleRejected:pass
    else:raise AssertionError('Collision was not whole-instance rejected')
    checks=[]
    # Raw missing ref cannot be graded faithfully; grade its supported authored
    # completion, while retaining its exact omissions separately above.
    completion=g.generate_easy(parameters=CASES[1]['parameters'],profile='q-13506');check_record(completion)
    grading=[r for r in raw if ':answer-field/correct' in r['question'][':question/answer-fields'][0]]+[completion]+generated+slot_records
    for index,r in enumerate(grading):
        f=r['question'][':question/answer-fields'][0];correct_id=f[':answer-field/correct'][1];casechecks=[]
        if f[':answer-field/type'].endswith('/radio'):
            casechecks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct_id else 'rejected','purpose':'display-verified owned choice'} for a in f[':answer-field/choices']]
        else:
            value=check_record(r);v=scalar(value)
            equivalent=str(v)+'+0' if v>=0 else '('+str(v)+')+0'
            casechecks=[{'submitted':value,'expected':'accepted','purpose':'canonical fragment'},{'submitted':equivalent,'expected':'accepted','purpose':'unsimplified equivalent entry'},{'submitted':str(v+1),'expected':'rejected','purpose':'wrong fragment'}]
        checks.append({'label':str(index),'record':r,'checks':casechecks})
    (HERE/'engine-input.json').write_text(json.dumps(checks,indent=2)+'\n')
    engine=REPO/'generate/runs/current/check-engine';subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    report=json.loads((HERE/'engine-report.json').read_text())
    review=[]
    for case,r in zip(CASES,raw):
        review.append({'label':'Original raw public replay '+case['source_id'],'record':r})
        # Change complete mathematical objects, preserving observed recipe slots.
        p=copy.deepcopy(case['parameters']);p['matrix']=[[str(-int(v)) if re.fullmatch('-?\\d+',v) else v for v in row] for row in p['matrix']]
        if 'opaque' in p:p['opaque']=[str(-int(v)) for v in p['opaque']]
        variant=g.generate_easy(83,case['template'],parameters=p,profile=case['bank_profile']);check_record(variant)
        review.append({'label':'Generated parameterized observed-bank variant '+case['source_id']+' (raw evidence-only)','record':variant})
    for level in ('easy','moderate','hard'):
        for r in [r for r in generated if r['question'][':question/difficulty'].endswith('/'+level)][:2]:review.append({'label':'Authored normal '+level+' variant','record':r})
    review.append({'label':'Authored q-13506 completion','record':completion})
    for index,r in enumerate(slot_records[-2:],1):
        review.append({'label':'Authored fixed-matrix changed-target example '+str(index),'record':r})
    (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
    (HERE/'review.md').write_text('# Square-entry review\n\nRaw records retain source omissions. Generated raw-profile variants are evidence-only; normal variants are eligible.\n\n'+'\n\n---\n\n'.join('## '+x['label']+'\n\n'+g.markdown(x['record']) for x in review)+'\n')
    result={'passed':True,'source':g.PROVENANCE,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_fidelity':{'records':6,'rated_easy':5,'unrated':1,'exact_prompts':6,'exact_solutions':5,'solution_denominator':5,'exact_banks':6,'displayed_choices':26,'matched_correct_designations':5,'correct_designation_denominator':5,'missing_correct_designations':1,'presence_parity':6,'cases':fidelity},'normal_correctness_records':len(generated),'meaningful_domain_tasks':enumerated,'meaningful_sampled_tasks':counts,'default_templates':families,'default_bank_profiles':profiles,'native_grading':{k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_provenance':{'binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'harness_sha256':hashlib.sha256((engine.with_suffix('.rs')).read_bytes()).hexdigest()},'repairs':['q-125593 raw E matrix label retained; normal solution matches requested name','q-13506 raw absent difficulty/solution/correct retained; normal completion explicitly authored and inferred'], 'interpretation_limitations':['q-13490 historical5/4 scalar intent unidentifiable; public evidence-only slots retained, authored complete normal bank used'],'unresolved_findings':[], 'tests':['independent actual-display row/column and bank operations','worked-solution prose/rows/conclusion','raw key-presence/value parity','250 random records per level','all1889meaningful domain tasks public-API verified','all normal family/bank coverage','explicit scope guards and whole-bank collision rejection','stable content identity; incidental-cell task deduplication','four corruption regressions','real native grading']}
    result.update({'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),
        'normal_source_solution_sequence_matches':len(normal_sequence),'normal_source_solution_sequence_denominator':5,
        'presentation_normalization':{'raw_exact_preserved':True,'normal_aligned_replaced_by_bmatrix':True,'math_or_stage_changes':0},
        'current_source_context':current_context,
        'target_slot_checks':{'verified_records':len(slot_records),'structurally_ineligible_whole_banks_rejected':slot_rejections,'coverage':slot_coverage},
        'source_feedback':{'sources_with_feedback':0,'invented_feedback':0},
        'baseline_sha256_at_copy':'b37bf5c164840e3a1471cd1f10efa51af8d4a2d1226630662f8dc199d3b38b5c',
        'prior_approved_sha256':'8c08ebf52c0e8c817e90e115e150ba75d6468352913c65cd6bf4e7c965ce325a',
        'live_baseline_modified':False})
    result['tests']+=['all eligible per-profile target slots and ineligible structural banks',
        'fixed-matrix changed-target prompt/solution/bank checks','profile selection before parameters through whole-instance retry',
        'complete normalized normal source prose/stage parity','profile alias identity and explicit bounds',
        'control-character, stale-target and duplicated-stage corruption regressions']
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':True,'fidelity_records':6,'sampled_tasks':counts,'native':result['native_grading'],'target_slot_records':len(slot_records),'structural_bank_rejections':slot_rejections}))
if __name__=='__main__':main()
