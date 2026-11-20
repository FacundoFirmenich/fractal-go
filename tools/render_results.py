from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
g=json.loads((R/'research/fractalgo/results/gp.json').read_text());c=json.loads((R/'research/fractalgo/results/cassini.json').read_text())
for lang in ['ES','EN']:
 es=lang=='ES';lines=['# '+('Resultados ejecutados y límites' if es else 'Executed results and limitations'),'','| '+('Nodos | Ley | Media de componentes | MCSE |' if es else 'Nodes | Law | Mean components | MCSE |'),'|---|---|---|---|']
 for r in g['rows']:
  if r['prior']=='uniform_x' and r['threshold']==1:
   label=('GP conjunto' if es else 'Joint GP') if r['law']=='joint_GP' else ('Marginales independientes' if es else 'Independent marginals')
   lines.append(f"| {r['nodes']} | {label} | {r['components']['mean']:.6f} | {r['components']['mcse']:.6f} |")
 lines+=['',('Prior uniforme en x; umbral posterior/prior 1. Control sintético condicionado, no datos INPOP. Se conserva cada realización en gp_draws.csv.' if es else 'Uniform prior in x; posterior/prior threshold 1. Conditional synthetic control, not INPOP data. Each draw is retained in gp_draws.csv.'),'','## Cassini','',('La tabla incluye conteos de cola de la pasada 12 para umbral 0; la selección es exploratoria y no autoriza exclusiones.' if es else 'The table includes pass-12 tail counts at threshold 0; selection is exploratory and does not authorize exclusions.'),'','| '+('Modelo | Componentes observados (mediana) | Conteo de cola inferior |' if es else 'Model | Observed components (median) | Lower-tail count |'),'|---|---|---|']
 for r in c['rows']:
  if r['pass_id']==12 and r['threshold']==0:
   label=('Referencia 7200 s' if es else 'Reference 7200 s') if r['model']=='reference_7200' else ('Mezcla' if es else 'Mixture')
   lines.append(f"| {label} | {r['components_observed_median']} | {r['components_lower_tail_count']}/{r['draws']} |")
 lines+=['',('Estas fracciones predictivas no son probabilidades de una teoría ni valores-p calibrados. Se conservan todos los resultados por pasada en cassini.json. La entrada es una reconstrucción condicionada, no una reducción independiente de telemetría.' if es else 'These predictive fractions are neither theory probabilities nor calibrated p-values. All pass-level results are retained in cassini.json. The input is a conditional reconstruction, not an independent telemetry reduction.'),'',('Regeneración: `python tools/render_results.py`. Pruebas: 8 grupos del núcleo, incluidos 80 contrastes contra implementaciones independientes; registros en records/.' if es else 'Regenerate: `python tools/render_results.py`. Tests: 8 core groups including 80 comparisons against independent implementations; records in records/.'),'']
 (R/f'docs/RESULTS_{lang}.md').write_text('\n'.join(lines))
