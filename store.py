import asyncio

import click
import granian
from granian.constants import Interfaces, Loops

from src.application.di.container import StoreContainer
from src.interface.bot.main import main as bot_main
from src.interface.scripts import create_embeddings, save_embeddings, save_kinopoisk_collections, save_kinopoisk_series

container = StoreContainer()
container.wire(modules=[__name__, create_embeddings])


@click.group()
def run():
    pass


@click.command()
def save_kp_series():
    asyncio.run(save_kinopoisk_series())


@click.command()
def save_kp_collections():
    asyncio.run(save_kinopoisk_collections())


@click.command()
def api():
    granian.Granian(
        "src.interface.api.app.py:app",
        address="0.0.0.0",
        port=8000,
        workers=1,
        loop=Loops.asyncio,
        websockets=False,
        log_level="info",
        log_access=True,
        log_enabled=True,
        interface=Interfaces.ASGI,
    ).serve()


@click.command()
def bot():
    asyncio.run(bot_main())


@click.command()
def create_embeddings():
    asyncio.run(save_embeddings())


run.add_command(save_kp_series)
run.add_command(save_kp_collections)
run.add_command(api)
run.add_command(bot)
run.add_command(create_embeddings)


if __name__ == "__main__":
    run()
