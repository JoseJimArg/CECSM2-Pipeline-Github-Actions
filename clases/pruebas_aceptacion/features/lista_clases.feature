Feature: Como administrador quiero ver todas las clases en el sistema para saber cuales tengo registradas

    Scenario: Hay clases registradas
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "clases/"
        And que hago login como administrador
        When presiono el botón de iniciar sesión
        Then puedo ver una tabla con clases