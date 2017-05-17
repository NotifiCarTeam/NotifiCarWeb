import json

from car import handlers
from car.models import Car

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from mock import patch

from model_mommy import mommy

from telegram_bot.models import UserBotConversation


class TestStartCommand:

    start_command = handlers.StartCommand()

    @patch('django.contrib.auth.models.User.objects.get')
    @patch('telegram_bot.models.UserBotConversation.objects.update_or_create')
    @patch('telegram_bot.core.BotRequest.send_message')
    def test_handle_with_user_found(self, send_message_mock,
                                    bot_conversation_mock, user_mock):
        username = 'johndoe'
        user = mommy.prepare(User, username=username)
        user_mock.return_value = user

        chat_id = 1
        self.start_command.handle(chat_id, username)

        user_mock.assert_called_with(username=username)
        bot_conversation_mock.assert_called_with(user=user, chat=chat_id)

        text = 'Hello %s, welcome to NotifiCar Bot!' % user.username
        message = {'chat_id': chat_id, 'text': text}
        send_message_mock.assert_called_with(message)

    @patch('django.contrib.auth.models.User.objects.get')
    @patch('telegram_bot.core.BotRequest.send_message')
    def test_handle_with_user_not_found(self, send_message_mock, user_mock):
        user_mock.side_effect = ObjectDoesNotExist()

        chat_id = 1
        username = 'unexisting_user'
        self.start_command.handle(chat_id, username)

        user_mock.assert_called_with(username=username)

        text = 'This user is not registered in NotifiCar.'
        message = {'chat_id': chat_id, 'text': text}
        send_message_mock.assert_called_with(message)

    def test_missing_args_msg(self):
        msg = self.start_command.missing_arguments_message()
        assert msg == "It seems that you forgot to tell us your username..."


class TestHelpCommand:

    help_command = handlers.HelpCommand()

    def test_handle(self):
        chat_id = 1
        self.help_command.handle(chat_id)
        pass

    def test_missing_args_msg(self):
        self.help_command.missing_arguments_message()
        pass


class TestMessageToCommand:

    msg_to_command = handlers.MessageToCommand()

    def test_handle(self):
        chat_id = 1
        plate = 'ABC1234'
        msg = 'Some message'
        self.msg_to_command.handle(chat_id, plate, msg)

    def test_missing_args_msg(self):
        msg = self.msg_to_command.missing_arguments_message()
        assert msg == "Use message_to command like this:\n\n \
                /message_to car_license_plate message_to_send"


class TestInformCommand:

    inform_command = handlers.InformCommand()

    @patch('car.handlers.InformCommand.get_keyboard_options')
    @patch('car.models.Car.objects.get')
    @patch('telegram_bot.core.BotRequest.send_message')
    def test_handle_with_car_found(self, send_message_mock,
                                   car_mock, options_mock):
        keyboard_options_mock = json.dumps({'foo': 'bar'})
        options_mock.return_value = keyboard_options_mock
        car = mommy.prepare(Car)
        car_mock.return_value = car

        chat_id = 1
        plate = 'ABC9876'
        self.inform_command.handle(chat_id, plate)

        car_mock.assert_called_with(license_plate=plate)
        options_mock.assert_called_with(car)

        text = 'Choose a message to send to %s' % car.owner.username
        message = {
            'chat_id': chat_id,
            'text': text,
            'reply_markup': keyboard_options_mock
        }
        send_message_mock.assert_called_with(message)

    @patch('car.models.Car.objects.get')
    @patch('telegram_bot.core.BotRequest.send_message')
    def test_handle_with_car_not_found(self, send_message_mock, car_mock):
        car_mock.side_effect = Car.DoesNotExist()

        chat_id = 1
        plate = 'ABC9876'
        self.inform_command.handle(chat_id, plate)

        car_mock.assert_called_with(license_plate=plate)

        text = 'No car with license plate %s found.' % plate
        message = {'chat_id': chat_id, 'text': text}
        send_message_mock.assert_called_with(message)

    @patch('telegram_bot.core.BotRequest.answer_callback_query')
    @patch('telegram_bot.models.UserBotConversation.objects.get')
    @patch('car.models.Car.objects.get')
    @patch('telegram_bot.core.BotRequest.send_message')
    def test_handle_callback_query(self, send_message_mock,
                                   car_mock, bot_conversation_mock,
                                   bot_callback_query_mock):
        car = mommy.prepare(Car)
        car_mock.return_value = car

        conversation = mommy.prepare(UserBotConversation)
        bot_conversation_mock.return_value = conversation

        chat_id = conversation.chat
        query_id = 1
        car_id = car.pk
        option = 1
        self.inform_command.handle_callback_query(
            query_id, car_id, option, cmd=False
        )

        car_mock.assert_called_with(pk=car_id)
        bot_conversation_mock.assert_called_with(user=car.owner)

        message = {
            'chat_id': chat_id,
            'text': handlers.InformCommand.OPTIONS[0][2]
        }
        send_message_mock.assert_called_with(message)

        confirmation_msg = 'User %s (owner of %s) has been notified!'\
            % (car.owner.username, car.license_plate)
        bot_callback_query_mock.assert_called_with(
            query_id, confirmation_msg, True
        )

    def test_missing_args_msg(self):
        msg = self.inform_command.missing_arguments_message()
        assert msg == ("Use inform command like this:\n\n" +
                       " /inform car_license_plate")

    def test_get_keyboard_options(self):
        car = mommy.prepare(Car, pk=1)
        options_dict = self.generate_keyboard_options_dict(car)
        options = self.inform_command.get_keyboard_options(car)
        options = json.loads(options)
        assert options_dict == options

    def generate_keyboard_options_dict(self, car):
        options_dict = {'inline_keyboard': []}
        for option_text, option_data, opt_msg in self.inform_command.OPTIONS:
            callback_data = json.dumps({
                'car': car.pk,
                'option': option_data,
                'cmd': '/inform'
            })
            option = [{'text': option_text, 'callback_data': callback_data}]
            options_dict['inline_keyboard'].append(option)
        return options_dict
