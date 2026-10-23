"""Regression for d02e8980f26ead535fe5; parses visible records, never writes runtime files."""
import collections, copy, importlib.util, itertools, json, re, sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
OUT=HERE/'evidence'; OUT.mkdir(exist_ok=True)
s=importlib.util.spec_from_file_location('subject',HERE/'17592186161967.py')
g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
UNIT=('q-42531','q-130451','q-91162')
def save(name,data): (OUT/name).write_text(json.dumps(data,indent=2,default=int)+'\n')
def mats(text):
 return [[[int(v.strip()) for v in row.split('&')] for row in raw.split(r'\\')] for raw in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def ops(text):
 text=text.replace('{R}','R')
 return [(int(i)-1,int(j)-1,int(sign+(n or '1')),int(p)-1) for i,j,sign,n,p in re.findall(r'R_\{(\d)\}:=R_\{(\d)\}\s*([+-])\s*(\d*)\s*R_\{(\d)\}',text)]
def apply(A,operations):
 B=copy.deepcopy(A)
 for i,j,k,p in operations:
  assert i==j and i!=p
  B[i]=[x+k*y for x,y in zip(B[i],B[p])]
 return B
def inspect(r):
 q=r['question']; A,B=mats(q[':question/problem']);f=q[':question/answer-fields'][0];choices=f[':answer-field/choices']
 allops=[ops(x[':answer/value']) for x in choices]
 assert len(choices)==5 and len(set(tuple(o) for o in allops))==5
 assert all(len(o)==2 for o in allops)
 valid=[apply(A,o)==B for o in allops];assert sum(valid)==1
 ci=valid.index(True);assert choices[ci][':answer/id']==f[':answer-field/correct'][1]
 steps=mats(q[':question/worked-solution']);so=ops(q[':question/worked-solution'])
 assert len(steps)==3 and steps[0]==A and steps[1]==apply(A,so[:1]) and steps[2]==apply(A,so[:2])==B
 assert so[:2]==so[2:]==allops[ci]
 return [tuple(z[2] for z in o) for o in allops],ci
BASE={'A':[[1,2,3],[2,5,4],[-3,7,8]],'pivot':0,'column':0,'ks':[0,-2,3]}
def coefficients(a,b):
 p=copy.deepcopy(BASE);p['A'][1][0]=-a;p['A'][2][0]=-b;p['ks']=[0,a,b];return p
def groups_report(records):
 groups=collections.defaultdict(list)
 for r in records:
  bank,ci=inspect(r);a,b=bank[ci];p=r['generation']['bank_profile']
  # Recognize the fifth magnitude pattern solely from visible choices.
  ca=collections.Counter(abs(x) for x,y in bank);cb=collections.Counter(abs(y) for x,y in bank)
  ma=ca.most_common(1)[0][0];mb=cb.most_common(1)[0][0]
  extra=next(z for z in bank if tuple(map(abs,z))!=(ma,mb))
  shape='unit-first' if abs(extra[0])!=ma and abs(extra[1])==mb else 'unit-second' if abs(extra[0])==ma and abs(extra[1])!=mb else 'swap'
  stats=[]
  for dim in (0,1):
   counts=collections.Counter(z[dim] for z in bank);mode,n=counts.most_common(1)[0]
   unique=sum(v==n for v in counts.values())==1
   stats.append((unique,unique and mode==bank[ci][dim]))
  groups[(p,shape)].append({'correct':bank[ci],'extra':extra,'stats':stats,'position':ci})
 out={}
 for (p,shape),rows in groups.items():
  out[p+'/'+shape]={'count':len(rows),'first_mode_attempts':sum(r['stats'][0][0] for r in rows),'first_mode_success':sum(r['stats'][0][1] for r in rows),'second_mode_attempts':sum(r['stats'][1][0] for r in rows),'second_mode_success':sum(r['stats'][1][1] for r in rows),'positions':sorted({r['position'] for r in rows})}
 return out

def main():
 records=[];fixed=[];witnesses=[]
 minimal=g.generate(seed=472,bank_profile=UNIT[0],parameters=BASE);inspect(minimal)
 records.append(minimal)
 oldrange=[g.generate(seed=seed,bank_profile=p) for p in UNIT for seed in range(38191,38203)]
 records+=oldrange
 oldleaks=[]
 for r in oldrange:
  bank,ci=inspect(r);mode,n=collections.Counter(x[0] for x in bank).most_common(1)[0];oldleaks.append(n==3 and mode==bank[ci][0])
 assert not all(oldleaks),'Retained 36-case failure persists'
 # Enumerate every visible extra-option sign/role for magnitudes 2 and 3.
 # For each such identical bank, independently change A to require all four signs.
 for profile in g.PROFILES:
  wanted={(s*x,t*y) for x,y in ([(1,3),(2,1)] if profile in UNIT else [(3,2)]) for s in (-1,1) for t in (-1,1)}
  seen=set()
  for seed in range(200):
   probe=g.generate(seed=seed,bank_profile=profile,parameters=coefficients(2,3));bank,_=inspect(probe)
   extra=next(z for z in bank if tuple(map(abs,z))!=(2,3))
   if extra in seen:continue
   seen.add(extra);quartet=[]
   for a,b in itertools.product((-2,2),(-3,3)):
    params=coefficients(a,b)
    # Separate groups are distinct transformations, so delivery deduplication
    # cannot erase whole profile/role groups; within each quartet only signs vary.
    params['A'][1][1]=4+len(witnesses)%6
    params['A'][2][1]=-4+len(witnesses)//6
    r=g.generate(seed=seed,bank_profile=profile,parameters=params);bb,ci=inspect(r)
    assert bb==bank,'Visible bank leaks changed correct signs'
    assert bb[ci]==(a,b)
    quartet.append(r);fixed.append(r)
   assert len({inspect(r)[1] for r in quartet})==4
   witnesses.append({'profile':profile,'seed':seed,'extra':extra,'record_ids':[r['question'][':question/id'] for r in quartet],'correct_pairs':[inspect(r)[0][inspect(r)[1]] for r in quartet]})
   if seen==wanted:break
  assert seen==wanted,(profile,seen,wanted)
 save('regression-records.json',records+fixed)
 save('fixed-bank-records.json',fixed)
 save('regression-report.json',{'finding_id':'d02e8980f26ead535fe5','minimal_bank':inspect(minimal)[0],'old_seed_range_leaks':sum(oldleaks),'old_seed_range_count':len(oldleaks),'identical_bank_groups':len(witnesses),'controlled_records':len(fixed),'witnesses':witnesses,'groups':groups_report(fixed),'interpretation':'For every tested extra sign/role, the same ordered visible bank has four different correct pairs. Neither coefficient sign is determined by the bank. Unique modal coefficient succeeds 50% versus prior 100%.'})
 print(json.dumps({'status':'pass','old_shortcut_success':sum(oldleaks),'old_range_count':36,'identical_bank_groups':len(witnesses),'controlled_records':len(fixed)}))
if __name__=='__main__':main()
