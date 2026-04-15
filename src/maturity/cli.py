"""platform-maturity-model CLI entry point."""

from __future__ import annotations

from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from maturity.core.config import MaturityConfig
from maturity.assessors.repo import assess_from_repos
from maturity.assessors.scorer import compute_assessment
from maturity.reporters.narrator import generate_narrative, generate_roadmap
from maturity.reporters.markdown import generate_report, save_report

app = typer.Typer(name="platform-maturity", help="Platform engineering maturity assessment.")
console = Console()


@app.command("assess")
def assess(
    repo_dir: str = typer.Option(".", "--repo-dir", "-r", help="Directory containing repos"),
    org: str = typer.Option("", "--org", help="Organization name"),
    output: str = typer.Option("", "--output", "-o", help="Output report path"),
) -> None:
    """Assess platform engineering maturity from repositories."""
    config = MaturityConfig.from_env()
    base = Path(repo_dir)
    repos = [d for d in base.iterdir() if d.is_dir() and not d.name.startswith(".")] if base.is_dir() else [base]

    console.print(f"[dim]Scanning {len(repos)} repositories...[/dim]")
    domain_assessments = assess_from_repos(repos)
    assessment = compute_assessment(org or base.name, domain_assessments, config.industry)
    assessment.narrative = generate_narrative(assessment, config)
    assessment.roadmap = generate_roadmap(assessment)

    level_colors = {1: "red", 2: "orange3", 3: "yellow", 4: "cyan", 5: "green"}
    color = level_colors.get(assessment.overall_level, "white")

    console.print(Panel.fit(
        f"Overall level: [{color}]{assessment.overall_level}/5 — {assessment.level_name}[/{color}]\n"
        f"Score: [bold]{assessment.overall_score:.2f}/5.0[/bold]\n"
        f"Repos scanned: {len(repos)}",
        title="Platform Maturity Assessment",
        border_style="blue",
    ))

    table = Table(border_style="dim")
    table.add_column("Domain", style="bold")
    table.add_column("Level", justify="center")
    table.add_column("Evidence", justify="center")
    table.add_column("Top gap", style="dim")

    for da in assessment.domains:
        c = level_colors.get(da.assessed_level, "white")
        table.add_row(
            da.domain,
            f"[{c}]{da.assessed_level}/5[/{c}]",
            str(da.evidence_count),
            da.gaps[0] if da.gaps else "-",
        )
    console.print(table)

    if output:
        Path(output).write_text(generate_report(assessment))
        console.print(f"[green]✓[/green] Report saved to [cyan]{output}[/cyan]")
    else:
        path = save_report(assessment)
        console.print(f"[green]✓[/green] Report saved to [cyan]{path}[/cyan]")


@app.command("roadmap")
def roadmap(
    repo_dir: str = typer.Option(".", "--repo-dir", "-r"),
    target_level: int = typer.Option(0, "--target-level", "-t"),
) -> None:
    """Generate a prioritized roadmap to the next maturity level."""
    config = MaturityConfig.from_env()
    base = Path(repo_dir)
    repos = [d for d in base.iterdir() if d.is_dir() and not d.name.startswith(".")] if base.is_dir() else [base]

    domain_assessments = assess_from_repos(repos)
    assessment = compute_assessment(base.name, domain_assessments, config.industry)
    items = generate_roadmap(assessment, target_level)

    target = target_level or min(5, assessment.overall_level + 1)
    console.print(f"\n[bold]Roadmap to Level {target}[/bold] (from Level {assessment.overall_level})\n")
    for i, item in enumerate(items, 1):
        console.print(f"  {i}. [dim]{item}[/dim]")
    console.print()


def main() -> None:
    app()


if __name__ == "__main__":
    main()