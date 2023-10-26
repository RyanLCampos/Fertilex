import pickle
import os
import locale
from django.http import HttpResponse
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from .models import Previsao, ConfiguracaoPrevisao
from django.forms import formset_factory
from sklearn.preprocessing import StandardScaler
from django.contrib.auth.decorators import login_required
from .Modelo.model_ml import treinar_modelo
import pandas as pd


def realizar_scaler(dados):
    script_dir = os.path.dirname(__file__)

    if isinstance(dados[0], dict):
        dados = [list(item.values()) for item in dados]

    scaler_path = os.path.join(script_dir, './Modelo/scaler.sav')

    with open(scaler_path, 'rb') as arquivo_scaler:
        scaler = pickle.load(arquivo_scaler)

    dados_normalizados = scaler.transform(dados)
    return dados_normalizados

@login_required
def prever_nova(request):
    num_rows = int(request.POST.get('num_rows', 0))
    titulo = request.POST.get('titulo', '')
    scalerNP = request.POST.get('ScalerNP', '')
    smote = request.POST.get('smote', '')
    previsao = None
    colunas = ["N", "P", "K", "pH", "EC", "OC", "S", "Zn", "Fe", "Cu", "Mn"]

    if request.method == 'POST':
        dados = []
        colunas_selecionadas = request.POST.getlist('colunas_selecionadas')
        print(colunas_selecionadas) # Teste

        if "default" in colunas_selecionadas:
            colunas_selecionadas = ["N", "P", "K", "pH", "EC", "OC", "S", "Zn", "Fe", "Cu", "Mn"]

        for i in range(num_rows):
            row = {}
            for col in colunas_selecionadas:
                valor = float(request.POST.getlist(f'{col}[]')[i] or 0)
                row[col] = valor
            dados.append(row)

        print(dados) # Teste
        
        # Chama a função treinar_modelo passando a solicitação e a opção de scaler
        treinar_modelo(colunas_selecionadas, smote)
        dados_df = pd.DataFrame(dados, columns=colunas_selecionadas)

        if scalerNP != '':
            script_dir = os.path.dirname(__file__)
            scaler_path = os.path.join(script_dir, './Modelo/scaler.sav')

            with open(scaler_path, 'rb') as arquivo_scaler:
                scaler = pickle.load(arquivo_scaler)

            dados_preprocessados = scaler.transform(dados_df)
        else:
            dados_preprocessados = dados_df.values
            

        
        print("Dados Processados", dados_preprocessados) # Teste
        scalerNP = scalerNP.lower() == 'on'
        smote = smote.lower() == 'on'
        print("Smote: ", smote) # Teste
        print("Scaler: ", scalerNP) # Teste

        modelo_path = os.path.join(os.path.dirname(__file__), './Modelo/modelo_ml.sav')
        
        with open(modelo_path, 'rb') as modelo_arquivo:
            modelo = pickle.load(modelo_arquivo)

        resultados_modelo = [modelo.predict(np.array(linha).reshape(1, -1)) for linha in dados_preprocessados]


        # Cria uma nova lista de resultados para esta previsão
        resultados = []

        for r in resultados_modelo:
            if r == 0:
                resultado_legivel = "Baixa"
            elif r == 1:
                resultado_legivel = "Média"
            elif r == 2:
                resultado_legivel = "Alta"
            else:
                resultado_legivel = "Desconhecida"
            resultados.append(resultado_legivel)

        usuario = request.user  # Obtém o usuário logado

        if previsao is not None:
            # Atualiza a previsão existente se previsao_id for fornecido
            previsao.usuario = usuario
            previsao.titulo = titulo
            previsao.dados_tabela = dados_df.to_dict(orient='records')
            previsao.resultados = resultados
            previsao.configuracao.num_linhas = num_rows
            previsao.configuracao.standard_scaler = scalerNP
            previsao.configuracao.smote = smote
            previsao.configuracao.colunas_selecionadas = colunas_selecionadas
            previsao.configuracao.save()
            previsao.save()
        else:
            # Cria uma nova previsão se previsao_id não for fornecido
            configuracao = ConfiguracaoPrevisao.objects.create(num_linhas=num_rows, standard_scaler=scalerNP, smote=smote, colunas_selecionadas=colunas_selecionadas)
            previsao = Previsao(
                usuario=usuario,
                titulo=titulo,
                dados_tabela=dados_df.to_dict(orient='records'),
                resultados=resultados,
                configuracao=configuracao
            )
            previsao.save()

            # Após criar a nova previsão, vai obter o ID dela
            nova_previsao_id = previsao.id

            # Redireciona o usuário para a página de previsão da nova previsão
            return redirect('app_fertilex:prever_atualizar', previsao_id=nova_previsao_id)

    # Recupera as previsões do usuário para exibição
    previsoes = Previsao.objects.filter(usuario=request.user)

    return render(request, 'app_fertilex/criar_previsao.html', {'num_rows': num_rows, 'previsao': previsao, 'previsoes': previsoes, 'colunas': colunas})

