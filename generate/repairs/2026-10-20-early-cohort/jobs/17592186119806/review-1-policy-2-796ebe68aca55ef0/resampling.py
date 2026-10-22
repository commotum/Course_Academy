"""Exercise the duplicate/retry boundary without altering package files."""
import sys
sys.dont_write_bytecode=True
import review as a
g=a.g
base,irrelevant=a.load('irrelevant-records.json')[:2]
other=a.load('control-records.json')[0]
def semantic(r):
    p,d,v,b,x,t,answer=a.parsed(r)
    return (p,d,t,tuple((v[i],b[i]) for i in t[:2]))
assert semantic(base)==semantic(irrelevant)!=semantic(other)
original=g.generate
calls=[]
stream=[base,irrelevant,other]
def controlled(*args,**kwargs):
    calls.append(args)
    return stream[len(calls)-1]
g.generate=controlled
out=g.batch('easy',2,996037)
assert out==[base,other] and len(calls)==3
g.generate=lambda *args,**kwargs:base
try:
    g.batch('easy',2,996037)
except ValueError as ex:
    exhausted=str(ex)
else:raise AssertionError('Repeated duplicates did not exhaust bounded attempts')
finally:g.generate=original
a.save('resampling-results.json',{'command':str(a.PY)+' resampling.py','seed':996037,'passed':True,'injected_records':[base,irrelevant,other],'independent_semantic_test':'Requested component input pairs identical for first two even though unused component differs; third changes requested evidence.','accepted_records':out,'attempts_for_two_unique':len(calls),'all_duplicate_stream_error':exhausted,'method':'In-memory generate override isolates batch rejection behavior; no source or package edits.'})
print('Semantic duplicate rejected and retried; all-duplicate exhaustion correctly raises.')
