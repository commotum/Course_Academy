"""Independent displayed-function differentiation, step chains, fidelity and grading."""
import copy, hashlib, importlib.util, json, re, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
native=[]
cases=[{'source_id':sid,'level':'easy','bank_profile':c['profile'],**c} for sid,c in g.CASES.items()]

def save(path,obj):path.write_text(json.dumps(obj,indent=2,default=str)+'\n')
def eq(a,b):return g.sp.simplify(a-b)==0

def solution_values(q):
    text=q[':question/worked-solution']
    displays=re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S)
    assert len(displays)==2
    identity=displays[0].replace(r'\frac{\text{d}}{\text{d}x}','D')
    lhs,rhs=identity.split('=');assert eq(g.expression(lhs),g.expression(rhs))
    aligned=re.sub(r'\\(?:begin|end)\{aligned\}','',displays[1])
    target=g.sp.diff(g.expression(re.search(r'\$y\s*=\s*(.*?)\$',q[':question/problem'])[1]),g.x)
    values=[]
    for row in aligned.split(r'\\'):
        lhs,rhs=row.replace('&','').split('=')
        rhs=rhs.replace(r'\frac{\text{d}}{\text{d}x}','D')
        value=g.expression(rhs);assert eq(value,target),(rhs,value,target)
        values.append(value)
    assert len(values)==4
    return target

def ordered(q):
    q=copy.deepcopy(q)
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

def validate(rec):
    assert rec['knowledge_point']['db_id']==g.KP_ID and rec['knowledge_point']['id']==g.KP_UUID
    gen=rec['generation'];q=rec['question']
    assert gen['version']==g.VERSION and gen['domain']=='x>0'
    expected=g.generate(q[':question/difficulty'].split('/')[-1],gen['seed'],gen['template'],parameters=gen['parameters'],profile=gen['profile'])
    assert ordered(q)==ordered(expected['question'])
    assert gen['math_fingerprint']==g.fingerprint(q)
    target=solution_values(q)
    fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];a=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
    assert len({v[':answer/id'] for v in a})==len(a)
    cid=next(v for v in a if v[':answer/id']==correct)
    assert eq(g.expression(cid[':answer/value']),target)
    if f[':answer-field/type'].endswith('/radio'):
        assert len(a)==5 and sum(eq(g.expression(v[':answer/value']),target) for v in a)==1
        assert not any(eq(g.expression(v[':answer/value']),g.expression(w[':answer/value'])) for i,v in enumerate(a) for w in a[:i])
        assert '{{' not in q[':question/problem']
        checks=[{'submitted_answer_id':v[':answer/id'],'expected':'accepted' if v[':answer/id']==correct else 'rejected','purpose':'Owned source-profile choice designation'} for v in a]
    else:
        assert q[':question/problem'].count('{{field-1}}')==1
        assert len(a)==(2 if gen['profile']=='equivalent-entry' else 1)
        assert all(eq(g.expression(v[':answer/value']),target) for v in a)
        p=gen['parameters']
        checks=[{'submitted':v[':answer/value'],'expected':'accepted','purpose':'Canonical and retained equivalent value'} for v in a]
        checks += [{'submitted':f"{2*p['n']}/({2*p['d']}x)",'expected':'accepted','purpose':'Unreduced independent equivalent'}, {'submitted':g.latex(target+1),'expected':'rejected','purpose':'Incorrect constant term'}, {'submitted':g.latex(-target),'expected':'rejected','purpose':'Sign error'}]
    native.append({'label':q[':question/id'],'record':rec,'checks':checks})

def validate_existing(q):
    fields=q.get(':question/answer-fields',[]);assert len(fields)==1,'Missing learner fields'
    f=fields[0];assert ':answer-field/correct' in f,'Missing correct designation'
    assert ':question/worked-solution' in q,'Missing worked solution'
    assert q[':question/difficulty'][':db/ident']==':question.difficulty/easy'
    target=solution_values(q)
    correct=f[':answer-field/correct'];assert eq(g.expression(correct[':answer/value']),target)
    assert any(a[':answer/id']==correct[':answer/id'] for a in f[':answer-field/choices'])
    vals=[g.expression(a[':answer/value']) for a in f[':answer-field/choices']]
    if f[':answer-field/type'][':db/ident'].endswith('/radio'):
        assert len(vals)==5 and sum(eq(v,target) for v in vals)==1
        assert not any(eq(v,w) for i,v in enumerate(vals) for w in vals[:i])
    else:assert all(eq(v,target) for v in vals)
    return True

