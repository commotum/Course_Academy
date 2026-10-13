#!/usr/bin/env python3
"""Independent displayed-math/source/native-grading validation; fails closed."""
import hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z,u,v,w=g.x,g.y,g.z,g.u,g.v,g.w

def eq(a,b):
    delta=sp.simplify(sp.powdenest(a-b,force=True))
    return delta==0

def arrays(block):
    found=[]
    for m in re.finditer(r'\|\\begin\{aligned\}((?:(?!\\begin\{).)*?)\\end\{aligned\}\|',block,re.S):
        if '∂' in m[1] or '\\partial' in m[1]:continue
        cells=[[g.scalar(c.strip()) for c in row.split('&')] for row in m[1].split(r'\\')]
        assert len(set(map(len,cells)))==1 and len(cells)==len(cells[0])
        found.append((m.span(),sp.Matrix(cells)))
    return found

def evaluated(raw):
    for span,M in reversed(arrays(raw)):
        a,b=span;raw=raw[:a]+'('+g.tex(M.det())+')'+raw[b:]
    return g.scalar(raw)

def rows(block):
    # Nested arrays must not become independent teaching rows.
    for i,(span,M) in reversed(list(enumerate(arrays(block)))):
        a,b=span;block=block[:a]+'('+g.tex(M.det())+')'+block[b:]
    # Protect formal arrays too.
    block=re.sub(r'\|\\begin\{aligned\}((?:(?!\\begin\{).)*?)\\end\{aligned\}\|','FORMAL',block,flags=re.S)
    block=block.strip()
    if block.startswith(r'\begin{aligned}'):
        block=block[len(r'\begin{aligned}'):-len(r'\end{aligned}')]
    return [r.strip().rstrip('.') for r in block.split(r'\\')]

def prompt_components(record):
    prompt=record['question'][':question/problem'];block=g.displays(prompt)[0].strip()
    if '⟶' in block:
        cells=block.split('⟶',1)[1]
        cells=cells[len(r'[\begin{aligned}'):cells.index(r'\end{aligned}')]
        return tuple(g.scalar(c) for c in cells.split(r'\\'))
    # Actual assignments, whether source comma or authored quadruple spacing.
    parts=re.split(r'\\,|\\qquad\s*',block.rstrip('.'))
    assert len(parts)==3,block
    assert [p.split('=',1)[0].strip() for p in parts]==['u','v','w']
    return tuple(g.scalar(p.split('=',1)[1]) for p in parts)
MINORS={
'q-39300':[(0,0)],'q-39669':[(0,0),(0,1)],'q-161798':[(0,0)],
'q-161800':[(0,1),(0,2)],'q-161801':[(0,1),(0,2)],'q-161802':[(0,0)],
'q-161804':[(0,0)],'q-161805':[(0,0)],'q-161806':[(0,0),(0,1)],
'q-161807':[(0,1),(0,2)],'q-161808':[(2,0)],'q-161797':[(0,0)]}

def format_check(text):
    assert text.count('$$')%2==0 and text.replace('$$','').count('$')%2==0,'unbalanced math delimiter'
    depth=0
    for i,ch in enumerate(text):
        if ch not in '{}':continue
        slashes=0;j=i-1
        while j>=0 and text[j]=='\\':slashes+=1;j-=1
        if slashes%2:continue
        depth+=1 if ch=='{' else -1
        assert depth>=0,'closing brace'
    assert depth==0,'unbalanced braces'
    assert '\x08' not in text and '--' not in text and '+-' not in text

