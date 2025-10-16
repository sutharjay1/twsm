#!/usr/bin/env python3

from scraper import Newscraper
from sentiment import SentimentAnalyzer
from rich.console import Console
from rich.table import Table

console = Console()

def demo_modular_usage():
    console.print("[bold blue]🚀 Financial News Analysis Demo[/bold blue]\n")
    
    console.print("[yellow]Step 1: Initializing scraper...[/yellow]")
    scraper = Newscraper()
    
    console.print("[yellow]Step 2: Scraping news...[/yellow]")
    news_data = scraper.scrape_news()
    
    console.print(f"✅ Found {len(news_data['headlines'])} headlines and {len(news_data['stock_news'])} stock news items\n")
    
    console.print("[yellow]Step 3: Initializing sentiment analyzer...[/yellow]")
    analyzer = SentimentAnalyzer()
    
    console.print("[yellow]Step 4: Analyzing sentiment...[/yellow]")
    all_texts = news_data['headlines'] + news_data['stock_news']
    
    if all_texts:
        summary = analyzer.get_sentiment_summary(all_texts[:5])
        
        table = Table(title="📊 Sample Results")
        table.add_column("Text", style="white", min_width=40)
        table.add_column("Sentiment", style="bold")
        table.add_column("Confidence", style="cyan")
        
        for result in summary['detailed_results']:
            sentiment = result['sentiment']
            style = "green" if sentiment == "Positive" else "red" if sentiment == "Negative" else "yellow"
            
            table.add_row(
                result['text'][:50] + "..." if len(result['text']) > 50 else result['text'],
                f"[{style}]{sentiment}[/{style}]",
                f"{result['confidence']:.3f}"
            )
        
        console.print(table)
        
        console.print(f"\n[bold]Summary:[/bold]")
        console.print(f"Dominant sentiment: [{('green' if summary['dominant_sentiment'] == 'Positive' else 'red' if summary['dominant_sentiment'] == 'Negative' else 'yellow')}]{summary['dominant_sentiment']}[/]")
        console.print(f"Average confidence: {summary['average_confidence']:.3f}")
    
    console.print("\n[green]✅ Demo completed![/green]")

if __name__ == "__main__":
    demo_modular_usage()
