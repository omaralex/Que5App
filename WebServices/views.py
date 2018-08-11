# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.db  import  IntegrityError ,  transaction 
import json
import sys
import random
from django.core import serializers
from Main.models import * 
from Process.models import *

from push_notifications.models import APNSDevice, GCMDevice
from django.db.models import Q
 
 
def get_all_users_view(request):
    exito = ''
    try:
        consulta = list(UsuariosExtra.objects.all())
        listaUsuarios = []
        for obj in consulta: 
            dataUsuarios={}
            dataUsuarios['usuario'] = obj.usuario.username
            listaUsuarios.append(dataUsuarios)
        print(listaUsuarios)
        exito = 'ok'
    except:
        exito = 'Error. '+str(sys.exc_info()[1])
    
    d= json.dumps({'respuesta':exito,'data':listaUsuarios})
    mimetype="application/json"
    return HttpResponse(d,mimetype) 

@transaction.atomic
def create_user_view(request):
    if  request.method == 'POST':
        if request.content_type == 'application/json':
            if request.body:
                data = json.loads(request.body.decode("utf-8")) 
                print(str(data))
                email_ = data['email']
                usuario_ = data['usuario']
                password_ = data['password']
                token_ = data['token']
                exito=''
                data = ''
                if usuario_ != None:
                    try:
                        with transaction.atomic():
                            if not User.objects.filter(username=usuario_).exists():
                                
                                user = User.objects.create_user(username=usuario_, email=email_, password=password_)
                                user.save()
                                
                                U = UsuariosExtra(usuario=user)
                                U.save()
                                
                                if GCMDevice.objects.filter(user=user.pk,registration_id=token_).exists():
                                    exito='ok'    
                                else:
                                    F = GCMDevice(name=usuario_,user=user,registration_id=token_,cloud_message_type="FCM",active=True)
                                    F.save()
                                   

                                exito = 'ok'
                                data = 'Registro exitoso'
                            else:
                                exito = 'error'
                                data = 'Ya existe otro usuario con este nombre' 
                            
                    except IntegrityError:
                        exito='error'
                        data = str(sys.exc_info()[1])
                    except:
                        exito='error'
                        data = str(sys.exc_info()[1])
            else:
                exito='error'
                data='No esta definido el body'
        else:
            exito='error'
            data='No esta definido la cabecera como json'
    else:
        exito='error'
        data='Solo esta definido el metodo POST'

    d= json.dumps({'respuesta':exito,'data':data})
    mimetype="application/json"
    return HttpResponse(d,mimetype) 
 

def login_view(request): 
    exito=''
    data = ''
    if  request.method == 'POST':
        if request.content_type == 'application/json':
            if request.body:
                dataJson = json.loads(request.body.decode("utf-8"))
                usuario_ = dataJson['usuario']
                password_ = dataJson['password']
                if usuario_ != None and password_!=None:
                    try:
                        with transaction.atomic():
                            if User.objects.filter(username=usuario_).exists() and check_password(password_):
                                exito = 'ok'
                                data = 'Logueo exitoso'
                            else:
                                exito = 'error'
                                data = 'El usuario o password no son correctos. Intentelo de nuevo' 
                            
                    except IntegrityError:
                        exito='error'
                        data = str(sys.exc_info()[1])
                    except:
                        exito='error'
                        data = str(sys.exc_info()[1])
            else:
                exito='error'
                data='No esta definido el body'
        else:
            exito='error'
            data='No esta definido la cabecera como json'
    else:
        exito='error'
        data='Solo esta definido el metodo POST'
    d= json.dumps({'respuesta':exito,'data':data})
    mimetype="application/json"
    return HttpResponse(d,mimetype) 


def questions_random_view(request):
    exito = '' 
    datoPregunta={}
    listaPregunta = []
    try:
        idPreguntaRandom = random.randint(1,len(list(Preguntas.objects.all().values('pk'))))
        OP = Preguntas.objects.get(pk=idPreguntaRandom,tieneAlternativas='SI') 
        consulta = list(Alternativas.objects.filter(idPregunta=OP.pk).values('pk','alternativaDescripcion'))
        datoPregunta['pk']= OP.pk
        datoPregunta['preguntaDescripcion'] = OP.preguntaDescripcion
        datoPregunta['alternativas']= consulta
        listaPregunta.append(datoPregunta)
        exito = 'ok'
    except:
        exito = 'Error. '+str(sys.exc_info()[1])
    
    d= json.dumps({'respuesta':exito,'data':listaPregunta})
    mimetype="application/json"
    return HttpResponse(d,mimetype) 

