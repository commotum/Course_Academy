"""Independent displayed calculus, source-stage fidelity, API and native-grader QA."""
import hashlib, importlib.util, json, re, subprocess, sys, platform
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load(HERE.with_suffix('.py'),'draft64204')
reader=load(HERE/'math_parser.py','private64204reader')
x,u,C=reader.x,reader.u,reader.z
DER=r'\frac{\text{d}}{\text{d}x}'
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n')
def group(text, start):
    op = text[start]; close = {'[':']', '(' : ')', '{':'}'}[op]
    depth = 1; end = start+1
    while depth:
        assert end < len(text)
        depth += (text[end] == op) - (text[end] == close); end += 1
    return text[start+1:end-1], end

def scalar(text):
    text = text.strip().rstrip('.,').replace('✓', '').replace('C', 'z')
    while DER in text:
        at = text.index(DER)
        arg, end = group(text, at+len(DER))
        d = sp.diff(scalar(arg), x)
        text = text[:at] + '(' + sp.latex(d) + ')' + text[end:]
    return reader.scalar(text)

def equal(a, b):
    return sp.cancel(a-b) == 0

def value(text, affine):
    text = text.strip().rstrip('.,').replace('✓', '')
    if r'\int ' in text:
        prefix, body = text.split(r'\int ', 1)
        # A missing differential is never silently accepted in production.
        match = re.search(r'\\text\{d\}([ux])$', body)
        assert match, ('missing differential', text)
        var = u if match[1] == 'u' else x
        body = body[:match.start()].replace(r'\,', '').strip()
        if body.endswith(r'\cdot'): body = body[:-len(r'\cdot')]
        prefix = prefix.strip()
        if prefix.endswith(r'\cdot'): prefix = prefix[:-len(r'\cdot')].strip()
        coeff = sp.Integer(-1 if prefix == '-' else 1) if prefix in ('','-','+') else scalar(prefix)
        body_expr=scalar(body)
        if var==x:
            slope=sp.diff(affine,x);intercept=affine.subs(x,0)
            transformed=sp.cancel(body_expr.subs(x,(u-intercept)/slope))
            power=transformed.as_powers_dict().get(u,0);factor=sp.cancel(transformed/u**power)
            assert not factor.has(u) and power!=-1
            expr=coeff*factor/((power+1)*slope)*affine**(power+1)
        else:
            transformed=sp.cancel(body_expr);power=transformed.as_powers_dict().get(u,0);factor=sp.cancel(transformed/u**power)
            assert not factor.has(u) and power!=-1
            expr=coeff*factor/(power+1)*u**(power+1)
    else:
        expr = scalar(text)
    return expr.subs(u, affine)

def displayed_parameters(q):
 text=q[':question/problem']
 mat=re.search(r'\\frac\{(-?\d+)\}\{\(([^()]+)\)\^\{(\d+)\}\}',text)
 if mat:
  n=int(mat[1]);n=-n if text[mat.start()-1:mat.start()]=='-' else n
  L=scalar(mat[2]);m=int(mat[3])
 else:
  mat=re.search(r'\(1\)/\(\(([^()]+)\)\^\{8\}\)',text);assert mat,text
  n,L,m=1,scalar(mat[1]),8
 poly=sp.Poly(L,x);assert poly.degree()==1
 return [n,int(poly.coeff_monomial(x)),int(poly.coeff_monomial(1)),m]

