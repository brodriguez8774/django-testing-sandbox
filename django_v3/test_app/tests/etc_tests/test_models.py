"""
Model tests for Django v3.2 test project app.

Uses ETC package logic to execute.
Should otherwise be fairly similar to the "base_tests", as a way to
double-check that the ETC package functions as expected.
"""

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django_expanded_test_cases import IntegrationTestCase

# Internal Imports.
from test_app.models import UserProfile


class ModelTestCase(IntegrationTestCase):
    """Tests for app models."""

    @classmethod
    def setUpTestData(cls):
        """Set up testing data."""
        # Call parent logic.
        super().setUpTestData()

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

        try:
            if response.context is not None:
                for key in response.context.keys():
                    context_value = str(response.context.get(key))
                    # Truncate display if very long.
                    if len(context_value) > 80:
                        context_value = '"{0}"..."{1}"'.format(context_value[:40], context_value[-40:])
                    print('    * {0}: {1}'.format(key, context_value))
        except AttributeError:
            pass

    def display_session(self):
        """Prints out all session values to terminal."""
        print('{0} {1} {0}'.format('=' * 10, 'client.session'))

        for key, value in self.client.session.items():
            print('    * {0}: {1}'.format(key, value))

    def test__user_model_creation(self):
        """Verifies that expected user model properly generates."""
        with self.subTest('Check user creation using super user'):
            self.assertIsNotNone(self.test_superuser.profile)

            # Get corresponding auto-created profile model.
            user_profile = UserProfile.objects.get(user=self.test_superuser)
            self.assertEqual(user_profile, self.test_superuser.profile)

        with self.subTest('Check user creation using admin user'):
            self.assertIsNotNone(self.test_admin.profile)

            # Get corresponding auto-created profile model.
            user_profile = UserProfile.objects.get(user=self.test_admin)
            self.assertEqual(user_profile, self.test_admin.profile)

        with self.subTest('Check user creation using inactive user'):
            self.assertIsNotNone(self.test_inactive_user.profile)

            # Get corresponding auto-created profile model.
            user_profile = UserProfile.objects.get(user=self.test_inactive_user)
            self.assertEqual(user_profile, self.test_inactive_user.profile)

        with self.subTest('Check user creation using standard user'):
            self.assertIsNotNone(self.test_user.profile)

            # Get corresponding auto-created profile model.
            user_profile = UserProfile.objects.get(user=self.test_user)
            self.assertEqual(user_profile, self.test_user.profile)

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
            # Get response object.
            response = self.assertGetResponse('test_app:index', user=self.test_superuser)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_superuser.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.user)

            # Try again, to make sure that accessing any of the above values didn't somehow clear the client.
            self.assertEqual(self.test_superuser.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(self.test_superuser, response.wsgi_request.user)
            self.assertEqual(self.test_superuser, response.user)

        with self.subTest('Check login using admin user'):
            # Get response object.
            response = self.assertGetResponse('test_app:index', user=self.test_admin)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_admin.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.user)

            # Try again, to make sure that accessing any of the above values didn't somehow clear the client.
            self.assertEqual(self.test_admin.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(self.test_admin, response.wsgi_request.user)
            self.assertEqual(self.test_admin, response.user)

        with self.subTest('Check login using inactive user'):
            # Get response object.
            response = self.assertGetResponse('test_app:index', user=self.test_inactive_user)

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
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

            # Try again, to make sure that accessing any of the above values didn't somehow clear the client.
            self.assertEqual(self.test_inactive_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertTrue(isinstance(uwsgi_user, AnonymousUser))
            self.assertFalse(isinstance(uwsgi_user, get_user_model()))
            self.assertNotEqual(self.test_inactive_user, uwsgi_user)
            self.assertTrue(isinstance(response.user, AnonymousUser))
            self.assertFalse(isinstance(response.user, get_user_model()))

        with self.subTest('Check login using standard user'):
            # Get response object.
            response = self.assertGetResponse('test_app:index', user=self.test_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(self.test_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.user)

            # Try again, to make sure that accessing any of the above values didn't somehow clear the client.
            self.assertEqual(self.test_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(self.test_user, response.wsgi_request.user)
            self.assertEqual(self.test_user, response.user)

        with self.subTest('Check login using new user'):
            # Generate user model.
            new_user = get_user_model().objects.create(
                username='new_user',
                first_name='TestFirst',
                last_name='TestLast',
            )

            # Get response object.
            response = self.assertGetResponse('test_app:index', user=new_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks, of different ways to ensure expected user is logged in.
            self.assertEqual(new_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.user)

            # Try again, to make sure that accessing any of the above values didn't somehow clear the client.
            self.assertEqual(new_user.pk, int(self.client.session.get('_auth_user_id', None)))
            self.assertFalse(isinstance(response.wsgi_request.user, AnonymousUser))
            self.assertTrue(isinstance(response.wsgi_request.user, get_user_model()))
            self.assertEqual(new_user, response.wsgi_request.user)
            self.assertEqual(new_user, response.user)
