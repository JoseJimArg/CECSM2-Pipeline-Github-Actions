Feature: Como administrador quiero crear una cuenta de docente porque este tiene funciones esenciales en el sistema.

    Scenario: Datos correctos
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "docentes/"
        And que hago login como admin
        And que presiono el botón de iniciar sesión
        And presiono el botón "Nuevo"
        And capturo el usuario "Docente6"
        And capturo el nombre "Oscar"
        And capturo los apellidos "Corvera Espinosa"
        And capturo el correo "oscar6rock6@gmail.com"
        And capturo la contraseña "Corverita#1"
        And capturo la matrícula "35166871"
        When presiono el botón "Guardar"
        Then puedo ver al usuario "Oscar Corvera Espinosa" en la lista de docentes

    Scenario: Matrícula repetida
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "docentes/"
        And que hago login como admin
        And que presiono el botón de iniciar sesión
        And presiono el botón "Nuevo"
        And capturo el usuario "Docente5"
        And capturo el nombre "Oscar"
        And capturo los apellidos "Corvera Espinosa"
        And capturo el correo "oscar6rock5@gmail.com"
        And capturo la contraseña "Corverita#1"
        And capturo la matrícula "35166870"
        When presiono el botón "Guardar"
        Then el sistema me muestra el mensaje "La matrícula ya está en uso por un alumno"


    
