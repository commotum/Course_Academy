#!/usr/bin/env python3
"""Independent displayed-math, full-fidelity, identity, bounds and native QA."""
from copy import deepcopy
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
import sympy as sp

ROOT=Path(__file__).resolve().parent
SCRIPT=ROOT.with_suffix('.py')
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('triangular_generator',SCRIPT)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)


def independent_matrices(text):
    result={}
    for m in re.finditer(r'([A-E])=\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]',text,re.S):
        rows=[row.split('&') for row in m[2].split(r'\\')]
        mat=sp.Matrix([[sp.sympify(x.strip()) for x in row] for row in rows])
        assert mat.rows==mat.cols
        if m[1] in result:assert result[m[1]]==mat,'stale repeated solution matrix'
        result[m[1]]=mat
    return result


def good_labels(matrices,criterion):
    def eligible(mat):
        return all(mat[i,j]==0 for i in range(mat.rows) for j in range(mat.cols)
                   if (i>j if criterion=='upper' else i<j))
    return tuple(sorted(label for label,mat in matrices.items() if eligible(mat)))


def fields_equal(raw,source):
    fs=raw['question'][':question/answer-fields'];original=source[':question/answer-fields']
    assert len(fs)==len(original)
    for actual,expected in zip(fs,original):
        assert set(actual)==set(expected)-{':db/id'}
        assert actual.get(':answer-field/key')==expected.get(':answer-field/key')
        assert actual[':answer-field/type']==expected[':answer-field/type'][':db/ident']
        aa=actual[':answer-field/choices'];ee=expected[':answer-field/choices']
        assert len(aa)==len(ee)
        assert {(a[':answer/value'],a[':answer/type']) for a in aa}=={(a[':answer/value'],a[':answer/type'][':db/ident']) for a in ee}
        for a in aa:assert set(a)==set(ee[0])-{':db/id'}
        if ':answer-field/correct' in expected:
            key=actual[':answer-field/correct'][1]
            assert next(a[':answer/value'] for a in aa if a[':answer/id']==key)==expected[':answer-field/correct'][':answer/value']
    q=raw['question']
    assert set(q)==set(source)-{':db/id'}
    assert q[':question/problem']==source[':question/problem']
    assert q[':question/worked-solution']==source[':question/worked-solution']
    assert q.get(':question/math-academy-id')==source.get(':question/math-academy-id')


def formatting(text):
    assert '@@' not in text
    assert text.count('$$')%2==0
    assert text.replace('$$','').count('$')%2==0
    depth=0
    for i,c in enumerate(text):
        if i and text[i-1]=='\\':continue
        if c=='{':depth+=1
        if c=='}':depth-=1
        assert depth>=0,'closing TeX brace'
    assert depth==0,'unbalanced TeX braces'
    assert text.count(r'\begin{aligned}')==text.count(r'\end{aligned}')


