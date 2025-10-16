#!/usr/bin/env python3

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def show_sample_output():
    banner_text = """
╔═══════════════════════════════════════════════════════════════╗
║                   Financial News Analyzer                     ║
║              Real-time Market Sentiment Analysis              ║
╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner_text, style="bold blue", expand=False))
    
    console.print("✅ [green]All components initialized successfully![/green]\n")
    console.print("\n[bold magenta]🚀 Starting automatic analysis...[/bold magenta]\n")
    
    console.print("\n[bold yellow]Scraping latest market news...[/bold yellow]")
    console.print("\n✅ [green]Successfully scraped news from https://www.livemint.com/market[/green]")
    console.print("📅 [cyan]Timestamp: 2024-10-16 15:30:45[/cyan]\n")
    
    headlines_table = Table(title="📰 Market Headlines", show_header=True, header_style="bold magenta")
    headlines_table.add_column("ID", style="dim", width=4)
    headlines_table.add_column("News/Headline", style="white", min_width=50)
    headlines_table.add_column("Length", style="cyan", width=8)
    
    sample_headlines = [
        "Gold price today: Rates hit a new high of $4,289 on global market uncertainty",
        "Reliance Q2 results preview: Revenue, profit may rise on strong petrochemical performance",
        "Eternal share price: Will Friday bring a rebound or further decline?",
        "Infosys ADR shares crash 4% on NYSE after Q2 results disappoint investors"
    ]
    
    for i, headline in enumerate(sample_headlines, 1):
        headlines_table.add_row(str(i), headline, str(len(headline)))
    
    console.print(headlines_table)
    
    console.print("\n[bold yellow]Analyzing sentiment...[/bold yellow]")
    
    summary_text = """
[bold]Total Analyzed:[/bold] 4
[bold]Dominant Sentiment:[/bold] [green]Positive[/]
[bold]Average Confidence:[/bold] 0.728

[bold cyan]Distribution:[/bold cyan]
🟢 Positive: 2 (50.0%)
🟡 Neutral:  1 (25.0%)
🔴 Negative: 1 (25.0%)
    """
    
    console.print(Panel(summary_text, title="📈 Sentiment Summary", style="bold blue"))
    
    console.print("\n" + "="*80)
    console.print("[bold cyan]📊 DETAILED SENTIMENT BREAKDOWN[/bold cyan]")
    console.print("="*80)
    
    sentiment_table = Table(title="📊 Sentiment Analysis Results", show_header=True, header_style="bold magenta")
    sentiment_table.add_column("ID", style="dim", width=4)
    sentiment_table.add_column("Text Preview", style="white", min_width=40)
    sentiment_table.add_column("Sentiment", style="bold", width=12)
    sentiment_table.add_column("Confidence", style="cyan", width=12)
    sentiment_table.add_column("Scores", style="dim", width=30)
    
    sample_results = [
        ("Gold price today: Rates hit a new high...", "Positive", 0.558, "P:0.56 Neu:0.32 Neg:0.12"),
        ("Reliance Q2 results preview: Revenue...", "Positive", 0.686, "P:0.69 Neu:0.23 Neg:0.08"),
        ("Eternal share price: Will Friday bring...", "Neutral", 0.814, "P:0.15 Neu:0.81 Neg:0.04"),
        ("Infosys ADR shares crash 4% on NYSE...", "Negative", 0.855, "P:0.05 Neu:0.09 Neg:0.86")
    ]
    
    for i, (text, sentiment, confidence, scores) in enumerate(sample_results, 1):
        if sentiment == "Positive":
            sentiment_style = "bold green"
        elif sentiment == "Negative":
            sentiment_style = "bold red"
        else:
            sentiment_style = "bold yellow"
        
        sentiment_table.add_row(
            str(i),
            text,
            f"[{sentiment_style}]{sentiment}[/{sentiment_style}]",
            f"{confidence:.3f}",
            scores
        )
    
    console.print(sentiment_table)
    console.print("\n[bold green]✅ Analysis completed successfully![/bold green]")

if __name__ == "__main__":
    show_sample_output()
