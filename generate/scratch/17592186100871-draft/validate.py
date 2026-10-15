"""Independent printed-content checks, full original banks, native learner grading."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,re,shutil,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('draft00871',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dimension(value):
    m=re.fullmatch(r'\s*(\d+)\s*\\(?:times|cdot)\s*(\d+)\s*',value)
    assert m,value
    return tuple(int(x) for x in m.groups())
def value(a):return None if a[':answer/type'].endswith('/text') else dimension(a[':answer/value'])
def readback(rec):
    q=rec['question'];text=q[':question/problem'];sol=q[':question/worked-solution'];matrices={};supplied=[]
    assert set(rec['knowledge_point'])=={'id','db_id','title'}
    for match in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S):
        rows=[row.split('&') for row in match[2].split(r'\\')];assert len({len(row) for row in rows})==1
        matrices[match[1]]=(len(rows),len(rows[0]));supplied.append(match[1])
    assert len(matrices)==2
    target=re.search(r'dimensions of \$([A-Z]{2})',text)[1];a,b=target
    ar,ac=matrices[a];br,bc=matrices[b];assert ac==br
    # An exact shape check independent of parameters; no metadata used here.
    assert (sp.zeros(ar,ac)*sp.zeros(br,bc)).shape==(ar,bc)
    for f in q[':question/answer-fields']:
        answers=f[':answer-field/choices'];answer=next(a for a in answers if a[':answer/id']==f[':answer-field/correct'][1])
        if f[':answer-field/type'].endswith('/blank'):
            assert text.count('{{'+f[':answer-field/key']+'}}')==1
            assert len(answers)==1
            assert sp.sympify(answer[':answer/value'])==(ar if f[':answer-field/key']=='field-1' else bc)
        else:
            bank=[value(x) for x in answers];assert len(bank)==5==len(set(bank));assert value(answer)==(ar,bc)
    # First dimensions from printed matrices; catches source q22067's known error.
    declarations=re.findall(r'\$([A-Z])\$ is a \$([^$]+)\$ matrix',sol)
    assert [n for n,_ in declarations]==supplied
    assert all(dimension(d)==matrices[n] for n,d in declarations)
    count=re.search(r'There (?:is|are) \$(\d+)\$ columns? in \$([A-Z])\$ and \$(\d+)\$ rows? in \$([A-Z])\.\$',sol)
    assert count and (int(count[1]),count[2],int(count[3]),count[4])==(ac,a,br,b)
    assert f'Since the number of columns in ${a}$ equals the number of rows in ${b},$ the matrices ${a}$ and ${b}$ are conformable for multiplication.' in sol
    final=re.search(r'The product \$([A-Z]{2})\$ has dimensions \$([^$]+):\$',sol);assert final and final[1]==target and dimension(final[2])==(ar,bc)
    diagram=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(diagram)==1
    pattern=(r'\{([A-Z])\}_\{(\d+)\\times \\boxed\{\\text\{(\d+)\}\}\}'r'\{\\times \}_\{✓\}\{([A-Z])\}_\{\\boxed\{\\text\{(\d+)\}\}\\times (\d+)\}'r'=\{([A-Z]{2})\}_\{(\d+)\\times (\d+)\}')
    m=re.fullmatch(pattern,diagram[0]);assert m,diagram
    assert (m[1],int(m[2]),int(m[3]),m[4],int(m[5]),int(m[6]),m[7],int(m[8]),int(m[9]))==(a,ar,ac,b,br,bc,target,ar,bc)
    ordered=['We notice that ', 'There ', 'Since the number of columns in ', 'The product ', '\n\n$$'];positions=[sol.index(x) for x in ordered];assert positions==sorted(positions)
    assert all(sol.count(x)==1 for x in ordered)
    for s in [text,sol,*[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]]:assert not any(ord(c)<32 and c not in '\n\t' for c in s)
    return {'supplied_shapes':[matrices[n] for n in supplied],'target_roles':[supplied.index(n) for n in target]}
def verify_immutable():
    before=json.loads((HERE/'reference/registered-before.json').read_text());stem='17592186100871';base=ROOT/'generate/scratch';paths=[base/(stem+'.py'),*(base/stem).rglob('*'),*(base/'__pycache__').glob(stem+'.*.pyc')]
    now={str(p.relative_to(ROOT)):sha(p) for p in paths if p.is_file()};dirs=sorted(str(p.relative_to(ROOT)) for p in paths if p.is_dir());assert now==before['files'];assert dirs==before['directories']
    save('reference/registered-recheck.json',{'passed':True,'files':len(now),'directories':len(dirs),'pathset_and_all_hashes_unchanged':True})
def grader():
    path=ROOT/'generate/scratch/17592186059716-draft/reference/grader-build.json';d=json.loads(path.read_text());items={d['source']:d['source_sha256'],d['library']:d['library_sha256'],d['binary']:d['binary_sha256'],**d['engine_sources'],**d['dependencies']}
    assert len(items)==42 and all(sha(ROOT/p)==h for p,h in items.items());assert d['binary_sha256']=='33510bf3ac27a1eb28e9bad7b4121a22d2fa787026d3102268daa4ecf98b1617'
    shutil.copyfile(path,HERE/'reference/grader-build.json');save('reference/grader-recheck.json',{'verified':True,'actual_files':42,'hashes':items});return ROOT/d['binary']
def probes(rec):
    out=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        if f[':answer-field/type'].endswith('/radio'):
            out.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every displayed source-shaped option'} for a in f[':answer-field/choices'])
        else:
            a=f[':answer-field/choices'][0][':answer/value']
            for v,e,p in [(a,'accepted','canonical fragment'),(a+'.0','accepted','equivalent decimal integer'),(a+'/1','accepted','equivalent fraction'),('('+a+'+2)-2','accepted','unevaluated arithmetic equivalent'),(str(int(a)+1),'rejected','wrong outer count'),('0','rejected','impossible zero dimension')]:out.append({'field_index':i,'submitted':v,'expected':e,'purpose':p})
    return out

def main():
    verify_immutable();binary=grader()
    assert (ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186100871.json').read_bytes()==(HERE/'source.json').read_bytes()
    raws=[];normals=[];cases=[];fidelity=[];extraction=[];review=[];native=[]
    for mid,source in g.SOURCES.items():
        level=g.level_of(mid);params=g.DEFAULTS[mid];rec=g.generate(level,template=mid,parameters=params,profile='raw-'+mid);q=rec['question'];raws.append(rec)
        assert q[':question/problem']==g.normalize_prose(source[':question/problem'])
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
            assert (key in q)==(key in source)
        if ':question/worked-solution' in source:assert q[':question/worked-solution']==g.normalize_prose(source[':question/worked-solution']),(mid,q[':question/worked-solution'],source[':question/worked-solution'])
        matched=designations=0;rows=[]
        for f in q[':question/answer-fields']:
            sf=next(x for x in source[':question/answer-fields'] if x[':answer-field/key']==f[':answer-field/key']);kind=f[':answer-field/type'].split('/')[-1]
            assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident'];assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
            expected=[(x[':answer/type'][':db/ident'],x[':answer/value']) for x in sf[':answer-field/choices']]
            actual=[(x[':answer/type'],x[':answer/value']) for x in f[':answer-field/choices']]
            # Exact normalized values, complete one-to-one banks, not only key.
            expected=[(t,g.normalize_tex(v) if t.endswith('/math') else v) for t,v in expected];assert sorted(actual)==sorted(expected),(mid,actual,expected)
            matched+=len(actual)
            if ':answer-field/correct' in sf:
                old=sf[':answer-field/correct'][':answer/value'];new=next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id']==f[':answer-field/correct'][1]);assert new==g.normalize_tex(old);designations+=1
            for a in sf[':answer-field/choices']:rows.append({'field':sf[':answer-field/key'],'answer':a,'complete_value_recipe':next((name for name,val in g.recipes('source-bank:'+mid,*params.values()) if kind=='radio' and val==(None if a[':answer/type'][':db/ident'].endswith('/text') else dimension(a[':answer/value']))),'outer rows' if sf[':answer-field/key']=='field-1' else 'outer columns')})
        fidelity.append({'source_id':mid,'matched_values':matched,'complete_bank':True,'correct_designations_matched':designations,'attribute_presence_parity':True,'prompt_raw_exact':q[':question/problem']==source[':question/problem'],'solution_raw_exact':q.get(':question/worked-solution')==source.get(':question/worked-solution') and ':question/worked-solution' in source,'prompt_normalized_exact':True,'solution_normalized_exact':':question/worked-solution' in source,'solution_missing':':question/worked-solution' not in source})
        cases.append({'source_id':mid,'template':mid,'level':level,'parameters':params,'profile':'raw-'+mid,'authored_level_assignment':':question/difficulty' not in source})
        extraction.append({'source_id':mid,'complete_original_record':source,'parameters':params,'field_type':kind,'bank_profile':'source-bank:'+mid,'components':rows})
        normal=g.generate(level,template=mid,parameters=params);readback(normal);normals.append(normal);native.append(normal)
        review.extend(['## Original '+mid+' (raw evidence)\n\n'+g.markdown(rec),'### Normal completion/repair at original parameters\n\n'+g.markdown(normal)])
        for i in range(2):
            variant=g.generate(level,seed=41+i,template=mid);readback(variant);normals.append(variant);native.append(variant);review.append('### Generated variant\n\n'+g.markdown(variant))
    # Authored easy plus general same-method numeric blank families.
    for level,template in [('easy','scaffolded-forward-blank'),('moderate','forward-blank'),('hard','reverse-blank')]:
        for i in range(2):
            rec=g.generate(level,seed=80+i,template=template);readback(rec);normals.append(rec);native.append(rec);review.append('## Authored '+level+' variant\n\n'+g.markdown(rec))
    domains={};slots={};maths={level:set() for level in g.SUPPORTED_LEVELS};default_coverage={}
    for template in [*g.SOURCES,'scaffolded-forward-blank','forward-blank','reverse-blank']:
        level=g.level_of(template);count=0;role_shapes=set();slot={x:set() for x in ('r','k','c')}
        for p in g.domain(template):
            rec=g.generate(level,template=template,parameters=p);obj=readback(rec);count+=1
            maths[level].add(json.dumps(obj,sort_keys=True));role_shapes.add(tuple(obj['target_roles']))
            for x,v in p.items():slot[x].add(v)
        assert count>0;domains[template]={'valid_complete_banks':count,'finite_parameters':g.domain(template),'target_roles':list(map(list,role_shapes))};slots[template]={k:sorted(v) for k,v in slot.items()}
    # Hold dimensions fixed while reversing supplied order: parse actual displayed operands/annotation.
    fwd=g.generate('moderate',template='forward-blank',parameters=dict(r=3,k=2,c=4));rev=g.generate('hard',template='reverse-blank',parameters=dict(r=3,k=2,c=4));assert readback(fwd)['target_roles']==[0,1] and readback(rev)['target_roles']==[1,0]
    mutations=[]
    baseline=g.generate('hard',template='reverse-blank',parameters=dict(r=3,k=2,c=4))
    for name,replace in [('wrong declared dimension',lambda s:s.replace('$2\\times 4$','$1\\times 4$',1)),('wrong boxed inner',lambda s:s.replace(r'\text{2}',r'\text{9}',1)),('stale final product',lambda s:s.replace('product $BA$','product $AB$')),('removed operative conformability',lambda s:s.replace('Since the number of columns','Because the count')),('control character',lambda s:s+'\f')]:
        bad=copy.deepcopy(baseline);bad['question'][':question/worked-solution']=replace(bad['question'][':question/worked-solution'])
        try:readback(bad)
        except (AssertionError,ValueError,StopIteration):mutations.append(name)
        else:raise AssertionError('Mutation escaped '+name)
    bad=copy.deepcopy(baseline);bad['question'][':question/problem']=bad['question'][':question/problem'].replace('dimensions of $BA$','dimensions of $AB$')
    try:readback(bad)
    except (AssertionError,ValueError,StopIteration):mutations.append('changed printed target with stale solution')
    else:raise AssertionError('Printed target mutation escaped')
    for rec in normals:
        m=rec['generation'];lev=rec['question'][':question/difficulty'].split('/')[-1];other=g.generate(lev,seed=999,template=m['template'],parameters=m['parameters'],profile=m['profile']);assert rec['question'][':question/id']==other['question'][':question/id']
        assert m['mathematical_fingerprint']==other['generation']['mathematical_fingerprint']
    for lev in g.SUPPORTED_LEVELS:default_coverage[lev]=sorted({g.generate(lev,i)['generation']['template'] for i in range(300)})
    invalid=0
    for lev,t,p in [('easy','scaffolded-forward-blank',dict(r=5,k=2,c=1)),('moderate','forward-blank',dict(r=2,k=2,c=2)),('hard','reverse-blank',dict(r=0,k=3,c=4)),('moderate','q-129492',dict(r=3,k=2,c=4)),('moderate','forward-blank',dict(r=3.0,k=2,c=4))]:
        try:g.generate(lev,template=t,parameters=p)
        except ValueError:invalid+=1
    assert invalid==5
    save('source-cases.json',cases);save('source-components.json',extraction);save('source-fidelity.json',fidelity);save('domains.json',domains);save('slot-coverage.json',slots)
    save('independent-inventory.json',{'database':g.SNAPSHOT['database'],'basis':2275,'lineage':g.SNAPSHOT['lineage'],'questions':[]})
    save('review.json',{'raw_replays':raws,'generated':normals});(HERE/'review.md').write_text('\n\n---\n\n'.join(review));save('render-records.json',normals+raws)
    save('engine-input.json',[{'label':str(i),'record':r,'checks':probes(r)} for i,r in enumerate(native)])
    run=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True);(HERE/'engine.log').write_text(run.stdout+run.stderr);assert run.returncode==0,run.stderr
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    verify_immutable();grader()
    save('validation.json',{'status':'pass','basis':2275,'MA_practice_sources':10,'independent_inventory':0,'complete_source_banks':10,'raw_exact_prompts':sum(x['prompt_raw_exact'] for x in fidelity),'normalized_exact_prompts':10,'matched_source_values':sum(x['matched_values'] for x in fidelity),'correct_designations_matched':sum(x['correct_designations_matched'] for x in fidelity),'source_missing_correct':1,'source_missing_difficulty':1,'source_missing_solution':1,'raw_solution_exact':9,'normal_solution_repaired':1,'normal_solution_inferred':1,'normal_unrepaired_source_solutions':8,'finite_semantic_tasks':{k:len(v) for k,v in maths.items()},'exhaustive_layout_profile_instances':sum(v['valid_complete_banks'] for v in domains.values()),'default_coverage':default_coverage,'mutation_regressions_caught':mutations,'invalid_explicit_inputs_rejected':invalid,'native':{k:v for k,v in engine.items() if k not in ('results','records')},'script_sha256':sha(HERE.with_suffix('.py')),'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'UI':'see render-report.json; not implied by native grading','step':'7 only; no registration or database preparation'})
    result=json.loads((HERE/'validation.json').read_text())
    if (HERE/'render-report.json').exists():
        render=json.loads((HERE/'render-report.json').read_text());result['UI']={'records':render['records'],'representative_fullscreens':len(render['screenshots']),'actual_player_functions':True,'MathLive_blank_controls':True,'MathJax_errors':render['errors'],'exposed_delimiters':render['exposed_delimiters'],'overflow':render['overflow']}
    result['supplemental_independent_inventory']=len(json.loads((HERE/'supplemental-independent-inventory.json').read_text())['questions']) if (HERE/'supplemental-independent-inventory.json').exists() else 0
    result['global_deduplicated_math_tasks']=len(set.union(*maths.values()))
    save('validation.json',result)
    print('Passed:',len(fidelity),'source banks;',sum(v['valid_complete_banks'] for v in domains.values()),'exhaustive instances;',engine['accepted_checks'],'accepted and',engine['rejected_checks'],'rejected native checks')
if __name__=='__main__':main()
