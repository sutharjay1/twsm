from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
import time
from multi_scraper import MultiSourceScraper, ScraperFactory
from enhanced_sentiment import EnhancedSentimentAnalyzer


def demo_multi_source_analysis():
    console = Console()
    
    console.print(Panel("""
╔═══════════════════════════════════════════════════════════════╗
║                Multi-Source Financial Analysis Demo            ║
║         Scraping Google Finance, Yahoo Finance & More         ║
╚═══════════════════════════════════════════════════════════════╝
    """, style="bold blue"))
    
    console.print("\n[bold cyan]🚀 Initializing Multi-Source Scraper...[/bold cyan]")
    
    sources = ["livemint", "google", "yahoo", "marketwatch"]
    multi_scraper = MultiSourceScraper(sources)
    
    console.print("✅ [green]Multi-source scraper initialized[/green]")
    console.print(f"📊 [yellow]Active sources: {', '.join([s.title() for s in sources])}[/yellow]\n")
    
    console.print("[bold magenta]📰 Step 1: Scraping from all sources...[/bold magenta]")
    all_results = multi_scraper.scrape_all_sources()
    
    source_table = Table(title="📊 Source Results Summary", show_header=True, header_style="bold magenta")
    source_table.add_column("Source", style="bold cyan")
    source_table.add_column("Status", style="white")
    source_table.add_column("Headlines", style="green")
    source_table.add_column("Market Data", style="yellow")
    
    for source, data in all_results.items():
        if "error" in data:
            status = "[red]❌ Error[/red]"
            headlines = "0"
            market_data = "0"
        else:
            status = "[green]✅ Success[/green]"
            headlines = str(data.get("total_headlines", 0))
            market_data = str(data.get("total_stock_news", 0))
        
        source_table.add_row(source.title(), status, headlines, market_data)
    
    console.print(source_table)
    
    console.print("\n[bold magenta]📈 Step 2: Combining all news sources...[/bold magenta]")
    combined_data = multi_scraper.get_combined_news()
    
    total_headlines = len(combined_data.get("headlines", []))
    total_market_data = len(combined_data.get("stock_news", []))
    
    console.print(f"✅ [green]Combined {total_headlines} headlines and {total_market_data} market updates[/green]")
    
    if total_headlines > 0:
        console.print("\n[bold yellow]📰 Sample Headlines:[/bold yellow]")
        for i, headline in enumerate(combined_data["headlines"][:5], 1):
            preview = headline[:80] + "..." if len(headline) > 80 else headline
            console.print(f"  {i}. {preview}")
        
        if total_headlines > 5:
            console.print(f"  ... and {total_headlines - 5} more headlines")
    
    console.print("\n[bold magenta]🧠 Step 3: Initializing Enhanced Sentiment Analyzer...[/bold magenta]")
    sentiment_analyzer = EnhancedSentimentAnalyzer()
    console.print("✅ [green]Enhanced sentiment analyzer loaded[/green]")
    
    console.print("\n[bold magenta]📊 Step 4: Analyzing sentiment across all sources...[/bold magenta]")
    all_texts = combined_data.get("headlines", []) + combined_data.get("stock_news", [])
    
    if all_texts:
        sentiment_summary = sentiment_analyzer.get_sentiment_summary(all_texts)
        
        distribution = sentiment_summary["sentiment_distribution"]
        total = sentiment_summary["total_analyzed"]
        outlook = sentiment_summary["market_outlook"]
        
        sentiment_text = f"""
[bold]Total Articles Analyzed:[/bold] {total}
[bold]Sources Combined:[/bold] {', '.join([s.title() for s in combined_data.get('sources', [])])}

[bold cyan]Sentiment Distribution:[/bold cyan]
🟢 Positive: {distribution['Positive']} ({distribution['Positive']/total*100:.1f}%)
🟡 Neutral:  {distribution['Neutral']} ({distribution['Neutral']/total*100:.1f}%)
🔴 Negative: {distribution['Negative']} ({distribution['Negative']/total*100:.1f}%)

[bold magenta]Market Outlook:[/bold magenta] {outlook['outlook']} 
[bold]Confidence:[/bold] {outlook['confidence']}
[bold]Analysis:[/bold] {outlook['description']}
        """
        
        console.print(Panel(sentiment_text, title="📈 Multi-Source Sentiment Analysis", style="bold blue"))
        
        console.print("\n[bold magenta]🔍 Step 5: Source-by-Source Comparison...[/bold magenta]")
        source_comparison = sentiment_analyzer.get_source_comparison(all_results)
        
        if source_comparison.get("source_analyses"):
            comparison_table = Table(title="📊 Source Sentiment Comparison", show_header=True, header_style="bold magenta")
            comparison_table.add_column("Source", style="bold cyan")
            comparison_table.add_column("Articles", style="white")
            comparison_table.add_column("Dominant", style="bold")
            comparison_table.add_column("Confidence", style="yellow")
            comparison_table.add_column("Outlook", style="green")
            
            for source, analysis in source_comparison["source_analyses"].items():
                dominant = analysis["dominant_sentiment"]
                confidence = f"{analysis['confidence']:.3f}"
                outlook = analysis["market_outlook"]["outlook"]
                articles = str(analysis["article_count"])
                
                if dominant == "Positive":
                    dominant_style = "[green]Positive[/green]"
                elif dominant == "Negative":
                    dominant_style = "[red]Negative[/red]"
                else:
                    dominant_style = "[yellow]Neutral[/yellow]"
                
                comparison_table.add_row(
                    source.title(),
                    articles,
                    dominant_style,
                    confidence,
                    outlook
                )
            
            console.print(comparison_table)
            
            comparison_summary = source_comparison["comparison_summary"]
            if "most_bullish_source" in comparison_summary:
                console.print(f"\n🐂 [bold green]Most Bullish:[/bold green] {comparison_summary['most_bullish_source']['source'].title()}")
                console.print(f"🐻 [bold red]Most Bearish:[/bold red] {comparison_summary['most_bearish_source']['source'].title()}")
                console.print(f"🎯 [bold yellow]Highest Confidence:[/bold yellow] {comparison_summary['highest_confidence_source']['source'].title()}")
        
        console.print("\n[bold green]✅ Multi-source analysis completed successfully![/bold green]")
        
        console.print("\n[bold cyan]📋 Summary:[/bold cyan]")
        console.print(f"• Scraped from {len(all_results)} financial news sources")
        console.print(f"• Analyzed {total} articles for sentiment")
        console.print(f"• Overall market sentiment: {outlook['outlook']}")
        console.print(f"• Confidence level: {outlook['confidence']}")
        
    else:
        console.print("[red]❌ No articles found to analyze[/red]")


