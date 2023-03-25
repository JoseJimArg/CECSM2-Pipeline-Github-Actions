Feature: Como administrador 
                quiero ver la lista de alumnos 
                para saber cuáles tengo registrados.
    Scenario: Scenario name: Hay alumnos registrados
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "alumnos/"
        And que hago login como administrador
        When presiono el botón de iniciar sesión
        Then puedo ver una tabla con alumnos