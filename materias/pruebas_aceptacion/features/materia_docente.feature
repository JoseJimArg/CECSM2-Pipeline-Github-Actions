Feature: Asignar docentes a la materia
    Como administrador 
    quiero relacionar un maestro con sus materias 
    para registrar cuales materias va a impartir.

    Scenario: Agregado correcto
        Given que estoy logueado en el sistema 
        And agrego la materia "Frameworks" con descripcion "Nueva materia"
        And agrego el docente "Juan" "Perez", username "juanperez", password "Juanperez.3", email "juan@gmail.com", matricula "12345555"
        And me dirijo a "materias/lista/", selecciono asignar docentes a la materia "Frameworks"
        When ingreso el nombre de la matricula "12345555", selecciono al resuldado de la busqueda "Juan Perez"
        And pulso el botón Agregar
        Then puedo ve el mensaje "Docente asignado correctamente"


    Scenario: No se selecciona de la lista
        Given que estoy logueado en el sistema 
        And me dirijo a "materias/lista/", selecciono asignar docentes a la materia "Frameworks"
        And escribo la "12345555" y no selecciono al docente de la lista
        When pulso el botón Agregar
        Then puedo ve el mensaje "No se selecionó docente de la lista"

# 2.- No se selecciona de la lista
# Dado que me dirijo a la página la lista de materia y selecciono asignar docente de la materia blockchain.
# Cuando me dirijo a la página de la lista de materias y selecciono asignar docente de la materia blockchain, le escribo la matrícula de Ruben y no selecciono al docente de la lista
# Entonces puedo ver un mensaje de error por no haber seleccionado el docente.