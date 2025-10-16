# 📊 Financial News Analysis & Sentiment Prediction

A modular, interactive CLI application for scraping financial news and analyzing market sentiment using machine learning.

## 🚀 Features

- **🔍 Web Scraping**: Automated news extraction from LiveMint market section
- **🤖 Sentiment Analysis**: AI-powered sentiment classification using RoBERTa model
- **🎨 Interactive CLI**: Beautiful, colored terminal interface with rich tables
- **📊 Real-time Analysis**: Live market sentiment tracking
- **🧩 Modular Design**: Clean, reusable components

## 📁 Project Structure

```
├── main.py          # Main application entry point
├── cli.py           # Interactive CLI interface with rich formatting
├── scraper.py       # Web scraping module for news extraction
├── sentiment.py     # Sentiment analysis module using transformers
├── demo.py          # Simple demonstration of modular usage
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## 🛠️ Installation

1. **Clone and navigate to the project:**
   ```bash
   cd Financial-Data-Analysis-Stock-Prediction-with-ML-Web-Scraping
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

### Interactive CLI Mode
```bash
python main.py
```

This launches the full interactive CLI with:
- 📰 News scraping options
- 📊 Sentiment analysis tools  
- 🔍 Combined analysis workflows
- 📈 Summary statistics
- ⚙️ Settings management

### Modular Usage
```python
from scraper import Newscraper
from sentiment import SentimentAnalyzer

# Initialize components
scraper = Newscraper()
analyzer = SentimentAnalyzer()

# Scrape news
news_data = scraper.scrape_news()

# Analyze sentiment
results = analyzer.analyze_batch(news_data['headlines'])
```

### Quick Demo
```bash
python demo.py
```

## 🎨 CLI Features

- **🌈 Colored Output**: Rich terminal formatting with syntax highlighting
- **📋 Interactive Tables**: Organized data display with sorting and filtering
- **🔄 Progress Indicators**: Real-time loading animations
- **📊 Visual Charts**: Sentiment distribution and confidence metrics
- **⚡ Fast Navigation**: Intuitive menu system with keyboard shortcuts

## 📊 Sentiment Analysis

The application uses the `cardiffnlp/twitter-roberta-base-sentiment` model to classify text into:

- 🟢 **Positive**: Optimistic market sentiment
- 🟡 **Neutral**: Balanced or unclear sentiment  
- 🔴 **Negative**: Pessimistic market sentiment

Each prediction includes confidence scores and detailed breakdowns.

## 🔧 Modules

### `scraper.py`
- **Newscraper**: Web scraping class for LiveMint market news
- **Error handling**: Robust request management with timeouts
- **Data extraction**: Headlines and stock market news parsing

### `sentiment.py`  
- **SentimentAnalyzer**: ML-powered text sentiment classification
- **Batch processing**: Efficient analysis of multiple texts
- **Summary statistics**: Aggregate sentiment metrics

### `cli.py`
- **FinancialCLI**: Interactive terminal interface
- **Rich formatting**: Colors, tables, and progress bars
- **Menu system**: User-friendly navigation and options

## 📈 Sample Output

```
╔═══════════════════════════════════════════════════════════════╗
║                   Financial News Analyzer                     ║
║              Real-time Market Sentiment Analysis              ║
╚═══════════════════════════════════════════════════════════════╝

┌─────────────────────────── 📊 Sentiment Analysis Results ───────────────────────────┐
│ ID │ Text Preview                           │ Sentiment │ Confidence │ Scores        │
├────┼────────────────────────────────────────┼───────────┼────────────┼───────────────┤
│ 1  │ Markets rally as tech stocks surge...  │ Positive  │ 0.892      │ P:0.89 N:0.08 │
│ 2  │ Inflation concerns weigh on investor... │ Negative  │ 0.756      │ P:0.12 N:0.76 │
└────┴────────────────────────────────────────┴───────────┴────────────┴───────────────┘
```

## 🔮 Future Enhancements

- 📈 Stock price integration
- 🤖 Additional ML models
- 📊 Historical trend analysis
- 🌐 Multiple news sources
- 📱 Web dashboard interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.
