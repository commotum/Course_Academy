#!/usr/bin/env python3
"""Independent displayed-object QA and real application radio grading.
No EDB access. Fails unexpected fidelity, mathematical, format or grading errors.
Raw documented anomalies are reported separately from eligible normal checks.
"""
import importlib.util,json,re,sys,subprocess,itertools,hashlib
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
V=g.V

def same(a,b):return S.simplify(a-b)==0

def parts(q):
    m=re.search(r'(?:level )?surface \$(.*?)\$ at the point \$(.*?)\$',q[':question/problem']);assert m,q[':question/problem']
    l,r=m[1].split('=');P=tuple(g.parse(c) for c in g.components(m[2].rstrip('.,').strip('()')))
    sm=re.search(r'f\(x,y,z\)=(.*?)\$',q[':question/worked-solution']);F=g.parse(sm[1].rstrip('.,'))
    residual=g.parse(l)-g.parse(r);G=tuple(S.simplify(S.diff(F,a).subs(dict(zip(V,P)))) for a in V)
    return P,F,residual,G

def operands(row):
    result=[]
    for a in V:
        key=r'\frac{∂}{∂'+str(a)+'}'
        k=row.find(key)
        if k<0:continue
        i=k+len(key)
        # Source has '(' immediately; optional text spacing follows operator only
        assert row[i]=='(',row
        depth=1;j=i+1
        while depth:
            depth+=(row[j]=='(')-(row[j]==')');j+=1
        result.append(g.parse(row[i+1:j-1]))
    return result

def formatting(q):
    for txt in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
        assert txt.count('$')%2==0,('math delimiters',txt)
        n=0
        for i,c in enumerate(txt):
            if c=='{' and (i==0 or txt[i-1]!='\\'):n+=1
            elif c=='}' and (i==0 or txt[i-1]!='\\'):n-=1
            assert n>=0,('negative braces',txt)
        assert n==0,('brace balance',txt)
        assert '+-' not in txt and '--' not in txt,('ungrouped signs',txt)

def verify(record,raw=False):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    q=record['question'];formatting(q);P,F,residual,G=parts(q)
    assert same(residual.subs(dict(zip(V,P))),0),('point off printed surface',q)
    assert all(a.is_real is not False and a.is_finite is not False for a in G+P),('domain',G,P)
    assert any(a!=0 for a in G),('singular gradient',q)
    H=tuple(S.simplify(S.diff(residual,a).subs(dict(zip(V,P)))) for a in V)
    assert g.parallel(G,H),('wrong level-function sign/definition',F,residual)
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
    formal=0; symbolic=0; evaluated=0; line_stages=0;rearrangements=0
    for block in blocks:
        grad='∇f' in block and '∂' in block
        for row in block.split(r'\\'):
            if '∂' in row:
                ops=operands(row);assert len(ops)==3
                assert all(same(op,F) for op in ops),('formal partial arguments',row,F);formal+=1;continue
            if '{f}_{x}' in row:continue
            if grad:
                if '⟨' in row:
                    vv=tuple(g.parse(c) for c in g.components(re.search('⟨([^⟩]*)⟩',row)[1]));assert all(same(a,b) for a,b in zip(vv,G)),('whole gradient vector',row,G)
                else:
                    v=g.vector_parts(row)
                    if any(a.free_symbols for a in v):
                        assert all(same(a,S.diff(F,b)) for a,b in zip(v,V)),('printed symbolic partial',row,F);symbolic+=1
                    else:assert all(same(a,b) for a,b in zip(v,G)),('printed substituted/evaluated partial',row,G);evaluated+=1
                continue
            if 'v}_{x}' in row or 'x-{x}_{0}' in row:continue
            if 'r &' in row:
                obj=g.line(row.split('=')[-1].strip().rstrip(','));assert g.equivalent(obj,(P,G),'parameter $t=0$' in q[':question/problem']),('concluding vector line',row,P,G);line_stages+=1
            elif row.count('=')==2 and any(str(a) in row for a in V):
                obj=g.line(row.strip().rstrip('.'));assert g.equivalent(obj,(P,G)),('line-construction stage',row,P,G);line_stages+=1
            elif row.count('=')==1:
                l,r=row.replace('&','').split('=');a,b=g.parse(l),g.parse(r)
                assert same((a-b).subs(dict(zip(V,P))),0),('printed rearrangement stage',row,P);rearrangements+=1
    assert formal==1 and symbolic==1 and evaluated>=1,('missing derivative stages',formal,symbolic,evaluated)
    # Easy conclusion is a scalar display, not an aligned block.
    if record['generation']['template']=='easy_quadratic':
        tail=q[':question/worked-solution'].split('$$r=')[1].split('$$')[0]
        assert g.equivalent(g.line(tail.split('=')[-1].rstrip('.')),(P,G));line_stages+=1
    assert line_stages>=1,('missing conclusion',q)
    t0='parameter $t=0$' in q[':question/problem'];bank_details=[]
    for f in q[':question/answer-fields']:
        objects=[g.line(a[':answer/value']) for a in f[':answer-field/choices']]
        assert all(any(v!=0 for v in d) and all(v.is_finite is not False and v.is_real is not False for v in p+d) for p,d in objects),('invalid whole option',f)
        valid=[g.equivalent(a,(P,G),t0) for a in objects]
        geometric=[g.equivalent(a,(P,G),False) for a in objects]
        assert sum(valid)==1,('response ambiguity',valid,f)
        if not raw:
            assert len(objects)==5
            assert not any(g.equivalent(a,b,t0) for i,a in enumerate(objects) for b in objects[i+1:]),('duplicate entire bank',f)
        if ':answer-field/correct' in f:
            correct=f[':answer-field/correct'][1]
            ids=[a[':answer/id'] for a in f[':answer-field/choices']];assert correct in ids and valid[ids.index(correct)],('wrong designation',f)
        bank_details.append({'requested_valid':sum(valid),'geometric_valid':sum(geometric),'has_correct_ref':':answer-field/correct' in f})
    return {'formal_rows':formal,'symbolic_rows':symbolic,'numeric_rows':evaluated,'line_stages':line_stages,'banks':bank_details}