@login_required
def prever_atualizar(request, previsao_id):
    num_rows = int(request.POST.get('num_rows', 0))
    titulo = request.POST.get('titulo', '')
    previsao = None
    scalerNP = request.POST.get('ScalerNP', '')
    smote = request.POST.get('smote', '')
    colunas = ["N", "P", "K", "pH", "EC", "OC", "S", "Zn", "Fe", "Cu", "Mn"]
    dados = []

    colunas_selecionadas = request.POST.getlist('colunas_selecionadas')

    if "default" in colunas_selecionadas:
        colunas_selecionadas = ["N", "P", "K", "pH", "EC", "OC", "S", "Zn", "Fe", "Cu", "Mn"]

    if previsao_id is not None:
        # Se um previsao_id foi fornecido, recupera a previsão existente
        previsao = get_object_or_404(Previsao, id=previsao_id, usuario=request.user)

    if request.method == 'POST':

        # Preencha as listas com os valores dos campos
        for i in range(num_rows):
            row = {}
            for col in colunas_selecionadas:
                values = request.POST.getlist(f'{col}[]')
                
                # Verifica se o índice é válido antes de acessar a lista
                if i < len(values):
                    valor = float(values[i] or 0)
                    row[col] = valor
                else:
                    row[col] = 0  # Ou qualquer valor padrão desejado se o índice não for válido

            dados.append(row)

        # Chama a função treinar_modelo passando a solicitação e a opção de scaler
        treinar_modelo(colunas_selecionadas, smote)
        dados_df = pd.DataFrame(dados, columns=colunas_selecionadas)

        if scalerNP != '':
            script_dir = os.path.dirname(__file__)
            scaler_path = os.path.join(script_dir, './Modelo/scaler.sav')

            with open(scaler_path, 'rb') as arquivo_scaler:
                scaler = pickle.load(arquivo_scaler)
                
            dados_preprocessados = scaler.transform(dados_df)
        else:
            dados_preprocessados = dados

        
        scalerNP = scalerNP.lower() == 'on'
        smote = smote.lower() == 'on'
        print("Smote: ", smote)

        modelo_path = os.path.join(os.path.dirname(__file__), './Modelo/modelo_ml.sav')
        
        with open(modelo_path, 'rb') as modelo_arquivo:
            modelo = pickle.load(modelo_arquivo)
            
        dados_preprocessados = [list(linha.values()) if isinstance(linha, dict) else linha for linha in dados_preprocessados]
        resultados_modelo = [modelo.predict(np.array(linha).reshape(1, -1)) for linha in dados_preprocessados]

        resultados = []  # Cria uma nova lista de resultados para esta previsão

        for r in resultados_modelo:
            if r == 0:
                resultado_legivel = "Baixa"
            elif r == 1:
                resultado_legivel = "Média"
            elif r == 2:
                resultado_legivel = "Alta"
            else:
                resultado_legivel = "Desconhecida"
            resultados.append(resultado_legivel)

        usuario = request.user  # Obtém o usuário logado
        print(scalerNP)

        if previsao is not None:
            # Atualiza a previsão existente se previsao_id for fornecido
            previsao.usuario = usuario
            previsao.titulo = titulo
            previsao.dados_tabela = dados
            previsao.resultados = resultados
            previsao.configuracao.num_linhas = num_rows
            previsao.configuracao.standard_scaler = scalerNP
            previsao.configuracao.smote = smote
            previsao.configuracao.colunas_selecionadas = colunas_selecionadas
            previsao.configuracao.save()
            previsao.save()
            

            return redirect('app_fertilex:prever_atualizar', previsao_id=previsao_id)

    # Recarregue a previsão com os resultados atualizados
    if previsao_id is not None:
        previsao = Previsao.objects.get(id=previsao_id)

    # Recupera as previsões do usuário para exibição
    previsoes = Previsao.objects.filter(usuario=request.user)
    num_rows_list = range(num_rows)

    contexto = {
        'num_rows': previsao.configuracao.num_linhas, 
        'previsao': previsao, 
        'previsoes': previsoes, 
        'num_rows_list': num_rows_list, 
        'dados': previsao.dados_tabela,
        'scaler_checked': previsao.configuracao.standard_scaler,
        'smote_checked': previsao.configuracao.smote,
        'colunas_selecionadas': previsao.configuracao.colunas_selecionadas,
        'colunas': colunas
    }
    
    return render(request, 'app_fertilex/previsao.html', contexto)

