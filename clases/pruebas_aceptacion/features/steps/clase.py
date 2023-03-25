from selenium.webdriver.chrome.webdriver import WebDriver
from behave import when, then, given
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


@given(u'que ingreso al sistema con la dirección "{url}"')
def step_impl(context, url):
    context.url = url
    context.driver = webdriver.Chrome(executable_path=r'C:\chromedriver\chromedriver.exe')

@given(u'que me dirijo a "{url}"')
def step_impl(context, url):
    context.driver.get(f"{context.url}{url}")

@given(u'que hago login como administrador')
def step_impl(context):
    context.driver.find_element(By.ID, "id_username").send_keys("admin")
    context.driver.find_element(By.ID, "id_password").send_keys("admin")

@given(u'que presiono el botón de iniciar sesión')
def step_impl(context):
    context.driver.find_element(By.CLASS_NAME, "btn").click()
    time.sleep(2)

@given(u'que clickeo sobre "{btn}" en cualquier alumno')
def step_impl(context, btn):
    botones = context.driver.find_elements(By.CLASS_NAME, "btn")
    for boton in botones:
        if btn in boton.text:
            boton.click()
            break
    time.sleep(1)

@given(u'que busco "{materia}" en la barra de búsqueda')
def step_impl(context, materia):
    input_materias=context.driver.find_element(By.ID, "nombre_materia_input")
    input_materias.click()
    time.sleep(2)
    input_materias.send_keys(materia)
    time.sleep(2)


@given(u'clickeo encima de aquella con el ciclo "{ciclo}"')
def step_impl(context, ciclo):
    opciones=context.driver.find_elements(By.CLASS_NAME, "autocomplete-result-list")
    for opcion in opciones:
        if ciclo in opcion.text:
            opcion.click()
            break
    time.sleep(2)
    
@when(u'presiono el botón de iniciar sesión')
def step_impl(context):
    context.driver.find_element(By.CLASS_NAME, "btn").click()
    time.sleep(2)

@when(u'presiono "{btn}"')
def step_impl(context, btn):
    botones = context.driver.find_elements(By.CLASS_NAME, "btn")
    for boton in botones:
        if btn in boton.text:
            boton.click()
            break
    time.sleep(1)

@then(u'puedo ver una tabla con clases')
def step_impl(context):
    tabla = context.driver.find_element(By.TAG_NAME, "tbody").text
    assert "anatomia" in tabla

@then(u'el sistema me muestra el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    mensajes= context.driver.find_element(By.ID,"message_div").text
    assert mensaje in mensajes
    
# Steps for add a new Clase
@given(u'que estoy dentro del sistema')
def step_impl(context):
    login(context)
    
@given(u'me dirijo a la página "{url}"')
def step_impl(context, url):
    context.driver.get(context.url+url)
    time.sleep(1)
    
@when(u'pulso el botón de Guardar')
def step_impl(context):
    context.driver.find_element_by_id('submit_button').click()
    
@then(u'el sistema muestra el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    mensaje_mostrado = context.driver.find_element_by_xpath(
        '/html/body/div').text
    time.sleep(2)
    assert mensaje == mensaje_mostrado

@then(u'cierro sesion en el sistema.')
def step_impl(context):
    time.sleep(1)
    context.driver.find_element_by_xpath(
        '/html/body/nav/div/div/ul/li[4]/a').click()
    time.sleep(1)
    
@when(u'selecciono un profesor')
def step_impl(context):
    context.driver.find_element_by_xpath('/html/body/div/div[2]/div/form/p[1]/select/option[2]').click()

@when(u'selecciono una materia')
def step_impl(context):
    context.driver.find_element_by_xpath('/html/body/div/div[2]/div/form/p[2]/select/option[2]').click()

@when(u'selecciono un grupo')
def step_impl(context):
    context.driver.find_element_by_xpath('/html/body/div/div[2]/div/form/p[4]/select/option[2]').click()

@when(u'selecciono un ciclo')
def step_impl(context):
    context.driver.find_element_by_xpath('/html/body/div/div[2]/div/form/p[3]/select/option[2]').click()
    time.sleep(1)
    
@then(u'el sistema muestra el mensaje de error "{mensaje_error}"')
def step_impl(context, mensaje_error):
    time.sleep(1)
    mensaje_mostrado = context.driver.find_element_by_xpath(
        '/html/body/div/div[2]/div/form/ul/li').text
    time.sleep(1)
    assert mensaje_error == mensaje_mostrado
    
@given(u'ya está agregada una clase con los mismo datos')
def step_impl(context):
    pass
 
# Helpers to steps
def login(context):
    context.driver.get(context.url+'login/')
    time.sleep(1)
    context.driver.find_element_by_id('id_username').send_keys('admin')
    context.driver.find_element_by_id('id_password').send_keys('admin')
    context.driver.find_element_by_id('login_button').click()