from behave import given, when, then
import time

@given(u'que me logueo en el sistema y me dirijo a la lista de grupos')
def step_impl(context):
    user_login(context)
    context.browser.get(f'{context.url}grupos')


@when(u'doy click en editar el grupo "{semestre}" "{letra}", le doy el valor de "{nuevo_semestre}" al semestre')
def step_impl(context, semestre, letra, nuevo_semestre):
    context.browser.find_element_by_id(f'editar-{semestre}{letra}').click()
    context.browser.find_element_by_id('id_semestre').send_keys(nuevo_semestre)


@then(u'doy click en guardar puedo ver el grupo "{grupo}" en la lista de grupos')
def step_impl(context, grupo):
    context.browser.find_element_by_id('submit_button').click()
    table = context.browser.find_element_by_tag_name('table')
    tbody = table.find_element_by_tag_name('tbody')
    assert grupo in tbody.text, f'Se esperaba {grupo}, se encontró {tbody.text}'


@then(u'doy click en guardar me redirige a la lista de grupos')
def step_impl(context):
    context.browser.find_element_by_id('submit_button').click()
    titulo = context.browser.find_element_by_tag_name('h1')
    assert 'Lista de grupos' in titulo.text, f'Se esperaba Lista de grupos, se encontró {titulo.text}'


def user_login(context):
    context.browser.get(f'{context.url}login')
    context.browser.find_element_by_id('id_username').send_keys('admin')
    context.browser.find_element_by_id('id_password').send_keys('admin')
    context.browser.find_element_by_id('login_button').click()
