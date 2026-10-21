"""Minimal reproduction; no writes to the generator package."""
import argparse,sys
from pathlib import Path
sys.dont_write_bytecode=True
p=argparse.ArgumentParser();p.add_argument('--package',type=Path,default=Path(__file__).resolve().parent.parent/'workspace');p.add_argument('--template',default='q-74625');a=p.parse_args()
sys.path.insert(0,str(a.package.resolve()))
import generator
print(generator.generate(template=a.template,replay=True))
