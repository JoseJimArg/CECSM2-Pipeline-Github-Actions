from behave import given, when, then
import time
# from grupos.models import Semestre, Letra

# Debe estar agregado el semestre 2,3 y la letra A
# Debe haberse creado el usuario admin
# No debe de haber grupos registrados


@given(u'que me logueo como administrador')
def step_impl(context):
    # agregar_semestre_letras()
    user_login(context)


@when(u'voy a nuevo grupo, ingreso el semestre "{semestre}" y la letra "{letra}", doy click en guardar')
def step_impl(context, semestre, letra):
    context.browser.get(f'{context.url}grupos/nuevo')
    context.browser.find_element_by_id('id_semestre').send_keys(str(semestre))
    context.browser.find_element_by_id('id_letra').send_keys(str(letra))
    context.browser.find_element_by_id('submit_button').click()
    # time.sleep(2)


@then(u'puedo ver el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    div = context.browser.find_element_by_id('message_div')
    assert mensaje in div.text, f'Se esperaba {mensaje} y se encontró {div.text}'


@given(u'que estoy logueado en el sistema')
def step_impl(context):
    pass


@when(u'regreso a nuevo grupo, ingreso otra vez el semestre "{semestre}" y la letra "{letra}", doy click en guardar')
def step_impl(context, semestre, letra):
    context.browser.get(f'{context.url}grupos/nuevo')
    context.browser.find_element_by_id('id_semestre').send_keys(str(semestre))
    context.browser.find_element_by_id('id_letra').send_keys(str(letra))
    context.browser.find_element_by_id('submit_button').click()
    # time.sleep(2)

# def agregar_semestre_letras():
#     Semestre.objects.create(semestre=3)
#     Letra.objects.create(letra='A')


def user_login(context):
    context.browser.get(f'{context.url}login')
    context.browser.find_element_by_id('id_username').send_keys('admin')
    context.browser.find_element_by_id('id_password').send_keys('admin')
    context.browser.find_element_by_id('login_button').click()