def check(r):
 meta,q=r['generation'],r['question'];p=displayed_parameters(q);assert p==meta['parameters']
 assert r==g.generate(q[':question/difficulty'].split('/')[-1],meta['seed'],template=meta['template'],parameters=p,profile=meta['profile'],field_type=meta['field_type'])
 assert set(r)=={'knowledge_point','question','generation'} and set(r['knowledge_point'])=={'db_id','id','title'}
 n,a,b,m=p;L=a*x+b;integrand=sp.cancel(n/L**m)
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 bank=f[':answer-field/choices'];assert len(bank)==5
 choices=[scalar(v[':answer/value']) for v in bank];ds=[sp.cancel(sp.diff(v,x)) for v in choices]
 assert len(set(ds))==5,('modulo C duplicate',meta)
 ci=[i for i,o in enumerate(bank) if o[':answer/id']==f[':answer-field/correct'][1]];assert len(ci)==1
 assert equal(ds[ci[0]],integrand)
 assert all(not equal(d,integrand) for i,d in enumerate(ds) if i!=ci[0])
 assert meta['mathematical_fingerprint']==g.fingerprint(p)
 assert r['knowledge_point']['id']==g.KP_UUID
 sol=q[':question/worked-solution']
 sub=re.search(r'Let \$u=([^$]+)\.\$',sol);assert sub and equal(scalar(sub[1]),L)
 jac=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=(-?\d+)',sol);assert jac and int(jac[1])==a
 dx=re.search(r'⟹\\,\\text\{d\}x=(.*?)\\text\{d\}u',sol);assert dx
 assert equal(scalar(dx[1]) if dx[1] not in ('','-') else sp.Integer(-1 if dx[1]=='-' else 1),sp.Rational(1,a))
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==4
 assert equal(sp.diff(value(blocks[0],L),x),integrand)
 stages=[]
 for index,block in enumerate(blocks[2:]):
  block=block.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
  rs=block.split(r'\\');stages.append(rs)
  for row in rs:
   for expression in row.split('& ='):
    if not expression.strip():continue
    val=value(expression,L)
    assert equal(sp.diff(val,x),integrand) if index==0 else equal(val,integrand),(meta,expression,val,integrand)
 if meta['role'] in ('authored','legacy-repair'):
  assert [len(rs) for rs in stages]==[6,5]
  # Read ordered formal operands from the displayed row: replacement before
  # integration, separate factors before collection, unevaluated power division,
  # back-substitution, reciprocal rewrite, and chain-rule factors in that order.
  r0,r1,r2,r3,r4,r5=stages[0];d0,d1,d2,d3,d4=stages[1]
  assert r'\int {u}' in r0 and r'\cdot' in r0 and r'\text{d}u' in r0
  assert r1.count(r'\cdot')==1 and r'\int {u}' in r1
  assert r'\int {u}' in r2 and r'\cdot' not in r2
  assert rf'\frac{{{{u}}^{{-{m-1}}}}}{{(-{m-1})}}' in r3
  assert g.affine(a,b) in r4 and r'\int' not in r4
  assert r'\frac' in r5 and 'u' not in r5
  assert d0.count(DER)==3 and d1.count(DER)==2
  assert d2.count(r'\cdot')==3 and DER+'('+g.affine(a,b)+')' in d2
  assert d3.count(r'\cdot')==3 and DER not in d3
 return {'template':meta['template'],'parameters':p,'stages':stages,'ordered_row_counts':[len(z) for z in stages]}

def native(label,r):
 f=r['question'][':question/answer-fields'][0];correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
 checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct[':answer/id'] else 'rejected','purpose':'field-owned radio ID'} for a in f[':answer-field/choices']]
 checks +=[{'submitted':correct[':answer/value'],'expected':'unresolved','purpose':'malformed radio transport: math text instead of selected field-owned ID'},{'submitted':'('+correct[':answer/value']+')','expected':'unresolved','purpose':'malformed radio transport: equivalent math text instead of selected field-owned ID'},{'submitted':'0','expected':'unresolved','purpose':'ownership failure: nonexistent radio choice ID'}]
 return {'label':label,'record':r,'checks':checks}

