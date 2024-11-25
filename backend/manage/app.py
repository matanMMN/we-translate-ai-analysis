import click
from meditranslate.app.configurations import config
from meditranslate.app.loggers import logger
from globals import *

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group()
def app():
    """CLI for Managing the application"""
    click.echo(CLI_DIVIDER)
    # app.echo(f"Project Root: {ROOT_DIR}")
    # app.echo(f"python version: {PYTHON_VERSION}")
    # app = f"{config.APP_NAME} ({config.RELEASE_VERSION})"
    # app.echo(app)


@app.command()
def debug():
    pass

@app.command()
def runserver():
    pass

