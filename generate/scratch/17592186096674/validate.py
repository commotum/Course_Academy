"""Read displayed systems independently, verify every row operation and engine key."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,x):(H/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def system(text):
    # Independently parse equations, rather than trusting generator parameters.
    b=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)
    if not b:raise ValueError('No displayed linear system')
    x,y,z=s.symbols('x y z');rows=[]
    for row in b[1].split(r'\\'):
        lhs,rhs=row.replace('&','').strip().rstrip('.').split('=')
        lhs=re.sub(r'(?<=\d)(?=[xyz])','*',lhs)
        ex=s.sympify(lhs,locals={'x':x,'y':y,'z':z})
        rows.append([ex.coeff(v) for v in (x,y,z)]+[s.Rational(rhs)])
    return s.Matrix(rows)
def fingerprint(q):
    try:return hashlib.sha256(('gauss-jordan|'+str(list(system(q[':question/problem'])))).encode()).hexdigest()
    except ValueError:return 'unparsed|'+hashlib.sha256(q[':question/problem'].encode()).hexdigest()
def independent(rec):
    q=rec['question'];md=rec['generation'];mid=md['source_profile'];k=md['parameters']['scale']
    assert rec==g.generate('easy',md['seed'],mid,{'scale':k},mid)
    m=system(q[':question/problem']);assert m.rows==3 and m.cols==4
    assert m[:,:3].det()==1 and all(m[i,j]==0 for i in range(3) for j in range(i))
    target=m.rref()[0];expected=tuple(target[:,3]);f=q[':question/answer-fields'][0]
    vs=[g.triple(a[':answer/value']) for a in f[':answer-field/choices']];ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
    assert vs[ci]==expected and sum(v==expected for v in vs)==1 and len(set(vs))==5
    assert all(len(v)==3 for v in vs)
    matrices=g.parse_matrices(q[':question/worked-solution']);assert matrices[0]==m and matrices[-1]==target
    assert all(z.rref()[0]==target for z in matrices)
    # Parse the actual operation annotations and apply each to the preceding matrix.
    block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)[1]
    segments=block.split(r'\\  & ∼')
    for i,segment in enumerate(segments[:-1]):
        op=re.search(r'\{R\}_\{([123])\}\s*&\s*:=\{R\}_\{([123])\}\+(.*?)\{R\}_\{([123])\}',segment)
        assert op,(mid,'unparsed operation',segment)
        dst,again,coef,src=op.groups();assert dst==again
        coef=coef.strip();factor=s.Rational(coef.strip('()')) if coef else s.Integer(1)
        calculated=matrices[i+1].copy();di,si=int(dst)-1,int(src)-1
        calculated[di,:]=calculated[di,:]+factor*calculated[si,:]
        assert calculated==matrices[i+2],(mid,k,'row operation',op.groups())
    if 'then solve' in q[':question/problem']:
        assert system(q[':question/worked-solution'].split('The corresponding system is now')[1])==s.eye(3).row_join(s.Matrix(expected))
        # Explicit vector and coordinate conclusions must agree too.
        tail=q[':question/worked-solution'].split('So,')[1]
        values=re.findall(r'[xyz]\s*=\s*(-?\d+)',tail);assert tuple(map(s.Rational,values))==expected,(mid,k,tail,expected)
        vector=re.search(r'⟨\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*⟩',tail)
        if vector:assert tuple(map(s.Rational,vector.groups()))==expected
    for t in (q[':question/problem'],q[':question/worked-solution']):assert t.count('$')%2==0 and t.replace(r'\{','').replace(r'\}','').count('{')==t.replace(r'\{','').replace(r'\}','').count('}')
    assert fingerprint(q)==md['mathematical_fingerprint']
    for a in f[':answer-field/choices']:
        if a[':answer/type']==':answer.type/math':assert '$' not in a[':answer/value'] and r'\\begin' not in a[':answer/value']
def checks(r):
    f=r['question'][':question/answer-fields'][0]
    return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every option through actual application grade_field'} for a in f[':answer-field/choices']]
def main():
    records=g.batch('easy',108,2633);replays=[];components=[];reviews=[]
    for mid in sorted(set(g.SOURCES)-set(g.EXCLUDED)):
        old=g.SOURCES[mid];r=g.generate('easy',0,mid,{'scale':1});independent(r);f=old[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
        oldbank=[g.triple(a[':answer/value']) for a in f[':answer-field/choices']];newbank=[g.triple(a[':answer/value']) for a in rf[':answer-field/choices']]
        assert sorted(oldbank)==sorted(newbank) and g.triple(f[':answer-field/correct'][':answer/value'])==g.triple(next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]))
        assert system(old[':question/problem'])==system(r['question'][':question/problem'])
        assert g.parse_matrices(old[':question/worked-solution'])==g.parse_matrices(r['question'][':question/worked-solution'])
        m,bank,correct,shape=g.components(mid)
        components.append({'source':mid,'source_db_id':old[':db/id'],'source_uuid':old[':question/id'],'template':shape,'field_type':'radio','choice_count':5,'matrix':m.tolist(),'correct':correct,'choices':[{'source_answer_uuid':a[':answer/id'],'exact_value':a[':answer/value'],'tuple':v,'recipe':'scale * '+str(v),'interpretation':'observed homogeneous expression pattern; error mechanism unresolved'} for a,v in zip(f[':answer-field/choices'],bank)],'matched_choices':5,'total_choices':5,'matched_distractors':4,'total_distractors':4,'complete_bank':True,'plot_rating':'none','source_replay_matrices_and_system':True})
        replays.append(r);variant=g.generate('easy',1,mid,{'scale':3});reviews.append('## '+mid+' original\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\n## Scale 3 variant\n\n'+g.markdown(variant))
    for r in records:independent(r)
    assert len({fingerprint(r['question']) for r in records})==len(records)
    assert g.batch('easy',108,2633)==records
    # Seed and answer order do not contribute to mathematical content identity.
    assert g.generate('easy',77,'q-20591',{'scale':2})['question']==g.generate('easy',78,'q-20591',{'scale':2})['question']
    allrecords=replays+records;save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(allrecords)])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
    save('source-components.json',components);(H/'review.md').write_text('\n\n---\n\n'.join(reviews));save('review.json',{'replays':replays,'variants':records})
    save('validation.json',{'status':'pass','source_basis':g.CAPTURE['basis'],'generator_sha256':hashlib.sha256(H.with_suffix('.py').read_bytes()).hexdigest(),'complete_source_banks':9,'matched_distractors':36,'total_distractors':36,'matched_choices':45,'total_choices':45,'missing_options':[],'extra_options':[],'all_bounded_variants':108,'independent_displayed_system_and_solution_checks':len(allrecords),'actual_engine_report':'engine-report.json','source_fidelity':'All complete banks, system equations, matrices, operation sequence and response contracts replay. Stored redundant answer LaTeX escaping normalized; spacing standardized. Full source prose retained in parameterized solution.','slot_coverage':{'scale':list(g.SCALES),'fixed_coefficient_matrices':9,'target_role':'RREF or solution of same complete 3x3 system; no variable target positions'},'deterministic':True,'distinct_mathematical_tasks':108})
if __name__=='__main__':main()
