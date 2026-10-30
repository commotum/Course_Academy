#!/usr/bin/env python3
"""Seeded bilinear cross-product practice. Runtime is entirely self-contained."""
import argparse
import hashlib
import itertools
import json
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record, validate_tex

KP = 17592186203897
VERSION = '1.3.0'
NS = uuid.UUID('d535bb46-315d-4a65-8504-d84eb62adb63')
SOURCE = {
 'easy': ['5071b5db-b2c7-5b4f-b394-920acc893dc1','64a063c4-201d-50ad-960d-a431962b0bcf','77730a53-5e90-5c0a-a69e-20df2d022292','a3d1133f-829b-534e-b655-fa677f60efbd','d4525e65-242b-5b41-baf9-63cf6511ce20'],
 'moderate': ['eed27f20-b67a-5b7d-a3c2-a07a46e7e902','49ac232e-6de6-51a0-b147-f48cc384e577','48383069-88ac-53ba-a18f-1b9e7ee17931','f371d14b-8e3d-511c-bad0-0c7eef2c31d9'],
 'hard': ['55262969-4b93-56e8-8ac6-8050498b3bd0'],
}
def cross(a,b):
 return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def scale(n,v): return tuple(n*x for x in v)
def add(*vs): return tuple(map(sum,zip(*vs)))
def linear(weights,vs): return add(*(scale(n,v) for n,v in zip(weights,vs)))
def sym(s): return r'\mathbf{'+s+'}'
def lin(coeffs,objects):
 parts=[]
 for n,obj in zip(coeffs,objects):
  if not n: continue
  part=('' if abs(n)==1 else str(abs(n)))+obj
  parts.append(('-' if n<0 else ('+' if parts else ''))+part)
 return ''.join(parts) or '0'
def vec(v,notation='basis'):
 if notation=='tuple': return r'\langle '+','.join(map(str,v))+r'\rangle'
 return lin(v,[sym(x) for x in 'ijk']) if any(v) else sym('0')
def par(s): return '('+s+')'
def pair(x,y): return sym(x)+r'\times '+sym(y)
def uid(s): return str(uuid.uuid5(NS,s))
def display(rows): return '$$\n'+r'\begin{aligned}'+'\n'+r' \\ '.join(rows)+'\n'+r'\end{aligned}'+'\n$$'

def sum_rows(coefficients, objects):
 rows=[]
 for start in range(0,len(objects),2):
  text=lin(coefficients[start:start+2],objects[start:start+2])
  if start and coefficients[start]>0: text='+'+text
  rows.append(('&=' if not start else r'&\quad ')+text)
 return rows

def description(i):
 p,q,r,s=i['coefficients']; side=i['side']; band=i['band']
 if band=='hard':
  L=[(p,'a'),(q,'b')]; R=[(r,'c'),(s,'d')]
 elif side=='left': L=[(p,'a'),(q,'b')]; R=[(r,'c')]
 else: L=[(r,'c')]; R=[(p,'a'),(q,'b')]
 operand=lambda terms: par(lin([n for n,_ in terms],[sym(x) for _,x in terms]))
 lhs=operand(L)+r'\times '+operand(R)
 terms=[(u*v,x,y,u,v) for u,x in L for v,y in R]
 weights=[n for n,_,_,_,_ in terms]
 products=([tuple(v) for v in i['replay_products']] if 'replay_products' in i else [cross(i['vectors'][x],i['vectors'][y]) for _,x,y,_,_ in terms])
 return lhs,terms,weights,products

def bank(i,weights,products):
 # A whole profile is chosen before values. No pooled first-valid fallback.
 if len(weights)==2:
  a,b=weights; t=abs(i['coefficients'][2]); sign=lambda n: 1 if n>0 else -1
  if i['profile']=='factor-sign':
   bad=[(sign(a)*t,b),(a,sign(b)*t),(-a,b),(a,-b)]
   reasons=['Omitted the first inner scalar','Omitted the second inner scalar','Changed the first contribution sign','Changed the second contribution sign']
  else:
   bad=[(a,0),(b,a),(i['coefficients'][2],i['coefficients'][2]),(a,-b)]
   reasons=['Omitted the second distributed term','Assigned the scalar factors to the wrong products','Omitted both inner scalar factors','Changed the second contribution sign']
 else:
  if i['profile']=='omit-pair':
   bad=[tuple((0 if k<2 else -n) if j==k else n for j,n in enumerate(weights)) for k in range(4)]
   reasons=[('Omitted' if k<2 else 'Changed the sign of')+' ordered pairing '+str(k+1) for k in range(4)]
  else:
   bad=[tuple((-n if k<2 else 0) if j==k else n for j,n in enumerate(weights)) for k in range(4)]
   reasons=[('Changed the sign of' if k<2 else 'Omitted')+' ordered pairing '+str(k+1) for k in range(4)]
 values=[linear(weights,products)]+[linear(w,products) for w in bad]
 if len(set(values))!=5: raise ValueError('Ambiguous profile for these values')
 return values,['Correct distribution']+reasons

