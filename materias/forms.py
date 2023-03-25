from django import forms
from .models import Materia


class FormMateria(forms.ModelForm):
    class Meta:
        model = Materia

        fields = 'nombre', 'descripcion', 'tipo'

        widgets = {
            'nombre' : forms.TextInput(attrs={'class' : 'form-control', 'maxlength' : '60'}),
            'descripcion' : forms.Textarea(attrs={'class' : 'form-control', 'maxlength' : '350'}),
            'tipo' : forms.Select(attrs={'class' : 'form-select', 'required' : 'requierd'}),
        }


class FormMateriaEditar(forms.ModelForm):
    class Meta:
        model = Materia

        fields = 'descripcion', 'tipo'
