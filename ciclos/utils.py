from .models import CicloEscolar


def desactivar_ciclo_activo():
    ciclo_desactivar = CicloEscolar.objects.filter( activo = True ).first()
    if ciclo_desactivar:
        ciclo_desactivar.update_active(False)