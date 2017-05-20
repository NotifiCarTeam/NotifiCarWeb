[![Build Status](https://travis-ci.org/NotifiCarTeam/NotifiCarWeb.svg?branch=master)](https://travis-ci.org/NotifiCarTeam/NotifiCarWeb)

[![codecov](https://codecov.io/gh/NotifiCarTeam/NotificarWeb/branch/master/graph/badge.svg)](https://codecov.io/gh/NotifiCarTeam/NotificarWeb)

# NotifiCar Web

The NotifiCar is an application that provides a way for drivers to communicate with each other by their cars plate numbers.

This is the web application of the NotifiCar that provides the means to user registration to NotifiCar.

The most insteresting characteristic of NotifiCar is it's integration with Telegram by a bot ([@NotificarBot](https://telegram.me/NotifiCarBot) ), that provides a mobile solution through Telegram to the application.
In this Telegram bot, people can notify drivers about things going on in their cars.

The current version of NotifiCar is running in PythonAnywhere under [http://italopaiva.pythonanywhere.com](http://italopaiva.pythonanywhere.com).

# Running the NotifiCar

NotifiCar was build in Django, so you'll need python and pip to proceed.
Follow these steps to run the NotifiCar:

1. Clone the repository and navigate to it

`$ git clone https://github.com/NotifiCarTeam/NotifiCarWeb.git && cd NotificarWeb`

2. Install the requirements
  
`$ pip install -r requirements.txt`

3. Run the migrations

`$ ./manage.py migrate`

4. Run the server

`$ ./manage.py runserver`

# Running NotifiCar tests

NotifiCar is shipped with _tox_, so just run tox to run the test suite:

`$ tox`

OBS.: You'll need _nodejs_ to run the acceptance tests on _PhantomJS_, so install _node_ first.

## Running only unit tests

NotifiCar unit tests relies on _pytest_, so just run it:

`$ pytest --cov=.`

## Running only acceptance tests

Remembering that the acceptance tests will need _PhantomJS_ in order to be able to run, so install _nodejs_ and run `$ npm install` before running the tests.

NotifiCar uses _behave_ and _selenium_ to run acceptance tests, so just run:

`$ ./manage.py behave`
