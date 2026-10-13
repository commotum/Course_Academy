"""Independent QA from displayed equations, stages and prose; native engine checks."""
import copy
import hashlib
import importlib.util
import json
import math as pymath
import re
import subprocess
import sys
import uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,k=sp.symbols('x y k')

def math(text):
    text=re.sub(r'\\(?:dfrac|frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',text).replace(' ','').strip().rstrip('.')
    assert re.fullmatch(r'[xyk0-9()+*/.\-]+',text),text
    return parse_expr(text,local_dict={'x':x,'y':y,'k':k},transformations=standard_transformations+(implicit_multiplication_application,))
def equation(text):
    left,right=text.strip().rstrip('.').split('=');return sp.expand(math(left)-math(right))
def equivalent(a,b):
    assert a.coeff(y)!=0 and b.coeff(y)!=0
    ratio=sp.cancel(a.coeff(y)/b.coeff(y))
    return ratio!=0 and sp.expand(a-ratio*b)==0

def formatting(text):
    assert text.count('$')%2==0
    braces=0
    for ch in text:
        if ch=='{':braces+=1
        elif ch=='}':braces-=1
        assert braces>=0
    assert braces==0
    assert '--' not in text and '+-' not in text and '\\frac{}' not in text
    assert '![' not in text

def displayed(record):
    assert record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=record['question'];gen=record['generation'];formatting(q[':question/problem'])
    pieces=re.findall(r'\$(.*?)\$',q[':question/problem'])
    assert len(pieces)==4 and pieces[2]=='k' and pieces[3]=='k ='
    known=equation(pieces[0]);unknown=equation(pieces[1])
    assert not known.has(k) and unknown.coeff(x)==k and unknown.coeff(y)!=0
    assert sp.Poly(known,x,y).total_degree()==1 and sp.Poly(unknown,x,y).total_degree()==1
    m=sp.cancel(-known.coeff(x)/known.coeff(y));b=unknown.coeff(y)
    assert m!=0 and b.is_Integer and 2<=abs(b)<=9
    assert abs(m.p)<=12 and 1<=m.q<=7
    h=sp.cancel(-known.subs({x:0,y:0})/known.coeff(y));c=-unknown.subs({x:0,y:0})
    assert h.is_Integer and -12<=h<=12 and c.is_Integer and -15<=c<=15
    p=gen['parameters']
    assert sp.Rational(p['slope'])==m and p['known_intercept']==h and p['unknown_y_coefficient']==b and p['unknown_constant']==c
    if not pieces[0].startswith('y = '):
        assert known.coeff(x)==m.p*p['known_scale'] and known.coeff(y)==-m.q*p['known_scale']
    answer=sp.solve(sp.Eq(-k/b,m),k)[0]
    assert not equivalent(known,unknown.subs(k,answer)), 'Coincident, not distinct parallel lines'
    form='mixed-form' if pieces[0].startswith('y = ') else 'two-standard'
    expected_fingerprint=g.digest({'assessed_known_form':form,'known_reduced_slope':str(m),'unknown_y_coefficient':int(b)})
    assert gen['parameter_fingerprint']==expected_fingerprint
    fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];assert f[':answer-field/type']==':answer-field.type/blank' and f[':answer-field/key']=='field-1'
    assert q[':question/problem'].count('{{field-1}}')==1 and q[':question/problem'].count('{{')==1
    for value in (q[':question/id'],f[':answer-field/id']):uuid.UUID(value)
    raw=gen['evidence_only']
    contents={'version':g.VERSION,'problem':q[':question/problem'],
              'solution':None if raw else q[':question/worked-solution'],
              'difficulty':None if raw else q[':question/difficulty'].split('/')[-1],
              'field_type':f[':answer-field/type'],'key':f[':answer-field/key'],
              'bank':None if raw else [a[':answer/value'] for a in f[':answer-field/choices']],
              'correct':None if raw else next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])}
    content_hash=hashlib.sha256(json.dumps(contents,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert gen['content_fingerprint']==content_hash
    expected_qid=str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question:'+content_hash))
    expected_fid=str(uuid.uuid5(uuid.UUID(g.KP_UUID),expected_qid+':field:field-1'))
    assert q[':question/id']==expected_qid and f[':answer-field/id']==expected_fid
    if not raw:
        for a in f[':answer-field/choices']:
            assert a[':answer/id']==str(uuid.uuid5(uuid.UUID(g.KP_UUID),expected_fid+':answer:'+a[':answer/value']))
    if gen['evidence_only']:
        assert not gen['eligible_for_learning']
        for attr in (':question/difficulty',':question/worked-solution'):assert attr not in q
        for attr in (':answer-field/choices',':answer-field/correct'):assert attr not in f
        return answer
    assert gen['eligible_for_learning']
    level=q[':question/difficulty'].split('/')[-1];assert level in g.SUPPORTED_LEVELS
    assert (form=='mixed-form')==(level=='easy')
    assert (m.q>1)==(level=='hard')
    if level=='hard':
        assert pymath.gcd(abs(int(b)),int(m.q))==1 and answer.q>1
        assert pymath.gcd(abs(int(known.coeff(x))),abs(int(known.coeff(y))))==1
    if gen['bank_profile']=='authored-blank' and form=='two-standard':
        assert pymath.gcd(abs(int(known.coeff(x))),abs(int(known.coeff(y))))==1
    bank=f[':answer-field/choices'];assert len(bank)==1
    assert f[':answer-field/correct']==[':answer/id',bank[0][':answer/id']]
    assert bank[0][':answer/type']==':answer.type/math' and '$' not in bank[0][':answer/value']
    assert math(bank[0][':answer/value'])==answer
    uuid.UUID(bank[0][':answer/id'])
    solution=q[':question/worked-solution'];formatting(solution)
    aligned=re.findall(r'\\begin\{aligned\}\n(.*?)\n\\end\{aligned\}',solution,re.S)
    assert len(aligned)==(1 if level=='easy' else 2)
    originals=[unknown] if level=='easy' else [known,unknown]
    for block,orig in zip(aligned,originals,strict=True):
        rows=block.split(' '+r'\\'+'\n');coeff=orig.coeff(y)
        expected_count=4 if coeff < -1 else 3
        assert len(rows)==expected_count,(rows,coeff)
        residuals=[equation(row.replace('&','')) for row in rows]
        assert all(equivalent(orig,row) for row in residuals),rows
        # Exact operation structure beyond equal mathematical values: original,
        # move x to RHS, optional sign normalization, then divide coefficient.
        assert sp.expand(residuals[0]-orig)==0
        lhs,rhs=rows[1].replace('&','').split('=')
        assert math(lhs)==coeff*y and math(rhs)==-orig.coeff(x)*x-orig.subs({x:0,y:0})
        if coeff < -1:
            lhs,rhs=rows[2].replace('&','').split('=')
            assert math(lhs)==-coeff*y and math(rhs)==orig.coeff(x)*x+orig.subs({x:0,y:0})
        lhs,rhs=rows[-1].replace('&','').split('=')
        assert math(lhs)==y and math(rhs)==sp.solve(orig,y)[0]
        assert rows[-1]!=rows[-2], 'A division row must not collapse into duplicate text'
    equalities=[block for block in re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S) if not block.startswith(r'\begin')];assert len(equalities)==1
    assert sp.solve(equation(equalities[0]),k)==[answer]
    slope_claims=re.findall(r'So, the slope is \$(.*?)\$\.',solution)
    assert len(slope_claims)==(1 if level=='easy' else 2)
    if level=='easy':
        claim=re.search(r'its slope is \$(.*?)\$\.',solution);assert math(claim[1])==m
    else:assert math(slope_claims[0])==m
    assert math(slope_claims[-1])==-k/b
    # Read the quoted source equations in prose as well as aligned rows.
    quoted=re.findall(r'To find the slope of the line \$(.*?)\$',solution)
    assert len(quoted)==len(originals)
    assert all(sp.expand(equation(text)-orig)==0 for text,orig in zip(quoted,originals))
    conclusion=re.search(r'Multiplying both sides by \$(.*?)\$ gives \$k=(.*?)\$\.',solution)
    assert conclusion and math(conclusion[1])==-b and math(conclusion[2])==answer
    final=re.search(r'Consequently, \$k=(.*?)\$\.',solution);assert final and math(final[1])==answer
    assert solution.startswith('For two lines to be parallel, they must have the same slope.')
    assert 'Since the slopes of the two lines must be equal, we must have' in solution
    return answer

def refresh_identity(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    answer=f[':answer-field/choices'][0][':answer/value']
    contents={'version':g.VERSION,'problem':q[':question/problem'],'solution':q[':question/worked-solution'],
              'difficulty':q[':question/difficulty'].split('/')[-1],
              'field_type':f[':answer-field/type'],'key':f[':answer-field/key'],'bank':[answer],'correct':answer}
    content_hash=hashlib.sha256(json.dumps(contents,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    q[':question/id']=g.uid('question:'+content_hash);f[':answer-field/id']=g.uid(q[':question/id']+':field:field-1')
    aid=g.uid(f[':answer-field/id']+':answer:'+answer);f[':answer-field/choices'][0][':answer/id']=aid;f[':answer-field/correct']=[':answer/id',aid]
    record['generation']['content_fingerprint']=content_hash
    return record

def checks(record):
    value=displayed(record)
    return [{'submitted':record['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'],'expected':'accepted','purpose':'canonical scalar fragment'},
            {'submitted':f'({2*value.p})/({2*value.q})','expected':'accepted','purpose':'unreduced equivalent rational'},
            {'submitted':str(value),'expected':'accepted','purpose':'plain rational spelling'},
            {'submitted':str(value+1),'expected':'rejected','purpose':'incorrect coefficient'},
            {'submitted':str(-value),'expected':'rejected','purpose':'actual sign reversal'}]
def write(name,value):(D/name).write_text(json.dumps(value,indent=2)+'\n')
def fails(operation):
    try:operation()
    except (ValueError,AssertionError):return
    raise AssertionError('Invalid or mutated record accepted')

def main():
    cases=[{'source_id':'q-214098','level':'easy','template':'mixed-form','parameters':{'slope':'2','known_intercept':5,'unknown_y_coefficient':3,'unknown_constant':9,'known_scale':1},'bank_profile':'raw-q-214098'},
           {'source_id':'q-214099','level':'moderate','template':'two-standard','parameters':{'slope':'4','known_intercept':1,'unknown_y_coefficient':-5,'unknown_constant':15,'known_scale':2},'bank_profile':'raw-q-214099'}]
    source={q[':question/math-academy-id']:q for q in g.SOURCE['record'][':knowledge-point/questions']}
    review=[];native=[];ledger=[];raw_records=[]
    for case in cases:
        kwargs={key:case[key] for key in ('level','template','parameters')}
        raw=g.generate(**kwargs,profile=case['bank_profile']);displayed(raw);raw_records.append(raw)
        q=raw['question'];old=source[case['source_id']];f=q[':question/answer-fields'][0];oldf=old[':question/answer-fields'][0]
        assert set(q)==set(old) and set(f)==set(oldf)
        assert q[':question/problem']==old[':question/problem']
        for key in set(old)-{':question/id',':question/answer-fields'}:assert q[key]==old[key]
        for key in set(oldf)-{':answer-field/id',':answer-field/type'}:assert f[key]==oldf[key]
        assert f[':answer-field/type']==oldf[':answer-field/type'][':db/ident']
        completed=g.generate(**kwargs,profile='completed-'+case['source_id']);answer=displayed(completed)
        assert completed['question'][':question/problem']==q[':question/problem']
        native.append({'label':'source-supported-completion/'+case['source_id'],'record':completed,'checks':checks(completed)})
        review.extend([{'label':case['source_id']+' raw public evidence','record':raw},{'label':case['source_id']+' authored answer/solution/level completion','record':completed}])
        # Changed inputs pass through each public raw and completed profile; no literal replay shortcut.
        changed={**case['parameters'],'slope':'-3','known_intercept':-2,'unknown_y_coefficient':4,'unknown_constant':7,'known_scale':1}
        for profile in (case['bank_profile'],'completed-'+case['source_id']):
            variant=g.generate(case['level'],parameters=changed,profile=profile)
            displayed(variant);assert variant['question'][':question/problem']!=q[':question/problem']
            assert variant['generation']['parameter_fingerprint']!=raw['generation']['parameter_fingerprint']
            review.append({'label':profile+' changed-parameter variant (authored level routing)','record':variant})
            if not variant['generation']['evidence_only']:native.append({'label':profile+'/changed','record':variant,'checks':checks(variant)})
        ledger.append({'source_id':case['source_id'],'exact_prompt':True,'attribute_presence_parity':True,'field_layout':True,'enum_normalization':'dict ident to required local enum string','identity_normalization':'content-derived UUIDs; original DB ids retained in raw evidence only','missing_bank_correct_solution_difficulty_preserved':True,'independently_solved_answer':str(answer),'observed_bank_count':0})
    count=0;coverage={};all_native_candidates=[]
    for level in g.SUPPORTED_LEVELS:
        records=g.batch(level,len(g.eligible_pairs(level)),84018)
        assert len({r['generation']['parameter_fingerprint'] for r in records})==len(records)
        slopes=set();bs=set();signs=set()
        for rec in records:
            value=displayed(rec);count+=1
            slopes.add(rec['generation']['parameters']['slope']);bs.add(rec['generation']['parameters']['unknown_y_coefficient']);signs.add(int(sp.sign(value)))
        # Determinism/identity over explicit same parameters and equivalent rational spelling.
        for rec in records[:32]:
            p=rec['generation']['parameters'];seed=rec['generation']['seed']
            assert rec==g.generate(level,seed,parameters=p)
            other=g.generate(level,seed+81,parameters=p);assert other['question']==rec['question']
            m=sp.Rational(p['slope']);alias={**p,'slope':str(2*m.p)+'/'+str(2*m.q)}
            assert g.generate(level,seed,parameters=alias)['question']==rec['question']
            native.append({'label':level+'/'+str(seed),'record':rec,'checks':checks(rec)})
        assert {g.generate(level,seed)['generation']['template'] for seed in range(100)}==({'mixed-form'} if level=='easy' else {'two-standard'})
        coverage[level]={'meaningful_tasks_enumerated_and_display_checked':len(records),'known_slopes':len(slopes),'unknown_y_coefficients':sorted(bs),'answer_signs':sorted(signs),'source_difficulty_labels':0,'difficulty_origin':'authored'}
        for rec in records[:3]:review.append({'label':level+' authored default variant','record':rec})
    # Explicit signed/zero constant boundaries; values cannot remove level workload.
    boundary=0
    for level in g.SUPPORTED_LEVELS:
        for m in ('-12','12') if level!='hard' else ('-12/7','12/7','1/2','-1/2'):
            for b in (-9,-2,2,9):
                if level=='hard' and pymath.gcd(abs(b),sp.Rational(m).q)!=1:continue
                for h,c in ((-12,15),(0,-15),(12,0)):
                    p={'slope':m,'known_intercept':h,'unknown_y_coefficient':b,'unknown_constant':c,'known_scale':1}
                    if sp.Rational(c,b)==h:continue
                    rec=g.generate(level,parameters=p);displayed(rec);boundary+=1
                    native.append({'label':'boundary/'+level+'/'+str(boundary),'record':rec,'checks':checks(rec)})
    anchor=cases[0]['parameters']
    for level,p in [('easy',{**anchor,'slope':'1/2'}),('moderate',{**anchor,'slope':'1/2'}),('hard',anchor),('hard',{**anchor,'slope':'2/3','unknown_y_coefficient':3}),('easy',{**anchor,'unknown_y_coefficient':1}),('easy',{**anchor,'known_scale':2}),('hard',{**anchor,'slope':'13/7'}),('easy',{**anchor,'slope':'0'}),('easy',{**anchor,'unknown_constant':15})]:
        fails(lambda level=level,p=p:g.generate(level,parameters=p))
    fails(lambda:g.generate('moderate',template='mixed-form',parameters=anchor))
    # Incidental intercepts and source equation scaling never pad task counts.
    base=g.generate('easy',parameters=anchor);changed=g.generate('easy',parameters={**anchor,'known_intercept':-1,'unknown_constant':12})
    assert base['generation']['parameter_fingerprint']==changed['generation']['parameter_fingerprint'] and base['question'][':question/id']!=changed['question'][':question/id']
    scale_case=cases[1]['parameters'];scale1=g.generate('moderate',parameters={**scale_case,'known_scale':1},profile='completed-q-214099');scale2=g.generate('moderate',parameters=scale_case,profile='completed-q-214099')
    assert scale1['generation']['parameter_fingerprint']==scale2['generation']['parameter_fingerprint']
    # Real regressions: prompt coefficient, first moved row sign, concluding coefficient,
    # and omission of the required moved-x stage even if equivalence still holds.
    original=g.generate('easy',parameters=anchor)
    for old,new in [('kx + 3y = 9','kx + 4y = 9'),('3y &= -kx + 9','3y &= kx + 9'),('Consequently, $k=-6$.','Consequently, $k=6$.')]:
        bad=copy.deepcopy(original)
        key=':question/problem' if old.startswith('kx +') else ':question/worked-solution'
        assert old in bad['question'][key];bad['question'][key]=bad['question'][key].replace(old,new);fails(lambda:displayed(refresh_identity(bad)))
    bad=copy.deepcopy(original);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('3y &= -kx + 9','y &= -\\frac{k}{3}x + 3');fails(lambda:displayed(refresh_identity(bad)))
    write('source-cases.json',cases);write('source-replays.json',raw_records);write('review.json',review)
    text='# Originals and generated review\n\nCaptured practices are unrated and lack banks, correct designations and worked solutions. Raw public profiles preserve those omissions; completed records and all difficulty labels are authored.\n\n'
    for old in source.values():text+='## Original '+old[':question/math-academy-id']+'\n\n'+old[':question/problem']+'\n\nMissing answer bank, correct reference, worked solution and difficulty.\n\n'
    text+='\n\n---\n\n'.join('## '+item['label']+'\n\n'+g.markdown(item['record']) for item in review);(D/'review.md').write_text(text+'\n')
    write('engine-input.json',native)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
    eng=json.loads((D/'engine-report.json').read_text());assert eng['documented_unresolved_checks']==0
    sha=lambda path:hashlib.sha256(Path(path).read_bytes()).hexdigest()
    report={'status':'pass','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},
       'source_provenance':{key:g.SOURCE[key] for key in ('database','basis','lineage')},
       'source_fidelity':{'raw_exact_prompts':2,'attribute_presence_parity':2,'field_layouts':2,'complete_observed_banks_available':0,'observed_choices_available':0,'correct_designations_available':0,'worked_solutions_available':0,'observed_difficulties_available':0,'authored_completions':2,'results':ledger,'unmatched_observed_choices':[]},
       'mathematics':{'displayed_records_checked':count,'coverage':coverage,'boundary_instances':boundary,'source_profile_parameter_changes_checked':4,'mutation_regressions_rejected':4,'actual_content_identity_recomputed':True,'actual_printed_equations_and_all_stages_checked':True,'line_equivalence_and_distinctness_checked':True,'difficulty_guards_apply_to_explicit_inputs':True,'primitive_hard_guard':True},
       'native_grading':{key:eng[key] for key in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},
       'native_raw_evidence':'2 incomplete records excluded: absent choices/correct reference cannot be natively graded; supported completions graded separately',
       'hashes':{'generator':sha(D.with_suffix('.py')),'validator':sha(__file__),'source':sha(D/'source.json'),'grader':sha(ROOT/'generate/runs/current/check-engine'),'grader_source':sha(ROOT/'generate/runs/current/check-engine.rs')},
       'limitations':['No observed answer keys, banks, practice solutions or difficulty labels exist; none can count as exact fidelity matches.','Raw profiles are evidence-only and ineligible for learning, including changed parameters.','Difficulty boundaries are authored design claims grounded in canonical isolation and sibling standard-form conversion; hard uses familiar exact fractions, no new branch.','No opaque historical bank was captured; there is no wrong-choice intention to infer. Blank completions do not invent distractors.','Content UUIDs replace source UUIDs in local schema; raw attribute-presence and every other source value are preserved with enum-string normalization.']}
    write('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
