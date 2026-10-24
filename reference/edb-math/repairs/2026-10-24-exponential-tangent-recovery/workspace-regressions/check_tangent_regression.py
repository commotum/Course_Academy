#!/usr/bin/env python3
"""Retained finding65f96ea95438cd2c7b13: current CLI and delivery survivors."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import sympy as s
import tangent_probe as probe


def inspect(records):
    report=probe.probes(records)
    assert report['correct']==0, 'The retained bank-only rule still identifies a key'
    ranks=Counter();positions=Counter();witnesses=[]
    for record in records:
        question=record['question'];problem=question[':question/problem']
        function=probe.parse(re.search(r'y\s*=\s*([^$]+)',problem)[1].rstrip(',.'))
        point=probe.parse(re.search(r'point where \$x=([^$]+)',problem)[1].rstrip('.'))
        base,exponent=function.as_base_exp()
        assert base in [2,3,4,5,6] and point in [-1,0,1]
        assert s.Poly(exponent,probe.x).degree()==1
        ordinate=function.subs(probe.x,point);evaluated=exponent.subs(probe.x,point)
        expected=probe.expected(record);cs=probe.choices(record)
        values=[probe.parse(c[':answer/value']) for c in cs]
        slopes=[s.simplify(s.diff(v,probe.x)) for v in values]
        assert len(values)==len(set(slopes))==5
        hits=[i for i,v in enumerate(values) if s.simplify(v-expected)==0]
        assert len(hits)==1 and cs[hits[0]][':answer/id']==probe.correct(record)
        positions[hits[0]]+=1
        ranks[sorted(range(5),key=lambda i:float(slopes[i])).index(hits[0])]+=1
        alternatives=[]
        for value,slope in zip(values,slopes):
            assert s.simplify(value.subs(probe.x,point)-ordinate)==0
            coefficient=s.simplify(slope/(ordinate*s.log(base)))
            offset=s.simplify(evaluated-coefficient*point)
            assert coefficient.is_Integer and 1<=abs(coefficient)<=9
            assert offset.is_Integer and 1<=abs(offset)<=5
            assert abs(evaluated)<=2
            curve=base**(coefficient*probe.x+offset)
            tangent=s.diff(curve,probe.x).subs(probe.x,point)*(probe.x-point)+curve.subs(probe.x,point)
            assert s.simplify(tangent-value)==0
            alternatives.append({'coefficient':int(coefficient),'offset':int(offset),'equation':str(value)})
        witnesses.append({'question':question[':question/id'],'same_bank_supported_targets':alternatives})
    return {**report,'ranks':dict(ranks),'positions':dict(positions),'counterfactuals':witnesses}


def main():
    here=Path(__file__).resolve().parent
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package',type=Path,default=here)
    parser.add_argument('--source',type=Path)
    parser.add_argument('--inventory',type=Path)
    parser.add_argument('--output',type=Path,default=here/'evidence/tangent-regression/current')
    args=parser.parse_args();package=args.package.resolve()
    source=(args.source or package.parent/'source/source.json').resolve()
    inventory=(args.inventory or package.parent/'source/inventory.json').resolve()
    repo=next(p for p in package.parents if (p/'generate/pipeline/check_delivery.py').is_file())
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    negative=probe.probes(probe.load(here/'tangent-negative.json'))
    assert negative['correct']==negative['total']==4, 'Historical counterexample was lost'
    reports={'historical_negative':negative,'current':{}}
    for name,count,seed in [('requested',4,1072510293),('fresh',24,800)]:
        assets=out/(name+'-assets');assets.mkdir(exist_ok=True)
        command=[sys.executable,str(package/'generator.py'),'--difficulty','hard','--count',str(count),'--seed',str(seed),'--format','json']
        result=subprocess.run(command,cwd=package,env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(assets)},capture_output=True,text=True,check=True)
        batch=out/(name+'.json');batch.write_text(result.stdout)
        records=json.loads(result.stdout);assert len(records)==count
        before=inspect(records)
        delivery=out/(name+'-delivery')
        filter_command=[sys.executable,str(repo/'generate/pipeline/check_delivery.py'),'--input',str(batch),'--source',str(source),'--inventory',str(inventory),'--difficulty','hard','--output',str(delivery),'--asset-root',str(assets),'--math-root',os.environ.get('EDB_MATH_ROOT','/media/jake/SSD/EDB/math')]
        filtered=subprocess.run(filter_command,cwd=package,capture_output=True,text=True,check=True)
        (out/(name+'-delivery.log')).write_text(filtered.stdout+filtered.stderr)
        accepted=probe.load(delivery/'accepted.json');assert len(accepted)==count
        after=inspect(accepted)
        if name=='fresh':assert len(after['ranks'])==len(after['positions'])==5
        reports['current'][name]={'command':command,'delivery_command':filter_command,'before':before,'after':after}
    reports['passed']=True
    probe.save(out/'regression.json',reports)
    print(json.dumps({'passed':True,'requested':4,'fresh':24,'historical_cue':negative['correct'],
                      'current_cue':0,'report':str(out/'regression.json')}))


if __name__=='__main__':main()
