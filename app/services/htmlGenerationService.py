import os

from app.config.settings import SETTINGS
from app.repo.articleRepo import ArticleRepo


class HTMLGenerationService:
    def __init__(self):
        self.loc = SETTINGS["HTML_GENERATION_PATH"]
        self.repo = ArticleRepo()

    def generateHtml(self) -> None:
        articles = self.repo.get_recent_articles()
        formattedArticles = []
        for article in articles:
            formattedArticles.append(ARTICLE_TEMPLATE.format(
                category=(article.get("category") or "other").strip().lower(),
                source=article.get("source_name", ""),
                article_title=article.get("title", ""),
                article_summary_ai="article_summary_ai" if \
                    (not article.get("summary") or article.get("body_truncated", 0)) \
                    else "",
                summary=article.get("summary_ai", "") if \
                    (not article.get("summary") or article.get("body_truncated", 0)) \
                    else article.get("summary"),
                bias_width=f"{(article.get("bias_score") or 0)*100:.2f}%",
                bias_value=f"{(article.get("bias_score") or 0):.2f}",
                factuality_width=f"{(article.get("factuality_score") or 0)*100:.2f}%",
                factuality_value=f"{(article.get("factuality_score") or 0):.2f}",
                tone_value=article.get("tone", "Neutral"),
                emotional_value="Yes" if article.get("emotional_language", 0) else "No",
                bias_reasoning=article.get("bias_reasoning", "")
            ))
        # Create html file in location if it does not exist
        try:
            with open(self.loc, 'w', encoding="utf-8") as f:
                f.write(HTML_TEMPLATE.format(
                    data="\n".join(formattedArticles)
                ))
        except Exception as e:
            print(f"Error occurred during HTML generation: {e}")
            return
        print(f"HTML Generated At {self.loc}.")

ARTICLE_TEMPLATE = """
<a class="card {category}" href="">
    <div class="article-metadata">
        <div class="source-row">
            <span class="source-name">{source}</span>
        </div>
        <span class="article-published">September 4, 2021</span>
    </div>
    <span class="article-title">{article_title}</span>
    <p class="article-summary {article_summary_ai}">
        {summary}
    </p>

    <div class="card-divider"></div>
    
    <div class="article-metrics">
        <div class="score-bar">
            <span class="score-bar-label">Bias</span>
            <div class="score-bar-track">
                <div class="score-bar-fill score-bar-fill-bias" style="width: {bias_width}"></div>
            </div>
            <span class="score-bar-value">{bias_value}/1.0</span>
        </div>
        <div class="score-bar">
            <span class="score-bar-label">Factuality</span>
            <div class="score-bar-track">
                <div class="score-bar-fill score-bar-fill-factual" style="width: {factuality_width}"></div>
            </div>
            <span class="score-bar-value">{factuality_value}/1.0</span>
        </div>
        <div class="metric">
            <span class="metric-label">Tone</span>
            <span class="metric-value">{tone_value}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Emotional</span>
            <span class="metric-value">{emotional_value}</span>
        </div>
    </div>
    <p class="metric-reasoning">
        {bias_reasoning}
    </p>
</a>
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="header">
        <span id="title">News</span>
    </div>
    <div id="body-container">
        <nav id="menu-sidebar">
            <div id="sidebar-label">Categories</div>
            <a href="?category=world" class="sidebar-item active" data-category="world">World</a>
            <a href="?category=politics" class="sidebar-item" data-category="politics">Politics</a>
            <a href="?category=business" class="sidebar-item" data-category="business">Business</a>
            <a href="?category=technology" class="sidebar-item" data-category="technology">Technology</a>
            <a href="?category=science" class="sidebar-item" data-category="science">Science</a>
            <a href="?category=health" class="sidebar-item" data-category="health">Health</a>
            <a href="?category=sports" class="sidebar-item" data-category="sports">Sports</a>
            <a href="?category=entertainment" class="sidebar-item" data-category="entertainment">Entertainment</a>
            <a href="?category=environment" class="sidebar-item" data-category="environment">Environment</a>
            <a href="?category=crime" class="sidebar-item" data-category="crime">Crime</a>
            <a href="?category=other" class="sidebar-item" data-category="other">Other</a>
        </nav>
        <div id="main">
            <h1 id="category-heading" class="main-heading"></h1>
            <div id="cards-grid" class="cards-grid">
                {data}
            </div>
            </main>
        </div>
            </div>
        </div>
    </div>
    <script>
        (function () {{
            const params = new URLSearchParams(window.location.search);
            const active = params.get("category") || "world";
            const heading = document.getElementById("category-heading");
            const items = document.querySelectorAll(".sidebar-item");
        
            items.forEach(function (item) {{
                item.classList.remove('active');
                if (item.dataset.category === active) {{
                    item.classList.add('active');
                    heading.textContent =
                        active.charAt(0).toUpperCase() + active.slice(1) + ' News';
                    }}
                }});
            }})();
            const params = new URLSearchParams(window.location.search);
            const active = params.get("category") || "world";
            const articles = document.querySelectorAll(".card");
            articles.forEach(article => {{
                console.log(article.classList);
                console.log(active);
                if(article.classList.contains(active)){{
                    console.log("contains")
                    article.hidden=false;
                }} else {{
                    article.hidden=true;
            }}
        }});
            
    </script>
</body>
</html>
"""