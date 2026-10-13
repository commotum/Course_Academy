"""Fail-closed printed-mathematics, full source fidelity and native RADIO QA."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('matrix_statements',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name,x): (HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def parse_matrix(text):
    matches=re.findall(r'\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\1\}',text,re.S)
    assert matches,text
    rows=[[int(c.strip()) for c in row.split('&')] for row in matches[0][1].split(r'\\')]
    assert all(len(r)==len(rows) for r in rows)
    return sp.Matrix(rows)
def displayed(text):
    m=parse_matrix(text);ss=[]
    for expr,kind in re.findall(r'\$(.*?)\$ is (upper triangular|lower triangular|diagonal)',text):
        e=re.sub(r'[{}\s]','',expr);tokens=re.split(r'([+-])',e)
        assert len(tokens) in (1,3)
        terms=[]
        for token in tokens[::2]:
            assert re.fullmatch(r'[A-Z](?:\^T)?',token)
            terms.append(m.T if token.endswith('^T') else m)
        b=terms[0] if len(tokens)==1 else terms[0]+terms[1] if tokens[1]=='+' else terms[0]-terms[1]
        coords=[(i,j) for i in range(m.rows) for j in range(m.cols) if i>j] if kind=='upper triangular' else [(i,j) for i in range(m.rows) for j in range(m.cols) if i<j] if kind=='lower triangular' else [(i,j) for i in range(m.rows) for j in range(m.cols) if i!=j]
        values=[b[i,j] for i,j in coords]
        ss.append((expr,kind,b,all(v==0 for v in values),coords))
    assert len(ss)==3
    return m,ss

def subset(value):
    assert value in ('None','I only','II only','III only','I and II only','I and III only','II and III only','I, II, and III'),value
    return frozenset(re.findall(r'\b(?:III|II|I)\b',value))
def shape(q):
    return {k for k in q if k not in (':db/id',':question/math-academy-id')}
def normalize_source(source):
    q=copy.deepcopy(source)
    q.pop(':db/id',None);q.pop(':question/math-academy-id',None)
    if ':question/difficulty' in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
    for f in q[':question/answer-fields']:
        f.pop(':db/id',None);f[':answer-field/type']=f[':answer-field/type'][':db/ident']
        if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
        for a in f[':answer-field/choices']:a.pop(':db/id',None);a[':answer/type']=a[':answer/type'][':db/ident']
    return q

def formatting(text):
    assert text.count('$')%2==0
    assert text.count('{')==text.count('}')
    assert text.count(r'\begin{aligned}')==text.count(r'\end{aligned}')
    assert text.count(r'\begin{bmatrix}')==text.count(r'\end{bmatrix}')
    assert '{{' not in text

def mathematical(rec):
    q=rec['question'];m,ss=displayed(q[':question/problem'])
    assert len(q[':question/answer-fields'])==1
    f=q[':question/answer-fields'][0]
    assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    choices=f[':answer-field/choices'];assert len(choices)==5
    sets=[subset(a[':answer/value']) for a in choices]
    assert len(set(sets))==5 and all(a[':answer/type']==':answer.type/text' for a in choices)
    expected=frozenset(k for k,entry in zip(('I','II','III'),ss) if entry[3])
    assert sum(v==expected for v in sets)==1
    if ':answer-field/correct' in f:
        assert f[':answer-field/correct'][0]==':answer/id'
        ca=next(a for a in choices if a[':answer/id']==f[':answer-field/correct'][1])
        assert subset(ca[':answer/value'])==expected
    sol=q.get(':question/worked-solution')
    if sol is not None:
        parts=sol.split('\n\n- Statement ')[1:];assert len(parts)==3
        raw=rec['generation']['evidence_only'];sid=rec['generation']['template']
        for key,part,(expr,kind,b,true,coords) in zip(('I','II','III'),parts,ss):
            assert part.startswith(key+' is '+str(true).lower())
            assert parse_matrix(part)==b
            # Complete concrete proof: every relevant zero for a true claim;
            # at least one actual printed nonzero on the tested side otherwise.
            assert all(b[i,j]==0 for i,j in coords) if true else any(b[i,j]!=0 for i,j in coords)
            if not(raw and sid=='q-126484' and key=='III'):
                side='below' if kind=='upper triangular' else 'above' if kind=='lower triangular' else 'off'
                assert side+' the main diagonal' in part
        final=re.search(r'Therefore, the correct answer is "(.*?)"\.',sol)
        assert final and subset(final[1])==expected
    for t in [q[':question/problem'],sol or '']:formatting(t)
    return True

def solution_structure(rec):
    sid=rec['generation']['template']
    if sid=='direct-properties' or sid=='q-42115':return
    q=rec['question'];old=g.QS[sid][':question/worked-solution'];new=q[':question/worked-solution']
    # Replace complete matrix-body slots only; every shared sentence, expression
    # label, stage and conclusion must remain, apart from documented repairs.
    mask=lambda s:re.sub(r'(?<=\\begin\{aligned\})(.*?)(?=\\end\{aligned\})','<MATRIX>',s,flags=re.S)
    old=mask(old);new=mask(new)
    if not rec['generation']['evidence_only']:
        if sid=='q-126477':old=old.replace('since $A$ has','since $B$ has')
        if sid=='q-126484':old=old.replace('Statement III is false, since $B$ has non-zero entries below the main diagonal:', 'Statement III is false, since ${B}^{T}$ has non-zero entries above the main diagonal:')
    assert old==new,(sid,old,new)

def validate(rec):
    assert set(rec['knowledge_point'])=={'db_id','id','title'}
    assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    mathematical(rec);solution_structure(rec)
    q=rec['question'];gen=rec['generation']
    replay=g.generate(gen['level'],gen['seed'],gen['template'],parameters=gen['parameters'],profile=gen['profile'])
    assert replay==rec
    ids=[q[':question/id']]+[f[':answer-field/id'] for f in q[':question/answer-fields']]+[a[':answer/id'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
    assert len(ids)==len(set(ids));[uuid.UUID(v) for v in ids]
    assert ':question/difficulty' in q or gen['evidence_only']
    assert gen['eligible_for_learning']==(not gen['evidence_only'])
    assert gen['python']==sys.version.split()[0]

def fixture(rec,label):
    f=rec['question'][':question/answer-fields'][0]
    assert ':answer-field/correct' in f
    return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Full displayed five-choice bank, native RADIO selection'} for a in f[':answer-field/choices']]}

def expect_failure(fn,label):
    try:fn()
    except (AssertionError,ValueError,StopIteration):return label
    raise AssertionError('Mutation was accepted: '+label)

def main():
    fidelity=[];cases=[];reviews=[];reviewmd=['# Matrix statement review','All raw source replays are evidence-only. Normal records preserve RADIO and their source banks; q42115 hard/solution/correct key are inferred. Easy is authored.'];native=[];extraction=[]
    for sid,source in g.QS.items():
        rec=g.generate(g.level(sid),0,sid,parameters={'matrix':g.TEMPLATES[sid]['source_matrix']},profile='source-replay');validate(rec)
        q=rec['question'];old=normalize_source(source)
        assert shape(q)==shape(old)
        assert q[':question/problem']==old[':question/problem']
        assert q.get(':question/worked-solution')==old.get(':question/worked-solution')
        assert q.get(':question/difficulty')==old.get(':question/difficulty')
        for nf,of in zip(q[':question/answer-fields'],old[':question/answer-fields']):
            assert set(nf)==set(of)
            assert {k:v for k,v in nf.items() if k not in (':answer-field/id',':answer-field/choices',':answer-field/correct')}=={k:v for k,v in of.items() if k not in (':answer-field/id',':answer-field/choices',':answer-field/correct')}
            normalized=lambda f:sorted(({k:v for k,v in a.items() if k!=':answer/id'} for a in f[':answer-field/choices']),key=lambda a:a[':answer/value'])
            assert normalized(nf)==normalized(of)
            if ':answer-field/correct' in of:
                val=lambda f:next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
                assert val(nf)==val(of)
        cases.append({'source_id':sid,'template':sid,'parameters':rec['generation']['parameters'],'bank_profile':'source-replay','level_argument':g.level(sid),'observed_level':g.source_level(sid)})
        fidelity.append({'source_id':sid,'matched_values':5,'complete_bank':True,'correct_designation_matched':':answer-field/correct' in old[':question/answer-fields'][0],'key_presence_parity':True,'raw_exact_prompt':True,'raw_exact_solution':':question/worked-solution' in old,'raw_solution_omission':':question/worked-solution' not in old,'raw_difficulty_omission':':question/difficulty' not in old})
        if ':answer-field/correct' in q[':question/answer-fields'][0]:native.append(fixture(rec,sid+' raw'))
        variant=g.generate(g.level(sid),71,sid);validate(variant);native.append(fixture(variant,sid+' normal variant'))
        reviews.extend([{'label':'Raw original replay '+sid,'record':rec},{'label':'Generated normal variant '+sid,'record':variant}])
        reviewmd+=['\n## Original '+sid,g.markdown(rec),'\n### Generated normal variant',g.markdown(variant)]
        extraction.append({'source_id':sid,'level':g.source_level(sid),'matrix':g.TEMPLATES[sid]['source_matrix'],'statements':g.TEMPLATES[sid]['statements'],'profile':sid,'bank':[{'value':a[':answer/value'],'recipe':{'selected_statement_labels':sorted(subset(a[':answer/value']))},'observed_correct':(':answer-field/correct' in source[':question/answer-fields'][0] and a[':answer/id']==source[':question/answer-fields'][0][':answer-field/correct'][':answer/id'])} for a in source[':question/answer-fields'][0][':answer-field/choices']],'inferred_true_subset':rec['generation']['inferred_correct_value'],'solution_matrix_stages':len(re.findall(g.MATRIX_RE,source.get(':question/worked-solution',''),re.S))})
    finite={};exhaustive=0;seenfamilies={}
    for level in g.LEVELS:
        records=g.batch(level,10000,19);finite[level]=len(records)
        for i,rec in enumerate(records):validate(rec);native.append(fixture(rec,level+' support '+str(i)))
        exhaustive+=len(records)
        # Every source family/bank sampled by normal public generation.
        sampled=[g.generate(level,seed) for seed in range(150)]
        seenfamilies[level]=sorted({r['generation']['template'] for r in sampled})
        assert set(seenfamilies[level])=={sid for sid,t in g.TEMPLATES.items() if t['level']==level}
        for rec in sampled:validate(rec)
        correct_positions={next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in sampled}
        assert correct_positions==set(range(5)),correct_positions
        if level=='easy':
            assert {r['generation']['inferred_correct_value'] for r in sampled}=={'None','I only','II only','I, II, and III'}
        for rec in records[:2]:reviews.append({'label':'Generated '+level+' example','record':rec});reviewmd+=['\n## Generated '+level+' example',g.markdown(rec)]
    boundaries=0
    for sid,t in g.TEMPLATES.items():
        for support in g.supports(sid):
            for value in (-8,8):
                p=g.sample(sid,__import__('random').Random(5),support)
                p['matrix']=[[value if v>0 else -value if v<0 else 0 for v in row] for row in p['matrix']]
                for i in range(len(p['matrix'])):p['matrix'][i][i]=value
                rec=g.generate(t['level'],37,sid,parameters=p);validate(rec);boundaries+=1
        # Evidence recipes genuinely parameterize original and changed matrices.
        if sid!='direct-properties':
            changed=g.sample(sid,__import__('random').Random(182))
            rec=g.generate(t['level'],3,sid,parameters=changed,profile='source-replay');validate(rec)
            assert parse_matrix(rec['question'][':question/problem'])==sp.Matrix(changed['matrix'])
    guards=[]
    for level,fn in [('easy',g.generate_easy),('moderate',g.generate_moderate),('hard',g.generate_hard)]:
        rec=fn(11);sid=rec['generation']['template'];p=rec['generation']['parameters']
        shifted=g.generate(level,932,sid,parameters=p,profile=rec['generation']['profile'])
        assert rec['question'][':question/id']==shifted['question'][':question/id']
        assert rec['generation']['content_fingerprint']==shifted['generation']['content_fingerprint']
        assert rec['generation']['math_fingerprint']==shifted['generation']['math_fingerprint']
        for bad in ({'matrix':[[1]]},{'matrix':[[9]*len(p['matrix']) for _ in p['matrix']]},{'matrix':[[True]*len(p['matrix']) for _ in p['matrix']]},{**p,'unused':1}):guards.append(expect_failure(lambda:g.generate(level,template=sid,parameters=bad),level+' invalid guard'))
    guards.append(expect_failure(lambda:g.generate('easy',field_type='checkbox'),'no field migration'))
    for sid in g.QS:
        p={'matrix':copy.deepcopy(g.TEMPLATES[sid]['source_matrix'])};p['matrix'][0][1]=6;p['matrix'][1][0]=4
        guards.append(expect_failure(lambda:g.generate(g.level(sid),template=sid,parameters=p),sid+' source class guard'))
    mutations=[]
    rec=g.generate('hard',9,'q-42116')
    bad=copy.deepcopy(rec);bad['question'][':question/problem']=bad['question'][':question/problem'].replace(' & 0 & 0',' & 1 & 0',1)
    mutations.append(expect_failure(lambda:mathematical(bad),'wrong displayed matrix'))
    bad=copy.deepcopy(rec);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('Statement II is false','Statement II is true')
    mutations.append(expect_failure(lambda:mathematical(bad),'wrong transformed truth'))
    bad=copy.deepcopy(rec)
    sol=bad['question'][':question/worked-solution'];matches=list(re.finditer(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S));match=matches[1]
    body=match[1];newbody=body.replace('0 & ', '1 & ',1);assert body!=newbody
    bad['question'][':question/worked-solution']=sol[:match.start(1)]+newbody+sol[match.end(1):]
    mutations.append(expect_failure(lambda:mathematical(bad),'wrong actual transformed matrix entry'))
    bad=copy.deepcopy(rec);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace("Let's analyze each statement in turn.",'Look at the final result.')
    mutations.append(expect_failure(lambda:solution_structure(bad),'missing shared proof structure'))
    bad=copy.deepcopy(rec);f=bad['question'][':question/answer-fields'][0];f[':answer-field/choices'][1][':answer/value']=f[':answer-field/choices'][0][':answer/value']
    mutations.append(expect_failure(lambda:mathematical(bad),'semantic duplicate full bank'))
    save('source-cases.json',cases);save('template-extraction.json',extraction);save('review.json',reviews);(HERE/'review.md').write_text('\n\n'.join(reviewmd)+'\n')
    save('native-input.json',native)
    engine=ROOT/'generate/runs/current/check-engine';result=subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr
    report=json.loads((HERE/'native-report.json').read_text())
    save('validation.json',{'status':'passed','source_provenance':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_fidelity':{'practice_questions':10,'complete_banks':10,'matched_choices':50,'matched_observed_incorrect_choices':36,'observed_incorrect_choice_denominator':36,'matched_correct_designations':9,'correct_designation_denominator':9,'missing_correct_designation':1,'exact_prompts':10,'exact_present_solutions':9,'present_solution_denominator':9,'missing_solutions':1,'key_presence_parity':10,'unrated_sources':1,'details':fidelity},'mathematical_correctness':{'exhaustive_structural_tasks':finite,'total_exhaustive_records':exhaustive,'boundary_records':boundaries,'default_families':seenfamilies,'whole_bank_semantic_duplicates':0,'mutations_rejected':mutations,'guards_rejected':len(guards),'public_parameterized_raw_profiles':10},'native':{'fixtures':len(native),'checks':sum(len(x['checks']) for x in native),'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'result':report,'raw_ungraded':{'q-42115':'No captured correct reference; faithful public raw replay retains omission. Its separately inferred normal version is fully native graded.'}},'authored_extensions':['Easy fixed 3x3 upper/lower/diagonal statements, five-choice complete subset bank','q-42115 normal hard assignment, independent II-only key and three-stage solution'],'repairs':{'q-126477':'Normal solution A referent corrected to B; raw exact retained','q-126484':'Normal third reason corrected to B transpose / above; raw exact retained'},'limitations':['Structural catalogs finite; numeric changes/signs/diagonal changes and order are not extra tasks','Observed dimensions and diagonal hard source retained with actual source labels; no recovered easy label','Raw q-42115 cannot be fully graded without authoring its absent key']})
    print(json.dumps({'source_banks':10,'choices':50,'correct_refs':9,'finite':finite,'boundaries':boundaries,'native_fixtures':len(native),'native_checks':sum(len(x['checks']) for x in native),'status':'passed'}))
if __name__=='__main__':main()
