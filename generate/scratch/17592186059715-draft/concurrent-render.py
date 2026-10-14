import importlib.util,json,sys
from pathlib import Path
s=importlib.util.spec_from_file_location("g",sys.argv[1]);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
g.HERE=Path(sys.argv[2]);g.ROOT=Path(sys.argv[3]);g.HERE.mkdir(parents=True,exist_ok=True)
r=g.render_plots(json.loads(sys.argv[4]),["P","Q"],"grid",2);print(json.dumps(r))
