from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from applications.authentication.models import CustomUser
from .models import Domain, Experience, Region, Speciality


class CustomUserAdmin(UserAdmin):
    # Customize the fields displayed in the list view
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser',)
    readonly_fields = ("date_joined",)
    # Customize the fields displayed in the add/edit forms
    fieldsets = (
        ("Login element", {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'isClient', 'location', 'profile_img', 'cv_file', 'availability', 'region', 'domains')}),
        # ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Customize the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'isClient',
                'location',
                'profile_img',
                'cv_file',
                'availability',
                'region',
                'domains',
            ),
        }),
    )
    # Customize the search fields
    search_fields = ('email',)
    # Customize the ordering of records
    ordering = ('first_name',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Domain)
admin.site.register(Experience)
admin.site.register(Region)
admin.site.register(Speciality)
