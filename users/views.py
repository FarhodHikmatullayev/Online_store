from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from users.forms import CreateUserForm, ChangeProfileForm, MyAuthenticationForm


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, 'First, you should logout')
            return redirect('users:logout')
        form = MyAuthenticationForm()
        ctx = {
            'form': form,
        }
        return render(request, 'users/login.html', ctx)

    def post(self, request):
        form = MyAuthenticationForm(data=request.POST)
        ctx = {
            "form": form,
        }
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('product:list')
        messages.error(request, 'Any fields might be wrong, Please check and try again')
        return render(request, 'users/login.html', ctx)


class LogOutView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.warning(request, 'First, you should login')
            return redirect('users:login')
        logout(self.request)
        messages.success(request, 'You have successfully logged out')
        return redirect('users:login')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, 'First, you should logout')
            return redirect('users:logout')
        form = CreateUserForm()
        ctx = {
            'form': form
        }
        return render(request, 'users/register.html', ctx)

    def post(self, request):
        form = CreateUserForm(data=request.POST)
        ctx = {
            'form': form,
        }
        if form.is_valid():
            form.save()
            messages.success(request, "You successfully registered")
            return redirect('users:login')
        messages.error(request, 'Any fields might be wrong, Please check and try again')
        return render(request, 'users/register.html', ctx)


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        ctx = {
            'user': user,
        }
        return render(request, 'users/profile.html', ctx)


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ChangeProfileForm(instance=request.user)
        ctx = {
            'form': form,
        }
        return render(request, 'users/edit_profile.html', ctx)

    def post(self, request):
        form = ChangeProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        ctx = {
            "form": form
        }
        if form.is_valid():
            form.save()
            messages.success(request, f"Profile has successfully edited")
            return redirect('users:profile')
        else:
            return render(request, 'users/edit_profile.html', ctx)
