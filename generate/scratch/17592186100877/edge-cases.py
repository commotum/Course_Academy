#!/usr/bin/env python3
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,copy,subprocess
H=Path(__file__).parent;sp=importlib.util.spec_from_file_location('edge_reader',H/'validate.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V);G=V.G
out=[]
for label,p in [('natural zero',dict(n=2,a=1,b=1,c=6,lo=-1,hi=1)),('natural one',dict(n=2,a=3,b=4,c=12,lo=0,hi=2)),('negative shift positive whole interval',dict(n=2,a=5,b=-1,c=10,lo=1,hi=2)),('zero shift positive x interval',dict(n=2,a=3,b=0,c=4,lo=1,hi=2)),('zero shift negative x interval',dict(n=2,a=3,b=0,c=4,lo=-2,hi=-1))]:
 r=G.generate('hard',template='q-336745',parameters=p,profile='observed');answer,counts=V.readback(r['question'],'q-336745');out.append({'label':label,'answer':str(answer),'parameters':p,'counts':counts});assert answer==({'natural zero':0,'natural one':1}.get(label,answer))
for p in [dict(n=2,a=1,b=-1,c=6,lo=-2,hi=2),dict(n=2,a=0,b=1,c=6,lo=0,hi=1),dict(n=2,a=1,b=1,c=6,lo=1,hi=0),dict(n=3,a=1,b=1,c=6,lo=0,hi=1)]:
 try:G.generate('hard',template='q-336745',parameters=p,profile='observed')
 except ValueError:out.append({'invalid_parameters_rejected':p})
 else:raise AssertionError('invalid/pole crossing input admitted')
p=G.parameters(G.CONFIG['q-113747'][2]);a=G.generate('moderate',template='q-113747',parameters=p,profile='observed');b=G.generate('moderate',template='q-113747',parameters=p,profile='authored');assert a['generation']['math_fingerprint']==b['generation']['math_fingerprint'];assert a['question'][':question/id']!=b['question'][':question/id']
out.append({'distinct_whole_bank_id':True,'same_actual_math_id':True})
for badseed in [True,1.5,'2']:
 try:G.generate('easy',badseed)
 except ValueError:out.append({'invalid_seed_rejected':repr(badseed)})
 else:raise AssertionError('non-builtin integer seed accepted')
cli=subprocess.run([sys.executable,'-B',str(H.with_suffix('.py')),'--count','0'],capture_output=True,text=True)
assert cli.returncode==2 and '--count must be positive'in cli.stderr;out.append({'cli_zero_count_rejected':True})
for level in ('easy','moderate','hard'):
 r=G.generate(level,1);m=r['generation'];assert m['eligible']is True and m['evidence_only']is False and m['source_basis']==2275 and 'origin'in m and 'authored_completion'in m and 'source_repairs'in m
out.append({'public_eligibility_and_source_metadata_valid':True})
p=G.parameters(G.CONFIG['q-12917'][2]);p['lo']=-1
try:G.generate('moderate',template='q-12917',parameters=p,profile='observed')
except ValueError as e:assert 'transformed lower endpoint one'in str(e)
else:raise AssertionError('source-profile omitted lower-log condition unenforced')
out.append({'observed_lower_endpoint_condition_explicit':True});(H/'edge-cases.json').write_text(json.dumps(out,indent=2)+'\n');print('Boundary, zero/one, pole and bank identity checks passed.')
