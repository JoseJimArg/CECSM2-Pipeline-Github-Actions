from selenium.webdriver.chrome.webdriver import WebDriver
from behave import when, then, given
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


@given(u'que hago login como administrador')
def step_impl(context):
    context.driver.find_element(By.ID, "id_username").send_keys("admin")
    context.driver.find_element(By.ID, "id_password").send_keys("admin")

@given(u'que presiono el botón de iniciar sesión')
def step_impl(context):
    context.driver.find_element(By.CLASS_NAME, "btn").click()
    time.sleep(2)

@given(u'registro los datos de un alumno')
def step_impl(context):
    context.driver.find_element(By.ID, "id_username").send_keys("corverin")
    context.driver.find_element(By.ID, "id_first_name").send_keys("Oscar")
    context.driver.find_element(By.ID, "id_last_name").send_keys("Corvera")
    context.driver.find_element(By.ID, "id_email").send_keys("oscar6rock@gmail.com")
    context.driver.find_element(By.ID, "id_password").send_keys("Corverita#1")
    context.driver.find_element(By.ID, "id_matricula").send_keys("35166869")

@given(u'registro los datos de un alumno cuya matricula ya está en uso por un docente')
def step_impl(context):
    context.driver.find_element(By.ID, "id_username").send_keys("corverin2")
    context.driver.find_element(By.ID, "id_first_name").send_keys("Oscar")
    context.driver.find_element(By.ID, "id_last_name").send_keys("Corvera")
    context.driver.find_element(By.ID, "id_email").send_keys("oscar6rock2@gmail.com")
    context.driver.find_element(By.ID, "id_password").send_keys("Corverita#1")
    context.driver.find_element(By.ID, "id_matricula").send_keys("35166861")

@when(u'presiono Guardar')
def step_impl(context):
    context.driver.find_element(By.CLASS_NAME, "btn").click()
    time.sleep(2)

@when(u'presiono el botón de iniciar sesión')
def step_impl(context):
    context.driver.find_element(By.CLASS_NAME, "btn").click()
    time.sleep(2)

@then(u'puedo ver una tabla con alumnos')
def step_impl(context):
    tabla = context.driver.find_element(By.TAG_NAME, "tbody").text
    assert "alumno" in tabla

@then(u'puedo ver al alumno "{alumno}" en la lista de alumnos')
def step_impl(context, alumno):
    tabla = context.driver.find_element(By.TAG_NAME, "tbody").text
    assert alumno in tabla

@then(u'puedo ver el mensaje de error "{mensaje}"')
def step_impl(context, mensaje):
    mensajes = context.driver.find_element(By.CLASS_NAME, "errorlist").text
    assert mensaje in mensajes