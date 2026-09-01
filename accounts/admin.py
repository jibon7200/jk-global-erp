from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """
    Customizes how the User model appears in Django's built-in Admin Panel
    (accessible at /admin/). This lets Jibon manage users easily
    without needing custom code for basic user management.
    """

    model = User

    list_display = ('username', 'email', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('JK Global Role Info', {'fields': ('role', 'phone_number')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('JK Global Role Info', {'fields': ('role', 'phone_number')}),
    )


admin.site.register(User, CustomUserAdmin)

admin.site.site_header = "JK GLOBAL Administration"
admin.site.site_title = "JK GLOBAL Admin Portal"
admin.site.index_title = "Welcome to JK GLOBAL — Managing Director: Jibon"
