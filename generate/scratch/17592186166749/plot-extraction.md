# Static dependency-tree extraction

Both source assets were inspected at original 412×272 resolution:

- images/11/118759b163a4410f66d5855d7b7b1fd9c2ee4be585e778a759997036bd95f765.png: f(x,y) at left; two blue right-directed edges to x(s,t),y(s,t), labeled f_x,f_y. Each intermediate has right-directed s,t branches labeled its partial. The lower t branch from each intermediate is shaded pale cream. Terminal path products show f_x x_t and f_y y_t for t, and the corresponding s products for unhighlighted branches.
- images/21/21cec766fe72965697304ef4288ffb2b090ddfca179210165dbcfd42ec490b27.png: same complete topology, with s branches highlighted instead. Both terminal derivatives remain partials, not ordinary derivatives.

White/transparent light background, black serif symbolic labels, blue arrow edges, pale cream broad highlights behind selected paths. Nodes and edge labels are symbolic, not parameter slots; no evaluated numerical geometry, plot boundaries, endpoints or coordinate scales occur. The requested coordinate selects one complete asset. Parameter translations leave all symbolic dependency relations unchanged, so exact source paths are reused. No assessed parameter-dependent plot exists; no renderer needed. Raster hashes are recorded in plot-assets.json.
