import click
from manage.db import db
from manage.app import app


@click.group()
def cli():
    """Main CLI entry point."""

cli.add_command(db)
cli.add_command(app)

if __name__ == "__main__":
    cli()
