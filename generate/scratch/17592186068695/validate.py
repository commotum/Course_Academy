#!/usr/bin/env python3
"""Independent graph/slot/fidelity checks, then actual grade_field radio checks."""
import copy, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('continuity_generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

# Independently transcribed local predicates from actual source rasters.
EXPECTED={
 'q-48039':{'4020dd89':('pole',False),'4a009c92':('jump',False),'56576892':('point',False),'f4a28f88':('connected',True),'29ff22e9':('pole',False)},
 'q-48081':{'0a31db89':('point',False),'8c2cca8f':('pole',False),'fdd6b61f':('connected',True),'56a689e2':('pole',False),'4ad2a8ae':('jump',False)},
 'q-69782':{'42e1d990':('jump',False),'d124370f':('connected',True),'17fc3c79':('pole',False),'76a1b2ca':('point',False),'135973e3':('pole',False)},
 'q-48082':{'c6f0914f':('connected',True),'c2f85d1a':('pole',False),'14349b3d':('jump',False),'3073f651':('point',False),'c95d9944':('unilateral_pole',False)},
 'q-102106':[('connected',True),('connected',True),('pole',False)],
 'q-78133':[('jump',False),('connected',True),('point',False)],
 'q-102115':[('jump',False),('point',False),('connected',True)],
 'q-78131':[('pole',False),('connected',True),('connected',True)],
 'q-78132':[('connected',True),('jump',False),('connected',True)]}


def scalar(v):return sp.Rational(v)
def limit_status(obj,t):
    """Independent exact graph evaluator; no generator's inspect_at invocation."""
    x=sp.Symbol('x',real=True);t=scalar(t);ls=[];rs=[];vals=[]
    for row in obj['segments']:
        a,b=map(scalar,(row['lo'],row['hi']));expr=sp.sympify(row['expr'],locals={'x':x},evaluate=False)
        if a<t<=b:ls.append(sp.limit(expr,x,t,dir='-'))
        if a<=t<b:rs.append(sp.limit(expr,x,t,dir='+'))
        if a<t<b and str(t) not in obj['holes']+obj['poles']+row.get('raw_excluded',[]):
            v=expr.subs(x,t)
            if v.is_finite:vals.append(v)
    if str(t) in obj['values']:vals=[scalar(obj['values'][str(t)])]
    assert len(set(map(str,vals)))<=1,'Graph is not a function'
    l=ls[0] if ls else None;r=rs[0] if rs else None;v=vals[0] if vals else None
    assert all(z==l for z in ls) and all(z==r for z in rs),'Overlapping disagreeing branches'
    finite=l is not None and r is not None and l.is_finite is True and r.is_finite is True
    exists=bool(finite and sp.simplify(l-r)==0)
    return {'left':str(l),'right':str(r),'value':str(v),'defined':v is not None,'limit_exists':exists,
            'limit_matches_value':bool(exists and v is not None and sp.simplify(v-l)==0),
            'continuous':bool(exists and v is not None and sp.simplify(v-l)==0)}


def check_math(s):
    assert not any(ord(c)<32 and c not in '\n\t' for c in s),'Control character'
    assert s.count('$')%2==0,'Unbalanced math dollars'
    depth=0
    for i,c in enumerate(s):
        if i and s[i-1]=='\\':continue
        if c=='{':depth+=1
        if c=='}':depth-=1
        assert depth>=0,'Unmatched brace'
    assert depth==0,'Unmatched brace'


def read_coordinates(s):
    # Read the actual printed x coordinates, including authored fractional slots.
    out=[]
    for m in re.finditer(r'x=([^$]*?)(?=\$)',s):
        z=m[1].rstrip('.,?').replace(' ','')
        if z.startswith('\\frac') or z.startswith('-\\frac'):
            p=re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(\d+)\}',z)
            assert p,z;out.append(scalar(('-' if p[1] else '')+p[2]+'/'+p[3]))
        else:out.append(scalar(z))
    return out


def graph_equivalence(a,b):
    # Complete piecewise graph equality respects every segment/exclusion/value.
    if a['values']!=b['values'] or a['holes']!=b['holes'] or a['poles']!=b['poles']:return False
    knots=sorted(set(scalar(s[k]) for ob in (a,b) for s in ob['segments'] for k in ('lo','hi')))
    x=sp.Symbol('x',real=True)
    for lo,hi in zip(knots,knots[1:]):
        mid=(lo+hi)/2
        ea=[sp.sympify(s['expr'],locals={'x':x}) for s in a['segments'] if scalar(s['lo'])<mid<scalar(s['hi'])]
        eb=[sp.sympify(s['expr'],locals={'x':x}) for s in b['segments'] if scalar(s['lo'])<mid<scalar(s['hi'])]
        if bool(ea)!=bool(eb):return False
        if ea and sp.simplify(ea[0]-eb[0])!=0:return False
    return True


