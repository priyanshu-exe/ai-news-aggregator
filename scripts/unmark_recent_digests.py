from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()
from app.database.connection import SessionLocal
from app.database import models

session = SessionLocal()
cutoff = datetime.utcnow() - timedelta(hours=48)

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
