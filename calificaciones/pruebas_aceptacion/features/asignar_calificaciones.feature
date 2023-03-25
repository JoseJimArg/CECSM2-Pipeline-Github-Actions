Feature: Asignar Calificacion

    Como profesor
    quiero poder asignar las calificaciones de mis alumnos en la clase
    para poder reportarlas y que los alumnos las puedan consultar

    Scenario: Datos correctos
        Given que estoy logueado en el sistema como docente, me dirijo a mis clases
        And selecciono registrar calificaciones del "Primer Parcial" se la clase Redes
        And le ingreso una calificacion de "8.5" a "Rafael" "Medina"
        When doy click en registrar
        Then puedo ver el mensahe de "Se registraron 1 calificaciones"

    Scenario: No permite inputs vacios
        Given que estoy logueado en el sistema como docente, me dirijo a mis clases
        And selecciono registrar calificaciones del "Primer Parcial" se la clase Redes
        And le ingreso borro la calificacion a "Rafael" "Medina"
        When doy click en registrar
        Then puedo ver el mensahe de "Se registraron 0 calificaciones"