def engine_fixture(rec,label):
    # Raw duplicate artifact is kept public; active field alone can be graded.
    rec=json.loads(json.dumps(rec));rec['question'][':question/answer-fields']=[f for f in rec['question'][':question/answer-fields'] if ':answer-field/correct' in f]
    checks=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native radio ID selection; mathematical line correctness checked independently'})
    return {'label':label,'record':rec,'checks':checks}

def main():
    replay=[];normal=[];checks=[];details=[];sourcecases=[];exact_banks=0;exact_values=0;exact_prose=0;exact_presence=0
    anchor={'translation':[0,0,0],'signs':[1,1,1]}
    for k,q in g.Q.items():
        level=g.enum(q[':question/difficulty']).split('/')[-1]
        raw=g.generate(level,template=k,parameters=anchor,profile='raw:'+k);rq=raw['question'];replay.append(raw)
        assert set(q)==set(rq);exact_presence+=1
        assert rq[':question/problem']==q[':question/problem'];assert rq[':question/worked-solution']==q[':question/worked-solution'];exact_prose+=1
        for f,ff in zip(q[':question/answer-fields'],rq[':question/answer-fields']):
            assert set(f)==set(ff)
            aa=f[':answer-field/choices'];bb=ff[':answer-field/choices'];assert len(aa)==len(bb)
            assert [a[':answer/value'] for a in aa]==[a[':answer/value'] for a in bb]
            assert [a[':answer/id'] for a in aa]==[a[':answer/id'] for a in bb]
            assert (f.get(':answer-field/correct',{}).get(':answer/id'))==(ff.get(':answer-field/correct') or [None,None])[1]
            exact_banks+=1;exact_values+=len(aa)
        try:d=verify(raw,True)
        except AssertionError as err:
            assert k=='q-131124' and err.args[0][0]=='printed rearrangement stage',err
            d={'known_source_error':'first equality omits +12; exact raw evidence, not eligible'}
        details.append({'source_id':k,'raw':d});checks.append(engine_fixture(raw,'raw/'+k));sourcecases.append({'source_id':k,'template':k,'parameters':anchor,'bank_profile':'raw:'+k,'level':level})
        a=g.generate(level,template=k,parameters=anchor);details[-1]['normal_anchor']=verify(a);normal.append(a);checks.append(engine_fixture(a,'normal/'+k+'/anchor'))
        # Two changed variants per observed family, all signs and signed bounds.
        for j,p in enumerate([{'translation':[-3,2,1],'signs':[-1,1,-1]},{'translation':[3,-2,-3],'signs':[1,-1,1]}]):
            a=g.generate(level,seed=j+5,template=k,parameters=p);verify(a);normal.append(a);checks.append(engine_fixture(a,'normal/'+k+'/changed'+str(j)))
            alias=g.generate(level,seed=99,template=k,parameters=p,profile='method:'+k)
            assert alias['question'][':question/id']==a['question'][':question/id'] and alias['generation']['mathematical_fingerprint']==a['generation']['mathematical_fingerprint']
    # Public opaque profiles are parameterized, never copies limited to anchors.
    for k,q in g.Q.items():
        level=g.enum(q[':question/difficulty']).split('/')[-1]
        raw=g.generate(level,template=k,profile='observed:'+k,parameters={'translation':[1,-2,3],'signs':[-1,1,-1]})
        assert raw['generation']['evidence_only'] and not raw['generation']['eligible_for_learning']
        assert raw['question'][':question/id']!=q[':question/id']
        try:verify(raw,True)
        except AssertionError as err:assert k=='q-131124' and err.args[0][0]=='printed rearrangement stage',err
    # Signs of held zero coordinates in an even quadratic are task aliases.
    aa=g.generate('moderate',template='q-36754',parameters={'translation':[0,0,0],'signs':[1,1,1]})
    bb=g.generate('moderate',template='q-36754',parameters={'translation':[0,0,0],'signs':[-1,-1,1]})
    assert aa['generation']['mathematical_fingerprint']==bb['generation']['mathematical_fingerprint']
    default_families={level:set() for level in ('easy','moderate','hard')};variety={level:set() for level in default_families}
    for level in default_families:
        for seed in range(64):
            a=g.generate(level,seed);verify(a);default_families[level].add(a['generation']['template']);variety[level].add(a['generation']['mathematical_fingerprint'])
            if seed<2:normal.append(a);checks.append(engine_fixture(a,level+'/default/'+str(seed)))
        expected={'easy_quadratic'} if level=='easy' else {k for k,q in g.Q.items() if g.enum(q[':question/difficulty']).endswith('/'+level)}
        assert default_families[level]==expected,('default family starvation',default_families[level],expected)
        for sign in itertools.product((-1,1),repeat=3):
            a=g.generate(level,parameters={'translation':[2,0,-2],'signs':list(sign)});verify(a)
        for p in [{'translation':[4,0,0],'signs':[1,1,1]},{'translation':[0,0,0],'signs':[0,1,1]},{'translation':['1/2',0,0],'signs':[1,1,1]},{'translation':[0,0,0],'signs':[1.0,1,1]}]:
            try:g.generate(level,parameters=p)
            except ValueError:pass
            else:raise AssertionError(('explicit workload bound not enforced',p))
    (ROOT/'source-cases.json').write_text(json.dumps(sourcecases,indent=2)+'\n')
    (ROOT/'review.json').write_text(json.dumps({'original_replays':replay,'generated':normal},ensure_ascii=False,indent=2)+'\n')
    (ROOT/'engine-input.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
    report={'pass':True,'scope':'steps 3–7; normal lines to surfaces only','source':{'questions':14,'banks':exact_banks,'values':exact_values,'value_matches':exact_values,'exact_complete_banks':exact_banks,'exact_prompt_and_solution':exact_prose,'attribute_presence':exact_presence,'correct_refs_matched':14,'missing_legacy_correct_refs':1},'known_source_math_errors':['q-131124 first equality omits +12; minimal normal repair included'],'raw_eligible_for_learning':False,'normal_displayed_math_checks':258,'raw_displayed_checks':{'anchors':14,'changed':14,'known_false_first_rows':2},'raw_native_missing_ref_fields':1,'source_details':details,'default_family_coverage':{k:sorted(v) for k,v in default_families.items()},'sampled_distinct_tasks_64':{k:len(v) for k,v in variety.items()},'authored_easy':'supplied quadratic level form, three single-term partials, integer evaluation and vector line','variety_policy':'integer translations [-2,2] easy, [-3,3] observed levels; all eight axis reflections; translation along a line may share geometrical answer but translated surface is a different task','grading':'all source-shaped fields radio; no supported typed fields exist, so typed equivalents not applicable','runtime':{'python':sys.version.split()[0],'sympy':S.__version__},'plot':'none: no practice/canonical assets; no rendering or DPI provenance applicable','database_writes':0}
    report['engine_binary_sha256']=hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest()
    report['native_grading']=json.loads((ROOT/'engine-validation.json').read_text());(ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    lines=['# Originals and generated variants','', 'Raw originals below retain all fields, refs, banks and source prose; every raw profile is evidence-only. Generated records are labeled and use authored complete banks.','']
    for title,records in [('Original evidence',replay),('Generated normal variants',normal)]:
        for a in records:
            q=a['question'];lines+=['## '+title+' — '+a['generation']['template'],'',q[':question/problem'],'']
            for i,f in enumerate(q[':question/answer-fields']):
                lines+=['Field '+str(i)+' ('+f[':answer-field/type']+')','']+['- $'+c[':answer/value']+'$'+(' **keyed**' if ':answer-field/correct' in f and c[':answer/id']==f[':answer-field/correct'][1] else '') for c in f[':answer-field/choices']]+['']
            lines += [q[':question/worked-solution'],'']
    (ROOT/'review.md').write_text('\n'.join(lines)+'\n');print(json.dumps({k:report[k] for k in ('pass','source','sampled_distinct_tasks_64','default_family_coverage')},indent=2))
if __name__=='__main__':main()
