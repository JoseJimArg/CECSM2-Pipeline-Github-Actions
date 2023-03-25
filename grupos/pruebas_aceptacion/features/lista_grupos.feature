Feature: Como administrador 
            quiero ve los grupos que tengo 
            para saber cuales ya tengo
    
    Scenario: Visualizar grupos correctamente
        Given que estoy logueado en el sistema y agrego el grupo "8" "B"
        When me dirio a la lista de grupos
        Then puedo ver el grupo "8" "B" en la lista