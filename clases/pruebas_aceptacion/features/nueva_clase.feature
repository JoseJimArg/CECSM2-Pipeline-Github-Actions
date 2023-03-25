Feature: Como administrador del sistema
                quiero agregar una nueva clase
                para definir la clase de una materia con su grupo y ciclo escolar.

    Scenario: Datos correctos
        Given que estoy dentro del sistema
        And me dirijo a la página "clases/nueva/"
        When selecciono un profesor
        And selecciono una materia
        And selecciono un grupo
        And selecciono un ciclo
        And pulso el botón de Guardar
        Then el sistema muestra el mensaje "Clase agregada correctamente"
        And cierro sesion en el sistema.

    Scenario: Clase existente
        Given que estoy dentro del sistema
        And me dirijo a la página "clases/nueva/"
        And ya está agregada una clase con los mismo datos
        When selecciono un profesor
        And selecciono una materia
        And selecciono un grupo
        And selecciono un ciclo
        And pulso el botón de Guardar
        Then el sistema muestra el mensaje de error "La clase ya está registrada."
        And cierro sesion en el sistema.