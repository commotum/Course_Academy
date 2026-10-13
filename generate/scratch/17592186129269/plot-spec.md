# Asset extraction

1. Specific inspection: the canonical inverse-map SVG shows a three-row input column `(x,y,z)`, a right arrow, and output `(x²,xy,yz)`; the other SVG shows the formal forward map `(u,v,w)→(x(u,v,w),y(u,v,w),z(u,v,w))`. Black typeset mathematics, white background after compositing, no axes, scales, geometric annotations or answer choices.
2. Shared role: these are standalone mathematical typesetting assets, not plots. Practice questions express the corresponding structures directly in Markdown/TeX.
3. Components: bracket glyphs, ordered three-row entries, arrow and transformation label. The mathematical roles are confirmed by raster inspection, not merely filenames or accessibility titles.
4. Specification: plot rating **none**. Keep exact asset/hash evidence for the canonical example; normal generated questions render parameterized component columns in TeX. No plot renderer is needed. `render_assets.py` uses installed librsvg/cairo to inspect original SVGs and does not author SVGs or change shared dependencies.
