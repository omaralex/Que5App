# -*- coding: utf-8 -*-
from django.db import models 
from datetime import datetime
from time import time

class Preguntas(models.Model):
    id = models.AutoField("id:", primary_key=True)
    preguntaDescripcion =models.CharField("Descripcion de la Pregunta:",max_length=500)
    tipoPregunta = models.CharField("Tipo de Pregunta:",max_length=10)
    tieneAlternativas = models.CharField("Tiene Alternativas:",max_length=10)
    fecha_creacion = models.DateField("Fecha Creacion:",auto_now=True)
    fecha_actualizacion = models.DateField("Fecha Actualizacion:",auto_now=True)
    estado = models.BooleanField(verbose_name="Estado:",default=True)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Preguntas"
        verbose_name = "Pregunta"

    def __str__(self):
        return str(self.preguntaDescripcion)

class Alternativas(models.Model):
    id = models.AutoField("id:", primary_key=True)
    idPregunta = models.ForeignKey(Preguntas,on_delete=models.CASCADE)
    alternativaDescripcion =models.CharField("Descripcion de la Pregunta:",max_length=500)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Alternativas"
        verbose_name = "Alternativa"

    def __str__(self):
        return str(self.alternativaDescripcion)

 