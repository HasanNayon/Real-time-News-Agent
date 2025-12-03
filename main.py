from news_fetcher import NewsFetcher
from llm_summarizer import LLMSummarizer
import sys

class NewschatBot:
    """Real-time News Chatbot with LLM summarization"""
    
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.summarizer = LLMSummarizer()
        self.current_articles = []
        
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("📰 REAL-TIME NEWS CHATBOT 📰")
        print("="*60)
        print("\nWhat would you like to do?")
        print("1. Get top headlines")
        print("2. Search for specific news")
        print("3. Get news by category")
        print("4. Summarize current news")
        print("5. Ask a question about current news")
        print("6. Exit")
        print("-"*60)
        
    def display_categories(self):
        """Display available categories"""
        print("\nAvailable categories:")
        print("1. Business")
        print("2. Entertainment")
        print("3. General")
        print("4. Health")
        print("5. Science")
        print("6. Sports")
        print("7. Technology")
        
    def get_top_headlines(self):
        """Fetch and display top headlines"""
        print("\n🔍 Fetching top headlines...")
        country = input("Enter country code (default: us, press Enter to skip): ").strip() or 'us'
        
        try:
            page_size = int(input("How many articles? (1-10, default: 5): ").strip() or 5)
            page_size = min(max(page_size, 1), 10)
        except ValueError:
            page_size = 5
        
        self.current_articles = self.news_fetcher.get_top_headlines(country=country, page_size=page_size)
        self._display_articles()
        
    def search_news(self):
        """Search for specific news"""
        query = input("\n🔍 Enter search query: ").strip()
        if not query:
            print("❌ Please enter a search term.")
            return
        
        try:
            page_size = int(input("How many articles? (1-10, default: 5): ").strip() or 5)
            page_size = min(max(page_size, 1), 10)
        except ValueError:
            page_size = 5
        
        print(f"\n🔍 Searching for '{query}'...")
        self.current_articles = self.news_fetcher.search_news(query, page_size=page_size)
        self._display_articles()
        
    def get_category_news(self):
        """Get news by category"""
        self.display_categories()
        categories = {
            '1': 'business',
            '2': 'entertainment',
            '3': 'general',
            '4': 'health',
            '5': 'science',
            '6': 'sports',
            '7': 'technology'
        }
        
        choice = input("\nSelect category (1-7): ").strip()
        category = categories.get(choice)
        
        if not category:
            print("❌ Invalid category selection.")
            return
        
        try:
            page_size = int(input("How many articles? (1-10, default: 5): ").strip() or 5)
            page_size = min(max(page_size, 1), 10)
        except ValueError:
            page_size = 5
        
        print(f"\n🔍 Fetching {category} news...")
        self.current_articles = self.news_fetcher.get_top_headlines(category=category, page_size=page_size)
        self._display_articles()
        
    def summarize_news(self):
        """Summarize current articles using LLM"""
        if not self.current_articles:
            print("\n❌ No articles loaded. Please fetch news first.")
            return
        
        print("\n🤖 Generating summary with AI...")
        summary = self.summarizer.summarize_articles(self.current_articles)
        print("\n" + "="*60)
        print("📝 AI SUMMARY")
        print("="*60)
        print(summary)
        print("="*60)
        
    def ask_question(self):
        """Ask a question about current articles"""
        if not self.current_articles:
            print("\n❌ No articles loaded. Please fetch news first.")
            return
        
        question = input("\n❓ Ask your question: ").strip()
        if not question:
            print("❌ Please enter a question.")
            return
        
        print("\n🤖 Thinking...")
        answer = self.summarizer.answer_question(self.current_articles, question)
        print("\n" + "="*60)
        print("💬 AI ANSWER")
        print("="*60)
        print(answer)
        print("="*60)
        
    def _display_articles(self):
        """Display fetched articles"""
        if not self.current_articles:
            print("\n❌ No articles found.")
            return
        
        print(f"\n✅ Found {len(self.current_articles)} articles:\n")
        print("="*60)
        
        for i, article in enumerate(self.current_articles, 1):
            print(f"\n📰 Article {i}")
            print(f"Title: {article['title']}")
            print(f"Source: {article['source']}")
            print(f"Published: {article['publishedAt']}")
            print(f"Description: {article['description']}")
            print(f"URL: {article['url']}")
            print("-"*60)
        
        print(f"\n✅ {len(self.current_articles)} articles loaded and ready for summarization!")
        
    def run(self):
        """Main application loop"""
        print("\n👋 Welcome to Real-Time News Chatbot!")
        print("This chatbot fetches real-time news and uses AI to summarize and answer questions.")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.get_top_headlines()
            elif choice == '2':
                self.search_news()
            elif choice == '3':
                self.get_category_news()
            elif choice == '4':
                self.summarize_news()
            elif choice == '5':
                self.ask_question()
            elif choice == '6':
                print("\n👋 Thank you for using News Chatbot! Goodbye!")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice. Please select 1-6.")
            
            input("\n⏎ Press Enter to continue...")


if __name__ == "__main__":
    try:
        bot = NewshatBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)
