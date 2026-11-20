from pathlib import Path
import io,zipfile,hashlib,base64,nbformat
R=Path(__file__).resolve().parents[1]
b=io.BytesIO()
with zipfile.ZipFile(b,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(R.rglob('*')):
  rel=p.relative_to(R)
  if not p.is_file() or any(x in rel.parts for x in ['.git','.venv','__pycache__','release']):continue
  if p.name.startswith('FRACTALGO_') or p.suffix=='.log':continue
  z.write(p,str(rel))
raw=b.getvalue();digest=hashlib.sha256(raw).hexdigest();payload=base64.b64encode(raw).decode()
setup='PAYLOAD_SHA256='+repr(digest)+'\nPAYLOAD='+repr(payload)+'''
from pathlib import Path
import base64,hashlib,zipfile,io,tempfile,subprocess,sys
raw=base64.b64decode(PAYLOAD)
assert hashlib.sha256(raw).hexdigest()==PAYLOAD_SHA256
WORK=Path(tempfile.mkdtemp(prefix='FractalGo_'))
with zipfile.ZipFile(io.BytesIO(raw)) as archive:
    assert all((WORK/n).resolve().is_relative_to(WORK) for n in archive.namelist())
    archive.extractall(WORK)
print(WORK)
'''
for lang in ['ES','EN']:
 es=lang=='ES';nb=nbformat.v4.new_notebook();nb.metadata['kernelspec']={'name':'python3','language':'python','display_name':'Python 3'}
 nb.cells=[nbformat.v4.new_markdown_cell('# FractalGo · '+('cuaderno autónomo\n\nEjecutar todas reproduce controles, cálculos y figuras. La primera instalación requiere Internet. Controles sintéticos y Cassini reconstruido, no detección física. DOI: 10.5281/zenodo.24383318. CC BY 4.0 (LICENSES.md). Windows/Linux/macOS: interfaz visual en app.py; iOS/iPadOS: Colab en navegador.' if es else 'standalone notebook\n\nRun all reproduces controls, calculations and figures. First installation requires Internet. Synthetic controls and reconstructed Cassini, not physical detection. DOI: 10.5281/zenodo.24383318. CC BY 4.0 (LICENSES.md). Windows/Linux/macOS: visual interface in app.py; iOS/iPadOS: Colab in a browser.')),
 nbformat.v4.new_code_cell(setup),nbformat.v4.new_code_cell("subprocess.run([sys.executable,'-m','pip','install','-r',str(WORK/'requirements.txt')],check=True)\nsubprocess.run([sys.executable,str(WORK/'run.py'),'all'],cwd=WORK,check=True)"),nbformat.v4.new_code_cell("from IPython.display import Image,display\nfor case in ['gp','cassini']:\n    display(Image(filename=str(WORK/f'research/fractalgo/results/topology_{case}_"+lang.lower()+".png')))"),nbformat.v4.new_markdown_cell('## '+('Guardar resultados' if es else 'Save results')),nbformat.v4.new_code_cell("import shutil\narchive=shutil.make_archive(str(WORK.parent/(WORK.name+'_outputs')),'zip',WORK)\nprint(archive)\nDOWNLOAD=False\nif DOWNLOAD:\n    from google.colab import files\n    files.download(archive)")]
 nbformat.write(nb,R/f'FRACTALGO_{lang}.ipynb')
(R/'FRACTALGO_STANDALONE.py').write_text(setup+"\nif __name__=='__main__':\n    raise SystemExit(subprocess.call([sys.executable,str(WORK/'launch.py'),sys.argv[1] if len(sys.argv)>1 else 'ui'],cwd=WORK))\n")
(R/'release').mkdir(exist_ok=True);(R/'release/FractalGo_0.1.0_ES_EN.zip').write_bytes(raw)
print('Payload',len(raw),digest)
