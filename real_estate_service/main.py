from telegram import Update
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
from django.core.asgi import get_asgi_application
import uvicorn
import django
import os
import logging
import json
import asyncio
from dotenv import load_dotenv

load_dotenv()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate_service.settings')
django.setup()

from tg_bot import tgbot_core  # noqa E402

WEBHOOK_URL = 'https://428ff6f4-59a6-4e0b-a428-278c4a81ea85.tunnel4.com'
PORT = 8000


@csrf_exempt
async def webhook(request: HttpRequest) -> HttpResponse:
    """Handle incoming Telegram updates by putting them
    into the `update_queue`"""
    await tgbot_core.tgbot.ptb_app.update_queue.put(
        Update.de_json(
            data=json.loads(request.body),
            bot=tgbot_core.tgbot.ptb_app.bot)
    )
    return HttpResponse()


async def main():
    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=get_asgi_application(),
            port=PORT,
            use_colors=True,
            host='localhost',
            log_level=logging.DEBUG,
        )
    )

    await tgbot_core.tgbot.ptb_app.bot.setWebhook(
        url=f'{WEBHOOK_URL}/telegram/',
        allowed_updates=Update.ALL_TYPES,
    )

    async with tgbot_core.tgbot.ptb_app:
        await tgbot_core.tgbot.ptb_app.start()
        await webserver.serve()
        await tgbot_core.tgbot.ptb_app.stop()


if __name__ == '__main__':
    asyncio.run(main())
