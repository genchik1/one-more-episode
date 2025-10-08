import asyncio

import click
import granian
from granian.constants import Interfaces, Loops

from src.application.di.container import StoreContainer
from src.interface import scripts
from src.interface.bot.main import main as bot_main

container = StoreContainer()
container.wire(modules=[__name__, scripts.create_embeddings, scripts.send_messages])


@click.group()
def run():
    pass


@click.command()
def save_kp_series():
    asyncio.run(scripts.save_kinopoisk_series())


@click.command()
def save_kp_collections():
    asyncio.run(scripts.save_kinopoisk_collections())


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
    asyncio.run(scripts.save_embeddings())


@click.command()
def send_messages():
    asyncio.run(scripts.send_messages_to_bot())


run.add_command(save_kp_series)
run.add_command(save_kp_collections)
run.add_command(api)
run.add_command(bot)
run.add_command(create_embeddings)
run.add_command(send_messages)


if __name__ == "__main__":
    run()
