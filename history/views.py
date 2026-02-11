from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import TimePeriod, HistoricalFigure, HistoricalSite
from .forms import HistoricalFigureForm


def home(request):
    """Home page with overview"""
    periods_count = TimePeriod.objects.count()
    figures_count = HistoricalFigure.objects.count()
    sites_count = HistoricalSite.objects.count()
    
    recent_figures = HistoricalFigure.objects.all().order_by('-created_at')[:3]
    featured_sites = HistoricalSite.objects.all()[:3]
    
    context = {
        'periods_count': periods_count,
        'figures_count': figures_count,
        'sites_count': sites_count,
        'recent_figures': recent_figures,
        'featured_sites': featured_sites,
    }
    return render(request, 'history/home.html', context)


# TIME PERIODS
def period_list(request):
    """List all time periods"""
    periods = TimePeriod.objects.all()
    return render(request, 'history/period_list.html', {'periods': periods})


def period_detail(request, pk):
    """Detail view for a specific period"""
    period = get_object_or_404(TimePeriod, pk=pk)
    figures = period.figures.all()
    sites = period.sites.all()
    context = {
        'period': period,
        'figures': figures,
        'sites': sites,
    }
    return render(request, 'history/period_detail.html', context)


# HISTORICAL FIGURES
def figure_list(request):
    """List all historical figures"""
    figures = HistoricalFigure.objects.all().select_related('time_period')
    return render(request, 'history/figure_list.html', {'figures': figures})


def figure_detail(request, pk):
    """Detail view for a specific figure"""
    figure = get_object_or_404(HistoricalFigure, pk=pk)
    related_sites = figure.sites.all()
    context = {
        'figure': figure,
        'related_sites': related_sites,
    }
    return render(request, 'history/figure_detail.html', context)


@login_required
def figure_create(request):
    """Create a new historical figure (CRUD - Create)"""
    if request.method == 'POST':
        form = HistoricalFigureForm(request.POST, request.FILES)
        if form.is_valid():
            figure = form.save(commit=False)
            figure.created_by = request.user
            figure.save()
            messages.success(request, 'Historical figure created successfully!')
            return redirect('history:figure_detail', pk=figure.pk)
    else:
        form = HistoricalFigureForm()
    return render(request, 'history/figure_form.html', {'form': form, 'title': 'Add New Figure'})


@login_required
def figure_edit(request, pk):
    """Edit existing figure (CRUD - Update)"""
    figure = get_object_or_404(HistoricalFigure, pk=pk)
    if request.method == 'POST':
        form = HistoricalFigureForm(request.POST, request.FILES, instance=figure)
        if form.is_valid():
            form.save()
            messages.success(request, 'Figure updated successfully!')
            return redirect('history:figure_detail', pk=figure.pk)
    else:
        form = HistoricalFigureForm(instance=figure)
    return render(request, 'history/figure_form.html', {'form': form, 'title': 'Edit Figure'})


@login_required
def figure_delete(request, pk):
    """Delete a figure (CRUD - Delete)"""
    figure = get_object_or_404(HistoricalFigure, pk=pk)
    if request.method == 'POST':
        figure.delete()
        messages.success(request, 'Figure deleted successfully!')
        return redirect('history:figure_list')
    return render(request, 'history/figure_confirm_delete.html', {'figure': figure})


# HISTORICAL SITES
def site_list(request):
    """List all historical sites"""
    sites = HistoricalSite.objects.all()
    return render(request, 'history/site_list.html', {'sites': sites})


def site_detail(request, pk):
    """Detail view for a specific site"""
    site = get_object_or_404(HistoricalSite, pk=pk)
    context = {
        'site': site,
        'time_periods': site.time_periods.all(),
        'related_figures': site.related_figures.all(),
    }
    return render(request, 'history/site_detail.html', context)


# AUTHENTICATION
def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('history:home')
    else:
        form = UserCreationForm()
    return render(request, 'history/register.html', {'form': form})


def user_login(request):
    """User login"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('history:home')
    else:
        form = AuthenticationForm()
    return render(request, 'history/login.html', {'form': form})


def user_logout(request):
    """User logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('history:home')


@login_required
def profile(request):
    """User profile page"""
    user_figures = HistoricalFigure.objects.filter(created_by=request.user)
    context = {
        'user_figures': user_figures,
    }
    return render(request, 'history/profile.html', context)