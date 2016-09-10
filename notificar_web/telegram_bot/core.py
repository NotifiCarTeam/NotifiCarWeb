from django.conf import settings
import requests


def send_message(message):
    requests.post('https://api.telegram.org/bot%s/sendMessage' % settings.BOT_TOKEN, data=message)


class CommandHandler:
    """ Base class for bot commands handlers
    """
    def handle(self, chat_id, *args):
        """ Method to handle the requested action
        """
        raise NotImplementedError

    def missing_arguments_message(self):
        """ Method to define the message to display
            when missing arguments from commmand
        """
        return None
