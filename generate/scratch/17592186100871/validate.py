"""Independent rendered matrix, bank, solution and native-grader validation."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));from math_reader import *
spec=importlib.util.spec_from_file_location('dimensions',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,default=str)+'\n')
def audit(rec):
    q=rec['question'];mats,(a,b),(r,k,c)=displayed(q)
    A=sp.Matrix([[0]*mats[a][1] for _ in range(mats[a][0])]);B=sp.Matrix([[0]*mats[b][1] for _ in range(mats[b][0])]);assert (A*B).shape==(r,c)
    fields=q[':question/answer-fields'];kind=fields[0][':answer-field/type'];assert len(fields)==(1 if kind.endswith('/radio') else 2)
    for f in fields:
        values=[];correct=f[':answer-field/correct'][1]
        for option in f[':answer-field/choices']:
            value=dimension(option[':answer/value']) if kind.endswith('/radio') else int(option[':answer/value'])
            expected=(r,c) if kind.endswith('/radio') else r if f[':answer-field/key']=='field-1' else c
            assert (value==expected)==(option[':answer/id']==correct)
            assert value not in values;values.append(value)
        assert len(values)==(5 if kind.endswith('/radio') else 1)
    s=re.sub(r'\$([A-Z])([.,])\$',r'$\1$\2',q[':question/worked-solution'])
    assertions=re.findall(r'\$([A-Z])\$ is a \$(\d+)\\times (\d+)\$ matrix',s)
    # Second source sentence omits "is a"; parse separately.
    assert len(assertions)==2,(q[':question/id'],assertions)
    for name,rows,cols in assertions:assert (int(rows),int(cols))==mats[name]
    assert re.search(r'\$'+a+b+r'\$ has dimensions \$'+str(r)+r'\\times '+str(c)+r':\$',s)
    assert ('columns in $'+a+'$' in s or 'column in $'+a+'$' in s) and ('rows in $'+b+'$' in s or 'row in $'+b+'$' in s), (a,b,s)
    assert str(k)+r'}}\times '+str(c) in s and a+b+'}_{'+str(r)+r'\times '+str(c) in s
    for text in (q[':question/problem'],s):assert text.count('$')%2==0 and text.count('{')==text.count('}')
    return {'fingerprint':(r,k,c),'operand_dimensions':mats,'actual_matrix_product_verified':True}

def engine_checks(rec,label):
    checks=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        if f[':answer-field/type'].endswith('/radio'):
            checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all field-owned options'} for a in f[':answer-field/choices'])
        else:
            n=int(f[':answer-field/choices'][0][':answer/value'])
            checks.extend({'field_index':i,'submitted':s,'expected':e,'purpose':'equivalent integer or incorrect dimension'} for s,e in [(str(n),'accepted'),(str(n)+'.0','accepted'),(str(n)+'+0','accepted'),(str(n+1),'rejected'),(str(-n),'rejected')])
    return {'label':label,'record':rec,'checks':checks}

def native(records,path):
    write(path/'native-input.json',[engine_checks(r,str(i)) for i,r in enumerate(records)])
    x=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],text=True,capture_output=True,check=True,timeout=55)
    (path/'native.log').write_text(x.stdout+x.stderr);rep=json.loads((path/'native-report.json').read_text());assert rep['documented_unresolved_checks']==0;return rep

def main():
    records=[];fidelity=[];components=[];review=[];coverage={}
    for mid,t in g.TEMPLATES.items():
        src=g.SOURCE_BY_ID[mid];r=g.generate(t['level'],template=mid,replay=True);audit(r);sf=sorted(src[':question/answer-fields'],key=lambda f:f[':answer-field/key']);gf=r['question'][':question/answer-fields']
        assert src[':question/problem']==r['question'][':question/problem']
        corrected=src[':question/worked-solution'].replace('$3\\times 2$ matrix','$4\\times 2$ matrix') if mid=='q-22067' else src[':question/worked-solution'];assert corrected==r['question'][':question/worked-solution']
        matched=0;choices=[]
        for old,new in zip(sf,gf):
            assert old[':answer-field/key']==new[':answer-field/key'] and old[':answer-field/type'][':db/ident']==new[':answer-field/type']
            for a in old[':answer-field/choices']:
                val=dimension(a[':answer/value']) if t['field_type']=='radio' else int(a[':answer/value'])
                matches=[z for z in new[':answer-field/choices'] if (dimension(z[':answer/value']) if t['field_type']=='radio' else int(z[':answer/value']))==val];assert len(matches)==1
                assert (a[':answer/id']==old[':answer-field/correct'][':answer/id'])==(matches[0][':answer/id']==new[':answer-field/correct'][1]);matched+=1
                recipe=next(recipe for recipe,value in g.recipes(mid,*displayed(src)[2]) if value==val) if t['field_type']=='radio' else 'outer-left rows' if old[':answer-field/key']=='field-1' else 'outer-right columns'
                choices.append({'field':old[':answer-field/key'],'source_answer_id':a[':answer/id'],'observed':a[':answer/value'],'recipe':recipe,'full_value_reproduced':True})
        fidelity.append({'source_id':mid,'options_matched':matched,'options_total':sum(len(f[':answer-field/choices']) for f in sf),'distractors_matched':4 if t['field_type']=='radio' else 0,'complete_bank':True,'missing_options':[],'extra_options':[],'prompt_exact':True,'solution_exact':mid!='q-22067','supported_source_correction':'A is 4×2, not 3×2' if mid=='q-22067' else None})
        components.append({'source_id':mid,'difficulty':t['level'],'field_type':t['field_type'],'template':('reverse' if t['level']=='hard' else 'forward')+'-'+t['field_type'],'observed_dimensions':displayed(src)[2],'profile':t['profile'],'choices':choices,'original_problem':src[':question/problem'],'original_solution':src[':question/worked-solution'],'domain':g.domain(mid)})
        coverage[mid]=[]
        for p in g.domain(mid):
            z=g.generate(t['level'],seed=23,template=mid,parameters=dict(zip(('r','k','c'),p)));audit(z);records.append(z);coverage[mid].append(p)
            assert z==g.generate(t['level'],seed=23,template=mid,parameters=z['generation']['parameters'])
            assert z['question']==g.generate(t['level'],seed=999,template=mid,parameters=z['generation']['parameters'])['question']
        changed=next(p for p in g.domain(mid) if p!=displayed(src)[2]);review.append({'source_id':mid,'source':src,'variant':g.generate(t['level'],template=mid,parameters=dict(zip(('r','k','c'),changed)))})
    # Exercise same operands in both product orders; keys and solution must follow target.
    forward=g.generate('moderate',template='q-129492',parameters={'r':3,'k':3,'c':2});reverse=g.generate('hard',template='q-129489',parameters={'r':2,'k':3,'c':4})
    # Actual same-data target swap is source-backed square reverse vs forward-square profile.
    src=g.SOURCE_BY_ID['q-22067'];_,labels,p=displayed(src);a,b=labels
    swapped=g.generate('hard',template='q-22067',replay=True);swapped['question'][':question/problem']=src[':question/problem'].replace('$BA?$', '$AB?$')
    assert fingerprint(src)==(2,4,2) and fingerprint(swapped['question'])==(4,2,4)
    try:audit(swapped)
    except AssertionError:stale_caught=True
    else:raise AssertionError('Stale target references/key were not caught')
    rep=native(records,HERE/'reference/validation')
    write(HERE/'source-fidelity.json',fidelity);write(HERE/'source-components.json',components);write(HERE/'review.json',review)
    (HERE/'review.md').write_text('\n\n---\n\n'.join('Source '+x['source_id']+'\n\n'+x['source'][':question/problem']+'\n\n'+x['source'][':question/worked-solution']+'\n\nVariant\n\n'+g.markdown(x['variant']) for x in review))
    write(HERE/'validation.json',{'status':'passed','source_banks':len(fidelity),'complete_banks_matched':len(fidelity),'matched_options':sum(x['options_matched'] for x in fidelity),'total_options':sum(x['options_total'] for x in fidelity),'mathematical_checks':len(records),'distinct_finite_tasks':{l:len(g.candidates(l)) for l in g.SUPPORTED},'slot_coverage':coverage,'target_swap_stale_key_caught':stale_caught,'seed_does_not_create_content':True,'native':rep,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'native_binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'source_exclusions':g.EXCLUDED})
    print(json.dumps({'source_banks':len(fidelity),'parameter_cases':len(records),'native_accepted':rep['accepted_checks'],'native_rejected':rep['rejected_checks']}))
if __name__=='__main__':main()
