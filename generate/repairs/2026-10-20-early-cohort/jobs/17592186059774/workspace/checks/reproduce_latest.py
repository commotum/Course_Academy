"""Run the exact retained reviewer reproduction, redirecting evidence writes here."""
import importlib.util
from pathlib import Path
import runpy
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT.parent / 'review-1-policy-2-22438d1e0e264086'
spec = importlib.util.spec_from_file_location('independent', REVIEW / 'independent.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
# Keep the original inputs and all assertions; change only the write destination.
module.save = lambda name, value: (ROOT / 'evidence/batch-repair' / name).write_text(
    module.json.dumps(value, indent=2, default=str))
sys.modules['independent'] = module
runpy.run_path(str(REVIEW / 'reproduce_batch_shortcut.py'), run_name='__main__')
