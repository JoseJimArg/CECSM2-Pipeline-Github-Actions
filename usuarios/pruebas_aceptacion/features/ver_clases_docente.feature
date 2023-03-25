Feature: Quiero poder ver las clases de un docente porque
    es importante saber que clases imparto yo como profesor

    Scenario: Ver clases del docente de manera corrrecta
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "login/"
        And que hago login como admin con los datos "Docente4" y "Nueva#12345"
        And presiono "Iniciar Sesión"
        And me voy al apartado de clases
        And selecciono mis clases
        Then puedo ver las clases de "Docente4"