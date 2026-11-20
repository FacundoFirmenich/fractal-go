import os,sys,subprocess,venv
from pathlib import Path
R=Path(__file__).resolve().parent
folder=R/'.venv';python=folder/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
if not python.exists():venv.EnvBuilder(with_pip=True).create(folder)
subprocess.run([str(python),'-m','pip','install','-r',str(R/'requirements.txt')],check=True)
raise SystemExit(subprocess.call([str(python),str(R/'run.py'),sys.argv[1] if len(sys.argv)>1 else 'ui'],cwd=R))
