from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages


# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("blog:post_list")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


def login_view(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            username_ = login_form.cleaned_data["username"]
            password_ = login_form.cleaned_data["password"]
            user = authenticate(username=username_, password=password_)
            print("Welcome to site....")

            if user is not None:
                login(request, user)
                return redirect("blog:post_list")
            else:
                messages.error(request, f"Register yourself...")
        else:
            messages.error(request, "Invalid username or password")

    else:
        login_form = AuthenticationForm()

    return render(request, "registration/login.html", {"form":login_form})