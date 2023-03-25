from behave import given, when, then
from selenium.webdriver.common.keys import Keys
import time


@given(u'que estoy logueado en el sistema')
def step_impl(context):
    user_login(context)


@given(u'agrego la materia "{materia}" con descripcion "{descripcion}"')
def step_impl(context, materia, descripcion):
    context.driver.get(f'{context.url}materias/agregar/')
    context.driver.find_element_by_id('id_nombre_input').send_keys(materia)
    context.driver.find_element_by_id('id_descripcion_input').send_keys(descripcion)
    context.driver.find_element_by_id('id_btn_guardar').click()
    


@given(u'agrego el docente "{nombre}" "{apellido}", username "{username}", password "{password}", email "{email}", matricula "{matricula}"')
def step_impl(context, nombre, apellido, username, password, email, matricula):
    context.driver.get(f'{context.url}docentes/nuevo/')
    context.driver.find_element_by_id('id_username').send_keys(username)
    context.driver.find_element_by_id('id_first_name').send_keys(nombre)
    context.driver.find_element_by_id('id_last_name').send_keys(apellido)
    context.driver.find_element_by_id('id_email').send_keys(email)
    context.driver.find_element_by_id('id_password').send_keys(password)
    context.driver.find_element_by_id('id_matricula').send_keys(matricula)
    context.driver.find_element_by_tag_name('html').send_keys(Keys.END)
    time.sleep(2)
    context.driver.find_element_by_id('submit_button').click()
    
@given(u'me dirijo a "{pagina}", selecciono asignar docentes a la materia "{materia}"')
def step_impl(context, pagina, materia):
    context.driver.get(f'{context.url}{pagina}')
    context.driver.find_element_by_id(f'relacionar_docente_{materia}').click()


@when(u'ingreso el nombre de la matricula "{matricula}", selecciono al resuldado de la busqueda "{nombre}"')
def step_impl(context, matricula, nombre):
    context.driver.find_element_by_id('matricula_input').send_keys(matricula)
    time.sleep(1)
    context.driver.find_element_by_class_name('autocomplete-result').click()


@when(u'pulso el botón Agregar')
def step_impl(context):
    context.driver.find_element_by_id('submit_button').click()


@then(u'puedo ve el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    div = context.driver.find_element_by_id('message_div')
    assert mensaje in div.text, f'Se esperaba {mensaje} y se encontró {div.text}'
    
    
# Segundo escenario

@given(u'escribo la "{matricula}" y no selecciono al docente de la lista')
def step_impl(context, matricula):
    context.driver.find_element_by_id('matricula_input').send_keys(matricula)


def user_login(context):
    context.driver.get(f'{context.url}login')
    context.driver.find_element_by_id('id_username').send_keys('admin')
    context.driver.find_element_by_id('id_password').send_keys('admin')
    context.driver.find_element_by_id('login_button').click()





