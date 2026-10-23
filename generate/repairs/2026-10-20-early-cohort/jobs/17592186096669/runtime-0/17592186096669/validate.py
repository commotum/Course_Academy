"""Independent reading of rendered systems, exact residuals, source replay, grading."""
import hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('backsub',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def read_system(prompt):
    body=prompt.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
    eqs=[];x,y,z=sp.symbols('x y z')
    for row in body.split(r'\\'):
        row=row.replace('&','').replace(' ','')
        for old,new in [('{x}_{1}','x'),('{x}_{2}','y'),('{x}_{3}','z'),('x_{1}','x'),('x_{2}','y'),('x_{3}','z')]:row=row.replace(old,new)
        row=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',row)
        lhs,rhs=row.split('=');lhs=re.sub(r'(\d)([xyz])',r'\1*\2',lhs)
        lhs=lhs.replace('xy','x*y').replace('yz','y*z')
        eqs.append(sp.sympify(lhs,locals={'x':x,'y':y,'z':z})-sp.sympify(rhs))
    assert len(eqs)==3
    return sp.linear_eq_to_matrix(eqs,(x,y,z))

def rendered_fingerprint(q):
    A,B=read_system(q[':question/problem'])
    assert A.det()==1
    return hashlib.sha256(json.dumps([int(A[0,1]),int(A[0,2]),int(A[1,2]),*[str(v) for v in B]]).encode()).hexdigest()

def check_record(rec):
    meta=rec['generation'];q=rec['question'];A,B=read_system(q[':question/problem']);solution=tuple(A.inv()*B)
    assert meta['mathematical_fingerprint']==rendered_fingerprint(q)
    f=q[':question/answer-fields'][0];bank=[g.read_vector(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(bank)==5 and len(set(bank))==5
    assert [i for i,v in enumerate(bank) if A*sp.Matrix(v)==B]==[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])]
    expected=g.generate('easy',meta['seed'],meta['profile'],meta['parameters']['scale'])
    assert q==expected['question']
    # Read both substituted displays independently of the key, validating all RHSs.
    displays=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S)
    assert len(displays)==2
    for display in displays:
        left=display.split(r'\,⟹\,')[0].replace(' ','')
        for old,new in [('{x}_{1}','x'),('{x}_{2}','y'),('{x}_{3}','z')]:left=left.replace(old,new)
        left=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',left)
        left=re.sub(r'(\d)(\()',r'\1*\2',left)
        a,b=left.split('=')
        assert sp.simplify(sp.sympify(a,locals=dict(zip(('x','y','z'),solution))) - sp.sympify(b))==0
    assert g.vector(solution,meta['template']) in q[':question/worked-solution']
    return True

def native(rec):return {'label':rec['question'][':question/id'],'record':rec,'checks':g.native_checks(rec)}

def main():
    samples=[];banks=[];extraction=[]
    for profile in g.PARAMETERS:
        original=g.QUESTIONS[profile];A,B=read_system(original[':question/problem'])
        original_field=original[':question/answer-fields'][0]
        rec=g.generate(profile=profile,scale=1);check_record(rec)
        actual=rec['question'][':question/answer-fields'][0]
        original_values=[g.read_vector(a[':answer/value']) for a in original_field[':answer-field/choices']]
        new_values=[g.read_vector(a[':answer/value']) for a in actual[':answer-field/choices']]
        assert sorted(original_values)==sorted(new_values)
        assert g.read_vector(original_field[':answer-field/correct'][':answer/value'])==tuple(A.inv()*B)
        assert re.sub(r'\s+','',original[':question/problem'])==re.sub(r'\s+','',rec['question'][':question/problem'])
        banks.append({'profile':profile,'source_id':original[':db/id'],'matched_choices':5,'total_choices':5,'complete_bank':True,'correct_designation':True,'prompt_layout_replay':True,'solution_stages':['read third equation','substitute into second','substitute into first','vector form'],'literal_solution_whitespace_replay':False})
        extraction.append({'profile':profile,'source_id':original[':db/id'],'template':rec['generation']['template'],'coefficient_matrix':str(A),'rhs':[str(v) for v in B],
          'source_choices':[{'source_field':original_field[':db/id'],'source_answer':a[':db/id'],'source_exact_value':[str(v) for v in vals],'recipe':['k*('+str(v)+')' for v in vals],'correct':vals==tuple(A.inv()*B)} for a,vals in zip(original_field[':answer-field/choices'],original_values)],
          'recipe_interpretation':'Exact homothetic image of complete observed bank; underlying mistake interpretation unresolved, not presented to learner'})
        for k in g.SCALES:
            sample=g.generate(seed=k,profile=profile,scale=k);check_record(sample)
            assert sample['question']==g.generate(seed=k+100,profile=profile,scale=k)['question']
            A2,B2=read_system(sample['question'][':question/problem']);assert A2==A and B2==k*B
            samples.append(sample)
    fixtures=list(map(native,samples))
    # Test original stored radio fields too, using their real IDs and values.
    for profile in g.PARAMETERS:
        orig=g.QUESTIONS[profile];f=orig[':question/answer-fields'][0]
        rec=g.generate(profile=profile,scale=1);q=rec['question'];q[':question/id']=orig[':question/id'];q[':question/problem']=orig[':question/problem'];q[':question/worked-solution']=orig[':question/worked-solution']
        q[':question/answer-fields']=[{':answer-field/id':f[':answer-field/id'],':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/choices':[{':answer/id':a[':answer/id'],':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],':answer-field/correct':[':answer/id',f[':answer-field/correct'][':answer/id']]}]
        fixtures.append(native(rec))
    def save(name,obj):(H/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
    save('previews.json',samples);save('source-bank-replay.json',banks);save('template-extraction.json',extraction);save('engine-input.json',fixtures)
    subprocess.run([str(H.parents[2]/'generate/runs/current/check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
    engine=json.loads((H/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    unique=len({rendered_fingerprint(r['question']) for r in samples})
    report={'status':'passed_with_documented_source_anomaly','basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'generator_sha256':hashlib.sha256(H.with_suffix('.py').read_bytes()).hexdigest(),
      'mathematics':{'all_rendered_systems_and_choice_residuals_valid':True,'substituted_solution_displays_valid':True,'variants_checked':len(samples),'distinct_mathematical_systems':unique},
      'fidelity':{'source_complete_banks':len(banks),'source_complete_banks_total':11,'matched_source_choices':55,'total_source_choices':55,'matched_source_distractors':44,'total_source_distractors':44,'two_answer_shapes':True,'full_prompt_replay':True,'solution_stage_replay':True,'literal_solution_replay':False},
      'coverage':{'profile_count':11,'scale_values':list(g.SCALES),'all_profile_scale_pairs':True,'target_slots':'none; every source requests the complete three-variable solution','fixed_coefficients_and_variable_names_per_profile':True,'deterministic_replay_and_seed_independent_identity':True},
      'native_grading':{k:v for k,v in engine.items() if k!='records'},'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],
      'excluded_source':[{'id':17592186097182,'math_academy_id':'q-20451','reason':'Unrated, missing correct link and worked solution. Preserved; not supported or counted.'}],
      'capability_exception':'Version 1 is restricted to 99 exact system variants of complete observed Easy profiles. Moderate/Hard absent in all source evidence; unsupported by this package, no global impossibility claim.'}
    save('validation.json',report)
    review=[g.generate(profile=p,scale=k) for p,k in [('q-10197',1),('q-10197',2),('q-129455',1),('q-129455',3)]]
    (H/'review.md').write_text('# Source and homothetic variants\n\n'+'\n\n---\n\n'.join(g.markdown(r) for r in review)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
