"""Printed-content oracle, source fidelity, mutation tests and native small batches."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('perp_points_validation',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y=g.parser.SYMS['x'],g.parser.SYMS['y'];parse=g.parser.parse
def save(n,v):(H/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def normalize_line(t):
    l,r=t.replace('&','').split('=');p=sp.Poly(sp.expand(parse(l)-parse(r)),x,y)
    assert p.total_degree()==1
    a=p.coeff_monomial(x);b=p.coeff_monomial(y);c=p.coeff_monomial(1);scale=a or b
    assert scale
    return tuple(sp.cancel(z/scale) for z in (a,b,c))
def prompt_data(q):
    text=q[':question/problem'];assert 'perpendicular' in text and 'line passing through the points' in text
    pts=[tuple(map(int,z)) for z in re.findall(r'\((-?\d+),\s*(-?\d+)\)',text)]
    assert len(pts)==3
    (h,k),(a,b),(c,d)=pts
    assert c!=a and d!=b
    reference=sp.Rational(d-b,c-a);slope=sp.Rational(a-c,d-b);intercept=k-slope*h
    return pts,reference,slope,intercept
def check(record):
    q=record['question'];s=record['generation']['template'];pts,r,m,b=prompt_data(q);(h,k),A,B=pts
    # Reference line is independently reconstructed from BOTH displayed endpoints.
    reference_b=A[1]-r*A[0]
    assert all(z[1]==r*z[0]+reference_b for z in (A,B)) and m*r==-1
    f=q[':question/answer-fields'][0];blank=f[':answer-field/type'].endswith('/blank');bank=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
    target=normalize_line('y='+g.tex(m*x+b));keys=[]
    assert len(bank)==(1 if blank else 5)
    for a in bank:
        key=normalize_line('y='+a[':answer/value'] if blank else a[':answer/value']);keys.append(key)
        assert (key==target)==(a[':answer/id']==correct),('wrong full line or correct marker',s,a)
    assert len(set(keys))==len(keys)
    sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
    assert len(blocks)==2
    slope_rows=3+int(s in {'q-103455','q-215768','q-237224','q-237225'})+int(s in {'q-215768','q-23453','q-237036','q-72567','q-72568'})
    target_rows=5 if s in {'q-237036','q-72567','q-72568'} else 4
    assert [len(z.split('\\\\')) for z in blocks]==[slope_rows,target_rows],('erased/reordered operative stage',s)
    # Prose reference endpoints and target cannot be stale, even if key stayed right.
    pairs=[tuple(map(int,z)) for z in re.findall(r'\((-?\d+),\s*(-?\d+)\)',sol)]
    assert pairs==[A,B,pts[0]],('wrong reference or target in solution',pairs,pts)
    for row in blocks[0].split('\\\\')[1:]:
        lhs,rhs=row.replace('&','').split('=',1);assert not lhs.strip()
        assert sp.cancel(parse(rhs.rstrip('. '))-r)==0,('wrong slope computation',row,r)
    # The substituted slope numerator/denominator must use the actual supplied
    # endpoints, not merely happen to give an equal slope from unrelated points.
    subrow=blocks[0].split('\\\\')[1]
    def minus(a,b):return str(a)+'-'+('('+str(b)+')' if b<0 else str(b))
    expected=r'\frac{'+minus(B[1],A[1])+'}{'+minus(B[0],A[0])+'}'
    assert re.sub(r'\s','',subrow.split('=',1)[1])==expected
    rec=re.search(r'm\\cdot\s*\((.*?)\)\s*=\s*-1.*?m\s*=\s*(.*?)\.',sol,re.S)
    assert rec and parse(rec[1])==r and parse(rec[2])==m,('wrong reciprocal/sign',sol)
    targetblock=blocks[1].split('\\\\')
    for row in targetblock[1:]:
        assert normalize_line(row)==target,('wrong point-slope/expansion/final equation',row)
    # Substitution must explicitly preserve the actual target, including a stage
    # algebraically equal to the next stage at zero or one coordinates.
    subrow=targetblock[1].replace('&','');left,right=subrow.split('=',1)
    assert left.strip()==minus('y',k) and ('('+minus('x',h)+')') in right.replace(' ','')
    g.fmt.validate_generated_record(record)
    return True

def native(record,label):
    pts,r,m,b=prompt_data(record['question']);(h,k),_,_=pts;f=record['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'owned choice ID; full equation independently validated'} for a in f[':answer-field/choices']]
        checks += [{'submitted':v,'expected':'unresolved','purpose':'foreign/malformed submission; separate from owned choice IDs'} for v in ('garbage','999999','00000000-0000-0000-0000-000000000000')]
    else:
        checks=[{'submitted':v,'expected':e,'purpose':p} for v,e,p in [
            (g.tex(m*x+b),'accepted','canonical RHS'),(str(m*x+b),'accepted','expanded RHS equivalent'),
            (f'({m.p}*x+({b*m.q}))/{m.q}','accepted','single fraction RHS equivalent'),
            (f'({m})*(x-({h}))+({k})','accepted','point-slope RHS equivalent'),
            ('y='+g.tex(m*x+b),'unresolved','full equation unsupported for supplied y= RHS blank'),
            (g.tex(-m*x+y)+'='+g.tex(b),'unresolved','standard equation unsupported for supplied y= RHS blank'),
            (str(m*x+b+1),'rejected','ordinary wrong intercept'),(str(-m*x+b),'rejected','ordinary wrong perpendicular sign'),
            ('garbage','unresolved','malformed scalar submitted separately')]]
    return {'label':label,'record':record,'checks':checks}

def main():
    engine=ROOT/'generate/runs/current/check-engine';engine_sha=hashlib.sha256(engine.read_bytes()).hexdigest()
    assert engine_sha=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
    raw=[g.raw_replay(s) for s in g.SOURCES];save('raw-source-replay.json',{'source_basis':2275,'questions':raw})
    summary=[];cases=[];review=[];inputs=[]
    for s,q in g.SOURCES.items():
        level=g.source_level(s);out=g.generate(level,0,s,g.original(s));check(out)
        assert raw[list(g.SOURCES).index(s)]['question']==q
        of=q[':question/answer-fields'][0];f=out['question'][':question/answer-fields'][0];old=of.get(':answer-field/choices',[]);blank=f[':answer-field/type'].endswith('/blank')
        compare=lambda z:parse(z[':answer/value']) if blank else normalize_line(z[':answer/value'])
        if old:assert sorted(map(str,map(compare,old)))==sorted(map(str,map(compare,f[':answer-field/choices'])))
        if ':answer-field/correct' in of:
            a=next(z for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert compare(a)==compare(of[':answer-field/correct'])
        exact=s not in g.INCOMPLETE and s!=g.GRAPH
        if exact:
            assert out['question'][':question/problem']==g.fmt.normalize_prose(q[':question/problem'])
            assert out['question'][':question/worked-solution']==g.fmt.normalize_prose(q[':question/worked-solution'])
        summary.append({'source_id':s,'raw_attributes_exact':True,'raw_eligible':False,'prompt_and_ordered_solution_reproduced':exact,'complete_observed_bank_matched':bool(old),'matched_values':len(old),'matched_distractors':len(old)-1 if not blank else 0,'captured_correct_ref_matched':':answer-field/correct' in of,'missing':raw[list(g.SOURCES).index(s)]['generation']['missing'],'served_origin':out['generation']['origin']})
        review.append('## Captured original / '+s+'\n\n'+q[':question/problem']+'\n\n'+'\n'.join('$'+z[':answer/value']+'$' for z in old)+'\n\n'+q.get(':question/worked-solution','**Worked solution missing in immutable evidence.**'))
        for i in range(3):
            r=out if i==0 else g.generate(level,2275+i,s);check(r)
            cases.append({'source_id':s,'difficulty':level,'template':s,'parameters':r['generation']['parameters'],'bank_profile':r['generation']['bank_profile'],'record':r,'case_role':'original parameters or explicit repair' if i==0 else 'changed variant'})
            inputs.append(native(r,s+'-'+str(i)));review.append('## '+s+' / '+str(i)+'\n\n'+g.markdown(r))
    # All hard moderate-family templates are explicitly authored, same workload.
    for s in g.SOURCES:
        if g.source_level(s)!='moderate':continue
        for i in range(3):
            r=g.generate('hard',9000+i,s);check(r);cases.append({'source_id':s,'difficulty':'hard','template':s,'parameters':r['generation']['parameters'],'bank_profile':r['generation']['bank_profile'],'record':r,'case_role':'authored hard; no observed hard source'});review.append('## Authored hard / '+s+' / '+str(i)+'\n\n'+g.markdown(r));inputs.append(native(r,'hard-'+s+'-'+str(i)))
    counts={};coverage={}
    for level in g.LEVELS:
        records=g.batch(level,150,10000);counts[level]=len(records);slots={k:set() for k in ('target_x','target_y','reference1_x','reference1_y','dx','dy','slope','profile','template')}
        for r in records:
            check(r);pts,ref,m,b=prompt_data(r['question']);P,A,B=pts
            for key,val in [('target_x',P[0]),('target_y',P[1]),('reference1_x',A[0]),('reference1_y',A[1]),('dx',B[0]-A[0]),('dy',B[1]-A[1]),('slope',str(m)),('profile',r['generation']['bank_profile']),('template',r['generation']['template'])]:slots[key].add(val)
        coverage[level]={k:sorted(v,key=str) for k,v in slots.items()};inputs.extend(native(r,level+'-sample-'+str(i)) for i,r in enumerate(records[:4]))
    # Source-profile order was fixed before constructing the complete bank.
    assert set(coverage['easy']['profile'])=={None,'q-22642','q-23453'}
    assert set(coverage['moderate']['profile'])==set(coverage['hard']['profile'])=={None,'q-103440','q-103455','q-72567','q-72568'}
    base=g.generate('moderate',1,'q-237036',{'P':[-5,5],'A':[-4,-3],'B':[2,3]});mutations=[]
    changes=[('wrong reference point',lambda q:q.__setitem__(':question/problem',q[':question/problem'].replace('(-4,-3)','(-3,-3)'))),('wrong reciprocal sign',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('m=-1.','m=1.'))),('stale target',lambda q:q.__setitem__(':question/problem',q[':question/problem'].replace('(-5,5)','(-4,5)'))),('stale slope coefficient',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('=-x-5','=-2x-5'))),('erased algebraically equal stage',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace(r' \\ y-5 & =-1(x+5)','')))]
    for name,change in changes:
        bad=copy.deepcopy(base);change(bad['question']);assert bad!=base,name
        try:check(bad)
        except (AssertionError,ValueError):mutations.append({'mutation':name,'caught':True})
        else:raise AssertionError('uncaught '+name)
    # Changed target alone forces all stages/keys to change; ref points held fixed.
    changed=g.generate('moderate',1,'q-237036',{'P':[-4,5],'A':[-4,-3],'B':[2,3]});check(changed)
    assert base['generation']['mathematical_fingerprint']!=changed['generation']['mathematical_fingerprint']
    # Line comparators include horizontal/vertical equations, though this source
    # solution branch does not support generating their different reasoning steps.
    assert normalize_line('x=2')==normalize_line('-3x=-6') and normalize_line('y=1')==normalize_line('2y=2')
    assert normalize_line('x=2')!=normalize_line('y=2')
    # Zero and one remain normal eligible answers, including constant cancellation.
    for k in (0,1):check(g.generate('easy',0,'q-237224',{'P':[0,k],'A':[0,0],'B':[2,3]}))
    for k in (0,1):check(g.generate('moderate',0,'q-237036',{'P':[3,k-2],'A':[0,0],'B':[2,3]}))
    a=g.generate('moderate',1,'q-237036',{'P':[-5,5],'A':[-4,-3],'B':[2,3]});z=g.generate('moderate',999,'q-237036',{'P':[-5,5],'A':[-4,-3],'B':[2,3]});assert a['question']==z['question']
    z=g.generate('moderate',1,'q-237036',{'P':[-5,5],'A':[0,0],'B':[2,2]});assert a['generation']['mathematical_fingerprint']==z['generation']['mathematical_fingerprint'] and a['question'][':question/id']!=z['question'][':question/id']
    save('sourcecases.json',{'source_basis':2275,'cases':cases});save('source-replay.json',{'source_basis':2275,'sources':summary,'raw_exact':len(raw),'complete_observed_banks':sum(bool(z['complete_observed_bank_matched']) for z in summary),'observed_values':sum(z['matched_values'] for z in summary),'observed_distractors':sum(z['matched_distractors'] for z in summary),'unrecoverable_graph':g.GRAPH,'incomplete':sorted(g.INCOMPLETE)})
    save('native-input.json',inputs);native_dir=H/'native';native_dir.mkdir(exist_ok=True);reports=[]
    for i in range(0,len(inputs),8):
        file='batch-'+str(i//8);ip=native_dir/(file+'-input.json');rp=native_dir/(file+'-report.json');batch=inputs[i:i+8]
        cached=ip.exists() and rp.exists() and json.loads(ip.read_text())==batch
        if not cached:
            save('native/'+file+'-input.json',batch);subprocess.run([str(engine),str(ip),str(rp)],check=True)
        reports.append(json.loads(rp.read_text()))
    report={k:sum(r[k] for r in reports) for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','database_writes')};report.update({'entry_point':'course_academy_engine::learning::grade_field','engine_sha256':engine_sha,'small_batch_size':8,'records':[z for r in reports for z in r['records']]});save('native-grading.json',report)
    baseline=json.loads((H/'registered-baseline.json').read_text());paths=sorted([str((ROOT/'generate/scratch/17592186175923.py').relative_to(ROOT)),*[str(p.relative_to(ROOT)) for p in (ROOT/'generate/scratch/17592186175923').rglob('*')]])
    assert paths==sorted(baseline['paths']);assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha for p,sha in baseline['files'].items())
    (H/'review.md').write_text('\n\n'.join(review)+'\n')
    save('validation.json',{'mathematics_passed':True,'distinct_random_records_checked':counts,'sourcecases_checked':len(cases),'slot_coverage':coverage,'mutations':mutations,'changed_target_reference_fixed_checked':True,'registered_full_tree_immutable':True,'no_valid_answers_pruned':True,'native_counts':{k:v for k,v in report.items() if k.endswith('checks')},'limitations':['q-167797 reference graph missing in evidence; raw replay ineligible; served text repair uses explicitly authored reference points at evidenced slope -3.','Hard source absent; hard is authored same-method moderate workload.','Full equations unsupported for RHS-only blanks, separate from valid equivalent RHS.','Malformed/foreign submissions unresolved, separately reported.']})
    print('Verified',counts,'sourcecases',len(cases),'native',report['accepted_checks'],report['rejected_checks'],report['documented_unresolved_checks'])
if __name__=='__main__':main()