def main():
    records=[];fidelity=[];review=[];values=designations=solutions=0
    for case in cases:
        sid=case['source_id'];source=g.QS[sid]
        rec=g.generate('easy',0,case['template'],parameters=case['parameters'],profile=case['profile']);validate(rec)
        generated=rec['question'];f=source[':question/answer-fields'][0];out=generated[':question/answer-fields'][0]
        remaining=list(out[':answer-field/choices'])
        for a in f[':answer-field/choices']:
            # Equivalent blank aliases are paired by notation first, mathematical
            # equivalence second, so each full bank member has exactly one mate.
            match=next((v for v in remaining if v[':answer/value']==a[':answer/value']),None)
            if match is None:match=next((v for v in remaining if eq(g.expression(v[':answer/value']),g.expression(a[':answer/value']))),None)
            assert match is not None,(sid,a)
            remaining.remove(match);values+=1
        assert not remaining and len(f[':answer-field/choices'])==len(out[':answer-field/choices'])
        if ':answer-field/correct' in f:
            actual=next(v for v in out[':answer-field/choices'] if v[':answer/id']==out[':answer-field/correct'][1])
            assert eq(g.expression(actual[':answer/value']),g.expression(f[':answer-field/correct'][':answer/value']));designations+=1
        assert source[':question/problem']==generated[':question/problem'],(sid,source[':question/problem'],generated[':question/problem'])
        if ':question/worked-solution' in source:
            assert source[':question/worked-solution']==generated[':question/worked-solution'],sid
            solution_values(source);solutions+=1
        fidelity.append({'source_id':sid,'complete_bank_match':True,'values':len(f[':answer-field/choices']),'prompt_exact':True,'solution_exact':':question/worked-solution' in source,'correct_observed':':answer-field/correct' in f,'source_rating_observed':':question/difficulty' in source})
        records.append(rec)
        review+=['## Source '+sid,source[':question/problem'],'\nBank: '+', '.join('$'+a[':answer/value']+'$' for a in f[':answer-field/choices']),source.get(':question/worked-solution','No source solution; generated solution authored from canonical e-3627.'),'### Replay',g.markdown(rec)]
    coverage={};sample=[]
    for template,(_,profiles) in g.TEMPLATES.items():
        for profile in profiles:
            key=template+'/'+profile;coverage[key]=0
            # Both signs, min/max magnitudes and denominators plus seeded interior.
            ps=[{'n':n,'d':d,'e':profile=='euler'} for n in (-30,-11,-2,2,11,30) for d in ((2,3,11,12) if profile in ('fraction','equivalent-entry') else (1,2,12) if profile=='canonical' else (1,))]
            for p in ps:
                try:g.validate_parameters(p,profile)
                except ValueError:continue
                rec=g.generate('easy',1,template,parameters=p,profile=profile);validate(rec);sample.append(rec);coverage[key]+=1
            for seed in range(10):
                rec=g.generate('easy',seed,template,profile=profile);validate(rec);sample.append(rec);coverage[key]+=1
            review += ['## Variant '+key,g.markdown(sample[-1])]
    for level in ('moderate','hard'):
        try:g.generate(level,0)
        except ValueError:pass
        else:raise AssertionError('Unsupported level accepted')
    for p in ({'n':1,'d':1,'e':False},{'n':0,'d':1,'e':False},{'n':2,'d':2,'e':False},{'n':31,'d':1,'e':False}):
        try:g.generate('easy',0,'blank',parameters=p,profile='canonical')
        except ValueError:pass
        else:raise AssertionError('Invalid boundary accepted')
    a=g.generate('easy',4,'blank',parameters={'n':13,'d':2,'e':False},profile='canonical');b=g.generate('easy',9,'blank',parameters={'n':13,'d':2,'e':False},profile='canonical')
    assert ordered(a['question'])==ordered(b['question']) and a['generation']['math_fingerprint']==b['generation']['math_fingerprint']
    save(HERE/'source-cases.json',cases);save(HERE/'review.json',records+sample);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save(HERE/'native-input.json',native)
    subprocess.run([str(HERE/'check-current-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    nr=json.loads((HERE/'native-report.json').read_text());assert nr['documented_unresolved_checks']==0
    result={'passed':True,'source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'fidelity':{'complete_banks':len(fidelity),'total_banks':8,'matched_values':values,'total_values':26,'supplied_correct_designations':designations,'independently_inferred_designations':2,'exact_prompts':8,'exact_supplied_worked_solutions':solutions,'authored_missing_solutions':2},'source_details':fidelity,'profile_boundary_and_seed_checks':coverage,'native_checks':{k:nr[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'identity_seed_invariant':True,'unsupported_levels_rejected':True,'no_plots_required':True,'database_writes':0}
    assert values==26 and designations==6 and solutions==6
    save(HERE/'validation.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
