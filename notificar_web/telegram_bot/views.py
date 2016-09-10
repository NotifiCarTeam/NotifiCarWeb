from django.http import HttpResponse, Http404
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from .models import UserBotConversation
from .core import send_message
import json


class BotFacade(View):

    http_method_names = [u'post']

    def post(self, request):
        msg = json.loads((request.body).decode('UTF-8'))
        msg = msg['message']
        chat_id = msg['chat']['id']
        command = msg['text']
        self.handle(command, chat_id)
        return HttpResponse('OK')

    def handle(self, cmd, chat_id):
        cmd_and_args = cmd.split(' ') # The command and it arguments is separated by a blank space
        command = cmd_and_args[0] # The first argument is the command
        handler = self.get_handler(command)
        if handler is not None:
            expected_num_of_args = handler.NUM_OF_ARGS + 1
            if(len(cmd_and_args) == expected_num_of_args):
                args = cmd_and_args[1:] # The arguments is all the list but the first element
                handler.handle(chat_id, *args)
            else:
                missing_args_msg = handler.missing_arguments_message()
                if missing_args_msg is not None:
                    message = {'chat_id': chat_id, 'text': missing_args_msg}
                    send_message(message)

    def get_handler(self, command):
        # Getting the user handlers module
        bot_handlers_module = __import__(settings.BOT_HANDLERS_MODULE)

        if command == '/start':
            handler = bot_handlers_module.handlers.StartCommand()
        elif command == '/help':
            handler = bot_handlers_module.handlers.HelpCommand()
        elif command in bot_handlers_module.handlers.SUPPORTED_COMMANDS:
            handler = bot_handlers_module.handlers.SUPPORTED_COMMANDS[command]()
        else:
            # It is not a recognized command
            handler = None
        return handler

def bot_facade():
  return BotFacade.as_view()