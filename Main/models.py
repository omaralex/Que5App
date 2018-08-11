# -*- coding: utf-8 -*-
from django.db import models 
from datetime import datetime
from time import time
from django.contrib.auth.models import User

def get_upload_file_name(instance,filename):
    instante=str(datetime.now()).replace(' ','').replace('-','_').replace(':','_').replace('.','_')
    return "%s_%s"%((instante+str(time())).replace('.','_'),filename)

class GrupoChat(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion = models.DateField("Fecha Creacion:",auto_now=True) 
    estado = models.BooleanField(verbose_name="Estado:",default=True) 
    foto = models.FileField(upload_to=get_upload_file_name)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Grupos Chats"
        verbose_name = "Grupo Chat"

    def __str__(self):
        return str(self.id)

class ParticipantesGrupo(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario =  models.CharField(max_length=10,default='') 
    id_g =  models.ForeignKey(GrupoChat, on_delete=models.CASCADE)  
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Participantes Grupos"
        verbose_name = "Participante Grupo"

    def __str__(self):
        return str(self.id)

class ChatsGrupos(models.Model): 
    id = models.CharField(max_length=100,primary_key=True)
    mensaje = models.CharField(max_length=500)
    tipo_mensaje = models.CharField(max_length=10)
    estado_mensaje =  models.CharField(max_length=10)
    id_e =  models.CharField(max_length=10,default='')
    id_g =  models.ForeignKey(GrupoChat, on_delete=models.CASCADE)
    timestamp = models.CharField(max_length=30)
    

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Chats Grupos"
        verbose_name = "Chat Grupo"

    def __str__(self):
        return str(self.id)

class Chats(models.Model): 
    id = models.CharField(max_length=100,primary_key=True)
    mensaje = models.CharField(max_length=500)
    tipo_mensaje = models.CharField(max_length=10)
    estado_mensaje =  models.CharField(max_length=10)
    id_e =  models.CharField(max_length=10,default='')
    id_r =  models.CharField(max_length=10,default='')
    timestamp = models.CharField(max_length=30)
    

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Chats"
        verbose_name = "Chat"

    def __str__(self):
        return str(self.id)

class UsuariosExtra(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateField("Fecha Creacion:",auto_now=True)
    fecha_actualizacion = models.DateField("Fecha Actualizacion:",auto_now=True)
    estado = models.BooleanField(verbose_name="Estado:",default=True)
    estado_notificacion = models.BooleanField(verbose_name="Estado:",default=False)
    foto = models.FileField(upload_to=get_upload_file_name)

    class Meta:
        ordering = ["usuario"]
        verbose_name_plural = "Usuarios Extras"
        verbose_name = "Usuario Extra"

    def __str__(self):
        return str(self.usuario.username)


class ReceptoresGrupo(models.Model):
    id = models.AutoField(primary_key=True)
    id_r =  models.CharField(max_length=10,default='')
    id_chat_grupo =  models.ForeignKey(ChatsGrupos, on_delete=models.CASCADE,default=None)
    id_g =  models.ForeignKey(GrupoChat, on_delete=models.CASCADE)  
    tipo_mensaje = models.CharField(max_length=10) 
    mensaje = models.CharField(max_length=500)
    estado_mensaje =  models.CharField(max_length=10)
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Receptores Grupos"
        verbose_name = "Receptores Grupo"

    def __str__(self):
        return str(self.id)


 