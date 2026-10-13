# Plot extraction and reusable specification

## 1. Original plots

All nineteen assets (17 practice, 2 canonical) are listed with original dimensions/hashes in source-assets.json. Original rasters were inspected at original resolution, composited on white where transparent. q-18180: AB10/AD6 at A62°, DC11/BC9 at C51.8°. q-54258: AB8/AD5 at A80°, DC10/BC7 at C50°. q-72754: AB6/AD8 at A85°, DC14/BC16 at C37°. q-285703: AB6/AD7 at A50°, DC8/BC7 at C43°; solution adds dotted BD. q-67787: AB12/AD14 at A42.1°, DC7/BC5 at C103.8°; solution adds dashed BD. q-67788: DA18/DC21 at D60°, AB36/BC30 at B33°; solution adds dashed AC. Canonical: AB42/BC35 at B36° and CD20/DA18 at D80°, solution adds AC.

Parallelograms have light blue interior fill. q-279762 AB10/BC6 with B60°, q-285737 AB8/BC4 with B120°, q-54339 DC8/DA5 with D55°, q-72768 AB18/BC8 with B70°. Solutions add dashed AC. Source angle sectors are blue at A/D, yellow at the other opposite vertex, with the q-67787 C sector green; sides have black edges and unboxed positive lengths. Vertex letters sit outside the polygon. There are no coordinate axes, units/grid ticks, arrowheads, right-angle marks, or plotted answer options. Some diagrams are schematic and measured angles are rounded.

## 2. Shared visual pattern

Draw quadrilateral ABCD with four vertex labels, known sides beside the relevant edges and colored included-angle sectors. The prompt hides the useful diagonal except in authored easy; the solution draws the same polygon with that diagonal visible. Parallelogram fill reinforces its symmetry. Plots carry the mathematical givens, so rating remains heavy.

## 3. Components

White background, black polygon, italic A/B/C/D labels outside corners, positive side numerals outside edges, degree labels inside sectors, optional dashed AC or BD, light blue parallelogram fill. Source originals are reused only for raw anchor replay, with unchanged paths/hashes. Changed parameters update every length, angle, vertex position and sector. Source placement differences are retained in raw prompts and solution masks. Normal renderer uses blue/yellow sectors, a documented incidental color normalization.

## 4. Extracted specification

Matplotlib constructs a first triangle with its actual sides/included angle. The second triangle uses circle intersection from its two side lengths and common diagonal, on the opposite side; marked second angles may differ only within their displayed measurement rounding allowance. For the AC layout the vertex names and side mappings are rotated, retaining DA/DC at D and AB/BC at B. Parallelogram opposite vectors are equal. Normal instances must be convex with side ratio <=3 and interior angles >=25° for readable labels. Bounds derive from all actual vertices and a 16% span margin; labels and sectors scale by span. Aspect ratio is equal. The learner sees a schematic disclaimer and calculates with marked measurements. Correct area and options are never sampled independently of the diagram.

PNG files and JSON sidecars are written with unique temporary files and atomic replacement. Cache requires both files. Sidecars contain actual render coordinates, edge labels, angle labels, shown diagonal, Python/Matplotlib versions and PNG hash. Separate-process concurrency tests exercise duplicate and different instances with fresh writes. No SVG, image models, shared temporary input file, or environment installation is used. New assets remain available for active parent review; old previews are not pruned.

Parent clarification: normal general-quadrilateral prompts state that the marked angles are rounded to their shown precision and ask for the area estimate from those values. The geometry guard admits only a common-diagonal realization within that precision. Raw source wording remains untouched, including incompatible recorded examples.
