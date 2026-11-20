from pathlib import Path
import json
from streamlit.testing.v1 import AppTest
R=Path(__file__).resolve().parents[1];rows=[]
for lang in ['Castellano','English']:
 a=AppTest.from_file(str(R/'app.py'),default_timeout=50).run();a.sidebar.selectbox[0].set_value(lang).run()
 for page in list(a.sidebar.radio[0].options):
  a.sidebar.radio[0].set_value(page).run();assert not a.exception,(lang,page,a.exception)
  rows.append(dict(language=lang,page=page,passed=True))
 a.sidebar.radio[0].set_value(a.sidebar.radio[0].options[0]).run()
 [r for r in a.radio if r.label in ['Vista','View']][0].set_value('Profundidad' if lang=='Castellano' else 'Depth').run();assert not a.exception
 a.select_slider[0].set_value(4).run();assert not a.exception
 rows.append(dict(language=lang,page='3D and guided tour',passed=True))
(R/'records/ui_checks.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('PASS',len(rows),'UI checks')
