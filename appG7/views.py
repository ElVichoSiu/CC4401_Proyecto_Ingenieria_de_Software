from django.shortcuts import redirect, render
from appG7.models import User, Sesion
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Sala, Sesion, OpinionUser, Member
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, SesionFilterForm
from django.db.models import Count

def register_user(request):
    if request.method == 'GET': # Si estamos cargando la página
        return render(request, "appG7/register_user.html") # Mostrar el template

    elif request.method == 'POST': # Si estamos recibiendo el form de registro
        # Tomar los elementos del formulario que vienen en request.POST
        username = request.POST['username']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        contraseña = request.POST['contraseña']
        pronombre = request.POST['pronombre']
        mail = request.POST['mail']

        # Crear el nuevo usuario
        user = User.objects.create_user(username=username, first_name=nombre, last_name=apellido,password=contraseña, email=mail, pronombre=pronombre)
        messages.success(request, 'Se creó el usuario para ' + user.username)
        return HttpResponseRedirect('/')

@login_required(login_url='/login')
def index_page(request):
    form = SesionFilterForm(request.GET)
    sesiones = Sesion.objects.all()
    user = request.user

    if form.is_valid():
        ramo = form.cleaned_data.get('ramo')
        if ramo and ramo != 'all':
            sesiones = sesiones.filter(ramo=ramo)

    for sesion in sesiones:
        sesion.is_member = sesion.members.filter(id=user.id).exists()

    mis_sesiones = Sesion.objects.filter(members=user)

    context = {
        'form': form,
        'sesiones': sesiones,
        'mis_sesiones': mis_sesiones,
    }

    if request.method == 'GET':
        return render(request,"appG7/index.html", context)

@login_required(login_url='/login')
def estudio_page(request):
    if request.method == 'GET':
        return render(request,"appG7/sesion_estudio.html")
    elif request.method == 'POST': # Si estamos recibiendo el form de registro
    # Tomar los elementos del formulario que vienen en request.POST
        hora =  request.POST['hora']
        fecha =  request.POST['fecha']
        ramo =   request.POST.get( 'ramo')
        seccion =  request.POST['seccion']
        maxMembers = request.POST['max_members']
        descripcion = request.POST['descripcion']
        autor = request.user.username
        link=request.POST['link']
        # Crear el nuevo usuario
        sesion = Sesion.objects.create(autor=autor,
        hora=hora,
        fecha=fecha,
        ramo=ramo,
        seccion=seccion,
        maxMembers=maxMembers,
        descripcion = descripcion,
        link=link)

        messages.success(request, 'Se creó la nueva sesion de estudio para ' + sesion.autor)
        ubicacion = request.POST.get('lugares')  
        Sala.objects.create(sesion=sesion, ubicacion=ubicacion)

        return HttpResponseRedirect('/')

def login_user(request):
    if request.method == 'GET':
        return render(request,"appG7/login.html")
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['contraseña']
        usuario = authenticate(username=username,password=contraseña)
        if usuario is not None:
            login(request,usuario)
            return HttpResponseRedirect('/') # Redireccionar a la página de sesiones disponibles
        else:
            return HttpResponseRedirect('/register')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login')

def ver_sesiones(request):
    form = SesionFilterForm(request.GET)
    sesiones = Sesion.objects.annotate(num_members=Count('members'))
    # Nombre provisional del html donde se podrá ver el listado de las sesiones disponibles
    if form.is_valid():
        ramo = form.cleaned_data.get('ramo')
        if ramo and ramo != 'all':
            sesiones = sesiones.filter(ramo=ramo)

    context = {
        'form': form,
        'sesiones': sesiones,
    }

    return render(request, 'appG7/index.html', context)

@login_required(login_url='/login')
def opinion_usuario(request, critico_name, criticado_name):
    if request.method == 'GET':
        user = request.user
        return render(request,"appG7/opinion_usuario.html", {'user': user})

    if request.method == 'POST':
        id_criticado = criticado_name
        opinion = request.POST['opinion']
        puntualidad = request.POST['puntualidad']
        respeto = request.POST['respeto']
        instance1 = request.user
        instance2 = User.objects.get(username = id_criticado)
        OpinionUser.objects.create(id_critico=instance1, id_criticado=instance2, opinion=opinion, puntualidad=puntualidad, respeto=respeto)
        return HttpResponseRedirect('/perfil/' + str(instance2.username) + '/')

class UserProfile(View):
    def get(self, request, user_apodo):
        user = get_object_or_404(User, username=user_apodo)
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        opiniones = OpinionUser.objects.filter(id_criticado=user)

        context = {
            'user': user,
            'user_form': user_form,
            'profile_form': profile_form,
            'opiniones': opiniones
        }

        return render(request, 'appG7/perfil.html', context)

    def post(self, request, user_apodo):
        user = get_object_or_404(User, username=user_apodo)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(f'/perfil/{user.username}/')  

        opiniones = OpinionUser.objects.filter(id_criticado=user)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'opiniones': opiniones
        }

        return render(request, 'appG7/perfil.html', context)

@login_required(login_url='/login')
def unirse_sesion(request, session_id):
    sesion = get_object_or_404(Sesion, id=session_id)

    if sesion.members.count() >= sesion.maxMembers:
        messages.error(request, 'La sesión ya está llena.')
        return HttpResponseRedirect(f'/')

    Member.objects.get_or_create(id_user=request.user, id_host=sesion)
    messages.success(request, 'Te has unido a la sesión.')
    return HttpResponseRedirect(f'/')

@login_required(login_url='/login')
def salirse_sesion(request, session_id):
    sesion = get_object_or_404(Sesion, id=session_id)
    Member.objects.filter(id_user=request.user, id_host=sesion).delete()
    messages.success(request, 'Has dejado la sesión.')
    return HttpResponseRedirect(f'/')

@login_required(login_url='/login')
def mis_sesiones(request):
    user = request.user
    sesiones = Sesion.objects.filter(members=user)

    context = {
        'sesiones': sesiones,
    }

    return render(request, 'appG7/mis_sesiones.html', context)

@login_required(login_url='/login')
def detalle_sesion(request, session_id):
    sesion = get_object_or_404(Sesion, id=session_id)
    user = request.user

    context = {
        'sesion': sesion,
        'user': user,
    }

    return render(request, 'appG7/detalle_sesion.html', context)

@login_required(login_url='/login')
def expulsar_miembre(request, session_id, miembro_id):
    sesion = get_object_or_404(Sesion, id=session_id)
    miembro = get_object_or_404(User, id=miembro_id)
    Member.objects.filter(id_user=miembro, id_host=sesion).delete()
    return HttpResponseRedirect(f'/detalle_sesion/{session_id}/')

@login_required(login_url='/login')
def borrar_sesion(request, session_id):
    sesion = get_object_or_404(Sesion, id=session_id)
    sesion.delete()
    messages.success(request, 'Has eliminado la sesión.')
    return HttpResponseRedirect(f'/')