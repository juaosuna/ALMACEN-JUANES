from ast import Return
from contextlib import redirect_stderr
from email.message import EmailMessage
from multiprocessing import context
from django.db import  IntegrityError

from django.contrib.sites.shortcuts import get_current_site 
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


from django.shortcuts import render, redirect
from accounts.models import Account
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def registrarse(request):
    context={}
    if request.method == 'POST':
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        username = request.POST['username'] 
        email = request.POST['email']
        
        #validacion de campos
        ok = True
        if not email:
            context['alarma'] = 'Ingrese el correo electronico'
            ok = False
        if not password or len(password) < 5:
            context['alarma'] = 'Ingrese un password de cinco(5) o mas caracteres'
            ok = False
        if password != confirmPassword:
            context['alarma'] = '¡El password no coincide!'
            ok = False

        #todo ok
        if ok:
            existe = Account.objects.filter(email=email).exists()
            if not existe:
                user = Account.objects.create_user(first_name=username, last_name=username, username=username, email=email, password=password)
                try:
                    user.save()
                except:
                    user=None
                    return render(request,'resgistro.html',{'alarma': 'Ya existe el usuario '})
                
                
                context['alarma'] = 'Usuario guardado con exito!'
                
                #modulo para mensajes
                current_site = get_current_site(request)
                mail_subject = 'Por favor para activar su cuenta en el sistema de Almacen Juanes'

                body = render_to_string('verificacion_email.html',{

                    'user' : user,
                    'domain' : current_site,
                    'uid' : str(urlsafe_base64_encode(force_bytes(user.pk))),
                    'token' : default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject,body,to=[to_email])
                send_email.send()

                context = {
                    'mensaje' : 'Bienvenido' + username + '. Favor activar su cuenta en el enlace enviado a su correo.'
                }
                return redirect(login)
                
                
            else:
                context['alarma'] = '¡El correo ya existe!'

    return render(request, 'usuarios/registro.html', context)

#************************CONTROL DE INGRESO DE USUARIOS*********************
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email= email, password = password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'home.html')
        else:
            return render(request, 'usuarios/login.html', {'alarma' : 'Correo o password no valido'}) 

    else:
        return render((request), 'usuarios/login.html')
    
#********************* DESACTIVACION DEL USUARIO *************************
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

def activate(request, uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('registro')


def verContactenos(request):
    return render(request,'contactenos.html')