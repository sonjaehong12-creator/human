import streamlit as st
import feedparser
from datetime import datetime

# ==========================================
# AI & Digital Education News Dashboard
# 주제:
# AI와 디지털 교육은 교육 불평등을 줄이는가, 심화시키는가?
# ==========================================

st.set_page_config(
    page_title="AI & Digital Education News",
    page_icon="🧠",
    layout="wide"
)

# ------------------------------------------
# RSS 피드 목록
# ------------------------------------------
RSS_FEEDS = {
    "BBC": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "The Guardian": "https://www.theguardian.com/technology/rss",
    "Reuters": "https://feeds.reuters.com/reuters/technologyNews"
}

# ------------------------------------------
# 키워드 설정
# ------------------------------------------
TOPIC_KEYWORDS = [
    "AI education",
    "digital learning",
    "education inequality",
    "online education",
    "edtech",
    "artificial intelligence",
    "digital divide",
    "remote learning"
]

# ------------------------------------------
# 헤드라인 수집 함수
# ------------------------------------------
def fetch_news():
    articles = []
    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title     = getattr(entry, "title", "").strip()
                link      = getattr(entry, "link", "")
                published = getattr(entry, "published", "No date")

                # 날짜 파싱 (published_parsed 우선 사용)
                parsed_date = getattr(entry, "published_parsed", None)
                if parsed_date:
                    try:
                        published = datetime(*parsed_date[:6]).strftime("%Y-%m-%d %H:%M")
                    except Exception:
                        pass

                # 키워드 필터
                if any(kw.lower() in title.lower() for kw in TOPIC_KEYWORDS):
                    articles.append({
                        "title":     title,
                        "link":      link,
                        "published": published,
                        "source":    source
                    })
        except Exception:
            pass  # 피드 파싱 실패 시 조용히 스킵

    # 중복 제목 제거
    seen = set()
    unique = []
    for a in articles:
        key = a["title"].lower()[:80]
        if key not in seen:
            seen.add(key)
            unique.append(a)

    return unique

# ------------------------------------------
# 캐시된 데이터 로드 (함수 정의를 호출보다 먼저)
# ------------------------------------------
@st.cache_data(ttl=300)
def load_data():
    return fetch_news()

# ------------------------------------------
# 제목 영역
# ------------------------------------------
st.title("🧠 AI & Digital Education News Dashboard")
st.markdown(
    """
    실시간 RSS 기반 뉴스 수집  
    주제: **AI와 디지털 교육은 교육 불평등을 줄이는가, 심화시키는가?**
    """
)

# ------------------------------------------
# 새로고침 버튼
# ------------------------------------------
if st.button("🔄 새로고침"):
    st.cache_data.clear()

# ------------------------------------------
# 데이터 로드
# ------------------------------------------
articles = load_data()

# ------------------------------------------
# 검색창
# ------------------------------------------
search_keyword = st.text_input(
    "🔍 키워드 검색",
    placeholder="예: AI, inequality, online learning"
)

# ------------------------------------------
# 검색 필터
# ------------------------------------------
if search_keyword:
    filtered_articles = [
        article for article in articles
        if search_keyword.lower() in article["title"].lower()
    ]
else:
    filtered_articles = articles

# ------------------------------------------
# 결과 표시
# ------------------------------------------
st.subheader(f"📰 뉴스 헤드라인 ({len(filtered_articles)}개)")

if filtered_articles:
    for article in filtered_articles:
        st.markdown("---")
        st.markdown(f"### [{article['title']}]({article['link']})")
        st.caption(f"📅 {article['published']} | 🏢 {article['source']}")
else:
    st.warning("검색 결과가 없습니다.")

# ------------------------------------------
# 하단 설명
# ------------------------------------------
st.markdown("---")
st.markdown(
    """
    ### 📌 사용 RSS 출처
    - BBC Technology
    - The Guardian Technology
    - Reuters Technology

    ### 📌 핵심 키워드
    AI Education, Digital Divide, EdTech, Online Learning, Education Inequality
    """
)
