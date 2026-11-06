# 7. Plot Generator

Use the plot specification from [Plot Extraction](5-plot-extraction.md) when [Template Generator](6-template-generator.md) needs new plots. Implement shared Python rendering functions in the knowledge point's script. Generate plots programmatically through Matplotlib or TikZ only.

1. Use Matplotlib by default; choose TikZ when the extracted diagram needs specialized geometric constructions, label placement, or mathematical typesetting.
2. Implement the reusable background, coordinate systems, shapes, curves, styling, markers, and annotations, with optional components controlled by the template.
3. Accept the question's sampled parameters and computed mathematical data, deriving positions, labels, scales, and plotted values from that same instance.
4. Render the required prompt, answer-choice, and worked-solution plots, using each choice's own mathematical data where choices are plots.
5. Save assets with reproducible names and return their paths and placement roles to the template generator.
6. Compare rendered variants with source examples, checking mathematical accuracy, visible labels, bounds, scale, clipping, overlap, and readability at the intended display size.

Use a helper such as `render_plots(instance, output_dir)` that returns an asset map for the prompt, choices, and solution. Reuse unchanged assets. Plot rendering must not independently resample question parameters or change the correct answer; convert exact values to numerical coordinates only when rendering requires it.

For TikZ, have Python fill a reusable TikZ template with the same instance data and compile it into a plot asset. Keep both renderers behind the same helper interface and record the selected renderer with each plot template. Do not implement a direct SVG renderer.

Preserve meaningful geometry and instructional cues, including whether figures are drawn to scale. Keep correct and distractor plots consistent in presentation. Record rendering settings and dependency versions with the instance, and return completed assets to [Template Generator](6-template-generator.md) for assembly and validation.

For graph recognition from a calculated table, assess coordinate readability separately from curve correctness. Choose a regular grid that supports the needed coordinates and the distinctions between candidates at the actual display size; automatic “nice” tick spacing alone is insufficient. Derive bounds and scale from the complete bank before selecting its correct role. Do not add the correct table's dots, coordinate labels, parameter labels or construction guides to answer choices to compensate for an unreadable grid. Keep source-supported plotted table points in the worked solution. Reject or resample a bank if its distinguishing features become too small to read. Record grid spacing, pixel scale and complete-bank checks with the rendered assets.

Check the companion table and formulas at the same display size. A visible curve does not make a question usable if the requested table cell or one of its defining formulas is offscreen. Split long generated tables into small panels with repeated parameter/coordinate headings and preserve each requested cell's global parameter association. Use independently breakable coordinate displays rather than locking multiple formulas into one wide gathered row.
