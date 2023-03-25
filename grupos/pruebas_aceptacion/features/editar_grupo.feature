Feature: Como administrador
            quiero editar un grupo
            para modificar sus detalles

    Scenario: Editar satisfactoriamente
        Given que me logueo en el sistema y me dirijo a la lista de grupos
        When doy click en editar el grupo "7" "A", le doy el valor de "4" al semestre
        Then doy click en guardar puedo ver el grupo "4 A" en la lista de grupos

    Scenario: redireccion a la lista de grupos
        Given que me logueo en el sistema y me dirijo a la lista de grupos
        When doy click en editar el grupo "4" "A", le doy el valor de "8" al semestre
        Then doy click en guardar me redirige a la lista de grupos