def build(i,seed=0):
 lhs,terms,weights,products=description(i); result=linear(weights,products)
 notation=i['notation']; v=lambda x:vec(x,notation)
 givens=[pair(x,y)+'&='+v(g) for (_,x,y,_,_),g in zip(terms,products)]
 order=i.get('given_order',list(range(len(givens))))
 prompt='Find $'+lhs+'$, given\n\n'+display([givens[k] for k in order])
 # Show distribution on original operands, then scalar extraction and every sum.
 expanded_objects=[par(lin([u],[sym(x)]))+r'\times '+par(lin([vv],[sym(y)])) for n,x,y,u,vv in terms]
 extracted_objects=[par(pair(x,y)) for _,x,y,_,_ in terms]
 substituted_objects=[par(v(g)) for g in products]
 contribution_objects=[par(v(scale(n,g))) for n,g in zip(weights,products)]
 solution='Distribute over each sum or difference, keeping the operands in their original order:\n\n'+display(['&'+lhs]+sum_rows([1]*len(terms),expanded_objects))+ '\n\nExtract the scalars, substitute the given ordered products, and add corresponding components:\n\n'+display(
 sum_rows(weights,extracted_objects)+sum_rows(weights,substituted_objects)+sum_rows([1]*len(terms),contribution_objects)+['&='+v(result)])
 prompt=normalize_prose(prompt); solution=normalize_prose(solution)
 # A fixed three-component skeleton reveals no result signs or cancellation.
 values,reasons=(bank(i,weights,products) if i['response']=='radio' else (None,None))
 semantic={'band':i['band'],'lhs':lhs,'products':products,'response':i['response'],'notation':notation,'profile':i['profile'] if values else None,'bank':values}
 digest=hashlib.sha256(json.dumps(semantic,sort_keys=True).encode()).hexdigest()
 qid=uid(digest); fields=[]
 if values:
  choices=[{':answer/id':uid(qid+'/selection/'+str(k)),':answer/type':':answer.type/math',':answer/value':normalize_tex(v(a))} for k,a in enumerate(values)]
  order_rng=random.Random(str(seed)+digest); order_rng.shuffle(choices)
  fields=[{':answer-field/id':uid(qid+'/selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(qid+'/selection/0')]}]
 else:
  chunks=[]
  for k,n in enumerate(result):
   key='field-'+str(k+1); aid=uid(qid+'/'+key+'/value')
   fields.append({':answer-field/id':uid(qid+'/'+key),':answer-field/key':key,':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':str(n)}],':answer-field/correct':[':answer/id',aid]})
   chunks.append('{{'+key+'}}')
  if notation=='basis': skeleton=chunks[0]+' $'+sym('i')+'+$ '+chunks[1]+' $'+sym('j')+'+$ '+chunks[2]+' $'+sym('k')+'$'
  else: skeleton='$\\langle$ '+(' $,$ '.join(chunks))+' $\\rangle$'
  prompt=normalize_prose(prompt+'\n\nEnter the signed components, including any zeros.\n\n$'+lhs+'=$ '+skeleton)
 for field in fields:
  for a in field[':answer-field/choices']: validate_tex(a[':answer/value'])
 rec={'knowledge_point':KP,'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+i['band'],':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':i['band']+'-'+i['side'],'parameters':i,'semantic_id':digest,'source_question_ids':SOURCE[i['band']], 'result':result,'weights':weights,'bank_vectors':values,'error_recipes':reasons}}
 return validate_generated_record(rec)

def cases(band):
 if band=='hard': return list(itertools.product(['both'],[-1,1],[-1,1],['radio','blank']))
 return list(itertools.product(['left','right'],[-1,1],[-1,1],['radio','blank']))
def sample_instance(rng,band,role):
 side,sign,outer_sign,response=role
 if band=='hard':
  coeff=[rng.choice([-1,1]),sign,rng.choice([-1,1]),outer_sign]
  coeff[rng.randrange(4)]*=2
  vectors={x:tuple(rng.randint(-1,1) for _ in range(3)) for x in 'abcd'}
  if not any(cross(vectors['a'],vectors['b'])) or not any(cross(vectors['c'],vectors['d'])): raise ValueError('Parallel operand pair')
  profile=rng.choice(['omit-pair','sign-pair'])
 else:
  coeff=[rng.choice([-1,1])*rng.choice([2,3]),sign*rng.choice([2,3]),1 if band=='easy' else outer_sign*2,0]
  vectors={x:tuple(rng.randint(-3,3) for _ in range(3)) for x in 'ab'}
  axis=rng.randrange(3); vectors['c']=tuple(int(k==axis) for k in range(3))
  # The components parallel to c are irrelevant and remain genuine latent values.
  profile=rng.choice(['factor-sign','distribution'])
 i={'band':band,'side':side,'coefficients':coeff,'vectors':vectors,'response':response,'notation':rng.choice(['basis','tuple']),'profile':profile}
 lhs,terms,weights,products=description(i)
 if any(not any(v) for v in products): raise ValueError('Zero supplied product')
 if band=='hard' and max(abs(x) for v in products for x in v)>2: raise ValueError('Arithmetic bound')
 if response=='radio': bank(i,weights,products)
 return i

def bank_cues(record):
 # Position/rank strategies may see only the rendered bank, never the givens.
 field=record['question'][':question/answer-fields'][0]
 if not field[':answer-field/type'].endswith('/radio'): return None
 ordered=field[':answer-field/choices']
 # UUIDs were created before the option shuffle; map them to the authored vectors.
 qid=record['question'][':question/id']; values=record['generation']['bank_vectors']
 by_id={uid(qid+'/selection/'+str(k)):tuple(v) for k,v in enumerate(values)}
 vectors=[by_id[a[':answer/id']] for a in ordered]
 index=next(k for k,a in enumerate(ordered) if a[':answer/id']==field[':answer-field/correct'][1])
 correct=vectors[index]; norms=[sum(x*x for x in v) for v in vectors]
 # A tied norm does not single out an option.
 norm_rank=sorted(norms).index(norms[index]) if norms.count(norms[index])==1 else None
 modes=[]
 for k in range(3):
  counts={n:sum(v[k]==n for v in vectors) for n in {v[k] for v in vectors}}
  modes.append({n for n,c in counts.items() if c==max(counts.values())})
 modal=[j for j,v in enumerate(vectors) if all(v[k] in modes[k] for k in range(3))]
 # This slot is present only when the bank-only modal rule uniquely selects the key.
 # Non-predictions must not be balanced as though they were an answer position.
 modal_cue=True if modal==[index] else None
 return index,sorted(vectors).index(correct),norm_rank,modal_cue

def bank_shape(record):
 values=[tuple(v) for v in record['generation']['bank_vectors']]
 return sum(tuple(-x for x in v) in values for v in values)

def repeat_bank_cue(record,previous):
 cues=bank_cues(record)
 if cues is None:return False
 i=record['generation']['parameters']
 for group in ['all','side','notation','profile','bank_shape']:
  prior=[r for r in previous if bank_cues(r) is not None and
   (group=='all' or (bank_shape(r)==bank_shape(record) if group=='bank_shape' else r['generation']['parameters'][group]==i[group]))]
  if not prior:continue
  for k,cue in enumerate(cues):
   if cue is not None and all(bank_cues(r)[k]==cue for r in prior):return True
 return False

def generate(difficulty,count,seed):
 if difficulty=='unclassified': difficulty='moderate'
 if count<0: raise ValueError('Count must be nonnegative')
 rng=random.Random(seed); roles=cases(difficulty); rng.shuffle(roles)
 records=[]; seen=set(); attempts=0
 while len(records)<count:
  attempts+=1
  if attempts>max(10000,count*500): raise RuntimeError('Could not construct the requested distinct batch')
  try: i=sample_instance(rng,difficulty,roles[len(records)%len(roles)]); rec=build(i,seed)
  except ValueError: continue
  # Compare mathematical instances, ignoring option ordering and identity.
  signature=json.dumps([description(i)[0],description(i)[3]],sort_keys=True)
  if signature in seen or repeat_bank_cue(rec,records): continue
  seen.add(signature); records.append(rec)
 return records

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--difficulty',choices=['unclassified','easy','moderate','hard'],default='moderate')
 parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0)
 parser.add_argument('--format',choices=['json'],default='json');args=parser.parse_args()
 print(json.dumps(generate(args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
