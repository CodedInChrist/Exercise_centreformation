from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Salle(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=100, unique=True)
    capacite = models.PositiveIntegerField()
    localisation = models.CharField(max_length=200, blank=True)
    createur = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom} ({self.capacite} places)"

class Formateur(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialite = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Session(models.Model):
    id = models.BigAutoField(primary_key=True)
    titre = models.CharField(max_length=200)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    formateur = models.ForeignKey(Formateur, on_delete=models.CASCADE)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    nombre_participants = models.PositiveIntegerField()
    createur = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.date_fin <= self.date_debut:
            raise ValidationError("shiramwo umusi uri nyuma y'umusi wa mbere")
        
        if self.date_debut < timezone.now():
            raise ValidationError("uyo musi wararenganye")
        
        if self.nombre_participants > self.salle.capacite:
            raise ValidationError(f"Trop de participants pour {self.salle.nom}")
        
        conflits = Session.objects.filter(
            salle=self.salle,
            date_debut__lt=self.date_fin,
            date_fin__gt=self.date_debut
        )
        
        if self.pk:
            conflits = conflits.exclude(pk=self.pk)
        
        if conflits.exists():
            raise ValidationError("Salle yarafashwe")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.titre} - {self.salle.nom}"