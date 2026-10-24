
# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186184153-source-policy.json'))
    raise SystemExit(0)

from forward import sample,main
KP=17592186184153

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186184153-source-policy.json'))

if __name__=="__main__":main(KP)
