"""CLI entrypoint for Augustus.

This module defines the command-line interface using Typer.
All business logic should be delegated to other modules.
"""

import typer
from typing_extensions import Annotated

from augustus import __version__

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
def index(
    path: Annotated[
        str,
        typer.Argument(help="Path to the folder to index"),
    ] = ".",
) -> None:
    """Index a folder's contents for semantic search.
    
    This command will be implemented in a future step.
    """
    typer.echo(f"[Placeholder] Would index: {path}")
    typer.echo("(Not yet implemented)")


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
