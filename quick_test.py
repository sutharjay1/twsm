#!/usr/bin/env python3

from multi_scraper import ScraperFactory, MultiSourceScraper
from enhanced_sentiment import EnhancedSentimentAnalyzer
import time

def quick_test():
    print("🚀 Quick Multi-Source Financial Analysis Test")
    print("=" * 50)
    
    print("\n1. Testing individual sources...")
    available_sources = ScraperFactory.get_available_sources()
    print(f"Available sources: {', '.join(available_sources)}")
    
    print("\n2. Testing Google Finance scraper...")
    try:
        google_scraper = ScraperFactory.create_scraper("google")
        google_data = google_scraper.scrape_news()
        print(f"✅ Google Finance: {len(google_data['headlines'])} headlines, {len(google_data['stock_news'])} market updates")
    except Exception as e:
        print(f"❌ Google Finance error: {e}")
    
    print("\n3. Testing Yahoo Finance scraper...")
    try:
        yahoo_scraper = ScraperFactory.create_scraper("yahoo")
        yahoo_data = yahoo_scraper.scrape_news()
        print(f"✅ Yahoo Finance: {len(yahoo_data['headlines'])} headlines, {len(yahoo_data['stock_news'])} market updates")
    except Exception as e:
        print(f"❌ Yahoo Finance error: {e}")
    
    print("\n4. Testing multi-source combination...")
    try:
        multi_scraper = MultiSourceScraper(["livemint", "google"])
        combined_data = multi_scraper.get_combined_news()
        total_articles = len(combined_data['headlines']) + len(combined_data['stock_news'])
        print(f"✅ Combined data: {total_articles} total articles from {len(combined_data.get('sources', []))} sources")
        
        if combined_data['headlines']:
            print(f"📰 Sample headline: {combined_data['headlines'][0][:100]}...")
    except Exception as e:
        print(f"❌ Multi-source error: {e}")
    
    print("\n5. Testing enhanced sentiment analysis...")
    try:
        analyzer = EnhancedSentimentAnalyzer()
        
        sample_texts = [
            "Stock market surges on positive earnings reports",
            "Market crashes amid recession fears and inflation concerns",
            "Steady trading continues with mixed signals from investors"
        ]
        
        results = analyzer.get_sentiment_summary(sample_texts)
        print(f"✅ Sentiment analysis complete:")
        print(f"   - Total analyzed: {results['total_analyzed']}")
        print(f"   - Dominant sentiment: {results['dominant_sentiment']}")
        print(f"   - Market outlook: {results['market_outlook']['outlook']}")
        
    except Exception as e:
        print(f"❌ Sentiment analysis error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Quick test completed!")
    print("\nTo run the full analysis:")
    print("  python enhanced_cli.py")
    print("\nTo run the demo:")
    print("  python multi_source_demo.py")

if __name__ == "__main__":
    quick_test()
