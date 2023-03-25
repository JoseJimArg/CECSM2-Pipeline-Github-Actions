Feature: Como administrador quiero añadir un nuevo alumno para registrarlo en el sistema.
    Scenario: Registro correcto
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "alumnos/nuevo/"
        And que hago login como administrador
        And que presiono el botón de iniciar sesión
        And registro los datos de un alumno
        When presiono Guardar
        Then puedo ver al alumno "Oscar" en la lista de alumnos
    Scenario: Matrícula repetida
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "alumnos/nuevo/"
        And que hago login como administrador
        And que presiono el botón de iniciar sesión
        And registro los datos de un alumno cuya matricula ya está en uso por un docente
        When presiono Guardar
        Then puedo ver el mensaje de error "La matrícula ya está en uso por un docente"
    