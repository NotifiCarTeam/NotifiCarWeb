from django.contrib.auth.models import User
from behave import given, then


@given(u'The user "{username}" with the password "{password}"')
def create_user(context, username, password):
    User.objects.create_user(username=username, password=password)


@then(u'The user "{username}" should be registered')
def get_user(context, username):
    try:
        user = User.objects.get(username=username)
        assert user.username == username
    except User.DoesNotExist:
        assert False
