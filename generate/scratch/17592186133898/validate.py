"""Read rendered objects independently; verify full banks and every solution RHS."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));from math_reader import *
spec=importlib.util.spec_from_file_location('curl',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(p,v):p.write_text(json.dumps(v,indent=2,default=str)+'\n')
def eq(a,b):return sp.simplify(a-b)==0

def audit(rec):
    q=rec['question'];P,Q,pt=displayed(q);D=sp.diff(Q,x)-sp.diff(P,y)
    answer=sp.simplify(D.subs(dict(zip((x,y),pt)),simultaneous=True)) if pt else sp.simplify(D)
    if pt:
        for v in (P,Q):
            z=v.subs(dict(zip((x,y),pt)),simultaneous=True);assert z.is_real is not False and not z.has(sp.zoo,sp.nan,sp.oo)
    f=q[':question/answer-fields'][0];values=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(values)==5 and len(set(a[':answer/id'] for a in f[':answer-field/choices']))==5
    for a,val in zip(f[':answer-field/choices'],values):assert eq(val,answer)==(a[':answer/id']==f[':answer-field/correct'][1])
    assert all(not eq(a,b) for k,a in enumerate(values) for b in values[k+1:])
    n=0
    for bi,block in enumerate(re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)):
        for row in block.split(r'\\'):
            if '& =' not in row:continue
            rhs=row.split('& =',1)[1];ds=derivative_inputs(rhs)
            if ds:
                assert [d[0] for d in ds]==['x','y'];assert eq(parse(ds[0][1]),Q) and eq(parse(ds[1][1]),P);n+=2
            else:assert eq(parse(rhs),D if bi==0 else answer),(g.VERSION,rec['generation'],rhs);n+=1
    assert n>=3
    for t in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in f[':answer-field/choices']]:
        assert t.count('$')%2==0
        assert t.count('{')==t.count('}')
    return {'fingerprint':fingerprint(q),'displayed_rows_checked':n}

def engine_checks(rec,label):
    f=rec['question'][':question/answer-fields'][0]
    return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned option; full source bank'} for a in f[':answer-field/choices']]}

def native(records,path):
    path.mkdir(parents=True,exist_ok=True);write(path/'native-input.json',[engine_checks(r,str(k)) for k,r in enumerate(records)])
    binary=ROOT/'generate/runs/current/check-engine'
    result=subprocess.run([str(binary),str(path/'native-input.json'),str(path/'native-report.json')],capture_output=True,text=True,check=True,timeout=55)
    (path/'native.log').write_text(result.stdout+result.stderr)
    rep=json.loads((path/'native-report.json').read_text());assert rep['documented_unresolved_checks']==0
    return rep

def main():
    records=[];fidelity=[];review=[];components=[];coverage={}
    for mid,t in sorted(g.TEMPLATES.items()):
        src=g.SOURCE_BY_ID[mid];r=g.generate(t['level'],template=mid,parameters={'c':1});audit(r)
        assert r['question'][':question/problem']==src[':question/problem'] and r['question'][':question/worked-solution']==src[':question/worked-solution']
        sf=src[':question/answer-fields'][0];gf=r['question'][':question/answer-fields'][0]
        assert gf[':answer-field/key']==sf[':answer-field/key'] and gf[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        matches=[]
        for a in sf[':answer-field/choices']:
            found=[z for z in gf[':answer-field/choices'] if eq(parse(a[':answer/value']),parse(z[':answer/value']))];assert len(found)==1
            assert (a[':answer/id']==sf[':answer-field/correct'][':answer/id'])==(found[0][':answer/id']==gf[':answer-field/correct'][1]);matches.append(a[':answer/id'])
        fidelity.append({'source_id':mid,'template':mid,'profile':t['profile'],'distractors_matched':4,'distractors_total':4,'complete_bank_matched':True,'missing_options':[],'extra_options':[],'prompt_solution_exact':True,'notation_normalization':'remove captured extra backslash and literal/Unicode function application markers from new answer values; algebra unchanged'})
        P,Q,pt=displayed(src);components.append({'source_id':mid,'P':str(P),'Q':str(Q),'evaluation_point':None if pt is None else list(map(str,pt)),'domain':'x+y>0' if mid=='q-131348' else 'x²+y²>0' if mid=='q-131343' else 'R²','slots':{'c':{'role':'common nonzero positive scalar on complete components and bank','observed':1,'sampling':list(g.SCALES),'dependent':['prompt RHS','formal derivative inputs','every solution RHS','complete answer bank']}},'choices':[{'source_answer_id':a[':answer/id'],'exact_observed_expression':str(parse(a[':answer/value'])),'recipe':'c * ('+str(parse(a[':answer/value']))+')','interpretation':'observed expression pattern; underlying misconception unresolved'} for a in sf[':answer-field/choices']]})
        coverage[mid]=[]
        for c in g.SCALES:
            r=g.generate(t['level'],seed=13,template=mid,parameters={'c':c});audit(r);records.append(r);coverage[mid].append(c)
            assert r==g.generate(t['level'],seed=13,template=mid,parameters={'c':c})
            other=g.generate(t['level'],seed=999,template=mid,parameters={'c':c});assert other['question']==r['question']
            if c in (2,9):review.append({'source_id':mid,'source':src,'variant':r})
    assert len({fingerprint(r['question']) for r in records})==len(records)
    rep=native(records,HERE/'reference/validation')
    write(HERE/'source-fidelity.json',fidelity);write(HERE/'source-components.json',components);write(HERE/'review.json',review)
    (HERE/'review.md').write_text('\n\n---\n\n'.join('Source '+a['source_id']+'\n\n'+a['source'][':question/problem']+'\n\n'+a['source'][':question/worked-solution']+'\n\nVariant\n\n'+g.markdown(a['variant']) for a in review))
    write(HERE/'validation.json',{'status':'passed','supported_templates':len(g.TEMPLATES),'complete_source_banks':len(fidelity),'matched_distractors':4*len(fidelity),'total_distractors':4*len(fidelity),'bounded_domain_questions':len(records),'distinct_mathematical_tasks':len(records),'slot_coverage':coverage,'all_displayed_solution_rows_valid':True,'determinism':True,'seed_change_does_not_change_question':True,'native':rep,'excluded_sources':g.EXCLUDED,'blank_generators':0,'native_binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'sympy':sp.__version__})
    print(json.dumps({'templates':len(g.TEMPLATES),'validated_questions':len(records),'grader_accepted':rep['accepted_checks'],'grader_rejected':rep['rejected_checks']}))
if __name__=='__main__':main()
