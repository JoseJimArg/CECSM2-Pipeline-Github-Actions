Feature: Quiero poder ver una cuenta de docente porque
    es importante saber los datos de un usuario.

    Scenario: Ver docente de manera correcta
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "login/"
        And que hago login como admin con los datos "admin" y "admin"
        And presiono "Iniciar Sesión"
        And me voy al apartado de docentes
        And selecciono ver al "Docente4"
        Then puedo ver al usuario "Docente4"