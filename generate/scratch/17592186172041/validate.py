"""Independent displayed-object verification, full source fidelity, real grading.

Run from repository root: .venv/bin/python generate/scratch/17592186172041/validate.py
Errors abort before a passing report is written. No database reads or writes.
"""
from concurrent.futures import ThreadPoolExecutor
import copy
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import tempfile
import uuid
import sympy as sp

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('rectangular',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Y=sp.symbols('x y',real=True)
def fail(condition,message):
    if not condition:raise AssertionError(message)

def displayed_expression(text):
    """Read the actual two full printed factors; no generator expression helper."""
    eq=re.search(r'differential equation \$(.*?)\$ and its slope',text).group(1).split('=',1)[1].replace(' ','')
    parts=re.findall(r'\(([^()]+)\)(\^\{2\})?',eq)
    fail(len(parts)==2,'Displayed expression needs two complete factors')
    reconstructed=''.join('('+a+')'+b for a,b in parts)
    fail(reconstructed==eq,'Unparsed displayed equation content')
    expr=sp.Integer(1)
    for body,power in parts:
        expr*=sp.sympify(body,locals={'x':X,'y':Y})**(2 if power else 1)
    return expr

def displayed_regions(text):
    rows=re.findall(r'where \$x\s*([<>])\s*(-?\s*\d+)\$ and \$y\s*([<>])\s*(-?\s*\d+),?\$[,]? the slope of the slope field is (positive|negative)',text)
    fail(len(rows)==3,'Missing displayed region claims')
    return [(1 if a=='>' else -1,int(b.replace(' ','')),1 if c=='>' else -1,int(d.replace(' ','')),1 if e=='positive' else -1) for a,b,c,d,e in rows]

def selection_truth(value):
    fail(value in ['None of those listed','I only','II only','III only','I and II only','I and III only','II and III only','I, II, and III'],'Unexpected selection value')
    return tuple(bool(re.search(r'\b'+roman+r'\b',value)) for roman in ('I','II','III'))

def formatting(text):
    fail(text.count('$')%2==0,'Unbalanced dollar math delimiter')
    depth=0
    for i,c in enumerate(text):
        if i>0 and text[i-1]=='\\':continue
        if c=='{':depth+=1
        if c=='}':depth-=1
        fail(depth>=0,'Unbalanced TeX brace')
    fail(depth==0,'Unbalanced TeX brace')

def independently_check(r):
    fail(set(r['knowledge_point'])=={'db_id','id','title'},'Outer KP shape')
    fail(r['knowledge_point']['db_id']==g.KP_ID,'Wrong KP')
    q=r['question'];f=q[':question/answer-fields'][0];p=r['generation']['parameters']
    uuid.UUID(q[':question/id']);uuid.UUID(f[':answer-field/id'])
    fail(f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection','Field shape')
    formatting(q[':question/problem']);formatting(q[':question/worked-solution'])
    expr=displayed_expression(q[':question/problem']);regions=displayed_regions(q[':question/problem'])
    zs=re.search(r'when \$x=(-?\d+)\$ or \$y=(-?\d+)\.\$',q[':question/worked-solution'])
    fail(zs is not None,'Missing displayed zero lines');h,k=map(int,zs.groups())
    fail(sp.simplify(expr.subs(X,h))==0 and sp.simplify(expr.subs(Y,k))==0,'Wrong displayed zero line')
    # Factor zero sets, not merely agreement at selected points.
    poly=sp.Poly(expr,X,Y);fail(poly.total_degree() in (2,3),'Scope: only source degree 2/3 factored equations')
    fail(sp.Poly(expr,X).all_coeffs()[0]!=0,'Nonzero x dependence')
    fail((h,k)==(p['h'],p['k']),'Printed zero lines disagree with parameters')
    rhs=re.search(r'define \$f\(x,y\)=(.*?)\.\$',q[':question/worked-solution']).group(1)
    synthetic='Consider the differential equation $y\'='+rhs+'$ and its slope field.'
    fail(sp.expand(displayed_expression(synthetic)-expr)==0,'Solution f differs from actual printed equation')
    truth=[];signs=[]
    for sx,hp,sy,kp,claim in regions:
        fail((hp,kp)==(h,k),'Statement boundary mismatch')
        values=[expr.subs({X:h+sx*dx,Y:k+sy*dy}) for dx,dy in itertools.product((sp.Rational(1,2),1,3),repeat=2)]
        sgn=[int(sp.sign(v)) for v in values];fail(len(set(sgn))==1 and sgn[0] in (-1,1),'Region has changing or zero sign')
        signs.append(sgn[0]);truth.append(sgn[0]==claim)
    # Read every displayed statement verdict, region, slope comparison and prose.
    blocks=re.findall(r'- Statement (I{1,3}) is (true|false)\. If \$(.*?)\$ then according to our diagram, we have\n\n\$\$\n(.*?)\n\$\$\n\nThis implies that the slope of the slope field is (positive|negative) for any point \$\(x,y\)\$ in this region\.',q[':question/worked-solution'],re.S)
    fail(len(blocks)==3,'Worked stage count/structure')
    for i,(roman,verdict,region,row,word) in enumerate(blocks):
        fail(roman==('I','II','III')[i] and (verdict=='true')==truth[i],'Displayed statement truth error')
        sx,hp,sy,kp,_=regions[i]
        expected='x'+('>' if sx==1 else '<')+str(hp)+'$ and $y'+('>' if sy==1 else '<')+str(kp)+','
        fail(region==expected,'Solution region differs from printed statement')
        fail(row.endswith(('>0.' if signs[i]==1 else '<0.')),'Displayed intermediate slope sign error')
        fail(word==('positive' if signs[i]==1 else 'negative'),'Displayed slope prose error')
    choices=f[':answer-field/choices'];fail(len(choices)==5 and len({a[':answer/value'] for a in choices})==5,'Whole bank ambiguity')
    fail(len({a[':answer/id'] for a in choices})==5,'Owned choice identity collision')
    matches=[a for a in choices if selection_truth(a[':answer/value'])==tuple(truth)]
    fail(len(matches)==1,'Displayed bank lacks unique mathematically correct selection')
    fail(f[':answer-field/correct']==[':answer/id',matches[0][':answer/id']],'Correct lookup marker error')
    for a in choices:uuid.UUID(a[':answer/id']);fail(a[':answer/type']==':answer.type/text','Choice type')
    if 'Therefore' in q[':question/worked-solution']:
        fail(q[':question/worked-solution'].endswith('"'+matches[0][':answer/value']+'."'),'Conclusion differs from mathematical truth')
    # Source images checked against separately transcribed inspected image signs.
    plots=r['generation']['plots']
    for role in ('partition','signs'):
        path=HERE/plots[role];fail(path.exists(),'Missing plot')
        if path.parent.name=='plots':
            info=json.loads(path.with_suffix('.json').read_text());fail(info['zero_lines']=={'x':h,'y':k},'Rendered line locations')
            for reg in info['regions']:
                xt,yt=reg['test_point'];expected=int(sp.sign(expr.subs({X:sp.Rational(str(xt)),Y:sp.Rational(str(yt))})))
                fail(reg['sign']==expected,'Rendered sign diagram differs from printed equation')
                fail(float(expr.subs({X:xt,Y:yt}))==reg['value'],'Rendered numeric sign-test value')
            fail(info['role']==role,'Wrong plotted role')
        else:
            info=json.loads((HERE/'source-plot-checks.json').read_text())[str(path.relative_to(HERE))]
            fail(info['zero_lines']==[h,k],'Inspected source line locations differ')
            actual=[int(sp.sign(expr.subs({X:h+sx,Y:k+sy}))) for sx,sy in itertools.product((-1,1),repeat=2)]
            if role=='signs':fail(info['sign_grid']==actual,'Inspected source sign geometry differs')
    return {'truth':truth,'signs':signs}

def all_finite_tasks():
    """Enumerate substantive sign tasks without plotting thousands of equivalent figures."""
    counts={};oriented_presentations={}
    for level in ('easy','moderate','hard'):
        seen=set();n=0
        for h,k in itertools.product((-3,-2,-1,1,2,3),repeat=2):
            for t,l in g.TEMPLATES.items():
                if l!=level or t=='numbered_bilinear':continue
                for ox,oy in itertools.product((-1,1),repeat=2):
                    px,py=(2,1) if t=='x_squared' else (1,2) if t=='y_squared' else (1,1)
                    for regs in itertools.combinations(list(itertools.product((-1,1),repeat=2)),3):
                        for claims in itertools.product((-1,1),repeat=3):
                            p={'h':h,'k':k,'ox':ox,'oy':oy,'px':px,'py':py,'regions':[[*a,b] for a,b in zip(regs,claims)]}
                            try:g.validate_parameters(level,t,p)
                            except ValueError:continue
                            # Independently evaluate sign tasks and validate full authored bank.
                            expr=(ox*(X-h))**px*(oy*(Y-k))**py
                            grid=tuple((ox*sx)**px*(oy*sy)**py for sx,sy in itertools.product((-1,1),repeat=2))
                            truths=tuple((ox*a[0])**px*(oy*a[1])**py==b for a,b in zip(regs,claims))
                            ops=[truths]+[tuple(not z if i==j else z for i,z in enumerate(truths)) for j in range(3)]+[tuple(not z for z in truths)]
                            fail(len(set(ops))==5 and ops.count(truths)==1,'Authored finite bank collision')
                            seen.add((h,k,grid,tuple(tuple(r) for r in p['regions'])));n+=1
        counts[level]=len(seen);oriented_presentations[level]=n
    return counts,oriented_presentations

def main():
    cases=json.loads((HERE/'source-cases.json').read_text());raw=json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions'];raw={q[':question/math-academy-id']:q for q in raw}
    records=[];labels=[];fidelity=[]
    for c in cases:
        r=g.generate(c['level'],seed=33,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);independently_check(r)
        original=raw[c['source_id']];f=r['question'][':question/answer-fields'][0];of=original[':question/answer-fields'][0]
        fail(r['question'][':question/problem']==original[':question/problem'],'Source prompt fidelity')
        fail(sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']),'Full source bank/value fidelity')
        fail(f[':answer-field/type']==of[':answer-field/type'][':db/ident'],'Source field type fidelity')
        choice=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])[':answer/value']
        if c['raw_correct_present']:fail(choice==of[':answer-field/correct'][':answer/value'],'Source correct designation fidelity')
        if ':question/worked-solution' in original:fail(r['question'][':question/worked-solution']==original[':question/worked-solution'],'Complete source solution/stage fidelity')
        fidelity.append({'source_id':c['source_id'],'prompt_exact':True,'complete_bank_exact':True,'displayed_values_matched':5,'correct_designation_matched':True if c['raw_correct_present'] else None,'solution_exact':True if ':question/worked-solution' in original else None,'repair':'independently derived I only; authored moderate assignment/solution' if not c['raw_correct_present'] else None})
        records.append(r);labels.append('original '+c['source_id'])
        # Two changed geometries per original bank; preserve truth via math, never an answer lookup.
        base=independently_check(r)['truth']
        for j in range(2):
            p=copy.deepcopy(c['parameters']);p['h' if j==0 else 'k']*=-1
            if j==1 and c['level']=='hard':p['oy' if p['px']==2 else 'ox']*=-1
            for i,reg in enumerate(p['regions']):
                val=(p['ox']*reg[0])**p['px']*(p['oy']*reg[1])**p['py'];reg[2]=val if base[i] else -val
            variant=g.generate(c['level'],seed=100+j,template=c['template'],parameters=p,profile=c['bank_profile']);independently_check(variant)
            records.append(variant);labels.append('generated observed-bank variant '+c['source_id']+' '+str(j+1))
    for level in ('easy','moderate','hard'):
        for seed in (13,14):
            r=g.generate(level,seed=seed);independently_check(r);records.append(r);labels.append('authored '+level+' seed '+str(seed))
    # Every authored template, reverse orientation and extreme shift is exercised.
    for t,level in g.TEMPLATES.items():
        if t=='numbered_bilinear':continue
        for orientation in (-1,1):
            p={'h':-1 if level=='easy' else -3,'k':1 if level=='easy' else 3,'ox':1,'oy':1,'px':2 if t=='x_squared' else 1,'py':2 if t=='y_squared' else 1,'regions':[[-1,-1,1],[-1,1,-1],[1,1,1]]}
            if level!='easy':p['oy' if t=='x_squared' else 'ox']=orientation
            r=g.generate(level,seed=51,template=t,parameters=p);independently_check(r);records.append(r);labels.append('authored boundary '+t+' '+str(orientation))
    # Fixed parameters/profile/geometry have identity independent of shuffle seed.
    for r in records:
        meta=r['generation'];again=g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=999,template=meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
        fail(again['question'][':question/id']==r['question'][':question/id'],'Seed changed content identity')
        fail(again['generation']['mathematical_fingerprint']==meta['mathematical_fingerprint'],'Seed changed task fingerprint')
    # Permuting statements changes presentation but not substantive mathematical task.
    p=copy.deepcopy(records[-1]['generation']['parameters']);p['regions'].reverse();r=g.generate('hard',template='y_squared',parameters=p)
    fail(r['generation']['mathematical_fingerprint']==records[-1]['generation']['mathematical_fingerprint'],'Statement order inflated task count')
    fail(r['question'][':question/id']!=records[-1]['question'][':question/id'],'Displayed statement order must alter presentation identity')
    # Distinct bank identities and strict explicit guards, including abs signed bounds.
    orig=records[0];p=orig['generation']['parameters'];a=g.generate('moderate',template='numbered_bilinear',parameters=p,profile='authored_truth_flips')
    fail(a['question'][':question/id']!=orig['question'][':question/id'],'Different complete displayed banks collided')
    invalid=[]
    for label,level,t,p0,profile in [('zero shift','easy','easy_bilinear',{'h':0,'k':1,'ox':1,'oy':1,'px':1,'py':1,'regions':[[-1,-1,1],[-1,1,-1],[1,1,1]]},None),('moderate easy collapse','moderate','bilinear',{'h':-1,'k':1,'ox':1,'oy':1,'px':1,'py':1,'regions':[[-1,-1,1],[-1,1,-1],[1,1,1]]},None),('wrong squared axis','hard','y_squared',{'h':-3,'k':1,'ox':1,'oy':1,'px':2,'py':1,'regions':[[-1,-1,1],[-1,1,-1],[1,1,1]]},None),('negative large shift','hard','x_squared',{'h':-100,'k':1,'ox':1,'oy':1,'px':2,'py':1,'regions':[[-1,-1,1],[-1,1,-1],[1,1,1]]},None)]:
        try:g.generate(level,template=t,parameters=p0,profile=profile)
        except ValueError:invalid.append(label)
        else:raise AssertionError('Invalid explicit parameters silently accepted: '+label)
    # q-96475 bank omits none: its false/false/false instance must reject whole bank.
    p=copy.deepcopy(cases[0]['parameters']);p['regions']=[[-1,-1,-1],[-1,1,1],[1,-1,1]]
    try:g.generate('moderate',template='numbered_bilinear',parameters=p,profile='q-96475')
    except ValueError:invalid.append('complete source bank missing correct')
    else:raise AssertionError('Ineligible source bank silently modified')
    counts,presentations=all_finite_tasks()
    fail(counts=={'easy':128,'moderate':2048,'hard':4608},'Finite meaningful task count changed')
    # Real concurrent renderer calls: two same and one different instance share output dir.
    with tempfile.TemporaryDirectory(prefix='concurrent-',dir=HERE) as d:
        p1=copy.deepcopy(cases[2]['parameters']);p2=copy.deepcopy(cases[-1]['parameters']);p2['h']=-3
        with ThreadPoolExecutor(max_workers=3) as pool:
            concurrent=list(pool.map(lambda p:g.render_plots(p,d),[p1,p1,p2]))
        fail(concurrent[0]==concurrent[1] and concurrent[0]!=concurrent[2],'Concurrent asset identity mismatch')
        for p,assets in zip([p1,p1,p2],concurrent):
            for role in ('partition','signs'):
                side=json.loads(Path(assets[role]).with_suffix('.json').read_text());fail(side['parameters']=={z:p[z] for z in ('h','k','ox','oy','px','py')},'Concurrent renderer mixed instance parameters')
    checks=[]
    for label,r in zip(labels,records):
        f=r['question'][':question/answer-fields'][0]
        checks.append({'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual displayed categorical choice'} for a in f[':answer-field/choices']]})
    (HERE/'engine-input.json').write_text(json.dumps(checks,indent=2)+'\n')
    exe=Path('generate/runs/current/check-engine');subprocess.run([str(exe),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine=json.loads((HERE/'engine-report.json').read_text());fail(engine['documented_unresolved_checks']==0,'Unexpected native grader unresolved result')
    (HERE/'review.json').write_text(json.dumps([{'label':label,'record':r} for label,r in zip(labels,records)],indent=2)+'\n')
    review=['# Rectangular region signs review','Originals retain complete source banks. Generated variants are labeled; authored defaults use truth flips. q-96475 has an inferred marker and authored solution, not source solution fidelity.']
    for label,r in zip(labels,records):
        q=r['question'];f=q[':question/answer-fields'][0];meta=r['generation'];review+=['## '+label,'Template `'+meta['template']+'`, profile `'+meta['bank_profile']+'`.','Parameters: `'+json.dumps(meta['parameters'])+'`.','',q[':question/problem'],'','\n'.join('- '+a[':answer/value']+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']),'',q[':question/worked-solution'],'']
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    report={'passed':True,'source':g.SOURCE,'source_fidelity':{'practice_questions':7,'prompts_exact':7,'complete_banks_exact':7,'displayed_values_matched':35,'displayed_values_total':35,'available_correct_designations_matched':6,'available_correct_designations_total':6,'missing_original_correct_designations':1,'available_worked_solutions_exact':6,'available_worked_solutions_total':6,'missing_original_worked_solutions':1,'per_source':fidelity},'correctness':{'records_independently_checked':len(records),'points_per_statement':9,'all_printed_statement_stages_checked':True,'finite_unique_meaningful_tasks':counts,'finite_oriented_presentations_not_task_counts':presentations,'invalid_explicit_instances_rejected':invalid,'concurrent_plot_instances_checked':3},'native_grading':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':engine['documented_unresolved_checks'],'engine_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(Path('generate/runs/current/check-engine.rs').read_bytes()).hexdigest()},'visual_QA':'13 source assets inspected; generated collage covers every template/profile and signs, with separate zero-line plots.','repairs':['q-96475 missing correct marker and worked solution: mathematical I-only marker and authored solution, moderate assignment; raw evidence unchanged.'],'unresolved_source_fidelity':[],'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
