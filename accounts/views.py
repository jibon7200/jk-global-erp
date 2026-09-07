from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django import forms
from core.models import SiteSettings
from core.decorators import admin_required
from .models import User


class CustomLoginView(LoginView):
    """
    Custom login page for JK GLOBAL.
    Uses our own template (accounts/login.html) instead of Django's
    default plain login page, so we can show the company logo,
    branding, and a modern design.
    """
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.get_settings()
        return context

    def get_success_url(self):
        return '/dashboard/'


def custom_logout_view(request):
    """
    Logs the user out and sends them back to the login page
    with a clean, simple redirect (no confirmation page needed).
    """
    logout(request)
    return redirect('accounts:login')

class StaffUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), required=False, help_text="Leave blank to keep unchanged when editing.")

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'role', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'role': forms.Select(attrs={'class': 'form-input'}),
        }


def _base_context(request, active_menu):
    return {
        'site_settings': SiteSettings.get_settings(),
        'is_admin': request.user.is_admin_role(),
        'active_menu': active_menu,
    }


@login_required
@admin_required
def user_list_view(request):
    users = User.objects.all()
    context = _base_context(request, 'users')
    context['users'] = users
    return render(request, 'accounts/user_list.html', context)


@login_required
@admin_required
def user_add_view(request):
    if request.method == 'POST':
        form = StaffUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password') or User.objects.make_random_password()
            user.set_password(password)
            user.save()
            messages.success(request, f'User "{user.username}" created.')
            return redirect('accounts:user_list')
    else:
        form = StaffUserForm()

    context = _base_context(request, 'users')
    context['form'] = form
    return render(request, 'accounts/user_form.html', context)


@login_required
@admin_required
def user_edit_view(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = StaffUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, f'User "{user.username}" updated.')
            return redirect('accounts:user_list')
    else:
        form = StaffUserForm(instance=user)

    context = _base_context(request, 'users')
    context['form'] = form
    context['is_edit'] = True
    context['target_user'] = user
    return render(request, 'accounts/user_form.html', context)