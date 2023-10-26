from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from .forms import RegistrationForm, AtualizarDados, AtualizarDadosPerfil
from django.contrib.auth.decorators import login_required

# Create your views here.

# Função para Cadastrar Usuario
def cadastrar(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('app_fertilex:resultados')
    else:
        form = RegistrationForm()
    return render(request, 'Users/cadastrar.html', {'form': form})

# Função para realizar a autenticação e login do usuario
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            url = reverse('app_fertilex:resultados')
            return redirect(url)
    else:
        form = AuthenticationForm()
    return render(request, 'Users/login.html', {'form': form})


# Função para deslogar o usuario.
def logout_view(request):
    logout(request)
    messages.info(request, 'Logout realizado com sucesso!')
    return redirect('Users:login')

@login_required
def perfil(request):
    if request.method == 'POST':
        u_form = AtualizarDados(request.POST, instance=request.user)
        p_form = AtualizarDadosPerfil(request.POST, request.FILES ,instance=request.user.perfil)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Sua conta foi atualizada com sucesso!')
            return redirect('/perfil')

    else:
        u_form = AtualizarDados(instance=request.user)
        p_form = AtualizarDadosPerfil(instance=request.user.perfil)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'Users/perfil.html', context)