#!/usr/bin/env python3
"""Independent displayed-expression, every-stage, source and frozen-native checks."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
D=Path(__file__).parent
s=importlib.util.spec_from_file_location('secant_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
X=g.PARSER.X

def formula(prompt):
 m=re.search(r'\$y\s*=\s*(.*?)\$',prompt,re.S)
 assert m,prompt
 return g.PARSER.expression(m[1].strip().rstrip('.'))
def rhs_rows(solution):
 out=[]
 for block in re.findall(r'\$\$(.*?)\$\$',solution,re.S):
  block=re.sub(r'\\(?:begin|end)\{aligned\}','',block)
  rows=[]
  for row in block.split(r'\\'):
   if row.strip():
    assert '&' in row and '=' in row,row
    rows.append(row.split('&',1)[1].strip().removeprefix('=').strip())
  out.append(rows)
 return out

def row_value(raw):
 op=r'\frac{\text{d}}{\text{d}x}'
 if op in raw:
  # Parse each ordered formal D operand, rather than ignoring the first row.
  assert raw.startswith(op),raw
  return sp.diff(g.PARSER.expression(raw[len(op):]),X)
 endpoint=False
 for end in [r'\,{|}_{x=0}',r'{|}_{x=0}']:
  if raw.endswith(end):raw=raw[:-len(end)];endpoint=True;break
 val=g.PARSER.expression(raw)
 return val.subs(X,0) if endpoint else val

def skeleton(raw,sid):
 # Compare operative source structure, not just equal values or row counts.
 raw=re.sub(r'\s+','',raw)
 if sid=='q-340620':raw=re.sub(r'(?<![0-9])\d+(?=\{e\})','',raw)
 return re.sub(r'\d+','#',raw)

def source_shapes(sid):
 original=g.QS[sid].get(':question/worked-solution')
 if original is None:
  original=g.authored_solution(sid,g.ANCHORS[sid],g.expressions(sid,g.ANCHORS[sid])[1])
 return [[skeleton(row,sid) for row in block] for block in rhs_rows(g.FMT.normalize_prose(original))]

def mathcheck(record):
 q=record['question'];sid=record['generation']['template'];f=formula(q[':question/problem']);d=sp.diff(f,X)
 assert not f.has(sp.zoo,sp.nan,sp.oo)
 blocks=rhs_rows(q[':question/worked-solution'])
 # Source row counts and structural stages are contractual, independently of equality.
 counts={'q-1892':[2],'q-31280':[3],'q-1883':[4],'q-1938':[5],'q-337182':[6],'q-104325':[4],'q-105314':[3],'q-105316':[2],'q-340608':[2],'q-340611':[3],'q-340620':[2,4]}
 assert [len(b) for b in blocks]==counts[sid],(sid,blocks)
 observed_shapes=source_shapes(sid)
 actual_shapes=[[skeleton(row,sid) for row in block] for block in blocks]
 if sid=='q-340611' and record['generation']['parameters']['a']!='e':
  expected_solution=g.QS[sid][':question/worked-solution'].replace('{e}','{2}').replace(' & ={2}^{x}sec⁡(x)+',' & ={2}^{x}'+r'\ln 2'+'sec⁡(x)+').replace('(1+tan⁡(x))','('+r'\ln 2'+'+tan⁡(x))')
  observed_shapes=[[skeleton(row,sid) for row in block] for block in rhs_rows(g.FMT.normalize_prose(expected_solution))]
 assert actual_shapes==observed_shapes,(sid,actual_shapes,observed_shapes)
 for n,block in enumerate(blocks):
  expected=d.subs(X,0) if sid=='q-340620' and n==1 else d
  for row in block:assert g.eq(row_value(row),expected),(sid,row,row_value(row),expected)
 if sid=='q-1938':
  assert r'\frac{(' in blocks[0][1] and ')(' in blocks[0][1] and r'^{2}' in blocks[0][1]
  assert r'\frac{' in blocks[0][2] and r'\operatorname' in blocks[0][2] or r'\sec' in blocks[0][2]
  assert '(x' in blocks[0][3],blocks[0][3]
 if sid=='q-337182':
  assert ')(' in blocks[0][1] and r'\frac{(' not in blocks[0][2]
  assert 'x' in blocks[0][3] and '(' in blocks[0][3] and '(' in blocks[0][4] and '(' in blocks[0][5]
 if sid=='q-104325':assert ')(' in blocks[0][1] and '(' in blocks[0][2] and '(' in blocks[0][3]
 if sid in ('q-105314','q-340611'):assert '+' in blocks[0][1] and '(' in blocks[0][2]
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for fld in q[':question/answer-fields'] for a in fld[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
  assert text.count('$')%2==0 and text.count('{')==text.count('}'),text
  assert '@@' not in text and '+-' not in text and '--' not in text
 fld=q[':question/answer-fields'][0];vals=[g.PARSER.expression(a[':answer/value']) for a in fld[':answer-field/choices']]
 if fld[':answer-field/type']==':answer-field.type/blank':
  assert '{{'+fld[':answer-field/key']+'}}' in q[':question/problem']
  full=q[':question/problem'].split('\n\n',1)[1]
  full=full.replace('{{'+fld[':answer-field/key']+'}}','('+fld[':answer-field/choices'][0][':answer/value']+')').replace('$','').replace('\n','')
  expected=d.subs(X,0) if sid=='q-340620' else d
  assert g.eq(g.PARSER.expression(full.split('=',1)[1]),expected),(sid,full)
 else:
  expected=d
  assert len(vals)==5
  assert all(not g.eq(v,w) for n,v in enumerate(vals) for w in vals[n+1:])
  correct=[a for a,v in zip(fld[':answer-field/choices'],vals) if g.eq(v,expected)]
  assert len(correct)==1 and correct[0][':answer/id']==fld[':answer-field/correct'][1]
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 return len([v for b in blocks for v in b])

def faithful(record,original):
 q=record['question']
 for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
  assert (key in q)==(key in original),(original[':question/math-academy-id'],key)
 for key in (':question/problem',':question/worked-solution',':question/difficulty'):
  if key in original:assert q[key]==g.strip_db(original[key]),(key,q[key],original[key])
 for generated,source in zip(q.get(':question/answer-fields',[]),original.get(':question/answer-fields',[])):
  assert generated[':answer-field/key']==source[':answer-field/key']
  assert generated[':answer-field/type']==g.strip_db(source[':answer-field/type'])
  assert sorted(a[':answer/value'] for a in generated[':answer-field/choices'])==sorted(a[':answer/value'] for a in source[':answer-field/choices'])
  assert (':answer-field/correct' in generated)==(':answer-field/correct' in source)
  if ':answer-field/correct' in source:
   assert next(a[':answer/value'] for a in generated[':answer-field/choices'] if a[':answer/id']==generated[':answer-field/correct'][1])==source[':answer-field/correct'][':answer/value']

def main():
 originals=[];review=[];native=[];source_cases=[];stages=0;total=0;unique=set();counts={};rejections=0
 for sid in g.QS:
  level=g.LEVELS[sid];raw=g.generate(level,template=sid,profile='observed-'+sid,parameters=g.ANCHORS[sid]);faithful(raw,g.QS[sid]);originals.append(raw)
  source_cases.append({'source_id':sid,'template':sid,'level':level,'parameters':g.ANCHORS[sid],'bank_profile':'observed-'+sid})
  normal_anchor=g.generate(level,template=sid,parameters=g.ANCHORS[sid]);mathcheck(normal_anchor)
  changed=[];rawchanged=[];count=0
  for p in g.domain(sid):
   try:r=g.generate(level,template=sid,parameters=p)
   except ValueError as exc:
    if 'collision' not in str(exc) and 'ambiguous' not in str(exc):raise
    rejections+=1;continue
   stages+=mathcheck(r);count+=1;total+=1;unique.add(r['generation']['mathematical_fingerprint'])
   # Raw parameterized evidence also checks missing-attribute preservation away from anchor.
   rawp=g.generate(level,template=sid,profile='observed-'+sid,parameters=p)
   for rawfield in rawp['question'].get(':question/answer-fields',[]):
    rawvalues=[g.PARSER.expression(ans[':answer/value']) for ans in rawfield[':answer-field/choices']]
    assert all(not g.eq(v,w) for n,v in enumerate(rawvalues) for w in rawvalues[n+1:]),(sid,p,'historical bank collision')
    if ':answer-field/correct' in rawfield:
     cv=next(v for a,v in zip(rawfield[':answer-field/choices'],rawvalues) if a[':answer/id']==rawfield[':answer-field/correct'][1])
     assert g.eq(cv,g.expressions(sid,p)[2]),(sid,p,'historical designation wrong')
   if len(changed)<2 and p!=g.ANCHORS[sid]:changed.append(r);rawchanged.append(rawp)
   fld=r['question'][':question/answer-fields'][0]
   if fld[':answer-field/type']==':answer-field.type/radio':
    checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==fld[':answer-field/correct'][1] else 'rejected','purpose':'every field-owned choice'} for a in fld[':answer-field/choices']]
    checks += [{'submitted':'foreign-answer-uuid','expected':'unresolved','purpose':'foreign choice identity'},{'submitted':fld[':answer-field/choices'][0][':answer/value'],'expected':'unresolved','purpose':'math text is not radio identity'},{'submitted':'{{malformed','expected':'unresolved','purpose':'malformed radio submission'}]
   else:
    v=g.PARSER.expression(fld[':answer-field/choices'][0][':answer/value'])
    # Expanded equivalent differs genuinely in structure for product blanks; scalars
    # use an unreduced sum rather than simplifying back to the identical string.
    equivalent=g.tex(sp.expand(v))
    if equivalent==fld[':answer-field/choices'][0][':answer/value']:equivalent='('+fld[':answer-field/choices'][0][':answer/value']+'+1)-1'
    checks=[{'submitted':fld[':answer-field/choices'][0][':answer/value'],'expected':'accepted','purpose':'canonical blank'},{'submitted':equivalent,'expected':'accepted','purpose':'legitimate noncanonical equivalent'},{'submitted':g.tex(v+1),'expected':'rejected','purpose':'ordinary wrong exact value'},{'submitted':r'\frac{','expected':'unresolved','purpose':'malformed blank'}]
   if sid=='q-340611' and p['a'] in (4,8,9):
    check=next(c for c in checks if c['purpose']=='legitimate noncanonical equivalent')
    check['expected']='unresolved';check['purpose']='documented native log-power equivalence limit'
    checks.append({'submitted':r'\tan x+\ln '+str(p['a']),'expected':'accepted','purpose':'accepted reordered equivalent without log-power identity'})
   native.append({'label':sid+':'+json.dumps(p,sort_keys=True),'record':r,'checks':checks})
   # Distinct raw historical radio banks are engine-tested in their own profiles.
   # Raw incomplete records retain absent keys and cannot be valid grading fixtures.
   if rawp['question'][':question/id']!=r['question'][':question/id']:
    for rf in rawp['question'].get(':question/answer-fields',[]):
     if rf[':answer-field/type']==':answer-field.type/radio' and ':answer-field/correct' in rf:
      rawchecks=[{'submitted_answer_id':ans[':answer/id'],'expected':'accepted' if ans[':answer/id']==rf[':answer-field/correct'][1] else 'rejected','purpose':'every historical field-owned choice'} for ans in rf[':answer-field/choices']]
      rawchecks += [{'submitted':'foreign-answer-uuid','expected':'unresolved','purpose':'foreign historical choice identity'},{'submitted':rf[':answer-field/choices'][0][':answer/value'],'expected':'unresolved','purpose':'historical math text is not radio identity'},{'submitted':'{{malformed','expected':'unresolved','purpose':'malformed historical radio submission'}]
      native.append({'label':'observed-'+sid+':'+json.dumps(p,sort_keys=True),'record':rawp,'checks':rawchecks})
  counts[sid]=count
  review.append({'source_id':sid,'original':raw,'normal_at_original_parameters':normal_anchor,'generated_variants':changed,'observed_profile_variants':rawchanged})
 # Wrong intermediate mutation preserves final answer; row and formal-operand checks must fail.
 mutants=[]
 for r in [v['normal_at_original_parameters'] for v in review]:
  bad=copy.deepcopy(r);sol=bad['question'][':question/worked-solution'];rows=rhs_rows(sol)
  old=rows[0][0];bad['question'][':question/worked-solution']=sol.replace(old,old.replace('(3','(8',1) if '(3' in old else old.replace('x','2x',1),1)
  try:mathcheck(bad)
  except (AssertionError,ValueError):mutants.append({'template':r['generation']['template'],'formal_operand_mutation_rejected':True})
  else:raise AssertionError('Formal operand mutation survived '+r['generation']['template'])
  if len(rows[0])>2:
   bad=copy.deepcopy(r);old=rows[0][1];bad['question'][':question/worked-solution']=sol.replace(old,'('+old+')+1',1)
   try:mathcheck(bad)
   except (AssertionError,ValueError):pass
   else:raise AssertionError('Intermediate mutation survived')
 # Algebraically equal final expression cannot replace a factoring stage.
 factor=copy.deepcopy(next(v['normal_at_original_parameters'] for v in review if v['source_id']=='q-337182'))
 rs=rhs_rows(factor['question'][':question/worked-solution'])[0]
 factor['question'][':question/worked-solution']=factor['question'][':question/worked-solution'].replace(rs[3],rs[-1],1)
 try:mathcheck(factor)
 except AssertionError:pass
 else:raise AssertionError('Equal-final replacement erased source factorization stage')
 control=copy.deepcopy(review[0]['normal_at_original_parameters']);control['question'][':question/problem']+='\x0c'
 try:mathcheck(control)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('Control character accepted')
 # Strict type and key guards apply everywhere.
 for sid in g.QS:
  p=dict(g.ANCHORS[sid]);p['a']=True
  try:g.generate(g.LEVELS[sid],template=sid,parameters=p)
  except ValueError:pass
  else:raise AssertionError('bool accepted')
 for sid in g.QS:
  p=g.ANCHORS[sid];a=g.generate(g.LEVELS[sid],seed=1,template=sid,parameters=p);b=g.generate(g.LEVELS[sid],seed=2,template=sid,parameters=p)
  assert a['question'][':question/id']==b['question'][':question/id']
 input_path=D/'native-input.json';input_path.write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n')
 subprocess.run([str(D/'reference/check-engine'),str(input_path),str(D/'native-report.json')],check=True)
 native_report=json.loads((D/'native-report.json').read_text())
 result={'status':'passed','source_basis':2275,'source_records':len(originals),'raw_full_prompt_solution_and_presence_matches':len(originals),'original_complete_banks':sum(bool(q.get(':question/answer-fields')) for q in g.QS.values()),'original_values':sum(len(f[':answer-field/choices']) for q in g.QS.values() for f in q.get(':question/answer-fields',[])),'original_correct_designations':sum(':answer-field/correct' in f for q in g.QS.values() for f in q.get(':question/answer-fields',[])),'normal_finite_domain_instances':total,'normal_domain_counts':counts,'mathematical_tasks_across_profiles_and_response_roles':len(unique),'displayed_stages_checked':stages,'whole_bank_rejections':rejections,'mutations':mutants,'native':{k:v for k,v in native_report.items() if k!='records'},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'limits':['Two raw unrated originals retain missing solutions and correct refs; two source originals retain absent fields. All raw profiles are evidence-only.','Historical q-104325 and q-105316 banks have uncertain error intent, preserved by bounded algebraic replay; authored method banks serve normal practice.','Native ln(4)=2ln(2), ln(8)=3ln(2), ln(9)=2ln(3) equivalent blank entries are explicitly unresolved; canonical and reordered equivalents are accepted. No valid parameter removed.','No source plots. Hard retains fixed endpoint zero and source two-stage evaluation workload; coefficients provide finite differentiation tasks.']}
 for name,value in [('source-cases.json',source_cases),('review.json',review),('validation.json',result)]: (D/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
 lines=['# Secant differentiation review','Original evidence is labeled separately from normal completions and generated variants.']
 for item in review:
  lines+=['\n## '+item['source_id'],'\n### Original evidence',g.markdown(item['original']),'\n### Normal minimal completion at original parameters',g.markdown(item['normal_at_original_parameters'])]
  for n,v in enumerate(item['observed_profile_variants']):lines+=['\n### Generated observed-profile evidence variant '+str(n+1)+' '+json.dumps(v['generation']['parameters']),g.markdown(v)]
  for n,v in enumerate(item['generated_variants']):lines+=['\n### Generated variant '+str(n+1)+' '+json.dumps(v['generation']['parameters']),g.markdown(v)]
 (D/'review.md').write_text('\n\n'.join(lines)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
