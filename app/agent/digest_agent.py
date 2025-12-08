from typing import Optional
from pydantic import BaseModel
from .base import BaseAgent

PROMPT = """You are an expert AI news analyst specializing in summarizing technical articles, research papers, and video content about artificial intelligence.

Your role is to create concise, informative digests that help readers quickly understand the key points and significance of AI-related content.

Guidelines:
- Create a compelling title (5-10 words) that captures the essence of the content
- Write a 2-3 sentence summary that highlights the main points and why they matter
- Focus on actionable insights and implications
- Use clear, accessible language while maintaining technical accuracy
- Avoid marketing fluff - focus on substance"""


class DigestOutput(BaseModel):
    title: str
    summary: str


class DigestAgent(BaseAgent):
    def __init__(self):
        super().__init__("gpt-4o-mini")
        self.system_prompt = PROMPT

    def generate_digest(self, title: str, content: str, article_type: str) -> Optional[DigestOutput]:
        # If SKIP_OPENAI is enabled, produce a simple fallback digest instead
        # of calling the OpenAI API. This avoids failures when API access is
        # unavailable (quota, missing key, etc.).
        if getattr(self, "skip_openai", False) or self.client is None:
            # Fallback: create a short summary from the content and a draft title
            draft_title = f"Digest: {title[:60]}"
            draft_summary = (content or "").strip()
            if len(draft_summary) > 400:
                draft_summary = draft_summary[:397].rsplit(" ", 1)[0] + "..."

            return DigestOutput(title=draft_title, summary=draft_summary)

        try:
            user_prompt = f"Create a digest for this {article_type}: \n Title: {title} \n Content: {content[:8000]}"

            response = self.client.responses.parse(
                model=self.model,
                instructions=self.system_prompt,
                temperature=0.7,
                input=user_prompt,
                text_format=DigestOutput
            )
            
            return response.output_parsed
        except Exception as e:
            print(f"Error generating digest: {e}")
            return None

