"""Step7 independent prompt readback, source fidelity and current native grading."""
import sys
sys.dont_write_bytecode=True
import copy
import hashlib
import functools
import importlib.util
import itertools
import json
from pathlib import Path
import re
import shutil
import subprocess
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('draft00870',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def ungroup(s):return s.replace(r'\left(','').replace(r'\right)','').strip()
@functools.lru_cache(maxsize=None)
def expr(s):return sp.sympify(ungroup(s))
def dimensions(s):
    a,b=re.split(r'\s*\\(?:times|cdot)\s*',s)
    return (expr(a),expr(b))
def value(answer):
    return None if answer[':answer/type'].endswith('/text') else dimensions(answer[':answer/value'])

def readback(rec):
    q=rec['question'];text=q[':question/problem'];sol=q[':question/worked-solution']
    assert set(rec['knowledge_point'])=={'id','db_id','title'}
    factors=re.findall(r'\$([A-Z])\$ is a\s*\$([^$]+)\$ matrix',text)
    assert len(factors)==2,text
    bylabel={label:dimensions(dim) for label,dim in factors}
    target=re.search(r'\$([A-Z]{2})\??\$',text)[1];a,b=target
    left,right=bylabel[a],bylabel[b]
    assert left[1]==right[0]
    correct=(left[0],right[1])
    ordering='forward' if [label for label,_ in factors]==list(target) else 'reverse'
    semantic=[str(x).replace(' ','') for x in (left[0],left[1],right[1])]
    fingerprint=hashlib.sha256(json.dumps([ordering,semantic],separators=(',',':')).encode()).hexdigest()
    assert rec['generation']['mathematical_fingerprint']==fingerprint
    for field in q[':question/answer-fields']:
        choices=field[':answer-field/choices']
        answer=next(x for x in choices if x[':answer/id']==field[':answer-field/correct'][1])
        if field[':answer-field/type'].endswith('/blank'):
            assert text.count('{{'+field[':answer-field/key']+'}}')==1
            assert len(choices)==1
            assert expr(answer[':answer/value'])==correct[0 if field[':answer-field/key']=='field-1' else 1]
        else:
            assert len(choices)==5
            objects=list(map(value,choices))
            assert len(set(objects))==len(objects)
            assert value(answer)==correct
            assert objects.count(correct)==1
    # Independently parse the actual displayed ordered dimension annotation.
    displays=re.findall(r'\$\$\s*([\s\S]*?)\s*\$\$',sol)
    assert len(displays)==1
    pattern=(r'\{([A-Z])\}_\{(.+?)\\times \\boxed\{\\text\{(.+?)\}\}\}'
             r'\{\\times \}_\{✓\}\{([A-Z])\}_\{\\boxed\{\\text\{(.+?)\}\}\\times (.+?)\}'
             r'=\{([A-Z]{2})\}_\{(.+?)\\times (.+?)\}')
    match=re.fullmatch(pattern,displays[0]);assert match,displays[0]
    la,m,n,lb,n2,p,out,om,op=match.groups()
    assert (la,lb,out)==(a,b,target)
    assert (expr(m),expr(n),expr(n2),expr(p),expr(om),expr(op))==(*left,*right,*correct)
    for inner,label,role in [(left[1],a,'column' if left[1]==1 else 'columns'),(right[0],b,'row' if right[0]==1 else 'rows')]:
        found=re.search(r'\$([^$]+)\$ '+role+r' in \$'+label+r'\.?\$',sol)
        assert found and expr(found[1])==inner,(sol,label,role)
    final=re.search(r'\$'+target+r'\$ is a \$([^$]+)\$ matrix:',sol)
    assert final and dimensions(final[1])==correct
    # Every operative prose stage stays in order and appears exactly once.
    phrases=['There is ' if left[1]==1 else 'There are ', 'Since the number of columns in ', 'equals the number of rows in ', 'are conformable for multiplication, and ', '\n\n$$']
    positions=[sol.index(s) for s in phrases];assert positions==sorted(positions)
    assert all(sol.count(s)==1 for s in phrases)
    for part in [text,sol,*[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]]:
        assert not any(ord(c)<32 and c not in '\n\t' for c in part)
    return correct

def native_checks(rec):
    checks=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        if f[':answer-field/type'].endswith('/radio'):
            checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if f[':answer-field/correct'][1]==a[':answer/id'] else 'rejected','purpose':'Complete displayed bank'} for a in f[':answer-field/choices'])
        else:
            ans=f[':answer-field/choices'][0][':answer/value']
            equivalent=str(sp.expand(expr(ans))) if '+' in ans else ans+'.0'
            if '+' in ans:equivalent='+'.join(reversed(ans.split('+')))
            for submitted,expected,purpose in [(ans,'accepted','canonical dimension fragment'),(equivalent,'accepted','legitimate reordered symbolic sum or decimal integer'),('('+ans+')+0','accepted','unevaluated exact equivalent'),('('+ans+')+1','rejected','wrong increment'),('0','rejected','impossible zero dimension')]:
                checks.append({'field_index':i,'submitted':submitted,'expected':expected,'purpose':purpose})
    return checks

