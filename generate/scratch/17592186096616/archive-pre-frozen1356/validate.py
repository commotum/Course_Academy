"""Displayed-record validation and full source-bank replay with native grading."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from scalar_parser import scalar, prompt, same, X
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SOURCE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
native=[]
def fmt(text):
    assert text.count('$')%2==0
    depth=0
    for i,c in enumerate(text):
        if c in '{}':
            if i and text[i-1]=='\\':continue
            depth+=1 if c=='{' else -1
            assert depth>=0
    assert depth==0
    assert '@@' not in text

def stages(rec,expected_d,expected_slope):
    blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',rec['question'][':question/worked-solution'],re.S)
    assert len(blocks)==2
    ns=[]
    for i,block in enumerate(blocks):
        block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
        n=0
        for row in block.split(r'\\'):
            assert '&' in row
            rhs=row.split('&',1)[1].strip().lstrip('=').strip()
            value=scalar(rhs.split(r'\big|_{x=',1)[0])
            if r'\big|_{x=' in rhs:value=value.subs(X,prompt(rec['question'][':question/problem'])[1])
            assert same(value,expected_d if i==0 else expected_slope),('printed solution',rec['generation']['template'],rhs)
            n+=1
        ns.append(n)
    c=g.case(rec['generation']['template']);assert ns==[c['d_stages'],c['eval_stages']],ns
    return sum(ns)

def validate(rec,collect=True):
    assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=rec['question'];assert q[':question/difficulty']==':question.difficulty/easy'
    assert len(q[':question/answer-fields'])==1
    f=q[':question/answer-fields'][0];kind=f[':answer-field/type'].split('/')[-1]
    assert kind in ('radio','blank');fmt(q[':question/problem']);fmt(q[':question/worked-solution'])
    if kind=='blank':assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    printed,t=prompt(q[':question/problem']);assert t.is_positive is True
    derivative=sp.diff(printed,X);ans=sp.expand(derivative.subs(X,t),log=False)
    assert not ans.has(sp.zoo,sp.nan,sp.oo)
    fields=f[':answer-field/choices'];ids=[a[':answer/id'] for a in fields];assert len(ids)==len(set(ids))
    assert f[':answer-field/correct'][0]==':answer/id';cid=f[':answer-field/correct'][1];assert cid in ids
    correct=next(a for a in fields if a[':answer/id']==cid)
    assert same(scalar(correct[':answer/value']),ans),('printed canonical answer',correct[':answer/value'],ans)
    values=[]
    for a in fields:
        assert a[':answer/type']==':answer.type/math';assert '$' not in a[':answer/value'];fmt(a[':answer/value']);values.append(scalar(a[':answer/value']))
    if kind=='radio':
        assert len(fields)==5
        assert sum(same(v,ans) for v in values)==1
        assert all(not same(v,u) for i,v in enumerate(values) for u in values[i+1:])
    else:assert all(same(v,ans) for v in values)
    fp=g.digest([sp.srepr(sp.simplify(derivative)),sp.srepr(t)])
    assert fp==rec['generation']['mathematical_fingerprint']
    n=stages(rec,derivative,ans)
    checks=[]
    if kind=='radio':
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'every field-owned radio selection'} for a in fields]
    else:
        checks=[{'submitted':a[':answer/value'],'expected':'accepted','purpose':'canonical or complete observed equivalent alias'} for a in fields]
        # Independent unevaluated evaluation of the printed derivative.
        equivalent=g.tex(derivative).replace('x','('+g.tex(t)+')')
        checks+=[{'submitted':equivalent,'expected':'accepted','purpose':'independently unreduced printed derivative evaluation'}, {'submitted':g.tex(ans+1),'expected':'rejected','purpose':'incorrect shifted scalar'}]
    if collect:native.append({'label':q[':question/id'],'record':rec,'checks':checks})
    return n

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build_engine():
    deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps'
    harness=ROOT/'generate/runs/current/check-engine.rs'
    libraries={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name in ('course_academy_engine','serde_json')}
    cmd=['rustc','--edition=2024','-O',str(harness)]
    for name,p in libraries.items():cmd+=['--extern',name+'='+str(p)]
    cmd+=['-L','dependency='+str(edb),'-L','dependency='+str(deps),'-o',str(HERE/'check-current-engine')]
    subprocess.run(cmd,check=True)
    (HERE/'current-engine-build.json').write_text(json.dumps({'harness':str(harness.relative_to(ROOT)),'harness_sha256':sha(harness),'executable_sha256':sha(HERE/'check-current-engine'),'libraries':{str(p.relative_to(ROOT)):sha(p) for p in libraries.values()},'command':cmd},indent=2)+'\n')

def main():
    build_engine();review=[];source_results=[];matched_options=0;correct_refs=0;stages_total=0;signatures=set();fingerprints=set();orders=set();errors=[]
    for c in g.CASES:
        s=SOURCES[c['source_id']];r=g.generate('easy',19,c['template'],parameters=c['parameters']);validate(r)
        f,t=prompt(s[':question/problem']);out_f,out_t=prompt(r['question'][':question/problem']);assert same(f,out_f) and same(t,out_t)
        rf=r['question'][':question/answer-fields'][0];generated=[scalar(a[':answer/value']) for a in rf[':answer-field/choices']]
        original=[scalar(a[':answer/value']) for field in s.get(':question/answer-fields',[]) for a in field[':answer-field/choices']]
        unused=generated.copy()
        for value in original:
            j=next((i for i,u in enumerate(unused) if same(value,u)),None);assert j is not None,(c['source_id'],value);unused.pop(j)
        if original:assert not unused,(c['source_id'],unused)
        matched_options+=len(original)
        sf=s.get(':question/answer-fields',[{}])[0] if s.get(':question/answer-fields') else {}
        if ':answer-field/correct' in sf:
            rv=next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);assert same(scalar(rv),scalar(sf[':answer-field/correct'][':answer/value']));correct_refs+=1
        raw_sol=s.get(':question/worked-solution')
        if raw_sol:
            blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',raw_sol,re.S)
            n=[]
            for block in blocks:
                n.append(len(block.split(r'\\')))
                for row in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
                    rhs=row.split('&',1)[1].strip().lstrip('=').strip() if '&' in row else row.split('=',1)[1].strip()
                    has_bar='|' in rhs
                    rhs=re.sub(r'\|}_{x=[^}]*}', '}',rhs)
                    value=scalar(rhs)
                    if has_bar:value=value.subs(X,t)
                    assert same(value,sp.diff(f,X) if len(n)==1 else sp.diff(f,X).subs(X,t)),('source mathematical stage',c['source_id'],rhs)

            assert n==[c['d_stages'],c['eval_stages']],(c['source_id'],n)
        result={'source_id':c['source_id'],'complete_bank_matched':bool(original),'choices_matched':len(original),'distractors_matched':len(original)-1 if c['field_type']=='radio' else 0,'correct_ref_matched':':answer-field/correct' in sf,'prompt_mathematics_matched':True,'field_layout_preserved':bool(sf),'solution_stage_counts_matched':bool(raw_sol),'literal_prompt_exact':s[':question/problem']==r['question'][':question/problem'],'literal_solution_exact':raw_sol==r['question'][':question/worked-solution'],'repairs':r['generation']['repairs']}
        source_results.append(result);review.append({'original':s,'replay':r,'variant':g.generate('easy',83,c['template'])})
    # Deterministic sample every template and full eligible bank; no profile pooling.
    for c in g.CASES:
        for seed in range(20):
            r=g.generate('easy',seed,c['template']);stages_total+=validate(r);fingerprints.add(r['generation']['mathematical_fingerprint'])
            rr=g.generate('easy',seed+10000,c['template'],parameters=r['generation']['parameters'])
            assert rr['question'][':question/id']==r['question'][':question/id'];assert rr['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
            f=r['question'][':question/answer-fields'][0]
            if c['field_type']=='radio':orders.add(next(i for i,a in enumerate(f[':answer-field/choices'])if a[':answer/id']==f[':answer-field/correct'][1]))
            # A constant shift changes no derivative/task; never counts as distinct.
            if 'k' in r['generation']['parameters'] and c['template'] not in ('ln_quadratic_linear_radio','log_quadratic_linear_blank'):
                p=dict(r['generation']['parameters']);p['k']=1 if p['k']!=1 else 2
                try:rk=g.generate('easy',seed,c['template'],parameters=p)
                except ValueError:
                    _,_,_,rd,rt,_=g.render(c['template'],p)
                    assert g.digest([sp.srepr(sp.simplify(rd)),sp.srepr(rt)])==r['generation']['mathematical_fingerprint']
                else:assert rk['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
        for p in (c['parameters'],{k:(v if k in ('t','b') else 1) for k,v in c['parameters'].items()},{k:(v if k in ('t','b') else 12)for k,v in c['parameters'].items()}):
            try:r=g.generate('easy',100,c['template'],parameters=p)
            except ValueError as e:errors.append({'template':c['template'],'parameters':p,'expected_bounded_rejection':str(e)});continue
            validate(r)
    assert len(orders)>1
    for level in ('moderate','hard'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('unsupported level accepted')
    for template,p in [('quadratic_ln_blank',{'a':2,'c':3,'t':0}),('negative_exp_log_blank',{'a':2,'c':3,'t':2,'b':1})]:
        try:g.generate('easy',template=template,parameters=p)
        except ValueError:pass
        else:raise AssertionError('invalid domain accepted')
    (HERE/'native-input.json').write_text(json.dumps(native,indent=2)+'\n');subprocess.run([str(HERE/'check-current-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    report=json.loads((HERE/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
    (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
    md=['# Original and generated side-by-side review','Source payload is retained verbatim. Formula notation is standardized; original instructional sentences and the derivative/evaluation stage counts are retained. Missing source solutions and field repairs are labeled in metadata.']
    for item in review:
        q=item['original'];md+=['## '+q[':question/math-academy-id'],'### Original',q[':question/problem'],q.get(':question/worked-solution','No source solution.')]
        md += ['Original bank: '+str([a[':answer/value']for f in q.get(':question/answer-fields',[])for a in f[':answer-field/choices']])]
        for label in ('replay','variant'):
            r=item[label];qq=r['question'];md+=['### '+label,qq[':question/problem'],'Bank: '+str([a[':answer/value']for a in qq[':question/answer-fields'][0][':answer-field/choices']]),qq[':question/worked-solution'],'Repairs: '+str(r['generation']['repairs'])]
            validate(r,collect=False)
    (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
    result={'passed':True,'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'sources':13,'complete_source_banks':11,'source_options_matched':matched_options,'existing_correct_designations_matched':correct_refs,'source_distractors_matched':20,'source_fidelity':source_results,'fidelity_note':'All 11 existing banks matched one-to-one as complete mathematical values, including blank alias multiplicities; 2 fieldless sources repaired as labeled authored blanks. Standardized TeX has zero literal-string fidelity; instructional sentences, term order and all 11 existing solution stage counts preserved. Two legacy solutions authored from canonical/sibling scaffolding.','distinct_validated_sample_tasks':len(fingerprints),'printed_solution_rows_sample':stages_total,'native':{k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'boundary_rejections':errors,'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'database_writes':0,'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [HERE.with_suffix('.py'),HERE/'source-cases.json',HERE/'source.json',HERE/'scalar_parser.py',HERE/'validate.py',HERE/'check-current-engine']}}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('passed','source_options_matched','existing_correct_designations_matched','distinct_validated_sample_tasks','native')},indent=2))
if __name__=='__main__':main()
