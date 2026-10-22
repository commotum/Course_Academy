"""Affected integer-domain edges and invalid-instance rejection checks."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('audit',ROOT/'checks/validate_repair.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
g=a.g
records=[]
for sid,target in [('q-105161',[0,1,'-']),('q-105160',[0,1,'+'])]:
    n=len(g.parse_problem(g.CASES[sid][':question/problem'])[2])
    for sign in (-1,1):
        params={'a':[6*(-1 if i%2 else 1) for i in range(n)],
                'x':[sign*9,sign*(-3 if target[2]=='-' else 3)]+[0]*(n-2),
                'target':target,'choices':['-12','-1','0','6','12']}
        r=g.generate('easy',92000,sid,params)
        assert a.check(r)==sign*12
        records.append(r)
        for key,value in [('a',7),('x',10)]:
            bad=copy.deepcopy(params);bad[key][0]=value
            try:g.generate('easy',92000,sid,bad)
            except ValueError:pass
            else:raise AssertionError('Out-of-domain instance accepted')
        bad=copy.deepcopy(params);bad['choices']=['-12']*5
        try:g.generate('easy',92000,sid,bad)
        except ValueError:pass
        else:raise AssertionError('Repeated bank accepted')
params={'a':[6,-6,6,-6],'x':[9,-9,9,-9],'target':None,
        'choices':[g.tex(g.sp.ImmutableMatrix(v)) for v in
                   ([9,-9,9,-9],[-9,9,-9,9],[0,0,0,0],[9,9,9,9],[-9,-9,-9,-9])]}
r=g.generate('easy',92000,'q-105158',params);a.check(r);records.append(r)
a.write('boundary-records.json',records)
a.write('boundary-grader-input.json',[a.native(r,'boundary '+str(i)) for i,r in enumerate(records)])
a.write('boundaries.json',{'passed':True,'records':len(records),'a_extrema':[-6,6],'x_extrema':[-9,9],
                         'scalar_answer_extrema':[-12,12],'rejections':['a=7','x=10','repeated choices']})
print(json.dumps({'passed':True,'boundary_records':len(records)}))
