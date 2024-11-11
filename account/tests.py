from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse('recipe:home_page'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('recipe:home_page'))

    def test_password_change_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('password_change'), {
            'old_password': 'testpass',
            'new_password1': 'newtestpass',
            'new_password2': 'newtestpass'
        })
        self.assertRedirects(response, reverse('password_change_done'))
        self.client.logout()
        login_response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'newtestpass'})
        self.assertRedirects(login_response, reverse('recipe:home_page'))


class RegisterViewTests(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post_valid_data(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass1234',
            'password2': 'newpass1234'
        })
        self.assertRedirects(response, reverse('recipe:home_page'))
        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists)

    def test_register_view_post_invalid_data(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass1234',
            'password2': 'wrongpassword'
        })

        user_exists = User.objects.filter(username='newuser').exists()
        self.assertFalse(user_exists)
        self.assertEqual(response.status_code, 200)
        form = response.context_data['form']
        self.assertTrue(form.errors.get('password2'))

    def test_register_view_post_missing_data(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': '',
            'password2': ''
        })

        user_exists = User.objects.filter(username='newuser').exists()
        self.assertFalse(user_exists)

        self.assertEqual(response.status_code, 200)
        form=response.context_data['form']
        self.assertTrue(form.errors.get('password1'))
        self.assertTrue(form.errors.get('password2'))



class UserRegistrationFormTests(TestCase):

    def test_valid_data(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass1234',
            'password2': 'newpass1234'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid()) 

    def test_mismatched_passwords(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass1234',
            'password2': 'wrongpassword'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid()) 
        self.assertIn('The two password fields didn’t match.', form.errors['password2'])
        
    def test_invalid_email(self):
        form_data = {
            'username': 'newuser',
            'email': 'notanemail',
            'password1': 'newpass1234',
            'password2': 'newpass1234'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', form.errors['email'])
        