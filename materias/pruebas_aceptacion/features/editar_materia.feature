Característica: Como administrador del sistema
                quiero editar una nueva materia
                para poder cambiar sus detalles.

    Escenario: Edición correcta
        Dado que estoy dentro del sistema
        Y me dirijo a la página "materias/editar/15"
        Cuando la descripcion "Estudio de las partes y funcionamiento del cuerpo humano y tambien el estudio de su composición."
        Y pulso el botón Guardar
        Entonces el sistema me muestra el mensaje "Materia editada correctamente."
        Y cierro sesion en el sistema.

    Escenario: Edición con descripcion vacia
        Dado que estoy dentro del sistema
        Y me dirijo a la página "materias/editar/15"
        Cuando dejo la descripción vacia
        Y pulso el botón Guardar
        Entonces el sistema me muestra el mensaje de error "Este campo es obligatorio."
        Y cierro sesion en el sistema.