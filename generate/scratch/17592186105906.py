import runpy,sys
from pathlib import Path
LOCAL=Path(__file__).with_suffix("")
sys.path.insert(0,str(LOCAL))
if __name__=="__main__":runpy.run_path(str(LOCAL/"generator.py"),run_name="__main__")
