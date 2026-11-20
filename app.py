from pathlib import Path
import sys,json
import numpy as np
import plotly.graph_objects as go
import streamlit as st
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R))
from research.fractalgo.core import excursion,path_edges
st.set_page_config(page_title='FractalGo',page_icon='◈',layout='wide')
lang=st.sidebar.selectbox('Idioma / Language',['Castellano','English']);es=lang=='Castellano'
def T(a,b):return a if es else b
st.markdown('''<style>.stApp{background:linear-gradient(135deg,#fafbfe,#f1ecf9);color:#25324a}h1{font-weight:800;letter-spacing:-.04em}div[data-testid="stMetric"]{background:white;border:1px solid #dcd2ed;border-radius:16px;padding:18px;box-shadow:8px 12px 26px #cfc6df55}</style>''',unsafe_allow_html=True)
st.title('FractalGo')
st.caption(T('ESTRUCTURA · OBSERVACIÓN · DIAGNÓSTICO','STRUCTURE · OBSERVATION · DIAGNOSIS'))
st.write(T('Explorá qué cambia cuando conservamos las relaciones entre los datos.','Explore what changes when relationships between data are retained.'))
page=st.sidebar.radio(T('Explorar','Explore'),[T('Laboratorio','Laboratory'),'GP','Cassini',T('Método y fuentes','Method and sources')])
st.sidebar.caption(T('v0.1.0 · DOI pendiente','v0.1.0 · DOI pending'))
if page in ['Laboratorio','Laboratory']:
 st.subheader(T('Mismos valores, distinta conectividad','Same values, different connectivity'))
 z=st.slider(T('Amplitud del testigo sintético','Synthetic witness amplitude'),.1,4.,1.,.1)
 threshold=st.slider(T('Umbral posterior / prior','Posterior / prior threshold'),.5,2.,1.,.05)
 view=st.radio(T('Vista','View'),[T('Camino','Path'),T('Profundidad','Depth')],horizontal=True)
 a=np.r_[np.ones(40),-np.ones(40)];b=np.tile([1.,-1.],40)
 cols=st.columns(2)
 for col,v,label in zip(cols,[a,b],[T('Bloques','Blocks'),T('Alternancia','Alternation')]):
  result=excursion(z*v,np.ones(80),path_edges(80),threshold)
  active=result['log_ratio']>np.log(threshold);x=np.arange(80);y=np.sin(x/10)*.3
  with col:
   st.metric(label+' · '+T('componentes','components'),result['components'])
   colors=np.where(active,'#7954B3','#b8c6d8')
   fig=go.Figure()
   if view in ['Profundidad','Depth']:
    fig.add_trace(go.Scatter3d(x=x,y=y,z=result['log_ratio'],mode='lines+markers',marker=dict(size=5,color=colors),line=dict(color='#9ab6d2',width=3),customdata=x,hovertemplate='ID %{customdata}<br>log(p/π) %{z:.4f}<extra></extra>'))
    fig.update_layout(scene=dict(xaxis_title='ID',yaxis_title=T('Disposición visual','Visual layout'),zaxis_title='log(p/π)'))
   else:fig.add_trace(go.Scatter(x=x,y=result['log_ratio'],mode='lines+markers',marker=dict(color=colors,size=7),line=dict(color='#9ab6d2'),hovertemplate='ID %{x}<br>log(p/π) %{y:.4f}<extra></extra>'))
   fig.update_layout(height=350,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='white',margin=dict(l=15,r=15,t=15,b=25),font_color='#25324a')
   st.plotly_chart(fig,use_container_width=True)
   st.download_button(T('Descargar nodos y componentes','Download nodes and components'),json.dumps({k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in result.items()},indent=2),label+'.json',key=label)
 st.info(T('La altura y profundidad son una disposición visual, no una geometría física. El testigo es sintético; a umbral 1 conserva los mismos histogramas y cambia la conectividad.','Height and depth are a visual layout, not physical geometry. The witness is synthetic; at threshold 1 it retains identical histograms while changing connectivity.'))
 with st.expander(T('Recorrido guiado','Guided tour'),expanded=True):
  step=st.select_slider(T('Paso','Step'),options=[1,2,3,4],value=1)
  explanations=[T('1. Fijamos un mismo camino de 80 nodos.','1. Fix the same 80-node path.'),T('2. Reordenamos los mismos costes, manteniendo el grafo fijo.','2. Reorder the same costs while keeping the graph fixed.'),T('3. Seleccionamos p/prior por encima del umbral y contamos componentes.','3. Select p/prior above the threshold and count components.'),T('4. La diferencia revela estructura omitida por los resúmenes; no detecta una nueva fuerza.','4. The difference reveals structure omitted by summaries; it does not detect a new force.')]
  st.write(explanations[step-1])
elif page=='GP':
 data=json.loads((R/'research/fractalgo/results/gp.json').read_text())
 st.subheader(T('Ley conjunta y refinamiento','Joint law and refinement'))
 st.image(str(R/f'research/fractalgo/results/topology_gp_{"es" if es else "en"}.png'))
 st.caption(T('1024 realizaciones; barras de 2 errores estándar Monte Carlo. Dos priors son escenarios de sensibilidad.','1024 draws; bars show 2 Monte Carlo standard errors. Two priors are sensitivity scenarios.'))
 st.download_button(T('Resultados completos','Complete results'),json.dumps(data,indent=2),'gp.json')
elif page=='Cassini':
 data=json.loads((R/'research/fractalgo/results/cassini.json').read_text())
 ids=sorted({r['pass_id'] for r in data['rows']});pid=st.selectbox(T('Pasada','Pass'),ids)
 st.image(str(R/f'research/fractalgo/results/topology_cassini_{"es" if es else "en"}.png'))
 st.caption(T('1696 épocas reconstruidas; no reducción de telemetría primaria. Fracciones predictivas exploratorias, no valores-p calibrados.','1696 reconstructed epochs; not primary telemetry reduction. Exploratory predictive fractions, not calibrated p-values.'))
 rows=[r for r in data['rows'] if r['pass_id']==pid]
 st.table([{T('Modelo','Model'):T('Referencia 7200 s','Reference 7200 s') if r['model']=='reference_7200' else T('Mezcla','Mixture'),T('Umbral','Threshold'):r['threshold'],T('Componentes observados (mediana)','Observed components (median)'):r['components_observed_median'],T('Conteo de cola inferior','Lower-tail count'):f"{r['components_lower_tail_count']}/{r['draws']}"} for r in rows])
 st.download_button(T('Resultados completos','Complete results'),json.dumps(data,indent=2),'cassini.json')
else:
 st.markdown((R/f'docs/METHOD_{"ES" if es else "EN"}.md').read_text())
 st.markdown((R/f'docs/PROVENANCE_{"ES" if es else "EN"}.md').read_text())
 st.download_button(T('Registro de procedencia','Provenance ledger'),(R/'provenance/IMPORTED_FILES.json').read_bytes(),'IMPORTED_FILES.json')
