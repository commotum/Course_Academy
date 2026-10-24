"""Reproduce each old generated identity, mathematical task and complete bank."""
import importlib.util
import json
from pathlib import Path
import sys

H=Path(__file__).resolve().parent;ROOT=H.parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from generator_publish import normalized_question


def main():
    for kp in (17592186068916,17592186068917,17592186068918):
        inv=json.loads((H/str(kp)/'inventory/inventory.json').read_text())
        old=[q for q in inv['questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired')]
        evidence=[]
        if old:
            sys.modules.pop('printed',None)
            path=H/str(kp)/'originals'/f'{kp}.py'
            spec=importlib.util.spec_from_file_location('original_'+str(kp),path)
            g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
            candidates=[g.generate(values[0],0,t,{'m':m}) for t,values in g.DATA.items()
                        if values[0] in ('easy','moderate') for m in range(2,13)]
            for q in old:
                matches=[r for r in candidates if r['question'][':question/id']==q[':question/id']]
                assert len(matches)==1,(kp,q[':db/id'],len(matches))
                r=matches[0];left=normalized_question(q);right=normalized_question(r['question'])
                left_problem=left.pop(':question/problem');right_problem=right.pop(':question/problem')
                assert left==right,'Old bank, solution or identities failed exact reproduction'
                assert g.p.integral(left_problem)==g.p.integral(right_problem),'Old mathematical task changed'
                evidence.append({'entity':q[':db/id'],'uuid':q[':question/id'],
                    'finding':'Amplitude-only source clone replaced by reviewed structural families',
                    'reproduction':r,'verified':'Exact generated UUID, complete bank, worked solution, and printed mathematical task'})
        (H/str(kp)/'retirement-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
        print(kp,'old generated tasks and complete banks reproduced:',len(evidence))


if __name__=='__main__':main()
