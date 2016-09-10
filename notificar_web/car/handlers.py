""" Telegram Bot Handlers file

    This file must contain the command classes do handle the bot requests.

    There are two mandatory commands you MUST implement: StartCommand and HelpCommand.

    The other commands your bot may have, declare them on SUPPORTED_COMMANDS dict in the end of the file.

"""
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from telegram_bot.models import UserBotConversation
from telegram_bot.views import send_message
from car.models import Car
from car import signals

class StartCommand:

    NUM_OF_ARGS = 1

    def handle(self, cmd_and_args, chat_id):
        pass

class HelpCommand:

    NUM_OF_ARGS = 0

    def handle(self, cmd_and_args, chat_id):
        pass


# Beyond the commons /help and /start
SUPPORTED_COMMANDS = {
    # Map here your command classes like this:

    # '/command': ClassToAnswerThisCommand
}
