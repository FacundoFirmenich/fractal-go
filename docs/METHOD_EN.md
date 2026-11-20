# Method and interpretation contract

Graph G is declared before comparing realizations. For costs q and positive prior masses π, pᵢ ∝ πᵢ exp(−qᵢ/2). Excursions use pᵢ/πᵢ > τ; we report connected components, component masses and selected nodes. Jointly relabelling nodes, edges and weights preserves the result; changing the graph changes the question. A common cost shift leaves the posterior unchanged.

The threshold is strict. An empty excursion has zero components. Trapezoidal cell masses are not exact continuous integration. IDs and temporal gaps are retained; there is no Go-style node capture or deletion. No derived descriptor is multiplied into the likelihood as independent evidence from the same data.

For Cassini, edges connect epochs within one pass only, with gaps ≤ twice its median cadence. Positive and negative excursions are examined separately. Predictive counts are not uniformly calibrated p-values; model and threshold choices are exploratory. The implemented core is distinct from future persistence, triangulation or multifractal extensions.

Software and cited version: [FractalGo v0.1.0](https://doi.org/10.5281/zenodo.24383318) · [All versions](https://doi.org/10.5281/zenodo.24383317).
