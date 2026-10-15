#!/usr/bin/env python3
"""Additional independent stage, prose, held-slot and public-contract checks."""
import sys
sys.dont_write_bytecode=True
import importlib.util,json,re,hashlib,collections
from pathlib import Path
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('validator',D/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);m=v.m
counts=collections.Counter();native=[];render=[]
def rows(block):
 return [re.split(r'&\s*=',r)[1].split(r'\end{aligned}')[0].strip().rstrip('.') for r in block.split(r'\\') if re.search(r'&\s*=',r)]
def blocks(text):return re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S)
def prose(text):return m.re.sub(m.MATH if hasattr(m,'MATH') else v.re.compile(r'\$\$[\s\S]*?\$\$|\$[^$]*?\$'),'<MATH>',text)
def signature(rhs):
 return (r'\text{d}' in rhs,tuple('inner' if a in ('u','h') else 'restored' for a in re.findall(r'(?:\{e\}|e)\^\{([^{}]*)\}',rhs)),r'\cdot' in rhs,r'\frac' in rhs)
def verify(r):
 v.validate_record(r);q=r['question'];k=r['generation']['template'];sol=q.get(':question/worked-solution','')
 for text in [q[':question/problem'],sol,*[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]]:
  assert not any(ord(c)<32 and c not in '\n\t' for c in text)
 if not sol:return
 bs=blocks(sol);chain=rows(bs[2]);inner='h' if k in m.SPECS and m.SPECS[k][2].startswith('trig') else 'u';symbol=v.h if inner=='h' else v.u
 # Read the actual two product operands before substituting inner=g.
 operand=chain[1].split(r'\cdot');assert len(operand)==2
 components=bs[1].split(r'\,');outer=v.read(components[0].split('=',1)[1]);derivative=v.read(components[1].split('=',1)[1])
 assert v.equal(v.read(operand[0]),outer);assert v.equal(v.read(operand[1]),derivative)
 assert inner in v.read(operand[0]).free_symbols or symbol in v.read(operand[0]).free_symbols
 counts['separate_product_operands']+=2
 if k in m.SRC and ':question/worked-solution' in m.SRC[k]:
  src=m.normalize_prose(m.SRC[k][':question/worked-solution']);sb=blocks(src)
  assert prose(sol)==prose(src),'Complete shared prose changed'
  sc=rows(sb[2]);assert len(sc)==len(chain)
  # Source-specific operator/product/restoration stages; number changes may
  # change brace spelling, so inspect parsed exponential inputs separately.
  for source,row in zip(sc,chain):
   assert (r'\text{d}' in row)==(r'\text{d}' in source)
   assert (r'\cdot' in row)==(r'\cdot' in source),'Lost explicit operative multiplication'
   def exp_den(text):
    for hit in re.finditer(r'\\frac',text):
     try:
      _,end=v.group(text,hit.end());den,_=v.group(text,end)
      if re.search(r'(?:\{e\}|e)\^',den):return True
     except (AssertionError,IndexError):pass
    return False
   assert exp_den(row)==exp_den(source),'Lost reciprocal-exponential stage'
   for z in ('u','h'):
    assert bool(re.search(r'(?:\{e\}|e)\^\{'+z+r'\}',row))==bool(re.search(r'(?:\{e\}|e)\^\{'+z+r'\}',source)),'Lost exponent restoration stage'
   counts['preserved_chain_stages']+=1
  if len(bs)>3:
   erows=rows(bs[3]);assert len(erows)==len(rows(sb[3]))
   assert 'x' in erows[0] and 'x' not in erows[1],'Lost explicit substitution stage'
   assert '(' in erows[1],'Substitution operands prematurely evaluated'
   counts['preserved_evaluation_stages']+=len(erows)
  counts['complete_prose_matches']+=1
 counts['records']+=1
