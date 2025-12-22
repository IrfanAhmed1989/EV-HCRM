from pathlib import Path
import json, re

# 1) Write config.json (uses your password: iiii)
cfg={'host':'127.0.0.1','port':3306,'user':'root','password':'iiii','database':'ev_hcrm'}
Path('config.json').write_text(json.dumps(cfg, indent=2))
print('config.json written ✅')

# 2) Patch DAL.py to use TCP host/port instead of unix_socket
dal_p=Path('DAL.py'); dal=dal_p.read_text()
dal=dal.replace('unix_socket="/tmp/mysql.sock",', 'host=host,\n                port=port,')
dal_p.write_text(dal)
print('DAL.py patched ✅')

# 3) Patch BLL.py to read config.json and pass creds to DAL.connect()
bll_p=Path('BLL.py'); bll=bll_p.read_text()
if 'import json' not in bll: bll=bll.replace('from datetime import datetime', 'from datetime import datetime\nimport json')
if 'from pathlib import Path' not in bll: bll=bll.replace('import json', 'import json\nfrom pathlib import Path')
bll=bll.replace('self._db.connect(host="127.0.0.1", port=3306, user="root", password="iiii", database="ev_hcrm")', "cfg = json.loads(Path('config.json').read_text())\n        self._db.connect(host=cfg['host'], port=cfg['port'], user=cfg['user'], password=cfg['password'], database=cfg.get('database','ev_hcrm'))")
bll_p.write_text(bll)
print('BLL.py patched ✅')
