from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, CustomUserChangeForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


class ProfileView(CreateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('home')
    template_name = 'profile.html'


def edit_profile(request, *args, **kwargs):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserChangeForm(instance=request.user)
        args = {'form': form}
        return render(request, 'profile.html', args)
