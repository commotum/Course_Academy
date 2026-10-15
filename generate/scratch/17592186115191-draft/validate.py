#!/usr/bin/env python3
"""Read actual displayed cotangent mathematics and every source operative stage."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('cotangent_draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=g.PARSER.X

def baseline():
 original=D.with_name('17592186115191');paths=[original.with_suffix('.py')]+sorted(original.rglob('*'))
 actual=[{'path':str(p),'kind':'directory' if p.is_dir() else 'file','bytes':p.stat().st_size if p.is_file() else None,'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None} for p in paths]
 expected=json.loads((D/'registration-baseline.json').read_text())['paths']
 # Baseline uses repository-relative paths; validation also works with absolute invocation.
 root=D.resolve().parents[2]
 for row in actual:
  try:row['path']=str(Path(row['path']).resolve().relative_to(root))
  except ValueError:pass
 assert actual==expected,'Registered numeric script/evidence/cache tree changed'
 return {'paths':len(actual),'files':sum(r['kind']=='file' for r in actual),'unchanged':True}

def formula(prompt):
 m=re.search(r'\$(?:[fg]\(x\)|y)\s*=\s*(.*?)\$',prompt,re.S);assert m,prompt
 return g.PARSER.expression(m[1].strip().rstrip('.'))
def point(prompt):
 m=re.search(r"\$\{f\}\^\{'\}\((.*?)\)\$",prompt,re.S);assert m,prompt
 return g.PARSER.expression(m[1])
def rows(solution):
 blocks=[]
 for b in re.findall(r'\$\$(.*?)\$\$',solution,re.S):
  b=re.sub(r'\\(?:begin|end)\{aligned\}','',b);out=[]
  for row in b.split(r'\\'):
   if row.strip():
    assert '&' in row and '=' in row,row
    lhs,rhs=row.split('&',1);out.append((lhs.strip(),rhs.strip().removeprefix('=').strip()))
  blocks.append(out)
 return blocks

def row_value(raw):
 op=r'\frac{\text{d}}{\text{d}x}'
 if op in raw:
  assert raw.startswith(op),raw
  return sp.diff(g.PARSER.expression(raw[len(op):]),X)
 return g.PARSER.expression(raw)

def shape(raw,sid,a):
 # Normalize ONLY numeric coefficient slots and the documented unit omissions;
 # order, parentheses, factors, fractions, formal operands and row structure stay.
 raw=re.sub(r'\s+','',raw)
 if sid in ('q-340597','q-340599'):raw=re.sub(r'(?<![0-9])\d+(?=(?:x|ln|\\operatorname\{ln\}|cot|\\operatorname\{cot\}))','',raw)
 elif sid in ('q-31355','q-340598','q-340603'):raw=re.sub(r'(?<![0-9])\d+(?=(?:x|cot|\\operatorname\{cot\}|\{csc\}))','',raw)
 return re.sub(r'\d+','#',raw)
def observed_shapes(sid):
 s=g.QS[sid].get(':question/worked-solution') or g.authored_solution(sid,g.ANCHORS[sid]['a'])
 return [[shape(rhs,sid,g.ANCHORS[sid]['a']) for lhs,rhs in b] for b in rows(g.FMT.normalize_prose(s))]

def mathcheck(record):
 q=record['question'];sid=record['generation']['template'];a=record['generation']['parameters']['a'];f=formula(q[':question/problem']);d=sp.diff(f,X);endpoint=point(q[':question/problem']) if sid=='q-31288' else None
 assert not f.has(sp.zoo,sp.nan,sp.oo)
 # Check the actual requested order/name/argument and the supported supplied
 # function independently of the later derivative values.
 query=re.findall(r'\$([^$]*)\$',q[':question/problem'])[0]
 original_query=re.findall(r'\$([^$]*)\$',g.QS[sid][':question/problem'])[0]
 assert g.FMT.normalize_tex(query)==g.FMT.normalize_tex(original_query),(sid,'first derivative query changed')
 assert g.eq(f,g.expressions(sid,record['generation']['parameters'])[0]),(sid,'printed given differs from bounded family')
 for term in f.atoms(sp.cot,sp.tan,sp.sin,sp.cos,sp.csc,sp.sec,sp.log,sp.exp):assert term.args==(X,),(sid,'unsupported inner argument',term)
 blocks=rows(q[':question/worked-solution']);counts={'q-17639':[3],'q-31279':[3],'q-31288':[3,3],'q-31355':[3],'q-105309':[3],'q-340595':[3],'q-340597':[3],'q-340598':[3],'q-340599':[4],'q-340603':[3],'q-1913':[3]}
 assert [len(b) for b in blocks]==counts[sid]
 assert [[shape(rhs,sid,a) for lhs,rhs in b] for b in blocks]==observed_shapes(sid),(sid,blocks,observed_shapes(sid))
 for n,b in enumerate(blocks):
  expected=d.subs(X,endpoint) if n==1 and endpoint is not None else d
  for lhs,rhs in b:assert g.eq(row_value(rhs),expected),(sid,rhs,row_value(rhs),expected)
 if endpoint is not None:
  assert sp.sin(endpoint)!=0 and not f.subs(X,endpoint).has(sp.zoo,sp.nan,sp.oo)
  supplied=re.search(r'Then, we substitute \$x=(.*?)\$',q[':question/worked-solution'])[1]
  assert g.eq(g.PARSER.expression(supplied),endpoint)
  first_lhs=blocks[1][0][0];arg=re.search(r"\{f\}\^\{'\}\((.*)\)",first_lhs)[1]
  assert g.eq(g.PARSER.expression(arg),endpoint)
 # Derivative order and argument stay the actual source first derivative in x.
 assert r'\frac{\text{d}}{\text{d}x}' in blocks[0][0][1]
 for text in [q[':question/problem'],q[':question/worked-solution']]+[ans[':answer/value'] for fld in q[':question/answer-fields'] for ans in fld[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
  assert text.count('$')%2==0 and text.count('{')==text.count('}'),text
  assert '@@' not in text
  chunks=re.findall(r'\$\$.*?\$\$|\$[^$]*\$',text,re.S) if '$' in text else [text]
  assert all('+-' not in chunk and '--' not in chunk for chunk in chunks),(sid,text)
 fld=q[':question/answer-fields'][0];values=[g.PARSER.expression(ans[':answer/value']) for ans in fld[':answer-field/choices']]
 if fld[':answer-field/type']==':answer-field.type/blank':
  token='{{'+fld[':answer-field/key']+'}}';assert token in q[':question/problem'];v=fld[':answer-field/choices'][0][':answer/value'];context=q[':question/problem'].split('\n\n',1)[1].replace(token,'('+v+')')
  if sid in ('q-340599','q-340603'):
   tab=[line.split('|') for line in context.splitlines() if line.startswith('|')];assert len(tab)==3
   numerator=tab[0][3].replace('$','');denominator=tab[2][3].replace('$','')
   actual=g.PARSER.expression(numerator)/g.PARSER.expression(denominator)
  else:actual=g.PARSER.expression(context.replace('$','').replace('\n','').split('=',1)[1])
  assert g.eq(actual,d.subs(X,endpoint) if endpoint is not None else d),(sid,context,actual,d)
 else:
  assert len(values)==5
  assert all(not g.eq(v,w) for n,v in enumerate(values) for w in values[n+1:])
  correct=[ans for ans,v in zip(fld[':answer-field/choices'],values) if g.eq(v,d)]
  assert len(correct)==1 and correct[0][':answer/id']==fld[':answer-field/correct'][1]
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 return sum(map(len,blocks))

def faithful(record,original):
 q=record['question']
 for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (key in q)==(key in original),(original[':question/math-academy-id'],key)
 for key in (':question/problem',':question/worked-solution',':question/difficulty'):
  if key in original:assert q[key]==g.strip_db(original[key]),(original[':question/math-academy-id'],key,q[key],original[key])
 for fld,source in zip(q.get(':question/answer-fields',[]),original.get(':question/answer-fields',[])):
  assert fld[':answer-field/key']==source[':answer-field/key'] and fld[':answer-field/type']==g.strip_db(source[':answer-field/type'])
  assert sorted(a[':answer/value'] for a in fld[':answer-field/choices'])==sorted(a[':answer/value'] for a in source[':answer-field/choices'])
  assert (':answer-field/correct' in fld)==(':answer-field/correct' in source)
  if ':answer-field/correct' in source:assert next(a[':answer/value'] for a in fld[':answer-field/choices'] if a[':answer/id']==fld[':answer-field/correct'][1])==source[':answer-field/correct'][':answer/value']

def grader_checks(record):
 sid=record['generation']['template'];a=record['generation']['parameters']['a'];fld=record['question'][':question/answer-fields'][0]
 if fld[':answer-field/type']==':answer-field.type/radio':
  checks=[{'submitted_answer_id':ans[':answer/id'],'expected':'accepted' if ans[':answer/id']==fld[':answer-field/correct'][1] else 'rejected','purpose':'every owned radio choice'} for ans in fld[':answer-field/choices']]
  checks += [{'submitted':'foreign-answer-uuid','expected':'unresolved','purpose':'foreign radio identity'},{'submitted':fld[':answer-field/choices'][0][':answer/value'],'expected':'unresolved','purpose':'math text is not radio identity'},{'submitted':'{{malformed','expected':'unresolved','purpose':'malformed radio'}]
 else:
  canonical=fld[':answer-field/choices'][0][':answer/value'];v=g.PARSER.expression(canonical)
  equivalents={'q-31288':f'{a}*4','q-31355':rows(record['question'][':question/worked-solution'])[0][1][1],'q-340595':r'\frac{'+r'{e}^{x}\sin^{2}(x)+'+str(a)+r'}{\sin^{2}(x)}','q-340597':r'\frac{\cot(x)}{x/'+str(a)+'}','q-340598':r'\csc^{2}(x)('+str(a)+'x)','q-340599':r'\ln(x)('+str(a)+'x)','q-340603':r'\csc^{2}(x)('+str(a)+'x)'}
  equivalent=equivalents[sid];assert g.eq(g.PARSER.expression(equivalent),v)
  checks=[{'submitted':canonical,'expected':'accepted','purpose':'canonical blank'},{'submitted':equivalent,'expected':'accepted','purpose':'genuine algebraic equivalent blank'},{'submitted':g.tex(v+1),'expected':'rejected','purpose':'ordinary wrong plus one'},{'submitted':'foreign-answer-uuid','expected':'unresolved','purpose':'foreign text blank'},{'submitted':r'\frac{','expected':'unresolved','purpose':'malformed blank'}]
 return checks

def rejected_mutation(r,old,new,label):
 bad=copy.deepcopy(r);q=bad['question'];assert old in q[':question/worked-solution'];q[':question/worked-solution']=q[':question/worked-solution'].replace(old,new,1)
 try:mathcheck(bad)
 except (AssertionError,ValueError):return label
 raise AssertionError('Mutation survived '+label)

def main():
 before=baseline();review=[];cases=[];native=[];stages=0;total=0;unique=set();counts={};mutations=[]
 for sid in g.QS:
  level=g.LEVELS[sid];anchor=g.ANCHORS[sid];original=g.generate(level,template=sid,parameters=anchor,profile='observed-'+sid);faithful(original,g.QS[sid]);normal=g.generate(level,template=sid,parameters=anchor);mathcheck(normal)
  cases.append({'source_id':sid,'difficulty':level,'template':sid,'parameters':anchor,'bank_profile':'observed-'+sid})
  changed=[];observed=[];completed_variants=[];completed_anchor=None;count=0
  for p in g.domain(sid):
   r=g.generate(level,template=sid,parameters=p);stages+=mathcheck(r);count+=1;total+=1;unique.add(r['generation']['mathematical_fingerprint'])
   raw=g.generate(level,template=sid,parameters=p,profile='observed-'+sid)
   for rf in raw['question'].get(':question/answer-fields',[]):
    vals=[g.PARSER.expression(ans[':answer/value']) for ans in rf[':answer-field/choices']]
    assert all(not g.eq(v,w) for n,v in enumerate(vals) for w in vals[n+1:])
    matches=[ans for ans,v in zip(rf[':answer-field/choices'],vals) if g.eq(v,g.expressions(sid,p)[2])]
    assert len(matches)==1,(sid,p,'historical key inference not unique')
    if ':answer-field/correct' in rf:assert matches[0][':answer/id']==rf[':answer-field/correct'][1]
   if len(changed)<2 and p!=anchor:changed.append(r);observed.append(raw)
   native.append({'label':sid+':'+json.dumps(p,sort_keys=True),'record':r,'checks':grader_checks(r)})
   if raw['question'][':question/id']!=r['question'][':question/id']:
    for rf in raw['question'].get(':question/answer-fields',[]):
     if rf[':answer-field/type']==':answer-field.type/radio' and ':answer-field/correct' in rf:native.append({'label':'observed-'+sid+':'+json.dumps(p,sort_keys=True),'record':raw,'checks':grader_checks(raw)})
  if sid=='q-17639':
   for p in g.domain(sid):
    completed=g.generate(level,template=sid,parameters=p,profile='completed-observed-q-17639');mathcheck(completed)
    assert completed['generation']['evidence_only'] and not completed['generation']['eligible_for_learning']
    native.append({'label':'completed-observed-'+sid+':'+json.dumps(p,sort_keys=True),'record':completed,'checks':grader_checks(completed)})
    if p==anchor:completed_anchor=completed
    elif len(completed_variants)<2:completed_variants.append(completed)
  counts[sid]=count
  review.append({'source_id':sid,'original':original,'normal_at_original_parameters':normal,'generated_variants':changed,'observed_profile_variants':observed,'completed_historical_anchor':completed_anchor,'completed_historical_variants':completed_variants})
  rs=rows(normal['question'][':question/worked-solution'])[0];old=rs[0][1]
  mutations.append(rejected_mutation(normal,old,old.replace('x','2x',1),sid+':wrong formal operand, unchanged final'))
  mutations.append(rejected_mutation(normal,rs[1][1],rs[-1][1],sid+':erased source stage, equal value'))
  control=copy.deepcopy(normal);control['question'][':question/problem']+='\x0c'
  try:mathcheck(control)
  except (AssertionError,ValueError):pass
  else:raise AssertionError('Control character accepted')
 # Test stale prompt target and stale fixed blank context separately.
 hard=copy.deepcopy(next(x['normal_at_original_parameters'] for x in review if x['source_id']=='q-31288'));hard['question'][':question/problem']=hard['question'][':question/problem'].replace(r'\frac{\pi }{6}',r'\frac{\pi }{4}',1)
 try:mathcheck(hard)
 except (AssertionError,ValueError):mutations.append('stale hard evaluation target rejected')
 else:raise AssertionError('Stale evaluation target survived')
 order=copy.deepcopy(next(x['normal_at_original_parameters'] for x in review if x['source_id']=='q-31279'))
 order['question'][':question/problem']=order['question'][':question/problem'].replace('f^{′}(x)','f^{′′}(x)',1)
 try:mathcheck(order)
 except (AssertionError,ValueError):mutations.append('changed requested derivative order rejected')
 else:raise AssertionError('Wrong requested derivative order survived')
 for sid in g.QS:
  for invalid in (True,1.0,'1',0,-1,25):
   try:g.generate(g.LEVELS[sid],template=sid,parameters={'a':invalid})
   except ValueError:pass
   else:raise AssertionError('Invalid parameter accepted '+repr(invalid))
  r1=g.generate(g.LEVELS[sid],seed=1,template=sid,parameters=g.ANCHORS[sid]);r2=g.generate(g.LEVELS[sid],seed=91,template=sid,parameters=g.ANCHORS[sid]);assert r1['question'][':question/id']==r2['question'][':question/id']
 default={}
 for level in ('easy','moderate','hard'):
  seen={g.generate(level,seed=n)['generation']['template'] for n in range(32)};assert seen=={sid for sid in g.QS if g.LEVELS[sid]==level};default[level]=sorted(seen)
 (D/'native-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n');subprocess.run([str(D/'reference/check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 nr=json.loads((D/'native-report.json').read_text());after=baseline();assert before==after
 inventory={k:g.SOURCE[k] for k in ('database','basis','lineage')}|{'questions':[{'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Existing registered-generator hard coefficient variant of MA q-31288; explicit whole-number answer field and flattened aligned presentation. Current inventory only, not recovered MA difficulty/template evidence.'} for q in g.KP[':knowledge-point/questions'] if ':question/math-academy-id' not in q]}
 result={'status':'passed','source_basis':2275,'source_records':len(g.QS),'raw_full_prompt_solution_presence_matches':len(g.QS),'source_choice_banks':sum(bool(q.get(':question/answer-fields')) for q in g.QS.values()),'source_values':sum(len(f[':answer-field/choices']) for q in g.QS.values() for f in q.get(':question/answer-fields',[])),'completed_historical_evidence_native_instances':23,'source_existing_correct_refs':sum(':answer-field/correct' in f for q in g.QS.values() for f in q.get(':question/answer-fields',[])),'independent_inventory_records':len(inventory['questions']),'normal_finite_domain_instances':total,'normal_domain_counts':counts,'canonical_mathematical_tasks':len(unique),'displayed_stages_checked':stages,'default_family_coverage_seeds_0_to_31':default,'mutations':mutations,'native':{k:v for k,v in nr.items() if k!='records'},'registered_baseline_preservation':after,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'limits':['Raw missing original fields, keys, ratings and solutions are preserved and evidence-only.','q-17639 and q-1913 historical banks have unresolved wrong-operation intent; bounded replay remains evidence-only and authored method banks serve normal sampling.','Hard keeps pi/6 and negative coefficient1..24, with the original derivative, substitution, familiar csc value and squaring stages. No additional trigonometric chain rule.']}
 for name,obj in [('source-cases.json',cases),('review.json',review),('independent-inventory.json',inventory),('validation.json',result)]: (D/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
 lines=['# Cotangent differentiation review','Original MA evidence, normal completion at its anchor, and two changed variants of EACH profile. Independent inventory is separately captured.']
 for r in review:
  lines+=['## '+r['source_id'],'### Original MA evidence',g.markdown(r['original']),'### Normal minimal completion at original parameters',g.markdown(r['normal_at_original_parameters'])]
  if r['completed_historical_anchor'] is not None:lines+=['### Authored key/solution completion of opaque historical bank, evidence-only',g.markdown(r['completed_historical_anchor'])]
  for key,label in [('observed_profile_variants','Generated observed-profile evidence variant'),('generated_variants','Generated normal variant'),('completed_historical_variants','Generated completed-historical evidence variant')]:
   for n,v in enumerate(r[key]):lines+=['### '+label+' '+str(n+1)+' '+json.dumps(v['generation']['parameters']),g.markdown(v)]
 (D/'review.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
