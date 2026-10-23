"""Strict acceptance test. Run: JOB_PYTHON regression_reciprocal.py PACKAGE_ROOT.
Expected source family: q-70887 / 4890c920-695d-52f8-8b20-5f7886a5c8be.
"""
import importlib.util,json,pathlib,sys
sys.dont_write_bytecode=True
p=pathlib.Path(sys.argv[1]);spec=importlib.util.spec_from_file_location('g',p/'17592186096613.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
try:
 r=g.generate_easy(seed=17,parameters={'n':1,'d':4,'k':0})
 print(json.dumps({'record':r,'result':'construction succeeded; source bank/rendering/math still require review'},indent=2))
except ValueError as e:
 print(json.dumps({'source_id':'4890c920-695d-52f8-8b20-5f7886a5c8be','parameters':{'n':1,'d':4,'k':0},'expected':'supported ln(x)/4 source family','actual':str(e),'passed':False},indent=2));sys.exit(1)