def limpar_dados(request, previsao_id):
    # Recupera a previsão com base no ID fornecido
    previsao = get_object_or_404(Previsao, id=previsao_id, usuario=request.user)
    
    # Limpa os dados da tabela e os resultados
    previsao.dados_tabela = []
    previsao.resultados = []
    previsao.save()

    # Redireciona de volta à página de previsão com os dados limpos
    return redirect('app_fertilex:prever_atualizar', previsao_id=previsao_id)

# def limpar_dados(request, previsao_id):
#     # Recupera a previsão com base no ID fornecido
#     previsao = get_object_or_404(Previsao, id=previsao_id, usuario=request.user)

#     # Limpa os dados da tabela e os resultados
#     previsao.dados_tabela = []
#     previsao.resultados = []
#     previsao.save()

#     # Redireciona de volta à página de previsão com os dados limpos
#     return redirect('app_fertilex:prever_atualizar', previsao_id=previsao_id)
    

@login_required
def resultados(request):
    p = request.GET.get('p', '')

    if p:
        previsoes = Previsao.objects.filter(usuario=request.user, titulo__icontains=p)
    
    # Caso contrário, retorne todas as previsões do usuário
    previsoes = Previsao.objects.filter(usuario=request.user)
    
    context = {
        'previsoes': previsoes,
        'query': p,
    }
    
    return render(request, 'app_fertilex/resultados.html', context)

@login_required
def excluir_previsao(request, previsao_id):
    previsao = get_object_or_404(Previsao, id=previsao_id, usuario=request.user)
    
    if request.method == 'POST':
        if previsao.usuario == request.user:
            previsao.delete()
            if previsao.configuracao:
                previsao.configuracao.delete()
                return redirect('app_fertilex:resultados')
    
    return render(request, 'app_fertilex/excluir_previsao.html', {'previsao': previsao})


@login_required
def pesquisar_previsao(request):
    
    if 'p' in request.GET:
        p = request.GET['p']
        previsoes = Previsao.objects.filter(usuario=request.user, titulo__icontains=p)
    else:
        # Caso contrário, retorne todas as previsões do usuário
        previsoes = Previsao.objects.filter(usuario=request.user)

    context = {
        'previsoes': previsoes,
    }

    return render(request, 'app_fertilex/resultados.html', context)