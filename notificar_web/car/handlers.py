""" Telegram Bot Handlers file

    This file must contain the command classes do handle the bot requests.

    There are two mandatory commands you MUST implement: StartCommand and HelpCommand.

    The other commands your bot may have, declare them on SUPPORTED_COMMANDS dict in the end of the file.

"""
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from telegram_bot.models import UserBotConversation
from telegram_bot.core import send_message, answer_callback_query, CommandHandler
from car.models import Car
from car import signals
import json


class StartCommand(CommandHandler):

    NUM_OF_ARGS = 1

    def handle(self, chat_id, username):
        print(username)
        try:
            user = User.objects.get(username=username)
            UserBotConversation.objects.update_or_create(user=user, chat=chat_id) # Save the user chat_id
            text = 'Hello %s, welcome to NotifiCar Bot!' % username
        except ObjectDoesNotExist:
            text = 'This user is not registered in NotifiCar.'

        message = {'chat_id': chat_id, 'text':  text}
        send_message(message)

    def missing_arguments_message(self):
        return "It seems that you forgot to tell us your username..."


class HelpCommand(CommandHandler):

    NUM_OF_ARGS = 0

    def handle(self, chat_id):
        pass

    def missing_arguments_message(self):
        pass

class MessageToCommand(CommandHandler):

    NUM_OF_ARGS = 2

    def handle(self, chat_id, plate, msg):
        print(plate)
        print(msg)

    def missing_arguments_message(self):
        return "Use message_to command like this:\n\n /message_to car_license_plate message_to_send"

class InformCommand(CommandHandler):

    NUM_OF_ARGS = 1

    OPTIONS = [
        ('Janela aberta', 1, 'A janela do seu carro está aberta.'),
        ('Farol ligado', 2, 'O farol do seu carro está ligado.'),
        ('Porta aberta', 3, 'Uma porta do seu carro esta aberta.'),
        ('Alguém estranho no seu carro', 4, 'Ei, tem alguém estranho rondando o seu carro.'),
        ('Mal estacionado', 5, 'Seu carro está mal estacionado e pode estar atrapalhando alguém a sair.'),
    ]

    def get_keyboard_options(self, car):
        options_keyboard = {'inline_keyboard': []}
        for option_text, option_data, option_msg in self.OPTIONS:
            callback_data = json.dumps({'car': car.pk, 'option': option_data, 'cmd': '/inform'})
            option = [{'text': option_text, 'callback_data': callback_data}]
            options_keyboard['inline_keyboard'].append(option)
        json_serialized_options = json.dumps(options_keyboard)

        return json_serialized_options

    def handle(self, chat_id, plate):
        try:
            car = Car.objects.get(license_plate=plate)
            msg = 'Choose a message to send to %s' % car.owner.username
            options_keyboard = self.get_keyboard_options(car)
            send_message({'chat_id': chat_id, 'text': msg, 'reply_markup': options_keyboard})
        except Car.DoesNotExist:
            exception_msg = 'No car with license plate %s found.' % plate
            send_message({'chat_id': chat_id, 'text': exception_msg})

    def handle_callback_query(self, query_id, car, option, cmd=False):
        found_car = Car.objects.get(pk=car)
        conversation = UserBotConversation.objects.get(user=found_car.owner)
        chat_id = conversation.chat

        msg = None
        for option_text, option_number, option_msg in self.OPTIONS:
            if option_number == option:
                msg = option_msg

        if msg is not None:
            send_message({'chat_id': chat_id, 'text': msg})
            confirmation_msg = 'User %s (owner of %s) has been notified!' % (found_car.owner.username, found_car.license_plate)
            answer_callback_query(query_id, confirmation_msg, True)

    def missing_arguments_message(self):
        return "Use inform command like this:\n\n /inform car_license_plate"

# Beyond the commons /help and /start
SUPPORTED_COMMANDS = {
    # Map here your command classes like this:
    # '/command': ClassToAnswerThisCommand

    '/inform': InformCommand,
    '/message_to': MessageToCommand,
}
