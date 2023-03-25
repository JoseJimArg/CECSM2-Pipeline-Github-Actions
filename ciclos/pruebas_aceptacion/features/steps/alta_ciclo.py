from behave import given, when, then
import time
#Se nececita tener los tipos par y non ya agragados

@given(u'que estoy logueado en el sistema y me dirijo a la url de nuevo ciclo')
def step_impl(context):
    user_login(context)
    context.browser.get(f'{context.url}ciclos/nuevo')


@when(u'ingreso el año de inicio "{anio_inicio}" y el año de fin "{anio_fin}" y añado el tipo "{tipo}", doy click en guardar')
def step_impl(context, anio_inicio, anio_fin, tipo):
    context.browser.find_element_by_id('id_anio_inicio').send_keys(anio_inicio)
    context.browser.find_element_by_id('id_anio_fin').send_keys(anio_fin)
    context.browser.find_element_by_id('id_tipo_ciclo').send_keys(tipo)
    context.browser.find_element_by_id('submit_button').click()


@then(u'puedo ver un mensaje de "{mensaje}"')
def step_impl(context, mensaje):
    div = context.browser.find_element_by_id('message_div')
    assert mensaje in div.text, f'Se esperaba {mensaje} y se encontró {div.text}'


def user_login(context):
    context.browser.get(f'{context.url}login')
    context.browser.find_element_by_id('id_username').send_keys('admin')
    context.browser.find_element_by_id('id_password').send_keys('admin')
    context.browser.find_element_by_id('login_button').click()