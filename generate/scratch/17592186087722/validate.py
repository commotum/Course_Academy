#!/usr/bin/env python3
"""Fail-fast displayed-math, full-set fidelity, scope, identity, and native QA."""
import importlib.util,json,re,subprocess,hashlib
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('ranges',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2))
def independent_image(expr,d):
    """Endpoint/critical-value theorem, independent of generator function_range."""
    critical=sp.solve(sp.diff(expr,g.T),g.T)
    candidates=[]
    for b,is_open,side in [(d.start,d.left_open,'+'),(d.end,d.right_open,'-')]:
        value=sp.limit(expr,g.T,b,dir=side)
        attained=b not in (-sp.oo,sp.oo) and not is_open
        candidates.append((value,attained))
    for t in critical:
        if t.is_real and d.contains(t)==sp.true:candidates.append((sp.simplify(expr.subs(g.T,t)),True))
    low=min(a for a,_ in candidates);high=max(a for a,_ in candidates)
    return sp.Interval(low,high,left_open=not any(v==low and yes for v,yes in candidates),right_open=not any(v==high and yes for v,yes in candidates))
def complete_answer(record):
    q=record['question'];fields=q[':question/answer-fields'];sets={}
    for f in fields:
        ref=f[':answer-field/correct'][1];a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==ref)
        if f[':answer-field/type'].endswith('/radio'):return g.parse_sets(a[':answer/value'])
    ordered=sorted(fields,key=lambda f:f[':answer-field/key'])
    for i in range(0,len(ordered),2):
        val=''.join(f[':answer-field/choices'][0][':answer/value'] for f in ordered[i:i+2]);sets.update(g.parse_sets(('x' if i==0 else 'y')+val))
    return sets

def stage_checks(record):
    q=record['question'];x,y,d,_=g.parse_prompt(q[':question/problem']);assign={'x':x,'y':y,'t':g.T};count=0
    def expr(tex):
        # Function notation in the authored endpoint arithmetic means evaluation.
        tex=re.sub(r'([xy])\(([^()]*)\)',lambda m:'('+sp.latex(assign[m[1]].subs(g.T,g.latex_expr(m[2])))+')',tex)
        symbols={'x':sp.Symbol('x'),'y':sp.Symbol('y')}
        return g.latex_expr(tex).subs({symbols['x']:x,symbols['y']:y})
    solution=q[':question/worked-solution']
    for aligned in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S):
        rows=aligned.split('\\\\');lhs=None
        for row in rows:
            a,b=row.split('=',1);a=a.replace('&','').strip()
            if a:lhs=expr(a)
            assert sp.simplify(lhs-expr(b))==0,('Bad displayed square completion',row,q[':question/problem']);count+=1
    noaligned=re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}','',solution,flags=re.S)
    for outer,inner in re.findall(r'\$\$(.*?)\$\$|\$([^$]*?)\$',noaligned,re.S):
        tex=(outer or inner).strip().rstrip('.,:')
        if not tex or '\\in' in tex or '∈' in tex or ' and ' in tex:continue
        if ',' in tex:
            if re.search(r'[xy]\s*(?:\\ge|\\le|>|<)',tex):
                pairs=g.parse_sets(tex)
                assert pairs=={v:independent_image({'x':x,'y':y}[v],d) for v in pairs},('false complete solution constraint',tex)
                count+=len(pairs)
            continue
        bits=re.split(r'(\\geq(?![A-Za-z])|\\leq(?![A-Za-z])|\\ge(?![A-Za-z])|\\le(?![A-Za-z])|>|<|=)',tex)
        if len(bits)<3:continue
        for a,op,b in zip(bits[0::2],bits[1::2],bits[2::2]):
            # Ignore explanatory text; every supported actual arithmetic relation is checked.
            try:delta=sp.simplify(expr(a)-expr(b))
            except Exception as exc:raise AssertionError(('Unreadable solution stage',tex,str(exc)))
            if op=='=':
                if re.fullmatch(r't',a.strip()):
                    context=solution[solution.find('$'+tex+'$'):solution.find('$'+tex+'$')+110]
                    expected=sp.false if 'outside the given domain' in context else sp.true
                    assert d.contains(expr(b))==expected,('incorrect named-parameter admissibility',tex,context)
                else:assert delta==0,('false equation',tex,delta)
            else:
                rng=independent_image(delta,d) if delta.has(g.T) else sp.FiniteSet(delta)
                target=sp.Interval(0,sp.oo,left_open=op=='>') if op in ('\\ge','\\geq','>') else sp.Interval(-sp.oo,0,right_open=op=='<')
                assert rng.is_subset(target)==True,('false inequality',tex,rng,target)
            count+=1
    return count