for level,templates in m.NORMAL.items():
 for k in templates:
  a=m.generate(level,101,template=k);b=m.generate(level,202,template=k)
  for r in (a,b):verify(r);render.append(r)
  # Seed/answer ordering and parameter spellings never define task identity.
  c=m.generate(level,999,template=k,parameters=a['generation']['parameters']);verify(c)
  assert a['question'][':question/id']==c['question'][':question/id']
  assert a['generation']['mathematical_fingerprint']==c['generation']['mathematical_fingerprint']
  # A changed held coefficient must actually alter the printed assessed task.
  assert a['generation']['mathematical_fingerprint']!=b['generation']['mathematical_fingerprint'] or a['generation']['parameters']==b['generation']['parameters']
  f=a['question'][':question/answer-fields'][0]
  if f[':answer-field/type'].endswith('/blank'):
   kind='slope' if k=='two_power_slope' else m.SPECS[k][2]
   if kind.startswith('trig'):
    prompt=a['question'][':question/problem'];scale=re.search(r'f\(h\)=(.*?)e\^h',prompt)[1];coefficient=re.search(r'h\(x\)=(.*?)\\sin x',prompt)[1]
    eq='('+scale+')('+coefficient+r'\cos x)'
    if kind=='trig_quotient':eq='-('+eq+')'
    if kind=='trig_full':eq+='e^{'+coefficient+r'\sin x}'
   else:
    prompt=a['question'][':question/problem'];g=v.read(v.exp_arg(prompt));derivative=m.latex(v.s.diff(g,v.x))
    if kind=='slope':
     t=re.search(r'where \$x=(.*?)\.\$',prompt)[1]
     derivative=derivative.replace('x','('+t+')');gtex=v.exp_arg(prompt).replace('x','('+t+')')
    else:gtex=v.exp_arg(prompt)
    eq='e^{'+gtex+'}('+derivative+')'
   assert v.equal(v.read(eq),v.read(f[':answer-field/choices'][0][':answer/value']))
   native.append({'label':'independent-unreduced-'+k,'record':a,'checks':[{'submitted':eq,'expected':'accepted','purpose':'Independent unreduced displayed chain operands, exponent and evaluation'},{'submitted':'1','expected':'unresolved' if k=='q-166076' else 'rejected','purpose':'Known wrong unit scalar; q-166076 current engine cannot establish inequivalence'}]})
# Inspect each declared numerical slot across the sampled normal catalog.
slot_values=collections.defaultdict(lambda:collections.defaultdict(set))
for r in json.loads((D/'review.json').read_text()):
 if r['generation']['evidence_only']:continue
 for key,value in r['generation']['parameters'].items():slot_values[r['generation']['template']][key].add(value)
slot_values={k:{slot:sorted(values) for slot,values in slots.items()} for k,slots in slot_values.items()}
# Generator's guard, independent from the validator's guard.
saved=m.SRC['q-1953'][':question/problem']
try:
 m.SRC['q-1953'][':question/problem']=saved+'\x0c'
 try:m.generate_easy(11,template='q-1953')
 except ValueError:counts['generator_C0_mutation_rejected']+=1
 else:raise AssertionError('Generator emitted C0 content')
finally:m.SRC['q-1953'][':question/problem']=saved
# Change one assessed coefficient while holding every other slot fixed.
held=[]
for level,k,p in [('easy','q-107445',dict(a=1,n=3,b=-2,c=0)),('moderate','q-340948',dict(a=-2,n=3,b=5,c=0,t=1)),('hard','two_power_slope',dict(a=1,n=3,b=-2,m=2,c=1,t=2))]:
 pair=[]
 for value in (p['a'],2*p['a']):
  params=dict(p,a=value);r=m.generate(level,template=k,parameters=params);verify(r);pair.append(r)
 assert pair[0]['question'][':question/problem']!=pair[1]['question'][':question/problem']
 assert pair[0]['generation']['mathematical_fingerprint']!=pair[1]['generation']['mathematical_fingerprint']
 assert pair[0]['question'][':question/id']!=pair[1]['question'][':question/id']
 held.extend(pair);counts['held_slot_pairs']+=1
render.extend(held)
# Stage-preserving mathematical equality must still fail when pedagogy collapses.
r=m.generate_easy(11,template='q-1953');rhs=rows(blocks(r['question'][':question/worked-solution'])[2])[1]
bad=json.loads(json.dumps(r));bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(rhs,rhs.replace(r'\cdot',''),1)
try:verify(bad)
except (AssertionError,ValueError):counts['equivalent_stage_mutation_rejected']+=1
else:raise AssertionError('A removed explicit multiplication passed')
for key in (':question/problem',':question/worked-solution'):
 bad=json.loads(json.dumps(r));bad['question'][key]+='\x0c'
 try:verify(bad)
 except (AssertionError,ValueError):counts['C0_mutation_rejected']+=1
 else:raise AssertionError('C0 passed')
(D/'deep-native-input.json').write_text(json.dumps(native,indent=2)+'\n')
v.verify_native();v.subprocess.run(['generate/scratch/17592186059716-draft/check-engine',str(D/'deep-native-input.json'),str(D/'deep-native-report.json')],check=True)
(D/'deep-check.json').write_text(json.dumps({'status':'pass_with_documented_native_limit','counts':dict(counts),'sampled_slot_values':slot_values,'native':json.loads((D/'deep-native-report.json').read_text()),'limits':'Sampled source-specific stages and held-input identities; not exhaustive native grading. Raw anomalies remain ineligible. Source syntax aliases share task fingerprints.'},indent=2)+'\n')
(D/'render-records.json').write_text(json.dumps(render,indent=2)+'\n')
print(dict(counts))
