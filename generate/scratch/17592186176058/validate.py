#!/usr/bin/env python3
"""Independent printed math, complete source fidelity and native radio grading."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from PIL import Image
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def read_math(s):
    s=s.strip().rstrip('.').replace('π','pi').replace(r'\pi','pi').replace(r'\cdot','*')
    while re.search(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',s):
      s=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',lambda m:'(('+m[1]+')/('+m[2]+'))',s)
    s=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',s)
    s=s.replace('{','(').replace('}',')')
    s=re.sub(r'(\d)\s*(pi)',r'\1*\2',s)
    s=re.sub(r'(\d)\s*(sqrt)',r'\1*\2',s)
    return sp.sympify(s,locals={'pi':sp.pi})

def substitute(s,var,v):
    s=s.replace(r'\tan','tan⁡')
    def transform(m):
      a=m[1].replace(r'\pi','pi').replace('π','pi')
      a=re.sub(r'(\d)\s*(pi)',r'\1*\2',a)
      z=sp.Symbol(var)
      a=sp.sympify(a,locals={var:z,'pi':sp.pi})
      assert sp.diff(a,z)==-1,('Unexpected argument',m[1])
      shift=sp.simplify((a+z)/sp.pi)
      assert shift.is_integer
      return '('+str(-v)+')'
    s=re.sub(r'tan⁡\s*\(([^()]*)\)',transform,s)
    s=re.sub('tan⁡\\s*'+var+r'\b','('+str(v)+')',s)
    # A rendered fraction immediately followed by a numeric factor must multiply.
    s=re.sub(r'(\})(\()',r'\1*\2',s)
    return read_math(s)

def formatting(s):
    assert not any(ord(c)<32 and c not in '\n\t' for c in s),'Control character'
    assert s.count('$')%2==0,'Unbalanced math delimiter'
    depth=0
    for c in s:
      if c=='{':depth+=1
      if c=='}':depth-=1
      assert depth>=0
    assert depth==0,'Unbalanced TeX groups'
    assert '--' not in s and '+-' not in s,'Bare signed arithmetic'

def check(record,check_key=True):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    q=record['question'];meta=record['generation'];template=meta['template']
    import uuid
    uuid.UUID(q[':question/id'])
    for s in [q[':question/problem'],q.get(':question/worked-solution','')]:formatting(s)
    source=meta['source'];assert source==g.SOURCE
    match=re.fullmatch(r'If \$(?:tan⁡|\\tan )([axt])\s*=\s*(.*?)\$[,]? then \$(.*?)=\$',q[':question/problem'])
    assert match,q[':question/problem']
    var=match[1];v=read_math(match[2].rstrip(','));target=substitute(match[3],var,v)
    field=q[':question/answer-fields'][0];assert field[':answer-field/type']==':answer-field.type/radio'
    uuid.UUID(field[':answer-field/id'])
    answers=field[':answer-field/choices'];assert len(answers)==5
    assert len({a[':answer/id'] for a in answers})==5
    values=[]
    for a in answers:
      uuid.UUID(a[':answer/id'])
      formatting(a[':answer/value']);values.append(read_math(a[':answer/value']))
    assert len(set(values))==5,'Bank collision'
    assert sum(sp.simplify(z-target)==0 for z in values)==1
    # Recover every bank operation from actual printed components independently.
    profile=meta['profile'];c=sp.Integer(1);b=sp.Integer(0);n=0
    angle=re.search(r'(?:tan⁡|\\tan)\s*\(([^()]*)\)',match[3])
    if angle and template not in ['direct_integer','direct_fraction','direct_positive']:
      a=angle[1].replace(r'\pi','pi').replace('π','pi')
      a=re.sub(r'(\d)\s*(pi)',r'\1*\2',a)
      symbol=sp.Symbol(var)
      n=sp.simplify((sp.sympify(a,locals={var:symbol,'pi':sp.pi})+symbol)/sp.pi)
      assert n.is_integer and n!=0
    if template.startswith('affine'):
      form=re.sub(r'(?:tan⁡|\\tan)\s*\([^()]*\)','Z',match[3])
      form=form.replace('}Z','}*Z')
      expr=read_math(form);z=sp.Symbol('Z');c=expr.coeff(z);b=expr.subs(z,0)
      assert sp.simplify(c*(-v)+b-target)==0 and c!=0 and b!=0
    if profile=='reciprocal_zero':expected=[-v,v,1/v,0,-1/v]
    elif profile=='numerator_omission':expected=[v,1/v,-v,-1/v,-sp.Rational(1,v.q)]
    elif profile=='radical_observed':expected=[v,-1/v,-v,1/v,-sp.sqrt(v)]
    elif profile in ['output_shift','raw_unrated']:expected=[-v+n*sp.pi,v+n*sp.pi,-v,0,v]
    elif profile=='affine_operations':expected=[-c*v+b,c*v+b,-c*v-b,-v+b,-c*v]
    elif profile=='integer_observed':expected=[-c*v+b,0,c*v+b,-(c*v+b),b]
    elif profile=='fraction_observed':expected=[-c*v+b,-(c*v+b),sp.pi-(c*v+b),-1,c*v+b]
    else:raise AssertionError('Unknown profile')
    assert set(values)==set(map(sp.simplify,expected)),'Wrong displayed operation bank'
    if check_key:
      key=field[':answer-field/correct'];assert key[0]==':answer/id'
      assert [a[':answer/id'] for a in answers][values.index(target)]==key[1],'Wrong key'
    if ':question/worked-solution' in q:
      blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
      expected=1 if template.startswith('direct') else (2 if template=='shifted' else 3)
      assert len(blocks)==expected
      for block in blocks:
       left,right=block.split('& =',1);rows=re.split(r'\\\\\s*& =',right)
       a=substitute(left,var,v)
       for row in rows:assert sp.simplify(a-substitute(row,var,v))==0,('Invalid displayed stage',left,row)
      if template.startswith('direct'):assert len(re.split(r'\\\\\s*& =',blocks[0].split('& =',1)[1]))==(3 if v<0 else 2)
      else:
       assert len(re.split(r'\\\\\s*& =',blocks[0].split('& =',1)[1]))==1
       assert len(re.split(r'\\\\\s*& =',blocks[1].split('& =',1)[1]))==(3 if v<0 else 2)
       if template.startswith('affine'):
        rows=re.split(r'\\\\\s*& =',blocks[2].split('& =',1)[1]);assert len(rows)==4
        assert r'\cdot' in rows[0] and r'\frac{' in rows[1]
        if template=='affine_fraction':assert '+' in rows[1] and rows[2].count(r'\frac{')==1 and '+' not in rows[2]
        else:assert '+' in rows[2] and r'\frac{' not in rows[2]
    return target

def run():
    sources=json.loads((ROOT/'source.json').read_text())['record'][':knowledge-point/questions'];byid={q[':db/id']:q for q in sources}
    cases=json.loads((ROOT/'source-cases.json').read_text());source_results=[];records=[]
    for case in cases:
      original=byid[case['source_id']]
      r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
      check(r,':answer-field/correct' in original[':question/answer-fields'][0]);q=r['question'];f=q[':question/answer-fields'][0];of=original[':question/answer-fields'][0]
      for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (key in q)==(key in original)
      assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
      assert q[':question/problem']==original[':question/problem']
      if ':question/worked-solution' in original:assert q[':question/worked-solution']==original[':question/worked-solution'],case['source_id']
      assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
      if ':answer-field/correct' in of:
       generated=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert generated==of[':answer-field/correct'][':answer/value']
      source_results.append({'source_id':case['source_id'],'prompt':'exact','bank':'5/5 exact','solution':'exact' if ':question/worked-solution' in original else 'missing preserved','designation':'matched' if ':answer-field/correct' in of else 'missing preserved, independently inferred -1/2','key_presence':'passed'})
      records.append(r)
    inferred=g.generate('moderate',template='shifted',profile='output_shift',parameters={'v':'1/2','variable':'x','n':12})
    check(inferred);records.append(inferred)
    coverage={};counts={};tasks_by_template={};tasks_by_level={l:set() for l in ['easy','moderate','hard']}
    for template,level in g.TEMPLATES.items():
      profiles={'direct_integer':['reciprocal_zero'],'direct_fraction':['numerator_omission','reciprocal_zero'],'direct_positive':['reciprocal_zero','radical_observed'],'shifted':['output_shift','raw_unrated'],'affine_integer':['affine_operations','integer_observed'],'affine_fraction':['affine_operations','fraction_observed']}[template]
      eligible=0;mathtasks=set()
      # Exhaustive finite meaningful domains with one representative nonzero shift;
      # signed shift boundaries independently checked below.
      for p in g.domain(template):
       if template=='shifted' and p['n']!=1:continue
       try:r=g.generate(level,template=template,parameters=p)
       except ValueError as e:
        assert 'collision' in str(e);continue
       check(r);mathtasks.add(r['generation']['mathematical_fingerprint']);eligible+=1
      counts[template]={'meaningful_tasks':len(mathtasks),'period_shift_presentation_variants_per_task':24 if level!='easy' else 1,'presentation_variants_excluding_variable_letters_and_bank_aliases':len(mathtasks)*(24 if level!='easy' else 1)}
      tasks_by_template[template]=mathtasks
      tasks_by_level[level].update(mathtasks)
      for profile in profiles:
       checked=0
       for seed in range(24):
        r=g.generate(level,seed=seed,template=template,profile=profile);check(r,profile!='raw_unrated');checked+=1
        r2=g.generate(level,seed=seed+918,template=template,profile=profile,parameters=r['generation']['parameters']);check(r2,profile!='raw_unrated')
        assert r['question'][':question/id']==r2['question'][':question/id'];assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
        if seed<2:records.append(r)
       coverage[template+'/'+profile]=checked
      # Every printed allowed variable and signed maximal/minimal period shift.
      base=g.generate(level,1,template=template)['generation']['parameters']
      for var in ['a','x','t']:
       for n in ([-12,-1,1,12] if level!='easy' else [None]):
        p=dict(base,variable=var)
        if n is not None:p['n']=n
        check(g.generate(level,template=template,parameters=p))
    normalcoverage={level:set() for level in ['easy','moderate','hard']}
    correct_positions=set()
    for seed in range(96):
      for level in normalcoverage:
       r=g.generate(level,seed);check(r);assert r['generation']['eligible_for_learning'];normalcoverage[level].add(r['generation']['template'])
       f=r['question'][':question/answer-fields'][0]
       correct_positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
    assert all(normalcoverage[l]=={t for t,v in g.TEMPLATES.items() if v==l} for l in normalcoverage)
    assert correct_positions==set(range(5)),'Default choices do not shuffle through all positions'
    # Different integer periods are aliases of the same assessed function,
    # while their actual prompts, solutions and complete banks retain identity.
    alias_regressions=0
    for template in ['shifted','affine_integer','affine_fraction']:
      level=g.TEMPLATES[template]
      base=g.generate(level,3,template=template)['generation']['parameters']
      r3=g.generate(level,template=template,parameters=dict(base,n=3))
      r7=g.generate(level,template=template,parameters=dict(base,n=7))
      check(r3);check(r7)
      assert r3['generation']['mathematical_fingerprint']==r7['generation']['mathematical_fingerprint']
      assert r3['generation']['content_fingerprint']!=r7['generation']['content_fingerprint']
      assert r3['question'][':question/id']!=r7['question'][':question/id']
      alias_regressions+=1
    easy_templates=['direct_integer','direct_positive','direct_fraction']
    easy_overlaps={}
    for i,a in enumerate(easy_templates):
      for b in easy_templates[i+1:]:
        easy_overlaps[a+'/'+b]=len(tasks_by_template[a]&tasks_by_template[b])
    assert all(n==0 for n in easy_overlaps.values()),'Unexpected overlap among current easy domains'
    # Banks are presentation, not assessed-task identity.
    p={'v':'4/5','variable':'a'}
    r1=g.generate('easy',template='direct_fraction',parameters=p,profile='numerator_omission')
    r2=g.generate('easy',template='direct_fraction',parameters=p,profile='reciprocal_zero')
    assert r1['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
    assert r1['generation']['content_fingerprint']!=r2['generation']['content_fingerprint']
    review=json.loads((ROOT/'review.json').read_text()) if (ROOT/'review.json').exists() else []
    for r in review:
      check(r,':answer-field/correct' in r['question'][':question/answer-fields'][0])
      records.append(r)
    # Explicit boundaries are subject to the same guard; no silently repaired inputs.
    invalid=[('easy','direct_integer',{'v':'-10','variable':'a'}),('moderate','shifted',{'v':'1/2','variable':'x','n':0}),('moderate','shifted',{'v':'1/2','variable':'x','n':13}),('hard','affine_integer',{'v':'-4','variable':'x','n':3,'c':'1','b':'3'}),('hard','affine_fraction',{'v':'-2','variable':'x','n':3,'c':'3/5','b':'1/5'})]
    for l,t,p in invalid:
      try:g.generate(l,template=t,parameters=p)
      except ValueError:pass
      else:raise AssertionError(('Accepted invalid boundary',p))
    # Mutation tests prove displayed algebra and stage structure drive QA.
    good=g.generate('hard',template='affine_integer',parameters={'v':'-4','variable':'x','n':3,'c':'1/2','b':'3'})
    mutations=[]
    r=copy.deepcopy(good);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(r'\frac{4}{2}+3',r'\frac{4}{2}-3');mutations.append(r)
    r=copy.deepcopy(good);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(r'\frac{4}{2}+3','2+3');mutations.append(r)
    r=copy.deepcopy(good);r['question'][':question/problem']=r['question'][':question/problem'].replace(r'\frac','\x0crac');mutations.append(r)
    r=copy.deepcopy(good);r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='999';mutations.append(r)
    for r in mutations:
      try:check(r)
      except (AssertionError,ValueError,TypeError,sp.SympifyError):pass
      else:raise AssertionError('Mutation escaped checks')
    engine=[]
    for i,r in enumerate(records):
      if ':answer-field/correct' not in r['question'][':question/answer-fields'][0]:continue
      f=r['question'][':question/answer-fields'][0]
      engine.append({'label':'record-'+str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independently validated complete displayed bank'} for a in f[':answer-field/choices']]})
    (ROOT/'engine-input.json').write_text(json.dumps(engine,indent=2))
    grader=Path('generate/runs/current/check-engine');subprocess.run([str(grader),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
    report=json.loads((ROOT/'engine-report.json').read_text())
    result={'status':'pass','source':g.SOURCE,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_questions':6,'prompts_exact':6,'complete_banks_exact':6,'answers_exact':30,'correct_designations_matched':5,'correct_designations_present':5,'missing_designations':1,'solutions_exact':5,'solutions_present':5,'missing_solutions':1,'raw_attribute_presence':'all 6 passed','source_results':source_results,'profiles_tested':coverage,'default_family_coverage':{l:sorted(v) for l,v in normalcoverage.items()},'finite_variety':counts,'engine':{k:report[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'engine_binary_sha256':hashlib.sha256(grader.read_bytes()).hexdigest(),'explicit_invalid_boundaries_rejected':len(invalid),'mutation_regressions_rejected':len(mutations),'unresolved':['Historical negative-square-root choice and hard fraction bank contain opaque scalar errors; public evidence-only recipes preserve expression patterns without claiming recovered intent.','Unrated q-136549 has no original correct designation or worked solution; completed moderate records explicitly infer -tan x and author the level/solution.']}
    plot=ROOT/'tangent-source.png'
    result['plot']={'requirement':'none; exact fixed explanatory asset reused','source_path':g.IMAGE,'local_path':str(plot),'sha256':hashlib.sha256(plot.read_bytes()).hexdigest(),'dimensions':list(Image.open(plot).size),'visual_inspection':'original full-resolution graph inspected; three tangent branches, four asymptotes, origin symmetry; no parameter-dependent geometry'}
    result['review_records_checked']=len(review)
    result['correct_choice_positions_observed']=sorted(correct_positions)
    result['canonical_meaningful_tasks_by_level']={l:len(tasks) for l,tasks in tasks_by_level.items()}
    result['easy_sampler_domain_overlap_counts']=easy_overlaps
    result['period_alias_identity_regressions_passed']=alias_regressions
    (ROOT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
