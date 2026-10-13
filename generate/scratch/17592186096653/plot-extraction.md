# Plot extraction and renderer specification

1. Inspected all 23 source prompts in source-contact.png, composited on white. Each is a triangle OAB in varying orientations; blue arrows run from O to the two known endpoints, a black segment joins those endpoints, and an orange arrow runs from O to the internal point. Endpoint labels and lowercase vector labels agree with the prompt. No axes, coordinates, ticks or metric scale are assessed. The point is strictly inside the segment; only the prompt gives the numerical ratio. There are no solution/choice plots.

2. Shared pattern: two endpoint position vectors and the position vector to an internal ratio point. Geometry supports the two-step path and endpoint difference, without adding coordinate reading.

3. Source shapes are recorded in source.json. All labels, arrow directions, endpoint membership and basis correspondence are meaningful. Triangle orientation and font/style are incidental.

4. Matplotlib fixes A=(0,0), B=(4,0), O=(0.6,2.2), X=A+r/(r+s)(B−A). Vary r,s and all three vertex/basis labels together. Axes remain hidden; preserve blue known arrows, black segment and orange target arrow. Positive ratios guarantee internal membership. Bounds include all labels with fixed margins. PNG and JSON sidecar share the exact instance. Render cache keys include the diagram instance; cache requires both files. Unique private inputs and temporary output names, atomic replacement, and concurrency checks prevent mixed records. Cached Python 3.10/Matplotlib wheels are accessed read only; no environment installation.

Fresh generated plots are inspected with labels, arrow endpoints, margins and ratio membership checked. Independent QA reads PNG-linked sidecars and verifies their geometry against the actual displayed prompt. Source replay regenerates the mathematically equivalent diagram; pixel fidelity is not claimed.
