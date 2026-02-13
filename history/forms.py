from django import forms
from .models import HistoricalFigure, TimePeriod, HistoricalSite


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


class TimePeriodForm(forms.ModelForm):
    class Meta:
        model = TimePeriod
        fields = ['name', 'start_year', 'end_year', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Timurid Empire'}),
            'start_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1370'}),
            'end_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1507 (leave blank if ongoing)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe this period...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class HistoricalSiteForm(forms.ModelForm):
    class Meta:
        model = HistoricalSite
        fields = ['name', 'city', 'built_year', 'description', 'time_periods', 'related_figures', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Registan Square'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'built_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1420'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe this site...'}),
            'time_periods': forms.CheckboxSelectMultiple(),
            'related_figures': forms.CheckboxSelectMultiple(),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }