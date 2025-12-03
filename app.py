import streamlit as st
from news_fetcher import NewsFetcher
from llm_summarizer import LLMSummarizer
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Real-Time News Chatbot",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .article-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
        border-left: 5px solid #1E88E5;
    }
    .summary-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #e3f2fd;
        border-left: 5px solid #0D47A1;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'news_fetcher' not in st.session_state:
    st.session_state.news_fetcher = NewsFetcher()
    st.session_state.summarizer = LLMSummarizer()
    st.session_state.current_articles = []
    st.session_state.chat_history = []

# Title
st.markdown('<h1 class="main-header">📰 Real-Time News Chatbot</h1>', unsafe_allow_html=True)
st.markdown("### Get the latest news and AI-powered summaries")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # News source selection
    news_source = st.radio(
        "Select News Source:",
        ["Top Headlines", "Search News", "Category News"]
    )
    
    st.markdown("---")
    
    # Configuration based on selection
    if news_source == "Top Headlines":
        st.subheader("📊 Top Headlines")
        country = st.selectbox(
            "Select Country",
            ["us", "gb", "ca", "au", "in", "de", "fr", "jp", "cn", "br"],
            format_func=lambda x: {
                "us": "🇺🇸 United States",
                "gb": "🇬🇧 United Kingdom",
                "ca": "🇨🇦 Canada",
                "au": "🇦🇺 Australia",
                "in": "🇮🇳 India",
                "de": "🇩🇪 Germany",
                "fr": "🇫🇷 France",
                "jp": "🇯🇵 Japan",
                "cn": "🇨🇳 China",
                "br": "🇧🇷 Brazil"
            }[x]
        )
        num_articles = st.slider("Number of Articles", 1, 10, 5)
        
        if st.button("🔍 Fetch Headlines", use_container_width=True):
            with st.spinner("Fetching top headlines..."):
                st.session_state.current_articles = st.session_state.news_fetcher.get_top_headlines(
                    country=country,
                    page_size=num_articles
                )
                if st.session_state.current_articles:
                    st.success(f"✅ Loaded {len(st.session_state.current_articles)} articles!")
                else:
                    st.error("❌ No articles found.")
    
    elif news_source == "Search News":
        st.subheader("🔍 Search News")
        search_query = st.text_input("Enter search keywords", placeholder="e.g., artificial intelligence")
        num_articles = st.slider("Number of Articles", 1, 10, 5)
        
        if st.button("🔍 Search", use_container_width=True) and search_query:
            with st.spinner(f"Searching for '{search_query}'..."):
                st.session_state.current_articles = st.session_state.news_fetcher.search_news(
                    query=search_query,
                    page_size=num_articles
                )
                if st.session_state.current_articles:
                    st.success(f"✅ Found {len(st.session_state.current_articles)} articles!")
                else:
                    st.error("❌ No articles found.")
    
    else:  # Category News
        st.subheader("📑 Browse by Category")
        category = st.selectbox(
            "Select Category",
            ["business", "entertainment", "general", "health", "science", "sports", "technology"],
            format_func=lambda x: x.capitalize()
        )
        num_articles = st.slider("Number of Articles", 1, 10, 5)
        
        if st.button("🔍 Fetch News", use_container_width=True):
            with st.spinner(f"Fetching {category} news..."):
                st.session_state.current_articles = st.session_state.news_fetcher.get_top_headlines(
                    category=category,
                    page_size=num_articles
                )
                if st.session_state.current_articles:
                    st.success(f"✅ Loaded {len(st.session_state.current_articles)} articles!")
                else:
                    st.error("❌ No articles found.")
    
    st.markdown("---")
    
    # Action buttons
    st.subheader("🤖 AI Actions")
    
    if st.button("📝 Summarize All Articles", use_container_width=True, disabled=len(st.session_state.current_articles) == 0):
        with st.spinner("Generating AI summary..."):
            summary = st.session_state.summarizer.summarize_articles(st.session_state.current_articles)
            st.session_state.chat_history.append({
                "type": "summary",
                "content": summary,
                "timestamp": datetime.now()
            })
    
    if st.button("🗑️ Clear All", use_container_width=True):
        st.session_state.current_articles = []
        st.session_state.chat_history = []
        st.rerun()

# Main content area
if not st.session_state.current_articles:
    # Welcome message
    st.info("👈 Select a news source from the sidebar to get started!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📊 Top Headlines")
        st.write("Get the latest breaking news from around the world")
    with col2:
        st.markdown("### 🔍 Search News")
        st.write("Find articles about specific topics or keywords")
    with col3:
        st.markdown("### 📑 Category News")
        st.write("Browse news by category: Business, Tech, Sports, etc.")
    
else:
    # Display articles
    st.header(f"📰 Articles ({len(st.session_state.current_articles)})")
    
    # Create tabs for articles and chat
    tab1, tab2 = st.tabs(["📄 Articles", "💬 Chat & Summaries"])
    
    with tab1:
        for idx, article in enumerate(st.session_state.current_articles, 1):
            with st.container():
                st.markdown(f'<div class="article-card">', unsafe_allow_html=True)
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"### {idx}. {article['title']}")
                with col2:
                    if article['urlToImage']:
                        st.image(article['urlToImage'], width=100)
                
                st.markdown(f"**Source:** {article['source']} | **Published:** {article['publishedAt']}")
                st.markdown(f"**Description:** {article['description']}")
                
                with st.expander("Read more..."):
                    if article['content']:
                        st.write(article['content'])
                    st.markdown(f"[🔗 Read full article]({article['url']})")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        # Q&A Interface
        st.subheader("💬 Ask Questions About the Articles")
        
        question = st.text_input("Ask a question about the news:", placeholder="e.g., What are the main topics covered?")
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("📤 Ask", use_container_width=True) and question:
                with st.spinner("Thinking..."):
                    answer = st.session_state.summarizer.answer_question(
                        st.session_state.current_articles,
                        question
                    )
                    st.session_state.chat_history.append({
                        "type": "qa",
                        "question": question,
                        "answer": answer,
                        "timestamp": datetime.now()
                    })
                    st.rerun()
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("---")
            st.subheader("📝 History")
            
            for item in reversed(st.session_state.chat_history):
                if item['type'] == 'summary':
                    st.markdown(f'<div class="summary-box">', unsafe_allow_html=True)
                    st.markdown("**📝 AI Summary**")
                    st.markdown(f"*{item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}*")
                    st.write(item['content'])
                    st.markdown('</div>', unsafe_allow_html=True)
                elif item['type'] == 'qa':
                    st.markdown(f'<div class="summary-box">', unsafe_allow_html=True)
                    st.markdown(f"**❓ Question:** {item['question']}")
                    st.markdown(f"*{item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}*")
                    st.markdown(f"**💬 Answer:**")
                    st.write(item['answer'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info("💡 Generate a summary or ask questions to see them here!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        Built with ❤️ using Streamlit, NewsAPI, and Groq AI | 
        <a href='https://github.com/HasanNayon/Real-time-News-Agent' target='_blank'>GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)
