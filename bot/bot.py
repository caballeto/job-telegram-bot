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

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, MessageEntity
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from db import get_internships, get_grads, get_swes, get_all, save_link


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

LINK = 1


def start(update, context):
    logger.info('Printing start message')
    update.message.reply_text(
        'Hi! I am Faang Bot. I will post open jobs positions at Faang. '
        'Here\'s what I can do.\n\n'
        '/start - start talking with bot\n'
        '/help - help message with command descriptions\n'
        '/intern - show open intern positions\n'
        '/newgrad - show open new grad positions\n'
        '/experienced - show positions for experienced candidates\n'
        '/new - propose position job posting\n')


def help(update, context):
    logger.info('Printing help message')
    update.message.reply_text(
        'Here\'s what I can do.\n\n'
        '/start - start talking with bot\n'
        '/help - help message with command descriptions\n'
        '/all - show all open positions\n'
        '/newgrad - show all new-grad positions\n'
        '/intern - show all intern positions\n')


def experienced(update, context):
    update.message.reply_text('This feature is still in development. We\'ll notify you as soon as it will be available :)')


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


def new(update, context):
    logger.info('Adding new link proposal')
    update.message.reply_text('Thanks for contributing, please send me a URL to job posting. Send /cancel to cancel command.')
    return LINK


def received_link(update, context):
    user_data = context.user_data
    user = update.message.from_user
    link = update.message.text
    save_link(link, user['username'])
    update.message.reply_text('Thanks {0}, I will review the link during the next 24 hours, and will add it if everything is cool!'.format(user['first_name']))
    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation", user.first_name)
    update.message.reply_text('Okay, hope to talk about it again some day.')
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(config.API_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    new_handler = ConversationHandler(
        entry_points=[CommandHandler('new', new)],

        states = {
            LINK: [MessageHandler(Filters.entity(MessageEntity.URL), received_link)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(new_handler)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('experienced', experienced))
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
