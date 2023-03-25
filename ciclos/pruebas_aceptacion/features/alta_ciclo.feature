Feature: Alta de ciclos escolares
    Como administrador 
    quiero crear un nuevo ciclo escolar 
    para poder asignarlo a una clase

    Scenario: Agregado correcto
        Given que estoy logueado en el sistema y me dirijo a la url de nuevo ciclo
        When ingreso el año de inicio "2022" y el año de fin "2023" y añado el tipo "non", doy click en guardar
        Then puedo ver un mensaje de "Ciclo escolar creado con éxito"

    Scenario: Algun dato incorrecto
        Given que estoy logueado en el sistema y me dirijo a la url de nuevo ciclo
        When ingreso el año de inicio "2021" y el año de fin "2023" y añado el tipo "non", doy click en guardar
        Then puedo ver un mensaje de "Algunos datos son incorrectos, no se pudo crear el ciclo escolar"
