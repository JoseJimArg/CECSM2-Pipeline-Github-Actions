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
    yield context.browser
    context.browser.quit()


def before_all(context):
    use_fixture(browser_chrome, context)
#     Semestre.objects.create(numero='2').save()
#     Semestre.objects.create(numero='3').save()
#     Letra.objects.create(letra='A').save()

# def after_all(context):
#     Semestre.objects.get(numero='2').delete()
#     Semestre.objects.get(numero='3').delete()
#     Letra.objects.get(letra='A').delete()
#     Grupo.objects.all().delete()