# Unit-circle plots

All source asset references and their placement survive in the source snapshot.
The reviewed contact sheet includes every distinct source asset. Prompt diagrams
show blue unit circle centered at the origin, black arrowed x and y axes, light
gray grid with ±1 marks, black OP radius to P in quadrant I, and a gold sector
labeled theta from the positive x-axis to OP. Solution diagrams have the same
objects plus P(cos theta,sin theta). No choices contain plots.

Fixed: coordinate axes, unit radius, first quadrant, colors, center, OP,
angle origin, labels P and theta. Variable: P's exact x/y coordinates, OP slope,
sector angle, P and theta label positions tied to those coordinates. Easy x=m/n,
y=sqrt(1-x²). Moderate y=sqrt(a)/b, x=sqrt(1-y²). No independent plot sampling.
The diagram supplies quadrant and branch information, so changing parameters
requires new prompt and solution plots: moderate plot requirement.

`render_plots` uses Matplotlib, a 4.6-inch square canvas at 140 dpi (644×644),
equal aspect and explicit bounds. Source drawings are schematic; regenerated
points are on the exact unit circle and in the required quadrant. Solution labels
remain symbolic and do not reveal an extra method. Numerical theta labels are
not introduced. Local reproducible PNGs are reviewed before publication through
the existing ImageLibrary SHA-256 store. Original assets are retained unchanged.
