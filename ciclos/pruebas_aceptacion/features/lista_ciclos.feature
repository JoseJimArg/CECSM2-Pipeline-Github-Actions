Feature: Lista de ciclos escolares

    Como administrador 
    quiero ver una lista de los ciclos escolares 
    para saber cuales están registrados en el sistema

    Scenario: Visualizacion correcta
        Given que me logueo en el sistema
        When me dirijo a la direccion "ciclos/nuevo"
        Then puedo ver la lista de ciclos escolares