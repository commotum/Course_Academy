# Plot extraction and specification

All nine practice plots and the canonical plot were inspected at original resolution. Source copies preserve exact raster bytes. The root reviewer independently confirmed the same domains.

| Source | Dimensions | Radius² | θ/π interval | Meaningful geometry |
|---|---|---:|---|---|
| q-161044 | 360×304 | 5 | [0, 2] | blue disk/sector, exact axis intercepts, D label |
| q-38076 | 360×304 | 4 | [-0.5, 0.5] | blue disk/sector, exact axis intercepts, D label |
| q-161038 | 326×275 | 16 | [1, 1.5] | blue disk/sector, exact axis intercepts, D label |
| q-161039 | 360×304 | 4 | [0, 2] | blue disk/sector, exact axis intercepts, D label |
| q-161041 | 360×304 | 16 | [0, 2] | blue disk/sector, exact axis intercepts, D label |
| q-83499 | 360×304 | 4 | [-0.5, 0] | blue disk/sector, exact axis intercepts, D label |
| q-83500 | 360×304 | 2 | [0, 1] | blue disk/sector, exact axis intercepts, D label |
| q-83954 | 360×304 | 3 | [0.5, 1] | blue disk/sector, exact axis intercepts, D label |
| q-161043 | 360×304 | 25 | [0, 2] | blue disk/sector, exact axis intercepts, D label |

Canonical e-7347: 360×304, first-quadrant quarter disk radius 1. Full-circle practice plots additionally label x²+y²=n and ±R at all four axis intercepts. Partial plots show only the assessed sector with radial boundaries along coordinate axes; no shifted center, extra arcs or annular hole occurs. Black horizontal/vertical axes have arrowheads and x/y labels. Circle boundaries are blue, interiors pale blue, and D is blue. Numeric/radical labels are integral to the mathematical reading.

General representation: D={(r cosθ,r sinθ):0≤r≤√n,aπ≤θ≤bπ}. Renderer derives 401 arc points, radial boundary endpoints and intercept visibility from this same object. It uses equal x/y scale and limits ±1.45√n, labels ±√n (integer when n is square), the region D, and x²+y²=n for full disks. Each quarter-turn rotation moves the shaded geometry and eligible intercept labels consistently.

Plot rating **moderate**: every question relies on a simple region diagram. Prompt plots only; answer options and worked solutions contain math, not additional diagrams. Original geometry can reuse the byte-identical copied raster. Any changed geometry must use Matplotlib. The renderer uses an existing cached Python 3.10/Matplotlib runtime read-only when the main Python 3.13 environment lacks Matplotlib; paths and versions are recorded in every sidecar.

Every invocation uses a unique private render-input file and unique temporary PNG/sidecar, then atomic replace. Cache validity requires both files. Concurrent same-instance and different-instance fresh output checks validate sidecar geometry and clean only their own temporary files. No direct SVG/image-model rendering is used.

Generated rendered review covers full circles, all four quadrant sectors, right/upper/left/lower semicircle orientations and radical/square radii. Labels, axes, fill, boundary scale and clipping are checked visually; actual arc data and exact labels are independently checked in sidecars. Styling is normalized, not claimed pixel-identical to the source.