def raster_markers(path,side):
    """Read the actual PNG centers/rings at independently derived graph points."""
    im=np.asarray(Image.open(path).convert('RGB'));h,w=im.shape[:2];tf=side['pixel_transform'];obj=side['graph'];x=sp.Symbol('x',real=True)
    def color_at(a,v,filled):
        px=int(round(tf['x_offset']+tf['x_scale']*float(scalar(a))));py=int(round(tf['y_offset']+tf['y_scale']*float(scalar(v))))
        if not (8<=px<w-8 and 8<=py<h-8):return
        crop=im[py-7:py+8,px-7:px+8];red=(crop[:,:,0]>175)&(crop[:,:,1]<110)&(crop[:,:,2]<110)
        center=red[6:9,6:9]
        if filled:assert center.sum()>=5,(path,a,v,'missing filled marker')
        else:assert center.sum()==0 and red.sum()>=10,(path,a,v,'missing open marker')
    for a in obj['holes']:
        for b in obj['segments']:
            if scalar(b['lo'])<=scalar(a)<=scalar(b['hi']):
                v=sp.sympify(b['expr'],locals={'x':x}).subs(x,scalar(a))
                if v.is_finite:color_at(a,str(v),False);break
    for a,v in obj['values'].items():
        if not limit_status(obj,a)['continuous'] or a in obj.get('marked_values',[]):color_at(a,v,True)
    for a,v in obj.get('open_annotations',[]):color_at(a,v,False)
    # Open finite jump endpoints are read separately from every filled endpoint.
    for b in obj['segments']:
        expr=sp.sympify(b['expr'],locals={'x':x})
        for endpoint,direction in ((b['lo'],'+'),(b['hi'],'-')):
            a=scalar(endpoint)
            if a in (scalar(obj['bounds'][0]),scalar(obj['bounds'][1])):continue
            v=sp.limit(expr,x,a,dir=direction)
            if v.is_finite and not limit_status(obj,endpoint)['continuous'] and obj['values'].get(str(a))!=str(v):color_at(endpoint,str(v),False)


