from car import handlers

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from mock import patch

from model_mommy import mommy


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
        self.start_command.handle(chat_id, 'johndoe')

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
