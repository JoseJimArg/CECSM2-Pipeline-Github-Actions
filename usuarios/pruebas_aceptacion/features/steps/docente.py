from selenium.webdriver.chrome.webdriver import WebDriver
from behave import when, then, given
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


@given(u'que ingreso al sistema con la dirección "{url}"')
def step_impl(context, url):
    context.url = url
    context.driver = webdriver.Chrome(executable_path=r'C:\chromedriver\chromedriver.exe')
    context.driver.maximize_window()


@given(u'que me dirijo a "{url}"')
def step_impl(context, url):
    context.driver.get(f"{context.url}{url}")

 
@given(u'que hago login como docente con los datos "{usuario}" y "{contra}"')
def step_impl(context, usuario, contra):
    context.driver.find_element_by_id('id_username').send_keys(usuario)
    time.sleep(1)
    context.driver.find_element_by_id('id_password').send_keys(contra)
    time.sleep(2)

@given(u'que hago login como admin con los datos "{usuario}" y "{contra}"')
def step_impl(context, usuario, contra):
    context.driver.find_element_by_id('id_username').send_keys(usuario)
    time.sleep(1)
    context.driver.find_element_by_id('id_password').send_keys(contra)
    time.sleep(2)

@given(u'presiono "Iniciar Sesión"')
def step_impl(context):
    context.driver.find_element_by_id('login_button').click()
    time.sleep(2)


@given(u'me voy al apartado de docentes')
def step_impl(context):
    context.driver.find_element_by_xpath('//*[@id="navbarDropdownMenuLink"]').click()
    time.sleep(1)
    context.driver.find_element_by_xpath('/html/body/nav/div/div/ul/li[1]/ul/li[2]/a').click()
    time.sleep(1)

@given(u'me voy al apartado de clases')
def step_impl(context):
    context.driver.find_element_by_xpath('//*[@id="navbarDropdownMenuLink2"]').click()
    time.sleep(2)


@given(u'selecciono mis clases')
def step_impl(context):
    context.driver.find_element_by_xpath('/html/body/nav/div/div/ul/li[2]/ul/li[1]/a').click()
    time.sleep(1)

@given(u'selecciono editar al "Docente4"')
def step_impl(context):
    context.driver.find_element_by_xpath('/html/body/div/div[2]/div/table/tbody/tr[4]/td[3]/a[2]').click()
    time.sleep(1)
    
@given(u'selecciono ver al "Docente4"')
def step_impl(context):
    context.driver.find_element_by_xpath('/html/body/div/div[2]/div/table/tbody/tr[4]/td[3]/a[1]').click()
    time.sleep(2)

@given(u'cambio su matricula por "{matricula}" y pongo su password en "{contra}"')
def step_impl(context, contra, matricula):
    context.driver.find_element_by_id('id_password').clear()
    time.sleep(1)
    context.driver.find_element_by_id('id_password').send_keys(contra)
    time.sleep(1)
    context.driver.find_element_by_id('id_matricula').clear()
    time.sleep(1)
    context.driver.find_element_by_id('id_matricula').send_keys(matricula)
    time.sleep(1)


@given(u'presiono guardar')
def step_impl(context):
    context.driver.find_element_by_id('submit_button').click()
    time.sleep(2)

@given(u'vuelvo a hacer login con "{usuario}" y "{contra}"')
def step_impl(context, usuario, contra):
    context.driver.find_element_by_id('id_username').send_keys(usuario)
    time.sleep(1)
    context.driver.find_element_by_id('id_password').send_keys(contra)
    time.sleep(1)
    context.driver.find_element_by_id('login_button').click()
    time.sleep(1)


@given(u'presiono "Identificarse"')
def step_impl(context):
    context.driver.find_element(
        By.XPATH, '//*[@id="login-form"]/div[3]/input').click()
    time.sleep(2)


@given(u'puedo ver el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    respuesta = context.driver.find_element_by_id('user-tools').text
    assert mensaje in respuesta, f"esperado es {mensaje} y obtenido es {respuesta}"


@given(u'presiono el botón "Nuevo"')
def step_impl(context):
    context.driver.find_element(By.XPATH, '//*[@id="contenedor"]/div[2]/div/div/form/button').click()


@given(u'capturo el usuario "{username}"')
def step_impl(context, username):
    context.driver.find_element(By.ID, "id_username").send_keys(username)


@given(u'capturo el nombre "{name}"')
def step_impl(context, name):
    context.driver.find_element(By.ID, "id_first_name").send_keys(name)


@given(u'capturo los apellidos "{apellidos}"')
def step_impl(context, apellidos):
    context.driver.find_element(By.ID, "id_last_name").send_keys(apellidos)


@given(u'capturo el correo "{email}"')
def step_impl(context, email):
    context.driver.find_element(By.ID, "id_email").send_keys(email)


@given(u'capturo la contraseña "{password}"')
def step_impl(context, password):
    context.driver.find_element(By.ID, "id_password").send_keys(password)


@given(u'capturo la matrícula "{matricula}"')
def step_impl(context, matricula):
    context.driver.find_element(By.ID, "id_matricula").send_keys(matricula)


@when(u'presiono el botón "Guardar"')
def step_impl(context):
    context.driver.find_element(By.XPATH, '//*[@id="formulario"]/button').click()
    time.sleep(1)


@then(u'puedo ver al usuario "{usuario}" en la lista de docentes')
def step_impl(context, usuario):
    lista_docentes = context.driver.find_element(
        By.TAG_NAME, 'tbody').text
    assert usuario in lista_docentes


@then(u'el sistema me muestra el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    lista_errores = context.driver.find_element(By.CLASS_NAME, "errorlist").text
    assert mensaje in lista_errores

@then(u'puedo ver al usuario "{nombre}"')
def step_impl(context, nombre):
    username_docente = context.driver.find_element_by_xpath('/html/body/h4[1]').text
    assert nombre in username_docente
    time.sleep(2)
    
@then(u'puedo ver las clases de "{nombre}"')
def step_impl(context, nombre):
    username_docente = context.driver.find_element_by_xpath('/html/body/div/div[1]/div/h1').text
    assert nombre in username_docente
    time.sleep(2)
