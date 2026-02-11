from django.contrib import admin
from .models import TimePeriod, HistoricalFigure, HistoricalSite


@admin.register(TimePeriod)
class TimePeriodAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_year', 'end_year']
    search_fields = ['name', 'description']
    list_filter = ['start_year']


@admin.register(HistoricalFigure)
class HistoricalFigureAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'time_period', 'birth_year', 'death_year']
    search_fields = ['name', 'biography']
    list_filter = ['role', 'time_period']
    autocomplete_fields = ['time_period']


@admin.register(HistoricalSite)
class HistoricalSiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'built_year']
    search_fields = ['name', 'description']
    list_filter = ['city', 'time_periods']
    filter_horizontal = ['time_periods', 'related_figures']