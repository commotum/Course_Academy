#!/usr/bin/env python3
"""Independent rendered-ODE recognition, source fidelity, native grading.

No generator classification/rendering helpers are used for mathematical QA.
Derivative notation is translated to formal independent symbols; the actual
printed residual is parsed and simplified with SymPy before reading its order.
Initial-condition chains are read independently. The fixed worked solution is
checked against the complete prompt ODE and actual supplied condition components.
"""
import copy, hashlib, importlib.util, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SCRIPT=HERE.with_suffix('.py')
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);obj=importlib.util.module_from_spec(spec);sys.modules[name]=obj;spec.loader.exec_module(obj);return obj
g=module('ivp_generator',SCRIPT)
parser=module('independent_scalar',ROOT/'generate/runs/current/ode-scalar-parser.py')
D={1:parser.u,2:parser.v,3:parser.z}

def save(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def spans(text):return re.findall(r'(?<!\$)\$(?!\$)([^$]*?)\$(?!\$)',text,re.S)
def systems(text):
    result=re.findall(r'- \*\*([IV]+)\.\*\* \$(.*?)\$',text)
    assert [key for key,s in result]==['I','II','III'];return [s for key,s in result]
def deriv_tokens(tex):
    for n,signs in [(3,['‴',"'''"]),(2,['″',"''"]),(1,['′',"'"])]:
        for sign in signs:tex=tex.replace('{y}^{'+sign+'}',str(D[n]))
    tex=tex.replace(r'\dfrac{dy}{dx}',str(D[1])).replace(r'\frac{dy}{dx}',str(D[1]))
    for n in (2,3):
        for cmd in ('frac','dfrac'):
            tex=tex.replace('\\'+cmd+'{d^'+str(n)+'y}{dx^'+str(n)+'}',str(D[n]))
    return tex
def read_ode(tex):
    sides=tex.split('=');assert len(sides)==2,tex
    residual=sp.expand(parser.scalar(deriv_tokens(sides[0]))-parser.scalar(deriv_tokens(sides[1])))
    orders=[n for n,symbol in D.items() if residual.has(symbol)]
    assert orders,tex
    for n in orders:assert residual.coeff(D[n])!=0
    return max(orders),residual
def read_conditions(tex):
    """Read separate and chained point values from the actual displayed text."""
    tex=deriv_tokens(tex).strip().rstrip('.,').replace(r'\,','')
    if not tex:return []
    result=[]
    for fragment in tex.split(','):
        terms=fragment.strip().rstrip('.').split('=');assert len(terms)>=2,(tex,fragment)
        value=parser.scalar(terms[-1]);assert not value.free_symbols
        for left in terms[:-1]:
            m=re.fullmatch(r'([yuvz])\(([^()]*)\)',left.strip());assert m,(tex,left)
            point=parser.scalar(m[2]);assert not point.free_symbols
            result.append((m[1],point,value))
    return result
def actual_system(system):
    components=system.split(r',\,',1)
    order,residual=read_ode(components[0])
    conditions=read_conditions(components[1]) if len(components)>1 else []
    true=order==1 and any(name=='y' for name,point,value in conditions)
    return components[0],order,residual,conditions,true
def math_format(text):
    assert text.count('$')%2==0
    # Exhaust all math spans (including the formal display block).
    for tex in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)\$(?!\$)',text,re.S):
        value=tex[0] or tex[1];depth=0
        for c in value:
            if c=='{':depth+=1
            elif c=='}':depth-=1
            assert depth>=0,value
        assert depth==0,value
        assert not any(z in value for z in ('@@','--','+-','-+'))
    assert text.count(r'\left')==text.count(r'\right')
def validate_record(record,normal=False):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==17592186166815
    q=record['question'];gen=record['generation']
    assert all(k.startswith(':') for k in q)
    for key in (':question/problem',':question/worked-solution'):math_format(q[key])
    actual=[actual_system(s) for s in systems(q[':question/problem'])]
    fields=q[':question/answer-fields'];assert len(fields)==3
    ids=[q[':question/id']]
    for key,f,(_,order,residual,conditions,truth) in zip(('I','II','III'),fields,actual):
        assert f[':answer-field/key']==key and f[':answer-field/type']==':answer-field.type/checkbox'
        choices=f[':answer-field/choices'];assert len(choices)==2
        assert sorted(a[':answer/value'] for a in choices)==['false','true']
        assert all(a[':answer/type']==':answer.type/text' for a in choices)
        correct=[a for a in choices if a[':answer/id']==f[':answer-field/correct'][1]]
        assert f[':answer-field/correct'][0]==':answer/id' and len(correct)==1
        assert correct[0][':answer/value']==str(truth).lower()
        ids += [f[':answer-field/id']]+[a[':answer/id'] for a in choices]
        # Check the domain of the displayed ODE, without dividing by the highest
        # derivative coefficient or demanding an actual solution. Only the
        # documented raw q-96987 literal 1/x at x=0 is retained as an anomaly.
        function_conditions=[(point,value) for name,point,value in conditions if name=='y']
        for point,value in function_conditions:
            at_point=residual.subs({parser.x:point,parser.y:value},simultaneous=True)
            if at_point.has(sp.zoo,sp.nan,sp.oo,-sp.oo) or at_point.is_real is False:
                assert gen['profile']=='observed_raw' and gen['template']=='source_q-96987' and key=='III' and point==0,'Undocumented domain anomaly'
    assert len(ids)==len(set(ids));[uuid.UUID(i) for i in ids]
    solution=q[':question/worked-solution']
    assert solution.startswith(g.OPENING) or gen['template']=='source_q-96987'
    paragraphs=solution.split('\n\n- System ')[1:];assert len(paragraphs)==3
    for key,paragraph,(_,order,residual,conditions,truth) in zip(('I','II','III'),paragraphs,actual):
        assert paragraph.startswith(key+' ')
        verdict='is a first-order initial value problem.' if truth else 'is not a first-order initial value problem.'
        assert verdict in paragraph.split('$',1)[0],(paragraph,truth)
        listed=[];odes=[]
        for tex in spans(paragraph):
            tex=tex.rstrip('.,')
            if '=' not in tex:continue
            translated=deriv_tokens(tex)
            if re.match(r'[yuvz]\(',translated):listed.extend(read_conditions(tex))
            else:odes.append(read_ode(tex))
        if odes:
            assert len(odes)==1 and odes[0][0]==order and sp.simplify(odes[0][1]-residual)==0,(paragraph,residual)
        # Source omits the equation for a missing-condition option: preserve it.
        else:assert not truth and not conditions
        assert listed==conditions,(paragraph,listed,conditions)
        if conditions and order>1:
            assert ('*second*' if order==2 else '*third*')+'-order' in paragraph
            assert ('*two*' if order==2 else '*three*')+' initial conditions' in paragraph
            assert len(conditions)==order
    selected=[k for k,system in zip(('I','II','III'),actual) if system[-1]]
    expected=' and '.join(selected)+' only.'
    assert solution.endswith('Therefore, the correct answer is "'+expected+'"')
    if normal:
        assert gen['eligible_for_learning'] and not gen['evidence_only']
        for eq,order,residual,conditions,truth in actual:
            assert 1<=order<=3
            for name,point,value in conditions:
                assert point.is_real and (0<=point<=4 if gen['profile']=='observed_domain_repair' else 2<=point<=4) and -5<=value<=7
            if gen['template'].startswith('authored_'):
                level=q[':question/difficulty'].rsplit('/',1)[1]
                if level=='easy':assert order<=2 and r'\dfrac' not in eq and r'\left' not in eq
                elif level=='moderate':assert r'\dfrac' not in eq and r'\left' not in eq and '+x^2)' in eq
                else:assert r'\left(' in eq and r'\dfrac' in eq and r'\right)' in eq
                # Symbolic leading coefficient cannot vanish by cancellation;
                # regularity here is a sampling restriction, not a quiz demand.
                coefficient=sp.diff(residual,D[order]);assert not coefficient.has(*D.values())
                for point in (2,3,4):assert coefficient.subs(parser.x,point)>0
        if gen['template'] in ('authored_moderate','authored_hard'):assert any(s[1]>1 for s in actual)
    return len(actual)

