"""CLI entrypoint for Augustus.

This module defines the command-line interface using Typer.
All business logic should be delegated to other modules.
"""

from pathlib import Path

import typer
from typing_extensions import Annotated

from augustus import __version__
from augustus.ingest.index import ingest_dry_run

app = typer.Typer(
    name="augustus",
    help="A local-first CLI tool for understanding and querying folder contents.",
    add_completion=False,
)


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
) -> None:
    """Ingest a folder's contents (dry-run only for now)."""
    if not dry_run:
        typer.echo("Ingest without --dry-run is not implemented yet.")
        raise typer.Exit(code=1)

    summary = ingest_dry_run(Path(path), sample_size=sample_size)
    typer.echo(f"files discovered: {summary.discovered}")
    typer.echo(f"ignored: {summary.ignored}")
    typer.echo(f"loaded: {summary.loaded}")
    typer.echo("sample files:")
    if summary.sample_paths:
        for rel_path in summary.sample_paths:
            typer.echo(f"- {rel_path}")
    else:
        typer.echo("(none)")


@app.command()
def ask(
    question: Annotated[
        str,
        typer.Argument(help="Question to ask about the indexed folder"),
    ],
) -> None:
    """Ask a question about the indexed folder.
    
    This command will be implemented in a future step.
    """
    typer.echo(f"[Placeholder] Would answer: {question}")
    typer.echo("(Not yet implemented)")


@app.command()
def list() -> None:
    """List all indexed files.
    
    This command will be implemented in a future step.
    """
    typer.echo("[Placeholder] Would list indexed files")
    typer.echo("(Not yet implemented)")


if __name__ == "__main__":
    app()
