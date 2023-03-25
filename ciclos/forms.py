from django import forms
from .models import CicloEscolar
from django.core.exceptions import NON_FIELD_ERRORS


class CicloEscolarForm(forms.ModelForm):
    class Meta:
        model = CicloEscolar

        fields = 'anio_inicio', 'anio_fin', 'tipo_ciclo'

        widgets = {
            'anio_inicio': forms.NumberInput(attrs={'class': 'form-control'}),
            'anio_fin': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_ciclo': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'anio_inicio': 'Año de inicio',
            'anio_fin': 'Año de término',
            'tipo_ciclo': 'Tipo'
        }

        error_messages = {
            NON_FIELD_ERRORS: {'unique_together': 'El ciclo escolar ya existe'}

        }

    # Validaciones
    def clean(self):
        cleaned_data = super().clean()
        anio_inicio = cleaned_data.get('anio_inicio')
        anio_fin = cleaned_data.get('anio_fin')

        if anio_inicio > anio_fin:
            self.add_error(
                'anio_inicio', 'El año de inicio no puede ser mayor al año de fin')
        if anio_inicio == anio_fin:
            self.add_error(
                'anio_fin', 'El año de fin no puede ser igual al año de inicio')
        if anio_fin - anio_inicio > 1:
            self.add_error(
                'anio_fin', 'El ciclo escolar no puede durar más de un año')
