"""Strict expected-success regression for ba6171a94fdb8b8baa99.

Read visible prompts, choices, keys and solutions, using the independent oracle
in check_repair. No runtime package changes, services or database operations.
"""
import json
from check_repair import g, inspect, save

def main():
    records=[];checks=[]
    # Exact latest counterexamples and every formerly missing semantic pair.
    # Minimum feasible rows exercise the full-row-rank boundary too.
    parameters=[(3,4,2),(4,7,3),(3,3,2),(3,6,3),(4,8,4),
                (5,10,5),(6,12,6),(7,14,7)]
    for m,n,c in parameters:
        for profile in g.PROFILES['moderate']:
            p=dict(name='A',rows=m,columns=n,count=c,kind='non-pivot')
            r=g.generate('moderate',17,parameters=p,bank_profile=profile)
            fact=inspect(r);assert fact['rank']==n-c
            records.append(r);checks.append({'profile':profile,'parameters':p,'facts':fact})
    # Changing only irrelevant rows remains valid and preserves the answer.
    for profile in g.PROFILES['moderate']:
        pair=[g.generate('moderate',17,parameters=dict(name='A',rows=m,
              columns=7,count=3,kind='non-pivot'),bank_profile=profile) for m in (4,5)]
        assert [inspect(r)['rank'] for r in pair]==[4,4]
        records+=pair
    # The same design rule affects pivot profiles, not just the latest example.
    for profile in g.PROFILES['easy']:
        for m,n,c in [(3,3,1),(5,5,5)]:
            r=g.generate('easy',17,parameters=dict(name='A',rows=m,
                 columns=n,count=c,kind='pivot'),bank_profile=profile)
            assert inspect(r)['rank']==c;records.append(r)
    for m,n,c in [(3,7,3),(4,7,7),(4,7,0)]:
        try:g.generate('moderate',17,parameters=dict(name='A',rows=m,
              columns=n,count=c,kind='non-pivot'))
        except ValueError:pass
        else:raise AssertionError(('Invalid rank admitted',m,n,c))
    # Read normal output across the independently derived finite semantic domain.
    expected={(n,c) for n in range(3,16) for c in range(1,13) if 1<=n-c<=12}
    sampled=g.batch('moderate',len(expected),17)
    actual={(inspect(r)['columns'],inspect(r)['count']) for r in sampled}
    assert actual==expected
    save('root-cause/restriction-records.json',records)
    save('root-cause/restriction.json',{'status':'pass','finding':'ba6171a94fdb8b8baa99',
         'seed':17,'explicit_records':len(records),'checks':checks,
         'normal_semantic_tasks':len(actual),'invalid_cases_rejected':3})
    print(json.dumps({'status':'pass','explicit_records':len(records),
                      'normal_semantic_tasks':len(actual)}))

if __name__=='__main__':main()
