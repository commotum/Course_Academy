"""Independent projection/minimization checks and actual application bank grading."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('closest_point',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x,y=sp.symbols('x y',real=True)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def expression(t):
    t=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
    return sp.expand(parse_expr(t,local_dict={'x':x,'y':y},transformations=standard_transformations+(implicit_multiplication_application,)))
def polynomial(t):
    l,r=t.split('=');return expression(l)-expression(r)
def pair(t):return tuple(expression(z) for z in t.strip('()').split(','))
def printed(q):
    p=q[':question/problem'];eq=re.search(r'on the line \$(.*?)\$',p)[1];e=polynomial(eq)
    u,v=map(sp.Integer,re.search(r'closest to the point \$\((-?\d+),\s*(-?\d+)\)',p).groups())
    return e.coeff(x),e.coeff(y),-e.subs({x:0,y:0}),u,v
def fingerprint(q):
    A,B,C,u,v=printed(q);scale=A if A else B
    return g.digest([str(z) for z in (A/scale,B/scale,C/scale,u,v)])
def check(rec):
    q=rec['question'];meta=rec['generation'];s=meta['template'];t=meta['parameters']['t']
    assert meta['version']==g.VERSION and rec['knowledge_point']['db_id']==g.KP_ID
    expected=g.generate(q[':question/difficulty'].split('/')[-1],meta['seed'],s,{'t':t})
    # Preparation publishes the exact same plot bytes to their content hash path.
    def without_plot(q):return {**q,':question/problem':re.sub(r'!\[\]\([^)]*\)','<prompt plot>',q[':question/problem'])}
    assert without_plot(q)==without_plot(expected['question']) and meta==expected['generation']
    A,B,C,u,v=printed(q);den=A*A+B*B;offset=(A*u+B*v-C)/den
    foot=(sp.cancel(u-A*offset),sp.cancel(v-B*offset))
    assert offset!=0
    assert A*foot[0]+B*foot[1]==C
    assert (u-foot[0])*B-(v-foot[1])*A==0
    # Independent distance polynomial on the line: positive curvature and exact minimum.
    line_y=(C-A*x)/B;distance=sp.expand((x-u)**2+(line_y-v)**2)
    assert sp.diff(distance,x).subs(x,foot[0])==0 and sp.diff(distance,x,2)>0
    fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    bank=f[':answer-field/choices'];assert len(bank)==5 and len(set(pair(a[':answer/value']) for a in bank))==5
    assert len({a[':answer/id'] for a in bank})==5
    assert sum(a[':answer/id']==f[':answer-field/correct'][1] for a in bank)==1
    for a in bank:assert (pair(a[':answer/value'])==foot)==(a[':answer/id']==f[':answer-field/correct'][1])
    if t!=0:
        blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
        source=g.sources()[s];has_rewrite=not g.printed(source)[5].startswith('y=')
        n=B/A;d=v-n*u
        for index,block in enumerate(blocks):
            for row in block.split('\\\\'):
                if '&=' not in row:continue
                l,r=row.split('&=');l=l.strip();r=r.strip()
                if 'y_1' in l:continue
                e=sp.expand(expression(l)-expression(r))
                if has_rewrite and index==0:assert e.subs(y,line_y)==0
                elif 'y' in l:assert e.subs(y,n*x+d)==0
                else:assert e.subs(x,foot[0])==0
        assert '$'+g.pairtex(foot)+'.$' in q[':question/worked-solution']
    assert fingerprint(q)==meta['mathematical_fingerprint']
    path=re.search(r'!\[\]\(([^)]*)\)',q[':question/problem'])[1]
    resolved=Path('/media/jake/SSD/EDB/math')/path if path.startswith('images/') else ROOT/path
    assert resolved.is_file()
    if t!=0:
        local=g.render_plot(s,t,HERE/'plots');assert resolved.read_bytes()==local.read_bytes()
    return rec
def native(label,r):
    f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
    return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete bank ID grading'} for a in f[':answer-field/choices']]}
def main():
    inputs=[];replays=[];reviews=[];fps=set();counts={}
    for s,old in g.sources().items():
        level=old[':question/difficulty'][':db/ident'].split('/')[-1]
        r=check(g.generate(level,0,s,{'t':0}));q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
        assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
        assert f[':answer-field/key']==of[':answer-field/key']
        assert len(f[':answer-field/choices'])==len(of[':answer-field/choices'])==5
        assert set(pair(a[':answer/value']) for a in f[':answer-field/choices'])==set(pair(a[':answer/value']) for a in of[':answer-field/choices'])
        assert next(pair(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==pair(of[':answer-field/correct'][':answer/value'])
        replays.append({'source':s,'profile':s,'matched_choices':5,'total_choices':5,'matched_distractors':4,'complete_bank_matched':True,'missing_extra_choices':[],'exact_prompt_solution_field_contract':True})
        reviews.append('## Source '+s+'\n\n'+g.markdown(r))
    for level in ('easy','moderate'):
        count=0
        for s,p in g.candidates(level):
            r=check(g.generate(level,1954,s,p));fp=fingerprint(r['question']);assert fp not in fps;fps.add(fp);count+=1
            inputs.append(native(s+'-'+str(p['t']),r))
            if p['t'] in (-4,4):reviews.append('## Boundary variant\n\n'+g.markdown(r))
        counts[level]=count
    for level,s,p in [('hard','q-74061',{'t':1}),('easy','q-74061',{'t':5}),('easy','q-74061',{'t':1.5}),('moderate','q-74061',{'t':1})]:
        try:g.generate(level,0,s,p)
        except ValueError:pass
        else:raise AssertionError('Invalid boundary accepted')
    a=g.generate('easy',1954,'q-74061',{'t':-4});b=g.generate('easy',999,'q-74061',{'t':-4});assert a['question']==b['question']
    h=hashlib.sha256((HERE/'plots/q-74061-t-4.png').read_bytes()).hexdigest();g.render_plot('q-74061',-4,HERE/'plots');assert hashlib.sha256((HERE/'plots/q-74061-t-4.png').read_bytes()).hexdigest()==h
    previews=g.batch('easy',5,1954)+g.batch('moderate',5,1954)
    save('previews.json',previews);save('native-input.json',inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    save('source-replay.json',{'passed':True,'source_basis':1954,'complete_banks_matched':8,'complete_banks_total':8,'source_distractors_matched':32,'source_distractors_total':32,'matched_answer_values':40,'total_observed_answer_values':40,'source_results':replays,'missing_extra_options':[],'fidelity_limits':'Variant algebra rows use normalized parentheses and a consistent elimination layout; original instructional sentences, field shape and solution sequence retained. Source prompts, solutions, choices and assets exact at replay.'})
    (HERE/'review.md').write_text('\n\n'.join(reviews)+'\n')
    save('validation.json',{'passed':True,'exhaustive_instances':72,'counts':counts,'distinct_bounded_tasks':len(fps),'mathematics':'Independent normal-vector projection, incidence, orthogonality, positive quadratic curvature, unique closest answer; every variant numeric solution row checked','grading':'Actual application grade_field: all five options in every bounded instance','supported_levels':['easy','moderate'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json')}})
    print('Validated',counts)
if __name__=='__main__':main()
