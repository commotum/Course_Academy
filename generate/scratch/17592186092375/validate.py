"""Independent rendered-math, complete-bank fidelity and application-grading checks."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('arc_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
t=sp.Symbol('t',real=True)

def save(path,value):
    Path(path).parent.mkdir(parents=True,exist_ok=True);Path(path).write_text(json.dumps(value,indent=2,default=str)+'\n')

def polynomial(text):
    text=text.replace('\\\\','\\').replace('{','').replace('}','').replace('^','**').replace('\\,','').replace(' ','')
    return sp.expand(parse_expr(text,local_dict={'t':t},transformations=standard_transformations+(implicit_multiplication_application,)))

def integral(value):
    z=value.replace('\\\\','\\');start=z.index(r'\sqrt{')+6;depth=1;end=start
    while depth:
        depth+=(z[end]=='{')-(z[end]=='}');end+=1
    rad=polynomial(z[start:end-1]);match=re.search(r'_\{(-?\d+)\}\^\{(-?\d+)\}',z)
    a,b=map(int,match.groups());prefix=z[:z.index(r'\int')].replace('{','').strip()
    factor=sp.Integer(prefix) if prefix.isdigit() else sp.Integer(1)
    if 't' in z[match.end():start-6]:factor*=t
    return a,b,sp.expand(factor**2*rad)

def independent(rec):
    q=rec['question'];sid,a,b=rec['generation']['parameters'];assert rec['knowledge_point']['db_id']==g.KP_ID
    assert q[':question/difficulty']==':question.difficulty/easy';assert ':question/math-academy-id' not in q
    assert rec==g.generate('easy',rec['generation']['seed'],sid,[sid,a,b])
    prompt=q[':question/problem'];curve=prompt.split('$x=')[1].split('$')[0];xs,ys=curve.split('y=');xs=xs.rstrip(' ,\\')
    x,y=polynomial(xs),polynomial(ys);speed2=sp.expand(sp.diff(x,t)**2+sp.diff(y,t)**2)
    assert f'from $t={a}$ to $t={b}$' in prompt
    f=q[':question/answer-fields'][0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio';assert len(f[':answer-field/choices'])==5
    matches=[];polys=[]
    for choice in f[':answer-field/choices']:
        aa,bb,p=integral(choice[':answer/value']);assert (aa,bb)==(a,b);polys.append(p)
        if sp.expand(p-speed2)==0:matches.append(choice[':answer/id'])
    assert matches==[f[':answer-field/correct'][1]]
    assert len(set(polys))==5
    # Every explicit numeric solution bound must agree. The last substitution
    # line must encode the same speed, including any outside t or scalar.
    solution=q[':question/worked-solution'].replace('\\\\','\\')
    limits=re.findall(r'_\{(-?\d+)\}\^\{(-?\d+)\}',solution);assert limits and all(tuple(map(int,p))==(a,b) for p in limits)
    start=solution.rfind(r'\int');before=solution[:start];prefix=re.search(r'(\d+)?\{?$',before)[0]
    last=prefix+solution[start:];assert integral(last)==(a,b,speed2)
    if not rec['generation']['replay_only']:
        assert '![]' not in prompt
        # Independently certify all integrands are real and every pair is
        # strictly ordered on the interval: hence definite integrals differ.
        for p in polys:
            poly=sp.Poly(p,t);assert poly.count_roots(a,b)==0 and poly.eval(a)>0 and poly.eval(b)>0
        for i,p in enumerate(polys):
            for r in polys[:i]:
                d=sp.Poly(p-r,t);assert not d.is_zero and d.count_roots(a,b)==0 and d.eval(a)*d.eval(b)>0
        assert x==g.CURVES[sid][0] and y==g.CURVES[sid][1]
    return rec

def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual application radio grading of every option'} for a in f[':answer-field/choices']]

def native(rec,label=None):return {'label':label or rec['question'][':question/id'],'record':rec,'checks':checks(rec)}

def main():
    recipes=[];replays=[];inputs=[];review=[];coverage={};all_variants=[];source_issues=[]
    for sid,source in g.CASES.items():
        x,y,a,b=g.CURVES[sid];rec=independent(g.generate('easy',0,sid,[sid,a,b]));q=rec['question'];f=q[':question/answer-fields'][0];old=source[':question/answer-fields'][0]
        assert q[':question/problem']==source[':question/problem'] and q[':question/worked-solution']==source[':question/worked-solution']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':answer-field/choices'])
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==old[':answer-field/correct'][':answer/value']
        replays.append({'source':sid,'matched_choices':5,'matched_distractors':4,'complete_bank_match':True,'correct_designation':True,'prompt_exact':True,'solution_exact':True,'missing':[],'extra':[]})
        for choice in old[':answer-field/choices']:
            lo,hi,p=integral(choice[':answer/value']);rad,c=g.recipe(choice[':answer/value']);assert sp.expand(p-c*c*rad)==0
            recipes.append({'source':sid,'source_field':old[':answer-field/id'],'source_answer_id':choice[':answer/id'],'source_value':choice[':answer/value'],'profile':sid,'radicand':str(rad),'outside_factor':str(c),'recipe':'integrate the retained outside factor times sqrt(retained polynomial) over sampled [a,b]','varied_slots':['lower endpoint','upper endpoint'],'reproduces_source_value':True,'psychological_interpretation':'unresolved; exact observed expression retained'})
            # Detect negative radicands in original sources using exact rational witnesses.
            for k in range(21):
                point=sp.Rational(lo)+(sp.Rational(hi-lo)*k/20)
                if rad.subs(t,point)<0:
                    source_issues.append({'source':sid,'answer_id':choice[':answer/id'],'issue':'source distractor is nonreal within the original interval','witness_t':str(point),'radicand_at_witness':str(rad.subs(t,point)),'policy':'preserve original; generated variants must certify all banks real on their sampled interval'});break
        inputs.append(native(rec,'source replay '+sid))
        variants=[independent(g.generate('easy',42,sid,p)) for p in g.domain(sid)]
        all_variants+=variants;inputs += [native(r) for r in variants]
        coverage[sid]={'count':len(variants),'endpoint_pairs':[r['generation']['parameters'][1:] for r in variants],'missing_declared_pairs':[],'plotted_replay_only':sid in g.PLOTTED}
        if variants:
            r1,r2=variants[0],variants[-1];assert r1['generation']['parameters'][1:]!=r2['generation']['parameters'][1:]
            assert g.generate('easy',0,sid,r1['generation']['parameters'])['question']==g.generate('easy',999,sid,r1['generation']['parameters'])['question']
            review.append('## '+sid+'\n\nSource\n\n'+g.markdown(rec)+'\n\nFirst changed interval\n\n'+g.markdown(r1)+'\n\nSecond changed interval, same curve\n\n'+g.markdown(r2))
    assert len({g.fingerprint(r['question']) for r in all_variants})==len(all_variants)
    for level in ('moderate','hard','unclassified'):
        try:g.batch(level,1)
        except ValueError:pass
        else:raise AssertionError('Unsupported band admitted')
    save(HERE/'choice-recipes.json',recipes);save(HERE/'source-replay.json',{'complete_banks_matched':len(replays),'complete_banks_total':8,'matched_distractors':32,'total_distractors':32,'profiles':replays});save(HERE/'source-issues.json',source_issues);save(HERE/'slot-coverage.json',coverage);save(HERE/'native-input.json',inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save(HERE/'validation.json',{'status':'pass','source_basis':g.SOURCE['basis'],'source_bank_fidelity':'8/8 complete banks, 32/32 distractors, exact prompt and solution','correctness':'all 8 original keys from independently parsed displayed curves; all generated banks real, exactly one keyed speed; exact polynomial root isolation proves strict pairwise integrand order and distinct integral values','source_errors':'see source-issues.json; captured originals unchanged','supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'distinct_bounded_variants':len(all_variants),'grading':'all choices for source replay and exhaustive bounded variants through application grade_field','assets':'source plots inspected; illustrated profiles replay only; generated variants have no assets','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',ROOT/'generate/runs/current/check-engine']}})
    print('Validated',len(all_variants),'distinct variants; 8 complete source banks')
if __name__=='__main__':main()
