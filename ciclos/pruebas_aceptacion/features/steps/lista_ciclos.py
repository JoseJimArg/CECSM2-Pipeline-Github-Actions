from behave import given, when, then


@given(u'que me logueo en el sistema')
def step_impl(context):
    user_login(context)


@when(u'me dirijo a la direccion "{pagina}"')
def step_impl(context, pagina):
    context.browser.get(f'{context.url}{pagina}')


@then(u'puedo ver la lista de ciclos escolares')
def step_impl(context):
    head_table = context.browser.find_element_by_tag_name('thead')
    assert 'Nombre' in head_table.text
    assert 'Inicio' in head_table.text
    assert 'Fin' in head_table.text
    assert 'Tipo' in head_table.text


def user_login(context):
    context.browser.get(f'{context.url}login')
    context.browser.find_element_by_id('id_username').send_keys('admin')
    context.browser.find_element_by_id('id_password').send_keys('admin')
    context.browser.find_element_by_id('login_button').click()