"""
Model tests for Django v4.1 test project app.
"""

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import reverse
from django.test import TestCase

# Internal Imports.
from test_app.models import UserProfile


class ModelTestCase(TestCase):
    """Tests for app models."""

    @classmethod
    def setUpTestData(cls):
        """Set up testing data."""
        # Call parent logic.
        super().setUpTestData()

        # Generate user models.
        cls.test_super_user = get_user_model().objects.create(
            username='test_superuser',
            first_name='SuperUserFirst',
            last_name='SuperUserLast',
            is_superuser=True,
            is_staff=False,
            is_active=True,
        )
        cls.test_admin_user = get_user_model().objects.create(
            username='test_admin',
            first_name='AdminUserFirst',
            last_name='AdminUserLast',
            is_superuser=False,
            is_staff=True,
            is_active=True,
        )
        cls.test_inactive_user = get_user_model().objects.create(
            username='test_inactive',
            first_name='InactiveUserFirst',
            last_name='InactiveUserLast',
            is_superuser=False,
            is_staff=False,
            is_active=False,
        )
        cls.test_standard_user = get_user_model().objects.create(
            username='test_user',
            first_name='UserFirst',
            last_name='UserLast',
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )

    def debug_data(self, response):
        print('\n\n\n\n')
        self.display_content(response)
        print('\n\n')
        self.display_context(response)
        print('\n\n')
        self.display_session()
        print('\n\n\n\n')

    def display_content(self, response):
        """Prints out all page content to terminal."""
        print('{0} {1} {0}'.format('=' * 10, 'response.content'))

        print(response.content.decode('utf-8'))

    def display_context(self, response):
        """Prints out all context values to terminal."""
        print('{0} {1} {0}'.format('=' * 10, 'response.context'))

        for key in response.context.keys():
            context_value = str(response.context.get(key))
            # Truncate display if very long.
            if len(context_value) > 80:
                context_value = '"{0}"..."{1}"'.format(context_value[:40], context_value[-40:])
            print('    * {0}: {1}'.format(key, context_value))

    def display_session(self):
        """Prints out all session values to terminal."""
        print('{0} {1} {0}'.format('=' * 10, 'client.session'))

        for key, value in self.client.session.items():
            print('    * {0}: {1}'.format(key, value))

    def test__user_model_creation(self):
        """Verifies that expected user model properly generates."""
        with self.subTest('Check user creation using super user'):
            self.assertIsNotNone(self.test_super_user.profile)

            # Get corresponding auto-created profile model.
            user_profile = UserProfile.objects.get(user=self.test_super_user)
            self.assertEqual(user_profile, self.test_super_user.profile)

        with self.subTest('Check user creation using admin user'):
            self.assertIsNotNone(self.test_admin_user.profile)

            # Get corresponding auto-created profile model.
            user_profile = UserProfile.objects.get(user=self.test_admin_user)
            self.assertEqual(user_profile, self.test_admin_user.profile)

        with self.subTest('Check user creation using inactive user'):
            self.assertIsNotNone(self.test_inactive_user.profile)

            # Get corresponding auto-created profile model.
            user_profile = UserProfile.objects.get(user=self.test_inactive_user)
            self.assertEqual(user_profile, self.test_inactive_user.profile)

        with self.subTest('Check user creation using standard user'):
            self.assertIsNotNone(self.test_standard_user.profile)

            # Get corresponding auto-created profile model.
            user_profile = UserProfile.objects.get(user=self.test_standard_user)
            self.assertEqual(user_profile, self.test_standard_user.profile)

        with self.subTest('Check user creation using new user'):
            new_user = get_user_model().objects.create(
                username='new_user',
                first_name='TestFirst',
                last_name='TestLast',
            )
            self.assertIsNotNone(new_user.profile)

            # Get corresponding auto-created profile model.
            user_profile = UserProfile.objects.get(user=new_user)
            self.assertEqual(user_profile, new_user.profile)

    def test__assert_login(self):
        """Verifies that expected user model properly logs in."""
        with self.subTest('Check login using super user'):
            self.client.force_login(self.test_super_user)
            response = self.client.get(reverse('test_app:index'))

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_super_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(self.test_super_user, response.wsgi_request.user)

            # Try again, to make sure that accessing any of the above values didn't somehow clear the client.
            self.assertEqual(self.test_super_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(self.test_super_user, response.wsgi_request.user)

        with self.subTest('Check login using admin user'):
            self.client.force_login(self.test_admin_user)
            response = self.client.get(reverse('test_app:index'))

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(self.test_admin_user, response.wsgi_request.user)

            # Try again, to make sure that accessing any of the above values didn't somehow clear the client.
            self.assertEqual(self.test_admin_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(self.test_admin_user, response.wsgi_request.user)

        with self.subTest('Check login using inactive user'):
            self.client.force_login(self.test_inactive_user)
            response = self.client.get(reverse('test_app:index'))

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Get response's lazy user object.
            uwsgi_user = response.wsgi_request.user
            if hasattr(uwsgi_user, '_wrapped') and hasattr(uwsgi_user, '_setup'):
                if uwsgi_user._wrapped.__class__ == object:
                    uwsgi_user._setup()
                uwsgi_user = uwsgi_user._wrapped

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_inactive_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertTrue(isinstance(uwsgi_user, AnonymousUser))
            self.assertFalse(isinstance(uwsgi_user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, uwsgi_user)

            # Try again, to make sure that accessing any of the above values didn't somehow clear the client.
            self.assertEqual(self.test_inactive_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertTrue(isinstance(uwsgi_user, AnonymousUser))
            self.assertFalse(isinstance(uwsgi_user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, uwsgi_user)

        with self.subTest('Check login using standard user'):
            self.client.force_login(self.test_standard_user)
            response = self.client.get(reverse('test_app:index'))

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_standard_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(self.test_standard_user, response.wsgi_request.user)

            # Try again, to make sure that accessing any of the above values didn't somehow clear the client.
            self.assertEqual(self.test_standard_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(self.test_standard_user, response.wsgi_request.user)

        with self.subTest('Check login using new user'):
            # Generate user model.
            new_user = get_user_model().objects.create(
                username='new_user',
                first_name='TestFirst',
                last_name='TestLast',
            )
            self.client.force_login(new_user)
            response = self.client.get(reverse('test_app:index'))

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertEqual(new_user, response.wsgi_request.user)

            # Try again, to make sure that accessing any of the above values didn't somehow clear the client.
            self.assertEqual(new_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertEqual(new_user, response.wsgi_request.user)
