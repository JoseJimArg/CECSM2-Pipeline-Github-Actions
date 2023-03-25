Característica: Como administrador del sistema
                quiero agregar una nueva materia
                para poder relacionarla con un maestro y un grupo.

    Escenario: Datos correctos
        Dado que estoy dentro del sistema
        Y me dirijo a la página "materias/agregar/"
        Cuando ingreso el nombre de la materia "Anatomia1"
        Y la descripcion "Estudio de las partes y funcionamiento del cuerpo humano1"
        Y pulso el botón Guardar
        Entonces el sistema me muestra el mensaje "Materia agregada correctamente"
        Y cierro sesion en el sistema.

    Escenario: Nombre muy largo
        Dado que estoy dentro del sistema
        Y me dirijo a la página "materias/agregar/"
        Cuando ingreso el nombre de la materia "asdasdasdasdasdasdasdasdasdaasdasdasdasdasdasdasdaasdasdasdasdasdasdasdasdasdaasdasdasdasdasdasdasdaasdasdasdasdasdasdasdasdasdaasdasdasdasdasdasdasdaasdasdasdasdasdasdasdasdasdaasdasdasdasdasdasdasda"
        Y la descripcion "Estudio de las partes y funcionamiento del cuerpo humano2"
        Y pulso el botón Guardar
        Entonces el sistema me muestra el mensaje de error "Asegúrese de que este valor tenga como máximo 60 caracteres (tiene 200)."
        Y cierro sesion en el sistema.

    Escenario: Sin nombre
        Dado que estoy dentro del sistema
        Y me dirijo a la página "materias/agregar/"
        Cuando ingreso el nombre de la materia vacio
        Y la descripcion "Estudio de las partes y funcionamiento del cuerpo humano3"
        Y pulso el botón Guardar
        Entonces el sistema me muestra el mensaje de error "Este campo es obligatorio."
        Y cierro sesion en el sistema.

    Escenario: Sin descripcion 
        Dado que estoy dentro del sistema
        Y me dirijo a la página "materias/agregar/"
        Cuando ingreso el nombre de la materia "Anatomia4"
        Y la descripcion la dejo vacía
        Y pulso el botón Guardar
        Entonces el sistema me muestra el mensaje de error "Este campo es obligatorio."
        Y cierro sesion en el sistema.

    Escenario: Nombre existente
        Dado que estoy dentro del sistema
        Y me dirijo a la página "materias/agregar/"
        Y ya existe una materia llamada "Anatomia5"
        Cuando ingreso el nombre de la materia "Anatomia5"
        Y la descripcion "Estudio de las partes y funcionamiento del cuerpo humano5"
        Y pulso el botón Guardar
        Entonces el sistema me muestra el mensaje de error "Ya existe un/a Materia con este/a Nombre."
        Y cierro sesion en el sistema.
