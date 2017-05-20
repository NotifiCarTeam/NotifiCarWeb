from django.contrib.auth.models import User
from behave import given


@given(u'The user "{username}" with the password "{password}"')
def create_user(context, username, password):
    User.objects.create_user(username=username, password=password)