def send_message_view(request):
    exito=''
    data = ''
    if  request.method == 'POST':
        if request.content_type == 'application/json':
            if request.body:
                dataJson = json.loads(request.body.decode("utf-8"))
                print(dataJson)
                id_mensaje_ = dataJson['id_mensaje']
                mensaje_ = dataJson['mensaje']
                tipo_mensaje_ = dataJson['tipo_mensaje']
                timestamp_ = dataJson['timestamp']
                estado_mensaje_ = dataJson['estado_mensaje']
                id_e_ = dataJson['id_e']
                id_r_ = dataJson['id_r']
                id_g_ = dataJson['id_g']
                if id_g_=='-1':
                    CH = Chats(id=id_mensaje_,mensaje=mensaje_,tipo_mensaje=tipo_mensaje_,estado_mensaje='pendiente',id_e=id_e_,id_r=id_r_,timestamp=timestamp_)
                    CH.save()
                else:
                    CHG = ChatsGrupos(id=id_mensaje_,mensaje=mensaje_,tipo_mensaje=tipo_mensaje_,estado_mensaje='parcial',id_e=id_e_,id_g=id_g_,timestamp=timestamp_)
                    CHG.save()

                    consultaParticipantes = list(ParticipantesGrupo.objects.filter(id_g=id_g_).all())
                    for obj in consultaParticipantes:
                        if obj['id_r']!=id_e_:
                            OR = ReceptoresGrupo(id_r=obj['id_usuario'],id_chat_grupo=id_mensaje_,id_g=id_g_,tipo_mensaje=tipo_mensaje_,mensaje=mensaje_,estado_mensaje='pendiente')
                            OR.save()
                #OU = User.objects.get(username=id_r_)
                #devices = GCMDevice.objects.filter(user__pk=OU.pk).all()
                #print(devices)  

                #if UsuariosExtra.objects.filter(estado_notificacion=True,usuario__pk=OU.pk).exists():
                #    devices.send_message(message='Tiene mensajes pendientes de leer', use_fcm_notifications=False)
                
                #U = UsuariosExtra.objects.get(usuario__pk=OU.pk)
                #U.estado_notificacion=False
                #U.save()

                exito = 'ok'
                data=str(id_mensaje_)
            else:
                exito='error'
                data='No esta definido el body'
        else:
            exito='error'
            data='No esta definido la cabecera como json'
    else:
        exito='error'
        data='Solo esta definido el metodo POST'
    d= json.dumps({'respuesta':exito,'data':data})
    mimetype="application/json"
    return HttpResponse(d,mimetype)


def update_status_message_view(request):
    exito=''
    data = {}
    if  request.method == 'POST':
        if request.content_type == 'application/json':
            if request.body: 
                dataJson = json.loads(request.body.decode("utf-8"))
                id_mensaje_ = dataJson['id_mensaje'] 
                estado_mensaje_ = dataJson['estado_mensaje']

                OC = Chats.objects.get(id=id_mensaje_)
                OC.estado_mensaje = estado_mensaje_
                OC.save() 

                '''OU = User.objects.get(username=OC.id_e)
                print(str(OU))
                devices = GCMDevice.objects.filter(user__pk=OU.pk).all()
                print(devices)    
                devices.send_message(None, use_fcm_notifications=False,extra={"id_mensaje": str(id_mensaje_),"estado_mensaje": str(estado_mensaje_),"tipo":"actualizacion"})'''
                exito = 'ok'
                data['id_mensaje']=str(id_mensaje_)
                data['id_e']=str(OC.id_e)
            else:
                exito='error' 
        else:
            exito='error' 
    else:
        exito='error' 
    d= json.dumps({'respuesta':exito,'data':data})
    mimetype="application/json"
    return HttpResponse(d,mimetype)

