from app.database.repository import Repository
from app.database import models
from datetime import datetime, timezone

repo = Repository()

# Get unsent digests from last 24h
unsent = repo.get_recent_digests(hours=24, exclude_sent=True)
print(f'Unsent digests (last 24h): {len(unsent)}')
for d in unsent[:5]:
    print(f'  - {d["id"]} | created: {d["created_at"]} | sent: {d["sent_at"]}')

# Get all recent digests (including sent) ordered by creation time
print(f'\nAll digests (last 10, including sent):')
all_recent = repo.session.query(models.Digest).order_by(models.Digest.created_at.desc()).limit(10).all()
for d in all_recent:
    print(f'  - {d.id} | created: {d.created_at} | sent: {d.sent_at}')

repo.session.close()
