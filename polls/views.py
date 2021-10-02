from django.contrib import auth
from django.db.models.manager import EmptyManager
from django.shortcuts import render, redirect
from polls.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.http.response import Http404

#Função para redirecionar para a pagina de login
def login_user(request):
    return render (request, 'login.html')

#Função para deslogar
def logout_user(request):
    logout(request)
    return redirect('/')


#Função para autenticar o usuário
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            #Comando para retornar uma mensagem caso inserir usuario ou senha invalida
            messages.error(request, "Usuário ou senha inválidos")
 
    return redirect('/')   

#Função para listar os eventos
@login_required(login_url='/login/')
def lista_eventos (request):
    usuario = request.user
    data_atual = datetime.now()
    evento = Evento.objects.filter(usuario=usuario, data_evento__gt=data_atual)
    response = {'eventos':evento} 
    return render(request, 'agenda.html', response)


#Função para listar os eventos passados
@login_required(login_url='/login/')
def lista_passado (request):
    usuario = request.user
    data_atual = datetime.now()
    evento = Evento.objects.filter(usuario=usuario, data_evento__lt=data_atual)
    response = {'eventos':evento} 
    return render(request, 'passado.html', response)







#Função para redirecionar para pagina de cadastro de evento
@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados ['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)


#Função para salvar o novo evento inserido
@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.data_evento = data_evento
                evento.descricao = descricao
                try: 
                    evento.save()
                except Exception:
                    raise Http404()
        else:
            try:
                Evento.objects.create(titulo=titulo,
                data_evento=data_evento,
                descricao=descricao,
                usuario=usuario)
            except Exception:
                    raise Http404()    
    return redirect('/')

#Função para deletar dados
@login_required(login_url='/login/')  
def delete_evento(request, id_evento):
    usuario=request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()     
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()    
    return redirect('/')