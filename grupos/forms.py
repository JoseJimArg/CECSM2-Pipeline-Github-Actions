from django import forms
from .models import Grupo


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo

        fields = ('semestre', 'letra')

        widgets = {
            'semestre': forms.Select(attrs={'class': 'form-control'}),
            'letra': forms.Select(attrs={'class': 'form-control'}),
        }
