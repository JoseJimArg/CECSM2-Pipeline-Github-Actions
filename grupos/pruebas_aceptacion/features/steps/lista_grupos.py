from behave import given, when, then
import time


# Se necesita que el grupo no esté agragado
@given(u'que estoy logueado en el sistema y agrego el grupo "{semestre}" "{letra}"')
def step_impl(context, semestre, letra):
    user_login(context)
    context.browser.get(f'{context.url}grupos/nuevo')
    context.browser.find_element_by_id('id_semestre').send_keys(semestre)
    context.browser.find_element_by_id('id_letra').send_keys(letra)
    context.browser.find_element_by_id('submit_button').click()

@when(u'me dirio a la lista de grupos')
def step_impl(context):
    context.browser.get(f'{context.url}grupos')


@then(u'puedo ver el grupo "{semestre}" "{letra}" en la lista')
def step_impl(context, semestre, letra):
    table = context.browser.find_element_by_tag_name('table')
    tbody = table.find_element_by_tag_name('tbody')
    assert f'{semestre} {letra}' in tbody.text, f'se esperaba encontrar {semestre} {letra} y se encontro {tbody.text}'


def user_login(context):
    context.browser.get(f'{context.url}login')
    context.browser.find_element_by_id('id_username').send_keys('admin')
    context.browser.find_element_by_id('id_password').send_keys('admin')
    context.browser.find_element_by_id('login_button').click()