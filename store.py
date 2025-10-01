import asyncio

import click
import uvicorn

from src.application.di.container import StoreContainer
from src.interface.api.app import create_app
from src.interface.bot.main import main as bot_main
from src.interface.scripts import save_kinopoisk_collections, save_kinopoisk_series

container = StoreContainer()
container.wire(modules=[__name__])


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
    uvicorn.run(
        app=create_app(),
        # host="0.0.0.0",
        port=8000,
        workers=1,
        loop="uvloop",
    )


@click.command()
def bot():
    asyncio.run(bot_main())


run.add_command(save_kp_series)
run.add_command(save_kp_collections)
run.add_command(api)
run.add_command(bot)


if __name__ == "__main__":
    run()
