"""Strict repair acceptance test: currently fails on a legitimate reordered IVP."""
import importlib.util,sys,pathlib
sys.dont_write_bytecode=True
root=pathlib.Path(__file__).resolve().parent
entry=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else root.parent/'workspace/17592186229165.py'
spec=importlib.util.spec_from_file_location('candidate',entry)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
p=dict(h=1,k=1,f=1,k2=2,f2=1,v=0)
before=g.generate('hard',template='mixed',parameters=p,seed=90211)
p.update(k=2,k2=1)
after=g.generate('hard',template='mixed',parameters=p,seed=90211)
# Both orders must be admitted; the mathematical solution is unchanged.
assert before['question'][':question/answer-fields'][0][':answer-field/choices']
assert after['question'][':question/answer-fields'][0][':answer-field/choices']
print('Both legitimate forcing-component orders are admitted; separately verify solution and positional coverage.')
