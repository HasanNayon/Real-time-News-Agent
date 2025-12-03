import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMSummarizer:
    """Uses Groq API to summarize news articles"""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = "llama-3.1-70b-versatile"  # Fast and capable model
        
    def summarize_articles(self, articles, custom_prompt=None):
        """
        Summarize multiple news articles
        
        Args:
            articles (list): List of article dictionaries
            custom_prompt (str): Custom instruction for summarization
            
        Returns:
            str: Summarized content
        """
        if not articles:
            return "No articles to summarize."
        
        # Prepare article text
        articles_text = self._prepare_articles_text(articles)
        
        # Create prompt
        if custom_prompt:
            prompt = f"{custom_prompt}\n\nHere are the news articles:\n\n{articles_text}"
        else:
            prompt = f"""You are a helpful news assistant. Please provide a comprehensive summary of the following news articles. 
Include the key points, main events, and important details. Make it concise and easy to understand.

News Articles:

{articles_text}

Please provide a well-structured summary."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional news summarizer. Provide clear, accurate, and concise summaries of news articles."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1024,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {e}"
    
    def answer_question(self, articles, question):
        """
        Answer a question based on the news articles
        
        Args:
            articles (list): List of article dictionaries
            question (str): User's question
            
        Returns:
            str: Answer to the question
        """
        if not articles:
            return "I don't have any news articles to answer your question."
        
        articles_text = self._prepare_articles_text(articles)
        
        prompt = f"""Based on the following news articles, please answer this question: {question}

News Articles:

{articles_text}

Please provide a clear and informative answer based on the information in the articles."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that answers questions based on news articles. Be accurate and cite information from the articles when relevant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1024,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating answer: {e}"
    
    def _prepare_articles_text(self, articles):
        """Format articles for LLM processing"""
        articles_text = ""
        for i, article in enumerate(articles, 1):
            articles_text += f"\n--- Article {i} ---\n"
            articles_text += f"Title: {article['title']}\n"
            articles_text += f"Source: {article['source']}\n"
            articles_text += f"Published: {article['publishedAt']}\n"
            articles_text += f"Description: {article['description']}\n"
            if article['content']:
                articles_text += f"Content: {article['content']}\n"
            articles_text += f"URL: {article['url']}\n"
        
        return articles_text