def get_all_message_view(request):
    exito='' 
    dataMensajes={}
    if  request.method == 'POST':
        if request.content_type == 'application/json':
            if request.body: 
                dataJson = json.loads(request.body.decode("utf-8"))
                id_usuario_ = dataJson['id_usuario'] 
                dataMensajes['pendientes'] = []
                dataMensajes['entregados_vistos'] = []
                
                listaPendientes = []
                consultaPendientes=list(Chats.objects.filter(id_r=id_usuario_,estado_mensaje='pendiente').values('pk','mensaje','tipo_mensaje','estado_mensaje','id_e','id_r','timestamp'))
                consultaPendientesGrupos=list(ReceptoresGrupo.objects.filter(id_r=id_usuario_,estado_mensaje='pendiente').values('pk','id_r','id_chat_grupo','id_g','tipo_mensaje','mensaje','estado_mensaje'))

                print(str(consultaPendientes))

                for objPendientesChat in consultaPendientes:
                    dataPendientesChat = {}
                    dataPendientesChat['id_mensaje'] = objPendientesChat['pk']
                    dataPendientesChat['mensaje'] = objPendientesChat['mensaje']
                    dataPendientesChat['tipo_mensaje'] = objPendientesChat['tipo_mensaje'] 
                    dataPendientesChat['estado_mensaje'] = objPendientesChat['estado_mensaje'] 
                    dataPendientesChat['timestamp'] = objPendientesChat['timestamp'] 
                    dataPendientesChat['id_e'] = objPendientesChat['id_e'] 
                    dataPendientesChat['id_r'] = objPendientesChat['id_r']
                    dataPendientesChat['id_g'] = -1 
                    listaPendientes.append(dataPendientesChat)
                

                for objPendientesChatGrupo in consultaPendientesGrupos:
                    dataPendientesChatGrupo = {}
                    dataPendientesChatGrupo['id_mensaje'] = objPendientesChatGrupo['id_chat_grupo']
                    dataPendientesChatGrupo['mensaje'] = objPendientesChatGrupo['mensaje']
                    dataPendientesChatGrupo['tipo_mensaje'] = objPendientesChatGrupo['tipo_mensaje'] 
                    dataPendientesChatGrupo['estado_mensaje'] = objPendientesChatGrupo['estado_mensaje'] 
                    dataPendientesChatGrupo['timestamp'] = objPendientesChatGrupo['timestamp'] 
                    dataPendientesChatGrupo['id_g'] = objPendientesChatGrupo['id_g']
                    dataPendientesChat['id_e'] = -1 
                    dataPendientesChat['id_r'] = -1
                    listaPendientes.append(dataPendientesChatGrupo)

                listaEntregadosVistos = []
                consultaEntregadosVistos = list(Chats.objects.filter(Q(id_e=id_usuario_),Q(estado_mensaje='entregado')|Q(estado_mensaje='visto')).values('pk','mensaje','tipo_mensaje','estado_mensaje','id_e','id_r','timestamp'))
                consultaEntregadosVistosGrupo = list(ChatsGrupos.objects.filter(Q(id_e=id_usuario_),Q(estado_mensaje='parcial')).values('pk','mensaje','tipo_mensaje','estado_mensaje','id_e','id_g','timestamp'))

                for objEntregadosVistos in consultaEntregadosVistos:
                    dataMsjEntregadosVistos = {}
                    dataMsjEntregadosVistos['id_mensaje']=objEntregadosVistos['pk']
                    dataMsjEntregadosVistos['estado_mensaje']=objEntregadosVistos['estado_mensaje']
                    dataMsjEntregadosVistos['id_r']=objEntregadosVistos['id_r'] 
                    listaEntregadosVistos.append(dataMsjEntregadosVistos)
                
                for objEntregadosVistosGrupos in consultaEntregadosVistosGrupo:
                    consulta =  list(ParticipantesGrupo.objects.filter(Q(id_chat_grupo=objEntregadosVistosGrupos['pk']),Q(estado_mensaje='entregados')|Q(estado_mensaje='visto')).values('pk','id_usuario','id_g'))
                    for obj in consulta:
                        dataMsjEntregadosVistos = {}
                        dataMsjEntregadosVistos['id_mensaje']=obj['pk']
                        dataMsjEntregadosVistos['estado_mensaje']=obj['estado_mensaje']
                        dataMsjEntregadosVistos['id_r']=obj['id_r']
                        listaEntregadosVistos.append(dataMsjEntregadosVistos)

                
                dataMensajes['pendientes'] = listaPendientes
                dataMensajes['entregados_vistos'] = listaEntregadosVistos
                exito = 'ok' 
            else:
                exito='error' 
        else:
            exito='error' 
    else:
        exito='error'
    d= json.dumps({'respuesta':exito,'data':dataMensajes})
    mimetype="application/json"
    return HttpResponse(d,mimetype)


def push_notifications_view(request):
    exito = ''
    try:
        if request.method == "POST": 
            device =  GCMDevice.objects.all()
            print(device)
            device.send_message(message='4',extra={"title": "Notification title","nombre": "josue2222","prueba":"omar2222"})
            exito = 'ok'
    except:
        exito = 'Error. '+str(sys.exc_info()[1])
    
    d= json.dumps({'respuesta':exito})
    mimetype="application/json"
    return HttpResponse(d,mimetype) 


def register_token_view(request):
    exito=''
    data = ''
    if  request.method == 'POST':
        if request.content_type == 'application/json':
            if request.body:
                dataJson = json.loads(request.body.decode("utf-8"))
                usuario_ = dataJson['usuario']
                token_ = dataJson['token']
                tipo_ = dataJson['tipo']
                if usuario_ != None and token_!=None:
                    try:
                        with transaction.atomic():
                            if FCMDevice.objects.filter(name=usuario_,registration_id=token_).exists():
                                exito = 'ok'
                                data = 'ya se registro el token para este usuario'
                            else:
                                F = FCMDevice(name=usuario_,registration_id=token_,type=tipo_)
                                F.save()
                                exito = 'ok'
                                data = 'se registro correctamente el usuario con el token' 
                            
                    except IntegrityError:
                        exito='error'
                        data = str(sys.exc_info()[1])
                    except:
                        exito='error'
                        data = str(sys.exc_info()[1])
            else:
                exito='error'
                data='No esta definido el body'
        else:
            exito='error'
            data='No esta definido la cabecera como json'
    else:
        exito='error'
        data='Solo esta definido el metodo POST'
    d= json.dumps({'respuesta':exito,'data':data})
    mimetype="application/json"
    return HttpResponse(d,mimetype) 