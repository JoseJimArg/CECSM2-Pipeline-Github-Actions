from selenium.webdriver.chrome.webdriver import WebDriver
from behave import when, then, given
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

@when(u'presiono "Iniciar Sesión"')
def step_impl(context):
    context.driver.find_element(By.CLASS_NAME,"btn").click()

@then(u'El sistema me redirige a la pantalla de lista de grupos.')
def step_impl(context):
    url=context.driver.current_url
    assert "http://192.168.33.10:8000/grupos/" in url

@then(u'El sistema me indica con un mensaje "{mensaje}"')
def step_impl(context,mensaje):
    error=context.driver.find_element(By.CLASS_NAME,"alert").text
    assert mensaje in error

@given(u'que hago login como admin')
def step_impl(context):
    context.driver.find_element(By.ID,'id_username').send_keys("admin")
    context.driver.find_element(By.ID,'id_password').send_keys("admin")

@given(u'que hago login como admin con credenciales erróneas')
def step_impl(context):
    context.driver.find_element(By.ID,'id_username').send_keys("admin")
    context.driver.find_element(By.ID,'id_password').send_keys("admin2")

@given(u'que hago login como docente')
def step_impl(context):
    context.driver.find_element(By.ID,'id_username').send_keys("docente")
    context.driver.find_element(By.ID,'id_password').send_keys("Docente#1")

@given(u'que hago login como docente con credenciales erróneas')
def step_impl(context):
    context.driver.find_element(By.ID,'id_username').send_keys("docente")
    context.driver.find_element(By.ID,'id_password').send_keys("docente")

@when(u"presiono Cerrar sesión")
def step_impl(context):
    link= context.driver.find_element(By.XPATH, '//*[@id="navbarNavDropdown"]/ul/li[4]/a').click()
    time.sleep(2)


@then(u'puedo ver la pantalla de login')
def step_impl(context):
    campo_username=context.driver.find_element(By.ID,"id_username")
    campo_password=context.driver.find_element(By.ID,"id_password")
    assert campo_username is not None and campo_password is not None