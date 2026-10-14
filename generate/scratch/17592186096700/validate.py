"""Independent displayed-statement/PNG/prose checks; native grading kept separate."""
import concurrent.futures, hashlib, importlib.util, itertools, json, re, subprocess, sys
from fractions import Fraction
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ROOT=HERE.parents[2]

def check(condition,message):
    if not condition:raise AssertionError(message)
def write(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def latex_rat(s):
    s=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'\1/\2',s)
    return sp.Rational(s or '1')
def parse_equation(text):
    match=re.fullmatch(r'([a-e])=([+-]?(?:\d+(?:/\d+)?)?)([a-e])',re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'\1/\2',text.replace(' ','')))
    check(match is not None,'Unparseable displayed relation '+text)
    a,k,b=match.groups();return a,sp.Rational('-1' if k=='-' else '1' if k in ('','+') else k),b

def math_check(r,raster):
    q=r['question'];gen=r['generation'];fields=q[':question/answer-fields']
    st=[parse_equation(x) for x in re.findall(r'^- \*\*[IV]+\.\*\* \$(.*?)\$',q[':question/problem'],re.M)]
    check(len(st)==3,'Exactly three displayed statements')
    # Displacements are re-read from actual PNG endpoints snapped to its square grid.
    vectors={label:[sp.Integer(a['recovered_tip_grid'][j]-a['recovered_tail_grid'][j]) for j in (0,1)] for label,a in raster['arrows'].items()}
    true=frozenset(i for i,(a,k,b) in enumerate(st) if all(vectors[a][j]==k*vectors[b][j] for j in (0,1)))
    check(g.parse_subset(gen['correct_inference'])==true,'Inference versus displayed geometry')
    check(raster['equal_physical_scale'],'Equal physical grid scale')
    if gen['plot'].get('labels'):
        check(set(raster['labels'])==set('abcde'),'All five actual PNG labels checked')
        check(all(v['blue_pixels_within_bbox_and_3px_margin']==0 and v['black_text_pixels']>=5 and v['association_distance_grid']<=.9 for v in raster['labels'].values()),'Actual PNG text clearance and close association')
    check(set(r['knowledge_point'])=={'db_id','id','title'},'Knowledge point outer shape')
    check(len(fields)==3 and [f[':answer-field/key'] for f in fields]==list(g.ROMAN),'Three source statement keys')
    for i,f in enumerate(fields):
        check(f[':answer-field/type']==':answer-field.type/checkbox','Current checkbox type')
        bank={a[':answer/id']:a for a in f[':answer-field/choices']}
        check(sorted((a[':answer/type'],a[':answer/value']) for a in bank.values())==[(':answer.type/text','false'),(':answer.type/text','true')],'Complete boolean bank')
        ref=f[':answer-field/correct'];check(ref[0]==':answer/id' and ref[1] in bank,'Field-owned correct answer')
        check(bank[ref[1]][':answer/value']==('true' if i in true else 'false'),'Correct selection versus actual PNG')
    if gen['evidence_only']:
        check(not gen['eligible_for_learning'] and ':question/difficulty' not in q,'Source replay stays unrated')
        values=re.findall(r'([a-e])=\((-?\d+),(-?\d+)\)',q[':question/worked-solution']);check(len(values)==4,'Four source computed vectors')
        for label,x,y in values:check(vectors[label]==[int(x),int(y)],'Source solution versus actual PNG')
    else:
        check(gen['eligible_for_learning'],'Completed instances eligible')
        sol=q[':question/worked-solution']
        bullets=re.findall(r'^- Statement (I|II|III) is (true|false)\.',sol,re.M)
        check(bullets==[(g.ROMAN[i],'true' if i in true else 'false') for i in range(3)],'Worked statements/conclusion reflect rendered prompt')
        for a,value,b in re.findall(r'The magnitude of \$([a-e])\$ is \$(.*?)\$ times the magnitude of \$([a-e])\$',sol,flags=re.I):
            actual=sp.sqrt(sum(x*x for x in vectors[a]))/sp.sqrt(sum(x*x for x in vectors[b]));check(sp.simplify(actual-latex_rat(value))==0,'Displayed magnitude ratio')
        for a,b,wording in re.findall(r'[Vv]ectors \$([a-e])\$ and \$([a-e])\$ (?:are parallel and )?have (the same direction|opposite directions)',sol):
            dot=sum(vectors[a][j]*vectors[b][j] for j in (0,1));check((dot>0)==(wording=='the same direction'),'Displayed direction prose')
        for i,bullet in enumerate(sol.split('\n\n')[0].split('\n')):
            final=re.findall(r'\$([^$]*(?:=|\\neq)[^$]*)\$',bullet)[-1]
            expr=final.replace(r'\neq','=');check(parse_equation(expr)==st[i],'Solution conclusion uses actual statement slots')
        if len(true)==1:expected=f'Therefore, only statement {g.ROMAN[next(iter(true))]} is true.'
        elif len(true)==2:expected='Therefore, only statements '+' and '.join(g.ROMAN[i] for i in sorted(true))+' are true.'
        elif len(true)==3:expected='Therefore, all three statements are true.'
        else:expected='Therefore, none of the statements are true.'
        check(sol.endswith(expected),'Final true-subset prose')
    text=q[':question/problem']+q.get(':question/worked-solution','')
    check(text.count('$')%2==0 and text.count('{')==text.count('}'),'Math delimiter/group balance')
    ids=[q[':question/id']]
    import uuid
    for f in fields:
        check(f[':answer-field/id']==g.owned(q[':question/id'],f[':answer-field/key']),'Field UUID ownership')
        check(all(a[':answer/id']==g.owned(f[':answer-field/id'],a[':answer/value']) for a in f[':answer-field/choices']),'Answer UUID ownership')
        ids+=[f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]
    for x in ids:uuid.UUID(x)
    check(len(set(ids))==len(ids),'Unique owned IDs')
    return {'true_subset':g.subset_text(true),'vectors_read_from_png':{k:[str(x) for x in v] for k,v in vectors.items()}}

