from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Profile, Movie, Log, Profile
from django.urls import reverse
from django.utils import timezone
from django.contrib.messages import get_messages
from .forms import LogForm

User = get_user_model()

class UserProfileSignalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create groups
        cls.base_group = Group.objects.create(name='base')
        cls.business_group = Group.objects.create(name='business')

    def test_create_regular_user(self):
        '''
        When a regular user is created, it is connected to a newly created profile instance.
        The user is also added to the "base" group.
        '''
        user = User.objects.create_user(username='regular_user', password='password')
        # Check if profile is created
        self.assertTrue(Profile.objects.filter(user=user).exists())
        # Check if user is added to base group
        self.assertIn(user, self.base_group.user_set.all())

    def test_create_staff_user(self):
        '''
        A staff user does not have a profile associated and it is not contained in any group.
        '''
        user = User.objects.create_user(username='staff_user', password='password', is_staff=True)
        # Check if profile is not created
        self.assertFalse(Profile.objects.filter(user=user).exists())
        # Check if user is not added to base group
        self.assertNotIn(user, self.base_group.user_set.all())

    def test_create_superuser(self):
        '''
        A super user does not have a profile associated and it is not contained in any group.
        '''
        user = User.objects.create_superuser(username='superuser', password='password')
        # Check if profile is not created
        self.assertFalse(Profile.objects.filter(user=user).exists())
        # Check if user is not added to base group
        self.assertNotIn(user, self.base_group.user_set.all())

    '''
    def test_update_user_to_staff(self):
        user = User.objects.create_user(username='regular_user_update', password='password')
        user.is_staff = True
        user.save()
        self.assertFalse(Profile.objects.filter(user=user).exists())
        self.assertNotIn(user, self.base_group.user_set.all())

    def test_update_user_to_superuser(self):
        user = User.objects.create_user(username='regular_user_super', password='password')
        user.is_superuser = True
        user.save()
        self.assertFalse(Profile.objects.filter(user=user).exists())
        self.assertNotIn(user, self.base_group.user_set.all())
    '''


class AddLogViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create groups and add users to groups
        cls.base_group = Group.objects.create(name='base')
        cls.business_group = Group.objects.create(name='business')
        
        # Create users
        cls.user_base = User.objects.create_user(username='base_user', password='password')
        cls.user_business = User.objects.create_user(username='business_user', password='password')
        cls.user_no_group = User.objects.create_user(username='no_group_user', password='password', is_staff=True)

        cls.user_business.groups.remove(cls.base_group)
        cls.user_business.groups.add(cls.business_group)

        # Create movies
        cls.released_movie = Movie.objects.create(
            title='Released Movie', 
            plot='released movie',
            genres='released movie',
            director='released movie',
            cast='released movie',
            runtime=timezone.timedelta(seconds=1),
            release_date=timezone.now().date() - timezone.timedelta(days=1),
            production=Profile.objects.get(user=cls.user_business)
            )
        cls.unreleased_movie = Movie.objects.create(
            title='Unreleased Movie', 
            plot='unreleased movie',
            genres='unreleased movie',
            director='unreleased movie',
            cast='unreleased movie',
            runtime=timezone.timedelta(seconds=1),
            release_date=timezone.now().date() + timezone.timedelta(days=1),
            production=Profile.objects.get(user=cls.user_business)
            )

    def test_user_not_in_group(self):
        '''
        A user that is not in any group ("base" or "business") cannot log a movie.
        '''
        self.client.login(username='no_group_user', password='password')
        response = self.client.get(reverse('core:create_log', kwargs={'movie_pk': self.released_movie.pk}))
        self.assertRedirects(response, reverse('core:movie_page', kwargs={'pk': self.released_movie.pk}))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have permission to add a log for this movie.")

    def test_movie_not_released(self):
        '''
        A movie not yet released cannot be logged, but only watchlisted.
        '''
        self.client.login(username='base_user', password='password')
        response = self.client.get(reverse('core:create_log', kwargs={'movie_pk': self.unreleased_movie.pk}))
        self.assertRedirects(response, reverse('core:movie_page', kwargs={'pk': self.unreleased_movie.pk}))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You cannot log a movie that hasn't been released yet.")

    def test_valid_form_submission(self):
        '''
        Test for the valid form submission, the form data are sent using a POST request.
        '''
        self.client.login(username='base_user', password='password')
        form_data = {'like': True, 'just_watched': True}
        response = self.client.post(reverse('core:create_log', kwargs={'movie_pk': self.released_movie.pk}), form_data)
        self.assertRedirects(response, reverse('core:movie_page', kwargs={'pk': self.released_movie.pk}))
        self.assertTrue(Log.objects.filter(profile=self.user_base.profile, movie=self.released_movie).exists())

    def test_get_request_renders_form(self):
        '''
        A GET request triggers the rendering of the form.
        '''
        self.client.login(username='base_user', password='password')
        response = self.client.get(reverse('core:create_log', kwargs={'movie_pk': self.released_movie.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_log.html')
        self.assertIsInstance(response.context['form'], LogForm)
        self.assertEqual(response.context['movie'], self.released_movie)
