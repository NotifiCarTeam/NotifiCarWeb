from behave import then, when

# from selenium.webdriver.common.keys import Keys


@when(u'I access the URL "{url}"')
def access_url_impl(context, url):
    context.driver.get(context.base_url + "/")


@then(u'The browser URL should be "{url}"')
def url_should_be_impl(context, url):
    assert context.driver.current_url.endswith(url)
