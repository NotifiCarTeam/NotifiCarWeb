import json

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View

from .core import send_message


class BotFacade(View):

    START_COMMAND = '/start'
    HELP_COMMAND = '/help'

    http_method_names = [u'post']

    def post(self, request):
        msg = json.loads((request.body).decode('UTF-8'))
        print("MESSAGE:")
        print(msg)
        return self.handle_request_type(msg)

    def handle_request_type(self, request_dict):
        if 'message' in request_dict:
            """ In this case is a command request """
            msg = request_dict['message']
            chat_id = msg['chat']['id']
            if 'text' in msg:
                user_input = msg['text']
                self.handle_command(user_input, chat_id)
                response = HttpResponse('OK')
            else:
                response = HttpResponse(
                    'Not text requests not supported at the moment'
                )
        elif 'callback_query' in request_dict:
            """ In this case is callback from a inline button request """
            query = request_dict['callback_query']
            data = json.loads(query['data'])
            data['query_id'] = query['id']
            cmd = data["cmd"]

            bot_handlers_module = __import__(settings.BOT_HANDLERS_MODULE)
            handler = bot_handlers_module.handlers.SUPPORTED_COMMANDS[cmd]()

            handler.handle_callback_query(**data)

            response = HttpResponse('Callback OK')
        else:
            response = HttpResponse('Request not supported at the moment')

        return response

    def handle_command(self, user_input, chat_id):
        command, args = self.extract_command_args(user_input)
        handler = self.get_handler(command)
        if handler is not None:
            if(len(args) == handler.NUM_OF_ARGS):
                handler.handle(chat_id, *args)
            else:
                missing_args_msg = handler.missing_arguments_message()
                if missing_args_msg is not None:
                    message = {'chat_id': chat_id, 'text': missing_args_msg}
                    send_message(message)

    def extract_command_args(self, user_input):
        import re
        # The command starts with a forward slash (/)
        # and may have up to 32 characters
        command_re = re.compile(r'^/([a-zA-Z0-9_]{1,31})')
        re_match = command_re.match(user_input)

        if re_match is not None:
            command = re_match.group()
            args_str = user_input.replace(command, '')
            clean_spaces_re = re.compile("^\s+|\s*,\s*|\s+$")
            args = [e for e in clean_spaces_re.split(args_str) if e]
        else:
            command = None
            args = None

        return command, args

    def get_handler(self, command):
        # Getting the user handlers module

        bot_handlers_module = __import__(settings.BOT_HANDLERS_MODULE)

        if command == self.START_COMMAND:
            handler = bot_handlers_module.handlers.StartCommand()
        elif command == self.HELP_COMMAND:
            handler = bot_handlers_module.handlers.HelpCommand()
        elif command in bot_handlers_module.handlers.SUPPORTED_COMMANDS:
            handler = bot_handlers_module\
                .handlers\
                .SUPPORTED_COMMANDS[command]()
        else:
            # It is not a recognized command
            handler = None
        return handler


def bot_facade():
    return BotFacade.as_view()
