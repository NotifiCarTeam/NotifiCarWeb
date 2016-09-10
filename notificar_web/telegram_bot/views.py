from django.http import HttpResponse, Http404
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from .models import UserBotConversation
import requests
import json


def send_message(message):
    requests.post('https://api.telegram.org/bot%s/sendMessage' % settings.BOT_TOKEN, data=message)

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
        # Getting the user handlers module
        bot_handlers_mod = __import__(settings.BOT_HANDLERS_MODULE)

        cmd_and_args = cmd.split(' ')
        command = cmd_and_args[0]
        if command == '/start':
            bot_handlers_mod.handlers.StartCommand().handle(cmd_and_args, chat_id)
        elif command == '/help':
            bot_handlers_mod.handlers.HelpCommand().handle(cmd_and_args, chat_id)
        elif command in bot_handlers_mod.handlers.SUPPORTED_COMMANDS:
            bot_handlers_mod.handlers.SUPPORTED_COMMANDS[command]().handle(cmd_and_args, chat_id)
        else:
            # It is not a recognized command
            pass

def bot_facade():
  return BotFacade.as_view()