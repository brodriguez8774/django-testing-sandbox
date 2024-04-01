"""
View tests for Django REST test project app.

Uses ETC package logic to execute.
Should otherwise be fairly similar to the "base_tests", as a way to
double-check that the ETC package functions as expected.
"""

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django_expanded_test_cases import IntegrationTestCase


class ViewTestCase(IntegrationTestCase):
    """Tests for app views."""

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

    def test__assert_index_view(self):
        """Verifies that index view can be accessed as expected."""
        with self.subTest('Check views using super user'):
            # Get response object.
            response = self.assertGetResponse('test_app:index', user=self.test_superuser)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test App Index', page_content)

        with self.subTest('Check views using admin user'):
            # Get response object.
            response = self.assertGetResponse('test_app:index', user=self.test_admin)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test App Index', page_content)

        with self.subTest('Check views using inactive user'):
            # Get response object.
            response = self.assertGetResponse('test_app:index', user=self.test_inactive_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test App Index', page_content)

        with self.subTest('Check views using standard user'):
            # Get response object.
            response = self.assertGetResponse('test_app:index', user=self.test_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test App Index', page_content)

        with self.subTest('Check views using new user'):
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

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test App Index', page_content)

    def test__assert_login_view(self):
        """Verifies that login view can be accessed as expected."""
        with self.subTest('Check views without login'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_login_check', auto_login=False)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertIn('Please login to see this page.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using super user'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_login_check', user=self.test_superuser)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Login Check', page_content)
            self.assertIn('This view should require user login to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)

        with self.subTest('Check views using admin user'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_login_check', user=self.test_admin)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Login Check', page_content)
            self.assertIn('This view should require user login to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)

        with self.subTest('Check views using inactive user'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_login_check', user=self.test_inactive_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertIn('Please login to see this page.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using standard user'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_login_check', user=self.test_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Login Check', page_content)
            self.assertIn('This view should require user login to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)

        with self.subTest('Check views using new user'):
            # Generate user model.
            new_user = get_user_model().objects.create(
                username='new_user',
                first_name='TestFirst',
                last_name='TestLast',
            )

            # Get response object.
            response = self.assertGetResponse('test_app:view_with_login_check', user=new_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Login Check', page_content)
            self.assertIn('This view should require user login to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)

    def test__assert_permission_view(self):
        """Verifies that permission view can be accessed as expected."""

        # Create required permission.
        content_type = ContentType.objects.get_for_model(get_user_model())
        test_permission = Permission.objects.create(
            content_type=content_type,
            codename='test_permission',
            name='Test Permission',
        )

        with self.subTest('Check views without login'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_permission_check', auto_login=False)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertIn('Please login to see this page.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using super user - Without correct permission'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_permission_check', user=self.test_superuser)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Permission Check', page_content)
            self.assertIn('This view should require permission of "test_permission" to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)

        with self.subTest('Check views using super user - With correct permission'):
            # Add permission to user.
            self.test_superuser.user_permissions.add(test_permission)

            # Get response object.
            response = self.assertGetResponse('test_app:view_with_permission_check', user=self.test_superuser)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Permission Check', page_content)
            self.assertIn('This view should require permission of "test_permission" to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)

        with self.subTest('Check views using admin user - Without correct permission'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_permission_check', user=self.test_admin)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertNotIn('Please login to see this page.', page_content)
            self.assertIn('Your account doesn\'t have access to this page. To proceed,', page_content)
            self.assertIn('please login with an account that has access.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using admin user - With correct permission'):
            # Add permission to user.
            self.test_admin.user_permissions.add(test_permission)

            # Get response object.
            response = self.assertGetResponse('test_app:view_with_permission_check', user=self.test_admin)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Permission Check', page_content)
            self.assertIn('This view should require permission of "test_permission" to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)

        with self.subTest('Check views using inactive user - Without correct permission'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_permission_check', user=self.test_inactive_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertIn('Please login to see this page.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using inactive user - With correct permission'):
            # Add permission to user.
            self.test_inactive_user.user_permissions.add(test_permission)

            # Get response object.
            response = self.assertGetResponse('test_app:view_with_permission_check', user=self.test_inactive_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertIn('Please login to see this page.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using standard user - Without correct permission'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_permission_check', user=self.test_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertNotIn('Please login to see this page.', page_content)
            self.assertIn('Your account doesn\'t have access to this page. To proceed,', page_content)
            self.assertIn('please login with an account that has access.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using standard user - With correct permission'):
            # Add permission to user.
            self.test_user.user_permissions.add(test_permission)

            # Get response object.
            response = self.assertGetResponse('test_app:view_with_permission_check', user=self.test_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Permission Check', page_content)
            self.assertIn('This view should require permission of "test_permission" to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)

        with self.subTest('Check views using new user - Without correct permission'):
            # Generate user model.
            new_user = get_user_model().objects.create(
                username='new_user',
                first_name='TestFirst',
                last_name='TestLast',
            )

            # Get response object.
            response = self.assertGetResponse('test_app:view_with_permission_check', user=new_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertNotIn('Please login to see this page.', page_content)
            self.assertIn('Your account doesn\'t have access to this page. To proceed,', page_content)
            self.assertIn('please login with an account that has access.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using new user - With correct permission'):
            # Add permission to user.
            new_user.user_permissions.add(test_permission)

            # Get response object.
            response = self.assertGetResponse('test_app:view_with_permission_check', user=new_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Permission Check', page_content)
            self.assertIn('This view should require permission of "test_permission" to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)

    def test__assert_group_view(self):
        """Verifies that group view can be accessed as expected."""

        # Create required group.
        test_group = Group.objects.create(name='test_group')

        with self.subTest('Check views without login'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_group_check', auto_login=False)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertIn('Please login to see this page.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using super user - Without correct group'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_group_check', user=self.test_superuser)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Group Check', page_content)
            self.assertIn('This view should require group of "test_group" to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)

        with self.subTest('Check views using super user - With correct group'):
            # Add group to user.
            self.test_superuser.groups.add(test_group)

            # Get response object.
            response = self.assertGetResponse('test_app:view_with_group_check', user=self.test_superuser)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Group Check', page_content)
            self.assertIn('This view should require group of "test_group" to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)

        with self.subTest('Check views using admin user - Without correct group'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_group_check', user=self.test_admin)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertNotIn('Please login to see this page.', page_content)
            self.assertNotIn('Your account doesn\'t have access to this page. To proceed,', page_content)
            self.assertNotIn('please login with an account that has access.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using admin user - With correct group'):
            # Add group to user.
            self.test_admin.groups.add(test_group)

            # Get response object.
            response = self.assertGetResponse('test_app:view_with_group_check', user=self.test_admin)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Group Check', page_content)
            self.assertIn('This view should require group of "test_group" to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)

        with self.subTest('Check views using inactive user - Without correct group'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_group_check', user=self.test_inactive_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertIn('Please login to see this page.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using inactive user - With correct group'):
            # Add group to user.
            self.test_inactive_user.groups.add(test_group)

            # Get response object.
            response = self.assertGetResponse('test_app:view_with_group_check', user=self.test_inactive_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertIn('Please login to see this page.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using standard user - Without correct group'):
            # Get response object.
            response = self.assertGetResponse('test_app:view_with_group_check', user=self.test_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertNotIn('Please login to see this page.', page_content)
            self.assertNotIn('Your account doesn\'t have access to this page. To proceed,', page_content)
            self.assertNotIn('please login with an account that has access.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using standard user - With correct group'):
            # Add group to user.
            self.test_user.groups.add(test_group)

            # Get response object.
            response = self.assertGetResponse('test_app:view_with_group_check', user=self.test_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Group Check', page_content)
            self.assertIn('This view should require group of "test_group" to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)

        with self.subTest('Check views using new user - Without correct group'):
            # Generate user model.
            new_user = get_user_model().objects.create(
                username='new_user',
                first_name='TestFirst',
                last_name='TestLast',
            )

            # Get response object.
            response = self.assertGetResponse('test_app:view_with_group_check', user=new_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Login Page', page_content)
            self.assertIn('You need to login to continue.', page_content)
            self.assertNotIn('Please login to see this page.', page_content)
            self.assertNotIn('Your account doesn\'t have access to this page. To proceed,', page_content)
            self.assertNotIn('please login with an account that has access.', page_content)
            self.assertIn('Username:', page_content)
            self.assertIn('Password:', page_content)
            self.assertIn('login', page_content)

        with self.subTest('Check views using new user - With correct group'):
            # Add group to user.
            new_user.groups.add(test_group)

            # Get response object.
            response = self.assertGetResponse('test_app:view_with_group_check', user=new_user)

            # Display debug data to console on test failure.
            self.debug_data(response)

            # Various checks to ensure page is the one we expect.
            page_content = response.content.decode('utf-8')
            self.assertIn('Django REST - Test Group Check', page_content)
            self.assertIn('This view should require group of "test_group" to see.', page_content)
            self.assertIn('Back to Test App Views', page_content)
