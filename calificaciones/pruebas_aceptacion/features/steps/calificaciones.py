from behave import given, when, then
import time

# necesita tener el docente Armando villalobos
# La materia Redes
# Tener asignada esa materia al docente
# tener el grupo 5 C
# Tener el ciclo escolar 2021-2022par
# tener la clase redes 2021-2022par en 5 C con el docente Armando
# Solo tenerle asignada esa clase al docente
# tener creado el alumno Rafael Medina
# Asignarle la clase al alumno
# No tener calificacion para primer parcial para el alumno


@given(u'que estoy logueado en el sistema como docente, me dirijo a mis clases')
def step_impl(context):
    user_login(context)
    context.browser.get(f'{context.url}docentes/ver-clases/')


@given(u'selecciono registrar calificaciones del "{parcial}" se la clase Redes')
def step_impl(context, parcial):
    context.browser.find_element_by_link_text(parcial).click()


@given(u'le ingreso una calificacion de "{calificacion}" a "{nombre}" "{apellido}"')
def step_impl(context, nombre, apellido, calificacion):
    input = context.browser.find_element_by_id(f'{nombre}{apellido}')
    input.send_keys(calificacion)


@when(u'doy click en registrar')
def step_impl(context):
    context.browser.find_element_by_id('submit_button').click()


@then(u'puedo ver el mensahe de "{mensaje}"')
def step_impl(context, mensaje):
    div = context.browser.find_element_by_id('message_div')
    assert mensaje in div.text, f'Se esperaba {mensaje} y se encontró {div.text}'


@given(u'le ingreso borro la calificacion a "{nombre}" "{apellido}"')
def step_impl(context, nombre, apellido):
    input = context.browser.find_element_by_id(f'{nombre}{apellido}')
    input.clear()


# Editar

@given(u'le cambio la calificacion a "{calificacion}" a "{nombre}" "{apellido}"')
def step_impl(context, calificacion, nombre, apellido):
    input = context.browser.find_element_by_id(f'{nombre}{apellido}')
    input.clear()
    input.send_keys(calificacion)


def user_login(context):
    context.browser.get(f'{context.url}login')
    context.browser.find_element_by_id('id_username').send_keys('armandoV')
    context.browser.find_element_by_id('id_password').send_keys('Armando.1')
    context.browser.find_element_by_id('login_button').click()

# Consultar
@given(u'que me dirijo a la página "{url}"')
def step_impl(context, url):
    context.browser.get(context.url+url)
    time.sleep(1)

@when(u'ingreso la matricula "{matricula}"')
def step_impl(context, matricula):
    context.browser.find_element_by_id('id_matricula_alumno').send_keys(matricula)
    time.sleep(1)

@when(u'pulso el botón "Consultar"')
def step_impl(context):
    context.browser.find_element_by_id('id_btn_guardar').click()
    time.sleep(1)

@then(u'el sistema muestra el mensaje "{mensaje}" seguido del nombre del alumno encontrado')
def step_impl(context, mensaje):
    menssage_returned = context.browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/h3').text
    time.sleep(1)
    assert mensaje in menssage_returned
    
@when(u'no corresponde a ningun alumno registrado')
def step_impl(context):
    pass


@then(u'el sistema muestra el mensaje de error "{mensaje_error}"')
def step_impl(context, mensaje_error):
    time.sleep(1)
    mensaje_mostrado = context.browser.find_element_by_xpath(
        '/html/body/div[1]/div').text
    time.sleep(1)
    assert mensaje_error == mensaje_mostrado