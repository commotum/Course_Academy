"""Bank and deterministic-batch regressions; accepts an explicit candidate file."""
import argparse
import collections
import itertools
import json
import re
import generator as g


def failures(records):
    groups=collections.defaultdict(list)
    errors=[]
    for record in records:
        q=record['question'];field=q[':question/answer-fields'][0]
        if not field[':answer-field/type'].endswith('/radio'):continue
        points=[list(map(int,re.search(label+r'\((-?\d+),(-?\d+),(-?\d+)\)',q[':question/problem']).groups())) for label in 'ABCD']
        edges=[[x-y for x,y in zip(point,points[0])] for point in points[1:]]
        total=sum((-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))*edges[0][p[0]]*edges[1][p[1]]*edges[2][p[2]] for p in itertools.permutations(range(3)))
        values=[int(a[':answer/value']) for a in field[':answer-field/choices']]
        if sum(v%2 for v in values) in (1,4):errors.append({'id':q[':question/id'],'cue':'isolated bank parity'})
        key=abs(total);coordinates=(sorted(values).index(key),values.index(key))
        labels=['all-radio']
        for edge,row in enumerate(edges):
            if sum(x!=0 for x in row)==1:labels.append('axis-edge-'+str(edge)+'/'+str(next(i for i,x in enumerate(row) if x)))
            elif sum(x!=0 for x in row)==2:labels.append('two-component-edge-'+str(edge)+'/zero-'+str(row.index(0)))
        for label in labels:groups[label].append(coordinates)
    for label,positions in groups.items():
        if len(positions)<2:continue
        for column,name in [(0,'rank'),(1,'position')]:
            if len({p[column] for p in positions})==1:errors.append({'group':label,'cue':'constant '+name,'count':len(positions)})
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--candidate-records');args=parser.parse_args()
    if args.candidate_records:
        result=failures(json.load(open(args.candidate_records)));print(json.dumps({'failures':result}));return bool(result)
    checked=0
    for band in ['easy','moderate','hard']:
        for seed in [354113363,354113364,354113365,824907]:
            records=g.batch(band,5,seed)
            assert records==g.batch(band,5,seed)
            assert not failures(records),(band,seed,failures(records))
            checked+=len(records)
    print(json.dumps({'passed':True,'records':checked,'seeds_per_band':4}));return 0


if __name__=='__main__':raise SystemExit(main())
