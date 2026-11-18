from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileForm
from .models import CustomUser
from .decorators import role_required

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect('login')
        messages.error(request, "Please fix the errors below.")
    return render(request, 'accounts/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

@login_required
def dashboard_redirect(request):
    routes = {
        CustomUser.Role.ADMIN: 'admin_dashboard',
        CustomUser.Role.COORDINATOR: 'coordinator_dashboard',
        CustomUser.Role.ADVISER: 'adviser_dashboard',
    }
    return redirect(routes[request.user.role])

@role_required(CustomUser.Role.ADMIN)
def admin_dashboard(request):
    return render(request, 'accounts/dashboard_admin.html')

@role_required(CustomUser.Role.COORDINATOR)
def coordinator_dashboard(request):
    return render(request, 'accounts/dashboard_coordinator.html')

@role_required(CustomUser.Role.ADVISER)
def adviser_dashboard(request):
    return render(request, 'accounts/dashboard_adviser.html')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'u': request.user})

@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
        messages.error(request, "Please fix the errors below.")
    return render(request, 'accounts/profile_edit.html', {'form': form})