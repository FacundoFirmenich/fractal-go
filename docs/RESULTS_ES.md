# Resultados ejecutados y límites

| Nodos | Ley | Media de componentes | MCSE |
|---|---|---|---|
| 51 | GP conjunto | 1.000977 | 0.000977 |
| 51 | Marginales independientes | 1.729492 | 0.021892 |
| 101 | GP conjunto | 1.000977 | 0.000977 |
| 101 | Marginales independientes | 2.836914 | 0.030079 |
| 201 | GP conjunto | 1.000977 | 0.000977 |
| 201 | Marginales independientes | 5.073242 | 0.043338 |

Prior uniforme en x; umbral posterior/prior 1. Control sintético condicionado, no datos INPOP. Se conserva cada realización en gp_draws.csv.

## Cassini

La tabla incluye conteos de cola de la pasada 12 para umbral 0; la selección es exploratoria y no autoriza exclusiones.

| Modelo | Componentes observados (mediana) | Conteo de cola inferior |
|---|---|---|
| Referencia 7200 s | 32.0 | 0/512 |
| Mezcla | 32.0 | 1/512 |

Estas fracciones predictivas no son probabilidades de una teoría ni valores-p calibrados. Se conservan todos los resultados por pasada en cassini.json. La entrada es una reconstrucción condicionada, no una reducción independiente de telemetría.

Regeneración: `python tools/render_results.py`. Pruebas: 8 grupos del núcleo, incluidos 80 contrastes contra implementaciones independientes; registros en records/.
