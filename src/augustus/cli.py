"""CLI entrypoint for Augustus.

This module defines the command-line interface using Typer.
All business logic should be delegated to other modules.
"""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from typing_extensions import Annotated

from augustus import __version__
from augustus.ingest.index import VectorIndex, ingest_dry_run, ingest_folder

app = typer.Typer(
    name="augustus",
    help="A local-first CLI tool for understanding and querying folder contents.",
    add_completion=False,
)

console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        typer.echo(f"Augustus version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="Show version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Augustus - understand and query folder contents locally."""
    pass


@app.command()
def ingest(
    path: Annotated[
        str,
        typer.Argument(help="Path to the folder to ingest"),
    ] = ".",
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Print counts without indexing"),
    ] = False,
    sample_size: Annotated[
        int,
        typer.Option("--sample-size", min=1, help="Sample list size"),
    ] = 5,
    chunk_size: Annotated[
        int,
        typer.Option("--chunk-size", help="Chunk size in characters"),
    ] = 1000,
    chunk_overlap: Annotated[
        int,
        typer.Option("--chunk-overlap", help="Overlap between chunks"),
    ] = 200,
) -> None:
    """Ingest a folder's contents and build a searchable index."""
    folder_path = Path(path).resolve()

    if not folder_path.exists():
        console.print(f"[red]Error:[/red] Path does not exist: {folder_path}")
        raise typer.Exit(code=1)

    if not folder_path.is_dir():
        console.print(f"[red]Error:[/red] Not a directory: {folder_path}")
        raise typer.Exit(code=1)

    if dry_run:
        console.print("[dim]Running in dry-run mode (no index created)[/dim]\n")
        summary = ingest_dry_run(folder_path, sample_size=sample_size)

        console.print(f"files discovered: {summary.discovered}")
        console.print(f"ignored: {summary.ignored}")
        console.print(f"loaded: {summary.loaded}")
        console.print("\nsample files:")
        if summary.sample_paths:
            for rel_path in summary.sample_paths:
                console.print(f"  - {rel_path}")
        else:
            console.print("  (none)")
    else:
        console.print(f"[bold]Indexing folder:[/bold] {folder_path}\n")

        try:
            with console.status("[bold green]Loading and chunking files..."):
                summary = ingest_folder(
                    folder_path,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                )

            console.print(
                Panel(
                    f"[green]Index created successfully![/green]\n\n"
                    f"Files discovered: {summary.discovered}\n"
                    f"Files ignored: {summary.ignored}\n"
                    f"Files loaded: {summary.loaded}\n"
                    f"Chunks indexed: {summary.chunks}\n\n"
                    f"Index saved to: {folder_path / '.augustus'}",
                    title="Ingestion Complete",
                )
            )
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(code=1)
        except Exception as e:
            console.print(f"[red]Error during indexing:[/red] {e}")
            raise typer.Exit(code=1)


@app.command()
def ask(
    question: Annotated[
        str,
        typer.Argument(help="Question to ask about the indexed folder"),
    ],
    path: Annotated[
        str,
        typer.Option("--path", "-p", help="Path to the indexed folder"),
    ] = ".",
    k: Annotated[
        int,
        typer.Option("--results", "-k", help="Number of results to retrieve"),
    ] = 5,
) -> None:
    """Ask a question about the indexed folder.

    This command will be fully implemented in a future step.
    Currently shows retrieved context only.
    """
    folder_path = Path(path).resolve()
    index = VectorIndex(folder_path)

    if not index.exists():
        console.print(
            f"[red]Error:[/red] No index found at {folder_path / '.augustus'}\n"
            f"Run [bold]augustus ingest {path}[/bold] first."
        )
        raise typer.Exit(code=1)

    try:
        with console.status("[bold green]Searching..."):
            results = index.search(question, k=k)

        if not results:
            console.print("[yellow]No relevant results found.[/yellow]")
            return

        console.print(f"\n[bold]Question:[/bold] {question}\n")
        console.print(f"[dim]Found {len(results)} relevant chunks:[/dim]\n")

        for i, result in enumerate(results, 1):
            source = result["metadata"].get("source", "unknown")
            score = result["score"]
            content = result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"]

            console.print(
                Panel(
                    f"[dim]{content}[/dim]",
                    title=f"[{i}] {source} (score: {score:.3f})",
                )
            )

        console.print(
            "\n[dim]Note: Full answer generation will be implemented in a future step.[/dim]"
        )

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)


@app.command(name="list")
def list_files(
    path: Annotated[
        str,
        typer.Option("--path", "-p", help="Path to the indexed folder"),
    ] = ".",
) -> None:
    """List all indexed files.

    This command will be implemented in a future step.
    """
    folder_path = Path(path).resolve()
    index = VectorIndex(folder_path)

    if not index.exists():
        console.print(
            f"[red]Error:[/red] No index found at {folder_path / '.augustus'}\n"
            f"Run [bold]augustus ingest {path}[/bold] first."
        )
        raise typer.Exit(code=1)

    console.print("[yellow]List command not fully implemented yet.[/yellow]")
    console.print(f"Index exists at: {folder_path / '.augustus'}")


if __name__ == "__main__":
    app()