def main():
 source=json.loads((HERE/'source.json').read_text());qs={q.get(':question/math-academy-id',str(q[':db/id'])):q for q in source['record'][':knowledge-point/questions']};cases=json.loads((HERE/'source-cases.json').read_text())
 assert source['basis']==2275
 audits=[];replay=[];records=[];review=[];inputs=[];recipes={}
 for case in cases:
  sid=case['source_id'];old=qs[sid]
  rec=g.generate(case['level'],13,template=sid,parameters=case['parameters']);audits.append(check(rec));records.append(rec);inputs.append(native(sid,rec))
  if case['complete']:
   t=g.PROFILES[sid];new=rec['question'];f=new[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
   assert new[':question/problem']==g.fmt.normalize_prose(old[':question/problem'])
   sol=old[':question/worked-solution'];correction=t['source_correction']
   if correction:sol=sol.replace(correction['old'].replace('@@L@@',t['affine']),correction['new'].replace('@@L@@',t['affine']))
   assert new[':question/worked-solution']==g.fmt.normalize_prose(sol)
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(g.fmt.normalize_tex(a[':answer/value']) for a in of[':answer-field/choices'])
   cv=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert cv==g.fmt.normalize_tex(of[':answer-field/correct'][':answer/value'])
   replay.append({'source':sid,'role':case['role'],'choices_matched':5,'distractors_matched':4,'correct_designation_matched':True,'prompt_exact':new[':question/problem']==old[':question/problem'],'solution_raw_exact':new[':question/worked-solution']==old[':question/worked-solution'],'solution_full_normalized_and_supported_repair':True,'correction':correction})
   n,a,b,m=case['parameters'];recipes[sid]=[]
   for o in t['bank']:
    e=sp.cancel((scalar(o['source_value'])-C).subs(x,(u-b)/a));power=e.as_powers_dict()[u];coeff=sp.cancel(e/u**power)
    recipes[sid].append({**o,'coefficient':str(coeff),'power':str(power),'recipe':'coefficient*(a*x+b)^power+C','interpretation':'observed full algebraic pattern; misconception intent unresolved'})
   for bb in (t['bounds'][0],t['bounds'][1]):
    p=list(case['parameters']);p[2]=bb;r=g.generate(case['level'],27,template=sid,parameters=p);audits.append(check(r));records.append(r);inputs.append(native(sid+' '+str(bb),r))
    assert r['question'][':question/worked-solution']==g.fmt.normalize_prose(t['solution'].replace('@@L@@',g.affine(p[1],bb)))
   variant=g.generate(case['level'],29,template=sid,parameters=[*case['parameters'][:2],t['bounds'][0] if t['bounds'][0]!=case['parameters'][2] else t['bounds'][1],case['parameters'][3]])
  else:
   raw=g.generate('easy',13,template='q-12499-raw',parameters=case['parameters']);rf=raw['question'][':question/answer-fields'][0]
   assert sorted(a[':answer/value'] for a in rf[':answer-field/choices'])==sorted(g.fmt.normalize_tex(a[':answer/value']) for a in rf[':answer-field/choices'])
   # Mathematical one-to-one source replay despite original plain fraction notation.
   oldvalues=[scalar(v[':answer/value']) for v in old[':question/answer-fields'][0][':answer-field/choices']]
   newvalues=[scalar(v[':answer/value']) for v in rf[':answer-field/choices']]
   for v in oldvalues:
    match=next(i for i,w in enumerate(newvalues) if equal(v,w));newvalues.pop(match)
   assert not newvalues
   ds=[sp.diff(v,x) for v in oldvalues];assert len(set(ds))==3
   save('legacy-raw-reference.json',raw)
   variant=g.generate('easy',29,template=sid,parameters=[1,1,-12,8])
  review.append('## '+sid+' ('+case['role']+')\n\nOriginal\n\n'+old[':question/problem']+'\n\n'+old.get(':question/worked-solution','[No source solution]')+'\n\nServed parameterized replay\n\n'+g.markdown(rec)+'\n\nChanged intercept\n\n'+g.markdown(variant))
 for level in g.LEVELS:
  pool=g.domain(level);distinct={g.fingerprint(p) for p in pool};assert len(distinct)>100
  # Endpoints of each slot plus seeded independent draws, all rendered readbacks.
  chosen=[pool[0],pool[-1]]
  for slot in range(4):
   for value_ in sorted({p[slot] for p in pool}):chosen.append(next(p for p in pool if p[slot]==value_))
  chosen.extend(r['generation']['parameters'] for r in g.batch(level,15,37))
  seen=set()
  for p in chosen:
   if tuple(p) in seen:continue
   seen.add(tuple(p));r=g.generate(level,41,parameters=p);audits.append(check(r));records.append(r);inputs.append(native(level+str(p),r))
  preview=g.batch(level,3,2275);save('preview-'+level+'.json',preview);(HERE/('preview-'+level+'.md')).write_text('\n\n---\n\n'.join(map(g.markdown,preview)))
  review.append('## Authored '+level+'\n\n'+'\n\n---\n\n'.join(map(g.markdown,preview[:2])))
  # Strict input, bounds, finite capacity, stable identity independent of option order.
  for bad in (True,1.0,'1',None):
   for field in ('seed','count'):
    try:g.batch(level,**{field:bad})
    except (TypeError,ValueError):pass
    else:raise AssertionError((field,bad))
  for bad in ([True,*pool[0][1:]],[*pool[0][:2],0,pool[0][3]],[*pool[0][:3],1]):
   try:g.generate(level,parameters=bad)
   except (TypeError,ValueError):pass
   else:raise AssertionError(bad)
  try:g.batch(level,len(distinct)+1)
  except ValueError:pass
  else:raise AssertionError('capacity overflow')
  a=g.generate(level,0,parameters=pool[0]);b=g.generate(level,99,parameters=pool[0]);assert a['question'][':question/id']==b['question'][':question/id']
  batch=g.batch(level,40,17);assert len({r['generation']['mathematical_fingerprint'] for r in batch})==40
 cli=json.loads(subprocess.check_output([sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--count','3'],text=True));assert len(cli)==9 and all('question' in q for q in cli)
 # Equal displayed content across original/independent profiles owns identical
 # answers even when the captured bank orders differed.
 left=g.generate('moderate',0,template='q-12019',parameters=[3,-3,5,3])
 right=g.generate('moderate',0,template='17592186483548',parameters=[3,-3,5,3])
 assert left['question']==right['question']
 save('review.json',records);(HERE/'review.md').write_text('\n\n'.join(review));save('displayed-stage-audit.json',audits);save('bank-recipes.json',recipes);save('engine-input.json',inputs)
 engine=HERE/'check-engine';sha=hashlib.sha256(engine.read_bytes()).hexdigest();assert sha=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 baseline=json.loads((HERE/'registered-baseline.json').read_text());assert all(Path(p).is_file() and hashlib.sha256(Path(p).read_bytes()).hexdigest()==v for p,v in baseline.items());assert set(baseline)=={str(p) for p in [Path('generate/scratch/17592186064204.py'),*Path('generate/scratch/17592186064204').rglob('*')] if p.is_file()}
 capacity={level:{'parameter_tuples':len(g.domain(level)),'actual_distinct_integrands':len({g.fingerprint(p) for p in g.domain(level)})} for level in g.LEVELS};save('capacity.json',capacity)
 report={'status':'pass; pending independent root approval','basis':2275,'registered_files_preserved':len(baseline),'ma_complete_originals':8,'ma_complete_banks':8,'ma_complete_choices':40,'ma_distractors':32,'ma_correct_designations':8,'ma_incomplete_reference':{'source':'q-12499','full_raw_mathematical_bank_replayed':5,'unique_mod_C_values':3,'original_correct_designation':'absent; derived correct is authored','normal_repaired_duplicates':2,'solution':'authored missing solution','level':'authored easy'},'independent_complete_banks':2,'independent_choices':10,'source_replays':replay,'rendered_math_records_checked':len(audits),'native_genuine_math_unresolved_limits':0,'native_malformed_or_ownership_probes':3*len(inputs),'engine_sha256':sha,'engine':json.loads((HERE/'engine-report.json').read_text()),'capacity':capacity,'runtime':{'python':platform.python_version(),'sympy':sp.__version__},'limits':['No observed hard source label; hard is a conservative same-method design claim.','Legacy source has no correct designation or solution and duplicate primitive options; cannot claim original correctness/solution fidelity.','Observed coefficient/exponent distractor intent is unresolved; only intercept slots are used for those banks.','Radio fields assess selected field-owned IDs; algebraic string equivalence is inapplicable to native response contract.']}
 save('validation.json',report)
 print(json.dumps({k:v for k,v in report.items() if k not in ('engine','source_replays')},indent=2))
if __name__=='__main__':main()