def demo_individual_sources():
    console = Console()
    
    console.print(Panel("""
╔═══════════════════════════════════════════════════════════════╗
║                Individual Source Testing Demo                 ║
║              Testing Each Financial News Source               ║
╚═══════════════════════════════════════════════════════════════╝
    """, style="bold green"))
    
    available_sources = ScraperFactory.get_available_sources()
    
    for source in available_sources:
        console.print(f"\n[bold yellow]🔍 Testing {source.title()}...[/bold yellow]")
        
        try:
            scraper = ScraperFactory.create_scraper(source)
            data = scraper.get_news_with_metadata()
            
            console.print(f"✅ [green]{source.title()} - Success[/green]")
            console.print(f"   📰 Headlines: {data['total_headlines']}")
            console.print(f"   📈 Market Data: {data['total_stock_news']}")
            
            if data['data']['headlines']:
                console.print(f"   📝 Sample: {data['data']['headlines'][0][:60]}...")
            
        except Exception as e:
            console.print(f"❌ [red]{source.title()} - Error: {str(e)[:50]}...[/red]")
        
        time.sleep(1)


if __name__ == "__main__":
    console = Console()
    
    console.print("[bold cyan]Choose demo mode:[/bold cyan]")
    console.print("1. Full Multi-Source Analysis (Recommended)")
    console.print("2. Individual Source Testing")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "2":
        demo_individual_sources()
    else:
        demo_multi_source_analysis()
    
    console.print("\n[bold magenta]🎉 Demo completed! You can now use the enhanced CLI with:[/bold magenta]")
    console.print("[bold white]python enhanced_cli.py[/bold white]")
