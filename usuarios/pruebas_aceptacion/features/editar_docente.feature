Feature: Quiero poder editar una cuenta de docente porque este 
            tiene funciones esenciales en el sistema.

    Scenario: Editar docente con datos correctos
        Given que ingreso al sistema con la dirección "http:\\192.168.33.10:8000/"
        And que me dirijo a "login/"
        And que hago login como docente con los datos "Docente4" y "Nuevo#123"
        And presiono "Iniciar Sesión"
        And me voy al apartado de docentes
        And selecciono editar al "Docente4"
        And cambio su matricula por "35000010" y pongo su password en "Nueva#12345"
        And presiono guardar
        And vuelvo a hacer login con "Docente4" y "Nueva#12345"
        Then puedo ver al usuario "Docente4" en la lista de docentes