def check(record):
    q=record['question'];x,y,d,_=g.parse_prompt(q[':question/problem']);answer=complete_answer(record)
    assert isinstance(d,sp.Interval)
    truth={v:independent_image({'x':x,'y':y}[v],d) for v in answer}
    assert answer==truth,('Displayed prompt disagrees with full answer',q[':question/problem'],truth,answer)
    for f in q[':question/answer-fields']:
        choices=f[':answer-field/choices'];ids=[a[':answer/id'] for a in choices]
        assert len(set(ids))==len(ids) and f[':answer-field/correct'][1] in ids
        if f[':answer-field/type'].endswith('/radio'):
            sets=[g.parse_sets(a[':answer/value']) for a in choices]
            assert len(sets)==5 and len({str(s) for s in sets})==5 and sum(s==truth for s in sets)==1
            assert all(set(s)==set(truth) for s in sets)
            if len(truth)==2 and record['generation']['bank_profile']=='authored-endpoint-bank':
                for v in truth:assert sum(s[v]==truth[v] for s in sets)>=2,('one coordinate alone identifies answer',v,sets)
    assert q[':question/problem'].count('$')%2==0 and q[':question/worked-solution'].count('$')%2==0
    for text in (q[':question/problem'],q[':question/worked-solution']):assert text.count('{')==text.count('}')
    return stage_checks(record)

def engine_case(record,label):
    checks=[]
    for i,f in enumerate(record['question'][':question/answer-fields']):
        cid=f[':answer-field/correct'][1]
        if f[':answer-field/type'].endswith('/radio'):
            checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'owned radio option'} for a in f[':answer-field/choices'])
        else:
            correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)
            checks.append({'field_index':i,'submitted':correct,'expected':'accepted','purpose':'canonical split inequality fragment'})
            if '\\' in correct or correct in ('>','<'):
                wrong='<' if 'ge' in correct or correct=='>' else '>'
                checks.append({'field_index':i,'submitted':wrong,'expected':'rejected','purpose':'wrong direction'})
            else:
                value=g.latex_expr(correct);eq='('+str(2*value.p)+')/('+str(2*value.q)+')' if value.is_Rational else str(value)
                checks.extend([{'field_index':i,'submitted':eq,'expected':'accepted','purpose':'unreduced equivalent rational fragment'},{'field_index':i,'submitted':str(value+1),'expected':'rejected','purpose':'wrong endpoint'}])
    return {'label':label,'record':record,'checks':checks}

