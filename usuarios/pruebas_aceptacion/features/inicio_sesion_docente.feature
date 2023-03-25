Feature: Como profesor quiero iniciar sesión para administrar mis grupos.

    Scenario: Inicio de sesión correcto
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "login/"
        And que hago login como docente
        When presiono "Iniciar Sesión"
        Then El sistema me redirige a la pantalla de lista de grupos.

    Scenario: Inicio de sesión incorrecto
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "login/"
        And que hago login como docente con credenciales erróneas
        When presiono "Iniciar Sesión"
        Then El sistema me indica con un mensaje "Nombre de usuario o contraseña incorrectos."