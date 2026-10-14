#!/usr/bin/env python3
"""Independent actual-display mathematics, exact fidelity, finite domains, native grading."""
import collections,copy,hashlib,importlib.util,itertools,json,math,pathlib,re,subprocess,sys,uuid
import sympy as sp
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('special_matrix_draft',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def read_display(prompt):
    out={}
    for label,body in re.findall(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',prompt,re.S):
        body=re.sub(r'\\text\{[^}]*\}','',body)
        rows=[[sp.Rational(x.strip()) for x in row.split('&')] for row in body.split(r'\\')]
        out[label]=sp.Matrix(rows)
    assert len(out)==3,'Exactly three displayed matrices'
    return out

def independent_properties(m):
    square=m.rows==m.cols
    offzero=all(m[i,j]==0 for i in range(m.rows) for j in range(m.cols) if i!=j)
    ones=all(m[i,i]==1 for i in range(min(m.rows,m.cols)))
    return {'zero':all(v==0 for v in m),'square':square,'diagonal':square and offzero,'identity':square and offzero and ones}

def selected(f):
    ref=f.get(':answer-field/correct')
    return next((a[':answer/value'] for a in f[':answer-field/choices'] if ref and a[':answer/id']==ref[1]),None)

def check_record(rec):
    assert set(rec['knowledge_point'])=={'db_id','id','title'}
    assert rec['knowledge_point']['db_id']==g.KP_ID
    q=rec['question'];gen=rec['generation'];t=g.TEMPLATES[gen['template']];mats=read_display(q[':question/problem'])
    assert set(mats)==set(t['labels']),'Displayed label slots'
    inspected=sum(m.rows*m.cols for m in mats.values())
    for i,label in enumerate(t['labels']):
        m=mats[label];pr=independent_properties(m);role=t['roles'][i]
        assert 1<=m.rows<=5 and 1<=m.cols<=5,'Actual displayed shape scope'
        assert all(v.q==1 and -3<=v<=7 for v in m),'Actual displayed entry scope'
        if role=='identity':assert pr['identity']
        elif role=='diagonal':assert pr['diagonal']
        elif role=='rectangular':assert not pr['square']
        else:assert pr['square'] and sum(m[a,b]!=0 for a in range(m.rows) for b in range(m.cols) if a!=b)==t['counts'][i]
    if gen['bank_profile'].startswith('raw-'):assert inspected<=36
    else:
        actual_level=q[':question/difficulty'].split('/')[-1];lo,hi={'easy':(3,36),'moderate':(37,45),'hard':(46,60)}[actual_level]
        assert lo<=inspected<=hi,'Actual displayed workload scope'
    kind='identity' if 'identity matrices?' in q[':question/problem'] else 'diagonal'
    assert kind==t['kind'];truth={l:independent_properties(m)[kind] for l,m in mats.items()}
    for s in [q[':question/problem'],q.get(':question/worked-solution',''),*[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]]:
        assert not any(ord(c)<32 and c not in '\n\t' for c in s),'Unintended control character'
        g.validate_prose(s)
    fields=q[':question/answer-fields'];owned=[]
    for f in fields:
        uuid.UUID(f[':answer-field/id']);values=[a[':answer/value'] for a in f[':answer-field/choices']]
        assert len(values)==len(set(values)),'Equivalent bank options'
        if t.get('radio'):
            assert len(fields)==1 and f[':answer-field/type']==':answer-field.type/radio' and len(values)==5
            sets=[frozenset(re.findall(r'\$([A-Z])\$',v)) for v in values]
            assert len(set(sets))==5,'Wrong/wrong subset equivalence'
            expected=frozenset(l for l,b in truth.items() if b)
            if selected(f) is not None:assert frozenset(re.findall(r'\$([A-Z])\$',selected(f)))==expected
            assert sum(x==expected for x in sets)==1,'Complete bank correct subset'
        else:
            assert len(fields)==3 and f[':answer-field/type']==':answer-field.type/checkbox' and set(values)=={'false','true'}
            assert selected(f)==str(truth[f[':answer-field/key']]).lower(),'Actual displayed matrix key'
        for a in f[':answer-field/choices']:
            uuid.UUID(a[':answer/id']);owned.append(a[':answer/id'])
        if ':answer-field/correct' in f:assert f[':answer-field/correct'][1] in [a[':answer/id'] for a in f[':answer-field/choices']]
    assert len(owned)==len(set(owned)),'Field ownership'
    if ':question/worked-solution' in q:
        worked=q[':question/worked-solution'];blocks=worked.split('\n\n- ')
        assert len(blocks)==3
        for label,m in mats.items():
            block=next(b for b in blocks if re.search(r'(?:^- |^)\$'+label+r'\$ is ',b))
            claim=re.search(r'\$'+label+r'\$ is (\*not\* )?(?:a|an) '+kind+r' matrix',block)
            assert claim and (claim[1] is None)==truth[label],'Classification solution stage'
            pr=independent_properties(m)
            if not pr['square']:assert "since it's not a square matrix." in block
            elif kind=='diagonal':
                assert "It's a square matrix since it has the same number of rows and columns." in block,'Missing operative square stage'
                if pr['diagonal']:
                    assert 'all the entries that do not lie on the main diagonal are zeros.' in block,'Missing operative offdiagonal stage'
                    assert ('is not an identity matrix since the diagonal entries are not all ones.' in block)==(not pr['identity'])
                    if pr['identity']:assert 'also an identity matrix since the diagonal entries are all ones.' in block
                else:
                    witness=re.search(r'\$\{'+label.lower()+r'\}_\{(\d)(\d)\}=(-?\d+)\\ne 0\$',block)
                    assert witness,'Missing witness stage'
                    i,j,v=map(int,witness.groups());assert i!=j and 1<=i<=m.rows and 1<=j<=m.cols and m[i-1,j-1]==v and v!=0,'Actual displayed witness'
            elif pr['identity']:
                assert 'entries on the main diagonal are all ones, and the rest of the entries are zeros.' in block
            else:assert "Although it's a diagonal matrix, its diagonal entries are not all ones." in block
        # Independently read the actual conclusion, including absence of selections.
        end=worked.split('\n\n')[-1];reported=set(re.findall(r'\$([A-Z])\$',end))
        assert reported=={l for l,b in truth.items() if b},'Stale conclusion'
    return True

def capacities():
    """Exact finite semantic counts, excluding labels and nonzero magnitudes.

    Repeated equal-role matrix slots are unordered multisets. Diagonal-query diagonal entries are incidental. Identity-query nonidentity
    diagonal slots admit binary one/nonone signatures except the all-one case.
    """
    out={}
    for name,t in g.TEMPLATES.items():
        groups=collections.defaultdict(list)
        for i,role in enumerate(t['roles']):
            sig=(role,t['counts'][i],None,False)
            groups[sig].append(i)
        catalogs=[]
        for (role,k,mode,dense),slots in groups.items():
            cats=[]
            if role=='rectangular':
                # Count exact displayed 0/nonzero matrix signatures by cost, because
                # different rectangular dimensions with equal area are distinct.
                per_cost=collections.Counter(a*b for a in range(1,6) for b in range(1,6) if a!=b)
            else:
                per_cost={}
                for n in range(2 if role=='offdiagonal' else 1,6):
                    v=1 if role=='identity' or t['kind']=='diagonal' else 2**n-1
                    if role=='offdiagonal':v*=math.comb(n*(n-1),k)
                    per_cost[n*n]=v
            for combo in itertools.combinations_with_replacement(sorted(per_cost),len(slots)):
                mult=collections.Counter(combo);count=math.prod(math.comb(per_cost[c]+m-1,m) for c,m in mult.items())
                cats.append((sum(combo),count))
            catalogs.append(cats)
        out[name]={l:sum(math.prod(c for _,c in combo) for combo in itertools.product(*catalogs) if lo<=sum(cost for cost,_ in combo)<=hi) for l,(lo,hi) in {'easy':(3,36),'moderate':(37,45),'hard':(46,60)}.items()}
    return out

def main():
    src=json.loads((HERE/'source.json').read_text());cases=json.loads((HERE/'source-cases.json').read_text());sources={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
    native=[];originals=[];fidelity=[];option_count=0;designation_count=0
    def add_native(rec,label):
        checks=[]
        for i,f in enumerate(rec['question'][':question/answer-fields']):
            for a in f[':answer-field/choices']:
                checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Complete actual displayed bank; correct and every wrong answer'})
        native.append({'label':label,'record':rec,'checks':checks})
    for case in cases:
        sid=case['source_id'];old=sources[sid];rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check_record(rec);originals.append(rec)
        q=rec['question']
        for k in [':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields']:
            assert (k in q)==(k in old),'Source attribute presence: '+sid+' '+k
        assert q[':question/problem']==old[':question/problem'],'Raw-exact prompt: '+sid
        assert q.get(':question/worked-solution')==old.get(':question/worked-solution'),'Full shared prose/stage sequence: '+sid
        if ':question/difficulty' in old:assert q[':question/difficulty']==old[':question/difficulty'][':db/ident']
        of={f[':answer-field/key']:f for f in old[':question/answer-fields']};assert len(of)==len(q[':question/answer-fields'])
        for f in q[':question/answer-fields']:
            prev=of[f[':answer-field/key']]
            assert f[':answer-field/type']==prev[':answer-field/type'][':db/ident']
            assert sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in prev[':answer-field/choices'])
            assert (':answer-field/correct' in f)==(':answer-field/correct' in prev)
            if ':answer-field/correct' in prev:assert selected(f)==prev[':answer-field/correct'][':answer/value'];designation_count+=1
            option_count+=len(f[':answer-field/choices'])
        fidelity.append({'source_id':sid,'prompt_exact':True,'solution_exact':':question/worked-solution' in old,'attribute_presence_exact':True,'bank_exact':True,'designation_matched':':question/worked-solution' in old,'eligible_for_learning':rec['generation']['eligible_for_learning']})
        if sid!='q-7829':add_native(rec,'source '+sid)
        else:add_native(g.generate('easy',template=sid,parameters=case['parameters'],profile='method-'+sid),'authored completion of q-7829')
    variants=[];slot_coverage={};tested=0;unique={l:set() for l in g.SUPPORTED_LEVELS}
    for level in g.SUPPORTED_LEVELS:
        for name,t in g.TEMPLATES.items():
            slots=[{'shapes':set(),'witnesses':set(),'diagonal_signatures':set()} for _ in range(3)]
            for seed in range(120):
                rec=g.generate(level,seed,template=name);check_record(rec);tested+=1;unique[level].add(rec['generation']['parameter_fingerprint'])
                p=rec['generation']['parameters']
                for i,(m,w) in enumerate(zip(p['matrices'],p['witnesses'])):
                    slots[i]['shapes'].add((len(m),len(m[0])));slots[i]['witnesses'].add(tuple(w) if w else None);slots[i]['diagonal_signatures'].add(tuple(0 if sp.Rational(m[j][j])==0 else 1 if sp.Rational(m[j][j])==1 else 2 for j in range(min(len(m),len(m[0])))))
                if seed<2:variants.append(rec);add_native(rec,level+' '+name+' seed '+str(seed))
                if seed==0:
                    # Fixed explicit instance has stable identity despite seed/order.
                    other=g.generate(level,999,template=name,parameters=p)
                    assert rec['question'][':question/id']==other['question'][':question/id']
                    assert rec['generation']['content_fingerprint']==other['generation']['content_fingerprint']
            slot_coverage[level+' '+name]=[{k:sorted([list(x) if x is not None else None for x in v],key=str) for k,v in slot.items()} for slot in slots]
    # Exhaustive finite component masks are rendered through the public API:
    # all eligible offdiagonal obstruction positions, every identity diagonal
    # one/nonone mask, and every rectangular shape/pattern. Other slots stay small.
    finite_component_records=0
    minimal={'matrices':[[['0','1'],['0','0']],[['0']],[['0','1'],['1','0']]],'witnesses':[[1,2],None,[1,2]]}
    for slot,count in [(0,1),(2,2)]:
        for n in range(2,6):
            cells=[(a,b) for a in range(n) for b in range(n) if a!=b]
            for positions in itertools.combinations(cells,count):
                p=copy.deepcopy(minimal);m=[['0']*n for _ in range(n)]
                for a,b in positions:m[a][b]='1'
                p['matrices'][slot]=m;p['witnesses'][slot]=[positions[-1][0]+1,positions[-1][1]+1]
                check_record(g.generate('easy',template='q-11562',parameters=p));finite_component_records+=1
    for n in range(1,6):
        for mask in itertools.product([0,1],repeat=n):
            if all(mask):continue
            p={'matrices':[[['1']],[['1','1']],[[str(mask[a]) if a==b else '0' for b in range(n)] for a in range(n)]],'witnesses':[None,None,None]}
            check_record(g.generate('easy',template='q-68741',parameters=p));finite_component_records+=1
    for name,t in g.TEMPLATES.items():
        for slot,role in enumerate(t['roles']):
            if role!='rectangular':continue
            # Obtain one small eligible parameter baseline, then vary shape only.
            base=g.generate('easy',seed=0,template=name)['generation']['parameters']
            for j,other_role in enumerate(t['roles']):
                if other_role=='identity':base['matrices'][j]=[['1']];base['witnesses'][j]=None
                elif other_role=='diagonal':base['matrices'][j]=[['0']];base['witnesses'][j]=None
                elif other_role=='offdiagonal':
                    base['matrices'][j]=[['0','1'],['1' if t['counts'][j]==2 else '0','0']];base['witnesses'][j]=[1,2]
                else:
                    base['matrices'][j]=[['1','1']] if t.get('dense')==j or t.get('rectangular_patterns',{}).get(j)=='column_wrap' else [['1','0']];base['witnesses'][j]=None
            for r in range(1,6):
                for c in range(1,6):
                    if r==c:continue
                    p=copy.deepcopy(base)
                    p['matrices'][slot]=[['1']*c for _ in range(r)] if t.get('dense')==slot else g.rectangular_matrix(r,c,t.get('rectangular_patterns',{}).get(slot,'truncated'))
                    check_record(g.generate('easy',template=name,parameters=p));finite_component_records+=1
    # Explicit boundaries: all four classes overlap as required, including 1x1.
    for rows,want in [([['0']],{'zero':True,'square':True,'diagonal':True,'identity':False}),([['1']],{'zero':False,'square':True,'diagonal':True,'identity':True}),([['2']],{'zero':False,'square':True,'diagonal':True,'identity':False}),([['0','0']],{'zero':True,'square':False,'diagonal':False,'identity':False})]:
        assert g.properties(rows)==want and independent_properties(sp.Matrix(rows))==want
    # Public boundary instances exercise real response fields and worked prose.
    tiny={'matrices':[[['1']],[['1','1']],[['0']]],'witnesses':[None,None,None]}
    public_tiny=g.generate('easy',template='q-68741',parameters=tiny);check_record(public_tiny);add_native(public_tiny,'1x1 identity and zero diagonal overlap')
    for scalar in ['0','1']:
        p=copy.deepcopy(cases[0]['parameters']);p['matrices'][1]=[[scalar if i==j else '0' for j in range(3)] for i in range(3)]
        rec=g.generate('easy',template='q-11562',parameters=p);check_record(rec);add_native(rec,'diagonal criterion includes '+('zero' if scalar=='0' else 'identity'))
    # Incidental diagonal scalars and nonzero offdiagonal magnitude changes
    # never inflate task capacity, even when teaching notices change wording.
    pa=copy.deepcopy(cases[0]['parameters']);pb=copy.deepcopy(pa)
    pb['matrices'][0][0][1]='7';pb['matrices'][1][0][0]='-2'
    ra=g.generate('easy',template='q-11562',parameters=pa);rb=g.generate('easy',template='q-11562',parameters=pb)
    assert ra['generation']['parameter_fingerprint']==rb['generation']['parameter_fingerprint']
    assert ra['question'][':question/id']!=rb['question'][':question/id']
    mutation_count=0
    base=next(v for v in variants if v['generation']['template']=='q-11562')
    for mutation in ['stage','witness','key','control','conclusion','scope','bank-equivalence']:
        bad=copy.deepcopy(base);q=bad['question']
        if mutation=='stage':q[':question/worked-solution']=q[':question/worked-solution'].replace("It's a square matrix since it has the same number of rows and columns. ",'',1)
        elif mutation=='witness':q[':question/worked-solution']=re.sub(r'(\$\{[a-z]\}_\{)\d\d',r'\g<1>11',q[':question/worked-solution'],count=1)
        elif mutation=='key':
            f=q[':question/answer-fields'][0];f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])]
        elif mutation=='control':q[':question/problem']+='\x0c'
        elif mutation=='scope':q[':question/difficulty']=':question.difficulty/hard'
        elif mutation=='bank-equivalence':
            f=q[':question/answer-fields'][0];f[':answer-field/choices'][0][':answer/value']=f[':answer-field/choices'][1][':answer/value']
        else:q[':question/worked-solution']=q[':question/worked-solution'].rsplit('Therefore,',1)[0]+'Therefore, none of the given are diagonal matrices.'
        try:check_record(bad)
        except (AssertionError,ValueError):mutation_count+=1
        else:raise AssertionError('Mutation not rejected '+mutation)
    # Public explicit calls enforce all difficulty bounds, not just samplers.
    rejected=0
    for rec in variants:
        p=rec['generation']['parameters'];level=rec['question'][':question/difficulty'].split('/')[-1]
        for wrong in set(g.SUPPORTED_LEVELS)-{level}:
            try:g.generate(wrong,template=rec['generation']['template'],parameters=p)
            except ValueError:rejected+=1
            else:raise AssertionError('Cross-level workload accepted')
    # Direct changed-target test holds matrix entries fixed, changes a legitimate
    # witness to another nonzero offdiagonal cell, and checks printed operand.
    case=next(c for c in cases if c['source_id']=='q-11562');p=copy.deepcopy(case['parameters']);p['witnesses'][2]=[4,1]
    changed=g.generate('easy',template='q-11562',parameters=p,profile='raw-q-11562');check_record(changed)
    assert r'${l}_{41}=1\ne 0$' in changed['question'][':question/worked-solution']
    assert changed['question'][':question/id']!=originals[0]['question'][':question/id']
    assert changed['generation']['parameter_fingerprint']==originals[0]['generation']['parameter_fingerprint']
    # Defaults serve all six source-shaped families.
    default_coverage={l:sorted({g.generate(l,s)['generation']['template'] for s in range(120)}) for l in g.SUPPORTED_LEVELS}
    assert all(set(v)==set(g.TEMPLATES) for v in default_coverage.values())
    (HERE/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine=json.loads((HERE/'engine-report.json').read_text())
    baseline=json.loads((HERE/'baseline-hashes.json').read_text());assert all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in baseline.items()),'Registered baseline changed'
    current=[str(p.relative_to(ROOT)) for p in (ROOT/'generate/scratch/17592186087697').rglob('*') if p.is_file()]+['generate/scratch/17592186087697.py']
    assert set(current)==set(baseline),'Registered evidence files added/deleted'
    report={'pass':True,'database':'math','basis':2275,'lineage':src['lineage'],'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_coverage':{'original_questions':len(cases),'captured_originals':len(sources),'independent_inventory':0,'raw_exact_prompts':len(cases),'raw_exact_present_solutions':5,'present_solutions':5,'full_banks':6,'matched_options':option_count,'total_options':option_count,'matched_existing_correct_designations':designation_count,'existing_correct_designations':15,'missing_original_correct_designations':1,'missing_original_difficulties':1,'missing_original_solutions':1},'fidelity':fidelity,'generated_math_records':tested,'exhaustive_rendered_finite_component_records':finite_component_records,'generated_examples_per_level':12,'meaningful_sampled_tasks':{k:len(v) for k,v in unique.items()},'finite_semantic_capacities_per_template':capacities(),'capacity_notes':'Finite offdiagonal zero/nonzero masks for diagonal criteria; additional diagonal one/nonone masks for identity. Rectangular matrices count shape alone. Repeated equal-role matrix slots unordered. No labels, seeds, banks, diagonal values irrelevant to the criterion, or arbitrary nonzero magnitudes counted. Counts are per template; do not sum them as a deduplicated cross-template union.','slot_coverage':slot_coverage,'default_template_coverage':default_coverage,'mutation_regressions_rejected':mutation_count,'explicit_cross_level_rejections':rejected,'changed_target_fixed_entries':True,'overlap_and_1x1_checks':4,'native_grading':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':engine['documented_unresolved_checks'],'raw_missing_key_q7829':'Not gradable as captured; public raw evidence remains ineligible. Completed method profile independently keyed to D only.'},'registered_baseline_unchanged':True,'draft_script_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'registered_baseline_hashes':baseline,'authored_grade_uncertainty':'Only easy is observed. Moderate/hard split total inspected entries without new methods. No empirical MA grade calibration is claimed.','remaining_limits':['Raw q-7829 has no original key, level or solution; inference cannot count as original designation fidelity.','Authored moderate/hard inspection workload is a conservative design claim, not recovered difficulty evidence.','No human/native UI render inspection; shared UI TeX helper validates structure.'],'plot_rating':'none'}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    (HERE/'review.json').write_text(json.dumps({'original_replays':originals,'generated_variants':variants},indent=2)+'\n')
    md=['# Private draft review','Basis 2275. Raw original replay and authored generated variants are labeled separately.','']
    for case,rec in zip(cases,originals):md+=['## Original '+case['source_id'],'Raw profile; absent source attributes remain absent.','',g.markdown(rec),'']
    for rec in variants:
        gen=rec['generation'];md+=['## Authored '+rec['question'][':question/difficulty'].split('/')[-1]+' — '+gen['template']+' seed '+str(gen['seed']),'Authored grade calibration; source-shaped method bank.','',g.markdown(rec),'']
    (HERE/'review.md').write_text('\n'.join(md)+'\n')
    print(json.dumps({k:report[k] for k in ['pass','source_coverage','generated_math_records','meaningful_sampled_tasks','native_grading','registered_baseline_unchanged']},indent=2))
if __name__=='__main__':main()