def verify_immutable():
    before=json.loads((HERE/'reference/numeric-before.json').read_text())
    root=ROOT/'generate/scratch'
    paths=[root/'17592186100870.py',*sorted((root/'17592186100870').rglob('*')),*sorted((root/'__pycache__').glob('17592186100870.*.pyc'))]
    relative=[str(p.relative_to(ROOT)) for p in paths]
    assert relative==before['pathset'],'Numeric pathset changed'
    hashes={str(p.relative_to(ROOT)):sha(p) for p in paths if p.is_file()}
    assert hashes==before['files'],'Numeric source/evidence/bytecode changed'
    save('reference/numeric-recheck.json',{'passed':True,'files':len(hashes),'pathset_entries':len(relative),'hashes':hashes})

def provenance():
    path=ROOT/'generate/scratch/17592186059716-draft/reference/grader-build.json'
    shutil.copyfile(path,HERE/'reference/grader-build.json')
    data=json.loads(path.read_text());items={data['source']:data['source_sha256'],data['library']:data['library_sha256'],data['binary']:data['binary_sha256'],**data['engine_sources'],**data['dependencies']}
    assert len(items)==42
    assert all(sha(ROOT/p)==expected for p,expected in items.items())
    assert data['binary_sha256']=='33510bf3ac27a1eb28e9bad7b4121a22d2fa787026d3102268daa4ecf98b1617'
    save('reference/grader-provenance-recheck.json',{'passed':True,'actual_rechecked_files':len(items),'hashes':items})
    return ROOT/data['binary']

