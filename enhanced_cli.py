from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
import time
from typing import Dict, List, Optional
from multi_scraper import MultiSourceScraper, ScraperFactory
from sentiment import SentimentAnalyzer


class EnhancedFinancialCLI:
    def __init__(self):
        self.console = Console()
        self.multi_scraper = None
        self.sentiment_analyzer = None
        self.available_sources = ScraperFactory.get_available_sources()

    def display_banner(self):
        banner_text = """
╔═══════════════════════════════════════════════════════════════╗
║                Multi-Source Financial Analyzer                ║
║         Real-time Market Sentiment from Multiple Sources      ║
║                                                               ║
║  📊 LiveMint  📈 Google Finance  💰 Yahoo Finance  📰 MarketWatch ║
╚═══════════════════════════════════════════════════════════════╝
        """
        self.console.print(Panel(banner_text, style="bold blue", expand=False))

    def display_available_sources(self):
        source_info = {
            "livemint": "📊 LiveMint - Indian market news and analysis",
            "google": "📈 Google Finance - Global market data and news",
            "yahoo": "💰 Yahoo Finance - Comprehensive financial news",
            "marketwatch": "📰 MarketWatch - Real-time market updates"
        }
        
        self.console.print("\n[bold cyan]Available News Sources:[/bold cyan]")
        for source in self.available_sources:
            self.console.print(f"  • {source_info.get(source, f'{source.title()} - Financial news')}")

    def select_sources(self) -> List[str]:
        self.display_available_sources()
        
        self.console.print("\n[bold yellow]Source Selection Options:[/bold yellow]")
        self.console.print("1. All sources (recommended)")
        self.console.print("2. Select specific sources")
        self.console.print("3. Quick analysis (LiveMint + Google)")
        
        choice = Prompt.ask("\nChoose option", choices=["1", "2", "3"], default="1")
        
        if choice == "1":
            return self.available_sources
        elif choice == "2":
            selected = []
            for source in self.available_sources:
                if Confirm.ask(f"Include {source.title()}?", default=True):
                    selected.append(source)
            return selected if selected else ["livemint"]
        else:
            return ["livemint", "google"]

    def initialize_components(self, selected_sources: List[str]):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task1 = progress.add_task("Initializing multi-source scraper...", total=None)
            self.multi_scraper = MultiSourceScraper(selected_sources)
            progress.update(task1, completed=True)
            
            task2 = progress.add_task("Loading sentiment analysis model...", total=None)
            self.sentiment_analyzer = SentimentAnalyzer()
            progress.update(task2, completed=True)

        self.console.print("✅ [green]All components initialized successfully![/green]\n")

    def create_source_summary_table(self, all_results: Dict) -> Table:
        table = Table(title="📊 Source Summary", show_header=True, header_style="bold magenta")
        table.add_column("Source", style="bold cyan", width=15)
        table.add_column("Status", style="white", width=10)
        table.add_column("Headlines", style="green", width=10)
        table.add_column("Market Data", style="yellow", width=12)
        table.add_column("Total Items", style="bold", width=12)

        for source, data in all_results.items():
            if "error" in data:
                status = "[red]Error[/red]"
                headlines = "0"
                market_data = "0"
                total = "0"
            else:
                status = "[green]Success[/green]"
                headlines = str(data.get("total_headlines", 0))
                market_data = str(data.get("total_stock_news", 0))
                total = str(int(headlines) + int(market_data))

            table.add_row(
                source.title(),
                status,
                headlines,
                market_data,
                total
            )
        
        return table

    def create_combined_news_table(self, news_data: List[str], title: str, max_items: int = 20) -> Table:
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=4)
        table.add_column("News/Headline", style="white", min_width=60)
        table.add_column("Length", style="cyan", width=8)

        for i, item in enumerate(news_data[:max_items], 1):
            preview = item[:120] + "..." if len(item) > 120 else item
            table.add_row(
                str(i),
                preview,
                str(len(item))
            )
        
        if len(news_data) > max_items:
            table.add_row("...", f"[dim]({len(news_data) - max_items} more items)[/dim]", "")
        
        return table

    def create_sentiment_table(self, sentiment_results: List[Dict], max_items: int = 25) -> Table:
        table = Table(title="📊 Sentiment Analysis Results", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=4)
        table.add_column("Text Preview", style="white", min_width=50)
        table.add_column("Sentiment", style="bold", width=12)
        table.add_column("Confidence", style="cyan", width=12)
        table.add_column("Scores", style="dim", width=35)

        for i, result in enumerate(sentiment_results[:max_items], 1):
            sentiment = result["sentiment"]
            confidence = result["confidence"]
            
            if sentiment == "Positive":
                sentiment_style = "bold green"
            elif sentiment == "Negative":
                sentiment_style = "bold red"
            else:
                sentiment_style = "bold yellow"

            text_preview = result["text"][:50] + "..." if len(result["text"]) > 50 else result["text"]
            
            scores_text = f"P:{result['scores']['Positive']:.2f} Neu:{result['scores']['Neutral']:.2f} Neg:{result['scores']['Negative']:.2f}"
            
            table.add_row(
                str(i),
                text_preview,
                f"[{sentiment_style}]{sentiment}[/{sentiment_style}]",
                f"{confidence:.3f}",
                scores_text
            )
        
        if len(sentiment_results) > max_items:
            table.add_row("...", f"[dim]({len(sentiment_results) - max_items} more items)[/dim]", "", "", "")
        
        return table

    def display_sentiment_summary(self, summary: Dict, sources_info: Dict):
        total = summary["total_analyzed"]
        distribution = summary["sentiment_distribution"]
        dominant = summary["dominant_sentiment"]
        avg_conf = summary["average_confidence"]

        summary_text = f"""
[bold]Total Articles Analyzed:[/bold] {total}
[bold]Sources Used:[/bold] {', '.join([s.title() for s in sources_info.get('sources', [])])}
[bold]Dominant Sentiment:[/bold] [{'green' if dominant == 'Positive' else 'red' if dominant == 'Negative' else 'yellow'}]{dominant}[/]
[bold]Average Confidence:[/bold] {avg_conf:.3f}

[bold cyan]Sentiment Distribution:[/bold cyan]
🟢 Positive: {distribution['Positive']} ({distribution['Positive']/total*100:.1f}%)
🟡 Neutral:  {distribution['Neutral']} ({distribution['Neutral']/total*100:.1f}%)
🔴 Negative: {distribution['Negative']} ({distribution['Negative']/total*100:.1f}%)

[bold magenta]Market Outlook:[/bold magenta] {'Bullish 📈' if dominant == 'Positive' else 'Bearish 📉' if dominant == 'Negative' else 'Mixed 📊'}
        """
        
        self.console.print(Panel(summary_text, title="📈 Multi-Source Sentiment Summary", style="bold blue"))

    def scrape_all_sources(self):
        self.console.print("\n[bold yellow]Scraping from all selected sources...[/bold yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task = progress.add_task("Fetching news from multiple sources...", total=None)
            all_results = self.multi_scraper.scrape_all_sources()
            progress.update(task, completed=True)

        self.console.print(f"\n✅ [green]Successfully scraped from {len(all_results)} sources[/green]")
        
        summary_table = self.create_source_summary_table(all_results)
        self.console.print(summary_table)

        return all_results

    def get_combined_analysis(self):
        self.console.print("\n[bold yellow]Getting combined news analysis...[/bold yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task = progress.add_task("Combining news from all sources...", total=None)
            combined_data = self.multi_scraper.get_combined_news()
            progress.update(task, completed=True)

        return combined_data

    def analyze_sentiment(self, combined_data: Dict):
        all_texts = combined_data.get("headlines", []) + combined_data.get("stock_news", [])
        
        if not all_texts:
            self.console.print("[red]No text data to analyze.[/red]")
            return None

        self.console.print(f"\n[bold yellow]Analyzing sentiment for {len(all_texts)} articles...[/bold yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task = progress.add_task("Processing multi-source sentiment analysis...", total=None)
            summary = self.sentiment_analyzer.get_sentiment_summary(all_texts)
            progress.update(task, completed=True)

        self.display_sentiment_summary(summary, combined_data)
        return summary

    def full_analysis(self):
        self.console.print("\n[bold magenta]🚀 Starting comprehensive multi-source analysis...[/bold magenta]")
        
        all_results = self.scrape_all_sources()
        if not all_results:
            return None, None, None
        
        time.sleep(1)
        combined_data = self.get_combined_analysis()
        
        if combined_data.get("headlines") or combined_data.get("stock_news"):
            self.console.print(f"\n[bold green]📰 Found {len(combined_data.get('headlines', []))} headlines and {len(combined_data.get('stock_news', []))} market updates[/bold green]")
            
            if combined_data.get("headlines"):
                headlines_table = self.create_combined_news_table(
                    combined_data["headlines"], 
                    "📰 Combined Headlines from All Sources"
                )
                self.console.print(headlines_table)
            
            if combined_data.get("stock_news"):
                stock_table = self.create_combined_news_table(
                    combined_data["stock_news"], 
                    "📈 Combined Market Data from All Sources"
                )
                self.console.print(stock_table)
            
            time.sleep(1)
            sentiment_summary = self.analyze_sentiment(combined_data)
            return all_results, combined_data, sentiment_summary
        
        return all_results, combined_data, None

    def interactive_mode(self):
        while True:
            self.console.print("\n[bold cyan]🔄 Interactive Mode[/bold cyan]")
            self.console.print("1. Run full analysis")
            self.console.print("2. Scrape specific source")
            self.console.print("3. Change sources")
            self.console.print("4. Exit")
            
            choice = Prompt.ask("Choose option", choices=["1", "2", "3", "4"], default="1")
            
            if choice == "1":
                self.full_analysis()
            elif choice == "2":
                source = Prompt.ask("Enter source name", choices=self.available_sources)
                try:
                    scraper = ScraperFactory.create_scraper(source)
                    data = scraper.get_news_with_metadata()
                    self.console.print(f"✅ Scraped {data['total_headlines']} headlines from {source}")
                except Exception as e:
                    self.console.print(f"[red]Error: {e}[/red]")
            elif choice == "3":
                selected_sources = self.select_sources()
                self.multi_scraper = MultiSourceScraper(selected_sources)
                self.console.print(f"✅ Updated sources: {', '.join(selected_sources)}")
            else:
                break

    def run(self):
        self.display_banner()
        
        selected_sources = self.select_sources()
        self.console.print(f"\n[bold green]Selected sources: {', '.join([s.title() for s in selected_sources])}[/bold green]")
        
        try:
            self.initialize_components(selected_sources)
        except Exception as e:
            self.console.print(f"[red]❌ Failed to initialize: {e}[/red]")
            return

        all_results, combined_data, sentiment_summary = self.full_analysis()
        
        if sentiment_summary:
            self.console.print("\n" + "="*100)
            self.console.print("[bold cyan]📊 DETAILED MULTI-SOURCE SENTIMENT BREAKDOWN[/bold cyan]")
            self.console.print("="*100)
            
            sentiment_table = self.create_sentiment_table(sentiment_summary['detailed_results'])
            self.console.print(sentiment_table)
            
            self.console.print("\n[bold green]✅ Multi-source analysis completed successfully![/bold green]")
            
            if Confirm.ask("\nEnter interactive mode?", default=False):
                self.interactive_mode()
        else:
            self.console.print("[red]❌ Analysis failed. Please check your internet connection.[/red]")


if __name__ == "__main__":
    cli = EnhancedFinancialCLI()
    cli.run()
