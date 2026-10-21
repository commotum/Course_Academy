"""Strict visible-record regression for the retained rational-bank counterexample."""
import importlib.util,json,pathlib,sys
sys.dont_write_bytecode=True
ROOT=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186115241/workspace')
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('current_generator',ROOT/'17592186115241.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def probe(r):
 f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];key=f[':answer-field/correct'][-1]
 fractional=[c for c in cs if '\\frac' in c[':answer/value']]
 return {'fraction_count':len(fractional),'shortcut_correct':len(fractional)==1 and fractional[0][':answer/id']==key}
if __name__=='__main__':
 r=g.generate_easy(seed=71381,profile='q-32244');result={'record':r,'probe':probe(r)}
 out=ROOT/'evidence'/'fraction-counterexample.json';out.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result['probe']))
 assert not result['probe']['shortcut_correct'],'INCIDENTAL SHORTCUT: the only fractional answer is the correct answer'
