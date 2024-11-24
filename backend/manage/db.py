import click
from meditranslate.app.db.session import engines

@click.group()
def db():
    """Database-related commands."""
    pass

@db.command()
def seed():
    """Seed the database with initial data."""
    click.echo("Seeding the database...")


@db.command()
def drop_all():
    click.echo("drop_all!")

@db.command()
def recreate_all():
    # async def create_All():
    #     async with engine.begin() as conn:
    #         await conn.run_sync(Base.metadata.drop_all)
    #         await conn.run_sync(Base.metadata.create_all)
    click.echo("recreate all")


@db.command()
def create_all():
    click.echo("create_all")

@db.command()
def migrate_online():
    click.echo("migrate_online")

@db.command()
def migrate_offline():
    click.echo("migrate_offline")



