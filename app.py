import streamlit as st
import feedparser
from datetime import datetime
import time

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI & 디지털 교육 불평등 뉴스",
    page_icon="🎓",
    layout="wide",
)

# ── CSS 스타일 ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* 배경 */
.stApp {
    background-color: #0d0f14;
    color: #e8eaf0;
}

/* 헤더 */
.hero-header {
    border-left: 4px solid #00e5ff;
    padding: 1.2rem 1.5rem;
    margin-bottom: 2rem;
    background: linear-gradient(90deg, rgba(0,229,255,0.07) 0%, transparent 100%);
}
.hero-header h1 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    color: #00e5ff;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}
.hero-header p {
    font-size: 0.85rem;
    color: #7a8090;
    margin: 0;
    font-family: 'IBM Plex Mono', monospace;
}

/* 통계 배지 */
.stat-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.stat-badge {
    background: #161820;
    border: 1px solid #2a2d38;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: #7a8090;
}
.stat-badge span {
    color: #00e5ff;
    font-weight: 600;
}

/* 카드 */
.news-card {
    background: #161820;
    border: 1px solid #2a2d38;
    border-radius: 8px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s, transform 0.15s;
    position: relative;
    overflow: hidden;
}
.news-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: #00e5ff;
    opacity: 0;
    transition: opacity 0.2s;
}
.news-card:hover {
    border-color: #00e5ff;
    transform: translateX(3px);
}
.news-card:hover::before {
    opacity: 1;
}
.news-card a {
    text-decoration: none;
    color: inherit;
}
.news-title {
    font-size: 0.97rem;
    font-weight: 600;
    color: #dde1ee;
    line-height: 1.4;
    margin-bottom: 0.5rem;
}
.news-title:hover {
    color: #00e5ff;
}
.news-meta {
    display: flex;
    gap: 1rem;
    align-items: center;
    flex-wrap: wrap;
}
.source-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.15rem 0.55rem;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.source-bbc    { background: rgba(255,80,80,0.15);  color: #ff7070; border: 1px solid rgba(255,80,80,0.3); }
.source-guardian { background: rgba(0,229,255,0.1); color: #00e5ff; border: 1px solid rgba(0,229,255,0.25); }
.source-reuters  { background: rgba(255,190,60,0.1); color: #ffbe3c; border: 1px solid rgba(255,190,60,0.25); }
.source-default  { background: rgba(160,160,200,0.1); color: #a0a0c8; border: 1px solid rgba(160,160,200,0.2); }

.news-date {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #4a5060;
}

/* 검색창 */
div[data-testid="stTextInput"] input {
    background: #161820 !important;
    border: 1px solid #2a2d38 !important;
    border-radius: 6px !important;
    color: #e8eaf0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.88rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #00e5ff !important;
    box-shadow: 0 0 0 2px rgba(0,229,255,0.15) !important;
}

/* 버튼 */
div[data-testid="stButton"] button {
    background: transparent !important;
    border: 1px solid #00e5ff !important;
    color: #00e5ff !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    border-radius: 6px !important;
    padding: 0.45rem 1.2rem !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] button:hover {
    background: rgba(0,229,255,0.1) !important;
}

/* 구분선 */
hr { border-color: #2a2d38 !important; }

/* 필터 없음 메시지 */
.no-result {
    text-align: center;
    padding: 3rem;
    color: #4a5060;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
}

/* 섹션 레이블 */
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #4a5060;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.8rem;
}

/* 스크롤바 */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d0f14; }
::-webkit-scrollbar-thumb { background: #2a2d38; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── RSS 피드 설정 ─────────────────────────────────────────────
RSS_FEEDS = {
    "BBC": [
        "http://feeds.bbci.co.uk/news/education/rss.xml",
        "http://feeds.bbci.co.uk/news/technology/rss.xml",
    ],
    "The Guardian": [
        "https://www.theguardian.com/education/rss",
        "https://www.theguardian.com/technology/rss",
        "https://www.theguardian.com/inequality/rss",
    ],
    "Reuters": [
        "https://feeds.reuters.com/reuters/technologyNews",
        "https://feeds.reuters.com/reuters/educationNews",
    ],
}

KEYWORDS = [
    "artificial intelligence", "AI education", "digital divide",
    "edtech", "online learning", "education inequality",
    "digital equity", "educational technology", "e-learning",
    "ChatGPT", "generative AI", "algorithmic bias",
    "digital literacy", "access to education", "remote learning",
]

# ── 함수 ─────────────────────────────────────────────────────
def parse_date(entry):
    for attr in ("published_parsed", "updated_parsed"):
        val = getattr(entry, attr, None)
        if val:
            try:
                return datetime(*val[:6])
            except Exception:
                pass
    return None

def source_css_class(source):
    s = source.lower()
    if "bbc" in s:       return "source-bbc"
    if "guardian" in s:  return "source-guardian"
    if "reuters" in s:   return "source-reuters"
    return "source-default"

def is_relevant(title: str, summary: str) -> bool:
    text = (title + " " + summary).lower()
    return any(kw.lower() in text for kw in KEYWORDS)

@st.cache_data(ttl=300, show_spinner=False)
def fetch_headlines():
    articles = []
    for source, urls in RSS_FEEDS.items():
        for url in urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    title   = getattr(entry, "title",   "").strip()
                    link    = getattr(entry, "link",    "#")
                    summary = getattr(entry, "summary", "")
                    if not title:
                        continue
                    if not is_relevant(title, summary):
                        continue
                    pub = parse_date(entry)
                    articles.append({
                        "title":  title,
                        "link":   link,
                        "source": source,
                        "date":   pub,
                    })
            except Exception:
                pass

    # 중복 제목 제거 + 최신순 정렬
    seen = set()
    unique = []
    for a in articles:
        key = a["title"].lower()[:80]
        if key not in seen:
            seen.add(key)
            unique.append(a)

    unique.sort(key=lambda x: x["date"] or datetime.min, reverse=True)
    return unique

def render_card(article):
    src_cls = source_css_class(article["source"])
    date_str = article["date"].strftime("%Y-%m-%d  %H:%M") if article["date"] else "—"
    st.markdown(f"""
    <div class="news-card">
        <a href="{article['link']}" target="_blank" rel="noopener noreferrer">
            <div class="news-title">{article['title']}</div>
        </a>
        <div class="news-meta">
            <span class="source-tag {src_cls}">{article['source']}</span>
            <span class="news-date">{date_str}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── 헤더 ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1>🎓 AI & Digital Education</h1>
    <p>Does AI widen or close the education gap? · Real-time headlines from BBC · The Guardian · Reuters</p>
</div>
""", unsafe_allow_html=True)

# ── 컨트롤 바 ─────────────────────────────────────────────────
col_search, col_btn, col_space = st.columns([4, 1.2, 2])

with col_search:
    query = st.text_input(
        label="",
        placeholder="🔍  Filter by keyword  (e.g. ChatGPT, digital divide, equity ...)",
        label_visibility="collapsed",
    )

with col_btn:
    refresh = st.button("⟳  Refresh", use_container_width=True)

if refresh:
    st.cache_data.clear()

# ── 데이터 로드 ───────────────────────────────────────────────
with st.spinner("Fetching latest headlines …"):
    all_articles = fetch_headlines()

# ── 필터 적용 ─────────────────────────────────────────────────
if query.strip():
    q = query.strip().lower()
    filtered = [a for a in all_articles if q in a["title"].lower()]
else:
    filtered = all_articles

# ── 통계 배지 ─────────────────────────────────────────────────
now_str = datetime.now().strftime("%Y-%m-%d  %H:%M")
st.markdown(f"""
<div class="stat-row">
    <div class="stat-badge">Total&nbsp;<span>{len(all_articles)}</span>&nbsp;articles</div>
    <div class="stat-badge">Showing&nbsp;<span>{len(filtered)}</span>&nbsp;results</div>
    <div class="stat-badge">Updated&nbsp;<span>{now_str}</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Latest Headlines</div>', unsafe_allow_html=True)

# ── 기사 렌더링 ───────────────────────────────────────────────
if filtered:
    for article in filtered:
        render_card(article)
else:
    st.markdown("""
    <div class="no-result">
        No headlines matched your filter.<br>Try a different keyword.
    </div>
    """, unsafe_allow_html=True)

# ── 푸터 ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<p style="text-align:center; font-family:'IBM Plex Mono',monospace; font-size:0.72rem; color:#4a5060;">
    Data sourced from public RSS feeds · Auto-refreshes every 5 minutes · No API key required
</p>
""", unsafe_allow_html=True)
