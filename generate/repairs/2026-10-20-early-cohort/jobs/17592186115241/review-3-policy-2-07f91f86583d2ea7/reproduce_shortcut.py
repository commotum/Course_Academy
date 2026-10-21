"""Strict failing acceptance regression: ordinary source-profile banks must not identify the key by unique fraction formatting."""
import sys,json,pathlib,importlib.util
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;P=E.parent/'workspace';sys.path.insert(0,str(P))
spec=importlib.util.spec_from_file_location('current_generator',P/'17592186115241.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
r=g.generate_easy(seed=71381,profile='q-32244')
f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];key=f[':answer-field/correct'][-1]
fraction=[c for c in cs if '\\frac' in c[':answer/value']]
result={'command':str(sys.executable)+' -B reproduce_shortcut.py','record':r,'strategy':'Select the only vector containing a printed fraction, without inspecting the system.','selected_answer_id':fraction[0][':answer/id'] if len(fraction)==1 else None,'fraction_count':len(fraction),'shortcut_correct':len(fraction)==1 and fraction[0][':answer/id']==key}
(E/'strict-new-regression.json').write_text(json.dumps(result,indent=2)+'\n')
assert not result['shortcut_correct'], 'INCIDENTAL SHORTCUT: the only fractional answer is the correct answer'
