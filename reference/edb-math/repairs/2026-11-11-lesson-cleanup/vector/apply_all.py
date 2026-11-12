"""Sequential reviewed application; stop on any unconfirmed failure, then verify."""
import argparse,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true',required=True);p.parse_args()
for kp in [17592186096652,17592186096653,17592186096701,17592186235285]:
 print('Applying reviewed vector KP',kp,flush=True)
 subprocess.run([sys.executable,str(H/'publish.py'),str(kp),'--apply'],check=True)
subprocess.run([sys.executable,str(H/'verify_final.py')],check=True)
