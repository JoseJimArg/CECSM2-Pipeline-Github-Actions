Feature: Como profesor quiero cerrar sesión para cerrar el acceso a mi cuenta

    Scenario: Logout correcto
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "alumnos/"
        And que hago login como docente
        And que presiono el botón de iniciar sesión
        When presiono Cerrar sesión
        Then puedo ver la pantalla de login