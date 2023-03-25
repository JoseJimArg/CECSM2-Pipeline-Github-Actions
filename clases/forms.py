from django import forms
from django.core.exceptions import NON_FIELD_ERRORS


from .models import Clase


class FormClase(forms.ModelForm):
    class Meta:
        model = Clase

        fields = 'docente', 'materia', 'ciclo', 'grupo', 'cupo_total',

        widgets = {
            'docente': forms.Select(attrs={'class': 'form-control'}),
            'materia': forms.Select(attrs={'class': 'form-control'}),
            'ciclo': forms.Select(attrs={'class': 'form-control'}),
            'grupo': forms.Select(attrs={'class': 'form-control'}),
            'cupo_total': forms.NumberInput(attrs={'class': 'form-control', 'min' : '0'}),
        }

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'La clase ya está registrada.'}
        }
