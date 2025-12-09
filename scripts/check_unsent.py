from app.database.repository import Repository
from datetime import datetime, timedelta

repo = Repository()
unsent = repo.get_recent_digests(hours=24, exclude_sent=True)
print(f"Unsent digests in last 24h: {len(unsent)}")
for d in unsent:
    print(f"- {d['id']} | title: {d['title']} | created_at: {d['created_at']} | sent_at: {d['sent_at']}")
