# 🤖 AI News Chatbot - Quick Start Guide

## What This Chatbot Does

This AI-powered chatbot helps you stay informed about current events by:
1. **Understanding your questions** - You ask naturally about any topic
2. **Extracting the main theme** - AI identifies what news to search for
3. **Finding relevant news** - Automatically searches for latest articles
4. **Generating answers** - AI reads the news and provides a comprehensive response

## How It Works

### The Workflow

```
Your Question → AI Theme Extraction → News Search → AI Analysis → Answer + Sources
```

**Example:**
- You ask: "What's happening with artificial intelligence?"
- AI extracts: "artificial intelligence"
- System fetches: 5 latest news articles about AI
- AI reads articles and generates: A comprehensive answer with sources

## Getting Started

### 1. Setup (First Time Only)

```bash
# Clone the repository
git clone https://github.com/HasanNayon/Real-time-News-Agent.git
cd Real-time-News-Agent

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
# Copy .env.example to .env and add your API keys
```

### 2. Get API Keys

You need two free API keys:

**NewsAPI** (for fetching news)
- Visit: https://newsapi.org/
- Sign up for free account
- Copy your API key
- Add to `.env`: `NEWS_API_KEY=your_key_here`

**Groq AI** (for AI processing)
- Visit: https://console.groq.com/
- Sign up for free account
- Generate API key
- Add to `.env`: `GROQ_API_KEY=your_key_here`

### 3. Run the Chatbot

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Using the Chatbot

### Basic Usage

1. **Type your question** in the chat input at the bottom
2. **Press Enter** or click the Send button
3. **Wait for AI** to process (you'll see status messages)
4. **Read the answer** and expand sources to see which articles were used

### Example Questions

**Technology:**
- "What's the latest on artificial intelligence?"
- "Any news about Tesla?"
- "Tell me about new iPhone features"

**Current Events:**
- "What's happening with climate change?"
- "Latest news on elections?"
- "Any updates on space exploration?"

**Business & Finance:**
- "How is the stock market doing?"
- "Latest cryptocurrency news"
- "What's happening with Tesla stock?"

**Sports & Entertainment:**
- "Latest sports news"
- "Updates on the World Cup"
- "New movies coming out"

### Settings (Sidebar)

- **Articles to fetch**: Control how many articles AI analyzes (3-10)
- **News Region**: Select which country's news to prioritize
- **Clear Chat**: Start a fresh conversation

## Tips for Best Results

### ✅ Good Questions

- Be specific: "What's happening with AI regulation?"
- Ask about current events: "Latest news on climate summit"
- Use natural language: "Tell me about recent space missions"

### ❌ Avoid

- Very old topics: "News from 2020" (NewsAPI has date limits)
- Too vague: "Tell me everything" (be more specific)
- Non-news questions: "How to code in Python?" (this is a NEWS chatbot)

## Features

### 💬 Chat Interface
- Natural conversation flow
- Message history saved during session
- Timestamps on all messages

### 📰 Source Citations
- See which articles were used
- Direct links to full articles
- Source name and publish date

### 🧠 Smart Theme Extraction
- AI understands intent
- Extracts key topics automatically
- Optimizes search queries

### 🔄 Real-Time News
- Latest breaking news
- Multiple news sources
- Global coverage

## Troubleshooting

### App Won't Start

```bash
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt

# Check Python version (need 3.8+)
python --version
```

### "API Key Not Found" Error

Check your `.env` file has both keys:
```
NEWS_API_KEY=your_actual_key
GROQ_API_KEY=your_actual_key
```

### "No Articles Found"

- Try different keywords
- Check your NewsAPI key is valid
- Some topics may have limited coverage
- Try selecting different region

### Slow Responses

- Reduce number of articles (sidebar setting)
- Check internet connection
- API rate limits may apply on free tier

## Advanced Usage

### Command Line Interface

For testing, use the test script:
```bash
python test_chatbot.py
```

### Customization

Edit `llm_summarizer.py` to:
- Change AI model
- Adjust response length
- Modify prompts

Edit `news_fetcher.py` to:
- Change default country
- Adjust article count
- Modify search parameters

## API Limits (Free Tier)

**NewsAPI Free Tier:**
- 100 requests per day
- Articles from last 30 days only
- Delayed by 15 minutes

**Groq Free Tier:**
- Generous free tier
- Rate limits apply
- Fast response times

## Support

- **GitHub**: https://github.com/HasanNayon/Real-time-News-Agent
- **Issues**: Report bugs on GitHub Issues
- **Documentation**: Check README.md

## License

This project is open source. See LICENSE file for details.

---

**Built with ❤️ using Streamlit, NewsAPI, and Groq AI**