def ordered(x):
    if isinstance(x,dict):return {str(k):ordered(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return sorted([ordered(v) for v in x],key=lambda z:json.dumps(z,sort_keys=True))
    return str(x) if not isinstance(x,(str,int,float,bool)) and x is not None else x

def engine_item(r):
    checks=[]
    for i,f in enumerate(r['question'][':question/answer-fields']):
        correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        for a in f[':answer-field/choices']:
            checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==correct else 'rejected','purpose':'Actual field-owned choice ID for checked and unchecked submissions'})
    return {'label':r['question'][':question/id'],'record':r,'checks':checks}

def validate_records(records,path):
    path.mkdir(parents=True,exist_ok=True);original=json.loads((HERE/'original-geometry.json').read_text());request=[]
    for r in records:
        gen=r['generation'];q=r['question'];level=q.get(':question/difficulty',':question.difficulty/moderate').split('/')[-1]
        replay=g.generate(level,gen['seed'],template=gen['template'],parameters=gen['parameters'],profile=gen['bank_profile'])
        check(ordered(q)==ordered(replay['question']),'Deterministic public replay')
        p=g.normalize_parameters(level,gen['template'],gen['parameters'],gen['evidence_only'])
        check(gen['mathematical_fingerprint']==g.task_key(gen['template'],p),'Recomputed mathematical signature')
        plot=gen['plot'];asset=plot.get('source_asset') or q[':question/problem'].split('![](')[1].split(')')[0]
        if plot.get('source_asset'):
            case=g.match_original(gen['template'],p);transform=original[case['source_id']]['transform']
        else:transform=plot['transform']
        check(g.file_hash(asset)==plot['png_sha256'],'Plot hash')
        request.append({'id':q[':question/id'],'path':asset,'geometry':gen['geometry'],'transform':transform,'labels':plot.get('labels')})
    (path/'raster-input.json').write_text(json.dumps({'audit_existing':True,'records':request,'output':str(path/'raster-report.json')}))
    subprocess.run([g.RUNTIME,str(HERE/'render_plot.py'),str(path/'raster-input.json')],check=True,capture_output=True)
    raster=json.loads((path/'raster-report.json').read_text())
    (path/'math-report.json').write_text(json.dumps([math_check(r,raster[r['question'][':question/id']]) for r in records],indent=2))
    (path/'native-input.json').write_text(json.dumps([engine_item(r) for r in records],indent=2))
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True,capture_output=True)
    native=json.loads((path/'native-report.json').read_text());check(native['documented_unresolved_checks']==0,'Native grader unresolved')
    return native

