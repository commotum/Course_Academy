from audit_helpers import *
from inspect_cues import inspect
rs=[g.generate('easy',seed=764300+i,template='slope_sqrt_radio') for i in range(15)]
save('focused-samples.json',rs);save('focused-cues.json',inspect(rs))
print(inspect(rs)['groups']['slope_sqrt_radio'])
