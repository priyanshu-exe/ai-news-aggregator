from dotenv import load_dotenv
load_dotenv()

from app.agent.digest_agent import DigestAgent

agent = DigestAgent()

# sample content
title = "Test Article: Hugging Face Adapter"
content = "This is a short test article content about AI news. It should be summarized by the Hugging Face adapter if configured correctly."

out = agent.generate_digest(title=title, content=content, article_type='openai')
print('Digest result:')
print(out)
