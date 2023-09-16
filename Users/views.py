from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.urls import reverse

# Create your views here.

def cadastrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('app_fertilex:prever_nova')  # Redirecionar para a página de análises
    else:
        form = UserCreationForm()
    return render(request, 'Users/cadastrar.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            url = reverse('app_fertilex:prever_nova')
            return redirect(url)
    else:
        form = AuthenticationForm()
    return render(request, 'Users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Logout realizado com sucesso!')
    return redirect('login')
