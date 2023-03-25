Feature: Alta grupo
                Como administrador 
                quiero agregar un nuevo grupo 
                para poder asignarlo a una clase
    
    Scenario: Creación de grupo correctamente
        Given que me logueo como administrador
        When voy a nuevo grupo, ingreso el semestre "6" y la letra "A", doy click en guardar
        Then puedo ver el mensaje "Grupo agregado correctamente"

    Scenario: Grupo ya existente
        Given que estoy logueado en el sistema
        When voy a nuevo grupo, ingreso el semestre "7" y la letra "A", doy click en guardar
        And regreso a nuevo grupo, ingreso otra vez el semestre "7" y la letra "A", doy click en guardar
        Then puedo ver el mensaje "No se pudo crear el grupo"