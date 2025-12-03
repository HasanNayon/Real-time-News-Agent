import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class NewsFetcher:
    """Fetches real-time news from NewsAPI"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = 'https://newsapi.org/v2'
        
    def get_top_headlines(self, query=None, category=None, country='us', page_size=5):
        """
        Fetch top headlines from NewsAPI
        
        Args:
            query (str): Keywords or phrases to search for
            category (str): Category of news (business, entertainment, general, health, science, sports, technology)
            country (str): 2-letter ISO 3166-1 code of the country (default: 'us')
            page_size (int): Number of results to return (default: 5, max: 100)
            
        Returns:
            list: List of news articles
        """
        endpoint = f'{self.base_url}/top-headlines'
        
        params = {
            'apiKey': self.api_key,
            'pageSize': page_size,
            'country': country
        }
        
        if query:
            params['q'] = query
        if category:
            params['category'] = category
            
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'ok':
                return self._format_articles(data['articles'])
            else:
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return []
    
    def search_news(self, query, language='en', sort_by='publishedAt', page_size=5):
        """
        Search for news articles
        
        Args:
            query (str): Keywords or phrases to search for
            language (str): Language code (default: 'en')
            sort_by (str): Sort order (relevancy, popularity, publishedAt)
            page_size (int): Number of results to return
            
        Returns:
            list: List of news articles
        """
        endpoint = f'{self.base_url}/everything'
        
        params = {
            'apiKey': self.api_key,
            'q': query,
            'language': language,
            'sortBy': sort_by,
            'pageSize': page_size
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'ok':
                return self._format_articles(data['articles'])
            else:
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error searching news: {e}")
            return []
    
    def _format_articles(self, articles):
        """Format articles for better readability"""
        formatted = []
        for article in articles:
            formatted.append({
                'title': article.get('title', 'No title'),
                'description': article.get('description', 'No description'),
                'content': article.get('content', 'No content'),
                'source': article.get('source', {}).get('name', 'Unknown'),
                'author': article.get('author', 'Unknown'),
                'url': article.get('url', ''),
                'publishedAt': article.get('publishedAt', ''),
                'urlToImage': article.get('urlToImage', '')
            })
        return formatted
