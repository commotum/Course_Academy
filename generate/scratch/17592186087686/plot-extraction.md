# Plot extraction and specification

Practice questions and canonical example contain no plot. All generator templates have plot rating **none**; no assets or renderer are needed.

Two introduction-only originals were visually inspected at full native resolution via view_image: `/home/jake/Developer/MA/DATA/Lessons/837/Source/Images/c624ae330b1e5f51867eebeb4b2c88d8.png` (360×304) and `d266c54c63add0e0a2a374d625b5dcae.png` (360×304). The first has red y=2x+4 and blue y=2x-5, with equal upward slopes and different intercepts, and the second red y=(1/2)x+4 and blue y=2x-5 crossing. Black arrowed axes x/y are unticked; equation labels identify the line geometry. Their instructional role is equal-slope distinct-line parallelism versus different-slope intersection. They remain lesson context and are never reused as parameter-dependent practice assets.

The four plot extraction stages therefore reduce to: identify the two context-only slope-comparison graphs; generalize equal-versus-unequal slope relation; identify red/blue linear functions, offsets, unticked axes and labels; exclude them from all prompt/answer/solution templates. Any later plotted extension would require an independent Matplotlib/TikZ renderer and new QA, beyond this nonplotted assignment.
