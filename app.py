import streamlit as st
from news_fetcher import NewsFetcher
from llm_summarizer import LLMSummarizer
from fake_news_detector import FakeNewsDetector
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI News Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .user-message {
        padding: 1rem;
        border-radius: 10px;
        background-color: #E3F2FD;
        margin-bottom: 1rem;
        border-left: 4px solid #1E88E5;
    }
    .bot-message {
        padding: 1rem;
        border-radius: 10px;
        background-color: #F5F5F5;
        margin-bottom: 1rem;
        border-left: 4px solid #4CAF50;
    }
    .article-preview {
        padding: 0.8rem;
        border-radius: 8px;
        background-color: #FAFAFA;
        margin: 0.5rem 0;
        border-left: 3px solid #FF9800;
        font-size: 0.9rem;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'news_fetcher' not in st.session_state:
    st.session_state.news_fetcher = NewsFetcher()
    st.session_state.summarizer = LLMSummarizer()
    st.session_state.fake_detector = FakeNewsDetector()
    st.session_state.chat_history = []
    st.session_state.current_articles = []

# Title
st.markdown('<h1 class="main-header">🤖 AI News Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: gray;">Ask me anything about current events - I\'ll find the latest news and answer your questions!</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Number of articles to fetch
    num_articles = st.slider("Articles to fetch per query", 3, 10, 5, 
                             help="Number of news articles to search and analyze")
    
    # Country selection
    country = st.selectbox(
        "News Region",
        ["us", "gb", "ca", "au", "in"],
        format_func=lambda x: {
            "us": "🇺🇸 United States",
            "gb": "🇬🇧 United Kingdom",
            "ca": "🇨🇦 Canada",
            "au": "🇦🇺 Australia",
            "in": "🇮🇳 India"
        }[x],
        help="Select the region for news search"
    )
    
    st.markdown("---")
    
    # Chat history management
    st.subheader("💬 Chat Management")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.current_articles = []
        st.rerun()
    
    if st.session_state.chat_history:
        st.info(f"💬 {len(st.session_state.chat_history)} messages in history")
    
    st.markdown("---")
    
    # Example queries
    st.subheader("💡 Example Queries")
    st.markdown("""
    - What's happening with AI?
    - Latest news on climate change
    - Tell me about Tesla stock
    - Any updates on space exploration?
    - What's going on with elections?
    - Recent developments in technology
    """)
    
    st.markdown("---")
    st.caption("Powered by NewsAPI & Groq AI")

# Main chat interface
st.markdown("---")

# Chat display area
chat_container = st.container()

with chat_container:
    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.markdown(f'<div class="user-message">', unsafe_allow_html=True)
                st.markdown(f"**👤 You:** {msg['content']}")
                st.caption(msg['timestamp'].strftime('%I:%M %p'))
                st.markdown('</div>', unsafe_allow_html=True)
            
            elif msg['role'] == 'assistant':
                st.markdown(f'<div class="bot-message">', unsafe_allow_html=True)
                st.markdown(f"**🤖 AI Assistant:**")
                st.markdown(msg['content'])
                
                # Show fake news filtering info
                if msg.get('fake_filtered', 0) > 0:
                    st.info(f"🛡️ Filtered out {msg['fake_filtered']} fake news article(s)")
                
                # Show articles used
                if 'articles' in msg and msg['articles']:
                    with st.expander(f"📰 {len(msg['articles'])} verified news sources analyzed"):
                        for idx, article in enumerate(msg['articles'][:5], 1):
                            st.markdown(f'<div class="article-preview">', unsafe_allow_html=True)
                            st.markdown(f"**{idx}. {article['title']}**")
                            st.caption(f"{article['source']} · {article.get('publishedAt', 'Unknown')}")
                            if article.get('url'):
                                st.markdown(f"[Read full article →]({article['url']})")
                            st.markdown('</div>', unsafe_allow_html=True)
                
                st.caption(msg['timestamp'].strftime('%I:%M %p'))
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👋 Welcome! Ask me anything about current news and I'll search for the latest articles to answer your question.")
        
        # Example queries as buttons
        st.markdown("#### Try asking:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📱 What's happening with AI?"):
                user_query = "What's happening with AI?"
                st.session_state.trigger_query = user_query
                st.rerun()
            if st.button("🌍 Latest on climate change"):
                user_query = "Latest on climate change"
                st.session_state.trigger_query = user_query
                st.rerun()
        with col2:
            if st.button("🚀 Space exploration updates"):
                user_query = "Space exploration updates"
                st.session_state.trigger_query = user_query
                st.rerun()
            if st.button("💼 Technology trends"):
                user_query = "Technology trends"
                st.session_state.trigger_query = user_query
                st.rerun()

# Input area at the bottom
st.markdown("---")
col1, col2 = st.columns([6, 1])

with col1:
    user_input = st.text_input(
        "Ask about current news...",
        placeholder="e.g., What's the latest on artificial intelligence?",
        key="user_input",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("📤 Send", use_container_width=True, type="primary")

# Handle triggered query from example buttons
if 'trigger_query' in st.session_state:
    user_input = st.session_state.trigger_query
    del st.session_state.trigger_query
    send_button = True

# Process user input
if send_button and user_input:
    # Add user message to chat
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now()
    })
    
    # Show processing status
    with st.spinner("🔍 Extracting theme..."):
        # Extract theme from query
        theme = st.session_state.summarizer.extract_theme(user_input)
        st.toast(f"Searching for: {theme}", icon="🔍")
    
    with st.spinner("📰 Fetching news articles..."):
        # Fetch news based on theme
        articles = st.session_state.news_fetcher.search_news(
            query=theme,
            page_size=num_articles * 2  # Fetch more to account for filtering
        )
        
        if not articles:
            # Try getting top headlines if search fails
            articles = st.session_state.news_fetcher.get_top_headlines(
                query=theme,
                country=country,
                page_size=num_articles * 2
            )
        
        st.toast(f"Found {len(articles)} articles", icon="📰")
    
    with st.spinner("🛡️ Filtering fake news..."):
        # Filter out fake news
        real_articles, fake_count, _ = st.session_state.fake_detector.filter_fake_articles(articles)
        
        if fake_count > 0:
            st.toast(f"🚫 Filtered out {fake_count} fake news articles", icon="🛡️")
        
        # Limit to requested number
        real_articles = real_articles[:num_articles]
        
        if not real_articles:
            st.error("❌ No reliable news articles found after filtering. Try a different topic.")
            st.stop()
    
    with st.spinner("🤖 Analyzing news and generating answer..."):
        # Generate AI response using only real news
        answer = st.session_state.summarizer.answer_from_news(user_input, real_articles)
        
        # Add assistant response to chat
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': answer,
            'articles': real_articles,
            'timestamp': datetime.now(),
            'fake_filtered': fake_count
        })
    
    st.rerun()

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        🤖 AI News Chatbot | Powered by NewsAPI & Groq AI<br>
        <a href='https://github.com/HasanNayon/Real-time-News-Agent' target='_blank'>View on GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)