def check_record(record,allow_raw=False):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    q=record['question'];meta=record['generation'];level=q[':question/difficulty'].rsplit('/',1)[1]
    assert meta['eligible_for_learning']!=meta['evidence_only']
    assert allow_raw or not meta['evidence_only']
    criterion='upper' if 'upper triangular' in q[':question/problem'] else 'lower'
    formatting(q[':question/problem']);formatting(q[':question/worked-solution'])
    if level=='easy':
        assert 'Which of the following is ' in q[':question/problem']
        matrices={}
        for a in q[':question/answer-fields'][0][':answer-field/choices']:
            assert a[':answer/type']==':answer.type/math'
            assert '$' not in a[':answer/value']
            matrices.update(independent_matrices(a[':answer/value']))
        assert set(matrices)==set('ABCDE')
    else:
        matrices=independent_matrices(q[':question/problem'])
        assert set(matrices)==set('ABC' if level=='moderate' else 'ABCDE')
    eligible=good_labels(matrices,criterion)
    if level=='easy':assert len(eligible)==1
    if level=='moderate':assert len(eligible) in (1,2)
    if level=='hard':assert len(eligible) in (2,3) and all(m.rows==4 for m in matrices.values())
    assert len({tuple(mat) for mat in matrices.values()})==len(matrices),'duplicate entire matrices'
    field_ids=[];answer_ids=[]
    for f in q[':question/answer-fields']:
        assert f[':answer-field/type']==':answer-field.type/radio'
        field_ids.append(f[':answer-field/id']);choices=f[':answer-field/choices']
        assert len(choices)==5
        answer_ids.extend(a[':answer/id'] for a in choices)
        values=[a[':answer/value'] for a in choices]
        assert len(set(values))==5
        for a in choices:formatting(a[':answer/value'])
        if level=='easy':
            valid=[a for a in choices if good_labels(independent_matrices(a[':answer/value']),criterion)]
        else:
            banks=[tuple(sorted(re.findall(r'\$([A-E])\$',a[':answer/value']))) for a in choices]
            assert len(set(banks))==5,'duplicate subset choices'
            valid=[a for a,b in zip(choices,banks) if b==eligible]
        assert len(valid)==1,'ambiguous/missing mathematically correct option'
        if ':answer-field/correct' in f:assert f[':answer-field/correct']==[':answer/id',valid[0][':answer/id']]
        else:assert allow_raw and meta['profile']=='raw:q-42090'
    assert len(set(field_ids))==len(field_ids) and len(set(answer_ids))==len(answer_ids)
    solution=q[':question/worked-solution']
    if level=='easy':
        repeated=independent_matrices(solution)
        assert set(repeated)==set(matrices),'correct matrix and all four foils must repeat'
        for label,mat in matrices.items():assert repeated[label]==mat
        positive=re.search(r'Notice that \$([A-E])\$',solution)[1]
        assert (positive,)==eligible
        negative=solution.split('By contrast, matrices ')[1].split(' each')[0]
        assert tuple(sorted(re.findall(r'\$([A-E])\$',negative)))==tuple(x for x in 'ABCDE' if x not in eligible)
        side='below' if criterion=='upper' else 'above'
        assert 'entries *'+side+'*' in solution and 'non-zero entry '+side in solution
    else:
        first=solution.split(' since ')[0]
        assert tuple(sorted(re.findall(r'\$([A-E])\$',first)))==eligible
        second=solution.split('\n\n')[1].split(' since ')[0]
        expected_bad=tuple(sorted(x for x in matrices if x not in eligible))
        assert tuple(sorted(re.findall(r'\$([A-E])\$',second)))==expected_bad
        proofs=[]
        for m in re.finditer(r'\{([a-e])\}_\{([1-4])([1-4])\} & =(-?\d+)\\ne 0',solution):
            label=m[1].upper();i=int(m[2])-1;j=int(m[3])-1;value=sp.Integer(m[4]);proofs.append(label)
            assert i<matrices[label].rows and j<matrices[label].cols
            assert matrices[label][i,j]==value and value!=0,'stale witness value'
            assert (i>j if criterion=='upper' else i<j),'witness on wrong side'
        assert tuple(sorted(proofs))==expected_bad,'every foil must have one real witness'
        side='below' if criterion=='upper' else 'above'
        assert 'entries '+side+' the main diagonal are zeros' in solution
        assert 'element '+side+' the main diagonal' in solution
    # Display independently checked above; now ensure metadata describes it too.
    assert {k:sp.Matrix(v) for k,v in meta['parameters']['matrices'].items()}==matrices
    assert meta['parameters']['criterion']==criterion
    # Preserve the ENTIRE source family's prose and stage sequence under new
    # parameters, not just its first sentence or number of matrix/witness rows.
    if level!='hard':
        sid=meta['profile'].removeprefix('raw:')
        source=g.SOURCES[sid]
        def skeleton(text):
            text=re.sub(r'([A-E])=\[\\begin\{aligned\}.*?\\end\{aligned\}\]',
                        lambda m:'MATRIX_'+m[1],text,flags=re.S)
            text=re.sub(r'\{([a-e])\}_\{[1-4][1-4]\} & =-?\d+\\ne 0',
                        lambda m:'WITNESS_'+m[1],text)
            text=text.replace('upper triangular','CRITERION triangular').replace('lower triangular','CRITERION triangular').replace('above','SIDE').replace('below','SIDE')
            return re.sub(r'\b(?:a|an) CRITERION triangular', 'ARTICLE CRITERION triangular',text)
        assert skeleton(solution)==skeleton(source[':question/worked-solution']),'changed source teaching stages/prose'
        assert skeleton(q[':question/problem'])==skeleton(source[':question/problem']),'changed source prompt structure'


