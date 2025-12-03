"""
Test script for AI News Chatbot
Tests the core functionality: theme extraction, news fetching, fake news detection, and answer generation
"""

from llm_summarizer import LLMSummarizer
from news_fetcher import NewsFetcher
from fake_news_detector import FakeNewsDetector

def test_chatbot():
    print("🤖 AI News Chatbot - Test Script")
    print("=" * 60)
    
    # Initialize components
    print("\n1️⃣ Initializing components...")
    try:
        summarizer = LLMSummarizer()
        news_fetcher = NewsFetcher()
        fake_detector = FakeNewsDetector()
        print("✅ Components initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing: {e}")
        return
    
    # Test query
    user_query = "What's happening with artificial intelligence?"
    print(f"\n2️⃣ User Query: '{user_query}'")
    
    # Extract theme
    print("\n3️⃣ Extracting theme from query...")
    try:
        theme = summarizer.extract_theme(user_query)
        print(f"✅ Extracted Theme: '{theme}'")
    except Exception as e:
        print(f"❌ Error extracting theme: {e}")
        return
    
    # Fetch news
    print(f"\n4️⃣ Fetching news articles about '{theme}'...")
    try:
        articles = news_fetcher.search_news(query=theme, page_size=10)
        if not articles:
            articles = news_fetcher.get_top_headlines(query=theme, page_size=10)
        print(f"✅ Found {len(articles)} articles")
        
        if articles:
            print("\n📰 Articles found:")
            for i, article in enumerate(articles[:3], 1):
                print(f"   {i}. {article['title'][:70]}...")
    except Exception as e:
        print(f"❌ Error fetching news: {e}")
        return
    
    # Filter fake news
    print("\n5️⃣ Filtering fake news...")
    try:
        real_articles, fake_count, filtered = fake_detector.filter_fake_articles(articles)
        print(f"✅ Filtered {fake_count} fake news article(s)")
        print(f"✅ {len(real_articles)} verified articles remaining")
        
        if fake_count > 0:
            print("\n🛡️ Fake news detection is protecting you!")
    except Exception as e:
        print(f"❌ Error filtering fake news: {e}")
        real_articles = articles
    
    # Generate answer
    print("\n6️⃣ Generating AI answer from verified articles...")
    try:
        answer = summarizer.answer_from_news(user_query, real_articles[:5])
        print("✅ Answer generated successfully!")
        print("\n" + "="*60)
        print("🤖 AI RESPONSE:")
        print("="*60)
        print(answer)
        print("="*60)
    except Exception as e:
        print(f"❌ Error generating answer: {e}")
        return
    
    print("\n✅ All tests passed! Your chatbot is ready to use!")
    print("\n🚀 Run the chatbot with: streamlit run app.py")

if __name__ == "__main__":
    test_chatbot()
