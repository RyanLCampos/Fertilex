import pickle
import os
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DadosForm
from .models import Previsao
from django.forms import formset_factory
from sklearn.preprocessing import StandardScaler
from django.contrib.auth.decorators import login_required

PrevisaoFormSet = formset_factory(DadosForm, extra=0)

def pre_processamento(dados):
    # Aplicar o pré-processamento aos dados de entrada

    script_dir = os.path.dirname(__file__)

    # Caminho para o arquivo do modelo (a partir do diretório do script)
    scaler_path = os.path.join(script_dir, '../Model e data/scaler.sav')

    with open(scaler_path, 'rb') as arquivo_scaler:
        scaler = pickle.load(arquivo_scaler)

    dados_normalizados = scaler.transform(dados)
    return dados_normalizados

from django.shortcuts import render, get_object_or_404
from .models import Previsao  # Importe o modelo Previsao
import numpy as np
import pickle
import os

@login_required
def prever(request, previsao_id=None):
    num_rows = int(request.POST.get('num_rows', 0))
    previsao = None  # Inicialize a previsao como None por padrão
    resultados = []

    if previsao_id is not None:
        # Se um previsao_id foi fornecido, recupere a previsão existente
        previsao = get_object_or_404(Previsao, id=previsao_id, usuario=request.user)

    if request.method == 'POST':
        dados = []

        # Preencha as listas com os valores dos campos
        for i in range(num_rows):
            row = [
                float(request.POST.getlist(f'N[]')[i] or 0),  # Trata campos nulos como 0
                float(request.POST.getlist(f'P[]')[i] or 0),
                float(request.POST.getlist(f'K[]')[i] or 0),
                float(request.POST.getlist(f'pH[]')[i] or 0),
                float(request.POST.getlist(f'EC[]')[i] or 0),
                float(request.POST.getlist(f'OC[]')[i] or 0),
                float(request.POST.getlist(f'S[]')[i] or 0),
                float(request.POST.getlist(f'Zn[]')[i] or 0),
                float(request.POST.getlist(f'Fe[]')[i] or 0),
                float(request.POST.getlist(f'Cu[]')[i] or 0),
                float(request.POST.getlist(f'Mn[]')[i] or 0)
            ]
            dados.append(row)

        dados_preprocessados = [pre_processamento([linha]) for linha in dados]
        dados_preprocessados = np.array(dados_preprocessados)
        
        modelo_path = os.path.join(os.path.dirname(__file__), '../Model e data/modelo_ml.sav')
        
        with open(modelo_path, 'rb') as modelo_arquivo:
            modelo = pickle.load(modelo_arquivo)

        resultados_modelo = [modelo.predict(linha.reshape(1, -1)) for linha in dados_preprocessados]

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
            # Atualize a previsão existente se previsao_id for fornecido
            previsao.usuario = usuario
            previsao.titulo = "Título da Previsão"  # Atualize o título conforme necessário
            previsao.dados_tabela = dados
            previsao.resultados = resultados
            previsao.save()
        else:
            # Crie uma nova previsão se previsao_id não for fornecido
            previsao = Previsao(
                usuario=usuario,
                titulo="Título da Previsão",
                dados_tabela=dados,
                resultados=resultados
            )
            previsao.save()

    # Recupere as previsões do usuário para exibição
    previsoes = Previsao.objects.filter(usuario=request.user)

    return render(request, 'app_fertilex/previsao.html', {'num_rows': num_rows, 'resultados': resultados, 'previsao': previsao, 'previsoes': previsoes})


@login_required
def resultados(request):
    # Recupere todas as previsões do usuário logado
    previsoes = Previsao.objects.filter(usuario=request.user)
    return render(request, 'app_fertilex/resultados.html', {'previsoes': previsoes})

@login_required
def excluir_previsao(request, previsao_id):
    previsao = get_object_or_404(Previsao, id=previsao_id, usuario=request.user)
    
    if request.method == 'POST':
        if previsao.usuario == request.user:
            previsao.delete()
            return redirect('app_fertilex:resultados')
    
    return render(request, 'app_fertilex/excluir_previsao.html', {'previsao': previsao})
