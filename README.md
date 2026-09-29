# Course Academy

Our FIRe implementation is in [engine/fire](engine/fire/). It combines the
published mechanisms with configurable policies chosen for Course Academy.
The goal is a reliable engine of our own, informed by the available evidence;
matching Math Academy's private numerical values is not a requirement.
Start with the [research and implementation report](reference/fire-reconstruction.md),
[history verification](reference/fire-history-analysis.md), and
[data model](reference/fire-data-model.md).

```bash
python3 -m engine.fire demo
python3 -m unittest discover -s tests -v
```

The [schema index](schema/README.md) groups curriculum and learner data separately
from instructional content. FIRe policy settings are in
[schema/engine](schema/engine/). The [reference index](reference/README.md)
links the earlier research and source material.
