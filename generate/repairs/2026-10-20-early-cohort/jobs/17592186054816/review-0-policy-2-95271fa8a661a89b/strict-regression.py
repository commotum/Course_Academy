import json,sys,pathlib
sys.dont_write_bytecode=True
package=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent.parent/'workspace'
sys.path.insert(0,str(package))
import generator
r=generator.generate(count=1,seed=827461)[0]
q=r['question'];f=q[':question/answer-fields'][-1]
assert f[':answer-field/key']=='None of the above'
assert 'leave every box unchecked' not in q[':question/worked-solution'], 'Explicit None must be selected, but solution tells learner to leave every box unchecked'
