"""Reproducible author checks; run with the pinned job Python from this directory."""
import copy,collections,json,pathlib,re,subprocess,sys
import sympy as sp
import generator as g
E=pathlib.Path('evidence');E.mkdir(exist_ok=True)
def save(name,value): (E/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def independent(p):
    x=g.X;poly=sp.Poly.from_dict({(p['n'],):p['a']},x).as_expr()+p['k']*x**2+p['l']*x+p['d']
    f=p['c']*sp.Pow(p['b'],poly)
    derivative=sp.diff(f,x)
    if p.get('equation'):
        t=sp.Rational(p['point']);return sp.expand(derivative.subs(x,t)*(x-t)+f.subs(x,t))
    if 'point' in p:return derivative.subs(x,sp.Rational(p['point']))
    if p.get('fragment'):return sp.cancel(derivative/sp.Pow(p['b'],poly))
    return derivative

def blank_fixture(value,tag):
    aid=g.uid([tag,value]);return {'knowledge_point':g.KP,'question':{':question/id':g.uid(tag),':question/problem':'Check {{field-1}}',':question/answer-fields':[{':answer-field/id':g.uid([tag,'field']),':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value}],':answer-field/correct':[':answer/id',aid]}]},'generation':{'template':'independent-equivalence'}}
def field(r):return r['question'][':question/answer-fields'][0]
def key(r):return field(r)[':answer-field/correct'][1]
def mathkey(r):return sp.sympify(r['generation']['answer_math'][key(r)],locals={'x':g.X})
def grade_cases(r,label):
    f=field(r)
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(r) else 'rejected','purpose':'all choices, independently checked key'} for a in f[':answer-field/choices']]
    else:
        correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key(r))
        checks=[{'submitted':correct,'expected':'accepted','purpose':'stored key'}, {'submitted':r'2\cdot('+correct+r')/2','expected':'accepted','purpose':'independently chosen equivalent'}, {'submitted':g.tex(mathkey(r)+1),'expected':'rejected','purpose':'wrong additive offset'}, {'submitted':g.tex(-mathkey(r)),'expected':'rejected','purpose':'wrong sign'}]
    return {'label':label,'record':r,'checks':checks}

replays=[];native=[];fidelity=[]
for qid,spec in g.SPECS.items():
    p=g.complete(qid,None);r=g.generate(spec['level'],seed=17,template=qid,parameters=g.default_params(qid),profile='historical:'+qid)
    expected=independent(p);assert sp.simplify(expected-mathkey(r))==0,qid
    src=g.SOURCES[qid];banks=[]
    for fi,f in enumerate(src.get(':question/answer-fields',[])):
        bank=g.original_bank(qid,p,f)
        # Compare parameterized historical recipes as complete multisets.
        generated=g.historical_bank(qid,p,fi)
        leftovers=[v for _,v in generated]
        for text,value,_ in bank:
            matches=[j for j,v in enumerate(leftovers) if sp.simplify(v-value)==0]
            assert matches,(qid,fi,text)
            leftovers.pop(matches[0])
            normalized=g.normalize_tex(g.normalized(text))
            # Independent native semantic check binds each captured full value
            # to its explicit mathematical recipe, not just its designation.
            canonical=g.tex(value)
            if p.get('equation'):
                canonical='y-('+canonical+')';normalized='y-('+normalized.split('=',1)[1]+')'
            native.append({'label':qid+' source option '+str(fi)+' '+text,'record':blank_fixture(canonical,[qid,fi,text]),'checks':[{'submitted':normalized,'expected':'accepted','purpose':'source full option vs mathematical recipe'}]})
        assert not leftovers
        banks.append({'field':fi,'matched':len(bank),'total':len(bank),'has_captured_key':':answer-field/correct' in f})
    original_prompt=g.normalize_prose(g.normalized(src[':question/problem']))
    assert r['question'][':question/problem'].startswith(original_prompt),qid
    if ':question/difficulty' in src:assert r['question'][':question/difficulty']==src[':question/difficulty'][':db/ident']
    if src.get(':question/answer-fields') and ':answer-field/correct' in src[':question/answer-fields'][0]:
        source_key=src[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
        generated_key=next(a[':answer/value'] for a in field(r)[':answer-field/choices'] if a[':answer/id']==key(r))
        assert generated_key==g.normalize_tex(g.normalized(source_key)),(qid,'captured designation')
    replays.append(r);native.append(grade_cases(r,qid+' historical usable replay'))
    fidelity.append({'source':qid,'banks':banks,'prompt_matched':True,'original_difficulty_preserved':True,'missing_fields_completed':not bool(src.get(':question/answer-fields'))})
save('source-replay.json',replays);save('source-fidelity.json',{'sources':len(fidelity),'banks':sum(len(x['banks']) for x in fidelity),'options':sum(b['total'] for x in fidelity for b in x['banks']),'cases':fidelity})

records=[];counterfactuals=[];examples=[];checks=0
# Six per family: explicit sign/base boundaries plus ordinary seeded cases.
for qid,spec in g.SPECS.items():
    for j in range(6):
        r=g.generate(spec['level'],seed=1000+j,template=qid)
        p=g.complete(qid,r['generation']['parameters']);expected=independent(p)
        assert sp.simplify(expected-mathkey(r))==0,(qid,j)
        f=field(r);correct=0
        for a in f[':answer-field/choices']:
            val=sp.sympify(r['generation']['answer_math'][a[':answer/id']],locals={'x':g.X});correct+=sp.simplify(val-expected)==0
        assert correct==1,(qid,'ambiguous bank')
        # Read displayed input with an independent native equality check.
        formula=re.search(r'(?:f\(x\)|y)\s*=\s*(.*?)\$',r['question'][':question/problem'])[1].rstrip(',')
        u=p['a']*g.X**p['n']+p['l']*g.X+p['d']
        native.append({'label':qid+' prompt formula '+str(j),'record':blank_fixture(g.tex(p['c']*p['b']**u),[qid,j,'prompt']),'checks':[{'submitted':formula,'expected':'accepted','purpose':'rendered formula agrees with independent instance'}]})
        native.append(grade_cases(r,qid+' sampled '+str(j)));records.append(r);checks+=1
    # Relevant evidence counterfactual: coefficient sign reverses with all else held.
    p=g.default_params(qid);p['b']=3
    if qid=='q-107463':p['point']='0'
    p1=dict(p);p2=dict(p);p2['a']=-p1['a']
    pair=[]
    for params in (p1,p2):
        # Point shifts to maintain the reciprocal rule only when necessary.
        if qid=='q-48659':params['point']=str(sp.Rational(1,params['a']))
        r=g.generate(spec['level'],seed=31,template=qid,parameters=params)
        assert sp.simplify(mathkey(r)-independent(g.complete(qid,params)))==0
        pair.append(r);native.append(grade_cases(r,qid+' coefficient counterfactual '+str(params['a'])))
    assert sp.simplify(mathkey(pair[0])-mathkey(pair[1]))!=0,qid
    assert pair[0]['question'][':question/problem']!=pair[1]['question'][':question/problem']
    assert pair[0]['question'][':question/worked-solution']!=pair[1]['question'][':question/worked-solution']
    counterfactuals.append({'template':qid,'changed':'a (and reciprocal point only where constrained)','response_changed':True,'prompt_changed':True,'solution_changed':True,'records':pair})
    records.extend(pair)
    if qid in ('q-312462','q-340969','q-107463','q-107459'):examples.extend(pair)
# Irrelevant evidence for the coefficient-fragment demand.
p1=g.default_params('q-312462');p2={**p1,'d':-2};pair=[g.generate('easy',template='q-312462',parameters=p) for p in (p1,p2)]
assert sp.simplify(mathkey(pair[0])-mathkey(pair[1]))==0
assert pair[0]['question'][':question/problem']!=pair[1]['question'][':question/problem']
for i,r in enumerate(pair):native.append(grade_cases(r,'fragment irrelevant constant '+str(i)))
counterfactuals.append({'template':'q-312462','changed':'irrelevant exponent constant','response_preserved':True,'records':pair});records.extend(pair)
# Same function, different evaluation points (hold every coefficient fixed).
for qid in ('q-340969','q-340970','q-107463'):
    p1=g.default_params(qid);p2={**p1,'point':'0' if p1['point']!='0' else '-1'}
    if qid=='q-340970':p1={**p1,'a':-2,'d':-1};p2={**p1,'point':'-1'}
    pair=[g.generate(g.SPECS[qid]['level'],template=qid,parameters=p) for p in (p1,p2)]
    assert sp.simplify(mathkey(pair[0])-mathkey(pair[1]))!=0
    for i,r in enumerate(pair):native.append(grade_cases(r,qid+' point counterfactual '+str(i)))
    counterfactuals.append({'template':qid,'changed':'evaluation point only','response_changed':True,'records':pair});records.extend(pair)
# Explicit boundary domain checks (source degree/term count fixed).
for qid in g.SPECS:
    for base in (2,6):
        p=g.default_params(qid);p['b']=base
        r=g.generate(g.SPECS[qid]['level'],template=qid,parameters=p);records.append(r)
        assert sp.simplify(mathkey(r)-independent(g.complete(qid,p)))==0
        native.append(grade_cases(r,qid+' base boundary '+str(base)))
# Targeted follow-up to a small-sample cue uncertainty: positive linear cases
# were dominated by source a=9 boundaries, and q-107461 had only three positive
# examples. Hold all other source data fixed and exercise a=2,3,4,5.
for qid in ('q-1952','q-107461'):
    for coefficient in (2,3,4,5):
        p={**g.default_params(qid),'a':coefficient}
        r=g.generate('easy',seed=200+coefficient,template=qid,parameters=p)
        assert sp.simplify(mathkey(r)-independent(g.complete(qid,p)))==0
        native.append(grade_cases(r,qid+' targeted positive coefficient '+str(coefficient)));records.append(r)
# Fill only observed base-slot gaps, without sampling unrelated combinations.
for qid in g.SPECS:
    seen={r['generation']['parameters']['b'] for r in records if r['generation']['template']==qid}
    for base in sorted(set(range(2,7))-seen):
        p={**g.default_params(qid),'b':base};r=g.generate(g.SPECS[qid]['level'],seed=300+base,template=qid,parameters=p)
        assert sp.simplify(mathkey(r)-independent(g.complete(qid,p)))==0
        native.append(grade_cases(r,qid+' missing base '+str(base)));records.append(r)
# Deterministic CLI and direct generator replay.
a=[g.generate('easy',seed=18+i) for i in range(5)];b=[g.generate('easy',seed=18+i) for i in range(5)];assert a==b
save('samples.json',a);save('test-records.json',records);save('counterfactuals.json',counterfactuals);save('grader-input.json',native);save('render-records.json',examples+[replays[-1]]+[r for r in replays if r['generation']['template'] in ('q-71881','q-48631','q-48659')])
save('mathematics.json',{'source_cases':len(replays),'sample_cases':checks,'total_test_records':len(records),'counterfactual_pairs':len(counterfactuals),'determinism':True,'failures':[],'rejections':g.REJECTIONS})
print(json.dumps({'source_cases':len(replays),'records':len(records),'grader_cases':len(native),'counterfactual_pairs':len(counterfactuals),'rejections':g.REJECTIONS}))
