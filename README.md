# 📰 Real-Time News Chatbot

An intelligent web application that fetches real-time news from around the world and uses AI (Groq LLM) to summarize articles and answer questions about current events.

## ✨ Features

- **🌐 Beautiful Web Interface**: Modern Streamlit-based UI with responsive design
- **📊 Real-Time News Fetching**: Get the latest headlines from NewsAPI
- **🤖 AI-Powered Summarization**: Uses Groq's LLama 3.1 model to create concise summaries
- **💬 Intelligent Q&A**: Ask questions about news articles and get AI-generated answers
- **🔍 Multiple News Sources**: Search by keywords, categories, or get top headlines
- **📑 Category Filtering**: Browse news by Business, Technology, Sports, Health, Science, Entertainment, and more
- **🌍 Multi-Country Support**: Access news from USA, UK, Canada, Australia, India, and more
- **📝 Chat History**: Keep track of all summaries and questions in one place

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- NewsAPI key (free tier available at [newsapi.org](https://newsapi.org/))
- Groq API key (free tier available at [console.groq.com](https://console.groq.com/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/HasanNayon/Real-time-News-Agent.git
cd Real-time-News-Agent
```

2. **Create and activate virtual environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# On Windows Command Prompt:
venv\Scripts\activate.bat

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
   
   The `.env` file is already configured with your API keys. If you need to update them, edit `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```

5. **Run the Streamlit app**
```bash
streamlit run app.py
```

The app will automatically open in your default web browser at `http://localhost:8501`

## 📖 How to Use

### Web Interface (Streamlit)

1. **Select News Source** (in the sidebar):
   - **Top Headlines**: Get breaking news from a specific country
   - **Search News**: Find articles using keywords
   - **Category News**: Browse by category (Business, Tech, Sports, etc.)

2. **Configure Options**:
   - Choose country (for headlines)
   - Enter search terms (for search)
   - Select category (for category news)
   - Set number of articles (1-10)

3. **Fetch News**: Click the fetch/search button to load articles

4. **View Articles**: Browse articles in the "Articles" tab with:
   - Headlines and descriptions
   - Source and publish date
   - Images (when available)
   - Links to full articles

5. **AI Features** (in the "Chat & Summaries" tab):
   - Click "Summarize All Articles" to get an AI summary
   - Ask questions about the articles in the text input
   - View chat history with timestamps

### Command Line Interface (Optional)

You can still use the original CLI version:
```bash
python main.py
```

## 📖 CLI Usage (Original Version)

When you run the CLI chatbot, you'll see a menu with these options:

1. **Get Top Headlines**: Fetch the latest headlines from a specific country
2. **Search for Specific News**: Search for news articles using keywords
3. **Get News by Category**: Browse news by category (Business, Tech, Sports, etc.)
4. **Summarize Current News**: Get an AI-generated summary of loaded articles
5. **Ask a Question**: Ask questions about the current articles and get AI answers
6. **Exit**: Close the application

### Example Workflow

1. Choose option 2 (Search for specific news)
2. Enter a topic (e.g., "artificial intelligence")
3. Select how many articles to fetch (1-10)
4. Review the articles
5. Choose option 4 to get an AI summary
6. Choose option 5 to ask specific questions about the articles

## 🛠️ Project Structure

```
Real-time-News-Agent/
├── app.py               # Streamlit web application (main)
├── main.py              # Command-line interface version
├── news_fetcher.py      # NewsAPI integration module
├── llm_summarizer.py    # Groq LLM integration for summarization
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API keys)
├── .gitignore          # Git ignore file
├── venv/               # Virtual environment (created locally)
└── README.md           # Project documentation
```

## 🔑 API Keys

### NewsAPI
- Get your free API key at: https://newsapi.org/
- Free tier includes 100 requests per day

### Groq API
- Get your free API key at: https://console.groq.com/
- Free tier includes generous usage limits

## 🎯 Features Breakdown

### News Fetcher (`news_fetcher.py`)
- Fetches top headlines from specific countries
- Searches news by keywords
- Filters by categories
- Returns formatted article data

### LLM Summarizer (`llm_summarizer.py`)
- Uses Groq's LLama 3.1 70B model
- Generates concise summaries of multiple articles
- Answers questions based on article content
- Maintains context across conversations

### Streamlit App (`app.py`)
- Modern web interface with sidebar navigation
- Real-time article display with images
- Interactive AI chat interface
- Session state management for articles and chat history
- Responsive design with custom CSS styling

### CLI Application (`main.py`)
- Interactive command-line interface
- Manages user interactions
- Coordinates between news fetching and AI summarization
- Displays formatted results

## 💡 Tips

- **For Web App:**
  - Use the sidebar to navigate between different news sources
  - The "Chat & Summaries" tab keeps a history of all your interactions
  - Clear articles to start fresh with a new topic
  - Articles with images are more visually engaging

- **For CLI:**
  - Start with fewer articles (3-5) for faster summarization
  - Use specific keywords for better search results

- **General:**
  - The AI works best with at least 2-3 articles loaded
  - Be specific with your questions for better answers
  - Category browsing is great for daily news digests

## 🔒 Security Note

- Never commit your `.env` file to Git (already in `.gitignore`)
- Keep your API keys private
- The provided keys are for your personal use only

## 🤝 Contributing

Feel free to fork this project and submit pull requests. For major changes, please open an issue first.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [NewsAPI](https://newsapi.org/) for providing news data
- [Groq](https://groq.com/) for the LLM API
- [Streamlit](https://streamlit.io/) for the amazing web framework
- Built with Python and love ❤️

## 🐛 Troubleshooting

### Virtual Environment Issues
If you have issues activating the virtual environment:
- On Windows PowerShell, you may need to run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Alternatively, use Command Prompt instead of PowerShell

### Port Already in Use
If port 8501 is already in use:
```bash
streamlit run app.py --server.port 8502
```

### Module Not Found Errors
Make sure you're in the virtual environment and have installed all dependencies:
```bash
pip install -r requirements.txt
```

---

**Happy News Reading! 📰✨**