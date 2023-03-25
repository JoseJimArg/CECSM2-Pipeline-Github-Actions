Feature: Editar Calificacion

    Como profesor
    quiero poder editar las calificaciones de mis clases
    porque puede que yo me equivocara al evaluar

    Scenario: Datos correctos
        Given que estoy logueado en el sistema como docente, me dirijo a mis clases
        And selecciono registrar calificaciones del "Primer Parcial" se la clase Redes
        And le cambio la calificacion a "9.5" a "Rafael" "Medina"
        When doy click en registrar
        Then puedo ver el mensahe de "Se registraron 1 calificaciones"

    Scenario: No permite inputs vacios
        Given que estoy logueado en el sistema como docente, me dirijo a mis clases
        And selecciono registrar calificaciones del "Primer Parcial" se la clase Redes
        And le ingreso borro la calificacion a "Rafael" "Medina"
        When doy click en registrar
        Then puedo ver el mensahe de "Se registraron 0 calificaciones"