from app.db import SessionLocal
from app.services.rules import scan_all
db=SessionLocal();a=scan_all(db);print(f"Created {len(a)} alerts.")
for x in a:print(x.id,x.rule_name,x.severity,x.score)
db.close()