def audit(r):
    q=r['question'];meta=r['generation'];t=meta['source_id'];p=meta['parameters'];level=meta['requested_level'];raw=meta['bank_profile'] in ('observed','current')
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    for k in (':question/problem',':question/worked-solution'):check_math(q[k])
    # The prompt is the source of queried coordinates, not generation metadata.
    printed=read_coordinates(q[':question/problem']);assert list(map(str,printed))==meta['targets']
    assert all(a in printed for a in read_coordinates(q[':question/worked-solution'])) or g.SPECS[t]['level']=='easy'
    # Final source prose has context points outside the queried point for easy.
    if level=='hard':assert sum(a.q==2 for a in printed)>=2 and meta['half_unit_target_readings']==sum(a.q==2 for a in printed)
    elif not raw:assert all(a.q==1 for a in printed)
    for path,obj in meta['graphs'].items():
        assert scalar(obj['bounds'][0])<0<scalar(obj['bounds'][1]) and scalar(obj['bounds'][2])<0<scalar(obj['bounds'][3]),'Zero axes hidden or relocated'
        if path.startswith('images/'):
            assert (Path('/media/jake/SSD/EDB/math')/path).is_file()
        else:
            side=json.loads(Path(path).with_suffix('.json').read_text());assert side['graph']==obj;assert side['targets']==meta['targets'];raster_markers(path,side)
            if level=='hard':assert all(scalar(v).q==1 for v in side['tick_values']) and side['tick_step']=='1' and any(a not in list(map(scalar,side['tick_values'])) for a in printed)
    if g.SPECS[t]['level']=='easy':
        f=q[':question/answer-fields'][-1];correct=f[':answer-field/correct'][1]
        objects=[meta['graphs'][a[':answer/value']] for a in f[':answer-field/choices']]
        for i,a in enumerate(f[':answer-field/choices']):
            st=limit_status(meta['graphs'][a[':answer/value']],printed[0]);assert st['continuous']==(a[':answer/id']==correct)
        selected=next(meta['graphs'][a[':answer/value']] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
        contextual=[scalar(p['scale'])*scalar(str(a))+scalar(p['shift']) for a in g.SPECS[t].get('context',[])]
        solution_points=read_coordinates(q[':question/worked-solution'])
        assert printed[0] in solution_points
        assert set(solution_points)<=set(printed+contextual),'Stale easy prose coordinate'
        for a in contextual:assert not limit_status(selected,a)['continuous'],'False unrelated-discontinuity prose claim'
        for i,a in enumerate(objects):
            for b in objects[i+1:]:assert not graph_equivalence(a,b),'Equivalent complete graph choices'
        # Match EVERY per-option local topology against independent raster notes.
        for prefix,(kind,continuous) in EXPECTED[t].items():
            obj=g.transformed(g.G[prefix],p);st=limit_status(obj,printed[0]);assert st['continuous']==continuous
            if kind=='jump':assert st['defined'] and not st['limit_exists'] and st['left']!=st['right']
            if kind=='point':assert st['defined'] and st['limit_exists'] and not st['limit_matches_value']
            if 'pole' in kind:assert not st['limit_exists']
    else:
        path=re.findall(r'!\[\]\(([^)]+)\)',q[':question/problem'])[0];obj=meta['graphs'][path]
        statuses=[limit_status(obj,a) for a in printed];assert statuses==meta['continuity_checks']
        for st,(kind,value) in zip(statuses,EXPECTED[t]):
            assert st['continuous']==value
            if kind=='point':assert st['defined'] and st['limit_exists'] and not st['limit_matches_value']
            if kind=='jump':assert st['defined'] and not st['limit_exists'] and st['left']!=st['right']
            if kind=='pole':assert not st['limit_exists']
        wanted=g.subset_text([s['continuous'] for s in statuses])
        if q.get(':question/answer-fields'):
            fs=q[':question/answer-fields']
            if fs[0][':answer-field/type']==':answer-field.type/checkbox':
                assert [f[':answer-field/key'] for f in fs]==g.ROMAN
                for f,st in zip(fs,statuses):
                    assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==str(st['continuous']).lower()
            else:
                f=fs[0];assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==wanted
        # Each local solution sentence and final prose must match actual graph.
        bullets=[b for b in q[':question/worked-solution'].split('\n\n') if b.startswith('- ')]
        assert len(bullets)==3
        for b,a,st in zip(bullets,printed,statuses):
            assert a in read_coordinates(b) or '$'+g.tex(a)+'.$' in b
            assert ('is not continuous' in b)==(not st['continuous'])
        assert '"'+wanted+'"' in q[':question/worked-solution']
    for f in q.get(':question/answer-fields',[]):
        assert f[':answer-field/type'] in (':answer-field.type/radio',':answer-field.type/checkbox')
        if f[':answer-field/type']==':answer-field.type/checkbox':
            assert len(f[':answer-field/choices'])==2 and {a[':answer/value'] for a in f[':answer-field/choices']}=={'false','true'}
        else:assert len(f[':answer-field/choices'])==5
        for a in f[':answer-field/choices']:check_math(a[':answer/value'])
        if ':answer-field/correct' in f:assert sum(a[':answer/id']==f[':answer-field/correct'][1] for a in f[':answer-field/choices'])==1


def source_fidelity():
    counts={'questions':0,'prompts':0,'solutions':0,'fields':0,'options':0,'distractors':0,'correct_designations':0,'key_presence':0,'fieldless_sources':0,'missing_correct_fields':0}
    cases=[];records=[]
    for t,src in g.QUESTIONS.items():
        level=g.SPECS[t]['level'];p={'scale':1,'shift':0,'vertical':0};r=g.generate(level,template=t,parameters=p,profile='observed');audit(r);q=r['question']
        cases.append({'source_id':t,'template':t,'parameters':p,'bank_profile':'observed','level':level});records.append(r)
        counts['questions']+=1
        for key,counter in ((':question/problem','prompts'),(':question/worked-solution','solutions')):assert q[key]==src[key],(t,key);counts[counter]+=1
        assert q[':question/difficulty']==src[':question/difficulty'][':db/ident']
        for key in (':question/difficulty',':question/answer-fields',':question/worked-solution'):assert (key in q)==(key in src),(t,key);counts['key_presence']+=1
        fs=src.get(':question/answer-fields',[]);fg=q.get(':question/answer-fields',[]);assert len(fs)==len(fg)
        if not fs:counts['fieldless_sources']+=1
        for s,f in zip(fs,fg):
            assert f[':answer-field/key']==s[':answer-field/key'];assert f[':answer-field/type']==s[':answer-field/type'][':db/ident']
            counts['fields']+=1
            assert sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in s[':answer-field/choices'])
            counts['options']+=len(s[':answer-field/choices'])
            assert (':answer-field/correct' in f)==(':answer-field/correct' in s);counts['key_presence']+=1
            if ':answer-field/correct' in s:
                correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct[':answer/value']==s[':answer-field/correct'][':answer/value'];counts['correct_designations']+=1;counts['distractors']+=len(s[':answer-field/choices'])-1
            else:counts['missing_correct_fields']+=1
    (ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');return counts,records


def native_item(r,label):
    checks=[]
    for i,f in enumerate(r['question'][':question/answer-fields']):
        correct=f[':answer-field/correct'][1]
        for a in f[':answer-field/choices']:
            submit={'submitted_answer_id':a[':answer/id']}
            checks.append({'field_index':i,**submit,'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Actual source-shaped field grading'})
    return {'label':label,'record':r,'checks':checks}


def main():
    counts,originals=source_fidelity();review=[];native=[];seen={k:set() for k in ('easy','moderate','hard')};content=set();task=set()
    # Source-shaped family changed-coordinate coverage, defaults reach all banks.
    for t,l in g.SPECS.items():
        level=l['level']
        for seed,p in enumerate(({'scale':1,'shift':-3,'vertical':-1},{'scale':2,'shift':2,'vertical':1})):
            r=g.generate(level,seed,template=t,parameters=p);audit(r);review.append(r);native.append(native_item(r,t+'/'+str(seed)));content.add(r['generation']['content_fingerprint']);task.add(r['generation']['mathematical_fingerprint'])
            other=g.generate(level,seed+13,template=t,parameters=p);assert r['question'][':question/id']==other['question'][':question/id']
    for t in ('q-78133','q-102115'):
        r=g.generate('hard',8,template=t,parameters={'scale':'1/2','shift':-1,'vertical':1});audit(r);review.append(r);native.append(native_item(r,'hard/'+t));task.add(r['generation']['mathematical_fingerprint'])
    # Default selection without costly redundant graph renders.
    for level in seen:
        for seed in range(30):
            r=g.generate(level,seed);audit(r);seen[level].add(r['generation']['source_id']);content.add(r['generation']['content_fingerprint']);task.add(r['generation']['mathematical_fingerprint'])
    assert seen['easy']==set(k for k,v in g.SPECS.items() if v['level']=='easy');assert seen['moderate']==set(k for k,v in g.SPECS.items() if v['level']=='moderate');assert seen['hard']=={'q-78133','q-102115'}
    for level,p in [('easy',{'scale':'1/2','shift':0,'vertical':0}),('hard',{'scale':1,'shift':0,'vertical':0}),('moderate',{'scale':1,'shift':5,'vertical':0})]:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError('Explicit workload guard bypass')
    # Attribute identity, omission and graph-condition mutation regressions.
    sample=copy.deepcopy(review[-1]);path=next(iter(sample['generation']['graphs']));sample['generation']['graphs'][path]['values'].clear()
    try:audit(sample)
    except AssertionError:pass
    else:raise AssertionError('Missing filled point not detected')
    sample=copy.deepcopy(review[-1]);sample['question'][':question/worked-solution']+='\x0c'
    try:audit(sample)
    except AssertionError:pass
    else:raise AssertionError('C0 mutation not detected')
    sample=copy.deepcopy(review[-1]);sample['question'][':question/worked-solution']=sample['question'][':question/worked-solution'].replace('is not continuous','is continuous',1)
    try:audit(sample)
    except AssertionError:pass
    else:raise AssertionError('Final prose/local claim mutation not detected')
    # Direct singular-expression audit: cancelled denominator preserves hole.
    hole={'segments':[{'lo':'-1','hi':'1','expr':'1','raw_excluded':['0']}],'values':{},'holes':['0'],'poles':[],'bounds':['-1','1','-2','2']}
    assert not limit_status(hole,0)['continuous'] and limit_status(hole,0)['limit_exists']
    cancelled={'segments':[{'lo':'-1','hi':'1','expr':'x/x'}],'values':{},'holes':[],'poles':[],'bounds':['-1','1','-2','2']}
    cancelled=g.transformed(cancelled,{'scale':1,'shift':0,'vertical':0})
    assert cancelled['segments'][0]['raw_excluded']==['0']
    assert not limit_status(cancelled,0)['continuous'] and limit_status(cancelled,0)['limit_exists']
    (ROOT/'review.json').write_text(json.dumps(review,indent=2)+'\n')
    lines=['# Review: original evidence and changed-coordinate variants','', 'Original assets below are shown at source dimensions; generated curves are explicit schematic realizations of extracted topology.']
    for original in originals:
        t=original['generation']['source_id'];lines+=['','## Original '+t,'',g.markdown(original),'','### Generated variants']
        for r in review:
            if r['generation']['source_id']==t and r['generation']['requested_level']!='hard':lines+=['',g.markdown(r)]
    lines+=['','## Authored hard: half-unit coordinates with jump and hole','']
    for r in review:
        if r['generation']['requested_level']=='hard':lines+=[g.markdown(r),'']
    (ROOT/'review.md').write_text('\n'.join(lines)+'\n')
    subprocess.run([sys.executable,str(ROOT/'concurrency-check.py')],check=True)
    # Raw single-field supported observed banks also receive actual native checks.
    for r in originals:
        fs=r['question'].get(':question/answer-fields',[])
        if len(fs)==1 and ':answer-field/correct' in fs[0]:native.append(native_item(r,'observed/'+r['generation']['source_id']))
    # Reopen classification against current source: five migrated checkbox banks.
    current_counts={'questions':0,'prompts':0,'solutions':0,'fields':0,'options':0,'correct_designations':0}
    def contract(q):
        result={k:q[k] for k in (':question/problem',':question/worked-solution')}
        result['difficulty']=q[':question/difficulty'] if isinstance(q[':question/difficulty'],str) else q[':question/difficulty'][':db/ident']
        fields=[]
        for f in q.get(':question/answer-fields',[]):
            correct=f.get(':answer-field/correct')
            if isinstance(correct,list):correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct[1])
            elif correct is not None:correct=correct[':answer/value']
            fields.append({'key':f[':answer-field/key'],'type':f[':answer-field/type'] if isinstance(f[':answer-field/type'],str) else f[':answer-field/type'][':db/ident'],'choices':sorted([(a[':answer/type'] if isinstance(a[':answer/type'],str) else a[':answer/type'][':db/ident'],a[':answer/value']) for a in f[':answer-field/choices']]),'correct':correct})
        result['fields']=sorted(fields,key=lambda f:json.dumps(f,sort_keys=True))
        return result
    for t,src in g.CURRENT_QUESTIONS.items():
        r=g.generate(g.SPECS[t]['level'],template=t,parameters={'scale':1,'shift':0,'vertical':0},profile='current')
        audit(r);assert contract(r['question'])==contract(src),(t,'current contract replay')
        current_counts['questions']+=1;current_counts['prompts']+=1;current_counts['solutions']+=1
        fs=r['question'].get(':question/answer-fields',[])
        current_counts['fields']+=len(fs);current_counts['options']+=sum(len(f[':answer-field/choices']) for f in fs);current_counts['correct_designations']+=sum(':answer-field/correct' in f for f in fs)
        if r['generation']['eligible_for_learning']:native.append(native_item(r,'current/'+t))
    (ROOT/'current-replay.json').write_text(json.dumps({'passed':True,'basis':g.CURRENT_SOURCE['basis'],'matched':current_counts,'checkbox_source_questions':5,'historical_source_replay_retained':True,'source_exclusions':['q-48081 duplicate key/missing correct designation','q-48082 contradictory solution plot'],'current_normal_contract':'Easy single radio image bank; moderate/hard three Roman-key checkbox fields; boolean owned choices true/false'},indent=2)+'\n')
    (ROOT/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
    subprocess.run([str(ROOT/'check-engine'),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],check=True)
    engine=json.loads((ROOT/'native-report.json').read_text())
    report={'status':'passed','source_fidelity':counts,'source_scope':'9 practice originals; canonical separate; basis1356','normal_records_checked':len(content),'semantic_tasks':len(task),'default_family_coverage':{k:sorted(v) for k,v in seen.items()},'review_records':len(review),'current_source_fidelity':current_counts,'native':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':engine['documented_unresolved_checks'],'blanks':'not applicable; no observed blank fields'},'source_anomalies':['q-48081 duplicate legacy radio field, first missing correct ref; raw preserved, normal one widget and add missing shown-below solution plot' ,'Historical q-102106/q-78133 fieldless; current replay and normal output use three complete checkbox fields','Historical q-102115 unlabeled; current migrated source and normal output label I/II/III','q-78132 source omitted at: normal minimal prose repair','q-48082 solution raster reverses open/filled markers at unqueried x=2; raw preserved, normal uses the answer-option function' ], 'raster_qa':'Actual generated PNG open/filled centers and rings checked against independent branch/domain/value mathematics; pixel transform from recorded axes', 'plot_fidelity':'32 original assets inspected at original resolution; raw assets exact; changed geometry preserves extracted local topology, not unknown source algebraic formulas','dependencies':review[0]['generation']['dependencies'],'concurrency':json.loads((ROOT/'concurrency-report.json').read_text()),'database_writes':0}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
