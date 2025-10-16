import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Union
import time
from abc import ABC, abstractmethod
import json
import re


class BaseScraper(ABC):
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                return BeautifulSoup(response.content, "html.parser")
            else:
                print(f"Failed to retrieve {self.source_name}: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error fetching {self.source_name}: {e}")
            return None

    @abstractmethod
    def scrape_news(self) -> Dict[str, List[str]]:
        pass

    def get_news_with_metadata(self) -> Dict[str, any]:
        news_data = self.scrape_news()
        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": self.source_name,
            "total_headlines": len(news_data.get("headlines", [])),
            "total_stock_news": len(news_data.get("stock_news", [])),
            "data": news_data
        }


class LiveMintScraper(BaseScraper):
    def __init__(self):
        super().__init__("LiveMint")
        self.base_url = "https://www.livemint.com/market"

    def extract_market_headlines(self, soup: BeautifulSoup) -> List[str]:
        headlines = []
        news_blocks = soup.find_all("li", class_="newsBlock")
        
        for news_block in news_blocks:
            headline_element = news_block.find("h2")
            if headline_element:
                headline = headline_element.text.strip()
                if headline:
                    headlines.append(headline)
        
        return headlines

    def extract_stock_market_news(self, soup: BeautifulSoup, limit: int = 10) -> List[str]:
        stock_market_news = []
        h3_elements = soup.select(".market-new-common-collection_contentBox__leEBU h3")
        
        for i, h3_element in enumerate(h3_elements):
            if i >= limit:
                break
            a_tag = h3_element.find("a")
            if a_tag:
                news_text = a_tag.text.strip()
                if news_text:
                    stock_market_news.append(news_text)
        
        return stock_market_news

    def scrape_news(self) -> Dict[str, List[str]]:
        soup = self.fetch_page(self.base_url)
        if not soup:
            return {"headlines": [], "stock_news": []}
        
        headlines = self.extract_market_headlines(soup)
        stock_news = self.extract_stock_market_news(soup)
        
        return {
            "headlines": headlines,
            "stock_news": stock_news
        }


class GoogleFinanceScraper(BaseScraper):
    def __init__(self):
        super().__init__("Google Finance")
        self.base_url = "https://www.google.com/finance"
        self.news_url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZ4ZERBU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen"

    def extract_google_finance_news(self, soup: BeautifulSoup, limit: int = 15) -> List[str]:
        headlines = []
        
        article_selectors = [
            'article h3',
            'article h4', 
            '[data-n-tid] h3',
            '[data-n-tid] h4',
            '.JheGif',
            '.ipQwMb',
            '.DY5T1d'
        ]
        
        for selector in article_selectors:
            elements = soup.select(selector)
            for element in elements:
                if len(headlines) >= limit:
                    break
                text = element.get_text(strip=True)
                if text and len(text) > 20 and text not in headlines:
                    headlines.append(text)
        
        return headlines[:limit]

    def extract_market_data(self, soup: BeautifulSoup) -> List[str]:
        market_data = []
        
        price_selectors = [
            '.YMlKec',
            '.P6K39c',
            '[data-symbol]',
            '.ln0Gqe'
        ]
        
        for selector in price_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and any(char.isdigit() for char in text):
                    market_data.append(text)
        
        return market_data[:10]

    def scrape_news(self) -> Dict[str, List[str]]:
        headlines = []
        stock_news = []
        
        soup = self.fetch_page(self.base_url)
        if soup:
            headlines.extend(self.extract_google_finance_news(soup))
            stock_news.extend(self.extract_market_data(soup))
        
        news_soup = self.fetch_page(self.news_url)
        if news_soup:
            headlines.extend(self.extract_google_finance_news(news_soup, 10))
        
        return {
            "headlines": list(set(headlines))[:15],
            "stock_news": list(set(stock_news))[:10]
        }