def main():
    sources=g.SOURCE['record'][':knowledge-point/questions'];cases=[];engine=[];review=[];fidelity=[];stages=0
    banks=choices_total=matched_correct_refs=blank_fields=0
    for q in sources:
        sid=q[':question/math-academy-id'];ft=g.TEMPLATES[sid]['kind'];profile='observed:'+sid if ft=='radio' and q.get(':question/answer-fields') else 'blank-observed' if ft=='blank' else 'authored-endpoint-bank'
        p={'sx':1,'sy':1};r=g.generate('moderate',11,sid,parameters=p,profile=profile);stages+=check(r)
        assert r['question'][':question/problem']==q[':question/problem']
        if q.get(':question/worked-solution'):assert r['question'][':question/worked-solution']==q[':question/worked-solution']
        fields={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']};matches=0;refs=0
        for sf in q.get(':question/answer-fields',[]):
            gf=fields[sf[':answer-field/key']];original=sf[':answer-field/choices'];actual=gf[':answer-field/choices']
            assert sorted(a[':answer/value'] for a in original)==sorted(a[':answer/value'] for a in actual)
            matches+=len(original);choices_total+=len(original)
            if sf.get(':answer-field/correct'):
                actualcorrect=next(a for a in actual if a[':answer/id']==gf[':answer-field/correct'][1])
                assert actualcorrect[':answer/value']==sf[':answer-field/correct'][':answer/value'];refs+=1;matched_correct_refs+=1
            if ft=='blank':blank_fields+=1
        if ft=='radio' and q.get(':question/answer-fields'):banks+=1
        fidelity.append({'source_id':sid,'matched_values':matches,'matched_observed_correct_refs':refs,'observed_correct_refs':sum(':answer-field/correct' in f for f in q.get(':question/answer-fields',[])),'raw_solution_present':bool(q.get(':question/worked-solution')),'designation_origin':'authored repair' if sid in ('q-16203','q-16205','q-73604') else 'observed'})
        cases.append({'source_id':sid,'template':sid,'parameters':p,'bank_profile':profile,'level':'moderate','level_origin':'observed' if ':question/difficulty' in q else 'authored supported assignment'})
        engine.append(engine_case(r,sid));review.append({'label':'original replay '+sid,'record':r})
        for k in (2,3):
            params={'sx':k,'sy':4-k};v=g.generate('moderate',k,sid,parameters=params,profile=profile);stages+=check(v)
            if q.get(':question/worked-solution'):
                stripmath=lambda text:re.sub(r'\$\$.*?\$\$|\$[^$]*?\$', '<math>',text,flags=re.S)
                assert stripmath(v['question'][':question/worked-solution'])==stripmath(q[':question/worked-solution'])
                assert v['question'][':question/worked-solution'].count('\\\\')==q[':question/worked-solution'].count('\\\\')
                # Every nonfinal source square-completion arithmetic component survives verbatim.
                srcaligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
                outaligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',v['question'][':question/worked-solution'],re.S)
                for original,transported in zip(srcaligned,outaligned):
                    originalrows=original.split('\\\\');newrows=transported.split('\\\\');variable=originalrows[0].split('=')[0].replace('&','').strip();scale=params['s'+variable]
                    for originalrow,newrow in zip(originalrows[:-1],newrows[:-1]):
                        expected=str(scale)+r'\left('+originalrow.split('=',1)[1].strip()+r'\right)'
                        assert newrow.split('=',1)[1]==expected,('collapsed or altered arithmetic stage',sid,originalrow,newrow)
            review.append({'label':'generated observed transport '+sid+' '+str(k),'record':v});engine.append(engine_case(v,sid+' transport '+str(k)))
        for sx,sy in ((1,6),(6,1),(6,6)):
            edge=g.generate('moderate',19,sid,parameters={'sx':sx,'sy':sy},profile=profile);stages+=check(edge)
        # Independently validate default bank rather than relying on observed transport.
        if ft=='radio':
            r=g.generate('moderate',17,sid,parameters={'sx':2,'sy':3});stages+=check(r);engine.append(engine_case(r,sid+' authored bank'));review.append({'label':'generated authored bank '+sid,'record':r})
    # Every level varies domain orientation, endpoint inclusion, coefficient signs.
    unique={}
    for level in ('easy','moderate','hard'):
        fingerprints=set()
        for seed in range(60):
            r=g.generate(level,seed);stages+=check(r);fingerprints.add(r['generation']['parameter_fingerprint'])
            same=g.generate(level,seed+100,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['bank_profile']);assert same['question'][':question/id']==r['question'][':question/id']
            if seed<4:review.append({'label':'generated '+level+' '+str(seed),'record':r});engine.append(engine_case(r,level+' '+str(seed)))
        unique[level]=len(fingerprints);assert len(fingerprints)>=30
    # Vertices inside/outside and open endpoint whose alternate root is admissible.
    for bound,closed in [(-3,False),(0,False),(3,True),(3,False)]:
        p={'a':1,'b':-4,'c':1,'d':-1,'e':-2,'f':2,'bound':bound,'direction':'lower','closed':closed};r=g.generate('hard',parameters=p);stages+=check(r);engine.append(engine_case(r,'hard edge '+str(bound)+str(closed)))
    for sid in ('q-16203','q-73604','q-123767','q-327852','q-73617'):stages+=check(g.generate('moderate',template=sid,parameters={'sx':6,'sy':6}))
    # Domain must come from printed equations and both coordinate functions.
    altered=g.generate('moderate',template='q-73604',parameters={'sx':1,'sy':1});altered['question'][':question/problem']=altered['question'][':question/problem'].replace('t\\ge 0','t\\ge 2')
    try:check(altered)
    except AssertionError:pass
    else:raise AssertionError('Printed domain mutation was missed')
    # Reciprocal zero cannot be admissible, even when the other coordinate is asked.
    x,y,d,_=g.parse_prompt('Given $x=\\frac{1}{t},y=1-t,t\\ge0$');assert d==sp.Interval.open(0,sp.oo)
    # Finite intervals are parsed as printed, rather than assumed to be real-line.
    for notation,expected in [(r't\in(2,4)',sp.Interval.open(2,4)),(r't\in[-2,4]',sp.Interval(-2,4))]:
        x,y,d,_=g.parse_prompt('Given $x=t^2-4t,y=t,'+notation+'$');assert d==expected
        assert independent_image(x,d)==g.function_range(x,g.T,d)
    for level,name,p in [('easy','affine_endpoint',{'a':0,'b':1,'bound':0,'direction':'lower','closed':True}),('hard','two_quadratic_endpoints',{'a':1,'b':-8,'c':0,'d':1,'e':2,'f':0,'bound':0,'direction':'lower','closed':True}),('moderate','q-16199',{'sx':7,'sy':1})]:
        try:g.generate(level,template=name,parameters=p)
        except ValueError:pass
        else:raise AssertionError('Invalid explicit workload accepted')
    write('source-cases.json',cases);write('source-fidelity.json',fidelity);write('engine-input.json',engine)
    harness=REPO/'generate/runs/current/check-engine';subprocess.run([str(harness),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
    write('review.json',review)
    chunks=['# Review\n\nOriginal replay means observed prompt and complete bank, with explicitly authored repairs where the capture is missing fields/designations. Generated observed transport means every complete option is carried through a positive coordinate dilation; it does not claim a recovered distractor intention.']
    for item in review:
        meta=item['record']['generation']
        chunks.extend(['## '+item['label'],'Level origin: '+meta['level_origin']+'. Bank origin: '+meta['bank_origin']+'. Correct designation: '+('authored repair' if meta['authored_correct_designation'] else 'mathematically derived with observed source designation where available')+'.',g.markdown(item['record'])])
    (ROOT/'review.md').write_text('\n\n'.join(chunks))
    report={'status':'passed','source_basis':1356,'database_writes':0,'source_questions':23,'observed_rated_moderate':21,'unrated_authored_moderate':2,'complete_source_radio_banks_matched':banks,'source_radio_option_values_matched':banks*5,'source_blank_fields_matched':blank_fields,'all_source_field_values_matched':choices_total,'observed_correct_designations_matched':matched_correct_refs,'authored_designations':3,'fieldless_authored_bank':1,'source_worked_solutions_exact':21,'source_worked_solutions_absent_authored':2,'displayed_math_stages_checked':stages,'sample_unique_assessed_tasks_of_60':unique,'all_source_profiles_scale_corners':'passed (1,6), (6,1), (6,6)','generator_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'native_report':'engine-validation.json','native_input_sha256':hashlib.sha256((ROOT/'engine-input.json').read_bytes()).hexdigest(),'native_binary_sha256':hashlib.sha256(harness.read_bytes()).hexdigest(),'scope':'same coordinate range method, all three levels','limitations':['Missing refs q-16203/q-16205 are independently authored designations, not observed matches.','q-73604 original widget is not present in available local capture; raw fieldless EDB record retained, supported assessment authored.','Observed opaque bank bounds are transported complete-set profiles, never inferred error intentions.'],'checks':{'complete_mathematical_sets':'passed','printed_domain_and_coordinate_math':'passed','displayed_solution_stages':'passed','full_prompt_and_solution_replay':'passed','all_levels_scope_and_bounds':'passed','identity_and_blank_native_grading':'passed'}}
    write('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
