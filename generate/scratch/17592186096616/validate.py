"""Independent displayed-math, full fidelity, mutation and real native grading QA."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).parent;ROOT=H.parents[2]
sys.path.insert(0,str(H))
from scalar_parser import scalar,prompt,same,X,group
spec=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
S={q[':question/math-academy-id']:q for q in g.SOURCE['record'][':knowledge-point/questions']}
native=[]
def fmt(s):
    assert all(ord(c)>=32 or c in '\n\t\r' for c in s),'control character'
    assert s.count('$')%2==0,'math delimiters'
    depth=0
    for i,c in enumerate(s):
        if c in '{}':
            if i and s[i-1]=='\\':continue
            depth+=1 if c=='{' else -1;assert depth>=0,'TeX grouping'
    assert depth==0,'TeX grouping'
    assert '@@' not in s and '+-' not in s and '--' not in s,'invalid signed tokens'
def stripbars(s,t):
    # Read every actual evaluation operand, including nested fractions, before removing.
    for pattern in (r'\big|_{x=',r'|}_{x='):
        while pattern in s:
            i=s.index(pattern);start=i+len(pattern);# All operand braces are scanned below.
            # start lies after opening brace and x=, scan enclosing group independently.
            depth=1;j=start
            while depth:
                if s[j]=='{':depth+=1
                elif s[j]=='}':depth-=1
                j+=1
            assert same(scalar(s[start:j-1]),t),'stale evaluation operand'
            s=s[:i]+('}' if pattern.startswith('|}') else '')+s[j:]
    return s

def rows(rec,f,t):
    sol=rec['question'][':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==2
    c=g.case(rec['generation']['template']);ns=[]
    original_solution=S[c['source_id']].get(':question/worked-solution')
    original_blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',original_solution,re.S) if original_solution else []
    for bi,b in enumerate(blocks):
        b=b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');rr=b.split(r'\\');ns.append(len(rr))
        for ri,row in enumerate(rr):
            if original_blocks and bi==0:
                source_row=original_blocks[bi].split(r'\\')[ri]
                for operation in (g.D,r'\cdot'):
                    assert row.count(operation)==source_row.count(operation),'operative stage changed'
            if bi==1:row=stripbars(row,t)
            rhs=row.split('=',1)[1].replace('&','').strip()
            val=scalar(rhs)
            if bi==1:val=val.subs(X,t)
            assert same(val,sp.diff(f,X) if bi==0 else sp.diff(f,X).subs(X,t)),('printed stage',rec['generation']['template'],bi,row,val)
    expected=[c['d_stages'],c['eval_stages']]
    assert ns==expected,(ns,expected)
    # Point prose is an independently parsed operand; raw q-70903 alone has documented typo.
    m=re.search(r'Therefore, the slope\s+of the tangent at \$x=(.*?)\$',sol,re.S);assert m
    if not (rec['generation']['evidence_only'] and c['source_id']=='q-70903'):assert same(scalar(m[1]),t),'stale point prose'
    return sum(ns)
def validate(rec,collect=True):
    assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=rec['question'];fmt(q[':question/problem'])
    for b in re.findall(r'(?:\\log|\{log\})_\{(-?\d+)\}',q[':question/problem']):assert int(b)>0 and int(b)!=1
    f,t=prompt(q[':question/problem'])
    assert t.is_positive is True,'positive logarithm input'
    # Validate domains directly from printed log base before differentiation/CAS work.
    for b in re.findall(r'(?:\\log|\{log\})_\{(\d+)\}',q[':question/problem']):assert int(b)>0 and int(b)!=1
    assert f.has(sp.log(X));d=sp.diff(f,X);ans=sp.expand(d.subs(X,t),log=False)
    assert not ans.has(sp.zoo,sp.nan,sp.oo)
    if ':question/worked-solution' in q:fmt(q[':question/worked-solution']);rows(rec,f,t)
    assert rec['generation']['mathematical_fingerprint']==g.digest([sp.srepr(sp.simplify(d)),sp.srepr(sp.simplify(t))])
    if ':question/answer-fields' not in q:return
    field=q[':question/answer-fields'][0];kind=field[':answer-field/type'].split('/')[-1];aa=field[':answer-field/choices'];ids=[a[':answer/id']for a in aa];assert len(ids)==len(set(ids))
    vals=[]
    for a in aa:fmt(a[':answer/value']);assert '$' not in a[':answer/value'];vals.append(scalar(a[':answer/value']))
    if kind=='radio':assert len(aa)==5 and all(not same(u,v)for i,u in enumerate(vals)for v in vals[i+1:])
    else:
        assert all(same(v,ans)for v in vals)
        assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
    if ':answer-field/correct' not in field:return
    cid=field[':answer-field/correct'][1];assert cid in ids
    assert same(vals[ids.index(cid)],ans)
    if not collect:return
    if kind=='radio':checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'complete owned radio bank'}for a in aa]
    else:
        eq=g.tex(d).replace('x','('+g.tex(t)+')')
        checks=[{'submitted':a[':answer/value'],'expected':'accepted','purpose':'all stored spellings'}for a in aa]+[{'submitted':eq,'expected':'accepted','purpose':'unreduced derivative evaluated from actual printed function'},{'submitted':g.tex(ans+1),'expected':'rejected','purpose':'incorrect value'}]
    native.append({'label':q[':question/id'],'record':rec,'checks':checks})
def main():
    fidelity=[];review=[];normal=[];options=refs=0
    totals={'easy_radio':0,'easy_blank':0,'easy_fieldless':0,'unrated_radio':0}
    for source in S.values():
        fs=source.get(':question/answer-fields')
        key='easy_fieldless' if fs is None else ('easy_' if ':question/difficulty' in source else 'unrated_')+fs[0][':answer-field/type'][':db/ident'].split('/')[-1]
        totals[key]+=1
    assert totals=={'easy_radio':3,'easy_blank':6,'easy_fieldless':2,'unrated_radio':2}
    for c in g.CASES:
        s=S[c['source_id']];r=g.generate('easy',31,c['template'],parameters=c['parameters'],profile=c['bank_profile']);validate(r);q=r['question']
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in s),'raw key-presence mismatch'
        assert q[':question/problem']==s[':question/problem'];assert q.get(':question/worked-solution')==s.get(':question/worked-solution')
        sf=s.get(':question/answer-fields',[]);rf=q.get(':question/answer-fields',[])
        if sf:
            assert len(sf)==len(rf)==1
            assert (':answer-field/correct' in sf[0])==(':answer-field/correct' in rf[0])
            ov=sorted(a[':answer/value']for a in sf[0][':answer-field/choices']);rv=sorted(a[':answer/value']for a in rf[0][':answer-field/choices']);assert ov==rv,(c['source_id'],ov,rv)
            options+=len(ov)
            if ':answer-field/correct' in sf[0]:
                cv=sf[0][':answer-field/correct'][':answer/value'];rid=rf[0][':answer-field/correct'][1];assert next(a[':answer/value']for a in rf[0][':answer-field/choices']if a[':answer/id']==rid)==cv;refs+=1
        nr=g.generate('easy',41,c['template'],parameters=c['parameters']);validate(nr);variant=g.generate('easy',81,c['template']);validate(variant)
        review.append({'source_id':c['source_id'],'original':s,'raw_parameterized_replay':r,'normal_at_original':nr,'normal_variant':variant})
        fidelity.append({'source_id':c['source_id'],'raw_prompt_exact':True,'raw_solution_exact':':question/worked-solution' in s,'raw_attribute_presence_exact':True,'complete_bank_exact':bool(sf),'options':len(ov) if sf else 0,'existing_correct_exact':bool(sf and ':answer-field/correct' in sf[0])})
    raw_variants=[]
    for c in g.CASES:
        for seed in range(3):
            r=g.generate('easy',seed+200,c['template'],profile=c['bank_profile']);validate(r);raw_variants.append(r)
    slots={};fps={l:set()for l in g.SUPPORTED_LEVELS};families=set();orders=set()
    for level in g.SUPPORTED_LEVELS:
        ts=list(g.TEMPLATES) if level=='easy' else ['ln_quadratic_linear_radio'] if level=='moderate' else ['log_quadratic_linear_blank']
        for t in ts:
            for seed in range(15):
                r=g.generate(level,seed,t);validate(r);fps[level].add(r['generation']['mathematical_fingerprint']);normal.append(r)
                rr=g.generate(level,seed+1000,t,parameters=r['generation']['parameters'],profile=r['generation']['profile']);assert rr['question'][':question/id']==r['question'][':question/id']
                for k,v in r['generation']['parameters'].items():slots.setdefault(level+'/'+t+'/'+k,set()).add(v)
                ff=r['question'][':question/answer-fields'][0]
                if ff[':answer-field/type'].endswith('radio'):orders.add(next(i for i,a in enumerate(ff[':answer-field/choices'])if a[':answer/id']==ff[':answer-field/correct'][1]))
        for seed in range(30):families.add(g.generate(level,seed)['generation']['template'])
    assert families==set(g.TEMPLATES);assert len(orders)>1
    # Mutation regressions: actual prompt, derivative input, point prose and final stages.
    base=g.generate('easy',1,'quadratic_ln_blank',parameters={'a':5,'c':6,'t':3})
    mutations=[(':question/problem','y=5','y=7'),(':question/worked-solution','(5{x}^{2}','(7{x}^{2}'),(':question/worked-solution','at $x=3$','at $x=2$'),(':question/worked-solution','10\\cdot 3','10\\cdot 2'),(':question/worked-solution','5'+g.D+r'({x}^{2})+6'+g.D+r'(\operatorname{ln}x)',r'10x+\frac{6}{x}'),(':question/worked-solution','32','31'),(':question/problem','Given','Given\x0c')]
    for key,a,b in mutations:
        m=copy.deepcopy(base);assert a in m['question'][key];m['question'][key]=m['question'][key].replace(a,b,1)
        try:validate(m,False)
        except (AssertionError,ValueError,IndexError,TypeError,SyntaxError):pass
        else:raise AssertionError(('mutation accepted',a))
    for level,t,p in [('easy','quadratic_ln_blank',{'a':2,'c':3,'t':0}),('easy','negative_exp_log_blank',{'a':2,'c':3,'t':2,'b':1}),('moderate','ln_quadratic_linear_radio',{'a':2,'c':3,'k':4,'t':1}),('hard','log_quadratic_linear_blank',{'a':10,'c':3,'k':4,'s':2,'b':3})]:
        try:g.generate(level,template=t,parameters=p)
        except ValueError:pass
        else:raise AssertionError('scope/domain guard missed')
    (H/'native-input.json').write_text(json.dumps(native,indent=2)+'\n');engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(H/'native-input.json'),str(H/'native-report.json')],check=True)
    nr=json.loads((H/'native-report.json').read_text());assert nr['documented_unresolved_checks']==0
    levels={l:[g.generate(l,i+210)for i in range(2)]for l in g.SUPPORTED_LEVELS}
    data={'source_reviews':review,'generated_raw_variants':raw_variants,'generated_level_examples':levels};(H/'review.json').write_text(json.dumps(data,indent=2)+'\n')
    md=['# Frozen basis 1356 review','Raw replay retains omissions and the source q-70903 typo. Normal records complete missing fields/keys and use explicit authored method banks.']
    for item in review:
        md+=['## '+item['source_id'],'### Original',item['original'][':question/problem'],item['original'].get(':question/worked-solution','Source solution omitted.'),'Original bank: '+str([a[':answer/value']for f in item['original'].get(':question/answer-fields',[])for a in f[':answer-field/choices']])]
        for key in ('raw_parameterized_replay','normal_at_original','normal_variant'):
            q=item[key]['question'];md+=[key,q[':question/problem'],str([a[':answer/value']for f in q.get(':question/answer-fields',[])for a in f[':answer-field/choices']]),q.get(':question/worked-solution','Source solution omitted.')]
    for r in raw_variants[::3]:
        q=r['question'];md+=['## Changed-parameter evidence profile '+r['generation']['profile'],q[':question/problem'],str([a[':answer/value']for f in q.get(':question/answer-fields',[])for a in f[':answer-field/choices']]),q.get(':question/worked-solution','Source solution omitted.')]
    for l,rs in levels.items():
        for r in rs:md+=['## Authored/default '+l,r['question'][':question/problem'],r['question'][':question/worked-solution']]
    (H/'review.md').write_text('\n\n'.join(md)+'\n')
    from fractions import Fraction
    moderate_capacity=0
    for a in range(1,10):
        for c0 in range(1,10):
            for k in range(1,10):
                for t0 in range(2,5):
                    v=[Fraction(a,t0)+2*c0*t0-k,Fraction(a,t0)+2*c0*t0+k,-Fraction(a,t0)+2*c0*t0-k,Fraction(a,t0)+c0*t0-k,2*c0*t0-k]
                    moderate_capacity+=len(set(v))==5
    report={'passed':True,'authored_domain_capacity':{'moderate_distinct_eligible_tasks':moderate_capacity,'hard_parameter_combinations_upper_bound':9**3*8*3,'hard_note':'equivalent base/point scalings may deduplicate; upper bound is not a unique-task claim'},'basis':1356,'lineage':g.SOURCE['lineage'],'source_questions':13,'observed_type_totals':totals,'source_exact_prompts':13,'source_exact_present_solutions':11,'source_complete_banks':11,'source_exact_options':options,'source_exact_existing_correct_refs':refs,'source_raw_presence_parity':13,'source_fidelity':fidelity,'distinct_sample_tasks':{k:len(v)for k,v in fps.items()},'slot_coverage':{k:sorted(v)for k,v in slots.items()},'native':{k:nr[k]for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'raw_changed_parameter_variants':len(raw_variants),'mutation_regressions':len(mutations),'authored_levels':['moderate','hard'],'opaque_profiles_evidence_only':True,'database_writes':0}
    (H/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in ('passed','source_exact_options','source_exact_existing_correct_refs','distinct_sample_tasks','native')},indent=2))
if __name__=='__main__':main()
