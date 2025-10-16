from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import time
from typing import Dict, List
from scraper import Newscraper
from sentiment import SentimentAnalyzer


class FinancialCLI:
    def __init__(self):
        self.console = Console()
        self.scraper = None
        self.sentiment_analyzer = None

    def display_banner(self):
        banner_text = """
╔═══════════════════════════════════════════════════════════════╗
║                   Financial News Analyzer                     ║
║              Real-time Market Sentiment Analysis              ║
╚═══════════════════════════════════════════════════════════════╝
        """
        self.console.print(Panel(banner_text, style="bold blue", expand=False))

    def initialize_components(self):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task1 = progress.add_task("Initializing web scraper...", total=None)
            self.scraper = Newscraper()
            progress.update(task1, completed=True)
            
            task2 = progress.add_task("Loading sentiment analysis model...", total=None)
            self.sentiment_analyzer = SentimentAnalyzer()
            progress.update(task2, completed=True)

        self.console.print("✅ [green]All components initialized successfully![/green]\n")


    def create_news_table(self, news_data: Dict, title: str) -> Table:
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=4)
        table.add_column("News/Headline", style="white", min_width=50)
        table.add_column("Length", style="cyan", width=8)

        for i, item in enumerate(news_data, 1):
            table.add_row(
                str(i),
                item[:100] + "..." if len(item) > 100 else item,
                str(len(item))
            )
        
        return table

    def create_sentiment_table(self, sentiment_results: List[Dict]) -> Table:
        table = Table(title="📊 Sentiment Analysis Results", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=4)
        table.add_column("Text Preview", style="white", min_width=40)
        table.add_column("Sentiment", style="bold", width=12)
        table.add_column("Confidence", style="cyan", width=12)
        table.add_column("Scores", style="dim", width=30)

        for i, result in enumerate(sentiment_results, 1):
            sentiment = result["sentiment"]
            confidence = result["confidence"]
            
            if sentiment == "Positive":
                sentiment_style = "bold green"
            elif sentiment == "Negative":
                sentiment_style = "bold red"
            else:
                sentiment_style = "bold yellow"

            text_preview = result["text"][:40] + "..." if len(result["text"]) > 40 else result["text"]
            
            scores_text = f"P:{result['scores']['Positive']:.2f} Neu:{result['scores']['Neutral']:.2f} Neg:{result['scores']['Negative']:.2f}"
            
            table.add_row(
                str(i),
                text_preview,
                f"[{sentiment_style}]{sentiment}[/{sentiment_style}]",
                f"{confidence:.3f}",
                scores_text
            )
        
        return table

    def display_sentiment_summary(self, summary: Dict):
        total = summary["total_analyzed"]
        distribution = summary["sentiment_distribution"]
        dominant = summary["dominant_sentiment"]
        avg_conf = summary["average_confidence"]

        summary_text = f"""
[bold]Total Analyzed:[/bold] {total}
[bold]Dominant Sentiment:[/bold] [{'green' if dominant == 'Positive' else 'red' if dominant == 'Negative' else 'yellow'}]{dominant}[/]
[bold]Average Confidence:[/bold] {avg_conf:.3f}

[bold cyan]Distribution:[/bold cyan]
🟢 Positive: {distribution['Positive']} ({distribution['Positive']/total*100:.1f}%)
🟡 Neutral:  {distribution['Neutral']} ({distribution['Neutral']/total*100:.1f}%)
🔴 Negative: {distribution['Negative']} ({distribution['Negative']/total*100:.1f}%)
        """
        
        self.console.print(Panel(summary_text, title="📈 Sentiment Summary", style="bold blue"))

    def scrape_news(self):
        self.console.print("\n[bold yellow]Scraping latest market news...[/bold yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task = progress.add_task("Fetching news data...", total=None)
            news_data = self.scraper.get_news_with_metadata()
            progress.update(task, completed=True)

        self.console.print(f"\n✅ [green]Successfully scraped news from {news_data['source']}[/green]")
        self.console.print(f"📅 [cyan]Timestamp: {news_data['timestamp']}[/cyan]\n")

        if news_data['data']['headlines']:
            headlines_table = self.create_news_table(news_data['data']['headlines'], "📰 Market Headlines")
            self.console.print(headlines_table)

        if news_data['data']['stock_news']:
            stock_table = self.create_news_table(news_data['data']['stock_news'], "📈 Stock Market News")
            self.console.print(stock_table)

        return news_data

    def analyze_sentiment(self, news_data=None):
        if not news_data:
            self.console.print("[red]No news data available. Please scrape news first.[/red]")
            return None

        all_texts = news_data['data']['headlines'] + news_data['data']['stock_news']
        
        if not all_texts:
            self.console.print("[red]No text data to analyze.[/red]")
            return None

        self.console.print("\n[bold yellow]Analyzing sentiment...[/bold yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            task = progress.add_task("Processing sentiment analysis...", total=None)
            summary = self.sentiment_analyzer.get_sentiment_summary(all_texts)
            progress.update(task, completed=True)

        self.display_sentiment_summary(summary)
        return summary

    def full_analysis(self):
        self.console.print("\n[bold magenta]🚀 Starting full analysis...[/bold magenta]")
        
        news_data = self.scrape_news()
        if news_data:
            time.sleep(1)
            sentiment_summary = self.analyze_sentiment(news_data)
            return news_data, sentiment_summary
        return None, None


    def run(self):
        self.display_banner()
        
        try:
            self.initialize_components()
        except Exception as e:
            self.console.print(f"[red]❌ Failed to initialize: {e}[/red]")
            return

        self.console.print("\n[bold magenta]🚀 Starting automatic analysis...[/bold magenta]\n")
        
        news_data, sentiment_summary = self.full_analysis()
        
        if news_data and sentiment_summary:
            self.console.print("\n" + "="*80)
            self.console.print("[bold cyan]📊 DETAILED SENTIMENT BREAKDOWN[/bold cyan]")
            self.console.print("="*80)
            
            sentiment_table = self.create_sentiment_table(sentiment_summary['detailed_results'])
            self.console.print(sentiment_table)
            
            self.console.print("\n[bold green]✅ Analysis completed successfully![/bold green]")
        else:
            self.console.print("[red]❌ Analysis failed. Please check your internet connection.[/red]")


if __name__ == "__main__":
    cli = FinancialCLI()
    cli.run()