def check(record):
    q=record['question'];meta=record['generation'];key=meta['source_id'];raw=meta['profile']=='observed'
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]:format_check(text)
    F=prompt_components(record);J=sp.Matrix(F).jacobian((x,y,z));Dxy=sp.factor(J.det());assert Dxy!=0
    sub={u:F[0],v:F[1],w:F[2]}
    f=q[':question/answer-fields'][0];values=[g.scalar(a[':answer/value']) for a in f[':answer-field/choices']]
    correct=next(g.scalar(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
    assert eq(correct.subs(sub,simultaneous=True),1/Dxy),(key,correct,Dxy)
    assert len(values)==5 and all(not e.has(sp.zoo,sp.nan,sp.oo) for e in values)
    assert all(not eq(a,b) for i,a in enumerate(values) for b in values[:i])
    assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
    solution=q[':question/worked-solution'];tail=solution.split('First, we find the partial derivatives:',1)[1];blocks=g.displays(tail)
    if key:
        original_blocks=g.displays(g.Q[key][':question/worked-solution'].split('First, we find the partial derivatives:',1)[1])
        assert len(blocks)==len(original_blocks),(key,'missing solution block')
        for block,original_block in zip(blocks[1:],original_blocks[1:]):
            assert len(rows(block))==len(rows(original_block)),(key,'changed solution stage count')
    # Actual printed nine partial derivative right-hand sides, including zeros.
    partial=blocks[0];cells=re.findall(r'(?:& =|=)([^&]+?)(?=&|\\\\|\\end\{aligned\})',partial)
    assert len(cells)==9,(key,cells)
    assert all(eq(g.scalar(cell.strip()),expected) for cell,expected in zip(cells,list(J))),(key,'printed partials')
    det=blocks[1];arr=arrays(det);assert len(arr)>=2
    assert arr[0][1]==J,(key,'printed numeric Jacobian')
    expected_base=sp.Matrix(g.BASE[key]).jacobian((x,y,z)) if key else J
    expected_minors=MINORS[key] if key else [(0,0)]
    assert len(arr[1:])==len(expected_minors)
    structural_fail=[]
    for (_,M),(i,j) in zip(arr[1:],expected_minors):
        if M!=expected_base.minor_submatrix(i,j):structural_fail.append('cofactor_minor')
    if structural_fail:assert raw and key=='q-161807',(key,'incorrect cofactor',structural_fail)
    drows=rows(det)
    # Formal first row separately matches the source's unchanged operator mask.
    assert 'FORMAL' in drows[0]
    for row in drows[1:]:
        value=evaluated(row.split('=',1)[1]);assert eq(value,Dxy),(key,'det stage',row,value,Dxy)
    for block in blocks[2:]:
        rrows=rows(block)
        for row in rrows:
            left,right=row.split('& =',1) if '& =' in row else row.split('&=',1)
            if '∂' in right or '\\partial' in right:continue
            value=evaluated(right)
            target=1/Dxy if '∂(x,y,z)' in block or '\\partial(x,y,z)' in block else Dxy
            assert eq(value.subs(sub,simultaneous=True),target),(key,'rewrite/reciprocal',row,value,target)
            if left.strip() and '∂' not in left and '\\partial' not in left:
                assert eq(evaluated(left).subs(sub,simultaneous=True),target)
    # Component prose has full independent assignments with correct coordinate names.
    if 'Here, we have' in solution:
        here=g.displays(solution.split('Here, we have',1)[1])[0].strip();parts=here.split(r'\,')
        labels=[p.split('=',1)[0] for p in parts]
        label_error=labels!=['u(x,y,z)','v(x,y,z)','w(x,y,z)']
        if label_error:assert raw and key=='q-39300',(key,labels)
        assert all(eq(g.scalar(part.split('=',1)[1]),F[i]) for i,part in enumerate(parts))
    if not meta['evidence_only']:
        # Reconstruct wrong operations from the displayed derivative matrix.
        first_scale=meta['parameters'].get('u',meta['parameters'].get('a'))
        expected=[1/Dxy,Dxy,-1/Dxy,first_scale/Dxy,1/(first_scale*Dxy)]
        if q[':question/difficulty'].endswith('easy'):expected[3]=sp.Integer(1)
        displayed=[e.subs(sub,simultaneous=True) for e in values]
        assert all(sum(eq(a,b) for b in displayed)==1 for a in expected),(key,'wrong method operation')
    return {'cofactor_minor_error':bool(structural_fail),'component_label_error':raw and key=='q-39300'}

def real_value(expr,sub):
    """Evaluate rational powers with odd denominators using real roots."""
    if expr.is_Atom:return expr.subs(sub)
    if expr.is_Pow:
        base=real_value(expr.base,sub);power=expr.exp
        if power.is_Rational and power.q%2==1:
            return sp.real_root(base,power.q)**power.p
        return base**power
    args=[real_value(a,sub) for a in expr.args]
    return expr.func(*args)

def signed_cube_branch():
    r=g.generate('hard',template='source_161807',parameters={'u':1,'v':1,'w':1},profile='observed')
    F=prompt_components(r);J=sp.Matrix(F).jacobian((x,y,z));Dxy=J.det()
    f=r['question'][':question/answer-fields'][0]
    correct=next(g.scalar(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
    for values in itertools.product((-2,2),(-3,3),(-5,5)):
        point=dict(zip((x,y,z),values));sub={u:F[0].subs(point),v:F[1].subs(point),w:F[2].subs(point)}
        assert sp.simplify(real_value(correct,sub)-1/Dxy.subs(point))==0
        rewrite=g.displays(r['question'][':question/worked-solution'].split('Writing down',1)[1])[0]
        for row in rows(rewrite):
            left,right=row.split('& =',1)
            for side in (left,right):
                if side.strip():assert sp.simplify(real_value(evaluated(side),{**point,**sub})-Dxy.subs(point))==0
    # Real cube-root uniqueness gives root(t^3)=t for every nonzero real t;
    # squaring yields (t^3)^(2/3)=t^2. This is the advertised real convention.
    return {'all_eight_nonzero_sign_octants_verified':True,'raw_convention':'real cube root; principal complex fractional powers are not asserted','normal_domain':'positive x,y,z explicitly printed'}

def run():
    cases=[];review=[];native=[];fidelity=[];counts={};errors=[]
    branch=signed_cube_branch()
    for template,key in g.TEMPLATES.items():
        level=g.LEVELS[template];p={'u':1,'v':1,'w':1}
        record=g.generate(level,template=template,parameters=p,profile='observed')
        original=g.Q[key];q=record['question'];f=q[':question/answer-fields'][0];sf=original[':question/answer-fields'][0]
        assert q[':question/problem']==original[':question/problem']
        assert q[':question/worked-solution']==original[':question/worked-solution']
        for attr in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
            assert (attr in q)==(attr in original)
        assert f[':answer-field/key']==sf[':answer-field/key'] and f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        values=[a[':answer/value'] for a in f[':answer-field/choices']];sv=[a[':answer/value'] for a in sf[':answer-field/choices']]
        assert sorted(values)==sorted(sv)
        correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        assert correct==sf[':answer-field/correct'][':answer/value']
        finding=check(record);errors.append({'source_id':key,**finding})
        fidelity.append({'source_id':key,'complete_bank':True,'options':5,'distractors':4,'prompt_exact':True,'solution_exact':True,'presence_exact':True,'correct_designation':True})
        cases.append({'source_id':key,'source_uuid':original[':question/id'],'difficulty':level,'template':template,'parameters':p,'bank_profile':'observed'})
        review.append({'label':'Observed original '+key,'record':record})
        for profile in ('observed','method'):
            pool=g.eligible_parameters(level,template,profile)
            chosen=[p for p in pool if p['u']>1][:1]+[p for p in reversed(pool) if p['u']>1][:1]
            for i,p in enumerate(chosen):
                r=g.generate(level,seed=i+31,template=template,parameters=p,profile=profile);check(r)
                review.append({'label':f'Generated {profile} coordinate-scale variant {key} {i+1}','record':r})
        repaired=g.generate(level,template=template,parameters={'u':1,'v':1,'w':1},profile='source-repaired');check(repaired)
        review.append({'label':'Repaired evidence profile '+key,'record':repaired})
    for template in ('easy_diagonal','moderate_diagonal'):
        level=g.LEVELS[template]
        for i,p in enumerate(g.eligible_parameters(level,template,'method')[::max(1,len(g.eligible_parameters(level,template,'method'))//12)]):
            r=g.generate(level,seed=i,template=template,parameters=p);check(r)
            if i<2:review.append({'label':'Authored '+level+' example '+str(i+1),'record':r})
    # Diverse signed/domain boundary samples of every public complete profile.
    for template,level in g.LEVELS.items():
        for profile in (('observed','source-repaired','method') if template in g.TEMPLATES else ('method',)):
            pool=g.eligible_parameters(level,template,profile);fingerprints=set()
            for p in pool:
                data=g.inverse_data(g.TEMPLATES[template],p) if template in g.TEMPLATES else (g._easy(p) if level=='easy' else g._moderate(p))
                fingerprints.add(tuple(sp.srepr(e) for e in data[0]))
            counts[template+'/'+profile]=len(fingerprints)
            for i in sorted(set([0,len(pool)//3,len(pool)//2,len(pool)-1])):
                r=g.generate(level,seed=93,template=template,parameters=pool[i],profile=profile);check(r)
                twin=g.generate(level,seed=94,template=template,parameters=pool[i],profile=profile)
                assert r['question'][':question/id']==twin['question'][':question/id']
                assert r['generation']['mathematical_fingerprint']==twin['generation']['mathematical_fingerprint']
    # Exercise the real no-template default, not merely explicit source templates.
    default_counts={t:0 for t in g.TEMPLATES if g.LEVELS[t]=='moderate'}
    first_default={}
    for seed in range(48):
        record=g.generate_moderate(seed=seed)
        meta=record['generation'];template=meta['template']
        assert template in default_counts and meta['profile']=='method'
        assert meta['eligible_for_learning'] and not meta['evidence_only']
        default_counts[template]+=1
        if template not in first_default:
            check(record);first_default[template]=seed
            review.append({'label':f'Default moderate family {template}, seed {seed}','record':record})
    assert all(default_counts.values()),('default family coverage',default_counts)
    # Guard violations are rejected rather than silently resampled.
    for level,template,p in [('easy','easy_diagonal',{'a':1}),('easy','easy_diagonal',{'a':13}),('moderate','moderate_diagonal',{'a':2,'b':1}),('moderate','moderate_diagonal',{'a':8,'b':8}),('hard','source_39300',{'u':5,'v':1,'w':1}),('moderate','source_39669',{'u':4,'v':4,'w':1})]:
        try:g.generate(level,template=template,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('unguarded explicit boundary',p))
    for item in review:
        r=item['record'];f=r['question'][':question/answer-fields'][0]
        native.append({'label':item['label'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all owned radio choices; displayed mathematics independently verified'} for a in f[':answer-field/choices']]})
    (D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    (D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
    (D/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
    engine=D.parents[1]/'runs/current/check-engine'
    subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
    native_report=json.loads((D/'native-report.json').read_text())
    output={'status':'pass','source':g.SOURCE,'source_questions':12,'source_banks_matched':12,'source_options_matched':60,'source_distractors_matched':48,'source_correct_designations_matched':12,'exact_prompt_and_solution_replays':12,'raw_solution_structural_errors':2,'raw_solution_values_correct':12,'raw_component_label_fidelity_correct':11,'raw_cofactor_structure_correct':11,'repaired_component_labels_correct':12,'repaired_cofactor_structure_correct':12,'branch_validation':branch,'normal_repairs_pass':True,'fidelity':fidelity,'source_errors':errors,'finite_task_catalogs':counts,'default_moderate_coverage':{'seeds':48,'family_counts':default_counts,'first_seed_per_family':first_default,'authored_diagonal_requires_explicit_template':True},'native_grading':{k:native_report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_engine_provenance':{'binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'harness_source_sha256':hashlib.sha256(engine.with_suffix('.rs').read_bytes()).hexdigest(),'entry_point':native_report['entry_point']},'checks':['actual printed inverse maps','all nine displayed partials','numeric Jacobian','cofactor minor structure','every ordered arithmetic/rewrite/reciprocal stage','complete displayed choice bank and wrong derivative-row operations','full source prose and key-presence parity','signed and explicit bounds','seed/order identity','no-template default moderate covers all six observed method families','native grade_field'],'frozen':{str(p.relative_to(D.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [D.with_suffix('.py'),D/'source.json',D/'readback.py',D/'validate.py',D/'review.json']}}
    (D/'validation.json').write_text(json.dumps(output,indent=2)+'\n')
    (D/'review.md').write_text('# Inverse Jacobian review\n\nRaw source profiles are evidence only. Coordinate-transport variants preserve every opaque historical option without asserting its original error intention. Normal method variants use actual derivative-row mistakes.\n\n'+'\n\n---\n\n'.join('## '+item['label']+'\n\n'+g.markdown(item['record']) for item in review))
    print(json.dumps({k:output[k] for k in ('status','source_banks_matched','source_options_matched','native_grading')},indent=2))
if __name__=='__main__':run()