class YahooFinanceScraper(BaseScraper):
    def __init__(self):
        super().__init__("Yahoo Finance")
        self.base_url = "https://finance.yahoo.com"
        self.news_url = "https://finance.yahoo.com/news"

    def extract_yahoo_headlines(self, soup: BeautifulSoup, limit: int = 15) -> List[str]:
        headlines = []
        
        selectors = [
            'h3[data-test-locator="StreamTitle"]',
            'h3 a[data-test-locator="StreamTitle"]',
            '.Ov:nth-of-type(1) h3',
            '.js-stream-content h3',
            '[data-module="Stream"] h3',
            '.Fw(600) a',
            'h3.Mb\\(5px\\)',
            '.C\\(\\$c-link\\) h3'
        ]
        
        for selector in selectors:
            try:
                elements = soup.select(selector)
                for element in elements:
                    if len(headlines) >= limit:
                        break
                    text = element.get_text(strip=True)
                    if text and len(text) > 15 and text not in headlines:
                        headlines.append(text)
            except Exception:
                continue
        
        return headlines[:limit]

    def extract_market_movers(self, soup: BeautifulSoup) -> List[str]:
        movers = []
        
        selectors = [
            '[data-test="market-summary"] span',
            '.Trsdu\\(0\\.3s\\)',
            '[data-symbol] span',
            '.Fw\\(600\\).C\\(\\$c-trend-up\\)',
            '.Fw\\(600\\).C\\(\\$c-trend-down\\)'
        ]
        
        for selector in selectors:
            try:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(strip=True)
                    if text and (any(char.isdigit() for char in text) or '%' in text):
                        movers.append(text)
            except Exception:
                continue
        
        return movers[:10]

    def scrape_news(self) -> Dict[str, List[str]]:
        headlines = []
        stock_news = []
        
        main_soup = self.fetch_page(self.base_url)
        if main_soup:
            headlines.extend(self.extract_yahoo_headlines(main_soup))
            stock_news.extend(self.extract_market_movers(main_soup))
        
        news_soup = self.fetch_page(self.news_url)
        if news_soup:
            headlines.extend(self.extract_yahoo_headlines(news_soup, 10))
        
        return {
            "headlines": list(set(headlines))[:15],
            "stock_news": list(set(stock_news))[:10]
        }


class MarketWatchScraper(BaseScraper):
    def __init__(self):
        super().__init__("MarketWatch")
        self.base_url = "https://www.marketwatch.com"
        self.news_url = "https://www.marketwatch.com/latest-news"

    def extract_marketwatch_news(self, soup: BeautifulSoup, limit: int = 15) -> List[str]:
        headlines = []
        
        selectors = [
            '.article__headline a',
            'h3.article__headline',
            '.headline a',
            'h2 a',
            'h3 a',
            '.WSJTheme--headline-color-black'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                if len(headlines) >= limit:
                    break
                text = element.get_text(strip=True)
                if text and len(text) > 20 and text not in headlines:
                    headlines.append(text)
        
        return headlines[:limit]

    def scrape_news(self) -> Dict[str, List[str]]:
        headlines = []
        
        soup = self.fetch_page(self.news_url)
        if soup:
            headlines = self.extract_marketwatch_news(soup)
        
        return {
            "headlines": headlines,
            "stock_news": []
        }


class ScraperFactory:
    _scrapers = {
        "livemint": LiveMintScraper,
        "google": GoogleFinanceScraper,
        "yahoo": YahooFinanceScraper,
        "marketwatch": MarketWatchScraper
    }

    @classmethod
    def create_scraper(cls, source: str) -> BaseScraper:
        if source.lower() not in cls._scrapers:
            raise ValueError(f"Unsupported source: {source}. Available: {list(cls._scrapers.keys())}")
        return cls._scrapers[source.lower()]()

    @classmethod
    def get_all_scrapers(cls) -> Dict[str, BaseScraper]:
        return {name: scraper_class() for name, scraper_class in cls._scrapers.items()}

    @classmethod
    def get_available_sources(cls) -> List[str]:
        return list(cls._scrapers.keys())


class MultiSourceScraper:
    def __init__(self, sources: List[str] = None):
        if sources is None:
            sources = ["livemint", "google", "yahoo"]
        
        self.scrapers = {}
        for source in sources:
            try:
                self.scrapers[source] = ScraperFactory.create_scraper(source)
            except ValueError as e:
                print(f"Warning: {e}")

    def scrape_all_sources(self) -> Dict[str, Dict]:
        results = {}
        for source_name, scraper in self.scrapers.items():
            try:
                print(f"Scraping {source_name}...")
                results[source_name] = scraper.get_news_with_metadata()
                time.sleep(1)
            except Exception as e:
                print(f"Error scraping {source_name}: {e}")
                results[source_name] = {
                    "error": str(e),
                    "data": {"headlines": [], "stock_news": []}
                }
        return results

    def get_combined_news(self) -> Dict[str, List[str]]:
        all_results = self.scrape_all_sources()
        combined_headlines = []
        combined_stock_news = []
        
        for source, data in all_results.items():
            if "data" in data:
                combined_headlines.extend(data["data"].get("headlines", []))
                combined_stock_news.extend(data["data"].get("stock_news", []))
        
        return {
            "headlines": list(set(combined_headlines)),
            "stock_news": list(set(combined_stock_news)),
            "sources": list(all_results.keys()),
            "total_sources": len(all_results)
        }