def native_fixture(label,r):
    checks=[]
    for i,f in enumerate(r['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Complete owned boolean bank through native checkbox grader'})
    return {'label':label,'record':r,'checks':checks}

def main():
    source_cases=[];fidelity=[];native=[];review=[];originals=[];stage_count=0
    qkeys=(':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields')
    for sid,source in g.SOURCES.items():
        case={'source_id':source[':question/id'],'math_academy_id':sid,'db_id':source[':db/id'],'level':'easy','template':'source_'+sid,'parameters':g.DEFAULTS[sid],'bank_profile':'observed_raw'}
        source_cases.append(case)
        r=g.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
        stage_count+=validate_record(r)
        q=r['question']
        assert all((key in q)==(key in source) for key in qkeys)
        assert q[':question/problem']==source[':question/problem']
        assert q[':question/worked-solution']==source[':question/worked-solution']
        assert q[':question/difficulty']==source[':question/difficulty'][':db/ident']
        for f,old in zip(q[':question/answer-fields'],source[':question/answer-fields']):
            for k in (':answer-field/key',':answer-field/choices',':answer-field/correct',':answer-field/type'):assert (k in f)==(k in old)
            assert f[':answer-field/key']==old[':answer-field/key']
            assert f[':answer-field/type']==old[':answer-field/type'][':db/ident']
            assert sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in old[':answer-field/choices'])
            correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            assert correct==old[':answer-field/correct'][':answer/value']
        originals.append(r);native.append(native_fixture('source_'+sid,r))
        fidelity.append({'source':sid,'prompt_exact':True,'complete_worked_solution_exact':True,'field_layout_and_presence_exact':True,'complete_banks_matched':3,'values_matched':6,'correct_designations_matched':3,'mathematical_classification':'formal structural criterion; no existence assertion'})
        # Genuine parameterized changed-parameter replay through the public API.
        variants=[]
        for seed in (31,32):
            changed=g.generate('easy',seed,template='source_'+sid,profile='observed_regular')
            stage_count+=validate_record(changed,normal=True)
            assert changed['question'][':question/problem']!=q[':question/problem']
            assert changed['question'][':question/worked-solution']!=q[':question/worked-solution']
            variants.append(changed);review.append(changed)
            native.append(native_fixture('changed_'+sid+'_'+str(seed),changed))
        # Raw replay can also parameterize changed values without repairing them.
        changed_raw=g.generate('easy',99,template='source_'+sid,parameters=variants[0]['generation']['parameters'],profile='observed_raw')
        stage_count+=validate_record(changed_raw)
        assert changed_raw['question'][':question/problem']==variants[0]['question'][':question/problem']
    save('source-cases.json',source_cases)
    repaired=g.generate_easy(template='source_q-96987',profile='observed_domain_repair')
    stage_count+=validate_record(repaired,normal=True)
    raw_original=originals[list(g.SOURCES).index('q-96987')]
    assert repaired['question'][':question/problem']==raw_original['question'][':question/problem'].replace('2'+"{y}^{'}"+'-'+r'\frac{1}{x}'+'={e}^{y}'+r',\,'+'y(0)=1','2'+"{y}^{'}"+'-'+r'\frac{1}{x}'+'={e}^{y}'+r',\,'+'y(2)=1')
    save('domain-repair.json',repaired);native.append(native_fixture('minimal_domain_repair_q-96987',repaired))
    unique={};catalog_native=0;random_count=0
    for level in ('easy','moderate','hard'):
        unique[level]=set()
        for number,kinds in enumerate(g.CATALOG[level]):
            p={'kinds':kinds,'a':[2,3,5],'b':[1,3,5],'points':[2,3,4],'values':[-5,0,5]}
            r=g.generate(level,seed=number,parameters=p)
            stage_count+=validate_record(r,normal=True);native.append(native_fixture('catalog_'+level+'_'+str(number),r));catalog_native+=1
            unique[level].add(r['generation']['mathematical_fingerprint'])
            identical=g.generate(level,seed=number+17,parameters=p)
            assert identical['question'][':question/id']==r['question'][':question/id']
            assert identical['generation']['content_fingerprint']==r['generation']['content_fingerprint']
            # Numeric aliases do not inflate meaningful categorical task counts.
            changed=copy.deepcopy(p);changed['a']=[5,4,2];changed['b']=[5,4,3];changed['points']=[4,2,3]
            altered=g.generate(level,parameters=changed)
            stage_count+=validate_record(altered,normal=True)
            assert altered['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
            assert altered['question'][':question/id']!=r['question'][':question/id']
        assert len(unique[level])==len({tuple(sorted(kinds)) for kinds in g.CATALOG[level]})
        # Changing system labels/order affects presentation identity, not the
        # mathematical multiset of assessed classification cases.
        p={'kinds':g.CATALOG[level][0],'a':[2,2,2],'b':[1,1,1],'points':[2,2,2],'values':[0,0,0]}
        first=g.generate(level,parameters=p)
        p['kinds']=p['kinds'][1:]+p['kinds'][:1]
        permuted=g.generate(level,parameters=p)
        assert first['generation']['mathematical_fingerprint']==permuted['generation']['mathematical_fingerprint']
        assert first['question'][':question/id']!=permuted['question'][':question/id']
        for seed in range(150):
            r=g.generate(level,seed)
            stage_count+=validate_record(r,normal=True);random_count+=1
            if seed<2:review.append(r);native.append(native_fixture('review_'+level+'_'+str(seed),r))
    # Invalid explicit input is rejected, never replaced by a convenient sample.
    failures=0
    for level in ('easy','moderate','hard'):
        p=g.generate(level)['generation']['parameters']
        for key,bad in [('a',[0,2,2]),('a',[-2,2,2]),('a',[6,2,2]),('b',[0,1,1]),('points',[1,2,2]),('values',[-6,0,0])]:
            invalid=copy.deepcopy(p);invalid[key]=bad
            try:g.generate(level,parameters=invalid)
            except ValueError:failures+=1
            else:raise AssertionError((level,key,bad))
        if level!='easy':
            invalid=copy.deepcopy(p);invalid['kinds']=['ivp','missing','ivp']
            try:g.generate(level,parameters=invalid)
            except ValueError:failures+=1
            else:raise AssertionError('Higher-order workload vanished')
    p=copy.deepcopy(g.DEFAULTS['q-95985']);p['a']=0
    try:g.generate_easy(template='source_q-95985',parameters=p,profile='observed_raw')
    except ValueError:failures+=1
    else:raise AssertionError('Invalid observed coefficient accepted')
    for sid,index,key,value in [('q-96990',0,'point','-1'),('q-118791',1,'point','0'),('q-96990',0,'values',['0'])]:
        invalid=copy.deepcopy(g.DEFAULTS[sid]);invalid['conditions'][index][key]=value
        try:g.generate_easy(template='source_'+sid,parameters=invalid,profile='observed_raw')
        except ValueError:failures+=1
        else:raise AssertionError('New undocumented raw domain defect admitted')
    for kwargs in [{'level':'hard','template':'source_q-95985'},{'level':'easy','field_type':'radio'},{'level':'easy','profile':'opaque'},{'level':'moderate','template':'authored_hard'}]:
        try:g.generate(**kwargs)
        except ValueError:failures+=1
        else:raise AssertionError(kwargs)
    # Independent process determinism (unordered dictionary/set sampling traps).
    cli=[str(ROOT/'.venv/bin/python'),str(SCRIPT),'--difficulty','easy','--template','source_q-96986','--seed','22','--format','json']
    assert subprocess.check_output(cli)==subprocess.check_output(cli)
    raw_cli=[str(ROOT/'.venv/bin/python'),str(SCRIPT),'--difficulty','easy','--template','source_q-96986','--profile','observed_raw']
    assert '## Original source replay — easy' in subprocess.check_output(raw_cli,text=True)
    assert json.loads(subprocess.check_output(raw_cli+['--format','json']))[0]['question'][':question/problem']==g.SOURCES['q-96986'][':question/problem']
    normal_cli=subprocess.check_output([str(ROOT/'.venv/bin/python'),str(SCRIPT),'--difficulty','all'],text=True)
    for level in ('easy','moderate','hard'):assert '## Generated — '+level in normal_cli
    save('review.json',review+[repaired]);save('engine-input.json',native)
    engine=ROOT/'generate/runs/current/check-engine'
    subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine_report=json.loads((HERE/'engine-report.json').read_text())
    report={'passed':True,'source_provenance':g.SOURCE,'database_writes':0,
      'source_fidelity':{'questions':11,'exact_prompts':11,'exact_fixed_solutions':11,'field_layouts_and_presence_parity':11,'complete_boolean_field_banks':33,'all_choice_values_matched':66,'correct_designations_matched':33,'wrong_boolean_choices_matched':33,'raw_domain_wording_issue':'q-96987 System III includes 1/x at x=0; raw unchanged; regular authored sampling uses points 2..4'},
      'fidelity_cases':fidelity,'source_domain_correctness':{'ordinary_defined_point_records':10,'documented_raw_domain_wording_anomaly':1,'minimal_repaired_records':1},'changed_observed_public_api_variants':22,'changed_raw_public_api_variants':11,'authored_random_records_checked':random_count,'authored_ordered_layout_records_checked':catalog_native,'authored_coefficient_variants_checked':catalog_native,'independent_printed_system_checks':stage_count,'finite_semantic_catalog':{level:len(ids) for level,ids in unique.items()},'finite_ordered_layout_catalog':{level:len(catalog) for level,catalog in g.CATALOG.items()},'native_grading':{k:engine_report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'invalid_explicit_inputs_rejected':failures,'review_records':len(review)+1,'no_plots':True,
      'limitations':['All practice difficulty labels are easy. Moderate/hard workload distinctions are authored recognition scopes, not recovered source labels.','Coefficient and initial-value changes increase presentation variety but are excluded from semantic task counts. Finite meaningful catalogs are enumerated.','Raw source singular/unsatisfiable initial points are preserved as formal IVPs. Neither generator nor validator asserts existence or uniqueness. q-96987 also has a literal undefined 1/x at its initial point; raw replay remains evidence-only.'],
      'python':sys.version.split()[0],'sympy':sp.__version__,'generator_sha256':sha(SCRIPT),'source_sha256':sha(HERE/'source.json'),'engine_sha256':sha(engine),'engine_harness_sha256':sha(ROOT/'generate/runs/current/check-engine.rs'),'independent_parser_sha256':sha(ROOT/'generate/runs/current/ode-scalar-parser.py')}
    save('validation.json',report)
    # Complete side-by-side text with fixed solutions, not only previews.
    lines=['# IVP recognition review','',f'Basis 1356; generator {g.VERSION}. All originals below are evidence-only raw replays.']
    for i,r in enumerate(originals):
        sid=r['generation']['source_ids'][0]
        lines += ['',f'## Original {sid}',g.markdown(r)]
        for variant in review[2*i:2*i+2]:lines += ['',f'### Generated observed-recipe variant, seed {variant["generation"]["seed"]}',g.markdown(variant)]
    for r in review[22:]:lines += ['',f'## Authored {r["question"][":question/difficulty"].rsplit("/",1)[1]}, seed {r["generation"]["seed"]}',g.markdown(r)]
    lines += ['','## Minimal domain-wording repair of q-96987','Only the third system\'s initial point changes from 0 to 2. Higher-order distractors and the boolean bank remain unchanged.',g.markdown(repaired)]
    (HERE/'review.md').write_text('\n\n'.join(lines)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','source_fidelity','finite_semantic_catalog','native_grading','independent_printed_system_checks')},indent=2))
if __name__=='__main__':main()
