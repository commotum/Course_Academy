#!/usr/bin/env python3
"""Retained findings, independently reading visible matrices and actual delivery."""
import copy
from collections import Counter,defaultdict
from decimal import Decimal
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode=True
W=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186119772/workspace');E=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186119772/review-1-policy-2-8bffef87d808bbc0/author-check-current/evidence');E.mkdir(exist_ok=True)
sys.path.insert(0,str(W))
spec=importlib.util.spec_from_file_location('current_generator',Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186119772/workspace/17592186119772.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
REPO=Path('/home/jake/Developer/Course_Academy');PY=REPO/'.venv/bin/python'
# Separate parser and exact-zero witness; no use of generator's metadata or predicates.
RX=re.compile(r'([A-E])\s*=\s*(?:\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}|\[\\begin\{aligned\}(.*?)\\end\{aligned\}\])',re.S)
def parse(text):
 out={}
 for m in RX.finditer(text):
  a=tuple(tuple(Decimal(v.strip()) for v in row.split('&')) for row in (m[2] if m[2] is not None else m[3]).split(r'\\'))
  assert a and all(len(row)==len(a) for row in a)
  assert m[1] not in out or out[m[1]]==a
  out[m[1]]=a
 return out
def kind(x):return x.get(':db/ident') if isinstance(x,dict) else x
def correct(f):
 ref=f[':answer-field/correct'];aid=ref[':answer/id'] if isinstance(ref,dict) else ref[1]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def inspect(r):
 q=r['question'];fields=q[':question/answer-fields'];orientation='upper' if 'upper triangular' in q[':question/problem'] else 'lower'
 matrix=parse(q[':question/problem'])
 for f in fields:
  matrix.update(parse(f.get(':answer-field/key','')))
  for a in f[':answer-field/choices']:matrix.update(parse(a[':answer/value']))
 good=tuple(x for x,a in sorted(matrix.items()) if all(v==0 for i,row in enumerate(a) for j,v in enumerate(row) if (i>j if orientation=='upper' else i<j)))
 if kind(fields[0][':answer-field/type']).endswith('/checkbox'):
  actual=tuple(sorted(next(iter(parse(f[':answer-field/key']))) for f in fields if correct(f)=='true'))
 elif parse(correct(fields[0])):actual=tuple(parse(correct(fields[0])))
 else:actual=tuple(sorted(re.findall(r'\$([A-E])\$',correct(fields[0]))))
 assert actual==good,(q[':question/id'],actual,good)
 solution=q[':question/worked-solution']
 if len(matrix)==5 and kind(fields[0][':answer-field/type']).endswith('/radio'):
  assert re.search(r'Notice that \$([A-E])\$',solution)[1]==good[0]
  assert parse(solution)==matrix
 else:
  stated=tuple(sorted(re.findall(r'\$([A-E])\$',solution.split(' since')[0])))
  assert stated==good,(stated,good)
 for label,row,col,value in re.findall(r'\{([a-e])\}_\{([1-4])([1-4])\}\s*&\s*=(-?\d+(?:\.\d+)?)\\ne 0',solution):
  i,j=int(row)-1,int(col)-1
  assert (i>j if orientation=='upper' else i<j)
  assert matrix[label.upper()][i][j]==Decimal(value)!=0
 return {'answer':good,'orientation':orientation,'dimensions':tuple(len(a) for _,a in sorted(matrix.items())),
         'correct_position':None if len(fields)>1 else next(i for i,a in enumerate(fields[0][':answer-field/choices']) if a[':answer/value']==correct(fields[0])),
         'semantic':(orientation,tuple(sorted((len(a),tuple((i,j) for i,row in enumerate(a) for j,v in enumerate(row) if i!=j and v)) for a in matrix.values())))}
def save(name,value): (E/name).write_text(json.dumps(value,indent=2)+'\n')
commands=[]
def delivery(records,name):
 save(name+'-input.json',records)
 cmd=[str(PY),str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/(name+'-input.json')),'--source',str(W.parent/'source/source.json'),'--inventory',str(W.parent/'source/inventory.json'),'--difficulty','easy','--output',str(E/name),'--math-root','/media/jake/SSD/EDB/math']
 result=subprocess.run(cmd,capture_output=True,text=True)
 assert result.returncode==0,result.stderr+result.stdout
 commands.append(cmd)
 return json.loads((E/name/'accepted.json').read_text())
