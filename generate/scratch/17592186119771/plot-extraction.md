# Plot extraction and specification

## 1. Specific observations

Canonical e-4394 prompt asset `images/fc/fc2ed708d717844ca73b7ecbfd8467923fad091ae524153350e7e2fb3df1ea4e.png` shows A=[-2,0,0;6,-1,0;0,0,0], in black on white, with square brackets and A= to the left. The solution asset `images/52/5260137f2dbf20b44400659be8467da333ff228e5bff323465f920a9505ee5f2.png` repeats the same array, highlighting the three above-diagonal zeros blue. Both original raster files were visually inspected at full 162×74 resolution, and copied under `reference/canonical/` with hashes/dimensions in `plot-evidence.json`.

## 2. General pattern

These are standalone mathematical notation images. The color clarifies the complete zero region used for lower-triangular classification. There are no axes, scales, geometry or unreadable labels. Every practice source instead provides its complete matrix as TeX.

## 3. Components

White background, matrix brackets, name A, equality sign, 3×3 entry positions, literal entries, and blue above-diagonal-zero highlighting in the solution. Context: all three above-diagonal entries are zero, and a21=6 is a nonzero witness below; the zero last diagonal entry does not affect triangular validity.

## 4. Reusable specification

Practice generation uses the source TeX array masks, which replace all entries and repeat the complete matrix in each fixed solution. No canonical image path is reused in generated questions and no parameter-dependent raster plot is required. The canonical PNGs remain read-only context/evidence; plot rating **none**. No image model, direct SVG generation, Matplotlib or TikZ is called. The only image-processing step records original PNG metadata/hashes; it does not create or edit images.
