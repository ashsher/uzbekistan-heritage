from django import forms
from .models import HistoricalFigure


class HistoricalFigureForm(forms.ModelForm):
    class Meta:
        model = HistoricalFigure
        fields = ['name', 'birth_year', 'death_year', 'biography', 'role', 'time_period', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'birth_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1336'}),
            'death_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1405'}),
            'biography': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write biography...'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'time_period': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }