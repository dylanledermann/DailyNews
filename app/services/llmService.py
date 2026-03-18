import json
from app.config.settings import SETTINGS
from openai import OpenAI

CLASSIFICATION_PROMPT = """
You are a neutral media analysis tool. Your job is to analyze news articles objectively.
You must return ONLY a valid JSON object. Do not include any preamble, explanation, or markdown formatting.

## ARTICLE METADATA
Source: {source_name}
Known Lean: {source_lean}
Title: {title}
Summary: {summary}
{body_note}

## ARTICLE BODY
{body}

## INSTRUCTIONS
Analyze the article above and return this exact JSON structure with no deviations:

{{
    "category": "<category>",
    "political_lean": "<political_lean>",
    "bias_score": <bias_score>,
    "factuality_score": <factuality_score>,
    "tone": "<tone>",
    "bias_reasoning": "<bias_reasoning>",
    "emotional_language": <emotional_language>,
    "summary_ai": "<summary>"
}}

## FIELD DEFINITIONS

"category"
    The primary topic of the article.
    Must be exactly one of:
    Politics | Business | Technology | Science | Health | World |
    Sports | Entertainment | Environment | Crime | Other

"political_lean"
    The political leaning expressed in THIS specific article.
    Assess based on framing, word choice, and which perspectives are centered.
    Note: this may differ from the source's known lean — assess the article itself.
    Must be exactly one of:
    Far-Left | Left | Center-Left | Center | Center-Right | Right | Far-Right | Non-Political

"bias_score"
    A float between 0.0 and 1.0 measuring how biased the article is.
    Consider: loaded language, one-sided sourcing, omission of opposing views,
        emotionally charged framing, unsupported claims.
    0.0 = completely neutral, balanced, all sides represented
    0.5 = moderate bias, some loaded language or one-sided framing
    1.0 = extreme bias, propaganda-like, no opposing perspectives

"factuality_score"
    A float between 0.0 and 1.0 measuring confidence in factual accuracy.
    Consider: presence of named sources, citations, verifiable claims,
              use of hedging language, speculative statements.
    NOTE: You cannot verify claims in real time. Score based on
          journalistic rigor signals only, not ground truth.
    0.0 = entirely opinion, no sourcing, unverifiable claims
    0.5 = mix of fact and opinion, some sourcing
    1.0 = highly factual, well-sourced, verifiable claims throughout

"tone"
    The overall emotional tone of the article.
    Must be exactly one of:
    Neutral | Alarming | Optimistic | Critical | Investigative |
    Sensational | Sympathetic | Cynical

"bias_reasoning"
    An explanation for the bias_score.
    Be specific - cite the framing, language, or sourcing pattern that
    drove the score. Do not repeat the score itself.
    Example: "Article uses charged language like 'radical agenda' and only
        quotes one political perspective without rebuttal."
    Max 2 sentences.

"emotional_language"
    A boolean (true or false) indicating whether the article contains
    emotionally charged or inflammatory language designed to provoke
        a reaction rather than inform.
    true  = contains loaded terms, hyperbole, or fear/anger-inducing framing
    false = language is measured, neutral, and informational

"summary_ai"
    A neutral 2-3 sentence summary of what the article reports.
    Write as if summarizing for someone who has not read it.
    Do not editorialize. Do not include your own opinion.
    Do not begin with 'The article' or 'This article'.

## IMPORTANT RULES
- Return ONLY the JSON object. No text before or after.
- All string fields must use double quotes.
- bias_score and factuality_score must be floats, not strings.
- emotional_language must be a boolean (true/false), not a string.
- If the body is truncated or paywalled, base your analysis on the
  title and any available summary. Set factuality_score to null
  and add a "truncated": true field to your response.
- Do not let the source's known lean override your assessment of
  the article itself — a right-leaning outlet can publish a
  centrist article and vice versa.
- If a value cannot be determine, i.e. not enough information, mark it as a null value.
"""

# LLM querying service to generate article descriptions
class LLMService:
    def __init__(self):
        self.client = OpenAI(
            base_url=SETTINGS["LLM_BASE_URL"],
            api_key=SETTINGS["LLM_API_KEY"]
        )
        self.model = SETTINGS["LLM_MODEL"]

    def classify_article(self, article: dict) -> dict | None:
        body = article.get("body") or article.get("summary", "")
        if not body:
            return None
        
        body_truncated = article.get("body_truncated", 0)
        body_note = "(NOTE: Article body is paywalled/truncated - classify on title and summary only)" \
            if body_truncated else ""
        
        prompt = CLASSIFICATION_PROMPT.format(
            source_name=article["source_name"],
            source_lean=article["source_lean"],
            title=article["title"],
            summary=article["summary"],
            body=article["body"],
            body_note=body_note,
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.1,
                response_format={ "type": "json_object" }
            )
            raw = response.choices[0].message.content.strip()
            return json.loads(raw)
        
        except Exception as e:
            print(f"Error occurred during classification: {e}")
            return None