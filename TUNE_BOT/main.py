import os

from aiogram.webhook.aiohttp_server import setup_application, SimpleRequestHandler
from aiohttp.web_app import Application
from aiohttp.web import run_app

from conf.conf_bot import client, dp, PRODUCTION


async def delete_webhook():
    print("Delete webhook\n")
    # await start_build()
    await client.delete_webhook()


async def set_webhook():
    print("Set webhook\n")
    await client.set_webhook(
        url=os.getenv('PRODUCTION_URL'),
        secret_token=os.getenv('TELEGRAM_SECRET_TOKEN'),
    )


def start_development() -> None:
    dp.startup.register(delete_webhook)
    print("Starting DEVELOPMENT BOT")
    dp.run_polling(client)


def start_production() -> None:
    print("Starting PRODUCTION BOT\n")
    dp.startup.register(delete_webhook)
    dp.startup.register(set_webhook)
    app = Application()
    app["bot"] = client
    SimpleRequestHandler(
        dispatcher=dp,
        bot=client,
    ).register(app,  path="/telegram/api/")
    setup_application(app, dp, bot=client)
    run_app(app, host="0.0.0.0", port=8001)


if __name__ == '__main__':
    if PRODUCTION:
        start_production()

    else:
        start_development()
