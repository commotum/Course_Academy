import json,sys,unittest
from pathlib import Path
root=Path('/home/jake/Developer/Course_Academy')
sys.path[:0]=[str(root/'scripts'),str(root/'tests'),str(root)]
patterns=('test_generator*.py','test_inventory*.py','test_find_candidates*.py','test_integration_*.py','test_inverse_*.py','test_linear_trig*.py','test_substitution*.py','test_scoped_generator_constraints.py','test_trig*.py','test_recover_engine_only_refills.py')
def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item
def main():
    all_tests=[]
    for pattern in patterns:
        all_tests.extend(flatten(unittest.defaultTestLoader.discover(str(root/'tests'),pattern=pattern)))
    all_tests=list({test.id():test for test in all_tests if not test.id().startswith('test_generator_render.')}.values())
    part,count=map(int,sys.argv[1:3]); selected=all_tests[part::count]
    result=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(selected))
    Path(f'/tmp/generator-intent-final-shard-{part}.json').write_text(json.dumps({'tests':result.testsRun,'failures':[(t.id(),trace) for t,trace in result.failures],'errors':[(t.id(),trace) for t,trace in result.errors],'skipped':[(t.id(),reason) for t,reason in result.skipped],'passed':result.wasSuccessful(),'patterns':patterns,'total_selected':len(all_tests)}))
    raise SystemExit(int(not result.wasSuccessful()))

if __name__ == "__main__":
    main()
