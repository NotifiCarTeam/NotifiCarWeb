""" Telegram Bot Handlers file

    This file must contain the command classes do handle the bot requests.

    There are two mandatory commands you MUST implement: StartCommand and HelpCommand.

    The other commands your bot may have, declare them on SUPPORTED_COMMANDS dict in the end of the file.

"""
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from telegram_bot.models import UserBotConversation
from telegram_bot.core import send_message, CommandHandler
from car.models import Car
from car import signals


class StartCommand(CommandHandler):

    NUM_OF_ARGS = 1

    def handle(self, chat_id, username):
        print(username)
        # pass

    def missing_arguments_message(self):
        pass


class HelpCommand(CommandHandler):

    NUM_OF_ARGS = 0

    def handle(self, chat_id):
        pass

    def missing_arguments_message(self):
        pass


# Beyond the commons /help and /start
SUPPORTED_COMMANDS = {
    # Map here your command classes like this:

    # '/command': ClassToAnswerThisCommand
}
