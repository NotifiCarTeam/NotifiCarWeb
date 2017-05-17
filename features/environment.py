from selenium import webdriver


def before_feature(context, feature):
    context.driver = webdriver.PhantomJS(
        executable_path="node_modules/phantomjs/bin/phantomjs"
    )
    context.driver.set_window_size(1000, 600)
    context.driver.implicitly_wait(5)


def after_feature(context, feature):
    context.driver.quit()
