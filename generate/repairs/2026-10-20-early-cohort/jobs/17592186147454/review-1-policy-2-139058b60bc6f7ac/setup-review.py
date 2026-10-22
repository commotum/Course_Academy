import pathlib,shutil,json,hashlib,ast
E=pathlib.Path(__file__).resolve().parent;J=E.parent;P=J/'review-0-policy-2-6ca8b422a4136178';W=J/'workspace'
def save(p,v):(E/p).write_text(json.dumps(v,indent=2)+'\n')
save('package-before.json',{str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()})
shutil.copytree(P/'deps',E/'deps',dirs_exist_ok=True)
for name in ['source-gap-results.json','source-replay-results.json','scope-results.json']:
 shutil.copyfile(P/name,E/('prior-'+name))
# Retained regression executes only in a copied package, so its own output is confined here.
A=E/'author-check';(A/'17592186147454').mkdir(parents=True,exist_ok=True);(A/'evidence').mkdir(exist_ok=True)
for name in ['17592186147454.py','17592186147454/source.json','requirements.txt','repair_check.py']:
 shutil.copyfile(W/name,A/name)
(A/'evidence/deps').symlink_to(E/'deps',target_is_directory=True)
# Preserve independent parser/reduction checks from the preceding reviewer, not author helpers.
node=ast.parse((P/'review.py').read_text());keep=[]
for n in node.body:
 if isinstance(n,ast.FunctionDef) and n.name in ['parse','solve_check','linear_residual']:keep.append(ast.unparse(n))
s='from functools import lru_cache\nimport re,sympy as S\nfrom sympy.parsing.latex import parse_latex\nx,y,C,D=S.symbols("x y C D",positive=True)\n'+'\n\n'.join(keep)
s=s.replace(r'\\text\\{d\\}',r'\\(?:text|mathrm)\\{d\\}') if False else s
# A second derivative form is new presentation; normalize before parsing.
s=s.replace("s = s.strip()", "s = s.replace(r'\\mathrm{d}', r'\\text{d}')\n    s = s.strip()")
(E/'independent_math.py').write_text(s)
save('reuse-provenance.json',{'source_account':str(P/'source-analysis.json'),'math_parser':str(P/'review.py'),'unchanged_source_gap':str(P/'source-gap-results.json'),'notes':'Confirmed source account before package reads; prior parser reused and rerun on current displayed mathematics. Author check copied, not executed in workspace.'})
print('Prepared reviewer-owned dependencies, independent parser, and isolated author checks.')
