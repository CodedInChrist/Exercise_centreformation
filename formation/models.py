from django.db import models

class Salle(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    capacite = models.IntegerField() 
    description = models.TextField(blank=True, null=True)
    localisation = models.CharField(max_length=200, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

class Session(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    nombre_participants = models.IntegerField() 
    formateur = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)