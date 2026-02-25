from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import TimePeriod, HistoricalFigure, HistoricalSite


class ModelTests(TestCase):
    """Test database models"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.period = TimePeriod.objects.create(
            name='Test Period',
            start_year=1500,
            end_year=1600,
            description='Test description',
            created_by=self.user
        )
    
    def test_time_period_creation(self):
        """Test TimePeriod model"""
        self.assertEqual(self.period.name, 'Test Period')
        self.assertEqual(str(self.period), 'Test Period')
    
    def test_historical_figure_creation(self):
        """Test HistoricalFigure model"""
        figure = HistoricalFigure.objects.create(
            name='Test Figure',
            birth_year=1500,
            death_year=1550,
            biography='Test bio',
            role='ruler',
            time_period=self.period,
            created_by=self.user
        )
        self.assertEqual(figure.name, 'Test Figure')
        self.assertEqual(figure.time_period, self.period)
    
    def test_historical_site_creation(self):
        """Test HistoricalSite model"""
        site = HistoricalSite.objects.create(
            name='Test Site',
            city='tashkent',
            built_year=1550,
            description='Test site description',
            created_by=self.user
        )
        self.assertEqual(site.name, 'Test Site')
        self.assertEqual(site.city, 'tashkent')


class ViewTests(TestCase):
    """Test views"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.period = TimePeriod.objects.create(
            name='Test Period',
            start_year=1500,
            description='Test'
        )
    
    def test_home_page(self):
        """Test home page loads"""
        response = self.client.get(reverse('history:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Uzbekistan Heritage')
    
    def test_period_list(self):
        """Test period list page"""
        response = self.client.get(reverse('history:period_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_figure_list(self):
        """Test figure list page"""
        response = self.client.get(reverse('history:figure_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_site_list(self):
        """Test site list page"""
        response = self.client.get(reverse('history:site_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_required_for_create(self):
        """Test login required for creating entries"""
        response = self.client.get(reverse('history:figure_create'))
        self.assertEqual(response.status_code, 302)  # Redirects to login


class AuthenticationTests(TestCase):
    """Test authentication"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_user_registration(self):
        """Test user can register"""
        response = self.client.post(reverse('history:register'), {
            'username': 'newuser',
            'password1': 'testpass12345',
            'password2': 'testpass12345',
        })
        self.assertEqual(User.objects.count(), 1)
    
    def test_user_login(self):
        """Test user can login"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post(reverse('history:login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)  # Redirects after login