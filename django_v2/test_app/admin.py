"""
Admin views for Django v2.2 test project app.
"""

# Third-Party Imports.
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.sessions.models import Session


# region Admin Inlines

class GroupUserInline(admin.TabularInline):
    model = Group.user_set.through
    extra = 0


class PermissionGroupInline(admin.TabularInline):
    model = Permission.group_set.through
    extra = 0


class PermissionUserInline(admin.TabularInline):
    model = Permission.user_set.through
    extra = 0

# endregion Admin Inlines


# region Admin Definitions

class DjangoLogAdmin(admin.ModelAdmin):
    """
    Admin handling for Django's built-in admin view "LogEntry" models.
    """
    # Fields to display in admin list view.
    list_display = ('user', 'content_type', 'object_repr', 'action_time')
    if settings.DEBUG:
        list_display = ('id',) + list_display

    # Default field ordering in admin list view.
    ordering = ('-action_time', 'user__username', 'content_type')

    # Date filtering in admin list view.
    date_hierarchy = 'action_time'

    # Read only fields for admin detail view.
    readonly_fields = ('id', 'action_time')

    # Fieldset organization for admin detail view.
    fieldsets = (
        (None, {
            'fields': (
                'user',
                'content_type__app_label',
                'content_type__model',
                'object_id',
                'object_repr',
                'action_flag',
                'change_message',
            )
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('id', 'action_time')
        }),
    )


class DjangoUserAdmin(UserAdmin):
    """
    Admin handling for Django's built-in authentication "User" models.
    """
    # Fields to display in admin list view.
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active', 'last_login')
    if settings.DEBUG:
        list_display = ('id',) + list_display

    # Default field ordering in admin list view.
    ordering = ('username',)

    # Fields to filter by in admin list view.
    list_filter = ('is_active',)

    # Display many-to-many in more user-friendly format, in admin list view.
    filter_horizontal = ('user_permissions', 'groups',)

    # Read only fields for admin detail view.
    readonly_fields = ('id', 'date_joined', 'last_login')

    # Fieldset organization for admin detail view.
    fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'email', 'password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups', 'last_login'),
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('id', 'date_joined')
        }),
    )

    class Media:
        js = ['admin/js/list_filter_collapse.js']


class DjangoGroupAdmin(GroupAdmin):
    """
    Admin handling for Django's built-in permission "Group" models.
    """
    inlines = [GroupUserInline]

    # Fields to display in admin list view.
    list_display = ('name',)
    if settings.DEBUG:
        list_display = ('id',) + list_display

    # Default field ordering in admin list view.
    ordering = ('name',)

    # Display many-to-many in more user-friendly format, in admin list view.
    filter_horizontal = ('permissions',)

    # Read only fields for admin detail view.
    readonly_fields = ('id',)

    # Fieldset organization for admin detail view.
    fieldsets = (
        (None, {
            'fields': ('name', 'permissions')
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('id',)
        }),
    )


class DjangoPermissionAdmin(admin.ModelAdmin):
    """
    Admin handling for Django's built-in "Permission" models.
    """
    inlines = [PermissionGroupInline, PermissionUserInline]

    # Fields to display in admin list view.
    list_display = ('codename', 'name', 'content_type')
    if settings.DEBUG:
        list_display = ('id',) + list_display

    # Default field ordering in admin list view.
    ordering = ('content_type__app_label', 'content_type__model', 'name')

    # Read only fields for admin detail view.
    readonly_fields = ('id',)

    # Fieldset organization for admin detail view.
    fieldsets = (
        (None, {
            'fields': ('name', 'content_type', 'codename'),
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('id',)
        }),
    )


class DjangoSessionAdmin(admin.ModelAdmin):
    """
    Admin handling for Django's built-in "Session" models.
    """
    # Fields to display in admin list view.
    list_display = ('get_session_user', 'session_key', 'expire_date', 'is_valid')

    # Default ordering in admin views.
    ordering = ('-expire_date',)

    # Read only fields for admin detail view.
    readonly_fields = ('get_session_user', 'is_valid')

    # Fieldset organization for admin detail view.
    fieldsets = (
        (None, {
            'fields': ('get_session_user', 'session_key', 'session_data', 'expire_date', 'is_valid'),
        }),
    )

    def get_session_data(self, obj):
        """
        Alias for getting decoded session data.
        """
        # Decode our session data, or attempt to.
        return_val = obj.get_decoded()

        return return_val

    def is_valid(self, obj):
        """
        Returns bool indicating if session is corrupted or not.
        """
        if len(self.get_session_data(obj)) > 0:
            return True
        else:
            return False
    is_valid.boolean = True
    is_valid.short_description = 'Is Valid (Not Corrupted)'

    def get_session_user(self, obj):
        """
        Returns associated user model, or the string 'Anonymous' if session is corrupted or for a non-login.
        """
        try:
            user_id = self.get_session_data(obj)['_auth_user_id']
            return get_user_model().objects.get(id=user_id)
        except KeyError:
            return 'Anonymous'
    get_session_user.short_description = 'Session User'

# endregion Admin Definitions


# Register our updated admin views.
admin.site.unregister(Group)
admin.site.register(LogEntry, DjangoLogAdmin)
admin.site.register(get_user_model(), DjangoUserAdmin)
admin.site.register(Permission, DjangoPermissionAdmin)
admin.site.register(Group, DjangoGroupAdmin)
admin.site.register(Session, DjangoSessionAdmin)
