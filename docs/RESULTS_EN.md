# Executed results and limitations

| Nodes | Law | Mean components | MCSE |
|---|---|---|---|
| 51 | Joint GP | 1.000977 | 0.000977 |
| 51 | Independent marginals | 1.729492 | 0.021892 |
| 101 | Joint GP | 1.000977 | 0.000977 |
| 101 | Independent marginals | 2.836914 | 0.030079 |
| 201 | Joint GP | 1.000977 | 0.000977 |
| 201 | Independent marginals | 5.073242 | 0.043338 |

Uniform prior in x; posterior/prior threshold 1. Conditional synthetic control, not INPOP data. Each draw is retained in gp_draws.csv.

## Cassini

The table includes pass-12 tail counts at threshold 0; selection is exploratory and does not authorize exclusions.

| Model | Observed components (median) | Lower-tail count |
|---|---|---|
| Reference 7200 s | 32.0 | 0/512 |
| Mixture | 32.0 | 1/512 |

These predictive fractions are neither theory probabilities nor calibrated p-values. All pass-level results are retained in cassini.json. The input is a conditional reconstruction, not an independent telemetry reduction.

Regenerate: `python tools/render_results.py`. Tests: 8 core groups including 80 comparisons against independent implementations; records in records/.
