import sys
sys.dont_write_bytecode=True
import hashlib,importlib.util,itertools,json
from pathlib import Path
D=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('catalog00869',D.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
ordinary3=list(itertools.product(range(2,5),repeat=2));ordinary4=[x for x in itertools.product(range(2,6),repeat=2) if x[0]*x[1]<=20];nonsquare=[x for x in ordinary4 if x[0]!=x[1]]
pairs=list(itertools.permutations(range(3),2));triples=list(itertools.combinations(pairs,3));catalog={}
for level in g.LEVELS:
 tasks=set();profiles=0
 if level=='easy':shapes=itertools.chain(itertools.product(ordinary3,repeat=3),((a,b,(n,1)) for a,b in itertools.product(ordinary3,repeat=2) for n in range(2,5)))
 elif level=='moderate':
  def options(roles):return itertools.product(*[[(1,c) for c in range(2,6)] if v else ordinary4 for v in roles])
  shapes=itertools.chain(*(options(r) for r in [[False,True,True],[True,True,False],[False,False,True]]))
 else:shapes=itertools.chain.from_iterable(itertools.permutations(((1,n),(m,1),a)) for n,m in itertools.permutations(range(2,6),2) for a in nonsquare)
 for dims in shapes:
  for edges in triples:
   if level=='hard':
    row=next(i for i,x in enumerate(dims) if x[0]==1);col=next(i for i,x in enumerate(dims) if x[1]==1)
    if (row,col) not in edges or (col,row) not in edges:continue
   tasks.add(json.dumps(g.mathematical_task(dims,edges),separators=(',',':')));profiles+=6
 ordered=sorted(tasks);catalog[level]={'canonical_meaningful_tasks':len(tasks),'ordered_shape_and_statement_presentations':profiles,'canonical_catalog_sha256':hashlib.sha256('\n'.join(ordered).encode()).hexdigest(),'all_boolean_truth_patterns':sorted({tuple(a[0][1]==a[1][0] for a in json.loads(task)[1]) for task in tasks})}
 (D/('semantic-catalog-'+level+'.json')).write_text(json.dumps([json.loads(x) for x in ordered],separators=(',',':')))
(D/'semantic-catalog.json').write_text(json.dumps({'canonicalization':'Supplied dimension multiset plus multiset of ordered requested factor-dimension pairs; excludes variable labels,array order,statement order,entry values,profiles,answer-bank aliases.','levels':catalog},indent=2));print(catalog)
