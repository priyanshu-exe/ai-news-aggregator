from app.database.connection import SessionLocal
from app.database import models

s = SessionLocal()
print('openai count =', s.query(models.OpenAIArticle).count())
print('digests count =', s.query(models.Digest).count())
print('\nSample openai articles:')
for r in s.query(models.OpenAIArticle).limit(5):
    data = {k: v for k, v in r.__dict__.items() if not k.startswith('_')}
    print(data)

print('\nSample digests:')
for r in s.query(models.Digest).order_by(models.Digest.created_at.desc()).limit(5):
    data = {k: v for k, v in r.__dict__.items() if not k.startswith('_')}
    print(data)

s.close()
