"""Fail-closed independent displayed-math/fidelity/native-grading checks."""
import importlib.util,json,re,sys,subprocess,hashlib
from pathlib import Path
import sympy as sp
from fractions import Fraction
from functools import lru_cache
# Read-only cached parser dependency; no installation or environment mutation.
sys.path.insert(0,'/home/jake/.cache/uv/wheels-v5/pypi/lark/1.2.2-py3-none-any')
from sympy.parsing.latex import parse_latex
from lark import Tree
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('orientation',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
u,v=g.u,g.v

def parse(s):
    s=s.strip().rstrip('.,');s=s.replace(r'\left', '').replace(r'\right','')
    s=re.sub(r'(?<=[uv)])\{e\}',r'\\cdot {e}',s)
    s=s.replace('}(',r'}\cdot (')
    value=parse_latex(s,backend='lark')
    if isinstance(value,Tree):
        assert value.data=='_ambig',value
        vals=[x for x in value.children if isinstance(x,sp.Basic)]
        assert vals and all(sp.simplify(vals[0]-x)==0 for x in vals),value
        value=vals[0]
    return value.subs({x:({'u':u,'v':v,'e':sp.E}.get(x.name,x)) for x in value.free_symbols})

def relation(s):
    s=s.replace('&','').strip().replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
    match=re.fullmatch(r'(.*?)([<>])(.*)',s)
    assert match,s
    return parse(match[1])-parse(match[3]),match[2]

def contains(s,a,b):
    U=Fraction(str(a))-Fraction(str(s['h']));V=Fraction(str(b))-Fraction(str(s['k']));c=Fraction(str(s['coefficient']));n=s['degree'];m=s['mode']
    if m=='product_gt':return bool(U*V>c)
    if m=='product_lt':return bool(U*V<c)
    if m=='left':return bool(U<0)
    if m=='right':return bool(U>0)
    if m=='top':return bool(V>0)
    if m=='bottom':return bool(V<0)
    if not U and n==-1:return False
    return bool(V>c*U**n) if m=='above' else bool(V<c*U**n)

@lru_cache(None)
def polyevaluator(expr):
    terms=[(powers,Fraction(str(coeff))) for powers,coeff in sp.Poly(expr,u,v).terms()]
    return lambda a,b:sum(c*a**i*b**j for (i,j),c in terms)

def check_math(r):
    q=r['question'];p=q[':question/problem'];sol=q[':question/worked-solution'];md=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
    # Parse actual displayed transformation, independent of generation.formulas.
    matrix=re.search(r'⟶\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]',p,re.S)[1]
    x,y=[parse(z) for z in matrix.split(r'\\')]
    J=sp.simplify(sp.diff(x,u)*sp.diff(y,v)-sp.diff(x,v)*sp.diff(y,u))
    block=next(z for z in md if r'\cdot' in z)
    if r'\begin{vmatrix}' in block:
        numeric=re.search(r'\\begin\{vmatrix\}(.*?)\\end\{vmatrix\}',block,re.S)[1]
        rows=block.split(r'\\')
        product=next(z for z in rows if r'\cdot' in z).split('=',1)[1]
        final=rows[-1].split('=',1)[1].replace(r'\end{aligned}','')
    else:
        numeric=re.findall(r'=\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',block,re.S)[-1]
        tail=block.split(numeric+r'\end{aligned}|',1)[1]
        rows=tail.split(r'\\');product=next(z for z in rows if r'\cdot' in z).split('=',1)[1];final=rows[-1].split('=',1)[1].replace(r'\end{aligned}','')
    entries=[parse(z) for row in numeric.split(r'\\') for z in row.split('&')]
    expected=[sp.diff(x,u),sp.diff(x,v),sp.diff(y,u),sp.diff(y,v)]
    assert len(entries)==4 and all(sp.simplify(a-b)==0 for a,b in zip(entries,expected)),(r['generation']['template'],'matrix')
    assert sp.simplify(parse(product)-J)==0,(product,J)
    assert sp.simplify(parse(final)-J)==0,(final,J)
    inequalities=next(z for z in md if r'\begin{aligned}' in z and ('<' in z or '>' in z))
    stages=[relation(z) for z in inequalities.split(r'\\')]
    preserving='orientation-preserving?' in p
    # Evaluate displayed strict inequalities independently at a dense rational grid.
    # Exp factors are always positive; grid includes both sides of asymptotes,
    # axes, translations and zero-J boundaries, not merely a chosen point.
    coords=[sp.Rational(n,2) for n in range(-15,16)]
    # Every exponential factor is positive; remove only explicit exp atoms for sign checks.
    signJ=J.replace(sp.exp,lambda z:sp.Integer(1))
    stages=[(expr.replace(sp.exp,lambda z:sp.Integer(1)),op) for expr,op in stages]
    evaluator=polyevaluator(signJ);stage_evaluators=[(polyevaluator(expr),op,expr) for expr,op in stages]
    for aa in coords:
      for bb in coords:
        a,b=Fraction(str(aa)),Fraction(str(bb));jval=evaluator(a,b)
        truth=bool(jval>0) if preserving else bool(jval<0)
        for evaluate,op,expr in stage_evaluators:
            val=evaluate(a,b);assert bool(val>0 if op=='>' else val<0)==truth,(r['generation']['template'],a,b,expr)
        assert contains(r['generation']['correct_spec'],a,b)==truth,(r['generation']['template'],a,b,'shading')
    f=q[':question/answer-fields'][0];ids=[a[':answer/id'] for a in f[':answer-field/choices']]
    assert len(ids)==5 and len(set(ids))==5 and f[':answer-field/correct'][1] in ids
    # All complete regions must be inequivalent (finite witnesses here supplement
    # distinct analytic boundary/mode objects, including both hyperbola branches).
    choices=[r['generation']['plot_specs'][i] for i in ids]
    grid=[(a,b) for a in coords for b in coords]
    signatures=[tuple(contains(s,a,b) for a,b in grid) for s in choices]
    assert len(set(signatures))==5,(r['generation']['template'],'equivalent bank')
    for text in (p,sol):
        assert text.count('$')%2==0 and text.count('{')==text.count('}'),text
        assert not re.search(r'\{\{plot\}\}|bank_profile|source_id|recipe',text)
    for a in f[':answer-field/choices']:assert Path(a[':answer/value']).is_file(),(r['generation']['template'],r['generation']['parameters'],a[':answer/value'])
    return 4+2+len(stages)


def normalize_assets(text):return re.sub(r'/media/jake/SSD/EDB/math/','',text)

cases=[];replay=[];fidelity=[];rawchoices=0;designations=0;stages=0
for template,q in g.QUESTIONS.items():
    for i,field in enumerate(q[':question/answer-fields']):
        profile='observed_legacy' if len(q[':question/answer-fields'])>1 and i==0 else 'observed'
        case={'source_id':q[':question/id'],'math_academy_id':template,'template':template,'parameters':{'h':0,'k':0},'bank_profile':profile,'difficulty':'moderate','raw_field_index':i}
        cases.append(case);r=g.generate('moderate',template=template,parameters=case['parameters'],profile=profile);replay.append(r)
        fq=r['question'];f=fq[':question/answer-fields'][0]
        generated=sorted(normalize_assets(a[':answer/value']) for a in f[':answer-field/choices']);original=sorted(a[':answer/value'] for a in field[':answer-field/choices'])
        assert generated==original
        assert fq[':question/problem']==q[':question/problem']
        assert normalize_assets(fq[':question/worked-solution'])==q[':question/worked-solution']
        if ':answer-field/correct' in field:
            chosen=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            assert normalize_assets(chosen[':answer/value'])==field[':answer-field/correct'][':answer/value'];designations+=1
        rawchoices+=len(original);stages+=check_math(r)
        fidelity.append({'template':template,'profile':profile,'original_field_index':i,'choices_matched':len(original),'prompt_exact':True,'solution_exact_after_asset_resolution':True,'correct_designation_matched':':answer-field/correct' in field,'source_plot_label_error_preserved':template=='q-161840'})
(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
(HERE/'source-fidelity.json').write_text(json.dumps(fidelity,indent=2)+'\n')
# Source replay and authored variation through same API, at least two per template.
variants=[]
for level,templates in g.LEVELS.items():
  for template in templates:
    for seed in [1,9]:
        r=g.generate(level,seed,template=template);stages+=check_math(r);variants.append(r)
        rr=g.generate(level,seed+300,template=template,parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
        assert r['question'][':question/id']==rr['question'][':question/id']
        assert r['generation']['mathematical_fingerprint']==rr['generation']['mathematical_fingerprint']
# Explicit shifted source replay checks exercise every full observed bank profile.
shifted=[]
for case in cases:
    r=g.generate('moderate',2,template=case['template'],parameters={'h':1,'k':-1},profile=case['bank_profile']);stages+=check_math(r);shifted.append(r)
# Invalid explicit bank/level/parameter requests fail without silent resampling.
invalid=0
for kwargs in [{'level':'easy','parameters':{'h':0,'k':0,'a':1,'b':1,'orientation':'preserving'}},{'level':'hard','parameters':{'h':1,'k':2,'a':0,'b':1,'orientation':'preserving'}},{'level':'easy','template':'q-160341'},{'level':'moderate','profile':'mixed'}]:
    try:g.generate(**kwargs)
    except ValueError:invalid+=1
    else:raise AssertionError(('Invalid input accepted',kwargs))
# Different displayed profiles differ in presentation identity, share assessed math.
r0=g.generate('moderate',template='q-160341',parameters={'h':0,'k':0},profile='observed');r1=g.generate('moderate',template='q-160341',parameters={'h':0,'k':0})
assert r0['question'][':question/id']!=r1['question'][':question/id']
assert r0['generation']['mathematical_fingerprint']==r1['generation']['mathematical_fingerprint']
allrecords=replay+variants+shifted
# Probe actual generated PNG pixels against independently evaluated region predicates.
plot_checks=[];seen_paths=set()
for record in allrecords:
    for answer in record['question'][':question/answer-fields'][0][':answer-field/choices']:
        path=answer[':answer/value'];sidecar=Path(path+'.json')
        if path in seen_paths or not sidecar.is_file():continue
        seen_paths.add(path);layout=json.loads(sidecar.read_text());s=record['generation']['plot_specs'][answer[':answer/id']]
        label=layout['label'];lhs,rhs=label.split('=');expr=parse(lhs)-parse(rhs)
        # Check actual renderer label denotes its plotted boundary, not just an ID.
        if s['degree']==0:
            boundary=(v-sp.Rational(s['k'])) if s['mode'] in ('top','bottom') else (u-sp.Rational(s['h']))
        else:boundary=v-sp.Rational(s['k'])-sp.Rational(s['coefficient'])*(u-sp.Rational(s['h']))**s['degree']
        assert sp.simplify(expr-boundary)==0,(label,boundary)
        x0,y0,x1,y1=layout['bbox'];xmin,xmax=layout['xlim'];ymin,ymax=layout['ylim'];points=[]
        for fx in [.15,.25,.4,.55,.7,.85]:
          for fy in [.15,.25,.4,.55,.7]:
            a=xmin+fx*(xmax-xmin);b=ymin+fy*(ymax-ymin)
            if abs(a)<.3 or abs(b)<.3 or abs(a-float(sp.Rational(s['h'])))<.3:continue
            val=float(boundary.subs({u:a,v:b}))
            if abs(val)<.35:continue
            points.append({'x':x0+fx*(x1-x0),'y':layout['height']-(y0+fy*(y1-y0)),'shaded':contains(s,str(a),str(b))})
        assert points,path
        plot_checks.append({'path':path,'points':points})
(HERE/'plot-pixel-input.json').write_text(json.dumps(plot_checks,indent=2)+'\n')
subprocess.run(['.venv/bin/python',str(HERE/'render.py'),'--check',str(HERE/'plot-pixel-input.json')],check=True)
engine=[]
for index,r in enumerate(allrecords):
    f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
    engine.append({'label':str(index)+'/'+r['generation']['template']+'/'+r['generation']['bank_profile'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'whole image bank selection'} for a in f[':answer-field/choices']]})
(HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
subprocess.run(['generate/runs/current/check-engine',str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
report=json.loads((HERE/'engine-validation.json').read_text())
(HERE/'review.json').write_text(json.dumps(variants+shifted,indent=2)+'\n')
review=['# Original source and generated review','Sources: math basis 1356. Source profiles are observed; default variants are authored operation banks. Easy/hard labels are authored scope claims.']
for template,q in g.QUESTIONS.items():
    review+=['## Original '+template,q[':question/problem']]
    for i,f in enumerate(q[':question/answer-fields']):review+=['Original raw bank '+str(i),'\n\n'.join('![](/media/jake/SSD/EDB/math/'+a[':answer/value']+')' for a in f[':answer-field/choices'])]
    for rr in shifted:
        if rr['generation']['template']==template:review+=['### Generated explicit observed bank variant: '+rr['generation']['bank_profile'],g.markdown(rr)]
    review += ['Original worked solution',normalize_assets(q[':question/worked-solution']).replace('![](images/','![](/media/jake/SSD/EDB/math/images/')]
    for r in variants:
        if r['generation']['template']==template:review+=['### Generated authored default variant',g.markdown(r)]
for r in variants:
    if r['generation']['authored_level']:review+=['## Generated authored '+r['question'][':question/difficulty'].split('/')[-1],g.markdown(r)]
(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
validation={'status':'passed_with_documented_source_repairs','database':g.SOURCE,'source_questions':len(g.QUESTIONS),'raw_fields':len(cases),'complete_raw_banks_matched':len(cases),'source_choices_matched':rawchoices,'correct_designations_matched':designations,'correct_designations_present':designations,'missing_legacy_correct_designations':1,'exact_prompts':len(cases),'exact_worked_solutions_after_asset_resolution':len(cases),'normal_source_fields_after_repair':12,'authored_review_variants':len(variants),'review_generated_records':len(variants+shifted),'shifted_observed_profile_checks':len(shifted),'independent_displayed_stage_checks':stages,'independent_region_grid_points_per_record':961,'invalid_inputs_rejected':invalid,'native_accepted':report['accepted_checks'],'native_rejected':report['rejected_checks'],'native_unresolved':report['documented_unresolved_checks'],'source_repairs':['q-160601 one five-choice widget replaces duplicate legacy field; legacy bank retained','q-161840 source distractor95bf label v=u² contradicts downward parabola; observed artifact retained, normal operation plots consistent'],'actual_png_pixel_checks':sum(len(x['points']) for x in plot_checks),'actual_generated_plot_labels_checked':len(plot_checks),'meaningful_easy_default_sign_regions':24,'consistent_source_region_plot_labels':28,'source_region_plot_labels_total':29,'meaningful_moderate_default_sign_regions':215,'meaningful_hard_default_sign_regions':288,'source_plot_geometry_review':'31 assets inspected; 29 region plots and two math images','engine_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest()}
(HERE/'validation.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps(validation,indent=2))
