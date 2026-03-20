from pathlib import Path
import sys
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

# Ensure project root is on sys.path when running as: python scripts/unmark_recent_digests.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
from app.database.connection import SessionLocal
from app.database import models

session = SessionLocal()
cutoff = datetime.now(timezone.utc) - timedelta(hours=48)

# Find digests created within last 48 hours
q = session.query(models.Digest).filter(models.Digest.created_at >= cutoff)
found = q.count()
print(f'Found {found} digests created since {cutoff.isoformat()}')
ids = []
for d in q.all():
    ids.append(d.id)
    d.sent_at = None
session.commit()
print('Unmarked sent_at for digests:', ids)
session.close()
