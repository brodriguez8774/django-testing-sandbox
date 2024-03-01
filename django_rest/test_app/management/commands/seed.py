"""
Command to generate default project models.
"""

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Creates default project models.'

    def handle(self, *args, **kwargs):
        """
        The logic of the command.
        """
        self.generate_default_users()
        self.generate_permissions()

    def generate_default_users(self):
        """Generates default users to login with."""
        default_password = 'temppass2'

        try:
            super_user = get_user_model().objects.create(
                username='test_superuser',
                first_name='SuperUserFirst',
                last_name='SuperUserLast',
                is_superuser=True,
                is_staff=True,
                is_active=True,
            )
            super_user.set_password(default_password)
            super_user.save()
        except IntegrityError:
            pass

        try:
            admin_user = get_user_model().objects.create(
                username='test_admin',
                first_name='AdminUserFirst',
                last_name='AdminUserLast',
                is_superuser=False,
                is_staff=True,
                is_active=True,
            )
            admin_user.set_password(default_password)
            admin_user.save()
        except IntegrityError:
            pass

        try:
            inactive_user = get_user_model().objects.create(
                username='test_inactive',
                first_name='InactiveUserFirst',
                last_name='InactiveUserLast',
                is_superuser=False,
                is_staff=False,
                is_active=False,
            )
            inactive_user.set_password(default_password)
            inactive_user.save()
        except IntegrityError:
            pass

        try:
            standard_user = get_user_model().objects.create(
                username='test_user',
                first_name='UserFirst',
                last_name='UserLast',
                is_superuser=False,
                is_staff=False,
                is_active=True,
            )
            standard_user.set_password(default_password)
            standard_user.save()
        except IntegrityError:
            pass

    def generate_permissions(self):
        """Generates default general permission/groups."""
        try:
            content_type = ContentType.objects.get_for_model(get_user_model())
            test_permission = Permission.objects.create(
                content_type=content_type,
                codename='test_permission',
                name='Test Permission',
            )
        except IntegrityError:
            pass

        try:
            test_group = Group.objects.create(name='test_group')
        except IntegrityError:
            pass
