#!/usr/bin/env python3
"""Failure-enforcing fidelity, displayed-math, schema, bounds and native QA."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parent))
from independent_math import slopes as independently_transcribed_slopes
HERE=Path(__file__).resolve().parent
SCRIPT=HERE.parent/(HERE.name+'.py')
spec=importlib.util.spec_from_file_location('kp',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def correct(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def formatting(q):
    for key in (':question/problem',':question/worked-solution'):
        t=q[key];assert t.count('$')%2==0
        assert not any(ord(ch)<32 and ch not in '\n\t' for ch in t)
        depth=0
        for ch in t:
            if ch=='{':depth+=1
            elif ch=='}':depth-=1
            assert depth>=0
        assert depth==0
        assert not re.search(r'(?<!\\)(?:\+\-|--)',t)

def binding_check(r):
    # Read variable declaration/definition and differential inputs literally,
    # independently of generation metadata or generator substitution helpers.
    q=r['question'];prompt=q[':question/problem'];solution=q[':question/worked-solution']
    declaration=re.search(r'Let \$(\w)=(\w)\((\w)\)\$\.',prompt)
    if declaration:
        assert declaration[1]==declaration[2] and declaration[1]!=declaration[3]
        independent,dependent=declaration[3],declaration[1]
    else:independent,dependent='x','y'
    assert 'dependent variable $'+dependent+'$ and independent variable $'+independent+'$' in solution
    opening=solution.split('\n\nWith')[0]
    assert '=f('+dependent+'),' in opening and '=f('+dependent+').' in opening
    from scripts.question_capture.math_format import MATH
    for text in (prompt,solution):
        for match in MATH.finditer(text):
            body=match[0]
            for dep,ind in re.findall(r'\\frac\{\\text\{d\}([A-Za-z])\}\{\\text\{d\}([A-Za-z])\}',body):
                assert (ind,dep)==(independent,dependent)
            for dep in re.findall(r"\{([A-Za-z])\}\^\{[′']\}",body):assert dep==dependent
            for signature in re.findall(r'f\(([^)]*)\)',body):
                assert set(signature.split(','))<={independent,dependent}
    meta=r['generation']['bindings'];assert meta['independent']==independent and meta['dependent']==dependent
    return independent,dependent

def math_check(r):
    q=r['question'];eqs=g.prompt_equations(q[':question/problem']);assert len(eqs)==3
    binding=binding_check(r);independent,dependent=binding
    answers=g.designation(q[':question/problem'],eqs)
    assert answers==[correct(f) for f in q[':question/answer-fields']]
    independent_slopes=independently_transcribed_slopes(r['generation'],q[':question/difficulty'].split('/')[-1])
    for eq,reference in zip(eqs,independent_slopes):
        assert sp.simplify(g.isolate(eq,binding)-reference)==0,('independent displayed input mismatch',eq)
    errors=[]
    blocks=q[':question/worked-solution'].split('- Equation ')[1:]
    assert len(blocks)==3
    for i,(eq,block) in enumerate(zip(eqs,blocks)):
        expected=g.isolate(eq,binding);A=sp.simplify(sp.diff(expected,g.X))==0
        assert ('is an autonomous differential equation' in block)==A
        for display in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block,re.S):
            rows=display.split(r'\\')
            # Every structural row independently read from displayed math.
            for j,row in enumerate(rows):
                row=row.strip().replace(' & ', '').replace('&','')
                if '=f(' in row:
                    forms=['f('+dependent+')'] if A else (['f('+independent+','+dependent+')'] if expected.has(g.Y) else ['f('+independent+')','f('+independent+','+dependent+')'])
                    if row.split('=')[1] not in forms:errors.append([i,'formal_dependency'])
                    continue
                candidate=g.isolate(row,binding)
                if sp.simplify(candidate-expected)!=0:errors.append([i,'row_value'])
        # Read displayed where-f expression as well, catches stale prose slots.
        for form,rhs in re.findall(r'where \$(f\([^)]*\))=(.*?)\.\$',block):
            if sp.simplify(g.read(rhs,binding)-expected)!=0:errors.append([i,'where_value'])
            if form=='f('+dependent+')' and not A:errors.append([i,'where_dependency'])
    selected=[g.ROMAN[i] for i,v in enumerate(answers) if v=='true']
    assert q[':question/worked-solution'].endswith('"'+' and '.join(selected)+' only."')
    return errors

def schema(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];assert q[':question/difficulty'] in [':question.difficulty/'+l for l in g.CATALOG]
    import uuid
    uuid.UUID(q[':question/id']);seen=set()
    for f in q[':question/answer-fields']:
        uuid.UUID(f[':answer-field/id']);assert f[':answer-field/type']==':answer-field.type/checkbox'
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
        for a in f[':answer-field/choices']:
            uuid.UUID(a[':answer/id']);assert a[':answer/id'] not in seen;seen.add(a[':answer/id'])
            assert a[':answer/type']==':answer.type/text'
        assert f[':answer-field/correct'][0]==':answer/id'
        assert f[':answer-field/correct'][1] in [a[':answer/id'] for a in f[':answer-field/choices']]
    formatting(q)

cases=[];review=[];native=[];source_results=[];raw_errors={}
def native_add(label,r):
    checks=[]
    for i,f in enumerate(r['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==correct(f) else 'rejected','purpose':'actual checkbox Boolean choice grading'})
    native.append({'label':label,'record':r,'checks':checks})

for template,q in g.QUESTIONS.items():
    level=q[':question/difficulty'][':db/ident'].split('/')[-1];p=g.source_parameters(q)
    case={'source_id':q[':db/id'],'template':template,'level':level,'parameters':p,'bank_profile':'observed_raw'};cases.append(case)
    raw=g.generate(level,template=template,parameters=p,profile='observed_raw');schema(raw)
    a=raw['question'];assert a[':question/problem']==q[':question/problem'];assert a[':question/worked-solution']==q[':question/worked-solution']
    assert set(a)==set(q)
    for f,s in zip(a[':question/answer-fields'],q[':question/answer-fields']):
        assert set(f)==set(s)
        assert f[':answer-field/key']==s[':answer-field/key']
        assert sorted(x[':answer/value'] for x in f[':answer-field/choices'])==sorted(x[':answer/value'] for x in s[':answer-field/choices'])
        assert correct(f)==s[':answer-field/correct'][':answer/value']
        assert f[':answer-field/type']==s[':answer-field/type'][':db/ident']
        for answer in f[':answer-field/choices']:
            original=next(x for x in s[':answer-field/choices'] if x[':answer/value']==answer[':answer/value'])
            assert set(answer)==set(original)
            assert answer[':answer/type']==original[':answer/type'][':db/ident']
    errors=math_check(raw)
    if errors: raw_errors[template]=errors
    normal=g.generate(level,template=template,parameters=p,profile='observed_repaired');schema(normal);assert not math_check(normal),(template,math_check(normal))
    # Source masks must genuinely generalize through the exact public API.
    p2={k:(2 if v!=2 else 3) if k.startswith('n') and k[1:].isdigit() else v for k,v in p.items()}
    changed=g.generate(level,template=template,parameters=p2,profile='observed_repaired');schema(changed);assert not math_check(changed),(template,math_check(changed))
    assert changed['question'][':question/problem']!=a[':question/problem']
    review.extend([{'label':'observed original '+template,'record':raw},{'label':'generated source-template variant '+template,'record':changed}])
    native_add('source '+template,raw);native_add('changed source '+template,changed)
    source_results.append({'source_id':q[':db/id'],'template':template,'banks_matched':3,'values_matched':6,'designations_matched':3,'prompt_exact':True,'solution_raw_exact':True,'key_presence_exact':True,'original_math_errors':errors,'normal_solution_repaired':bool(errors)})
assert raw_errors=={'q-96702':[[1,'row_value'],[1,'where_value']]},raw_errors
source_boundary_instances=0
for template,q in g.QUESTIONS.items():
    level=q[':question/difficulty'][':db/ident'].split('/')[-1]
    for maximum in (False,True):
        parameters=g.source_parameters(q)
        for key,value in list(parameters.items()):
            if not key.startswith('n') or not key[1:].isdigit():continue
            uses_power=re.search(r'\}\^\{'+key[1:]+r'\}',q[':question/problem'])
            parameters[key]=(3 if uses_power else 8) if maximum else 2
        r=g.generate(level,template=template,parameters=parameters,profile='observed_repaired')
        schema(r);assert not math_check(r),(template,parameters,math_check(r));source_boundary_instances+=1
source_binding_instances=0
for template,q in g.QUESTIONS.items():
    level=q[':question/difficulty'][':db/ident'].split('/')[-1]
    for independent,dependent,notation in [('t','u','prime'),('s','v','leibniz')]:
        parameters=g.source_parameters(q)|{'independent':independent,'dependent':dependent,'notation':notation}
        record=g.generate(level,template=template,parameters=parameters,profile='observed_repaired')
        schema(record);assert not math_check(record)
        assert correct(record['question'][':question/answer-fields'][0])==q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
        source_binding_instances+=1
        native_add('equivalent variable/notation source '+template+' '+notation,record)
        review.append({'label':'generated source binding variant '+template+' '+notation,'record':record})
counts={};task_samples={};ids={}
for level,catalog in g.CATALOG.items():
    eligible=[list(k) for k in itertools.combinations(catalog,3) if {z.split(':')[1] for z in k}=={'x','y'}]
    counts[level]=len(eligible)*2
    semantic=set()
    # Exhaust finite categorical catalog and both criteria, not numerical aliases.
    for index,kinds in enumerate(eligible):
        for negate in (False,True):
            p={'kinds':kinds,'a':2+index%3,'b':1+index%4,'n':2+index%2,'c':5+index%3,'negate':negate}
            r=g.generate(level,seed=index,parameters=p);schema(r);assert not math_check(r),(level,p,math_check(r));semantic.add(r['generation']['mathematical_fingerprint'])
            same=g.generate(level,seed=index+91,parameters=p)
            assert r['question'][':question/id']==same['question'][':question/id']
            assert r['generation']['mathematical_fingerprint']==same['generation']['mathematical_fingerprint']
            ids.setdefault(level,set()).add(r['question'][':question/id'])
            if index<2: review.append({'label':'generated authored '+level+' '+str(index)+' criterion '+str(negate),'record':r})
            native_add('authored '+level+' '+str(index)+' '+str(negate),r)
    assert len(semantic)==counts[level];task_samples[level]=len(semantic)
    # Sampling and explicit inputs use identical workload bounds.
    for bad in [{'independent':'u','dependent':'u'},{'independent':'r'},{'notation':'partial'},{'a':1},{'a':-3},{'b':0},{'n':4},{'c':4},{'negate':'false'},{'kinds':[catalog[0]]*3}]:
        base={'kinds':eligible[0],'a':2,'b':1,'n':2,'c':5,'negate':False};base.update(bad)
        try:g.generate(level,parameters=base)
        except ValueError:pass
        else:raise AssertionError(('bound did not reject',level,bad))
    for seed in range(60):
        r=g.generate(level,seed);schema(r);assert not math_check(r)
    # Explicit numerical boundary values must remain valid.
    for a,b,n,c in itertools.product((2,4),(1,4),(2,3),(5,7)):
        r=g.generate(level,parameters={'kinds':eligible[-1],'a':a,'b':b,'n':n,'c':c,'negate':False});schema(r);assert not math_check(r)
binding_instances=0;sampled_bindings={};slot_coverage={};mutation_results=[]
for level in g.CATALOG:
    base=g.generate(level,seed=11)['generation']['parameters']
    invariant=g.generate(level,parameters=base)
    for permutation in itertools.permutations(base['kinds']):
        permuted=g.generate(level,seed=33,parameters=base|{'kinds':list(permutation)})
        assert permuted['question'][':question/id']==invariant['question'][':question/id']
        assert permuted['generation']['mathematical_fingerprint']==invariant['generation']['mathematical_fingerprint']
        assert permuted['question'][':question/problem']==invariant['question'][':question/problem']
        assert permuted['question'][':question/worked-solution']==invariant['question'][':question/worked-solution']
    fingerprint=None
    for independent,dependent in g.BINDING_PAIRS:
        for notation in g.NOTATIONS:
            parameters=base|{'independent':independent,'dependent':dependent,'notation':notation}
            r=g.generate(level,parameters=parameters);schema(r);assert not math_check(r)
            if fingerprint is None:fingerprint=r['generation']['mathematical_fingerprint']
            assert fingerprint==r['generation']['mathematical_fingerprint']
            binding_instances+=1;native_add('equivalent binding '+level+' '+independent+dependent+' '+notation,r)
            review.append({'label':'generated authored binding '+level+' '+independent+dependent+' '+notation,'record':r})
    sampled_bindings[level]=sorted({(g.generate(level,seed=i)['generation']['bindings']['independent'],g.generate(level,seed=i)['generation']['bindings']['dependent'],g.generate(level,seed=i)['generation']['bindings']['notation']) for i in range(100)})
    assert len(sampled_bindings[level])==8
    slot_coverage[level]={'binding_pairs':4,'derivative_notations':2,'families':sorted(set(k.split(':')[0] for k in g.CATALOG[level])),'criterion':[False,True],'numeric_boundaries':{'a':[2,4],'b':[1,4],'n':[2,3],'c':[5,7]},'presentation_aliases_excluded_from_task_counts':True}
    # Incidental numerical parameters and notation aliases do not create tasks.
    alternate=base|{'a':2 if base['a']!=2 else 4,'b':1 if base['b']!=1 else 4,'n':2 if base['n']!=2 else 3,'c':5 if base['c']!=5 else 7}
    assert g.generate(level,parameters=base)['generation']['mathematical_fingerprint']==g.generate(level,parameters=alternate)['generation']['mathematical_fingerprint']

def rejects(label,record):
    try:
        schema(record);assert not math_check(record);backbone_check(record)
    except (AssertionError,ValueError,KeyError):mutation_results.append({'mutation':label,'rejected':True})
    else:raise AssertionError(('mutation survived',label))

# Stage signatures read from actual displayed math. Equality/row counts cannot
# substitute for the factored divide-and-cancel operation at authored hard.
def backbone_check(record):
    meta=record['generation'];q=record['question']
    if meta['template']!='authored_triplet':return
    level=q[':question/difficulty'].split('/')[-1];binding=binding_check(record)
    eqs=g.prompt_equations(q[':question/problem']);blocks=q[':question/worked-solution'].split('- Equation ')[1:]
    for equation,block in zip(eqs,blocks):
        displays=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block,re.S)
        if level=='easy':assert not displays;continue
        assert len(displays)==1
        rows=displays[0].split(r'\\');A=g.autonomous(equation,binding)
        assert len(rows)==(4 if level=='hard' and A else 3)
        first=rows[0].strip().replace(' & ','').replace('&','')
        assert first==equation
        operation=rows[1].split('=')[1].strip()
        assert operation.startswith(r'\frac{')
        lhs,rhs=equation.split('=')
        dependent=binding[1];independent=binding[0]
        derivative_token=re.search(r'\\frac\{\\text\{d\}[A-Za-z]\}\{\\text\{d\}[A-Za-z]\}|\{[A-Za-z]\}\^\{[′\']\}',lhs)[0]
        if level=='hard':
            coefficient=lhs.replace(derivative_token,'')
            expected_operation=r'\frac{'+rhs+'}{'+coefficient+'}'
            if A:
                reduced_rhs=rows[2].split('=')[1]
                assert independent not in re.findall(r'\\[A-Za-z]+|[A-Za-z]',reduced_rhs)
        else:
            coefficient,constant=lhs.rsplit('+',1)
            coefficient=coefficient.replace(derivative_token,'')
            assert constant in ('1','2','3','4')
            expected_operation=r'\frac{'+rhs+'-'+constant+'}{'+coefficient+'}'
        assert operation==expected_operation

for level in ('moderate','hard'):
    fixture=g.generate(level,parameters={'kinds':list(g.CATALOG[level][:3]),'a':2,'b':1,'n':2,'c':5,'negate':False,'independent':'t','dependent':'u','notation':'prime'})
    backbone_check(fixture)
    for label,change in [('stale-independent-definition',lambda q:q.replace('independent variable $t$','independent variable $x$')),('stale-dependent-definition',lambda q:q.replace('dependent variable $u$','dependent variable $y$')),('wrong-formal-function-input',lambda q:q.replace('=f(u),','=f(t),',1)),('control-byte',lambda q:q+'\x0c')]:
        mutated=copy.deepcopy(fixture);mutated['question'][':question/worked-solution']=change(mutated['question'][':question/worked-solution']);rejects(level+' '+label,mutated)
    mutated=copy.deepcopy(fixture);mutated['question'][':question/problem']=mutated['question'][':question/problem'].replace('{u}', '{v}',1);rejects(level+' wrong derivative input',mutated)
    # Replace a required operative fraction by an algebraically equal simplified
    # RHS, keeping the same row count and all correct Boolean designations.
    mutated=copy.deepcopy(fixture);eq=g.prompt_equations(mutated['question'][':question/problem'])[0];expr=g.isolate(eq,('t','u'));actual=g.tex(expr).replace('x','t').replace('y','u')
    sol=mutated['question'][':question/worked-solution'];display=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);rows=display[1].split(r'\\');left=rows[1].split('=')[0];rows[1]=left+'='+actual
    mutated['question'][':question/worked-solution']=sol[:display.start(1)]+r'\\'.join(rows)+sol[display.end(1):];rejects(level+' erased operative quotient',mutated)

classification_boundaries=[(r't\frac{\text{d}u}{\text{d}t}=tu',True),(r'\frac{\text{d}u}{\text{d}t}=t-t+u',True),(r't\frac{\text{d}u}{\text{d}t}=t(u-u)',True),(r'\frac{\text{d}u}{\text{d}t}=tu',False),(r'\frac{\text{d}u}{\text{d}t}=0',True)]
for equation,expected in classification_boundaries:assert g.autonomous(equation,('t','u'))==expected
try:g.isolate(r'0\frac{\text{d}u}{\text{d}t}=u',('t','u'))
except AssertionError:pass
else:raise AssertionError('zero derivative coefficient survived')
for entry in review:
    record=entry['record'];backbone_check(record)

preserved=json.loads((HERE/'baseline-preservation.json').read_text())
baseline_paths=[Path(p) for p in preserved['paths']]
actual_paths=[Path(preserved['script'])]+[p for p in Path(preserved['directory']).rglob('*') if p.is_file()]
assert sorted(map(str,actual_paths))==preserved['paths']
assert all(hashlib.sha256(p.read_bytes()).hexdigest()==preserved['sha256'][str(p)] for p in baseline_paths)
assert json.loads((HERE/'independent-inventory.json').read_text())['questions']==[]
assert not ids['easy']&ids['moderate'] and not ids['moderate']&ids['hard']
write('source-cases.json',cases);write('review.json',review);write('native-input.json',native)
engine=SCRIPT.parent.parent/'runs/current/check-engine'
subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
report=json.loads((HERE/'native-report.json').read_text())
validation={'status':'passed','source':{k:g.CAPTURE[k] for k in ('database','basis','lineage')},'independently_transcribed_template_slopes_checked':True,'source_questions':len(cases),'complete_banks_matched':45,'displayed_values_matched':90,'correct_designations_matched':45,'exact_prompts':15,'raw_exact_solutions':15,'original_mathematically_correct_solutions':14,'supported_repaired_solutions':1,'raw_source_errors':raw_errors,'key_presence_parity':15,'source_results':source_results,'authored_semantic_tasks':counts,'exhausted_semantic_tasks':task_samples,'random_samples_checked':180,'boundary_instances_checked':48,'source_boundary_instances_checked':source_boundary_instances,'source_binding_instances_checked':source_binding_instances,'authored_binding_instances_checked':binding_instances,'triplet_permutation_identity_regressions':18,'sampled_binding_slot_coverage':sampled_bindings,'slot_coverage':slot_coverage,'structural_mutation_checks':mutation_results,'classification_zero_cancellation_boundaries':len(classification_boundaries)+1,'registered_baseline_files_preserved':len(baseline_paths),'independent_inventory_questions':0,'native_accepted':report['accepted_checks'],'native_rejected':report['rejected_checks'],'native_unresolved':report['documented_unresolved_checks'],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'database_writes':0}
write('validation.json',validation)
lines=['# Review','', 'All original records retain captured wording. Raw evidence is ineligible for learner use. One source error is listed in template-extraction.md. Generated labels identify authored versus source-mask variants.','']
for item in review:
    r=item['record'];q=r['question'];lines.extend(['## '+item['label'],'',q[':question/problem'],'', 'Correct checkbox values: '+', '.join(f[':answer-field/key']+'='+correct(f) for f in q[':question/answer-fields']),'',q[':question/worked-solution'],''])
(HERE/'review.md').write_text('\n'.join(lines))
print(json.dumps(validation,indent=2))
