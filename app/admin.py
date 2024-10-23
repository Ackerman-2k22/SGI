from django.contrib import admin
from .models import Incidents
from .models import Clients
from django.utils import timezone
# Register your models here.


class AdminIncidents(admin.ModelAdmin):
    readonly_fields = ('assigned_agent', 'created_at', 'description', 'incident_number','resolved_at')
    list_display = ('id', 'client_username', 'description', 'category', 'created_at', 'status', 'assigned_agent', 'comment','resolved_at')
    list_filter = ('category', 'status', 'created_at', 'assigned_agent', 'client','resolved_at')
    search_fields = ('id', 'client__username', 'description', 'category', 'created_at', 'status', 'assigned_agent', 'comment','resolved_at')
    list_per_page = 10


    def save_model(self, request, obj, form, change):
    
        if obj.status == 'terminé' and not obj.resolved_at:
            obj.resolved_at = timezone.localtime(timezone.now())

        elif obj.status != 'terminé':
            obj.resolved_at = None

        if obj.status in ['en cours', 'terminé']:
            obj.assigned_agent = f"{request.user.first_name} {request.user.last_name}"
        elif obj.status == 'en attente':
            obj.assigned_agent = "non attribué"

        super().save_model(request, obj, form, change)

    def client_username(self, obj):
        return obj.client.username if obj.client else 'Client inconnu'
    client_username.short_description = 'Nom d\'utilisateur du client'

class AdminClients(admin.ModelAdmin):

    readonly_fields = ('username', 'phone_number')
    list_display = ('client_id', 'username', 'phone_number')
    search_fields = ('client_id', 'username', 'phone_number')

admin.site.register(Incidents, AdminIncidents) 

admin.site.register(Clients, AdminClients)

