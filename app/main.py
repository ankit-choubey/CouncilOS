import sys

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

def show_welcome():
    if HAS_RICH:
        console = Console()
        title = Text("CouncilOS", style="bold cyan")
        subtitle = Text("⚖️ Multi-Agent Orchestration & Coordination Framework", style="italic white")
        
        panel = Panel(
            Text.assemble(title, "\n", subtitle),
            subtitle="v0.1.0",
            subtitle_align="right",
            border_style="cyan",
            expand=False
        )
        console.print(panel)
    else:
        print("=" * 60)
        print("CouncilOS ⚖️")
        print("Multi-Agent Orchestration & Coordination Framework")
        print("v0.1.0")
        print("=" * 60)

def main():
    show_welcome()
    if HAS_RICH:
        console = Console()
        console.print("[green]Initializing CouncilOS application...[/green]")
        console.print("[yellow]Ready for dynamic multi-agent debate.[/yellow]")
    else:
        print("Initializing CouncilOS application...")
        print("Ready for dynamic multi-agent debate.")

if __name__ == "__main__":
    main()

