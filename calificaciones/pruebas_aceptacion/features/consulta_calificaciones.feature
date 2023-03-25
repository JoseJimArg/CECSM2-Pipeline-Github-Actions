Feature: Como Alumno
                quiero poder consultar mis calificaciones
                para poder mantenerme al tanto de mi grade academico.

    Scenario: Visualizacion correcta
        Given que me dirijo a la página "calificaciones/consulta-calificaciones/"
        When ingreso la matricula "38192817"
        And pulso el botón "Consultar"
        Then el sistema muestra el mensaje "Calificaciones de " seguido del nombre del alumno encontrado

    Scenario: Matricula no registrada
        Given que me dirijo a la página "calificaciones/consulta-calificaciones/"
        When ingreso la matricula "30192817"
        And no corresponde a ningun alumno registrado
        And pulso el botón "Consultar"
        Then el sistema muestra el mensaje de error "Alumno no encontrado."