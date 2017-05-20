# flake8: noqa
from behave import then, when

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@when(u'I access the URL "{url}"')
def step_impl(context, url):
    context.driver.get(context.base_url + url)


@then(u'The browser URL should be "{url}"')
def step_impl(context, url):
    assert context.driver.current_url.endswith(url)


@when(u'I click in "{link}"')
def step_impl(context, link):
    context.driver.find_element_by_link_text(link).click()

@when(u'I click in "{link}" in modal')
def step_impl(context, link):
    WebDriverWait(context.driver, 10).until( \
        EC.visibility_of_element_located((By.LINK_TEXT, link)) \
    ).click()


@when(u'I click in "{button_id}" button')
def step_impl(context, button_id):
    context.driver.find_element_by_id(button_id).click()


@when(u'I click in "{button_id}" button in modal')
def step_impl(context, button_id):
    WebDriverWait(context.driver, 10).until( \
        EC.visibility_of_element_located((By.ID, button_id)) \
    ).click()


@when(u'I fill "{text}" in "{field_name}" field in modal')
def step_impl(context, text, field_name):
    field = WebDriverWait(context.driver, 10).until( \
        EC.visibility_of_element_located((By.NAME, field_name)) \
    )
    field.clear()
    field.send_keys(text)


@then(u'The field "{field_id}" should have an error')
def step_impl(context, field_id):
    field = context.driver.find_element_by_id(field_id)
    container = field.find_element_by_xpath('..')
    classes = container.get_attribute('class')
    assert 'has-error' in classes


@then(u'I should see "{content}" in "{element_id}"')
def step_impl(context, content, element_id):
    element = context.driver.find_element_by_id(element_id)
    assert (content in element.text) or \
           (content in element.get_attribute("value"))


@then(u'I should see "{content}" in page')
def step_impl(context, content):
    import re
    src = context.driver.page_source
    content_found = re.search(r'%s' % content, src)
    assert content_found is not None