def rejects(fn):
    try:fn()
    except (AssertionError,ValueError,IndexError):return
    raise AssertionError('negative regression was not rejected')


def write(name,data):
    (ROOT/name).write_text(json.dumps(data,indent=2)+'\n')


def main():
    source_cases=[];mapping=[];raws=[];normal_anchors=[];generated=[]
    for sid,source in g.SOURCES.items():
        r=g.recipe(sid);p={'criterion':r['criterion'],'matrices':deepcopy(r['matrices'])}
        case={'source_id':sid,'template':g.TEMPLATES[r['level']],'level':r['level'],'parameters':p,'profile':'raw:'+sid,'bank_profile':sid}
        source_cases.append(case)
        raw=g.generate(r['level'],profile='raw:'+sid,parameters=p);fields_equal(raw,source);check_record(raw,True);raws.append(raw)
        normal=g.generate(r['level'],profile=sid,parameters=p);check_record(normal);normal_anchors.append(normal)
        assert normal['question'][':question/problem']==source[':question/problem']
        assert normal['question'][':question/worked-solution']==source[':question/worked-solution']
        fieldmaps=[]
        for i,f in enumerate(source[':question/answer-fields']):
            choices=[]
            for a in f[':answer-field/choices']:
                value=a[':answer/value']
                label=value[0] if r['level']=='easy' else None
                choices.append({'source_answer_id':a[':answer/id'],'value':value,'type':a[':answer/type'][':db/ident'],
                                'recipe':{'whole_matrix':label,'dimension':len(r['matrices'][label]),'support':g.support(r['matrices'][label])} if label else {'labeled_subset':g.subset(value)},
                                'correct':a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id') if ':answer-field/correct' in f else None})
            fieldmaps.append({'field_index':i,'key_present':':answer-field/key' in f,'correct_present':':answer-field/correct' in f,'choices':choices})
        mapping.append({'source_id':sid,'profile':sid,'criterion':r['criterion'],'preferred_witnesses':r['preferred'],'fields':fieldmaps})
        generated.extend([g.generate(r['level'],seed=80+k,profile=sid) for k in (0,1)])
    for profile in ('hard_two','hard_three'):
        generated.extend([g.generate_hard(seed=80+k,profile=profile) for k in (0,1)])
    for record in generated:check_record(record)
    catalog_counts={};fingerprints={level:set() for level in g.LEVELS};tested=0
    for profile in (*g.SOURCES,'hard_two','hard_three'):
        level=g.recipe(profile)['level'] if profile.startswith('q-') else 'hard'
        catalog=g.catalog(profile);catalog_counts[profile]=len(catalog)
        for p in catalog:
            record=g.generate(level,parameters=p,profile=profile);check_record(record)
            fingerprints[level].add(record['generation']['mathematical_fingerprint']);tested+=1
    random_counts={};default_profiles={level:set() for level in g.LEVELS}
    for level in g.LEVELS:
        unique=set()
        for seed in range(150):
            record=g.generate(level,seed=seed);check_record(record)
            unique.add(record['generation']['mathematical_fingerprint']);default_profiles[level].add(record['generation']['profile'])
        random_counts[level]=len(unique)
    assert len(default_profiles['easy'])==6 and len(default_profiles['moderate'])==2 and len(default_profiles['hard'])==2
    # Same fixed objects/order cannot gain identities from seed or aliases.
    a=generated[0];level=a['question'][':question/difficulty'].rsplit('/',1)[1]
    b=g.generate(level,seed=902,profile=a['generation']['profile'],parameters=a['generation']['parameters'])
    assert a['question'][':question/id']==b['question'][':question/id']
    assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
    p=deepcopy(a['generation']['parameters'])
    for mat in p['matrices'].values():
        for i in range(len(mat)):mat[i][i]=0
        for i,row in enumerate(mat):
            for j,v in enumerate(row):
                if i!=j and v:row[j]=-1 if v>0 else 1
    c=g.generate(level,profile=a['generation']['profile'],parameters=p)
    assert a['generation']['mathematical_fingerprint']==c['generation']['mathematical_fingerprint']
    assert a['question'][':question/id']!=c['question'][':question/id']
    # Label aliases and reordered complete subset banks cannot inflate identity.
    mat=a['generation']['parameters']['matrices'];labels=sorted(mat);rename=dict(zip(labels,reversed(labels)))
    swapped={'criterion':a['generation']['parameters']['criterion'],'matrices':{rename[k]:v for k,v in mat.items()}}
    wit=g.witnesses(mat,a['generation']['parameters']['criterion'])
    orig=g.task_fingerprint(level,a['generation']['parameters'],[],wit)
    swapped_fp=g.task_fingerprint(level,swapped,[],{rename[k]:v for k,v in wit.items()})
    assert orig==swapped_fp
    # Answer subsets and the selected explanatory witness are presentation.
    assert orig==g.task_fingerprint(level,a['generation']['parameters'],[('A',)],{'A':(0,1)})
    # Every hard displayed object must occur in the complete response bank.
    for profile in ('hard_two','hard_three'):
        assert set().union(*(set(choice) for choice in g.hard_bank(profile)))==set('ABCDE')
    # Inclusive diagonal/identity membership and strict explicit bounds.
    for m in (sp.zeros(3),sp.eye(3),sp.diag(0,-5,2)):
        assert good_labels({'A':m},'upper')==('A',) and good_labels({'A':m},'lower')==('A',)
    p=deepcopy(a['generation']['parameters']);p['matrices']['A'][0][0]=12
    rejects(lambda:g.generate(level,profile=a['generation']['profile'],parameters=p))
    p=deepcopy(a['generation']['parameters']);p['matrices']['A'][0][0]=1.0
    rejects(lambda:g.generate(level,profile=a['generation']['profile'],parameters=p))
    p=deepcopy(a['generation']['parameters']);p['matrices']['A'][0].append(1)
    rejects(lambda:g.generate(level,profile=a['generation']['profile'],parameters=p))
    p=deepcopy(a['generation']['parameters']);p['matrices']['A']=[[1]]
    rejects(lambda:g.generate(level,profile=a['generation']['profile'],parameters=p))
    # Reject a whole bank rather than a replacement option: wrong-side/support
    # count invalidates the original bank's eligibility, even before rendering.
    p=deepcopy(g.recipe('q-126351')['matrices']);p['C'][0][1]=0
    rejects(lambda:g.generate_moderate(profile='q-126351',parameters={'criterion':'lower','matrices':p}))
    h=g.generate_hard(profile='hard_two');p=deepcopy(h['generation']['parameters']);p['matrices']['A']=deepcopy(p['matrices']['B'])
    rejects(lambda:g.generate_hard(profile='hard_two',parameters=p))
    p=deepcopy(h['generation']['parameters']);p['matrices']['C'][0][0]=100
    rejects(lambda:g.generate_hard(profile='hard_two',parameters=p))
    rejects(lambda:g.generate_easy(field_type='checkbox'))
    rejects(lambda:g.generate_hard(profile='q-42090'))
    # Force a same-support whole-matrix collision on the first sample. The
    # sampler must reject all five objects and resample the complete instance.
    original_fill=g.fill_values;attempts=[]
    def first_collision(base,rng):
        p=original_fill(base,rng);attempts.append(p)
        if len(attempts)==1:p['matrices']['B']=deepcopy(p['matrices']['A'])
        return p
    g.fill_values=first_collision
    try:
        resampled=g.generate_easy(seed=56,profile='q-126354')
        assert len(attempts)==2
        check_record(resampled)
    finally:g.fill_values=original_fill
    # Read printed witness/math regressions; validate must catch corruption.
    m=next(r for r in generated if r['generation']['profile']=='q-42090')
    damaged=deepcopy(m);sol=damaged['question'][':question/worked-solution']
    damaged['question'][':question/worked-solution']=re.sub(r'( & =)-?\d+(\\ne 0)',r'\g<1>0\2',sol,count=1)
    rejects(lambda:check_record(damaged))
    damaged=deepcopy(next(r for r in generated if r['question'][':question/difficulty']==':question.difficulty/easy'));sol=damaged['question'][':question/worked-solution']
    damaged['question'][':question/worked-solution']=g.MATRIX_RE.sub(lambda match:g.matrix_tex(match[1],[[9]*len(g.parse_matrices(match[0])[match[1]]) for _ in g.parse_matrices(match[0])[match[1]]]),sol,count=1)
    rejects(lambda:check_record(damaged))
    damaged=deepcopy(next(r for r in generated if r['question'][':question/difficulty']==':question.difficulty/easy'))
    label=next(iter(damaged['generation']['parameters']['matrices']))
    damaged['question'][':question/worked-solution']+='\n\n$$\n'+g.matrix_tex(label,damaged['generation']['parameters']['matrices'][label])+'\n$$'
    rejects(lambda:check_record(damaged))
    damaged=deepcopy(h);f=damaged['question'][':question/answer-fields'][0];f[':answer-field/choices'][0][':answer/value']=f[':answer-field/choices'][1][':answer/value']
    rejects(lambda:check_record(damaged))
    damaged=deepcopy(m);damaged['question'][':question/worked-solution']=sol+'$'
    rejects(lambda:check_record(damaged))
    # Grader checks each owned option at each source anchor and changed profile.
    engine=[]
    for i,record in enumerate(normal_anchors+generated):
        checks=[]
        for fi,f in enumerate(record['question'][':question/answer-fields']):
            for a in f[':answer-field/choices']:
                checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all whole bank choices; displayed math independently verified'})
        engine.append({'label':'record-'+str(i)+':'+record['generation']['profile'],'record':record,'checks':checks})
    write('engine-input.json',engine)
    subprocess.run([str(Path('generate/runs/current/check-engine')),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
    write('source-cases.json',source_cases);write('source-choice-mapping.json',mapping)
    write('review.json',{'raw_originals':raws,'authoritative_repaired_anchors':normal_anchors,'generated_variants':generated})
    review=['# Identifying a Triangular Matrix\n\nBasis1356; originals are publicly parameterized raw recipes. Generated variants use complete source banks or labeled authored hard profiles.']
    for sid,original in zip(g.SOURCES,raws):
        review+=['\n## Original '+sid+' (raw captured layout)\n\n'+g.markdown(original)]
        if sid=='q-42090':review+=['\nLegacy first field has no correct ref. Normal output removes that duplicate: the original MA widget is one five-choice radio. No checkbox migration.']
        review+=['\n### Generated variants of '+sid+'\n\n'+ '\n\n---\n\n'.join(g.markdown(v) for v in generated if v['generation']['profile']==sid)]
    for profile in ('hard_two','hard_three'):
        review+=['\n## Authored hard extension: '+profile+'\n\n'+'\n\n---\n\n'.join(g.markdown(v) for v in generated if v['generation']['profile']==profile)]
    (ROOT/'review.md').write_text('\n'.join(review)+'\n')
    report={'status':'pass','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},
            'source':{k:g.SNAPSHOT[k] for k in ('database','basis','lineage')},
            'source_fidelity':{'practice_questions':8,'raw_prompt_exact':8,'raw_solution_exact':8,'raw_fields_exact_presence':9,'raw_options_exact':45,'existing_correct_designations_matched':8,'missing_correct_designation_preserved':1,'designated_distractors_matched':32,'authoritative_normal_banks_matched':8,'authoritative_normal_options_matched':40,'normal_anchor_solutions_exact':8},
            'repairs':{'q-42090':'remove first duplicate legacy selection radio with absent correct ref; preserve both through raw:q-42090'},
            'catalog_profile_counts':catalog_counts,'catalog_unique_mathematical_tasks':{l:len(f) for l,f in fingerprints.items()},
            'catalog_records_independently_checked':tested,'random_records_checked':450,'sample_unique_tasks_150_seeds':random_counts,
            'default_profile_coverage':{l:sorted(x) for l,x in default_profiles.items()},'review_generated_variants':len(generated),
            'native':json.loads((ROOT/'engine-report.json').read_text()),
            'native_binary_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),
            'limitations':['Hard has no observed practice label; both hard profiles are authored design claims.',
                          'Legacy unkeyed-correct first field is raw evidence only and cannot be natively graded; all normal fields are graded.',
                          'Structural support relocation domains are authored extensions, not recovered Math Academy authoring code.',
                          'Finite catalogs enumerate the actual sampler, not every permissible bounded explicit matrix bank.'],
            'database_writes':0}
    write('validation.json',report)
    print(json.dumps({k:report[k] for k in ('status','source_fidelity','catalog_unique_mathematical_tasks','catalog_records_independently_checked','sample_unique_tasks_150_seeds')},indent=2))

if __name__=='__main__':main()
