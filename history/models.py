from django.db import models
from django.contrib.auth.models import User


class TimePeriod(models.Model):
    """Represents historical periods like empires, khanates, eras"""
    name = models.CharField(max_length=200)
    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)  # null if ongoing
    description = models.TextField()
    image = models.ImageField(upload_to='periods/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_year']
    
    def __str__(self):
        return self.name


class HistoricalFigure(models.Model):
    """Represents important historical individuals"""
    ROLE_CHOICES = [
        ('ruler', 'Ruler/Khan'),
        ('scientist', 'Scientist/Scholar'),
        ('poet', 'Poet/Writer'),
        ('warrior', 'Military Leader'),
        ('architect', 'Architect/Builder'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)
    biography = models.TextField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='other')
    time_period = models.ForeignKey(TimePeriod, on_delete=models.CASCADE, related_name='figures')
    image = models.ImageField(upload_to='figures/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['birth_year']
    
    def __str__(self):
        return self.name


class HistoricalSite(models.Model):
    """Represents historical places and monuments"""
    CITY_CHOICES = [
        ('tashkent', 'Tashkent'),
        ('samarkand', 'Samarkand'),
        ('bukhara', 'Bukhara'),
        ('khiva', 'Khiva'),
        ('shahrisabz', 'Shahrisabz'),
        ('termez', 'Termez'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=20, choices=CITY_CHOICES)
    built_year = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    time_periods = models.ManyToManyField(TimePeriod, related_name='sites', blank=True)
    related_figures = models.ManyToManyField(HistoricalFigure, related_name='sites', blank=True)
    image = models.ImageField(upload_to='sites/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.city})"