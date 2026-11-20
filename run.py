#!/usr/bin/env python3
"""FractalGo: reproduce / reproducir; no credentials or network for calculations."""
import os,sys,subprocess,json,hashlib,time,platform
from pathlib import Path
R=Path(__file__).resolve().parent
MODES={'test':['research/fractalgo/test_core.py'],'calculations':['research/fractalgo/run_cases.py'],'figures':['research/fractalgo/figures.py','tools/render_results.py']}
def main():
 mode=sys.argv[1] if len(sys.argv)>1 else 'all'
 if mode=='ui':return subprocess.call([sys.executable,'-m','streamlit','run',str(R/'app.py')],cwd=R)
 if mode not in [*MODES,'all']:raise SystemExit('Modo inválido / Invalid mode: '+mode)
 commands=sum(MODES.values(),[]) if mode=='all' else MODES[mode]
 env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MPLBACKEND='Agg')
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 inputs={str(p.relative_to(R)):sha(p) for p in R.rglob('*') if p.is_file() and '.git' not in p.parts and '.venv' not in p.parts and '__pycache__' not in p.parts and (p.suffix=='.py' and not p.name.startswith('FRACTALGO_') or str(p.relative_to(R)) in ['analyses/gp/results/gp_emulator.json','analyses/gp/sources/cassini/dss25_diseno_erfa_constant.npz','analyses/gp/sources/cassini/contraste_robusto_pesos.npz'])}
 start=time.time();rows=[]
 (R/'records').mkdir(exist_ok=True);(R/'figures').mkdir(exist_ok=True)
 for script in commands:
  t=time.time();result=subprocess.run([sys.executable,script],cwd=R,env=env,capture_output=True,text=True)
  (R/'records'/('run_'+Path(script).stem+'.log')).write_text(result.stdout+result.stderr)
  print(script,result.returncode,round(time.time()-t,2),flush=True);rows.append(dict(script=script,exit_code=result.returncode,seconds=time.time()-t))
  if result.returncode:break
 same=all(sha(R/p)==v for p,v in inputs.items())
 record=dict(mode=mode,python=platform.python_version(),inputs_sha256=inputs,inputs_unchanged=same,commands=rows,seconds=time.time()-start,success=same and all(r['exit_code']==0 for r in rows),scope_es='Ejecución numérica; no validación física independiente.',scope_en='Numerical execution; not independent physical validation.')
 (R/'records'/('execution_'+mode+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
 return 0 if record['success'] else 1
if __name__=='__main__':raise SystemExit(main())
