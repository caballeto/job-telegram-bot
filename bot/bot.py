#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

# create linkedin account
# create alerts for top 10 companies for swe intern / new grad / swe
# once a day load emails from email
# get each posting page, extract company, type (intern,grad,full)
# save to db

# update this bot script to make requests to database
# add redis cache with 1 hour ttl

# deploy to digital ocean

import logging
import config

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from db import get_internships, get_grads, get_swes, get_all


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    logger.info('Printing start message')
    update.message.reply_text(
        'Hi! I am Faang Bot. I will post open jobs positions at Faang. '
        'Here\'s what I can do.\n\n'
        '/start - start talking with bot\n'
        '/help - help message with command descriptions\n'
        '/all - show all open internship/new-grad positions\n'
        '/newgrad - show all new-grad positions\n'
        '/intern - show all intern positions\n')


def help(update, context):
    logger.info('Printing help message')
    update.message.reply_text(
        'Here\'s what I can do.\n\n'
        '/start - start talking with bot\n'
        '/help - help message with command descriptions\n'
        '/all - show all open positions\n'
        '/newgrad - show all new-grad positions\n'
        '/intern - show all intern positions\n')


def all(update, context):
    jobs = get_grads()
    jobs.extend(get_internships())
    logger.info('Printing {0} ALL jobs'.format(len(jobs)))
    update.message.reply_text('Printing all open internship and grad positions')
    for job in jobs:
        update.message.reply_text(job['link'])


def newgrad(update, context):
    jobs = get_grads()
    logger.info('Printing {0} ALL jobs'.format(len(jobs)))
    update.message.reply_text('Here\'s some new grad postings I\'ve found')
    for job in jobs:
        update.message.reply_text(job['link'])


def intern(update, context):
    jobs = get_internships()
    logger.info('Printing {0} ALL jobs'.format(len(jobs)))
    update.message.reply_text('Here\'s some internships I\'ve found')
    for job in jobs:
        update.message.reply_text(job['link'])


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1003656495:AAFHvQX8ZEb3RS83fHD72iaFI49pxKQMoa4", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('all', all))
    dp.add_handler(CommandHandler('newgrad', newgrad))
    dp.add_handler(CommandHandler('intern', intern))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
