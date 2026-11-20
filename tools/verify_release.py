from pathlib import Path
import json,ast,base64,hashlib,zipfile,io,nbformat,subprocess,tempfile,sys
R=Path(__file__).resolve().parents[1]
checks={}
ledger=json.loads((R/'provenance/IMPORTED_FILES.json').read_text())
checks['imported_files_unchanged']=all(hashlib.sha256((R/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in ledger)
run=json.loads((R/'records/execution_all.json').read_text());checks['reproduction_succeeded']=run['success'] and run['inputs_unchanged']
checks['ui_bilingual']=len(json.loads((R/'records/ui_checks.json').read_text()))==10
for lang in ['ES','EN']:
 nb=nbformat.read(R/f'FRACTALGO_{lang}.ipynb',as_version=4);nbformat.validate(nb)
 source=nb.cells[1].source;v={}
 for line in source.splitlines():
  if line.startswith(('PAYLOAD=','PAYLOAD_SHA256=')):
   k,s=line.split('=',1);v[k]=ast.literal_eval(s)
 raw=base64.b64decode(v['PAYLOAD']);assert hashlib.sha256(raw).hexdigest()==v['PAYLOAD_SHA256']
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert z.testzip() is None
  assert not any(Path(n).name.startswith(('PAPER_','SUPPLEMENTARY_','ASSESSMENT_')) for n in z.namelist())
  assert z.read('research/fractalgo/core.py')==(R/'research/fractalgo/core.py').read_bytes()
  if lang=='ES':
   with tempfile.TemporaryDirectory() as d:
    z.extractall(d);r=subprocess.run([sys.executable,'run.py','test'],cwd=d,capture_output=True,text=True);assert r.returncode==0,r.stderr
 checks['notebook_'+lang]=True
checks['no_fabricated_DOI']='doi:' not in (R/'CITATION.cff').read_text()
assert all(checks.values()),checks
(R/'records/distribution_verification.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
