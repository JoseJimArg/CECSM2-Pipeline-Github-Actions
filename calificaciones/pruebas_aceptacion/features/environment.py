from behave import fixture, use_fixture
from selenium.webdriver import Chrome
from unittest import TestCase

# No pude importar los modelos
# from grupos.models import Semestre, Letra, Grupo


@fixture
def browser_chrome(context):
    context.browser = Chrome()
    context.url = 'http://192.168.33.10:8000/'
    context.test = TestCase()
    # yield context.browser
    # context.browser.quit()


def before_all(context):
    use_fixture(browser_chrome, context)

# def after_all(context):
