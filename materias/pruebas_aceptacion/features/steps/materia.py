from behave import when, then, given
import time


@given(u'que estoy dentro del sistema')
def step_impl(context):
    login(context)


@given(u'me dirijo a la página "{url}"')
def step_impl(context, url):
    context.driver.get(context.url+url)
    time.sleep(1)


@when(u'ingreso el nombre de la materia "{nombre}"')
def step_impl(context, nombre):
    context.driver.find_element_by_id('id_nombre_input').send_keys(nombre)
    time.sleep(1)


@when(u'la descripcion "{descripcion}"')
def step_impl(context, descripcion):
    context.driver.find_element_by_id(
        'id_descripcion_input').send_keys(descripcion)
    time.sleep(1)


@when(u'pulso el botón Guardar')
def step_impl(context):
    context.driver.find_element_by_id('id_btn_guardar').click()


@then(u'el sistema me muestra el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    mensaje_mostrado = context.driver.find_element_by_xpath(
        '/html/body/div').text
    time.sleep(1)
    assert mensaje == mensaje_mostrado


@then(u'el sistema me muestra el mensaje de error "{mensaje_error}"')
def step_impl(context, mensaje_error):
    time.sleep(1)
    mensaje_mostrado = context.driver.find_element_by_xpath(
        '/html/body/div/div[2]/div/form/ul/li/ul/li').text
    time.sleep(1)
    assert mensaje_error == mensaje_mostrado


@when(u'ingreso el nombre de la materia vacio')
def step_impl(context):
    pass


@when(u'la descripcion la dejo vacía')
def step_impl(context):
    pass


@given(u'ya existe una materia llamada "{nombre}"')
def step_impl(context, nombre):
    context.driver.find_element_by_id('id_nombre_input').send_keys(nombre)
    context.driver.find_element_by_id('id_descripcion_input').send_keys(
        "Descripcion privisional diferente.")
    time.sleep(1)
    context.driver.find_element_by_id('id_btn_guardar').click()
    time.sleep(1)
    context.driver.get(context.url+"materias/agregar/")


@then(u'cierro sesion en el sistema.')
def step_impl(context):
    time.sleep(1)
    context.driver.find_element_by_xpath(
        '/html/body/nav/div/div/ul/li[4]/a').click()
    time.sleep(1)


def login(context):
    context.driver.get(context.url+'login/')
    time.sleep(1)
    context.driver.find_element_by_id('id_username').send_keys('admin')
    context.driver.find_element_by_id('id_password').send_keys('admin')
    context.driver.find_element_by_id('login_button').click()

# Steps for editar materia Scenario

@when(u'dejo la descripción vacia')
def step_impl(context):
    input = context.driver.find_element_by_id(
        'id_descripcion_input')
    input.clear()
    
# Steps for have a list of materia
@when(u'me dirijo a la página "{url}"')
def step_impl(context, url):
    context.driver.get(context.url+url)
    time.sleep(1)


@then(u'puedo ver la lista de materias con su nombre y acciones que puedo hacer con ellas')
def step_impl(context):
    materia_text = context.driver.find_element_by_xpath('/html/body/div/div[2]/div/table/thead/tr/th[1]').text
    accciones_text = context.driver.find_element_by_xpath('/html/body/div/div[2]/div/table/thead/tr/th[2]').text
    assert materia_text == "Materia" and accciones_text == "Acciones"
    time.sleep(1)
