from django.contrib import admin
from .models import Salle, Formateur, Session

admin.site.site_header = "Centre de Formation"

@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'capacite', 'localisation', 'createur')
    search_fields = ('nom', 'localisation')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.createur = request.user  # CORRIGÉ : 'createur'
        obj.save()

@admin.register(Formateur)
class FormateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialite')
    search_fields = ('user__username', 'user__first_name')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('titre', 'salle', 'formateur', 'date_debut', 'date_fin', 'createur')
    list_filter = ('salle', 'formateur')
    search_fields = ('titre', 'salle__nom')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.createur = request.user
        obj.save()
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(createur=request.user)