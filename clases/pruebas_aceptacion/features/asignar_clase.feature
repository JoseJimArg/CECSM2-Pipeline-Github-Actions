Feature: Como administrador quiero asignar clases a un alumno para mantener un registro de las clases que cursa

    Scenario: Asignación correcta
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "alumnos/"
        And que hago login como administrador
        And que presiono el botón de iniciar sesión
        And que clickeo sobre "Asignar clases" en cualquier alumno
        And que busco "anatomia" en la barra de búsqueda
        And clickeo encima de aquella con el ciclo "2020-2021par"
        When presiono "Agregar"
        Then el sistema me muestra el mensaje "Se registró la materia anatomia"

    Scenario: Materia no seleccionada o no existente
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "alumnos/"
        And que hago login como administrador
        And que presiono el botón de iniciar sesión
        And que clickeo sobre "Asignar clases" en cualquier alumno
        When presiono "Agregar"
        Then el sistema me muestra el mensaje "No se seleccionó una clase de la lista."