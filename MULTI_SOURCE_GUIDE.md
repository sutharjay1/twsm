# Multi-Source Financial News Scraper & Sentiment Analysis

A comprehensive financial news analysis tool that scrapes and analyzes sentiment from multiple major financial news sources including Google Finance, Yahoo Finance, LiveMint, and MarketWatch.

## 🌟 Features

### Multi-Source Scraping
- **Google Finance**: Market data, trending stocks, financial news
- **Yahoo Finance**: Comprehensive financial news, market movers, earnings reports
- **LiveMint**: Indian market news and analysis
- **MarketWatch**: Real-time market updates and financial news

### Enhanced Sentiment Analysis
- Financial keyword-aware sentiment analysis
- Source-specific sentiment comparison
- Market outlook prediction (Bullish/Bearish/Neutral)
- Confidence scoring and bias detection

### Interactive CLI
- Source selection and customization
- Real-time progress tracking
- Beautiful formatted output with Rich library
- Interactive mode for continuous analysis

## 🚀 Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Run Multi-Source Demo
```bash
python multi_source_demo.py
```

### 3. Run Enhanced CLI
```bash
python enhanced_cli.py
```

## 📊 Available Sources

| Source | Description | Data Types |
|--------|-------------|------------|
| **Google Finance** | Global market data and news | Headlines, Market data, Trending stocks |
| **Yahoo Finance** | Comprehensive financial coverage | News articles, Market movers, Earnings |
| **LiveMint** | Indian market focus | Market headlines, Stock news |
| **MarketWatch** | Real-time market updates | Breaking news, Market analysis |

## 🛠 Usage Examples

### Basic Multi-Source Scraping
```python
from multi_scraper import MultiSourceScraper

# Initialize with all sources
scraper = MultiSourceScraper()

# Get combined news from all sources
combined_data = scraper.get_combined_news()
print(f"Found {len(combined_data['headlines'])} headlines")
```

### Specific Source Scraping
```python
from multi_scraper import ScraperFactory

# Create specific scraper
google_scraper = ScraperFactory.create_scraper("google")
yahoo_scraper = ScraperFactory.create_scraper("yahoo")

# Get news data
google_news = google_scraper.get_news_with_metadata()
yahoo_news = yahoo_scraper.get_news_with_metadata()
```

### Enhanced Sentiment Analysis
```python
from enhanced_sentiment import EnhancedSentimentAnalyzer

analyzer = EnhancedSentimentAnalyzer()

# Analyze with financial context
texts = ["Stock market surges on positive earnings", "Market crashes amid recession fears"]
results = analyzer.get_sentiment_summary(texts)

print(f"Market Outlook: {results['market_outlook']['outlook']}")
print(f"Dominant Sentiment: {results['dominant_sentiment']}")
```

### Source Comparison
```python
from multi_scraper import MultiSourceScraper
from enhanced_sentiment import EnhancedSentimentAnalyzer

scraper = MultiSourceScraper(["google", "yahoo", "livemint"])
analyzer = EnhancedSentimentAnalyzer()

# Get data from all sources
all_results = scraper.scrape_all_sources()

# Compare sentiment across sources
comparison = analyzer.get_source_comparison(all_results)
print(f"Most Bullish Source: {comparison['comparison_summary']['most_bullish_source']['source']}")
```

## 🎯 CLI Options

### Enhanced CLI Features
- **Source Selection**: Choose specific sources or use all
- **Interactive Mode**: Continuous analysis with menu options
- **Progress Tracking**: Real-time scraping progress
- **Formatted Output**: Beautiful tables and summaries

### CLI Commands
```bash
# Run with all sources (default)
python enhanced_cli.py

# Demo mode
python multi_source_demo.py
```

## 📈 Sentiment Analysis Features

### Financial Keyword Recognition
The enhanced sentiment analyzer includes financial-specific keywords:

**Positive Keywords**: surge, rally, gains, bullish, growth, profit, earnings, outperform
**Negative Keywords**: plunge, crash, decline, bearish, loss, deficit, underperform
**Neutral Keywords**: stable, steady, maintain, hold, unchanged, flat

### Market Outlook Prediction
- **Strongly Bullish**: >60% positive sentiment
- **Bullish**: 40-60% positive sentiment  
- **Mixed/Neutral**: Balanced sentiment
- **Bearish**: 40-60% negative sentiment
- **Strongly Bearish**: >60% negative sentiment

### Source-Specific Analysis
Each source is analyzed separately to provide:
- Individual sentiment distribution
- Source reliability scoring
- Comparative analysis across sources
- Confidence levels per source

## 🔧 Customization

### Adding New Sources
1. Create a new scraper class inheriting from `BaseScraper`
2. Implement the `scrape_news()` method
3. Add to `ScraperFactory._scrapers` dictionary

```python
class NewSourceScraper(BaseScraper):
    def __init__(self):
        super().__init__("NewSource")
        self.base_url = "https://newsource.com"
    
    def scrape_news(self) -> Dict[str, List[str]]:
        # Implementation here
        pass
```

### Customizing Sentiment Analysis
- Modify financial keywords in `_load_financial_keywords()`
- Adjust financial bias weight in `analyze_sentiment()`
- Customize market outlook thresholds in `_determine_market_outlook()`

## 🚨 Error Handling

The system includes robust error handling:
- Network timeout protection
- Source-specific error isolation
- Graceful degradation when sources fail
- Detailed error reporting

## 📊 Output Formats

### Sentiment Summary
```json
{
  "total_analyzed": 45,
  "sentiment_distribution": {"Positive": 20, "Neutral": 15, "Negative": 10},
  "dominant_sentiment": "Positive",
  "market_outlook": {
    "outlook": "Bullish",
    "confidence": "High",
    "description": "Generally positive market sentiment"
  }
}
```

### Source Comparison
```json
{
  "most_bullish_source": {"source": "google", "positive_count": 15},
  "most_bearish_source": {"source": "marketwatch", "negative_count": 8},
  "highest_confidence_source": {"source": "yahoo", "confidence": 0.892}
}
```

## 🔍 Troubleshooting

### Common Issues
1. **Network Errors**: Check internet connection and firewall settings
2. **Model Loading**: Ensure transformers library is properly installed
3. **Source Failures**: Individual source failures won't stop overall analysis

### Performance Tips
- Use fewer sources for faster analysis
- Limit article count for quicker processing
- Run during off-peak hours for better source availability

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- New financial news sources
- Improved sentiment analysis algorithms
- Enhanced error handling
- Performance optimizations

## 📞 Support

For questions or issues, please open a GitHub issue with:
- Error messages (if any)
- Source configuration
- Expected vs actual behavior
