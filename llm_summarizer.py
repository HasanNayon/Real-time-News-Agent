import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMSummarizer:
    """LLM-based summarizer and query analyzer using Groq"""
    
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"  # Updated to current model
        
    def extract_theme(self, user_query):
        """
        Extract the main theme/keywords from user query for news search
        
        Args:
            user_query (str): User's question or query
            
        Returns:
            str: Extracted theme/keywords for news search
        """
        prompt = f"""You are a news search assistant. Extract the main theme, topic, or keywords from the user's query that would be best for searching news articles.

User Query: "{user_query}"

Return ONLY the search keywords or theme (2-5 words maximum). No explanation, just the keywords.
Examples:
- "What's happening with artificial intelligence?" -> "artificial intelligence"
- "Tell me about the latest in climate change" -> "climate change"
- "Any news on Tesla stock?" -> "Tesla stock"
- "What's going on with the elections?" -> "elections"

Keywords:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts search keywords from queries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            theme = response.choices[0].message.content.strip().strip('"').strip()
            return theme
            
        except Exception as e:
            print(f"Error extracting theme: {e}")
            return user_query
    
    def answer_from_news(self, user_query, articles):
        """
        Generate an answer to user's query based on fetched news articles
        
        Args:
            user_query (str): User's original question
            articles (list): List of news articles
            
        Returns:
            str: AI-generated answer based on the news
        """
        if not articles:
            return "I couldn't find any recent news articles related to your query. Please try a different topic."
        
        # Format articles for the LLM
        articles_text = "\n\n".join([
            f"Article {i+1}:\nTitle: {article['title']}\nSource: {article['source']}\nPublished: {article.get('publishedAt', article.get('published_at', 'Unknown'))}\nContent: {article['description']}"
            for i, article in enumerate(articles[:5])  # Limit to top 5 articles
        ])
        
        prompt = f"""You are a helpful news assistant. Based on the following recent news articles, answer the user's question in a comprehensive yet concise way.

User's Question: "{user_query}"

Recent News Articles:
{articles_text}

Instructions:
1. Provide a direct answer to the user's question
2. Reference specific information from the articles
3. Mention sources when relevant
4. Keep the answer informative but conversational
5. If articles don't fully answer the question, mention what information is available

Answer:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a knowledgeable news assistant that provides accurate information based on recent news articles."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "I encountered an error while processing the news articles. Please try again."
    
    def summarize_articles(self, articles, summary_type="brief"):
        """
        Summarize multiple news articles
        
        Args:
            articles (list): List of news articles
            summary_type (str): Type of summary ('brief', 'detailed')
            
        Returns:
            str: Summary of the articles
        """
        if not articles:
            return "No articles to summarize."
        
        articles_text = "\n\n".join([
            f"- {article['title']} ({article['source']}, {article.get('publishedAt', article.get('published_at', 'Unknown'))}): {article['description']}"
            for article in articles[:10]
        ])
        
        if summary_type == "brief":
            prompt = f"""Provide a brief summary (3-4 sentences) of the main themes and key points from these news articles:

{articles_text}

Summary:"""
        else:
            prompt = f"""Provide a detailed summary of these news articles, highlighting the main themes, key developments, and important details:

{articles_text}

Summary:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional news summarizer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300 if summary_type == "brief" else 600
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error summarizing articles: {e}")
            return "Error generating summary."
    
    def answer_question(self, question, articles):
        """
        Answer a specific question about the articles
        
        Args:
            question (str): User's question
            articles (list): List of news articles
            
        Returns:
            str: Answer to the question
        """
        return self.answer_from_news(question, articles)