def main():
    source=json.loads((HERE/'source.json').read_text())['record'];byid={q[':question/math-academy-id']:q for q in source[':knowledge-point/questions']};records=[];fidelity=[]
    for case in g.SOURCE_CASES:
        r=g.generate('moderate',0,case['template'],parameters=case['parameters'],profile='source-a' if case['template']==g.TEMPLATES[0] else 'source-b')
        q=byid[case['source_id']];new=r['question'];check(':question/difficulty' not in q and ':question/difficulty' not in new,'Unrated status preserved')
        for key in (':question/problem',':question/worked-solution'):check(new[key]==q[key],'Exact source text '+key)
        oldfields={f[':answer-field/key']:f for f in q[':question/answer-fields']}
        check(set(oldfields)==set(g.ROMAN),'Current source field layout')
        for f in new[':question/answer-fields']:
            old=oldfields[f[':answer-field/key']]
            check(f[':answer-field/type']==old[':answer-field/type'][':db/ident'],'Source field type')
            check(sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in old[':answer-field/choices']),'Complete source bank')
            correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);check(correct==old[':answer-field/correct'][':answer/value'],'Source correct designation')
        records.append(r);fidelity.append({'source_id':case['source_id'],'exact_prompt':True,'exact_solution':True,'complete_banks_matched':3,'values_matched':6,'correct_designations_matched':3,'unrated_status_preserved':True})
    for level in ('easy','moderate','hard'):
        for seed in range(6):records.append(g.generate(level,seed))
        for template in (g.TEMPLATES[:1] if level=='easy' else g.TEMPLATES):
            if level=='easy':params=dict(u=[-2,2],v=[0,-2],k='1',s=1,t=-1)
            elif level=='moderate':params=dict(u=[-3,2],v=[5,2],k='2',s=-1,t=-1)
            else:params=dict(u=[-4,2],v=[5,-2],k='3/2',s=-1,t=-1)
            records.append(g.generate(level,17,template,parameters=params))
    for r in records:
        gen=r['generation'];level=r['question'].get(':question/difficulty',':question.difficulty/moderate').split('/')[-1]
        other=g.generate(level,999,gen['template'],parameters=gen['parameters'],profile=gen['bank_profile']);check(ordered(other['question'])==ordered(r['question']),'Seed-independent authored identity')
        p=g.normalize_parameters(level,gen['template'],gen['parameters'],gen['evidence_only']);key=g.task_key(gen['template'],p)
        p['u'],p['v']=[-z for z in p['u']],[-z for z in p['v']];check(g.task_key(gen['template'],p)==key,'Rotation cannot create a task')
    for level,k in [('easy','2'),('moderate','3/2'),('hard','2')]:
        try:g.generate(level,parameters=dict(u=[2,1],v=[1,2],k=k,s=-1,t=-1))
        except ValueError:pass
        else:raise AssertionError('Explicit level boundary bypass')
    native=validate_records(records,HERE/'reference/current-validation')
    write('source-replay.json',{'status':'passed','basis':g.SOURCE['basis'],'questions':fidelity,'complete_banks':'6/6','values':'12/12','correct_designations':'6/6','solutions':'2/2','source_distractors':'6/6'})
    write('review.json',records);(HERE/'review.md').write_text('\n\n'.join('## '+r['generation']['template']+' — '+r['question'].get(':question/difficulty','source unrated')+'\n'+g.markdown(r) for r in records)+'\n')
    files=[HERE.with_suffix('.py'),HERE/'validate.py',HERE/'render_plot.py',HERE/'source.json',HERE/'dependency-lock.json',ROOT/'generate/runs/current/check-engine']
    write('validation.json',{'status':'passed','version':g.VERSION,'source':g.SOURCE,'source_fidelity':{'complete_banks':'6/6','values':'12/12','correct_designations':'6/6','solutions':'2/2'},'independent_png_math_records':len(records),'native_checks':native['accepted_checks']+native['rejected_checks'],'native_unresolved':0,'sha256':{str(p.relative_to(ROOT)):g.file_hash(p) for p in files},'authored_levels':['easy','moderate','hard'],'exceptions':[]})
    print('Passed current source replay, PNG mathematics and native checkbox grading:',len(records),'records',flush=True)
if __name__=='__main__':main()

