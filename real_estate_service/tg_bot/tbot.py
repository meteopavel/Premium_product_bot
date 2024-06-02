#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from object.models import City, Realty
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

CHOOSE_AREA, REPRESERNT_RESULTS = range(2)

reply_keyboard = [

]


async def choose_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    reply_keyboard = []
    async for city in City.objects.all().values_list('name', flat=True):
        reply_keyboard.append([str(city)])
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Hi! My name is Doctor Botter. I will hold a more complex conversation with you. "
        "Why don't you tell me something about yourself?",
        reply_markup=markup,
    )

    return CHOOSE_AREA


async def choose_area(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    user_data['city'] = update.message.text
    reply_keyboard = [['1-150'],
                      ['150-200'],
                      ['200-10000']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Set the area ",
        reply_markup=markup,
    )
    return REPRESERNT_RESULTS


async def represent_results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    user_data['area'] = update.message.text
    min_area = user_data['area'].split('-')[0]
    max_area = user_data['area'].split('-')[1]
    realty = Realty.objects.filter(city__name=user_data['city'])
    realty_area_gt = realty.filter(area__gt=min_area)
    realty_area_lt = await realty_area_gt.filter(area__lt=max_area).afirst()
    await update.message.reply_text(
        f'{min_area}, {max_area}, {realty_area_lt.title}'
    )
    return ConversationHandler.END


def main(token) -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", choose_city)],
        states={
            CHOOSE_AREA: [
                MessageHandler(
                    filters.Regex(
                        ".*"), choose_area
                ),
            ],
            REPRESERNT_RESULTS: [
                MessageHandler(
                    filters.Regex(
                        ".*"
                    ), represent_results
                )
            ]
        },
        fallbacks=[MessageHandler(filters.Regex(
            "^Done$"), choose_city)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
