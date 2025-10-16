import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time


class Newscraper:
    def __init__(self, base_url: str = "https://www.livemint.com/market"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return BeautifulSoup(response.content, "html.parser")
            else:
                print(f"Failed to retrieve webpage: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return None

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

    def extract_stock_market_news(self, soup: BeautifulSoup, limit: int = 7) -> List[str]:
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

    def get_news_with_metadata(self) -> Dict[str, any]:
        news_data = self.scrape_news()
        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": self.base_url,
            "total_headlines": len(news_data["headlines"]),
            "total_stock_news": len(news_data["stock_news"]),
            "data": news_data
        }
