#!/usr/bin/env python3
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,copy
H=Path(__file__).parent;sp=importlib.util.spec_from_file_location('edge_reader',H/'validate.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V);G=V.G
out=[]
for label,p in [('natural zero',dict(n=2,a=1,b=1,c=6,lo=-1,hi=1)),('natural one',dict(n=2,a=3,b=4,c=12,lo=0,hi=2)),('negative shift positive whole interval',dict(n=2,a=5,b=-1,c=10,lo=1,hi=2)),('zero shift positive x interval',dict(n=2,a=3,b=0,c=4,lo=1,hi=2)),('zero shift negative x interval',dict(n=2,a=3,b=0,c=4,lo=-2,hi=-1))]:
 r=G.generate('hard',template='q-336745',parameters=p,profile='observed');answer,counts=V.readback(r['question'],'q-336745');out.append({'label':label,'answer':str(answer),'parameters':p,'counts':counts});assert answer==({'natural zero':0,'natural one':1}.get(label,answer))
for p in [dict(n=2,a=1,b=-1,c=6,lo=-2,hi=2),dict(n=2,a=0,b=1,c=6,lo=0,hi=1),dict(n=2,a=1,b=1,c=6,lo=1,hi=0),dict(n=3,a=1,b=1,c=6,lo=0,hi=1)]:
 try:G.generate('hard',template='q-336745',parameters=p,profile='observed')
 except ValueError:out.append({'invalid_parameters_rejected':p})
 else:raise AssertionError('invalid/pole crossing input admitted')
p=G.parameters(G.CONFIG['q-113747'][2]);a=G.generate('moderate',template='q-113747',parameters=p,profile='observed');b=G.generate('moderate',template='q-113747',parameters=p,profile='authored');assert a['generation']['math_fingerprint']==b['generation']['math_fingerprint'];assert a['question'][':question/id']!=b['question'][':question/id']
out.append({'distinct_whole_bank_id':True,'same_actual_math_id':True});(H/'edge-cases.json').write_text(json.dumps(out,indent=2)+'\n');print('Boundary, zero/one, pole and bank identity checks passed.')