def main():
    verify_immutable();binary=provenance()
    original=ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186100870.json'
    assert original.read_bytes()==(HERE/'source.json').read_bytes()
    cases=[];fidelity=[];raws=[];review=[];normals=[];native=[];domains={};coverage={}
    for template,params in g.DEFAULTS.items():
        old=g.SOURCES[template];level=g.level_of(template)
        raw=g.generate(level,template=template,parameters=params,profile='raw-'+template)
        q=raw['question'];raws.append(raw)
        assert q[':question/problem']==g.normalize_prose(old[':question/problem'])
        for key in [':question/difficulty',':question/worked-solution']:
            assert (key in q)==(key in old),(template,key)
        if ':question/worked-solution' in old: assert q[':question/worked-solution']==g.normalize_prose(old[':question/worked-solution'])
        count=0;corrects=0
        for f in q[':question/answer-fields']:
            original_f=next(x for x in old[':question/answer-fields'] if x[':answer-field/key']==f[':answer-field/key'])
            expected=sorted((a[':answer/type'][':db/ident'],g.normalize_tex(a[':answer/value']) if a[':answer/type'][':db/ident'].endswith('/math') else a[':answer/value']) for a in original_f[':answer-field/choices'])
            actual=sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])
            assert actual==expected,(template,actual,expected)
            assert f[':answer-field/type']==original_f[':answer-field/type'][':db/ident']
            assert (':answer-field/correct' in f)==(':answer-field/correct' in original_f)
            if ':answer-field/correct' in original_f:
                a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
                assert a[':answer/value']==g.normalize_tex(original_f[':answer-field/correct'][':answer/value']);corrects+=1
            count+=len(actual)
        case={'source_id':template,'template':template,'level':level,'parameters':params,'profile':'raw-'+template,'authored_level_assignment':':question/difficulty' not in old}
        cases.append(case);fidelity.append({'source_id':template,'matched_values':count,'correct_designations_matched':corrects,'complete_bank':True,'raw_attribute_presence':True,'raw_exact_prompt':q[':question/problem']==old[':question/problem'],'solution_present':':question/worked-solution' in old,'raw_exact_solution_when_present':q[':question/worked-solution']==old[':question/worked-solution'] if ':question/worked-solution' in old else None})
        normal=g.generate(level,template=template,parameters=params);readback(normal);normals.append(normal)
        native.append(normal)
        if all(':answer-field/correct' in f for f in raw['question'][':question/answer-fields']):native.append(raw)
        review.extend(['## Original '+template+' (immutable evidence)\n\n'+g.markdown(raw),'### Normal original-parameter completion/repair\n\n'+g.markdown(normal)])
        accepted=0;rejected=0;slots={k:set() for k in params}
        # Exhaust the entire numeric domain for every default complete bank.
        triples=list(itertools.permutations(range(1,11),3))
        if template=='q-42379':triples.extend((m,n,m) for m in range(1,11) for n in range(1,11) if m!=n)
        for triple in triples:
            p=dict(zip(('m','n','p'),triple));rec=g.generate(level,template=template,parameters=p);readback(rec);accepted+=1
            for k,v in p.items():slots[k].add(v)
        # Opaque raw historical profiles still public and parameterized, with
        # whole-bank collision rejection separately enumerated.
        raw_valid=0;raw_reject=0
        for triple in triples:
            p=dict(zip(('m','n','p'),triple))
            try:g.generate(level,template=template,parameters=p,profile='raw-'+template);raw_valid+=1
            except ValueError as e:assert str(e).startswith('bank_collision:');raw_reject+=1
        domains[template]={'normal_tasks':accepted,'raw_eligible_banks':raw_valid,'raw_whole_bank_rejections':raw_reject}
        coverage[template]={k:sorted(v) for k,v in slots.items()};assert all(len(v)==10 for v in slots.values())
        # Each changed-role dimension checked with the others fixed.
        for slot in params:
            p=dict(params);p[slot]=next(x for x in range(1,11) if x not in p.values())
            if template=='q-42379' and slot=='n':p['p']=p['m']
            rec=g.generate(level,template=template,parameters=p);readback(rec);native.append(rec)
        variants=[g.generate(level,seed=41+i,template=template) for i in range(2)]
        for rec in variants:readback(rec);review.append('### Generated variant\n\n'+g.markdown(rec))
        normals.extend(variants);native.extend(variants)
    for template in ['symbolic-radio','symbolic-blank']:
        for triple in itertools.product(range(1,7),repeat=3):
            p=dict(zip(('m','n','p'),(f'{v}+{n}' for v,n in zip(('r','s','t'),triple))))
            rec=g.generate('hard',template=template,parameters=p);readback(rec)
        domains[template]={'normal_tasks':216}
        for i in range(3):
            rec=g.generate('hard',seed=90+i,template=template);readback(rec);normals.append(rec);native.append(rec);review.append('## Authored hard symbolic variant\n\n'+g.markdown(rec))
    # No metadata-only checks: mutations of printed stages must be caught.
    mutations=[]
    for label,change in [('swapped display labels',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('{P}','{@}').replace('{Q}','{P}').replace('{@}','{Q}'))),('wrong boxed inner',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace(r'\text{3}',r'\text{9}',1))),('stale final prose',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('$4\\times 7$','$9\\times 7$'))),('control character',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem']+'\f'))]:
        bad=copy.deepcopy(g.generate('easy',template='q-320315',parameters=g.DEFAULTS['q-320315']));change(bad)
        try:readback(bad)
        except (AssertionError,ValueError):mutations.append(label)
        else:raise AssertionError('Mutation not caught: '+label)
    assert len(mutations)==4
    invalid=0
    for level,p in [('easy',dict(m=0,n=2,p=3)),('moderate',dict(m=11,n=2,p=3)),('easy',dict(m=2.0,n=3,p=4)),('hard',dict(m='r+0',n='s+2',p='t+3')),('hard',dict(m='r+7',n='s+2',p='t+3')),('hard',dict(m='r+1',n='r+2',p='t+3'))]:
        try:g.generate(level,parameters=p)
        except ValueError:invalid+=1
    assert invalid==6
    default_coverage={level:sorted({g.generate(level,i)['generation']['template'] for i in range(250)}) for level in g.SUPPORTED_LEVELS}
    for level,templates in default_coverage.items():assert set(templates)==set(t for t in list(g.SOURCES)+['symbolic-radio','symbolic-blank'] if g.level_of(t)==level)
    square_shapes={g.generate('easy',i,template='q-42379')['generation']['parameters']['m']==g.generate('easy',i,template='q-42379')['generation']['parameters']['p'] for i in range(100)}
    assert square_shapes=={True,False}
    try:g.generate('hard',template='symbolic-radio',profile='raw-symbolic-radio')
    except ValueError:invalid+=1
    else:raise AssertionError('Authored template accepted nonexistent source profile')
    catalog={}
    for level, triples in [('easy',list(itertools.permutations(range(1,11),3))+[(m,n,m) for m in range(1,11) for n in range(1,11) if m!=n]),('moderate',list(itertools.permutations(range(1,11),3))),('hard',list(itertools.product(range(1,7),repeat=3)))]:
        catalog[level]={'meaningful_tasks':len(triples),'notation_bank_layout_aliases_counted':False,'domain':'m,n,p in1..10 pairwise distinct; easy additionally m=p not n' if level!='hard' else 'r+a,s+b,t+c, offsets1..6; symbolic general formulas'}
    save('semantic-catalog.json',catalog)
    # Seed/order independence for fixed parameters; math identity also excludes banks.
    for rec in normals:
        meta=rec['generation'];level=rec['question'][':question/difficulty'].split('/')[-1]
        other=g.generate(level,999,meta['template'],parameters=meta['parameters'],profile=meta['profile'])
        assert rec['question'][':question/id']==other['question'][':question/id']
        assert meta['mathematical_fingerprint']==other['generation']['mathematical_fingerprint']
    save('source-cases.json',cases);save('source-fidelity.json',fidelity);save('domains.json',domains);save('slot-coverage.json',coverage)
    save('independent-inventory.json',{'database':g.SNAPSHOT['database'],'basis':g.SNAPSHOT['basis'],'lineage':g.SNAPSHOT['lineage'],'questions':[]})
    save('review.json',{'raw_replays':raws,'generated':normals});(HERE/'review.md').write_text('\n\n---\n\n'.join(review))
    save('engine-input.json',[{'label':str(i),'record':rec,'checks':native_checks(rec)} for i,rec in enumerate(native)])
    run=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
    (HERE/'engine.log').write_text(run.stdout+run.stderr);assert run.returncode==0,run.stderr
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    verify_immutable();provenance()
    results={'status':'pass','source_basis':2275,'MA_sources':11,'independent_inventory':0,'matched_complete_source_banks':11,'matched_source_values':sum(x['matched_values'] for x in fidelity),'matched_correct_designations':sum(x['correct_designations_matched'] for x in fidelity),'raw_exact_prompts':sum(x['raw_exact_prompt'] for x in fidelity),'raw_exact_present_solutions':sum(x['raw_exact_solution_when_present'] is True for x in fidelity),'present_source_solutions':sum(x['solution_present'] for x in fidelity),'source_missing_correct_fields':2,'source_missing_ratings':2,'source_missing_solutions':2,'source_error_display_labels':1,'normal_numeric_exhaustive_checks':sum(x['normal_tasks'] for k,x in domains.items() if not k.startswith('symbolic')),'hard_domain_tasks':216,'hard_layout_checks':432,'scope_limit':'Authored hard symbolic dimensions; classification is a design claim. No matrix multiplication, equation solving, chain products or entry counting.','mutations_caught':mutations,'invalid_inputs_rejected':invalid,'default_template_coverage':default_coverage,'native_grading':{k:v for k,v in engine.items() if k!='records'},'generator_sha256':sha(HERE.with_suffix('.py'))}
    save('validation.json',results);print(json.dumps(results,indent=2))

if __name__=='__main__':main()
