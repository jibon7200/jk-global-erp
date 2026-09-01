from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Lets Jibon (Admin) upload/change the company logo and name
    directly from the Django Admin Panel at /admin/.
    """

    list_display = ('company_name', 'managing_director_name', 'updated_at')

    def has_add_permission(self, request):
        # Prevents creating more than one SiteSettings entry.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevents deleting the only settings entry.
        return False
