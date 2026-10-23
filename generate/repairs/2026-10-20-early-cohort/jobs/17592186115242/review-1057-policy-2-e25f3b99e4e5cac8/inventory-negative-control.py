"""Strict eligible-defect control: in-memory historical state restored in a local fixture only."""
import sys,pathlib,runpy,json
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent
ns=runpy.run_path(str(R/'retained-batch-checks.py'),run_name='negative_control')
# Functions hold the executed namespace; update globals without editing the tested predicate.
gl=ns['inventory_check'].__globals__;gl['INVENTORY']=R/'unretired-negative-control-inventory.json';gl['E']=R/'retained-inventory-negative';gl['E'].mkdir(exist_ok=True)
status=ns['inventory_check']();assert status==1
(R/'inventory-negative-control-results.json').write_text(json.dumps(dict(passed=True,strict_status=status,fixture='unretired-negative-control-inventory.json',changes='Only retirement flags reset to false for the five fully reproduced historical generated records. This is a local negative control, not a claim about current inventory.',report='retained-inventory-negative/inventory-results.json'),indent=2))
