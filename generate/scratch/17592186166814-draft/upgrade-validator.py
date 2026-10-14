from pathlib import Path
p=Path('generate/scratch/17592186166814-draft/validate.py');s=p.read_text()
s=s.replace('import hashlib,importlib.util,itertools,json,re,subprocess,sys','import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys\nsys.dont_write_bytecode=True')
s=s.replace("    q=r['question'];eqs=g.prompt_equations(q[':question/problem']);assert len(eqs)==3", "    q=r['question'];eqs=g.prompt_equations(q[':question/problem']);assert len(eqs)==3\n    binding=binding_check(r);independent,dependent=binding")
s=s.replace('expected=g.isolate(eq);','expected=g.isolate(eq,binding);')
s=s.replace("forms=['f(y)'] if A else (['f(x,y)'] if expected.has(g.Y) else ['f(x)','f(x,y)'])", "forms=['f('+dependent+')'] if A else (['f('+independent+','+dependent+')'] if expected.has(g.Y) else ['f('+independent+')','f('+independent+','+dependent+')'])")
s=s.replace('candidate=g.isolate(row)','candidate=g.isolate(row,binding)')
s=s.replace('g.read(rhs)-expected','g.read(rhs,binding)-expected')
s=s.replace("if form=='f(y)' and not A", "if form=='f('+dependent+')' and not A")
s=s.replace("        t=q[key];assert t.count('$')%2==0", "        t=q[key];assert t.count('$')%2==0\n        assert not any(ord(ch)<32 and ch not in '\\n\\t' for ch in t)")
start=s.index('def math_check(')
s=s[:start]+'''def binding_check(r):
    # Read variable declaration/definition and differential inputs literally,
    # independently of generation metadata or generator substitution helpers.
    q=r['question'];prompt=q[':question/problem'];solution=q[':question/worked-solution']
    declaration=re.search(r'Let \\$(\\w)=(\\w)\\((\\w)\\)\\$\\.',prompt)
    if declaration:
        assert declaration[1]==declaration[2] and declaration[1]!=declaration[3]
        independent,dependent=declaration[3],declaration[1]
    else:independent,dependent='x','y'
    assert 'dependent variable $'+dependent+'$ and independent variable $'+independent+'$' in solution
    opening=solution.split('\\n\\nWith')[0]
    assert '=f('+dependent+'),' in opening and '=f('+dependent+').' in opening
    from scripts.question_capture.math_format import MATH
    for text in (prompt,solution):
        for match in MATH.finditer(text):
            body=match[0]
            for dep,ind in re.findall(r'\\\\frac\\{\\\\text\\{d\\}([A-Za-z])\\}\\{\\\\text\\{d\\}([A-Za-z])\\}',body):
                assert (ind,dep)==(independent,dependent)
            for dep in re.findall(r"\\{([A-Za-z])\\}\\^\\{[′']\\}",body):assert dep==dependent
            for signature in re.findall(r'f\\(([^)]*)\\)',body):
                assert set(signature.split(','))<={independent,dependent}
    meta=r['generation']['bindings'];assert meta['independent']==independent and meta['dependent']==dependent
    return independent,dependent

'''+s[start:]
s=s.replace("p2={k:2 if v!=2 else 3 for k,v in p.items()}","p2={k:(2 if v!=2 else 3) if k.startswith('n') and k[1:].isdigit() else v for k,v in p.items()}")
s=s.replace("        parameters={}\n        for key,value in g.source_parameters(q).items():", "        parameters=g.source_parameters(q)\n        for key,value in list(parameters.items()):\n            if not key.startswith('n') or not key[1:].isdigit():continue")
marker="counts={};task_samples={};ids={}"
s=s.replace(marker,'''source_binding_instances=0
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
'''+marker)
s=s.replace("for bad in [{'a':1}","for bad in [{'independent':'u','dependent':'u'},{'independent':'r'},{'notation':'partial'},{'a':1}")
marker="assert not ids['easy']&ids['moderate'] and not ids['moderate']&ids['hard']"
s=s.replace(marker,'''binding_instances=0;sampled_bindings={};slot_coverage={};mutation_results=[]
for level in g.CATALOG:
    base=g.generate(level,seed=11)['generation']['parameters']
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
        displays=re.findall(r'\\\\begin\\{aligned\\}(.*?)\\\\end\\{aligned\\}',block,re.S)
        if level=='easy':assert not displays;continue
        assert len(displays)==1
        rows=displays[0].split(r'\\\\');A=g.autonomous(equation,binding)
        assert len(rows)==(4 if level=='hard' and A else 3)
        first=rows[0].strip().replace(' & ','').replace('&','')
        assert first==equation
        operation=rows[1].split('=')[1].strip()
        assert operation.startswith(r'\\frac{')
        if level=='hard':
            assert operation.count(r'\\left(')==3
            assert r'\\right)\\left(' in operation
            if A:assert r'\\frac{' not in rows[2] and r'\\left(' not in rows[2]
        else:
            assert r'\\left(' in operation and re.search(r'\\right\\)-[1-4]\\}',operation)

for level in ('moderate','hard'):
    fixture=g.generate(level,parameters={'kinds':list(g.CATALOG[level][:3]),'a':2,'b':1,'n':2,'c':5,'negate':False,'independent':'t','dependent':'u','notation':'prime'})
    backbone_check(fixture)
    for label,change in [('stale-independent-definition',lambda q:q.replace('independent variable $t$','independent variable $x$')),('stale-dependent-definition',lambda q:q.replace('dependent variable $u$','dependent variable $y$')),('wrong-formal-function-input',lambda q:q.replace('=f(u),','=f(t),',1)),('control-byte',lambda q:q+'\\x0c')]:
        mutated=copy.deepcopy(fixture);mutated['question'][':question/worked-solution']=change(mutated['question'][':question/worked-solution']);rejects(level+' '+label,mutated)
    mutated=copy.deepcopy(fixture);mutated['question'][':question/problem']=mutated['question'][':question/problem'].replace('{u}', '{v}',1);rejects(level+' wrong derivative input',mutated)
    # Replace a required operative fraction by an algebraically equal simplified
    # RHS, keeping the same row count and all correct Boolean designations.
    mutated=copy.deepcopy(fixture);eq=g.prompt_equations(mutated['question'][':question/problem'])[0];expr=g.isolate(eq,('t','u'));actual=g.tex(expr).replace('x','t').replace('y','u')
    sol=mutated['question'][':question/worked-solution'];display=re.search(r'\\\\begin\\{aligned\\}(.*?)\\\\end\\{aligned\\}',sol,re.S);rows=display[1].split(r'\\\\');left=rows[1].split('=')[0];rows[1]=left+'='+actual
    mutated['question'][':question/worked-solution']=sol[:display.start(1)]+r'\\\\'.join(rows)+sol[display.end(1):];rejects(level+' erased operative quotient',mutated)

classification_boundaries=[(r't\\frac{\\text{d}u}{\\text{d}t}=tu',True),(r'\\frac{\\text{d}u}{\\text{d}t}=t-t+u',True),(r't\\frac{\\text{d}u}{\\text{d}t}=t(u-u)',True),(r'\\frac{\\text{d}u}{\\text{d}t}=tu',False),(r'\\frac{\\text{d}u}{\\text{d}t}=0',True)]
for equation,expected in classification_boundaries:assert g.autonomous(equation,('t','u'))==expected
try:g.isolate(r'0\\frac{\\text{d}u}{\\text{d}t}=u',('t','u'))
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
'''+marker)
s=s.replace("'source_boundary_instances_checked':source_boundary_instances,", "'source_boundary_instances_checked':source_boundary_instances,'source_binding_instances_checked':source_binding_instances,'authored_binding_instances_checked':binding_instances,'sampled_binding_slot_coverage':sampled_bindings,'slot_coverage':slot_coverage,'structural_mutation_checks':mutation_results,'classification_zero_cancellation_boundaries':len(classification_boundaries)+1,'registered_baseline_files_preserved':len(baseline_paths),'independent_inventory_questions':0,")
p.write_text(s)
