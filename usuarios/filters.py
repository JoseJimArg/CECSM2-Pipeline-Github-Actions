import django_filters
from django import forms
from .models import Aspirante

STATUS_CHOICES = (
    (0, 'Pendientes'),
    (1, 'Aceptados'),
    (2, 'Rechazados'),
)

class AspiranteFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=STATUS_CHOICES, 
        empty_label=None, 
        label="Estatus", 
        widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )

    class Meta:
        model = Aspirante
        fields = ['status']
        