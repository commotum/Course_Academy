#!/usr/bin/env python3
"""Independent checks read actual rendered strings; native grading is separate."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)

def expr(tex):
 s=tex.replace('_{⏟}','').replace(r'\,','').replace(r'\cdot','*').replace('{','').replace('}','').strip().rstrip('.')
 return parse_expr(s,transformations=TRANS,local_dict={v:sp.Symbol(v) for v in ('x','y','z')})

def assert_format(text):
 assert all(ord(c)>=32 or c in '\n\t' for c in text),'C0 control byte'
 assert text.count('$')%2==0,'math delimiters'
 depth=0
 for c in text:
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0,'closing brace'
 assert depth==0,'unclosed brace'
 assert '+-' not in text and '--' not in text,'signed concatenation'


def displayed(record,allow_raw=False):
 q=record['question'];raw=record['generation']['evidence_only']
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 strings=[q[':question/problem']]+([q[':question/worked-solution']] if ':question/worked-solution' in q else [])
 for f in q.get(':question/answer-fields',[]):strings += [a[':answer/value'] for a in f.get(':answer-field/choices',[])]
 for s in strings:assert_format(s)
 first=re.findall(r'\$([^$]+)\$',q[':question/problem'])[0]
 target=sp.expand(expr(first));symbols=target.free_symbols;assert len(symbols)==1
 v=next(iter(symbols));h=-target.coeff(v)/2;c=target.coeff(v,0);r=c-h*h
 assert target.coeff(v,2)==1 and h>0 and h.is_Integer
 p={'v':str(v),'h':int(h),'c':int(c)}
 if not raw:g.guard(p,record['generation']['difficulty'],record['generation']['template'])
 # All stages parsed from actual Markdown; each equals the displayed polynomial.
 if ':question/worked-solution' in q:
  solution=q[':question/worked-solution'];rows=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S)
  assert len(rows)==4,'four teaching stages'
  for row in rows:assert sp.expand(expr(row)-target)==0,('invalid displayed stage',row)
  clean=[row.replace('{','').replace('}','') for row in rows]
  assert '-2\\cdot '+str(h)+str(v) in clean[0],'decompose into 2 times half'
  assert '+'+str(h)+'^2' in clean[1] and '-\\,'+str(h)+'^2' in clean[1],'add then subtract square before factor'
  assert '('+str(v)+'-'+str(h)+')^2' in clean[2] and '-'+str(h)+'^2' in clean[2],'factor before evaluating'
  assert clean[3].rstrip('.')=='('+str(v)+'-'+str(h)+')^2'+g.signed(r),'final collected constant'
  if 'Therefore' in solution:
   match=re.search(r'Therefore, \$p=(-?\d+)\$ and \$q=(-?\d+)\.\$',solution);assert match,'complete p/q conclusion'
   op=-1 if '('+str(v)+'-p' in q[':question/problem'] else 1
   assert int(match[1])==(-h if op==1 else h) and int(match[2])==r,'stale final prose'
 fields=q.get(':question/answer-fields',[])
 for f in fields:
  kind=f[':answer-field/type'];assert kind in (':answer-field.type/radio',':answer-field.type/blank')
  key=f[':answer-field/key'];vals=f.get(':answer-field/choices',[])
  if kind.endswith('/blank'):assert '{{'+key+'}}' in q[':question/problem'],'blank placeholder'
  if ':answer-field/correct' not in f:
   assert raw and allow_raw,'normal missing correct ref'
   if not kind.endswith('/radio'):continue
  correct=f.get(':answer-field/correct')
  if correct:
   assert len(correct)==2 and correct[0]==':answer/id'
   assert sum(a[':answer/id']==correct[1] for a in vals)==1,'correct owned'
   correct_value=next(a[':answer/value'] for a in vals if a[':answer/id']==correct[1])
  if kind.endswith('/radio'):
   objects=[];eligibility=[]
   for a in vals:
    value=a[':answer/value']
    if value.startswith('p'):
     pair=re.search(r'p\s*=\s*(-?\d+).*q\s*=\s*(-?\d+)',value);assert pair
     pv,qv=map(int,pair.groups());op=-1 if '('+str(v)+'-p' in q[':question/problem'] else 1
     objects.append((pv,qv));eligibility.append(sp.expand((v+op*pv)**2+qv-target)==0)
    else:
     obj=sp.expand(expr(value));objects.append(obj);eligibility.append(sp.expand(obj-target)==0)
   assert len(set(objects))==len(objects),'ambiguous bank'
   assert sum(eligibility)==1,'exactly one valid option'
   if correct:assert eligibility[next(i for i,a in enumerate(vals) if a[':answer/id']==correct[1])],'correct designation wrong'
  elif 'what are the values' in q[':question/problem']:
   op=-1 if '('+str(v)+'-p' in q[':question/problem'] else 1
   expected=(-h if op==1 else h) if key=='field-1' else r
   assert expr(correct_value)==expected
  else:assert sp.expand(expr(correct_value)-(v-h if key=='field-1' else abs(r)))==0
 if fields and all(f[':answer-field/type'].endswith('/blank') and ':answer-field/correct' in f for f in fields):
  values={f[':answer-field/key']:next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]) for f in fields}
  if 'what are the values' not in q[':question/problem']:
   assert sp.expand(expr(values['field-1'])**2+(1 if '=(${{field-1}}${)}^{2}\\,+' in q[':question/problem'] else -1)*expr(values['field-2'])-target)==0,'inserted fragments'
 return p


def fidelity():
 stats={'sources':0,'exact_prompts':0,'exact_present_solutions':0,'present_solutions':0,'complete_banks':0,'bank_choices':0,'distractors':0,'matched_correct_refs':0,'present_correct_refs':0,'missing_correct_refs':0,'missing_banks':0,'unrated':0,'fieldless':0}
 records=[];cases=[]
 for sid,case in g.CASES.items():
  r=g.generate(case['level'],profile='source:'+sid);q=r['question'];src=g.QUESTIONS[sid];displayed(r,True)
  for k in (':question/difficulty',':question/answer-fields',':question/worked-solution'):
   assert (k in q)==(k in src),(sid,'attribute presence',k)
  assert q[':question/problem']==src[':question/problem'];stats['exact_prompts']+=1
  if ':question/worked-solution' in src:
   assert q[':question/worked-solution']==src[':question/worked-solution'];stats['exact_present_solutions']+=1;stats['present_solutions']+=1
  else:assert ':question/worked-solution' not in q
  stats['unrated']+=int(':question/difficulty' not in src);stats['fieldless']+=int(':question/answer-fields' not in src)
  for sf in src.get(':question/answer-fields',[]):
   f=next(f for f in q[':question/answer-fields'] if f[':answer-field/key']==sf[':answer-field/key'])
   assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
   for k in (':answer-field/choices',':answer-field/correct'):assert (k in f)==(k in sf),(sid,k)
   if ':answer-field/choices' in sf:
    assert sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in sf[':answer-field/choices'])
    stats['bank_choices']+=len(sf[':answer-field/choices']);stats['complete_banks']+=1
    if f[':answer-field/type'].endswith('/radio'):stats['distractors']+=len(f[':answer-field/choices'])-1
   else:stats['missing_banks']+=1
   if ':answer-field/correct' in sf:
    stats['present_correct_refs']+=1
    a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
    assert a[':answer/value']==sf[':answer-field/correct'][':answer/value'];stats['matched_correct_refs']+=1
   else:stats['missing_correct_refs']+=1
  stats['sources']+=1;records.append(r)
  cases.append({'source_id':sid,'template':case['template'],'level':case['level'],'parameters':r['generation']['parameters'],'bank_profile':'source:'+sid,'authored_level_assignment':sid in ('q-235904','q-25253')})
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False)+'\n')
 return stats,records


def expect_failure(fn):
 try:fn()
 except (AssertionError,ValueError):return
 raise AssertionError('mutation or invalid explicit input was accepted')


def check_identity(records):
 for r in records:
  gen=r['generation'];kwargs={'template':gen['template'],'profile':gen['profile'],'parameters':gen['parameters']}
  if not gen['evidence_only']:kwargs['field_type']=r['question'][':question/answer-fields'][0][':answer-field/type']
  other=g.generate(gen['difficulty'],97,**kwargs)
  assert other['question'][':question/id']==r['question'][':question/id'],'seed changed identity'
  assert other['generation']['mathematical_fingerprint']==gen['mathematical_fingerprint']
 q=copy.deepcopy(next(r['question'] for r in records if not r['generation']['evidence_only'] and r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio')))
 f=q[':question/answer-fields'][0];base=g.uid('question',g.identity_payload(q))
 f[':answer-field/choices'].reverse();assert g.uid('question',g.identity_payload(q))==base
 f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])]
 assert g.uid('question',g.identity_payload(q))!=base,'correct value omitted from identity'
 del f[':answer-field/correct'];assert g.uid('question',g.identity_payload(q))!=base,'correct presence omitted from identity'
 q2=copy.deepcopy(q);del q2[':question/answer-fields'];assert g.identity_payload(q)!=g.identity_payload(q2)
 q2=copy.deepcopy(q);q2[':question/worked-solution']+=' ';assert g.identity_payload(q)!=g.identity_payload(q2)
 q2=copy.deepcopy(q);q2[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+=' ';assert g.identity_payload(q)!=g.identity_payload(q2)


def native_item(label,r):
 checks=[];p=displayed(r,True)
 for i,f in enumerate(r['question'].get(':question/answer-fields',[])):
  if ':answer-field/correct' not in f:return None
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete radio bank native selection'})
  else:
   value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);v=p['v'];h=p['h'];c=p['c']
   # A visibly unreduced alternate, not a simplified identical entry.
   alternate=(v+'-'+str(h+1)+'+1') if v in value else ('('+value+'-1)+1')
   if v in value:checks.append({'field_index':i,'submitted':str(h)+'-'+v,'expected':'rejected','purpose':'opposite binomial does not equal required fragment; normal positive-coefficient convention'})
   for submitted,expected,purpose in [(value,'accepted','canonical blank'),(alternate,'accepted','unreduced equivalent blank'),(str(expr(value)+1),'rejected','incorrect shifted blank')]:
    checks.append({'field_index':i,'submitted':submitted,'expected':expected,'purpose':purpose})
 return {'label':label,'record':r,'checks':checks} if checks else None


def main():
 stats,raw=fidelity();generated=[];coverage={};native=[]
 for level,templates in g.TEMPLATES.items():
  for template,kind in itertools.product(templates,['radio','blank']):
   for seed in range(30):
    r=g.generate(level,seed,template,kind);displayed(r);generated.append(r)
    if seed<3:native.append(native_item(level+'/'+template+'/'+kind+'/'+str(seed),r))
  coverage[level]={'tested_records':sum(r['generation']['difficulty']==level for r in generated),'default_templates':sorted({g.generate(level,seed)['generation']['template'] for seed in range(100)})}
 for sid,r in zip(g.CASES,raw):
  item=native_item(sid,r)
  if item:native.append(item)
 # Complete anomalies separately; these inferred fields/keys never count as raw matches.
 repaired=[]
 for sid in ('q-235904','q-25253','q-141615'):
  case=g.CASES[sid];r=g.generate(case['level'],template=case['template'],parameters={k:v for k,v in case.items() if k not in ('level','template')},field_type='blank' if sid=='q-235904' else 'radio')
  repaired.append(r);native.append(native_item('completed:'+sid,r))
 # Parameterized nonliteral raw replay remains a real API instance.
 for sid,case in g.CASES.items():
  p={k:v for k,v in case.items() if k not in ('level','template')};p['h']+=2 if sid=='q-3662' else (1 if p['h']<12 else -1)
  if 'opaque' in p:p['opaque']=[n+1 for n in p['opaque']]
  changed=g.generate(case['level'],profile='source:'+sid,parameters=p)
  # Historical opaque profiles can collide under supplied components; check all
  # nonopaque profiles' complete mathematical banks and all four displayed stages.
  displayed(changed,True)
 check_identity(raw+generated+repaired)
 base=next(r for r in generated if r['generation']['difficulty']=='hard')
 for where in ('prompt','solution','answer'):
  bad=copy.deepcopy(base)
  if where=='prompt':bad['question'][':question/problem']+='\x0c'
  elif where=='solution':bad['question'][':question/worked-solution']+='\x0c'
  else:bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+='\x0c'
  expect_failure(lambda:displayed(bad))
 bad=copy.deepcopy(base);rows=re.findall(r'\$\$\n(.*?)\n\$\$',bad['question'][':question/worked-solution'],re.S)
 bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(rows[0],rows[0].replace('-2\\cdot','+2\\cdot'));expect_failure(lambda:displayed(bad))
 # Algebraically equal replacement removes the operative add/subtract stage.
 bad=copy.deepcopy(base);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(rows[1],rows[3]);expect_failure(lambda:displayed(bad))
 # Stale final conclusion and fragment output are independently caught.
 bad=copy.deepcopy(base);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('Therefore, $p=','Therefore, $p=1');expect_failure(lambda:displayed(bad))
 for level in g.TEMPLATES:
  for kind in ('radio','blank',':answer-field.type/radio',':answer-field.type/blank'):displayed(g.generate(level,14,field_type=kind))
 for level,c in [('easy',0),('moderate',-1),('hard',0)]:expect_failure(lambda level=level,c=c:g.generate(level,parameters={'v':'x','h':5,'c':c}))
 expect_failure(lambda:g.generate('hard',parameters={'v':'x','h':2,'c':-5}))
 for kwargs in [dict(field_type='checkbox'),dict(template='nonsense'),dict(profile='nonsense'),dict(parameters={'v':'x','h':-5,'c':30}),dict(parameters={'v':'x','h':13,'c':30})]:expect_failure(lambda kwargs=kwargs:g.generate('moderate',**kwargs))
 (HERE/'native-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n')
 engine=HERE.parents[1]/'runs/current/check-engine'
 subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 report=json.loads((HERE/'native-report.json').read_text())
 summary={'status':'passed','source':stats,'generated_checked':len(generated),'coverage':coverage,'native':{k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'completed_source_anomalies':3,
 'mutations_rejected':['C0_prompt','C0_solution','C0_answer','distributed_sign','equal_but_collapsed_add_subtract','stale_conclusion','correct_ref_identity_value_and_presence'],
 'finite_meaningful_polynomial_counts':{'easy':1716,'moderate':1728,'hard':600},'task_count_convention':'Distinct monic even-negative polynomials excluding zero residual; variable aliases, bank/layout and p-sign convention aliases excluded. Radio h=1 excluded by bank collisions; blank supports it.',
 'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'native_binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'basis':1356,'database_writes':0,
 'unresolved_findings':['Historical q-141611 and q-141612 scalar distractor intentions are opaque; public raw profiles are evidence-only and never default sampling. Missing source correct designations (3 fields) cannot count as matched.']}
 (HERE/'validation.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
 # Review every observed source/template/bank plus two changed normal variants,
 # and two independent instances of each authored hard convention.
 review=[];text=['# Review: basis 1356','Raw replay preserves source attributes and strings. Generated variants are labeled separately.']
 for sid,r in zip(g.CASES,raw):
  text+=['\n## '+sid+' — raw original evidence',g.markdown(r)];review.append({'label':sid+' raw evidence','record':r})
  case=g.CASES[sid]
  changedp={k:v for k,v in case.items() if k not in ('level','template')}
  changedp['h']+=2 if sid=='q-3662' else (1 if changedp['h']<12 else -1)
  if 'opaque' in changedp:changedp['opaque']=[n+1 for n in changedp['opaque']]
  evidence_variant=g.generate(case['level'],seed=73,profile='source:'+sid,parameters=changedp)
  review.append({'label':sid+' changed-parameter raw-profile evidence (ineligible)','record':evidence_variant})
  text+=['\n### Changed-parameter original profile — evidence only, raw omissions retained',g.markdown(evidence_variant)]
  for seed in (21,37):
   variant=g.generate(case['level'],seed,case['template']);review.append({'label':sid+' authored method bank variant '+str(seed),'record':variant});text+=['\n### Generated variant '+str(seed)+' — authored complete method bank',g.markdown(variant)]
 for template in g.TEMPLATES['hard']:
  for seed in (21,37):
   r=g.generate_hard(seed,template);review.append({'label':'hard authored '+template+' '+str(seed),'record':r});text+=['\n## Hard authored '+template+' '+str(seed),g.markdown(r)]
 for sid,r in zip(('q-235904','q-25253','q-141615'),repaired):review.append({'label':'completed anomaly '+sid,'record':r})
 (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n');(HERE/'review.md').write_text('\n\n'.join(text)+'\n')
 print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
