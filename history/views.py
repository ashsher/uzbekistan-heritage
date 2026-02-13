from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import TimePeriod, HistoricalFigure, HistoricalSite
from .forms import HistoricalFigureForm, TimePeriodForm, HistoricalSiteForm


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


# ============= TIME PERIODS =============
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


@login_required
def period_create(request):
    """Create a new time period"""
    if request.method == 'POST':
        form = TimePeriodForm(request.POST, request.FILES)
        if form.is_valid():
            period = form.save(commit=False)
            period.created_by = request.user
            period.save()
            messages.success(request, 'Time period created successfully!')
            return redirect('history:period_detail', pk=period.pk)
    else:
        form = TimePeriodForm()
    return render(request, 'history/period_form.html', {'form': form, 'title': 'Add New Time Period'})


@login_required
def period_edit(request, pk):
    """Edit existing time period"""
    period = get_object_or_404(TimePeriod, pk=pk)
    if request.method == 'POST':
        form = TimePeriodForm(request.POST, request.FILES, instance=period)
        if form.is_valid():
            form.save()
            messages.success(request, 'Time period updated successfully!')
            return redirect('history:period_detail', pk=period.pk)
    else:
        form = TimePeriodForm(instance=period)
    return render(request, 'history/period_form.html', {'form': form, 'title': 'Edit Time Period'})


@login_required
def period_delete(request, pk):
    """Delete a time period"""
    period = get_object_or_404(TimePeriod, pk=pk)
    if request.method == 'POST':
        period.delete()
        messages.success(request, 'Time period deleted successfully!')
        return redirect('history:period_list')
    return render(request, 'history/period_confirm_delete.html', {'period': period})


# ============= HISTORICAL FIGURES =============
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
    """Create a new historical figure"""
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
    return render(request, 'history/figure_form.html', {'form': form, 'title': 'Add New Historical Figure'})


@login_required
def figure_edit(request, pk):
    """Edit existing figure"""
    figure = get_object_or_404(HistoricalFigure, pk=pk)
    if request.method == 'POST':
        form = HistoricalFigureForm(request.POST, request.FILES, instance=figure)
        if form.is_valid():
            form.save()
            messages.success(request, 'Historical figure updated successfully!')
            return redirect('history:figure_detail', pk=figure.pk)
    else:
        form = HistoricalFigureForm(instance=figure)
    return render(request, 'history/figure_form.html', {'form': form, 'title': 'Edit Historical Figure'})


@login_required
def figure_delete(request, pk):
    """Delete a figure"""
    figure = get_object_or_404(HistoricalFigure, pk=pk)
    if request.method == 'POST':
        figure.delete()
        messages.success(request, 'Historical figure deleted successfully!')
        return redirect('history:figure_list')
    return render(request, 'history/figure_confirm_delete.html', {'figure': figure})


# ============= HISTORICAL SITES =============
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


@login_required
def site_create(request):
    """Create a new historical site"""
    if request.method == 'POST':
        form = HistoricalSiteForm(request.POST, request.FILES)
        if form.is_valid():
            site = form.save(commit=False)
            site.created_by = request.user
            site.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Historical site created successfully!')
            return redirect('history:site_detail', pk=site.pk)
    else:
        form = HistoricalSiteForm()
    return render(request, 'history/site_form.html', {'form': form, 'title': 'Add New Historical Site'})


@login_required
def site_edit(request, pk):
    """Edit existing site"""
    site = get_object_or_404(HistoricalSite, pk=pk)
    if request.method == 'POST':
        form = HistoricalSiteForm(request.POST, request.FILES, instance=site)
        if form.is_valid():
            form.save()
            messages.success(request, 'Historical site updated successfully!')
            return redirect('history:site_detail', pk=site.pk)
    else:
        form = HistoricalSiteForm(instance=site)
    return render(request, 'history/site_form.html', {'form': form, 'title': 'Edit Historical Site'})


@login_required
def site_delete(request, pk):
    """Delete a site"""
    site = get_object_or_404(HistoricalSite, pk=pk)
    if request.method == 'POST':
        site.delete()
        messages.success(request, 'Historical site deleted successfully!')
        return redirect('history:site_list')
    return render(request, 'history/site_confirm_delete.html', {'site': site})


# ============= AUTHENTICATION =============
def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
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
    messages.info(request, 'You have been logged out successfully.')
    return redirect('history:home')


@login_required
def profile(request):
    """Enhanced user profile page"""
    user_figures = HistoricalFigure.objects.filter(created_by=request.user).order_by('-created_at')
    user_periods = TimePeriod.objects.filter(created_by=request.user).order_by('-created_at')
    user_sites = HistoricalSite.objects.filter(created_by=request.user).order_by('-created_at')
    
    context = {
        'user_figures': user_figures,
        'user_periods': user_periods,
        'user_sites': user_sites,
        'total_contributions': user_figures.count() + user_periods.count() + user_sites.count(),
    }
    return render(request, 'history/profile.html', context)