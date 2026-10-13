"""Independent displayed geometry, full bank replay, bounded family and real grader."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('distance_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x,y=sp.symbols('x y',real=True)

def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def parse(text):
    text=text.strip().rstrip('.').replace(r'\dfrac',r'\frac').replace(r'\left','').replace(r'\right','')
    text=re.sub(r'\{([xy])\}_\{([12])\}',r'\1_\2',text)
    while r'\frac' in text:
        changed=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',text)
        assert changed!=text,text;text=changed
    while r'\sqrt' in text:
        changed=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',text)
        assert changed!=text,text;text=changed
    text=text.replace('{','(').replace('}',')').replace('^','**')
    return parse_expr(text,local_dict={'x':x,'y':y,'m':sp.Symbol('m'),'d':sp.Symbol('d'),'x_1':sp.Symbol('x_1'),'x_2':sp.Symbol('x_2'),'y_1':sp.Symbol('y_1'),'y_2':sp.Symbol('y_2')},transformations=standard_transformations+(implicit_multiplication_application,))

def geometry(q):
    spans=re.findall(r'\$([^$]+)\$',q[':question/problem']);assert len(spans)==2,spans
    point=spans[0].strip().strip('()');xp,yp=[parse(t) for t in point.split(',')]
    lhs,rhs=spans[1].split('=');poly=sp.Poly(parse(lhs)-parse(rhs),x,y);assert poly.total_degree()==1
    A=poly.coeff_monomial(x);B=poly.coeff_monomial(y);C=-poly.coeff_monomial(1)
    assert A!=0 and B!=0
    return A,B,C,xp,yp

def fingerprint(q):
    return g.fingerprint_geometry(*geometry(q))

def check(rec):
    meta=rec['generation'];q=rec['question'];sid,k=meta['parameters'];level=q[':question/difficulty'].split('/')[-1]
    assert rec==g.generate(level,meta['seed'],sid,[sid,k]),'Deterministic complete replay'
    A,B,C,xp,yp=geometry(q);d=sp.simplify(abs(A*xp+B*yp-C)/sp.sqrt(A*A+B*B))
    # Solve original line + orthogonal normal independently of the sampler.
    h,j=sp.linsolve([A*x+B*y-C,B*(x-xp)-A*(y-yp)],(x,y)).args[0]
    assert sp.simplify(sp.sqrt((h-xp)**2+(j-yp)**2)-d)==0 and d>0
    f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
    assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    choices=f[':answer-field/choices'];values=[parse(a[':answer/value']) for a in choices];assert len(values)==5
    assert all('$' not in a[':answer/value'] for a in choices)
    assert all(sp.simplify(a-b)!=0 for i,a in enumerate(values) for b in values[i+1:])
    correct=next(i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1]);assert sp.simplify(values[correct]-d)==0
    assert all(sp.simplify(v-d)!=0 for i,v in enumerate(values) if i!=correct)
    sol=q[':question/worked-solution']
    if k>1:
        # Check every rendered alignment at the independently solved foot.
        subst={x:h,y:j,sp.Symbol('m'):B/A,sp.Symbol('d'):d,sp.Symbol('x_1'):xp,sp.Symbol('y_1'):yp,sp.Symbol('x_2'):h,sp.Symbol('y_2'):j}
        for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S):
            for row in block.split(r'\\'):
                lhs,rhs=row.replace('&','').split('=');lhs=lhs.strip()
                if not lhs:lhs='d'
                assert sp.simplify((parse(lhs)-parse(rhs)).subs(subst))==0,(sid,k,row)
        final=re.search(r'is \$([^$]*)\$$',sol);assert final and sp.simplify(parse(final[1])-d)==0
        assert f'the point $({g.tex(xp)},{g.tex(yp)})$' in sol
        assert f'intersect at the point $({g.tex(h)},{g.tex(j)}).$' in sol
    assert meta['mathematical_fingerprint']==fingerprint(q)
    for asset in meta['assets']:
        path=Path(asset['local_path']);path=path if path.is_absolute() else ROOT/path
        assert hashlib.sha256(path.read_bytes()).hexdigest()==asset['sha256']
        assert asset['path'] in sol
    return rec

def native(label,rec):
    f=rec['question'][':question/answer-fields'][0]
    return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual application radio grading for every bank option'} for a in f[':answer-field/choices']]}

def main():
    replay=[];records=[];inputs=[];review=[];options=[]
    for sid in g.CASES:
        old=g.SOURCES[sid];level=old[':question/difficulty'][':db/ident'].split('/')[-1]
        r=check(g.generate(level,0,sid,[sid,1]));q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
        oldvals=[parse(a[':answer/value']) for a in of[':answer-field/choices']];newvals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
        assert all(sum(sp.simplify(v-u)==0 for u in newvals)==1 for v in oldvals)
        assert q[':question/problem']==old[':question/problem']
        assert q[':question/worked-solution']==old[':question/worked-solution'] or sid=='q-114358'
        assert parse(of[':answer-field/correct'][':answer/value'])==parse(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))
        replay.append({'source':sid,'profile':sid,'matched_choices':5,'matched_distractors':4,'complete_bank_match':True,'correct_designation':True,'missing':[],'extra':[],'prompt_exact':True,'solution_exact':sid!='q-114358','documented_solution_correction':sid=='q-114358'})
        for a in of[':answer-field/choices']:
            options.append({'source':sid,'field':'selection','source_answer_id':a[':answer/id'],'original_value':a[':answer/value'],'recipe':'k * ('+a[':answer/value']+')','interpretation':'observed whole mathematical value scaled as a length; underlying error unresolved','reproduces_at_source':True,'profile':sid})
        for k in range(1,10):
            r=check(g.generate(level,0,sid,[sid,k]));assert g.generate(level,99,sid,[sid,k])['question']==r['question'];records.append(r);inputs.append(native(sid+' k='+str(k),r))
        variant=check(g.generate(level,42,sid,[sid,2]));review.append('## '+sid+'\n\nOriginal\n\n'+g.markdown(check(g.generate(level,0,sid,[sid,1])))+'\n\nVariant\n\n'+g.markdown(variant))
    assert len({fingerprint(r['question']) for r in records})==63
    assert g.fingerprint_geometry(3,2,6,1,-5)==g.fingerprint_geometry(6,4,12,1,-5)
    assert g.generate('moderate',0,'q-114341',['q-114341',2])['question']==g.generate('moderate',98,'q-114341',['q-114341',2])['question']
    for level in ('easy','unclassified'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('Unsupported level admitted')
    save('source-replay.json',{'passed':True,'complete_banks_matched':7,'complete_banks_total':7,'distractors_matched':28,'distractors_total':28,'profiles':replay,'excluded_sources':{'q-74036':'unrated, missing correct designation and worked solution','q-74037':'unrated, missing correct designation and worked solution','q-74437':'hard geometry and solution exist but no answer fields'},'source_error':{'q-114358':r'-5/2-2/5=-29/10, not +29/10; correction only in generated replay; original retained'}})
    save('choice-recipes.json',options);save('native-input.json',inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    save('previews.json',[g.generate('moderate',42),g.generate('hard',43),g.generate('hard',44)]);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('validation.json',{'passed':True,'exhaustive_instances':63,'new_distinct_bounded_geometries':56,'supported_levels':['moderate','hard'],'independent_checks':'parse displayed point and entire line; solve perpendicular foot independently; point-line distance formula; all bank values and correct designation; every generated alignment and final answer; stable identities and asset hashes','source_fidelity':'7/7 complete banks; 28/28 distractors; original prompts and solutions at replay except recorded sign correction; new numeric alignments normalized while source instructional sequence/prose retained','native_grading':'63 records, every choice graded by course_academy_engine::learning::grade_field','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'replenish.py',HERE/'capabilities.json',ROOT/'generate/runs/current/check-engine')}})

if __name__=='__main__':main()
